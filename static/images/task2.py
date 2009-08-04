import numpy as np
import scipy
import pylab
import pymorph
import readmagick
from scipy import ndimage
from pylab import cm
import pyslic
dna = readmagick.readimg('dna.jpeg')

TESTING = False
if TESTING:
    def savejet(img, name):
        pass
    def writeimg(img, name):
        pass
else:
    def savejet(img, name):
        img = (img - img.min())/float(img.ptp())*255
        img = img.astype(np.uint8)
        readmagick.writeimg((cm.jet(img)[:,:,:3]*255).astype(np.uint8), name)
    writeimg = readmagick.writeimg

dnaf = ndimage.gaussian_filter(dna, 8)
rmax = pymorph.regmax(dnaf)
pylab.imshow(pymorph.overlay(dna, rmax))
pylab.show()
writeimg(pymorph.overlay(dna, rmax), 'dnaf-rmax-overlay.jpeg')
savejet(dnaf, 'dnaf-8.jpeg')


dnaf = ndimage.gaussian_filter(dna, 16)
rmax = pymorph.regmax(dnaf)
pylab.imshow(pymorph.overlay(dna, rmax))
pylab.show()
writeimg(pymorph.overlay(dna, rmax), 'dnaf-16-rmax-overlay.jpeg')

seeds,nr_nuclei = ndimage.label(rmax)
print nr_nuclei

T = pyslic.thresholding.otsu(dnaf)
dist = ndimage.distance_transform_edt(dnaf > T)
dist = dist.max() - dist
dist = ((dist - dist.min())/float(dist.ptp())*255).astype(np.uint8)
pylab.imshow(dist)
pylab.show()

savejet(dist, 'dnaf-16-dist.jpeg')

nuclei = pymorph.cwatershed(dist, seeds)
pylab.imshow(nuclei)
pylab.show()
savejet(nuclei, 'nuclei-segmented.png')


whole = pyslic.segmentation.gvoronoi(nuclei)
pylab.imshow(whole)
pylab.show()
savejet(whole, 'whole-segmented.png')

borders = np.zeros(nuclei.shape, np.bool)
borders[ 0,:] = 1
borders[-1,:] = 1
borders[:, 0] = 1
borders[:,-1] = 1
at_border = np.unique(nuclei[borders])
for obj in at_border:
    whole[whole == obj] = 0
pylab.imshow(whole)
pylab.show()
savejet(whole, 'whole-segmented-filtered.png')
