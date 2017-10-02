# wire-protocol

[![Build Status](https://travis-ci.org/adbpy/wire-protocol.svg?branch=master)](https://travis-ci.org/adbpy/wire-protocol)
[![Test Coverage](https://codeclimate.com/github/adbpy/wire-protocol/badges/coverage.svg)](https://codeclimate.com/github/adbpy/wire-protocol/coverage)
[![Code Climate](https://codeclimate.com/github/adbpy/wire-protocol/badges/gpa.svg)](https://codeclimate.com/github/adbpy/wire-protocol)
[![Issue Count](https://codeclimate.com/github/adbpy/wire-protocol/badges/issue_count.svg)](https://codeclimate.com/github/adbpy/wire-protocol)

[![Updates](https://pyup.io/repos/github/adbpy/wire-protocol/shield.svg)](https://pyup.io/repos/github/adbpy/wire-protocol/)

[![Stories in Ready](https://badge.waffle.io/adbpy/wire-protocol.svg?label=ready&title=Ready)](http://waffle.io/adbpy/wire-protocol)

Android Debug Bridge (ADB) Wire Protocol

## Status

This project is actively maintained and under development.

## Installation

To install wire-protocol from [pip](https://pypi.python.org/pypi/pip):
```bash
    $ pip install adbwp
```

To install wire-protocol from source:
```bash
    $ git clone git@github.com:adbpy/wire-protocol.git
    $ cd wire-protocol && python setup.py install
```

## Goals/Scope

A standalone library that can be used for building protocol objects while remaining transport/application protocol agnostic.
The wire protocol should care about:

* Byte layout on the wire
* Model representation of Messages (header + payload)
* Provide simple API that convert bytes to/from models

The wire protocol should not care, nor have concept of:

* Synchronous vs. Asynchronous
* TCP, UDP, USB
* Sequence of messages required to complete a connection "handshake"
* Cryptography required to verify endpoints
* Anything else not explicitly mentioned above...

## Contributing

If you would like to contribute, simply fork the repository, push your changes and send a pull request.
Pull requests will be brought into the `master` branch via a rebase and fast-forward merge with the goal of having a linear branch history with no merge commits.

## License

[Apache 2.0](LICENSE)
