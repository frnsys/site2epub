import os
import justext
import requests
import subprocess

def site2epub(url, outdir):
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

    outfile = os.path.join(outdir, '{}.epub'.format(title))
    subprocess.run(['pandoc', '-o', outfile, '/tmp/site2epub.html'])
    return outfile


if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    if len(args) < 2:
        print('Specify the url and output dir')
        sys.exit(1)

    url, outdir = args
    path = site2epub(url, outdir)
    print(path)