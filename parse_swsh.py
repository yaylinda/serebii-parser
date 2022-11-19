import time
from common import get_html_lines
from common import export_to_csv
from common import export_to_json
from common import parse_moves


def parse_pokedex_html(html_lines, pokemon_generation_keyword):
  """
  """
  data = []

  print('[parse_pokedex_html] parsing %d lines of HTML' % len(html_lines))

  datum = {}
  datum['stats'] = []

  for line in html_lines:
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


def add_moves_data(original_data):
  """
  """
  data = []

  for datum in original_data:
    pokemon_page_html_lines = get_html_lines('https://www.serebii.net' + datum['pokemon_url'])
    datum['moves'] = parse_moves(datum['name'], pokemon_page_html_lines, 'swsh')
    data.append(datum)
    time.sleep(0.1)

  return data


def main(pokedex_url, pokemon_generation_keyword):
  """
  """
  html_lines = get_html_lines(pokedex_url)
  data = parse_pokedex_html(html_lines, pokemon_generation_keyword)
  data = add_moves_data(data)

  export_to_csv(data, pokemon_generation_keyword)
  export_to_json(data, pokemon_generation_keyword)


if __name__ == '__main__':
  main('https://www.serebii.net/swordshield/galarpokedex.shtml', 'pokedex-swsh')