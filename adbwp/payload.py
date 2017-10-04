"""
    adbwp.payload
    ~~~~~~~~~~~~~

    Contains functionality for message data payloads.
"""
from . import consts, hints


def checksum(data: hints.Buffer) -> hints.Int:
    """
    Compute the checksum value of a header that uses the given data payload.

    :param data: Data payload
    :type data: :class:`~bytes`, :class:`~bytearray`, :class:`~str`, or :class:`~memoryview`
    :return: Data payload checksum
    :rtype: :class:`~int`
    """
    return sum(as_bytes(data)) & consts.COMMAND_MASK


def null_terminate(data: hints.Buffer) -> hints.Bytes:
    """
    Null terminate the given data payload.

    :param data: Data payload
    :type data: :class:`~bytes`, :class:`~bytearray`, :class:`~str`, or :class:`~memoryview`
    :return: Data payload ending with a zero byte.
    :rtype: :class:`~bytes`
    """
    return as_bytes(data) + b'\0'


def as_bytes(data: hints.Buffer, encoding: hints.Str = 'utf-8', errors: hints.Str = 'strict') -> hints.Bytes:
    """
    Ensure the given data payload is a :class:`~bytes` instance.

    :param data: Data payload
    :type data: :class:`~bytes`, :class:`~bytearray`, :class:`~str`, or :class:`~memoryview`
    :param encoding: (Optional) Encoding if data payload is a :class:`~str`
    :type encoding: :class:`~str`
    :param errors: (Optional) How to handle encoding errors
    :type errors: :class:`~str`
    :return: Data payload as bytes
    :rtype: :class:`~bytes`
    :raises ValueError: When data is not one of the supported types
    """
    if isinstance(data, (bytes, bytearray)):
        return data
    if isinstance(data, str):
        return data.encode(encoding, errors)
    if isinstance(data, memoryview):
        return data.tobytes()

    raise ValueError('Expected bytes, bytearray, str, or memoryview; got {}'.format(type(data).__name__))


def system_identity_string(system_type: hints.SystemType, serial: hints.Str, banner: hints.Str):
    """
    Compute the system identity string data payload.

    :param system_type: System type creating the message
    :type system_type: :class:`~adbwp.enums.SystemType` or :class:`~str`
    :param serial: Unique identifier
    :type serial: :class:`~str`
    :param banner: Human readable version/identifier string
    :type banner: :class:`~str`
    :return: System identity string payload for connect messages
    :rtype: :class:`~str`
    """
    return null_terminate(':'.join((str(system_type), serial, banner)))
