#!/usr/bin/env python3
from pathlib import Path
import markdown
from weasyprint import HTML

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "release" / "v0.1" / "AI时代的小岛经济学-V0.1.pdf"

PARTS = {
    1: "第一部：智能只是工具",
    4: "第二部：这一次，好像不一样",
    7: "第三部：谁控制真正的生产能力",
    11: "第四部：东西越来越多，人却越来越没钱",
    14: "第五部：旧的收入体系开始松动",
    17: "第六部：岛上开始重新发明分配制度",
    20: "第七部：钱没有消失，只是稀缺变了",
    23: "第八部：人终于开始问“我为什么还要工作”",
    27: "第九部：两座完全不同的AI小岛",
}

CSS = r'''
@page { size: 6in 9in; margin: 19mm 17mm 18mm 17mm; }
@page front { margin: 0; @top-left { content:none } @top-right { content:none } @bottom-center { content:none } }
@page toc { margin: 20mm 17mm 18mm 17mm; @top-left { content:none } @top-right { content:none } @bottom-center { content: counter(page); font: 8pt "Noto Sans CJK SC"; color:#888; } }
@page part { margin: 0; @top-left { content:none } @top-right { content:none } @bottom-center { content:none } }
@page body {
  margin: 19mm 17mm 18mm 17mm;
  @top-left { content: "AI时代的小岛经济学"; font: 7.5pt "Noto Sans CJK SC"; color:#999; letter-spacing:.06em; }
  @top-right { content: string(chapter); font: 7.5pt "Noto Sans CJK SC"; color:#999; }
  @bottom-center { content: counter(page); font: 8pt "Noto Sans CJK SC"; color:#888; }
}
html, body { margin:0; padding:0; }
body { font-family:"Noto Serif CJK SC","Noto Serif CJK JP",serif; color:#222; }
.front-page { page:front; width:6in; height:9in; page-break-after:always; }
.front-page img { width:6in; height:9in; object-fit:cover; display:block; }
.toc { page:toc; page-break-before:always; }
.toc h1 { font-size:25pt; font-weight:600; margin:0 0 14mm; letter-spacing:.08em; }
.toc .part-name { margin:7mm 0 3mm; font-family:"Noto Sans CJK SC"; font-size:9pt; color:#777; letter-spacing:.08em; }
.toc a { display:block; color:#222; text-decoration:none; font-size:10pt; line-height:1.65; margin:1.6mm 0; }
.toc a::after { content: leader("·") target-counter(attr(href), page); color:#888; }
.part { page:part; width:6in; height:9in; page-break-before:always; page-break-after:always; display:flex; flex-direction:column; justify-content:center; padding:0 22mm; box-sizing:border-box; background:#f5f1e8; }
.part .num { font-family:"Noto Sans CJK SC"; font-size:9pt; color:#9c8c70; letter-spacing:.2em; margin-bottom:9mm; }
.part h2 { font-size:26pt; line-height:1.35; font-weight:600; margin:0; letter-spacing:.03em; }
.part .rule { width:24mm; border-top:1px solid #a9987a; margin-top:12mm; }
.chapter { page:body; page-break-before:always; }
.chapter h1 { string-set: chapter content(); font-size:22pt; line-height:1.35; font-weight:600; margin:7mm 0 14mm; letter-spacing:.02em; }
.chapter .chapter-no { font-family:"Noto Sans CJK SC"; font-size:8pt; color:#9a8b72; letter-spacing:.18em; margin-bottom:4mm; }
.chapter h2 { font-family:"Noto Sans CJK SC"; font-size:12.5pt; line-height:1.45; margin:10mm 0 4mm; font-weight:600; page-break-after:avoid; }
.chapter p { font-size:10.4pt; line-height:1.92; margin:0 0 3.1mm; text-align:justify; text-indent:2em; orphans:2; widows:2; }
.chapter h2 + p, .chapter blockquote + p, .chapter hr + p { text-indent:0; }
.chapter blockquote { margin:7mm 4mm; padding:5mm 5mm; border-left:2px solid #b49b72; background:#faf7f1; font-size:11pt; line-height:1.75; }
.chapter blockquote p { margin:0; text-indent:0; font-weight:500; }
.chapter hr { border:0; width:14mm; border-top:1px solid #b9ad9a; margin:9mm auto; }
.chapter strong { font-weight:700; }
.epilogue h1 { font-size:24pt; }
'''

def split_title(md_text: str):
    lines = md_text.strip().splitlines()
    title = lines[0].lstrip('#').strip() if lines and lines[0].startswith('#') else ''
    body = '\n'.join(lines[1:]).lstrip() if title else md_text
    return title, body

def chapter_num(path: Path):
    return int(path.name.split('-',1)[0])

chapters = sorted((ROOT / 'chapters').glob('*.md'))
entries = []
for p in chapters:
    title, body = split_title(p.read_text(encoding='utf-8'))
    entries.append((chapter_num(p), title, body))

html = ['<!doctype html><html><head><meta charset="utf-8"><style>', CSS, '</style></head><body>']

for name in ['01-cover.png','02-title-page.png','03-copyright-page.png','04-epigraph-page.png','05-author-bio-page.png']:
    img = (ROOT / 'book-pages' / name).resolve().as_uri()
    html.append(f'<section class="front-page"><img src="{img}"></section>')

html.append('<section class="toc"><h1>目录</h1>')
html.append('<div class="part-name">序章</div>')
for n, title, _ in entries:
    if n == 0:
        html.append(f'<a href="#chapter-{n}">{title}</a>')
for start, part_title in PARTS.items():
    html.append(f'<div class="part-name">{part_title}</div>')
    next_starts = [x for x in PARTS if x > start]
    end = min(next_starts) if next_starts else 30
    for n, title, _ in entries:
        if start <= n < end and n <= 29:
            html.append(f'<a href="#chapter-{n}">{title}</a>')
html.append('<div class="part-name">终章</div>')
for n, title, _ in entries:
    if n == 30:
        html.append(f'<a href="#chapter-{n}">{title}</a>')
html.append('</section>')

for n, title, body in entries:
    if n in PARTS:
        part_title = PARTS[n]
        part_no, part_name = part_title.split('：',1)
        html.append(f'<section class="part"><div class="num">{part_no}</div><h2>{part_name}</h2><div class="rule"></div></section>')
    body_html = markdown.markdown(body, extensions=['extra','sane_lists'])
    if n == 0:
        label = '序章'
    elif n == 30:
        label = '终章'
    else:
        label = f'CHAPTER {n:02d}'
    cls = 'chapter epilogue' if n == 30 else 'chapter'
    html.append(f'<section class="{cls}" id="chapter-{n}"><div class="chapter-no">{label}</div><h1>{title}</h1>{body_html}</section>')

html.append('</body></html>')
OUT.parent.mkdir(parents=True, exist_ok=True)
HTML(string=''.join(html), base_url=str(ROOT)).write_pdf(str(OUT))
print(OUT)
