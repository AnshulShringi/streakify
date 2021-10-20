Streakify
=========

Streakify helps you create and maintain long-term positive habits in your life. Collaborate with friends to build great habits together.

Streakify is a simple and user-friendly habit tracker and self-improvement app that helps plan your daily habits, track goals and develop your intellect & productivity. Join our science-based habit-building journeys to embrace a fabulous life-changing routine.

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style

:License: GPL-3.0

Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **superuser account**, use this command::

    $ python manage.py createsuperuser


Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy streakify

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest


Celery
^^^^^^

This app comes with Celery.

To run a celery worker:

.. code-block:: bash

    cd streakify
    celery -A config.celery_app worker -l info

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.



The app can be installed from:
------------------------------
https://play.google.com/store/apps/details?id=com.streakify.android
