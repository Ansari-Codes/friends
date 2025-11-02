import markdown
import bleach
from bs4 import BeautifulSoup
from nicegui.ui import add_css
from comps.Interface.INTERFACE import ANIMATIONS

def markdown_to_safe_html(md_text: str) -> str:
    css_string = ''
    for name, animation in ANIMATIONS.items():
        css_string += f"""
                @keyframes {name} {{
                {animation['keyframes']}
                }}
                .animate-{name} {{
                    {animation['class_string']}
                }}
            """
    add_css(css_string, shared=True)
    html = markdown.markdown(md_text, extensions=['extra'])

    allowed_tags = [
        'a', 'b', 'i', 'strong', 'em', 'p', 'ul', 'ol', 'li', 'br', 'hr',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'code', 'pre', 'span', 'div'
    ]

    # Allow all classes without filtering values
    allowed_attrs = {
        '*': ['class', 'style'],
        'a': ['href', 'title', 'rel', 'target', 'class']
    }

    # Sanitize HTML while keeping classes intact
    safe_html = bleach.clean(
        html,
        tags=allowed_tags,
        attributes=allowed_attrs,
        protocols=['http', 'https', 'mailto'],
        strip=True
    )

    # Apply inline styles
    style_map = {
        'h1': 'font-size:28px;margin:0;padding:0;line-height:1.1;',
        'h2': 'font-size:26px;margin:0;padding:0;line-height:1.1;',
        'h3': 'font-size:24px;margin:0;padding:0;line-height:1.2;',
        'h4': 'font-size:22px;margin:0;padding:0;line-height:1.5;',
        'h5': 'font-size:20px;margin:0;padding:0;line-height:1.5;',
        'h6': 'font-size:18px;margin:0;padding:0;line-height:1.5;',
        'p': 'font-size:14px;margin:0;padding:0;line-height:1.5;',
        'ul': 'margin:4px 0 4px 20px;padding:0;list-style-type:disc;',
        'ol': 'margin:4px 0 4px 20px;padding:0;list-style-type:decimal;',
        'li': 'font-size:14px;margin:2px 0;line-height:1.4;',
        'code': 'font-size:12px;background:#f4f4f4;padding:1px 3px;border-radius:2px;',
        'pre': 'font-size:12px;background:#f4f4f4;padding:4px 6px;border-radius:2px;overflow-x:auto;margin:2px 0;',
        'blockquote': 'font-size:14px;color:#555;border-left:2px solid #ccc;padding-left:6px;margin:2px 0;',
        'a': 'color:#1a0dab;text-decoration:underline;'
    }

    soup = BeautifulSoup(safe_html, 'html.parser')
    for tag_name, style in style_map.items():
        for tag in soup.find_all(tag_name):
            existing_style = tag.get('style', '')
            tag['style'] = f"{style} {existing_style}".strip()

    for a in soup.find_all('a'):
        a['target'] = '_blank'
        rel = a.get('rel', '')
        if 'noopener' not in rel:
            rel = (rel + ' noopener').strip()
        if 'noreferrer' not in rel:
            rel = (rel + ' noreferrer').strip()
        a['rel'] = rel

    return str(soup)
