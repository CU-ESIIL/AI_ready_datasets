"""Check rendered local links, fragments and media without network access."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

class Page(HTMLParser):
    def __init__(self, content):
        super().__init__(convert_charrefs=True)
        self.ids=set();self.links=[];self.images=[]
        self.feed(content)
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if 'id' in attrs:self.ids.add(attrs['id'])
        if tag=='a' and 'href' in attrs:self.links.append(attrs['href'])
        if tag in ('img','script','iframe') and 'src' in attrs:self.links.append(attrs['src'])
        if tag=='link' and 'href' in attrs:self.links.append(attrs['href'])
        if tag=='img':self.images.append(attrs)

def check(root, site_prefix="/AI_ready_datasets/"):
    root=Path(root).resolve();pages={path:Page(path.read_text()) for path in root.rglob('*.html') if 'overrides' not in path.relative_to(root).parts}
    errors=[]
    for path,page in pages.items():
        for link in page.links:
            parsed=urlsplit(link)
            if parsed.scheme or parsed.netloc:continue
            # MkDocs emits relative internal links; root paths are resolved inside site.
            local_path=parsed.path
            if local_path.startswith(site_prefix):local_path='/'+local_path[len(site_prefix):]
            target=((root/local_path.lstrip('/')) if local_path.startswith('/') else
                    path.parent/unquote(local_path)) if parsed.path else path
            target=target.resolve()
            if target.is_dir():target=target/'index.html'
            if not target.exists():errors.append(f'{path.relative_to(root)}: missing {link}')
            elif parsed.fragment and target in pages and unquote(parsed.fragment) not in pages[target].ids:
                errors.append(f'{path.relative_to(root)}: missing fragment {link}')
        for img in page.images:
            if 'alt' not in img:errors.append(f'{path.relative_to(root)}: image missing alt')
    if errors:raise SystemExit('\n'.join(errors))
    print(f'Checked {len(pages)} HTML pages: local links, fragments, media and alt attributes passed.')

if __name__=='__main__':check(sys.argv[1] if len(sys.argv)>1 else 'site')
