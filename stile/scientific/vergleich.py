# Erzeugt Vergleichsbild Original | v2 und Crops in voller Auflösung
from PIL import Image
B='/tmp/claude-0/-home-user-fragen-allgemein/0523a428-572b-5d43-9560-e7907758c764/scratchpad/stile'
o=Image.open(f'{B}/assets/originals/Scientific.png').convert('RGB'); v=Image.open(f'{B}/out2/Scientific_v2.png').convert('RGB')
w,h=o.size; c=Image.new('RGB',(w*2+40,h),'#888'); c.paste(o,(0,0)); c.paste(v,(w+40,0))
c.resize((c.width//2,c.height//2)).save(f'{B}/out2/Scientific_vergleich.jpg',quality=88)
crops={'hero':(250,700,1300,2000),'rechts_oben':(760,480,1536,1100),'links':(0,500,620,1450),'unten':(0,1850,1536,2752),'kopf':(0,60,1536,700),'rechts_mitte':(1100,980,1536,1800)}
for k,b in crops.items(): v.crop(b).save(f'{B}/out2/_crops_sci/v2_{k}.png')
print('ok')
