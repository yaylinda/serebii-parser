import csv
import requests

data_columns = [
  'id', 
  'name', 
  'pokemon_url'
  'types', 
  'abilities', 
  'image_src', 
  'stats']

def get_html(url):
  r = requests.get(url)
  return r.text

def parse_pokedex_html(html, pokemon_generation_keyword):
  data = []
  lines = html.splitlines()

  print('[parse_pokedex_html] parsing %d lines' % len(lines))

  datum = {}
  datum['stats'] = []

  for line in lines:
    if line.startswith('<table><tr><td class="pkmnblock">'):

      data.append(datum)
      datum = {}
      datum['stats'] = []

      datum['image_src'] = line.split('<img src="')[1].split(' class="stdsprite"')[0]
      datum['id'] = line.split('/small/')[1].split('.png')[0]
      datum['pokemon_url'] = line.split('><a href="')[1].split('"><img')[0]
    if line.startswith('<a href="/%s/' % pokemon_generation_keyword):
      datum['name'] = line.split('/">')[1].split('<br />')[0]
    if line.startswith('<a href="/abilitydex/'):
      ab1 = line.split('<br />')[0]
      ab2 = line.split('<br />')[1]
      datum['abilities'] = []
      datum['abilities'].append(ab1.split('.shtml">')[1].split('</a>')[0])
      datum['abilities'].append(ab2.split('.shtml">')[1].split('</a>')[0])
    if line.startswith('<td align="center" class="fooinfo"><a href="/%s/' % pokemon_generation_keyword):
      datum['types'] = []
      datum['types'].append(line.split('href="/%s/' % pokemon_generation_keyword)[1].split('.shtml')[0])
    if line.startswith('<td align="center" class="fooinfo">') and '</td>' in line:
      datum['stats'].append(line.split('<td align="center" class="fooinfo">')[1].split('</td>')[0])

  return data


def main():
  pokedex_url = 'https://www.serebii.net/swordshield/galarpokedex.shtml'
  html = get_html(pokedex_url)

  pokemon_generation_keyword = 'pokedex-swsh'
  data = parse_pokedex_html(html, pokemon_generation_keyword)

  print(data)

if __name__ == '__main__':
  main()
