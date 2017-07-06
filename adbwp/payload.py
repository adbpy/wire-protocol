"""
    adbwp.payload
    ~~~~~~~~~~~~~

    Contains functionality for message data payloads.
"""
from . import consts, hints


def checksum(data: hints.Payload) -> int:
    """
    Compute the checksum value of a header that uses the given data payload.

    :param data: Data payload
    :type data: :class:`~bytes`, :class:`~bytearray`, :class:`~str`, or :class:`~memoryview`
    :return: Data payload checksum
    :rtype: :class:`~int`
    """
    return sum(as_bytes(data)) & consts.COMMAND_MASK


def null_terminate(data: hints.Payload) -> bytes:
    """
    Null terminate the given data payload.

    :param data: Data payload
    :type data: :class:`~bytes`, :class:`~bytearray`, :class:`~str`, or :class:`~memoryview`
    :return: Data payload ending with a zero byte.
    :rtype: :class:`~bytes`
    """
    return as_bytes(data) + b'\0'


def as_bytes(data: hints.Payload, encoding: str='utf-8', errors: str='strict') -> bytes:
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
