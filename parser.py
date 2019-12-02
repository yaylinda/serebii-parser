import argparse
import csv
import requests


def get_html(url):
  """
  """
  print('[get_html] retrieving pokedex html from "%s"' % url)
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

    if line.startswith('<table><tr><td class="pkmnblock">'):
      if len(datum['stats']) > 0:
        data.append(datum)
        datum = {}
        datum['stats'] = []

      datum['image_src'] = line.split('<img src="')[1].split('" class="stdsprite"')[0]
      datum['id'] = line.split('/small/')[1].split('.png')[0]
      datum['pokemon_url'] = line.split('><a href="')[1].split('"><img')[0]

    elif line.startswith('<a href="/%s/' % pokemon_generation_keyword):
      datum['name'] = line.split('/">')[1].split('<br />')[0]

    elif line.startswith('<a href="/abilitydex/'):
      datum['abilities'] = []
      if '<br />' in line:
        sub_lines = line.split('<br />')
        for s in sub_lines:
          datum['abilities'].append(s.split('.shtml">')[1].split('</a>')[0])
      else:
        datum['abilities'].append(line.split('.shtml">')[1].split('</a>')[0])

    elif line.startswith('<td align="center" class="fooinfo"><a href="/%s/' % pokemon_generation_keyword):
      datum['types'] = []
      datum['types'].append(line.split('href="/%s/' % pokemon_generation_keyword)[1].split('.shtml')[0])

    elif line.startswith('<td align="center" class="fooinfo">') and '</td>' in line:
      datum['stats'].append(line.split('<td align="center" class="fooinfo">')[1].split('</td>')[0])

  print('[parse_pokedex_html] parsed %d Pokemon information from HTML' % len(data))
  return data


def export_to_csv(data, pokemon_generation_keyword):
  """
  """
  file = open('data/%s.csv' % pokemon_generation_keyword, 'w')
  writer = csv.DictWriter(file, fieldnames=['id','name','pokemon_url','types','abilities','image_src','stats'])
                                                      
  writer.writeheader()
  for row in data:
    writer.writerow(row)
  file.close()

  print('[export_to_csv] done writing to csv!')


def main(pokedex_url, pokemon_generation_keyword):
  """
  """
  html = get_html(pokedex_url)
  data = parse_pokedex_html(html, pokemon_generation_keyword)
  export_to_csv(data, pokemon_generation_keyword)


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
