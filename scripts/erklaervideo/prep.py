import json,sys
tk=sys.argv[1]
real=lambda ws:[x for x in ws if x.get("type","word")=="word" and not x["text"].startswith("[") and not x["text"].endswith("]") and x["text"]!="…"]
old=real(json.load(open("words.json"))["words"]); new=real(json.load(open(f"words-{tk}.json"))["words"])
assert len(old)==len(new),(len(old),len(new))
for o,n in zip(old,new): assert o["text"].lower().strip(".,?!:")[:3]==n["text"].lower().strip(".,?!:")[:3] or o["text"][0].isalpha()!=n["text"][0].isalpha(), (o["text"],n["text"])
warp=[[n["start"],o["start"]] for o,n in zip(old,new)]
warp.append([new[-1]["end"],old[-1]["end"]])
subs=json.load(open("subs.json"))
# Untertitel auf neue Zeiten: über Wortindex
oi={round(o["start"],3):i for i,o in enumerate(old)}
out=[]
for s in subs:
    i=min(range(len(old)),key=lambda k:abs(old[k]["start"]-s["s"]))
    out.append({"t":s["t"],"i":i})
for k,s in enumerate(out):
    j=out[k+1]["i"]-1 if k+1<len(out) else len(new)-1
    s["s"]=new[s["i"]]["start"]; s["e"]=new[j]["end"]+0.3
for a,b in zip(out,out[1:]): a["e"]=min(a["e"],b["s"])
json.dump({"warp":warp,"subs":out,"end":new[-1]["end"]},open(f"time-{tk}.json","w"),ensure_ascii=False)
print(tk,"Ende",new[-1]["end"])
