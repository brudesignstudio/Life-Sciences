"""Build ../index.html, the standalone page that works on any website, from app.html.

app.html is the source for the Claude artifact: the platform wraps it in a
document skeleton when it publishes. Opened from disk or hosted elsewhere, the
page needs that skeleton itself, which this script adds. Run after every change:

    python3 src/build.py
"""
import re
from pathlib import Path

src_dir = Path(__file__).parent
src = (src_dir / "app.html").read_text(encoding="utf-8")

split = src.index('<header class="top">')
head, body = src[:split].strip(), src[split:].strip()

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<style>
:root{{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}
body{{margin:0;font:14px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}}
img{{max-width:100%}}
[hidden]{{display:none!important}}
</style>
{head}
</head>
<body>
{body}
</body>
</html>
"""

# Write every non-ASCII character as an escape (CSS escapes in <style>, entities elsewhere)
# so symbols like the arrows and ellipses show correctly whatever encoding opens the file.
def ascii_only(html):
    out, pos = [], 0
    for m in re.finditer(r"<style>.*?</style>|<script>.*?</script>", html, re.S):
        out.append(re.sub(r"[^\x00-\x7f]", lambda c: f"&#x{ord(c.group()):X};", html[pos:m.start()]))
        block = m.group()
        if block.startswith("<style>"):
            block = re.sub(r"[^\x00-\x7f]", lambda c: f"\\{ord(c.group()):X} ", block)
        else:
            block = re.sub(r"[^\x00-\x7f]", lambda c: "\\u%04X" % ord(c.group()), block)
        out.append(block)
        pos = m.end()
    out.append(re.sub(r"[^\x00-\x7f]", lambda c: f"&#x{ord(c.group()):X};", html[pos:]))
    return "".join(out)

page = ascii_only(page)
out = src_dir.parent / "index.html"
out.write_text(page, encoding="utf-8")
print(f"Wrote {out.name} ({len(page.encode('utf-8')):,} bytes)")
