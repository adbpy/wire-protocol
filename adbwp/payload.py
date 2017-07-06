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
    return sum(data) & consts.COMMAND_MASK
