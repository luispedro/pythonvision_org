import numpy as np
import scipy
import pylab
import pymorph
import readmagick
import pit
from scipy import ndimage
dna = readmagick.readimg('dna.jpeg')

TESTING = True
if TESTING:
    def savejet(img, name):
        pass
else:
    def savejet(img):
        readmagick.writeimg((cm.jet(dnaf)[:,:,:3]*255).astype(np.uint8), name)
    
pylab.imshow(dna)
pylab.show()
savejet(dna, 'dna-coloured.jpeg')

pylab.imshow(dna)
pylab.gray()
pylab.show()

print dna.shape
print dna.dtype
print dna.max()
print dna.min()

pylab.imshow(dna // 2)
pylab.show()

T = pit.thresholding.otsu(dna)
pylab.imshow(dna > T)
pylab.show()

dnaf = ndimage.gaussian_filter(dna, 8)
T = pit.thresholding.otsu(dnaf)
pylab.imshow(dnaf > T)
pylab.show()

labeled,nr_objects = ndimage.label(dnaf > T)
print nr_objects
pylab.imshow(labeled)
pylab.jet()
pylab.show()
savejet(labeled, 'dnaf-otsu-labeled.jpeg')
