
from PIL import Image

filename = 'apple'
gry_srf = Image.open('images/' + filename + '.png').convert('LA')
gry_srf.save('images/gry_' + filename + '.png')