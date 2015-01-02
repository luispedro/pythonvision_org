---
title: Contribute
author: Luis Pedro Coelho <lpc@cmu.edu>
permalink: contribute.html
categories: pythonvision
---

=================
How to Contribute
=================

Pythonvision wants your help! Write tutorials, introduce your software, write
about your experience using Python. We have a page for `ideas
</contribute/ideas>`_, but we welcome your own.

Step by step with github
------------------------

1. Get a `github <http://www.github.com>`_ account (they're free).
2. Fork the `pythonvision_org <http://www.github.com/luispedro/pythonvision_org>`_ project.
3. Edit it. This can even be done directly as a text box on the github project page. Just like a wiki.
4. Send me a pull request or an `email <mailto:lpc@cmu.edu>`_.

Of course, you can just use a local fork with git and email me.

Editing pythonvision.org
------------------------

This is a `django-gitcms <http://luispedro.org/software/git-cms>`_ website.

There are two main content types:
- pages (they have a fixed URL)
- blog posts (they show up in the `blog </blog>`_ and in the RSS feed). 

Once you've decided what to do, just create a new file in the appropriate
directory. Let's create a new post, for example:

1. Create a new file under ``content/simpleblog/``. It *does not matter* what
the file is called, or what organisation you pick. For simplicity, I use a date based approach.
2. So, create the file ``content/simpleblog/2010/April/my_post.rst``
3. Edit it to look like this:

::

    title: Post
    slug: post
    timestamp: 2010-04-07 9:01
    categories: example
    author: Me <my@email.org>
    status: draft
    ---

    My Post
    -------

    Subtitle
    ........

    This is the best thing ever!


It has two parts:

1. A header (terminated by ``\n---\n``) which is of the form *property: value*.
2. Content in reStructured Text format.

The content for a blogpost needs the following fields:

1. title: post title
2. slug: a short string that is suitable for URL use
3. timestamp: when this is published
4. categories: this is a space separated list of categories (the list must
   match the `categories </categories>`_).
5. author: Use ``Name <email>`` format.
6. status: Right now, it only matters whether it is *published*, in which case
   it shows up; or not, in which case it doesn't.

Note that it is the ``timestamp`` field that decides when a post was published
and where it appears if viewed by date.

