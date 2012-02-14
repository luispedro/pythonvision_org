title: Mahotas 0.7.2
slug: mahotas-072
timestamp: Feb 14 2012 12:14
categories: pythonvision mahotas
author: Luis Pedro Coelho <luis@luispedro.org>
---

I am pleased to announce a new version of mahotas, my computer vision package 
for mahotas.

This is a minor release, but it fixes a few important bugs and adds the 
``gaussian_filter`` function as well as ``as_rgb`` which is very helpful for
interactive use::

    red = ...
    blue = ...

    imshow(mahotas.as_rgb(red, None, blue))

This is exactly the same as::

    import numpy as np
    imshow(np.dstack([
            mahotas.stretch(red),
            np.zeros(red.shape, dtype=np.uint8),
            mahotas.stretch(blue)
            ])

but as a single function call.
