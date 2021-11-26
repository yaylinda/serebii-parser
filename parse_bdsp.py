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

  parsing_pokemon_link = False
  parse_pokemon_link_prefix = '<a href="/%s/' % pokemon_generation_keyword

  datum = {}
  datum['stats'] = []

  for line in html_lines:

    if not parsing_pokemon_link and '<td class="pkmnblock">' in line:
      parsing_pokemon_link = True
    
    elif parsing_pokemon_link and parse_pokemon_link_prefix in line:
      parsing_pokemon_link = False
      datum['pokemon_url'] = line.split('<a href="')[1].split('">')[0]
      datum['name'] = line.split(parse_pokemon_link_prefix)[1].split('/">')[0].capitalize()
      data.append(datum)
      datum = {}

  print('[parse_pokedex_html] parsed %d Pokemon information from HTML' % len(data))
  return data


def parse_moves_and_stats(original_data):
  """
  """
  data = []

  for datum in original_data:
    pokemon_page_html_lines = get_html_lines('https://www.serebii.net' + datum['pokemon_url'])
    datum['moves'] = parse_moves(datum['name'], pokemon_page_html_lines)
    datum['stats'] = parse_stats(datum['name'], pokemon_page_html_lines)
    data.append(datum)
    time.sleep(0.1)

  return data


def parse_stats(pokemon_name, lines):
  stats = []

  expected_num_stats = 6

  parsing_stats = False
  parse_stats_line_prefix = 'class="fooinfo">Base Stats - Total:'
  stat_line_prefix = '<td align="center" class="fooinfo">'
  stat_line_suffix = '</td>'

  for line in lines:

    if not parsing_stats and parse_stats_line_prefix in line:
      parsing_stats = True

    elif parsing_stats:
      stats.append(int(line.split(stat_line_prefix)[1].split(stat_line_suffix)[0]))
      if len(stats) == expected_num_stats:
        break

  print('[parse_stats] parsed %s as stats for %s' % (str(stats), pokemon_name))

  return stats


def main(pokedex_url, pokemon_generation_keyword, game_version):
  """
  """
  html_lines = get_html_lines(pokedex_url)
  data = parse_pokedex_html(html_lines, pokemon_generation_keyword)
  data = parse_moves_and_stats(data)

  filename = 'pokedex-%s' % game_version
  export_to_csv(data, filename)
  export_to_json(data, filename)


if __name__ == '__main__':
  main('https://www.serebii.net/brilliantdiamondshiningpearl/sinnohpokedex.shtml', 'pokedex-swsh', 'bdsp')
