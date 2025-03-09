import csv
import json

def load_json(file):
  with open(file) as f:
    return json.load(f)

taggings = load_json('input/taggings.json')
taggings_dict = {}
for entry in taggings:
  uid = entry.pop('uid')
  tags = []
  for tag in entry['tags']:
    tags.append(tag['name'])
  taggings_dict[uid] = tags

cards = load_json('input/cards.json')
card_csv = []
for card in cards:
  uid = card['uid']
  price = card['printings']['latest']['prices']['tix']
  card_csv.append({
    'name': card['name'],
    'colors': card['colors'],
    'types': card['types'],
    'price': float(price) if price else None,
    'tags': taggings_dict.get(uid, [])
  })

with open('output/cards.csv', 'w', newline='') as f:
  writer = csv.DictWriter(f, fieldnames=['name', 'colors', 'types', 'price', 'tags'])
  writer.writeheader()
  writer.writerows(card_csv)

tags = load_json('input/tags.json')
uid_dict = { t['uid']: t['name'] for t in tags }
tag_csv = []
for tag in tags:
  ancestry = [uid_dict.get(id) for id in tag.get('ancestry', [])]
  childTags = [uid_dict.get(id) for id in tag.get('childTags', [])]

  # Filter out None values if necessary
  ancestry = [a for a in ancestry if a is not None]
  childTags = [c for c in childTags if c is not None]

  tag_csv.append({
    'name': tag['name'],
    'display_name': tag['displayName'],
    'description': tag['description'],
    'count': tag['count'],
    'exclusive': tag['exclusive'],
    'ancestry': ancestry,
    'childTags': childTags
  })

with open('output/tags.csv', 'w', newline='') as f:
  writer = csv.DictWriter(f, fieldnames=['name', 'display_name', 'description', 'count', 'exclusive', 'ancestry', 'childTags'])
  writer.writeheader()
  writer.writerows(tag_csv)
