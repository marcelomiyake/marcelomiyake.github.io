#!/usr/bin/env python3
"""Subset local icon fonts from the pinned Chirpy assets (requires fonttools[woff])."""
from pathlib import Path
import re
import shutil
import subprocess
from fontTools import subset
from fontTools.ttLib import TTFont

output = Path('assets/fonts')
output.mkdir(exist_ok=True)
theme = Path(subprocess.check_output(['bundle', 'info', 'jekyll-theme-chirpy', '--path'], text=True).strip())
icons = set()
for root in [theme / '_includes', theme / '_layouts', theme / '_data', theme / 'assets/js', Path('_data'), Path('_tabs'), Path('_posts'), Path('_includes'), Path('_layouts'), Path('assets/js')]:
    for path in root.rglob('*'):
        if path.is_file():
            icons.update(re.findall(r'fa-[a-z0-9-]+', path.read_text(errors='ignore')))
css = Path('assets/lib/fontawesome-free/css/all.min.css').read_text()
codepoints = set()
for selectors, codepoint in re.findall(r'([^{}]+)\{--fa:"\\([a-f0-9]+)"\}', css):
    if icons.intersection(re.findall(r'fa-[a-z0-9-]+', selectors)):
        codepoints.add(int(codepoint, 16))


def make_font(source, target, unicodes, family):
    font = TTFont(source)
    options = subset.Options()
    options.flavor = 'woff2'
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(unicodes=unicodes)
    subsetter.subset(font)
    # Subsets are modified fonts: use a new internal name for OFL reserved names.
    for record in font['name'].names:
        if record.nameID in {1, 3, 4, 6, 16}:
            record.string = family.encode(record.getEncoding())
    font.flavor = 'woff2'
    font.save(output / target)


for name in ['fa-solid-900', 'fa-regular-400', 'fa-brands-400']:
    make_font(f'assets/lib/fontawesome-free/webfonts/{name}.woff2', f'{name}.woff2', codepoints, f'SiteIcons-{name}')
# Keep aliases for used icons, plus the theme's utility classes and animations.
css = css.replace('../webfonts/', '').replace('font-display:block', 'font-display:swap')
css = re.sub(r'([^{}]+)\{--fa:"\\([a-f0-9]+)"\}',
             lambda match: match[0] if icons.intersection(re.findall(r'fa-[a-z0-9-]+', match[1])) else '', css)
(output / 'icons.css').write_text(css)
shutil.copyfile('assets/lib/fontawesome-free/webfonts/fa-v4compatibility.woff2', output / 'fa-v4compatibility.woff2')
shutil.copyfile('assets/lib/fontawesome-free/LICENSE.txt', output / 'FONT-AWESOME-LICENSE.txt')
print(f'Generated fonts for {len(icons)} theme icon classes in {output}')
