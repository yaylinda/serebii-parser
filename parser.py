import argparse
import csv
import json
import requests
import time


def get_html(url):
  """
  """
  r = requests.get(url)
  return r.text


def parse_pokedex_html(html, pokemon_generation_keyword):
  """
  """
  data = []
  lines = html.splitlines()

  print('[parse_pokedex_html] parsing %d lines of HTML' % len(lines))

  datum = {}
  datum['stats'] = []

  for line in lines:
    line = line.strip()

    if '<table><tr><td class="pkmnblock">' in line:
      if len(datum['stats']) > 0:
        data.append(datum)
        datum = {}
        datum['stats'] = []

      datum['image_src'] = line.split('<img src="')[1].split('" class="stdsprite"')[0]
      datum['id'] = line.split('/small/')[1].split('.png')[0]
      datum['pokemon_url'] = line.split('><a href="')[1].split('"><img')[0]

    elif '<a href="/%s/' % pokemon_generation_keyword in line and '/">' in line and '<br />' in line:
      datum['name'] = line.split('/">')[1].split('<br />')[0]

    elif '<a href="/abilitydex/' in line and '.shtml' in line:
      datum['abilities'] = []
      if '<br />' in line:
        sub_lines = line.split('<br />')
        for s in sub_lines:
          datum['abilities'].append(s.split('.shtml">')[1].split('</a>')[0])
      else:
        datum['abilities'].append(line.split('.shtml">')[1].split('</a>')[0])

    elif '<td align="center" class="fooinfo"><a href="/%s/' % pokemon_generation_keyword in line:
      datum['types'] = []
      if 'a> <a' in line:
          sub_lines = line.split('a> <a')
          for s in sub_lines:
            datum['types'].append(s.split('href="/%s/' % pokemon_generation_keyword)[1].split('.shtml')[0])
      else:
        datum['types'].append(line.split('href="/%s/' % pokemon_generation_keyword)[1].split('.shtml')[0])

    elif '<td align="center" class="fooinfo">' in line and '</td>' in line:
      datum['stats'].append(line.split('<td align="center" class="fooinfo">')[1].split('</td>')[0])

  print('[parse_pokedex_html] parsed %d Pokemon information from HTML' % len(data))
  return data


def parse_moves(original_data):
  """
  """
  data = []

  for datum in original_data:
    datum['moves'] = parse_moves_from_url(datum['name'], datum['pokemon_url'])
    data.append(datum)
    time.sleep(0.1)

  return data


def parse_moves_from_url(pokemon_name, url):
  """
  """

  html = get_html('https://www.serebii.net' + url)
  lines = html.splitlines()

  moves = []
  move = {}

  for line in lines:
    line = line.strip()

    # TODO - abstract parsing keywords like "swsh", "bw"

    if '<td rowspan="2" class="fooinfo"><a href="/attackdex-swsh/' in line:
      if len(move.keys()) == 3 and '<font size=\"1\"><i>(Details)</i>' not in move['name'] and move['name'] not in [m['name'] for m in moves]:
        moves.append(move)
        move = {}

      move['name'] = line.split('.shtml">')[1].split('</a></td>')[0]

    elif '<td class="cen"><img src="/pokedex-bw/type/' in line and '.gif' in line:
      move['type'] = line.split('<td class="cen"><img src="/pokedex-bw/type/')[1].split('.gif')[0]

    elif '<td class="cen"><img src="/pokedex-bw/type/' in line and '.png' in line:
      move['category'] = line.split('<td class="cen"><img src="/pokedex-bw/type/')[1].split('.png')[0]

    # TODO - parse other moves info, if needed

  print('[parse_moves_from_url] parsed %d moves for %s' % (len(moves), pokemon_name))

  return moves


def export_to_csv(data, pokemon_generation_keyword):
  """
  """
  with open('data/%s.csv' % pokemon_generation_keyword, 'w') as file:
    writer = csv.DictWriter(file, fieldnames=['id','name','pokemon_url','types','abilities','image_src','stats','moves'])                                               
    writer.writeheader()
    for row in data:
      writer.writerow(row)

  print('[export_to_csv] done writing to csv')


def export_to_json(data, pokemon_generation_keyword):
  """
  """
  with open('data/%s.json' % pokemon_generation_keyword, 'w') as file:
    json.dump(data, file)

  print('[export_to_json] done writing to json')


def main(pokedex_url, pokemon_generation_keyword):
  """
  """
  html = get_html(pokedex_url)
  data = parse_pokedex_html(html, pokemon_generation_keyword)
  data = parse_moves(data)

  export_to_csv(data, pokemon_generation_keyword)
  export_to_json(data, pokemon_generation_keyword)


if __name__ == '__main__':
  """
  """
  pokedex_urls = {
    'https://www.serebii.net/swordshield/galarpokedex.shtml' : 'pokedex-swsh'
  }

  parser = argparse.ArgumentParser(description='Script to parse HTML from serebii')
  parser.add_argument('--pokedex_url', help='serebii url to parse', choices=pokedex_urls.keys())
  args = parser.parse_args()

  main(args.pokedex_url, pokedex_urls[args.pokedex_url])
