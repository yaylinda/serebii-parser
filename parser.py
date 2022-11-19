import time
from common import get_html_lines, export_to_csv, export_to_json, parse_moves


def parse_pokedex_html(html_lines, pokemon_detail_page_url_prefix):
  """
  """
  data = []
  
  print('[parse_pokedex_html] parsing %d lines of HTML' % len(html_lines))

  parsing_pokemon_link = False
  parse_pokemon_link_prefix = '<a href="/%s/' % pokemon_detail_page_url_prefix

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


def add_additional_data(original_data, pokemon_detail_page_url_prefix, pokemon_img_src_prefix, game_version):
  """
  """
  data = []

  for datum in original_data:
    pokemon_page_html_lines = get_html_lines('https://www.serebii.net' + datum['pokemon_url'])
    pokemon_name = datum['name']
    datum['moves'] = parse_moves(pokemon_name, pokemon_page_html_lines, game_version)
    datum['stats'] = parse_stats(pokemon_name, pokemon_page_html_lines)
    datum['types'] = parse_types(pokemon_name, pokemon_page_html_lines)
    datum['image_src'] = parse_image_src(pokemon_name, pokemon_page_html_lines, pokemon_img_src_prefix)
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


def parse_types(pokemon_name, lines):
  types = []

  is_parsing_types = False
  start_parse_types_line_prefix = '<td class="tooltabcon">'
  end_parse_types_prefix = '</td>'
  type_line_prefix = 'href="/pokedex-sm/'
  type_line_suffix = '.shtml'

  for line in lines:
    if not is_parsing_types and start_parse_types_line_prefix in line:
      is_parsing_types = True

    elif is_parsing_types and type_line_prefix in line and type_line_suffix in line:
      if 'a> <a' in line:
        sub_lines = line.split('a> <a')
        for s in sub_lines:
          types.append(s.split(type_line_prefix)[1].split(type_line_suffix)[0])
      else:
        types.append(line.split(type_line_prefix)[1].split(type_line_suffix)[0])

    elif is_parsing_types and end_parse_types_prefix in line:
      is_parsing_types = False

  print('[parse_types] parsed %s as types for %s' % (str(types), pokemon_name))

  return types


def parse_image_src(pokemon_name, lines, pokemon_img_src_prefix):
  image_src = ''

  line_prefix = '/%s/pokemon/' % pokemon_img_src_prefix
  line_suffix = '.png'

  for line in lines:

    if ('<img src="/%s/pokemon/' % pokemon_img_src_prefix) in line and line_suffix in line:
      image_src = line_prefix + line.split(line_prefix)[1].split(line_suffix)[0] + line_suffix
      break
  
  print('[parse_image_src] parsed %s as img_src for %s' % (image_src, pokemon_name))
  
  return image_src


def parse(pokedex_urls, pokemon_detail_page_url_prefix, pokemon_img_src_prefix, game_version):
  """
  """
  all_data = []
  for url in pokedex_urls:
    html_lines = get_html_lines(url)
    data = parse_pokedex_html(html_lines, pokemon_detail_page_url_prefix)
    data = add_additional_data(data, pokemon_detail_page_url_prefix, pokemon_img_src_prefix, game_version)
    all_data = all_data + data

  filename = 'pokedex-%s' % game_version
  export_to_csv(all_data, filename)
  export_to_json(all_data, filename)
