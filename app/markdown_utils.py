import markdown2
import bleach


ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'a', 'hr'
]

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'code': ['class']
}

def markdown_to_html(text):
    if not text:
        return ""
    
    html = markdown2.markdown(text, extras=['fenced-code-blocks', 'tables', 'break-on-newline'])

    clean_html = bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True)
    return clean_html

