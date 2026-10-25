import argparse, datetime, json, pathlib, subprocess, xml.etree.ElementTree as ET

def text(node):
    return '' if node is None else ' '.join(''.join(node.itertext()).split())

def build(source, output):
    papers, venues = [], {}
    for file in sorted((source / 'data/xml').glob('*.xml')):
        root = ET.parse(file).getroot()
        for volume in root.findall('volume'):
            meta = volume.find('meta')
            year = text(meta.find('year'))
            if not year.isdigit():
                continue
            venue = text(meta.find('venue')) or root.attrib['id']
            book = text(meta.find('booktitle'))
            venues.setdefault(venue, venue.upper())
            for paper in volume.findall('paper'):
                title = text(paper.find('title'))
                if not title:
                    continue
                cid, vid, pid = root.attrib['id'], volume.attrib['id'], paper.attrib['id']
                ident = f'{cid}-{vid}.{pid}' if '.' in cid else f'{cid}{vid}-{int(pid):04d}'
                papers.append(dict(id=ident, title=title, year=int(year), venue=venue, book=book,
                    authors=', '.join(' '.join(filter(None, [text(a.find('first')), text(a.find('last'))])) for a in paper.findall('author')),
                    abstract=text(paper.find('abstract'))))
    if not papers:
        raise RuntimeError('No papers imported; refusing to publish an empty index')
    output.mkdir(parents=True, exist_ok=True)
    papers.sort(key=lambda p: (-p['year'], p['id']))
    (output / 'papers.json').write_text(json.dumps(dict(updated=datetime.datetime.now(datetime.timezone.utc).isoformat(), papers=papers, venues=venues), ensure_ascii=False), encoding='utf-8')
    print(f'Indexed {len(papers)} papers and {len(venues)} venues')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=pathlib.Path)
    parser.add_argument('--output', type=pathlib.Path, default=pathlib.Path('site/data'))
    args = parser.parse_args()
    build(args.source, args.output)
