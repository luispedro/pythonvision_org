---
title: Frequently Asked Questions
author: Luis Pedro Coelho <lpc@cmu.edu>
permalink: faq/
categories: pythonvision
---

# Frequently Asked Questions

## How does `label()` work?

We could be talking about `ndimage.label()` or some other implementation. In
general, though, these functions take a binary image and return a labeled
image. That is, they will return an integer image where the first region will
have pixel value 1, the second region will have pixel value 2, ....

