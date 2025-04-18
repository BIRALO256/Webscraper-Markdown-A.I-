from processor.markdownifier import html_to_markdown

def test_html_to_markdown():
    md = html_to_markdown('<h1>Title</h1>')
    assert '# Title' in md