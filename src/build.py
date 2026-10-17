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

# The live address, e.g. "https://your-username.github.io/your-repo/" (with the trailing slash).
# Link previews (iMessage, Slack, LinkedIn, etc.) need the full address to find the share image.
SITE_URL = ""

split = src.index('<header class="top">')
head, body = src[:split].strip(), src[split:].strip()

# On the website the icons are real files, so phones, home screens and link previews can fetch them
# (app.html keeps them built in, which is what the claude.ai version needs).
head = re.sub(r'<link rel="(icon|apple-touch-icon)"[^>]*>\s*', "", head)
img = (SITE_URL or "") + "icons/og-image.png"
web_head = f"""<meta name="description" content="Build Boolean searches, score candidates against the job description, and track BD contacts.">
<link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="icons/favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="icons/apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<meta name="theme-color" content="#1C1B20">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black">
<meta name="apple-mobile-web-app-title" content="Life Sciences">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Life Sciences Desk">
<meta property="og:title" content="Life Sciences Desk">
<meta property="og:description" content="Build Boolean searches, score candidates against the job description, and track BD contacts.">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
{f'<meta property="og:url" content="{SITE_URL}">' if SITE_URL else ''}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{img}">"""

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
{web_head}
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
if not SITE_URL:
    print("Note: SITE_URL is empty, so link previews may not show the share image. Set it at the top of src/build.py once the site is live.")
