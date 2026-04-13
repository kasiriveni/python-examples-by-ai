"""
Automation: Web scraping basics.
"""
from urllib.request import urlopen, Request
from html.parser import HTMLParser
import json

# Simple HTML parser
class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.current_text = ""
        self.in_link = False

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.in_link = True
            for attr, value in attrs:
                if attr == 'href':
                    self.links.append({"href": value, "text": ""})

    def handle_data(self, data):
        if self.in_link and self.links:
            self.links[-1]["text"] += data.strip()

    def handle_endtag(self, tag):
        if tag == 'a':
            self.in_link = False

# Parse sample HTML
sample_html = """
<html>
<body>
    <h1>Example Page</h1>
    <a href="https://python.org">Python Official</a>
    <a href="https://docs.python.org">Python Docs</a>
    <a href="https://pypi.org">PyPI</a>
    <p>Some text here.</p>
    <a href="https://github.com">GitHub</a>
</body>
</html>
"""

parser = LinkExtractor()
parser.feed(sample_html)

print("Extracted links:")
for link in parser.links:
    print(f"  {link['text']}: {link['href']}")

# Title extractor
class TitleExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title = ""

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True

    def handle_data(self, data):
        if self.in_title:
            self.title += data

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

# Table parser
class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.current_row = []
        self.current_cell = ""
        self.in_cell = False

    def handle_starttag(self, tag, attrs):
        if tag in ('td', 'th'):
            self.in_cell = True
            self.current_cell = ""
        elif tag == 'tr':
            self.current_row = []

    def handle_data(self, data):
        if self.in_cell:
            self.current_cell += data.strip()

    def handle_endtag(self, tag):
        if tag in ('td', 'th'):
            self.in_cell = False
            self.current_row.append(self.current_cell)
        elif tag == 'tr':
            if self.current_row:
                self.rows.append(self.current_row)

table_html = """
<table>
    <tr><th>Name</th><th>Age</th><th>City</th></tr>
    <tr><td>Alice</td><td>30</td><td>NYC</td></tr>
    <tr><td>Bob</td><td>25</td><td>LA</td></tr>
</table>
"""

tp = TableParser()
tp.feed(table_html)
print("\nParsed table:")
for row in tp.rows:
    print(f"  {row}")
