wire-protocol
=============

|Build Status| |codecov| |Code Climate| |Issue Count|

|Documentation Status|

Android Debug Bridge (ADB) Wire Protocol

Status
------

This project is actively maintained and under development.

Installation
------------

To install wire-protocol from
`pip <https://pypi.python.org/pypi/pip>`__:

.. code:: bash

       $ pip install adbwp

To install wire-protocol from source:

.. code:: bash

       $ git clone git@github.com:adbpy/wire-protocol.git
       $ cd wire-protocol && python setup.py install

Goals/Scope
-----------

A standalone library that can be used for building protocol objects
while remaining transport/application protocol agnostic. The wire
protocol should care about:

-  Byte layout on the wire
-  Model representation of Messages (header + payload)
-  Provide simple API that convert bytes to/from models

The wire protocol should not care, nor have concept of:

-  Synchronous vs. Asynchronous
-  TCP, UDP, USB
-  Sequence of messages required to complete a connection “handshake”
-  Cryptography required to verify endpoints
-  Anything else not explicitly mentioned above…

Contributing
------------

If you would like to contribute, simply fork the repository, push your
changes and send a pull request. Pull requests will be brought into the
``master`` branch via a rebase and fast-forward merge with the goal of
having a linear branch history with no merge commits.

License
-------

`Apache 2.0 <LICENSE>`__

.. |Build Status| image:: https://travis-ci.org/adbpy/wire-protocol.svg?branch=master
   :target: https://travis-ci.org/adbpy/wire-protocol
.. |codecov| image:: https://codecov.io/gh/adbpy/wire-protocol/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/adbpy/wire-protocol
.. |Code Climate| image:: https://codeclimate.com/github/adbpy/wire-protocol/badges/gpa.svg
   :target: https://codeclimate.com/github/adbpy/wire-protocol
.. |Issue Count| image:: https://codeclimate.com/github/adbpy/wire-protocol/badges/issue_count.svg
   :target: https://codeclimate.com/github/adbpy/wire-protocol
.. |Documentation Status| image:: https://readthedocs.org/projects/wire-protocol/badge/?version=latest
   :target: http://wire-protocol.readthedocs.io/en/latest/?badge=latest
