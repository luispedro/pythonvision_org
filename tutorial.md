---
title: Tutorial
permalink: basic-tutorial/
categories: tutorials
---

Python Image Tutorial
=====================

More than a HOWTO, this document is a HOW-DO-I use Python to do my image
processing tasks. Image processing means many things to many people, so
I will use a couple of examples from my research to illustrate.

Introduction
------------

### Basic Software

I am going to assume that you have installed the following:
:   -   Python 2.5, 2.6, or 2.7 (avoid 3.0 or 3.1—too new)
    -   numpy
    -   matplotlib
    -   mahotas
    -   ipython

Under Linux, you can just install your distribution’s packages (install at
least python-numpy, python-numpy-dev, python-matplotlib, ipython). Under
Windows or Mac OS, this is more complicated. Fortunately, some people have done
the work for us and built packages that have this. Install either Python(xy) or
the [Anaconda Distribution](http://continuum.io/downloads) (actually this works
on Linux too, if you prefer this method).


First Task: Counting Nuclei
---------------------------

Our first task will be to take this image and count the number of nuclei (you
can click on the image and download it to try this at home):

[![image](/media/files/images/dna.jpeg){:.resized-image style="width: 400px"}](/media/files/images/dna.jpeg)

Before we start, let us import the needed files. For all code examples in this
tutorial, I am going to assume that you typed the following before coming to
the example:

    import numpy as np
    import pylab
    import mahotas as mh


These are the packages listed above (except *pylab*, which is a part of
matplotlib).

In Python, there is image processing tools spread across many packages
instead of a single package. Fortunately, they all work on the same data
representation, the numpy array [^1]. A numpy array is, in our case,
either a two dimensional array of integers (height x width) or, for
colour images, a three dimensional array (height x width x 3 or height x
width x 4, with the last dimension storing (red,green,blue) triplets or
(red,green,blue,alpha) if you are considering transparency).

The first step is to get the image from disk into a memory array:

    dna = mh.imread('dna.jpeg')

Playing Around
--------------

In interactive mode (i.e., if you are running this inside *ipython*), you can
see the image:

    pylab.imshow(dna)
    pylab.show()

If you set up things in a certain way, you might not need the *pylab.show()*
line. For most installations, you can get this by running *ipython -pylab* on
the command line [^2].

You might be surprised that the image does not look at all like the one above.
It will probably look like:

[![image](/media/files/images/dna-coloured.jpeg){:.resized-image style="width: 400px"}](/media/files/images/dna-coloured.jpeg)

This is because, by default, pylab shows images as a heatmap. You can see the
more traditional grey-scale image by switching the colormap used. Instead of
the default *jet* colourmap, we can set it to the *gray* one, which is the
traditional greyscale representation:

    pylab.imshow(dna)
    pylab.gray()
    pylab.show()

We can explore our array a bit more:

    print dna.shape
    print dna.dtype
    print dna.max()
    print dna.min()

Since dna is just a numpy array, we have access to all its attributes
and methods (see the [numpy documentation](http://docs.numpy.org/) for
complete information).

The above code prints out:

    (1024, 1344)
    uint8
    252
    0

The shape is 1024 pixels high and 1344 pixels across (recall that the
convention is the matrix convention: *height x width*). The type is *uint8*,
i.e., unsigned 8-bit integer. The maximum value is 252 and the minimum value is
0 [^3].

    pylab.imshow(dna // 2)
    pylab.show()

Here, we are displaying an image where all the values have been divided by 2
[^4]. And the displayed image is still the same! In fact, pylab
contrast-stretches our images before displaying them.

Some Actual Work
----------------

Here’s the first idea for counting the nuclei. We are going to threshold the
image and count the number of objects.

    T = mh.thresholding.otsu(dna)
    pylab.imshow(dna > T)
    pylab.show()

Here, again, we are taking advantage of the fact that dna is a numpy array and
using it in logical operations (*dna \> T*). The result is a numpy array of
booleans, which pylab shows as a black and white image (or red and blue if you
have not previously called *pylab.gray()*).

[![image](/media/files/images/dna-otsu.jpeg){.resized-image style="width: 400px"}](/media/files/images/dna-otsu.jpeg)

This isn’t too good. The image contains many small objects. There are a
couple of ways to solve this. A simple one is to smooth the image a bit
using a Gaussian filter.

    dnaf = mh.gaussian_filter(dna, 8)
    T = mh.thresholding.otsu(dnaf)
    pylab.imshow(dnaf > T)
    pylab.show()

The function *mh.gaussian\_filter* takes an image and the standard
deviation of the filter (in pixel units) and returns the filtered image.
We are jumping from one package to the next, calling *mahotas* to filter
the image and to compute the threshold, using *numpy* operations to create a
thresholded images, and *pylab* to display it, but everyone works with *numpy
arrays*. The result is much better:

[![image](/media/files/images/dnaf-otsu.jpeg){.resized-image style="width: 400px"}](/media/files/images/dnaf-otsu.jpeg)

We now have some merged nuclei (those that are touching), but overall
the result looks much better. The final count is only one extra function
call away:

    labeled,nr_objects = mh.label(dnaf > T)
    print nr_objects
    pylab.imshow(labeled)
    pylab.jet()
    pylab.show()

We now have the number of objects in the image (*18*), and we also
displayed the *labeled* image. The call to *pylab.jet()* just resets the
colourmap to *jet* if you still had the greyscale map active.

[![image](/media/files/images/dnaf-otsu-labeled.jpeg){.resized-image style="width: 400px"}](/media/files/images/dnaf-otsu-labeled.jpeg)

We can explore the *labeled* object. It is an integer array of exactly
the same size as the image that was given to *mh.label()*. It’s
value is the label of the object at that position, so that values range
from 0 (the background) to *nr\_objects*.

Second Task: Segmenting the Image
---------------------------------

The previous result was acceptable for a first pass, but there were
still nuclei glued together. Let’s try to do better.

Here is a simple, traditional, idea:

1.  smooth the image
2.  find regional maxima
3.  Use the regional maxima as seeds for watershed

### Finding the seeds

Here’s our first try:

    dnaf = mh.gaussian_filter(dna, 8)
    rmax = mh.regmax(dnaf)
    pylab.imshow(mh.overlay(dna, rmax))
    pylab.show()

The `mh.overlay()` returns a colour image with the grey level
component being given by its first argument while overlaying its second
argument as a red channel. The result doesn’t look so good:

[![image](/media/files/images/dnaf-rmax-overlay.jpeg){.resized-image style="width: 400px"}](/media/files/images/dnaf-rmax-overlay.jpeg)

If we look at the filtered image, we can see the multiple maxima:

[![image](/media/files/images/dnaf-8.jpeg){.resized-image style="width: 400px"}](/media/files/images/dnaf-8.jpeg)

After a little fiddling around, we decide to try the same idea with a
bigger sigma value:

    dnaf = mh.gaussian_filter(dna, 16)
    rmax = mh.regmax(dnaf)
    pylab.imshow(mh.overlay(dna, rmax))

Now things look much better.

[![image](/media/files/images/dnaf-16-rmax-overlay.jpeg){.resized-image style="width: 400px"}](/media/files/images/dnaf-16-rmax-overlay.jpeg)

We can easily count the number of nuclei now:

    seeds,nr_nuclei = mh.label(rmax)
    print nr_nuclei

Which now prints `22`.

### Watershed

We are going to apply watershed to the distance transform of the
thresholded image:

    T = mh.thresholding.otsu(dnaf)
    dist = mh.distance(dnaf > T)
    dist = dist.max() - dist
    dist -= dist.min()
    dist = dist/float(dist.ptp()) * 255
    dist = dist.astype(np.uint8)
    pylab.imshow(dist)
    pylab.show()

[![image](/media/files/images/dnaf-16-dist.jpeg){.resized-image style="width: 400px"}](/media/files/images/dnaf-16-dist.jpeg)

After we contrast stretched the `dist` image, we can call
`mh.cwatershed` to get the final result [^5] (the colours in the
image come from it being displayed using the *jet* colourmap):

    nuclei = mh.cwatershed(dist, seeds)
    pylab.imshow(nuclei)
    pylab.show()

[![image](/media/files/images/nuclei-segmented.png){.resized-image style="width: 400px"}](/media/files/images/nuclei-segmented.png)

It’s easy to extend this segmentation to the whole plane by using
generalised Voronoi (i.e., each pixel gets assigned to its nearest
nucleus):

    whole = mh.segmentation.gvoronoi(nuclei)
    pylab.imshow(whole)
    pylab.show()

[![image](/media/files/images/whole-segmented.png){.resized-image style="width: 400px"}](/media/files/images/whole-segmented.png)

Often, we want to provide a little quality control and remove those
cells whose nucleus touches the border. So, let’s do that:

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

This is a bit more advanced, so let’s go line by line:

    borders = np.zeros(nuclei.shape, np.bool)

This builds an array of zeros, with the same shape as nuclei and of type
`np.bool`.

    borders[ 0,:] = 1
    borders[-1,:] = 1
    borders[:, 0] = 1
    borders[:,-1] = 1

This sets the borders of that array to `True` (`1` is often synonymous
with `True`).

    at_border = np.unique(nuclei[borders])

`nuclei[borders]` gets the values that the nuclei array has where
`borders` is `True` (i.e., the value at the borders), then `np.unique`
returns only the unique values (in our case, it returns
`array([ 0,  1,  2,  3,  4,  6,  8, 13, 20, 21, 22])`).

    for obj in at_border:
        whole[whole == obj] = 0

Now we iterate over the border objects and everywhere that `whole` takes
that value, we set it to zero [^5]. We now get our final result:

[![image](/media/files/images/whole-segmented-filtered.png){.resized-image style="width: 400px"}](/media/files/images/whole-segmented-filtered.png)

Learn More
----------

You can explore the documentation for numpy at
[docs.numpy.org](http://docs.numpy.org/). You will find documentation
for scipy at the same location. For mahotas, you can look at its
[online documentation](http://mahotas.readthedocs.org/).

However, Python has a really good online documentation system. You can
invoke it with `help(name)` or, if you are using *ipython* just by
typing a question mark after the name of the function you are interested
in. For example, if you want details on the *mahotas.regmax* function:

    In [2]: mh.regmax?
    Type:        function
    String form: <function regmax at 0x7fda440301b8>
    File:        /home/luispedro/.anaconda/lib/python2.7/site-packages/mahotas/morph.py
    Definition:  mh.regmax(f, Bc=None, out=None, output=None)
    Docstring:
    filtered = regmax(f, Bc={3x3 cross}, out={np.empty(f.shape, bool)})

    Regional maxima. This is a stricter criterion than the local maxima as
    it takes the whole object into account and not just the neighbourhood
    defined by ``Bc``::

        0 0 0 0 0
        0 0 2 0 0
        0 0 2 0 0
        0 0 3 0 0
        0 0 3 0 0
        0 0 0 0 0

    The top 2 is a local maximum because it has the maximal value in its
    neighbourhood, but it is not a regional maximum.


    Parameters
    ----------
    f : ndarray
    Bc : ndarray, optional
        structuring element
    out : ndarray, optional
        Used for output. Must be Boolean ndarray of same size as `f`

    Returns
    -------
    filtered : ndarray
        boolean image of same size as f.

    See Also
    --------
    locmax : function
        Local maxima. The local maxima are a superset of the regional maxima



All the projects listed above have very complete documentation. You can
also get information on methods of an object by typing, in `ipython`,
something like `img.ptp?` where `img` is a numpy array to get
information on the `ptp` function (which returns
`img.max() - img.min()`, by the way).

Footnotes
---------

[^1]: Strictly speaking, this is not true. There is also the Python
    Imaging Library (PIL), which is not the same as numpy (in fact, you
    have to convert back and forth). For the kind of image processing
    that I will be talking about, this does not matter as PIL is
    targeted towards other types of image manipulation.

[^2]: This is so useful that, if you are familiar with the shell, you
    might consider setting up an alias *pylab=ipython -pylab*. The pylab
    argument also imports several numerical packages (including numpy,
    which is named np, scipy, and pylab).

[^3]: For the curious, I contrast stretched the image for this tutorial.

[^4]: If you are not too familiar with Python, you might not be
    comfortable with the *dna // 2* notation. While 4 divided by 2 is
    obviously 2, it is not always clear what 3 divided by 2 should be.
    The *integer division* answer is that it’s 1 (with remainder 1),
    while the *floating-point division* answer is that it is 1.5. In
    Python, the *//* operator always gives you the integer division,
    while */* used to give you integer division and now gives you the
    floating-point one.
[^5]: In practice this is not the most efficient way to do this. The
    same operation can be done much faster using
    `for obj in at_border: whole *= (whole != obj)`. Multiplying or
    adding boolean arrays might seem strange at first, but it’s a very
    useful idiom.

