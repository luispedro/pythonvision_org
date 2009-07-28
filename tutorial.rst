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
    import pylab
    import pymorph
    import readmagick
    from scipy import ndimage

