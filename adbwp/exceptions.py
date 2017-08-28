"""
    adbwp.exceptions
    ~~~~~~~~~~~~~~~~

    Contains exception types used across the package.
"""


class WireProtocolError(Exception):
    """
    Base exception for all ADB wire protocol related errors.
    """


class PackError(WireProtocolError):
    """
    Exception raised when unable to pack/serialize a model into :class:`~bytes`.
    """


class UnpackError(WireProtocolError):
    """
    Exception raised when unable to unpack/deserialize :class:`~bytes` into a model.
    """


class ChecksumError(WireProtocolError):
    """
    Exception raised when the computed checksum of a data payload does not match the value in the header.
    """
