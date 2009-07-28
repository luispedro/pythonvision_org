=======================
Python Image Tutorial
=======================


More than a HOWTO, this document is a HOW-DO-I use Python to do my image processing tasks. Image processing means many things to many people, so I will use a couple of examples from my research to illustrate.

Introduction
~~~~~~~~~~~~

Basic Software
---------------

I am going to assuyme that you have installed the following:
    - Python 2.5, 2.6, or 2.7 (avoid 3.0 or 3.1---too new)
    - numpy
    - scipy
    - matplotlib
    - ipython

Under Linux, you can just install your distribution's packages (install at least python-numpy, python-scipy, python-numpy-dev, python-matplotlib, ipython). Under Windows or Mac OS, this is more complicated. Fortunately, some people have done the work for us and built packages that have this. Install either Python xy or the Enthought Python Distribution (actually this works on Linux too, if you prefer this method).

Other Software
--------------

You will need one of the following packages:
    - Python Image Library
    - readmagick

You should also download and install pymorph.

First Task: Counting Nuclei
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Our first task will be to take this image and count the number of nuclei:

.. image:: static/images/dna.jpeg
   :width: 25%
   :align: center

Before we start, let us import the needed files. For all code examples in this tutorial, I am going to assume that you typed the following before coming to the example:

.. code-block:: python

    import numpy as np
    import scipy
    import pylab
    import pymorph
    import readmagick
    from scipy import ndimage

In Python, there is image processing tools spread across many packages instead of a single package. Fortunately, they all work on the same data representation, the numpy array [#]_. A numpy array is, in our case, either a two dimensional array of integers (height x width) or, for colour images, a three dimensional array (height x width x 3 or height x width x 4, with the last dimension storing (red,green,blue) triplets or (red,green,blue,alpha) if you are considering transparency).

The first step is to get the image from disk into a memory array:

.. code-block:: python

   dna = readmagick.readimg('dna.jpeg')

If you don't have readmagick, you can use:

.. code-block:: python

   dna = scipy.misc.pilutil.imread('dna.jpeg')

Readmagick is not as standard as scipy, but it handles more file types.

Playing Around
~~~~~~~~~~~~~~

In interactive mode (i.e., if you are running this inside *ipython*), you can see the image:

.. code-block:: python

   pylab.imshow(dna)
   pylab.show()

If you set up things in a certain way, you might not need the *pylab.show()* line. For most installations, you can get this by running *ipython -pylab* on the command line [#]_.

You might be surprised that the image does not look at all like the one above. It will probably look like:

.. image:: static/images/dna-coloured.jpeg
    :width: 25%
    :align: center

This is because, by default, pylab shows images as a heatmap. You can see the more traditional grey-scale image by switching the colormap used:

.. code-block:: python

    pylab.imshow(dna)
    pylab.gray()
    pylab.show()

We can explore our array a bit more:

.. code-block:: python

    print dna.shape
    print dna.dtype
    print dna.max()
    print dna.min()

Since dna is just a numpy array, we have access to all its attributes and methods (see the `numpy documentation`_ for complete information).

.. _`numpy documentation`: http://docs.numpy.org/

The above code prints out:

::

    (1024, 1344)
    uint8
    252
    0

The shape is 1024 pixels high and 1344 pixels across (recall that the convention is the matrix convention: *height x width*). The type is *uint8*, i.e., unsigned 8-bit integer. The maximum value is 252 and the minimum value is 0 [#]_. 

.. code-block:: python

    pylab.imshow(dna // 2)
    pylab.show()

Here, we are displaying an image where all the values have been divided by 2 [#]_. And the displayed image is still the same! In fact, pylab contrast-stretches our images before displaying them.


Some Actual Work
~~~~~~~~~~~~~~~~

Here's the first idea for counting the nuclei. We are going to threshold the image and count the number of objects.

# FIXME: OTSU IS NOT A PART OF ANY PACKAGE!!!

.. code-block:: python

    T = otsu(dna)
    pylab.imshow(dna > T)
    pylab.show()

Here, again, we are taking advantage of the fact that dna is a numpy array and using it in logical operations (*dna > T*). The result is a numpy array of booleans, which pylab shows as a black and white image (or red and blue if you have not previously called *pylab.gray()*).

.. image:: static/images/dna-otsu.jpeg
   :width: 25%
   :align: center


This isn't too good. The image contains many small objects. There are a couple of ways to solve this. A simple one is to smooth the image a bit using a Gaussian filter.

.. code-block:: python

   dnaf = ndimage.gaussian_filter(dna, 8)
   T = otsu(dnaf)
   pylab.imshow(dnaf > T)
   pylab.show()

The function *ndimage.gaussian_filter* takes an image and the standard deviation of the filter (in pixel units) and returns the filtered image. We are jumping from one package to the next, calling *ndimage* to filter the image, *FIXME* to compute the threshold and *pylab* to display it, but everyone works with *numpy arrays*. The result is much better:

.. image:: static/images/dnaf-otsu.jpeg
   :width: 25%
   :align: center

We now have some merged nuclei (that were previously touching), but overall the result looks much better. The final count is only one extra function call away:

.. code-block:: python

   labeled,nr_objects = ndimage.label(dnaf > T)
   print nr_objects
   pylab.imshow(labeled)
   pylab.jet()
   pylab.show()

We now have the number of objects in the image (*18*), and we also displayed the *labeled* image. The call to *pylab.jet()* just resets the colourmap to *jet* if you still had the greyscale map active.


.. image:: static/images/dnaf-otsu-labeled.jpeg
   :width: 25%
   :align: center

We can explore the *labeled* object. It is an integer array of exactly the same size as the image that was given to *ndimage.label()*. It's value is the label of the object at that position, so that values range from 0 (the background) to *nr_objects*.

Footnotes
~~~~~~~~~


.. [#] Strictly speaking, this is not true. There is also the Python Imaging Library (PIL), which is not the same as numpy (in fact, you have to convert back and forth). For the kind of image processing that I will be talking about, this does not matter as PIL is targetted towards other types of image manipulation.

.. [#] This is so useful that, if you are familiar with the shell, you might consider setting up an alias *pylab=ipython -pylab*. The pylab argument also imports several numerical packages (including numpy, which is named np, scipy, and pylab).

.. [#] For the curious, I contrast stretched the image for this tutorial.

.. [#] If you are not too familiar with Python, you might not be confortable with the *dna // 2* notation. While 4 divided by 2 is obviously 2, it is not always clear what 3 divided by 2 should be. The *integer division* answer is that it's 1 (with remainder 1), while the *floating-point division* answer is that it is 1.5. In Python, the *//* operator always gives you the integer division, while */* used to give you integer division and now gives you the floating-point one.

