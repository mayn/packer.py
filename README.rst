==============
packer.py
==============
.. image:: https://img.shields.io/pypi/v/packer.py.svg
    :target: https://pypi.python.org/pypi/packer.py

.. image:: https://travis-ci.org/mayn/packer.py.svg?branch=master
    :target: https://travis-ci.org/mayn/packer.py

.. image:: https://ci.appveyor.com/api/projects/status/n1627wlm52q12db8/branch/master?svg=true
    :target: https://ci.appveyor.com/project/mayn/packer-py

.. image:: https://coveralls.io/repos/github/mayn/packer.py/badge.svg?branch=master
    :target: https://coveralls.io/github/mayn/packer.py



About
=====

packer.py - python library for interacting with hashicorp `packer`_ CLI executable.

Project follows `semantic versioning`_ , v0.x.x API should be considered unstable, API will change frequently, please plan accordingly.



Installation
============
packer.py can be installed via pip:

.. code:: sh

    $ pip install packer.py


Examples
========

Below is the packer.py equivalent of running `packer CLI commands`_

.. code:: python

    >>> from packerpy import PackerExecutable
    >>>
    >>> PackerExecutable().validate('/path/to/good_template.json')
    (0, '1521843453,,ui,say,Template validated successfully.\n', '')
    >>>
    >>> PackerExecutable().validate('/path/to/bad_template.json')
    (1, "1521843610,,ui,error,Template validation failed. Errors are shown below.\\n\n1521843610,,ui,error,Errors validating build 'amazon-ebs'. 1 error(s) occurred:\\n\\n* Bad script 'setup_things.sh': stat setup_things.sh: no such file or directory\n", '')
    >>>
    >>> PackerExecutable().validate('/path/to/bad_template.json', syntax_only=True)
    (0, '1521843659,,ui,say,Syntax-only check passed. Everything looks okay.\n', '')
    >>>
    >>> PackerExecutable(config={'stdout': None }).version()
    1521843095,,version,0.10.2
    1521843095,,version-prelease,
    1521843095,,version-commit,141440147f75b5d1ca500c133a5f879c226f2b10
    1521843095,,ui,say,Packer v0.10.2
    1521843095,,ui,say,
    1521843095,,ui,say,Your version of Packer is out of date! The latest version\nis 1.2.1. You can update by downloading from www.packer.io
    (0, None, '')
    >>>
    >>> PackerExecutable(config={'executable_path': '/path/to/packer_1.2.1' , 'stdout': None }).version()
    1521848321,,version,1.2.1
    1521848321,,version-prelease,
    1521848321,,version-commit,3d5592d04
    1521848321,,ui,say,Packer v1.2.1
    (0, None, '')



Currently supported Packer CLI commands
======================================

- build
- inspect
- validate
- version


Licensing
=========

packer.py is licensed under the `Apache license 2.0`_.
See `LICENSE`_ for the full license text.




.. _`packer`: https://www.packer.io/
.. _`packer CLI commands`: https://www.packer.io/docs/commands/index.html
.. _`LICENSE`: https://github.com/mayn/packer.py/blob/master/LICENSE
.. _`Apache license 2.0`: https://opensource.org/licenses/Apache-2.0
.. _`BSD 2-Clause license`: http://opensource.org/licenses/BSD-2-Clause
.. _`semantic versioning`: http://semver.org/
