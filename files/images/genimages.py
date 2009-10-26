import numpy as np
import pyslic
import pickle
import readmagick
imgs = pyslic.image.io.auto_detect_load('/media/TOSHIBA EXT/090721MFLPC_EB1')
B12 = [img for img in imgs if img.label == 'B12']
img = B12[18]
pickle.dump(img, file('original.images.pp','w'))
composite = img.composite()
def write(img, name):
    transformed = (img - img.min()).astype(float)/img.ptp()
    transformed = (transformed * 255).astype(np.uint8)
    readmagick.writeimg(transformed, name)
write(composite, 'composite.jpeg')
write(img.get('dna'), 'dna.jpeg')
write(img.get('protein'), 'protein.jpeg')

