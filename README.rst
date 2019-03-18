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


Configuration
=============

Packer Executable
******************

Specify Packer Location
^^^^^^^^^^^^^^^^^^^^^^^
Access to hashicorp `packer`_ executable is needed in order to use `packer.py`_.
When generating commands, if no location is specified, the following defaults are used.

    :\*nix: /usr/local/packer
    :macOS: /usr/local/packer
    :windows: packer.exe

These defaults can be overridden by explicitly setting the location of packer for your environment.


.. code:: python

    PackerExecutable(executable_path="/usr/local/bin/packer")

or

.. code:: python

    PackerExecutable("/usr/local/bin/packer")



Machine Readable Output
^^^^^^^^^^^^^^^^^^^^^^^
Commands are executed with packer's `machine readable format`_ enabled by default.
This can be disabled by setting

.. code:: python

    PackerExecutable(machine_readable=False)




Running Commands
==================
The following commands are currently supported:

* build
* inspect
* validate
* version

Below is the packer.py equivalent of running these `packer CLI commands`_


Configuration
******************

Templates
^^^^^^^^^
Templates are specified by passing their filepath to the command.

.. code:: python

    template = 'tests/templates/test_template1.json'
    PackerExecutable().validate(template)

Templates can also be specified as a string literal.

.. code:: python

    template = """
    {
        "variables": {
            "my_var1": "{{env `key1`}}"
        },
        "builders": [
            {
                "type": "file",
                "content": "Lorem ipsum dolor sit amet {{user `my_var1`}} ",
                "target": "/tmp/packer.test"
            }
        ]
    }
    """
    PackerExecutable().validate(template)


`packerlicious`_ templates can also be used and combined with packer.py.

.. code:: python

    from packerlicious import builder, Template, EnvVar
    from packerpy import PackerExecutable
    var1 = EnvVar("my_var1")
    var2 = EnvVar("my_var2")
    file_builder = builder.File()
    file_builder = builder.File(content="{} more words {}".format(var2.ref().data, var1.ref().data),
                                target="/tmp/packer.test"
                                )
    template = Template()
    template.add_variable([var1, var2])
    template.add_builder(file_builder)
    p = PackerExecutable("/usr/local/bin/packer")
    template_vars = {'my_var1': 'my_val1', 'my_var2': 'my_val2'}
    p.build(template.to_json(),
            var=template_vars
            )


Command Arguments
^^^^^^^^^^^^^^^^^^
`packer CLI commands`_ arguments can be specified by passing them as packer.py method arguments.

    $ packer validate -syntax-only -var "key1=my_value" tests/templates/test_template1.json

.. code:: python

    p = PackerExecutable("/usr/local/bin/packer")
    template = 'tests/templates/test_template1.json'
    p.validate(template,
               syntax_only=True,
               var="key1=my_value"
               )


The following rules are used by packer.py when converting to `packer CLI commands`.

Dashes in Packer Command Option Names
+++++++++++++++++++++++++++++++++++++
If the packer command option has a dash in it, pass it to packer.py with an underscore.

:``-on-error=cleanup``: ``on_error='cleanup'``



Boolean Values and Implicit Value Command Options
+++++++++++++++++++++++++++++++++++++++++++++++++
If the packer command option is either a boolean option or an option with an implicit value, pass it to packer.py as a boolean.

:``-color=false``: ``color=False``
:``-force``: ``force=True``


Repeating Command Options
+++++++++++++++++++++++++++

If the packer command options can be specified multiple times, pass the value as a dictionary to packer.py.
Multiple ``-var`` option is an example of this.

    $   packer build -var 'my_var1=my_val1' -var 'my_var2=my_val2' tests/templates/test_template1.json

.. code:: python

    from packerpy import PackerExecutable
    p = PackerExecutable("/usr/local/bin/packer")
    template = 'tests/templates/test_template1.json'
    template_vars = { 'my_var1': 'my_val1', 'my_var2': 'my_val2' }
    p.build(template,
               var=template_vars
               )


Build
*********
    $   packer build template.json

.. code:: python

    >>> from packerpy import PackerExecutable
    >>> p = PackerExecutable("/usr/local/bin/packer")
    >>> (ret, out, err) = p.build('tests/templates/test_template1.json')
    >>> ret==0
    True
    >>> print(ret)
    0
    >>> print(out)
    b"1552841678,,ui,say,Build 'file' finished.\n1552841678,,ui,say,\\n==> Builds finished. The artifacts of successful builds are:\n1552841678,file,artifact-count,1\n1552841678,file,artifact,0,builder-id,packer.file\n1552841678,file,artifact,0,id,File\n1552841678,file,artifact,0,string,Stored file: /tmp/packer.test \n1552841678,file,artifact,0,files-count,1\n1552841678,file,artifact,0,file,0,/tmp/packer.test \n1552841678,file,artifact,0,end\n1552841678,,ui,say,--> file: Stored file: /tmp/packer.test \n"
    >>> print(err)
    b''


Example of a failed build.

.. code:: python

    >>> from packerpy import PackerExecutable
    >>> p = PackerExecutable("/usr/local/bin/packer")
    >>> bad_template = """{
    ...     "builders": [
    ...         {
    ...             "type": "amazon-ebs",
    ...             "access_key": "..."
    ...         }
    ...     ]
    ... }
    ... """
    >>> (ret, out, err) = p.build(bad_template)
    >>> ret==0
    False
    >>> print(ret)
    1
    >>> print(out)
    b'1552841800,,ui,error,5 error(s) occurred:\\n\\n* ami_name must be specified\\n* ami_name must be between 3 and 128 characters long\\n* An ssh_username must be specified\\n  Note: some builders used to default ssh_username to "root".\\n* A source_ami or source_ami_filter must be specified\\n* An instance_type must be specified\n'
    >>> print(err)
    b''



Inspect
*********
    $   packer inspect template.json

.. code:: python

    >>> from packerpy import PackerExecutable
    >>> p = PackerExecutable("/usr/local/bin/packer")
    >>> (ret, out, err) = p.inspect('tests/templates/test_template1.json')
    >>> ret==0
    True
    >>> print(ret)
    0
    >>> print(out)
    b"1552841499,,ui,say,Optional variables and their defaults:\\n\n1552841499,,template-variable,my_var1,{{env `key1`}},0\n1552841499,,ui,say,  my_var1 = {{env `key1`}}\n1552841499,,ui,say,\n1552841499,,ui,say,Builders:\\n\n1552841499,,template-builder,file,file\n1552841499,,ui,say,  file\n1552841499,,ui,say,\n1552841499,,ui,say,Provisioners:\\n\n1552841499,,ui,say,  <No provisioners>\n1552841499,,ui,say,\\nNote: If your build names contain user variables or template\\nfunctions such as 'timestamp'%!(PACKER_COMMA) these are processed at build time%!(PACKER_COMMA)\\nand therefore only show in their raw form here.\n"
    >>> print(err)
    b''



Validate
*********
    $   packer validate template.json

.. code:: python

    >>> from packerpy import PackerExecutable
    >>> p = PackerExecutable("/usr/local/bin/packer")
    >>> (ret, out, err) = p.validate('tests/templates/test_template1.json')
    >>> ret==0
    True
    >>> print(ret)
    0
    >>> print(out)
    b'1552840497,,ui,say,Template validated successfully.\n'
    >>> print(err)
    b''


Example of a template which failed to validation.

.. code:: python

    >>> from packerpy import PackerExecutable
    >>> p = PackerExecutable("/usr/local/bin/packer")
    >>> bad_template = """{
    ...     "builders": [
    ...         {
    ...             "type": "amazon-ebs",
    ...             "access_key": "..."
    ...         }
    ...     ]
    ... }
    ... """
    >>> (ret, out, err) = p.validate(bad_template)
    >>> ret==0
    False
    >>> print(ret)
    1
    >>> print(out)
    b'1552840892,,ui,error,Template validation failed. Errors are shown below.\\n\n1552840892,,ui,error,Errors validating build \'amazon-ebs\'. 5 error(s) occurred:\\n\\n* ami_name must be specified\\n* ami_name must be between 3 and 128 characters long\\n* An ssh_username must be specified\\n  Note: some builders used to default ssh_username to "root".\\n* A source_ami or source_ami_filter must be specified\\n* An instance_type must be specified\n'
    >>> print(err)
    b''



Version
*********
    $   packer version

.. code:: python

    >>> from packerpy import PackerExecutable
    >>> p = PackerExecutable("/usr/local/bin/packer")
    >>> (ret, out, err) = p.version()
    >>> ret==0
    True
    >>> print(ret)
    0
    >>> print(out)
    b'1552840138,,version,1.0.3\n1552840138,,version-prelease,\n1552840138,,version-commit,c0ddb4a+CHANGES\n1552840138,,ui,say,Packer v1.0.3\n1552840138,,ui,say,\\nYour version of Packer is out of date! The latest version\\nis 1.3.5. You can update by downloading from www.packer.io\n'
    >>> print(err)
    b''



Licensing
=========

packer.py is licensed under the `Apache license 2.0`_.
See `LICENSE`_ for the full license text.




.. _`packer`: https://www.packer.io/
.. _`packer.py`: https://github.com/mayn/packer.py
.. _`packerlicious`: https://github.com/mayn/packerlicious
.. _`machine readable format`: https://www.packer.io/docs/commands/index.html#machine-readable-output
.. _`packer CLI commands`: https://www.packer.io/docs/commands/index.html
.. _`LICENSE`: https://github.com/mayn/packer.py/blob/master/LICENSE
.. _`Apache license 2.0`: https://opensource.org/licenses/Apache-2.0
.. _`BSD 2-Clause license`: http://opensource.org/licenses/BSD-2-Clause
.. _`semantic versioning`: http://semver.org/
