from parser import parse


if __name__ == '__main__':
  parse(
    [
      'https://www.serebii.net/brilliantdiamondshiningpearl/sinnohpokedex.shtml',
      'https://www.serebii.net/brilliantdiamondshiningpearl/otherpokemon.shtml'
    ], 
    'pokedex-swsh', 
    'swordshield',
    'bdsp'
  )