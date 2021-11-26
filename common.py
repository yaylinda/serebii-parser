import csv
import json


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
  with open('data/%s.json' % pokemon_genfilenameeration_keyword, 'w') as file:
    json.dump(data, file)

  print('[export_to_json] done writing to json')