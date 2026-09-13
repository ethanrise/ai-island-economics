#!/usr/bin/env python3
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED
from html import escape
import re
import uuid
import markdown

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "release" / "v0.1" / "AI时代的小岛经济学-V0.1.epub"
TITLE = "AI时代的小岛经济学"
SUBTITLE = "当生产不再需要人，世界将如何运转"
AUTHOR = "Ethan Rise"
LANG = "zh-CN"
IDENTIFIER = f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, 'https://github.com/ethanrise/ai-island-economics/v0.1')}"

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

CSS = """
html { writing-mode: horizontal-tb; }
body { font-family: serif; line-height: 1.8; margin: 5%; color: #222; }
h1 { font-size: 1.6em; line-height: 1.35; margin: 1.8em 0 1.2em; }
h2 { font-size: 1.15em; line-height: 1.45; margin: 1.8em 0 .8em; }
p { text-indent: 2em; margin: 0 0 .9em; }
h2 + p, blockquote + p, hr + p { text-indent: 0; }
blockquote { margin: 1.5em .6em; padding: .8em 1em; border-left: .18em solid #b49b72; background: #faf7f1; }
blockquote p { text-indent: 0; margin: 0; }
hr { border: 0; border-top: 1px solid #bbb; width: 18%; margin: 2em auto; }
.chapter-no { font-family: sans-serif; color: #8f8069; letter-spacing: .12em; font-size: .78em; margin-top: 2em; }
.part { min-height: 80vh; display: flex; flex-direction: column; justify-content: center; text-align: center; }
.part .num { font-family: sans-serif; color: #8f8069; letter-spacing: .18em; font-size: .85em; margin-bottom: 1.2em; }
.part h1 { font-size: 1.8em; margin: 0; }
.cover { margin: 0; padding: 0; text-align: center; }
.cover img { max-width: 100%; height: auto; }
nav ol { list-style: none; padding-left: 0; }
nav li { margin: .45em 0; }
nav .part-name { margin-top: 1.2em; font-weight: bold; }
a { color: inherit; text-decoration: none; }
""".strip()


def split_title(text: str):
    lines = text.strip().splitlines()
    if lines and lines[0].startswith('#'):
        title = lines[0].lstrip('#').strip()
        return title, '\n'.join(lines[1:]).lstrip()
    return '', text


def num_from_path(path: Path) -> int:
    return int(path.name.split('-', 1)[0])


def xhtml(title: str, body: str, body_class: str = '') -> str:
    return f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{LANG}" lang="{LANG}">
<head>
  <meta charset="utf-8" />
  <title>{escape(title)}</title>
  <link rel="stylesheet" type="text/css" href="css/book.css" />
</head>
<body class="{escape(body_class)}">
{body}
</body>
</html>'''

chapters = []
for p in sorted((ROOT / 'chapters').glob('*.md')):
    title, body = split_title(p.read_text(encoding='utf-8'))
    chapters.append((num_from_path(p), title, body))

items = []
spine = []
toc_entries = []

# Cover
cover_src = ROOT / 'book-pages' / '01-cover.png'
cover_xhtml = xhtml(TITLE, '<div class="cover"><img src="images/cover.png" alt="《AI时代的小岛经济学》封面" /></div>', 'cover')
items.append(('cover', 'cover.xhtml', 'application/xhtml+xml', 'cover'))
spine.append('cover')

# Title page
front_body = f'''<section class="part"><div class="num">V0.1 · 2026.09</div><h1>{escape(TITLE)}</h1><p style="text-indent:0;text-align:center">{escape(SUBTITLE)}</p><p style="text-indent:0;text-align:center">作者：{escape(AUTHOR)}</p></section>'''
items.append(('titlepage', 'title.xhtml', 'application/xhtml+xml', None))
spine.append('titlepage')

chapter_docs = {}
for n, title, body_md in chapters:
    if n in PARTS:
        part_title = PARTS[n]
        part_no, part_name = part_title.split('：', 1)
        pid = f'part-{n:02d}'
        pfile = f'part-{n:02d}.xhtml'
        pbody = f'<section class="part"><div class="num">{escape(part_no)}</div><h1>{escape(part_name)}</h1></section>'
        chapter_docs[pid] = xhtml(part_title, pbody, 'part')
        items.append((pid, pfile, 'application/xhtml+xml', None))
        spine.append(pid)
        toc_entries.append(('part', part_title, pfile))

    label = '序章' if n == 0 else ('终章' if n == 30 else f'CHAPTER {n:02d}')
    body_html = markdown.markdown(body_md, extensions=['extra', 'sane_lists'])
    cbody = f'<div class="chapter-no">{escape(label)}</div><h1>{escape(title)}</h1>{body_html}'
    cid = f'chapter-{n:02d}'
    cfile = f'chapter-{n:02d}.xhtml'
    chapter_docs[cid] = xhtml(title, cbody, 'chapter')
    items.append((cid, cfile, 'application/xhtml+xml', None))
    spine.append(cid)
    toc_entries.append(('chapter', title, cfile))

# Navigation document
nav_lines = [
    '<?xml version="1.0" encoding="utf-8"?>',
    '<!DOCTYPE html>',
    f'<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{LANG}" lang="{LANG}">',
    '<head><meta charset="utf-8" /><title>目录</title><link rel="stylesheet" type="text/css" href="css/book.css" /></head>',
    '<body><nav epub:type="toc" id="toc"><h1>目录</h1><ol>'
]
for kind, title, href in toc_entries:
    cls = ' class="part-name"' if kind == 'part' else ''
    nav_lines.append(f'<li{cls}><a href="{href}">{escape(title)}</a></li>')
nav_lines += ['</ol></nav></body></html>']
nav_doc = '\n'.join(nav_lines)
items.append(('nav', 'nav.xhtml', 'application/xhtml+xml', 'nav'))

manifest = []
for iid, href, media, props in items:
    prop_attr = f' properties="{props}"' if props else ''
    manifest.append(f'<item id="{iid}" href="{href}" media-type="{media}"{prop_attr} />')
manifest.append('<item id="css" href="css/book.css" media-type="text/css" />')
manifest.append('<item id="cover-image" href="images/cover.png" media-type="image/png" properties="cover-image" />')

spine_xml = '\n'.join(f'<itemref idref="{iid}" />' for iid in spine)

opf = f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id" xml:lang="{LANG}">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="book-id">{IDENTIFIER}</dc:identifier>
    <dc:title>{escape(TITLE)}</dc:title>
    <dc:creator>{escape(AUTHOR)}</dc:creator>
    <dc:language>{LANG}</dc:language>
    <dc:description>{escape(SUBTITLE)}</dc:description>
    <meta property="dcterms:modified">2026-09-13T00:00:00Z</meta>
  </metadata>
  <manifest>
    {' '.join(manifest)}
  </manifest>
  <spine>
    {spine_xml}
  </spine>
</package>'''

container_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>'''

OUT.parent.mkdir(parents=True, exist_ok=True)
with ZipFile(OUT, 'w') as zf:
    zf.writestr('mimetype', 'application/epub+zip', compress_type=ZIP_STORED)
    zf.writestr('META-INF/container.xml', container_xml, compress_type=ZIP_DEFLATED)
    zf.writestr('OEBPS/content.opf', opf, compress_type=ZIP_DEFLATED)
    zf.writestr('OEBPS/nav.xhtml', nav_doc, compress_type=ZIP_DEFLATED)
    zf.writestr('OEBPS/css/book.css', CSS, compress_type=ZIP_DEFLATED)
    zf.write(cover_src, 'OEBPS/images/cover.png', compress_type=ZIP_DEFLATED)
    zf.writestr('OEBPS/cover.xhtml', cover_xhtml, compress_type=ZIP_DEFLATED)
    zf.writestr('OEBPS/title.xhtml', xhtml(TITLE, front_body, 'titlepage'), compress_type=ZIP_DEFLATED)
    for iid, doc in chapter_docs.items():
        href = next(href for item_id, href, _, _ in items if item_id == iid)
        zf.writestr('OEBPS/' + href, doc, compress_type=ZIP_DEFLATED)

# Basic structural checks
with ZipFile(OUT, 'r') as zf:
    names = zf.namelist()
    assert names[0] == 'mimetype'
    assert zf.read('mimetype') == b'application/epub+zip'
    assert 'META-INF/container.xml' in names
    assert 'OEBPS/content.opf' in names
    assert 'OEBPS/nav.xhtml' in names
    assert len([n for n in names if n.startswith('OEBPS/chapter-')]) == len(chapters)

print(OUT)
