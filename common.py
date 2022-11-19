import csv
import json
import requests


def get_html_lines(url):
  """
  """
  r = requests.get(url)
  html = r.text
  lines = [x.strip() for x in html.splitlines()]

  return lines


def export_to_csv(data, filename):
  """
  """
  with open('data/%s.csv' % filename, 'w') as file:
    writer = csv.DictWriter(file, fieldnames=['id','name','pokemon_url','types','abilities','image_src','stats','moves'])                                               
    writer.writeheader()
    for row in data:
      writer.writerow(row)

  print('[export_to_csv] done writing to csv')


def export_to_json(data, filename):
  """
  """
  with open('data/%s.json' % filename, 'w') as file:
    json.dump(data, file)

  print('[export_to_json] done writing to json')


def parse_moves(pokemon_name, lines, attack_dex):
  """
  """
  moves = []
  move = {}

  for line in lines:
    # TODO - abstract parsing keywords like "swsh", "bw"

    if ('<td rowspan="2" class="fooinfo"><a href="/attackdex-%s/' % attack_dex) in line:
      if len(move.keys()) == 3 and '<font size=\"1\"><i>(Details)</i>' not in move['name'] and move['name'] not in [m['name'] for m in moves]:
        moves.append(move)
        move = {}

      move['name'] = line.split('.shtml">')[1].split('</a></td>')[0]\
        .replace('</a><br /><i>BDSP Only</i></td>', '')\
        .replace('</a><br /><i>SWSH Only</i></td>', '')

    elif '<td class="cen"><img src="/pokedex-bw/type/' in line and '.gif' in line:
      move['type'] = line.split('<td class="cen"><img src="/pokedex-bw/type/')[1].split('.gif')[0]

    elif '<td class="cen"><img src="/pokedex-bw/type/' in line and '.png' in line:
      move['category'] = line.split('<td class="cen"><img src="/pokedex-bw/type/')[1].split('.png')[0]

    # TODO - parse other moves info, if needed

  print('[parse_moves_from_url] parsed %d moves for %s' % (len(moves), pokemon_name))

  return moves