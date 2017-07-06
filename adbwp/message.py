"""
    adbwp.message
    ~~~~~~~~~~~~~

    Object representation of a message.
"""
import typing

from . import header, hints, payload


class Message(typing.NamedTuple('Message', [('header', header.Header), ('data', hints.Payload)])):
    """
    Represents an entire ADB protocol message.

    A message consists of a 24-byte header followed by an optional data payload.
    """


def new(command: hints.Command, arg0: int=0, arg1: int=0, data: hints.Payload=b'') -> Message:
    """
    Create a new :class:`~adbwp.message.Message` instance with optional default values.

    :param command: Command identifier
    :type command: :class:`~adbwp.enums.Command` or :class:`~int`
    :param arg0: (Optional) First argument of the command
    :type arg0: :class:`~int`
    :param arg1: (Optional) Second argument of the command
    :type arg1: :class:`~int`
    :param data: (Optional) Message payload
    :type data: :class:`~bytes`, :class:`~bytearray`, :class:`~str`, or :class:`~memoryview`
    :return: Message instance from given values
    :rtype: :class:`~adbwp.message.Message`
    """
    data = payload.as_bytes(data)
    return Message(header.new(command, arg0, arg1, len(data), payload.checksum(data), header.magic(command)), data)


def from_header(header: header.Header, data: hints.Payload=b'') -> Message:  # pylint: disable=redefined-outer-name
    """
    Create a new :class:`~adbwp.message.Message` instance from an existing :class:`~adbwp.header.Header`.

    :param header: Message header
    :type header: :class:`~adbwp.header.Header`
    :param data: (Optional) Message payload
    :type data: :class:`~bytes`, :class:`~bytearray`, :class:`~str`, or :class:`~memoryview`
    :return: Message instance from given values
    :rtype: :class:`~adbwp.message.Message`
    """
    return Message(header, payload.as_bytes(data))
