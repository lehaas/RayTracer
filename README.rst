.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/raytracer.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/raytracer
    .. image:: https://readthedocs.org/projects/raytracer/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://raytracer.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/raytracer/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/raytracer
    .. image:: https://img.shields.io/pypi/v/raytracer.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/raytracer/
    .. image:: https://img.shields.io/conda/vn/conda-forge/raytracer.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/raytracer
    .. image:: https://pepy.tech/badge/raytracer/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/raytracer
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/raytracer

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

=========
raytracer
=========

   Python implementation of a ray tracer following https://raytracing.github.io/books/RayTracingInOneWeekend.html.


.. _pyscaffold-notes:

Making Changes & Contributing
=============================

This project uses `pre-commit`_, please make sure to install it before making any
changes::

    pip install pre-commit
    cd raytracer
    pre-commit install

It is a good idea to update the hooks to the latest version::

    pre-commit autoupdate

Don't forget to tell your contributors to also install and use pre-commit.

.. _pre-commit: https://pre-commit.com/

Note
====

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.
