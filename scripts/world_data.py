"""Builds scripts/data/world.json from Natural Earth 1:110m countries (public domain):
country outlines in the Equal Earth projection, plus each country's label point.
Usage: python3 scripts/world_data.py ne_110m_admin_0_countries.geojson"""
import json, math, os, sys
A1, A2, A3, A4, M = 1.340264, -0.081106, 0.000893, 0.003796, math.sqrt(3) / 2


def equal_earth(lon, lat):
    l, p = math.radians(lon), math.radians(lat)
    t = math.asin(M * math.sin(p))
    t2, t6 = t * t, t ** 6
    x = l * math.cos(t) / (M * (A1 + 3 * A2 * t2 + t6 * (7 * A3 + 9 * A4 * t2)))
    y = t * (A1 + A2 * t2 + t6 * (A3 + A4 * t2))
    return x, y


def main(src):
    feats = json.load(open(src, encoding='utf-8'))['features']
    out = {'projection': 'Equal Earth', 'source': 'Natural Earth 1:110m admin 0 countries', 'countries': {}}
    for f in feats:
        p, g = f['properties'], f['geometry']
        if p['ADMIN'] == 'Antarctica':
            continue
        polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        rings = []
        for poly in polys:
            for ring in poly[:1]:  # outer rings are enough at this scale
                rings.append([[round(c, 3) for c in equal_earth(lon, lat)] for lon, lat in ring])
        out['countries'][p['ADMIN']] = dict(iso=p['ISO_A3'] if p['ISO_A3'] != '-99' else p['ADM0_A3'], rings=rings,
                                            label=[round(c, 4) for c in equal_earth(p['LABEL_X'], p['LABEL_Y'])])
    dst = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'world.json')
    json.dump(out, open(dst, 'w', encoding='utf-8'), separators=(',', ':'), ensure_ascii=False)
    print('%s: %d countries, %d KB' % (dst, len(out['countries']), os.path.getsize(dst) // 1024))


if __name__ == '__main__':
    main(sys.argv[1])
