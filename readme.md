# site2epub

Simple script to take the main contents of a webpage and output an epub file.

This uses `justext` for context extraction (worked best in my tests) and uses `pandoc` to generate the epub.

## Installation

```
pip install -r requirements.txt
apt install pandoc
```

## Usage

```
python site2epub.py <URL> <OUTPUT>.epub
```