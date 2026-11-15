from playwright.sync_api import sync_playwright
from PIL import Image
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width":1280,"height":1000}, device_scale_factor=2)
    pg.goto("http://localhost:8765/"); pg.wait_for_timeout(1200)
    pg.locator("#ergebnis").scroll_into_view_if_needed(); pg.wait_for_timeout(2500)
    pg.add_style_tag(content="header.top{display:none!important}")
    el=pg.locator("#ergebnis"); bb=el.bounding_box()
    pg.screenshot(path="a-ergebnis.png", clip={"x":bb["x"],"y":bb["y"],"width":bb["width"],"height":min(bb["height"],560)})
    pg = b.new_page(viewport={"width":1280,"height":1000}, device_scale_factor=2)
    pg.goto("http://localhost:8765/pro/"); pg.wait_for_timeout(800)
    pg.add_style_tag(content="header.top{display:none!important}")
    for k,v in {"#f-pow":"9","#f-cap":"10","#f-total":"19000","#f-store":"6500","#f-plz":"47051","#f-cons":"4500"}.items(): pg.fill(k,v)
    f=pg.locator("#offer"); f.scroll_into_view_if_needed(); f.screenshot(path="a-form.png")
    pg.click("#go"); pg.wait_for_timeout(3000)
    t=pg.locator("#teaser"); t.scroll_into_view_if_needed(); pg.wait_for_timeout(500); t.screenshot(path="a-ampel.png")
    b.close()
for f in ["a-ergebnis","a-form","a-ampel"]: print(f, Image.open(f+".png").size)
