import markdown
import bleach

def markdown_to_safe_html(md_text: str) -> str:

    # Convert Markdown to HTML
    html = markdown.markdown(md_text, extensions=['extra'])
    
    # Sanitize
    allowed_tags = [
        'a', 'b', 'i', 'strong', 'em', 'p', 'ul', 'ol', 'li', 'br', 'hr',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'code', 'pre'
    ]
    allowed_attrs = {'a': ['href', 'title', 'rel']}
    
    safe_html = bleach.clean(
        html,
        tags=allowed_tags,
        attributes=allowed_attrs,
        protocols=['http', 'https', 'mailto'],
        strip=True
    )
    safe_html = bleach.linkify(safe_html)
    
    return safe_html
