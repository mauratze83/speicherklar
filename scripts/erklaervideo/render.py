import json, sys, subprocess, os
from playwright.sync_api import sync_playwright
mode=sys.argv[1]; tk=sys.argv[2]; TM=json.load(open(f"time-{tk}.json")); W,H=(1920,1080) if mode=="h" else (1080,1920)
FPS=30; OFF=0.4; END=TM["end"]+OFF+2.3
W2=TM["warp"]
def o2n(x):
    for (n0,o0),(n1,o1) in zip(W2,W2[1:]):
        if x<=o1: return n0+(x-o0)*(n1-n0)/max(1e-6,o1-o0)
    return x-W2[-1][1]+W2[-1][0]
cuts=[0]+[o2n(a)+OFF for a in (3.4,19.4,27.15,36.4,47.65,59.1,65.75,70.1)]+[END]
subs=TM["subs"]
os.makedirs(f"sc-{mode}-{tk}",exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":W,"height":H})
    pg.goto("file:///home/claude/vid/stage.html"+("#v" if mode=="v" else "")); pg.wait_for_timeout(1000)
    pg.evaluate("s=>setSubs(s)",subs); pg.evaluate("w=>setWarp(w)",W2)
    for k in range(len(cuts)-1):
        f0,f1=round(cuts[k]*FPS),round(cuts[k+1]*FPS)
        tmp=f"sc-{mode}-{tk}/s{k}.tmp.mp4"
        ff=subprocess.Popen(["ffmpeg","-loglevel","error","-y","-f","image2pipe","-framerate",str(FPS),"-c:v","mjpeg","-i","-",
            "-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","-r",str(FPS),tmp],stdin=subprocess.PIPE)
        for n in range(f0,f1):
            pg.evaluate(f"render({n/FPS})")
            ff.stdin.write(pg.screenshot(type="jpeg",quality=92))
        ff.stdin.close()
        if ff.wait()==0: os.rename(tmp,f"sc-{mode}-{tk}/s{k}.mp4")
        print(mode,"Szene",k,f1-f0,"Frames",flush=True)
    b.close()
