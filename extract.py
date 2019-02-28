import os
import re
import requests
import demjson

TEMPLATE = '''<svg class="svg-inline--fa fa-{name} fa-w-14" aria-hidden="true" focusable="false" data-prefix="far" data-icon="share-alt" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" data-fa-i2svg=""><path fill="currentColor" d="{svg}"></path></svg>'''


def parse_url(prefix, url, height=48, width=48):

    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0', 'Referer': 'https://fontawesome.com/', })

    m = re.findall('var \w=(\{[^}]+\[\][^}]+\})', r.text, flags=re.M)

    # open('_icons_orig.js', 'w').write(r.text)

    for text in m:

        text = re.sub('([\w-]+):', r"'\1':", text)

        try:
            icons = demjson.decode(text)
        except demjson.JSONDecodeError:
            continue

        # open('_icons.js', 'w').write(text)
        # open('_icons.py', 'w').write(str(icons))

        os.makedirs('svg/{prefix}/'.format(prefix=prefix), exist_ok=1)
        os.makedirs('png/{prefix}/'.format(prefix=prefix), exist_ok=1)

        i = 0
        print('*'*80)
        print(prefix)
        print('*'*80)
        for name, (width, height, _, _, svg) in icons.items():
            i += 1
            print(i, name)

            params = dict(prefix=prefix, name=name, width=width, height=height, svg=svg)

            open('svg/{prefix}/{name}.svg'.format(**params), 'w').write(TEMPLATE.format(**params))

            os.system('rsvg-convert --format=png --height={height} --width={width} --output=png/{prefix}/{name}.png svg/{prefix}/{name}.svg'.format(**params))


def main():
    os.system('rm -rf png svg')

    # or https://pro.fontawesome.com/
    parse_url('solid', 'https://use.fontawesome.com/releases/v5.7.2/js/solid.js', 48, 48)
    parse_url('regular', 'https://use.fontawesome.com/releases/v5.7.2/js/regular.js', 48, 48)
    parse_url('brands', 'https://use.fontawesome.com/releases/v5.7.2/js/brands.js', 48, 48)
    parse_url('fontawesome', 'https://use.fontawesome.com/releases/v5.7.2/js/fontawesome.js', 48, 48)


if __name__ == '__main__':
    main()
