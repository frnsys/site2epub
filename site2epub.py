import justext
import requests
import subprocess

def site2epub(url, outfile=None):
    resp = requests.get(url)
    paragraphs = justext.justext(resp.content, justext.get_stoplist('English'))

    title = None
    html = ['<p>Saved from: {}</p>'.format(url)]
    for paragraph in paragraphs:
        if not paragraph.is_boilerplate:
            tag = paragraph.dom_path.rsplit('.', 1)[-1]
            if paragraph.is_heading:
                if title is None:
                    title = paragraph.text
                html.append('<{}>{}</{}>'.format(tag, paragraph.text, tag))
            else:
                html.append('<p>{}</p>'.format(paragraph.text))

    with open('/tmp/site2epub.html', 'w') as f:
        f.write('\n'.join(html))

    outfile = outfile or '{}.epub'.format(title)
    subprocess.run(['pandoc', '-o', outfile, '/tmp/site2epub.html'])


if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    if len(args) < 1:
        print('Specify the url')
        sys.exit(1)

    if len(args) >= 2:
        url, outfile = args
    else:
        url, outfile = args[0], None
    site2epub(url, outfile)