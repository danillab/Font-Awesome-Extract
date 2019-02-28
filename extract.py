import os
import re
import requests
import demjson

template = '''<svg class="svg-inline--fa fa-{name} fa-w-14" aria-hidden="true" focusable="false" data-prefix="far" data-icon="share-alt" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" data-fa-i2svg=""><path fill="currentColor" d="{svg}"></path></svg>'''

url = 'https://use.fontawesome.com/releases/v5.7.2/js/all.js' # or https://pro.fontawesome.com/...

r = requests.get(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0', 'Referer':'https://fontawesome.com/', })

m = re.search('var \w=(\{[^}]+512,[^}]+\})', r.text, flags=re.M)
icons = demjson.decode(m[1])

for name, (width, height, _, _, svg) in icons.items():
    open(f'svg/{name}.svg', 'w').write(template.format(name=name, width=width, height=height, svg=svg))

for name, _ in icons.items():
    os.system(f'rsvg-convert --format=png --height=32 --width=32 --output=png/{name}.png svg/{name}.svg')