"""Build the CCM Dashboard HTML with embedded data from CSVs."""
import csv
import json
from collections import Counter

def parse_data():
    events = []
    with open('data/Calendar-Grid view (chron).csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            start = row.get('Event start', '')
            year = ''
            month = ''
            if start and '/' in start:
                parts = start.split('/')
                if len(parts) >= 3:
                    month = parts[0].strip()
                    year = parts[2].strip().split()[0]
            types = [t.strip() for t in row.get('Type', '').split(',') if t.strip()]
            loc = row.get('Location', '').strip()
            is_virtual = any(w in loc.lower() for w in ['webinar', 'zoom', 'online', 'virtual', 'video conference'])
            title = row.get('Event title', '').strip()
            if not title:
                continue
            events.append({
                't': title[:140],
                's': start.strip(),
                'l': loc[:120],
                'a': row.get('About', '').strip()[:250],
                'tp': types,
                'lk': row.get('Registration link', '').strip(),
                'ls': row.get('Livestream', '').strip(),
                'r': row.get('Recorded', '').strip(),
                'y': year,
                'm': month,
                'v': is_virtual
            })

    events = [e for e in events if e['y']]

    newsletters = []
    with open('data/Newsletters-NJ newsletter repository.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name', '').strip()
            if not name:
                continue
            newsletters.append({
                'n': name,
                'd': row.get('Description', '').strip()[:250],
                'f': row.get('Frequency', '').strip(),
                'u': row.get('Subscribe', '').strip()
            })

    by_year = dict(sorted(Counter(e['y'] for e in events).items()))
    types_count = Counter()
    for e in events:
        for t in e['tp']:
            types_count[t] += 1

    virtual_by_year = {}
    for e in events:
        y = e['y']
        if y not in virtual_by_year:
            virtual_by_year[y] = [0, 0]
        if e['v']:
            virtual_by_year[y][0] += 1
        else:
            virtual_by_year[y][1] += 1

    month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    by_month = Counter()
    for e in events:
        m = e['m']
        if m.isdigit():
            mi = int(m)
            if 1 <= mi <= 12:
                by_month[month_names[mi-1]] += 1

    return json.dumps({
        'e': events,
        'n': newsletters,
        'by': by_year,
        'tc': dict(types_count.most_common()),
        'vby': dict(sorted(virtual_by_year.items())),
        'bm': {m: by_month.get(m, 0) for m in month_names},
        'fc': dict(Counter(n['f'] for n in newsletters)),
        'ls': sum(1 for e in events if e['ls'] == 'Yes'),
        'rc': sum(1 for e in events if e['r'] == 'Yes'),
        'te': len(events),
        'tn': len(newsletters)
    }, ensure_ascii=False)


if __name__ == '__main__':
    data_json = parse_data()

    with open('template.html', 'r', encoding='utf-8') as f:
        template = f.read()

    html = template.replace('__DATA_PLACEHOLDER__', data_json)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'Built index.html ({len(html):,} bytes)')
