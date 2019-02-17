import os
import justext
import subprocess
from slugify import slugify
from newspaper import Article
from datetime import datetime

tmpl = '''
<html>
<head>
    <title>{title}</title>
    <meta name="subtitle" content="{subtitle}">
    <meta name="author" content="{author}">
    <meta name="date" content="Created at {date}">
    <meta name="subject" content="{keywords}">
</head>
<body>
{body}
</body>
</html>
'''

def site2epub(url, outdir):
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    paragraphs = justext.justext(article.html, justext.get_stoplist('English'))

    html = []
    for paragraph in paragraphs:
        if not paragraph.is_boilerplate:
            tag = paragraph.dom_path.rsplit('.', 1)[-1]
            if paragraph.is_heading:
                html.append('<{}>{}</{}>'.format(tag, paragraph.text, tag))
            else:
                html.append('<p>{}</p>'.format(paragraph.text))


    title = article.title
    with open('/tmp/site2epub.html', 'w') as f:
        f.write(tmpl.format(
            title=title,
            author='; '.join(article.authors),
            subtitle='Saved from: {}'.format(url),
            keywords=', '.join(article.keywords),
            date=datetime.now(),
            body='\n'.join(html)))

    fname = '{}.epub'.format(slugify(title))
    outfile = os.path.join(outdir, fname)
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