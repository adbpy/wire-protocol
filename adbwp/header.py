"""
    adbwp.header
    ~~~~~~~~~~~~

    Object representation of a message header.
"""
import struct
import typing

from . import consts, enums, exceptions, hints

__all__ = ['Header', 'new', 'to_bytes', 'from_bytes']


#: Struct pack/unpack string for handling six unsigned integers that represent a header.
HEADER_FORMAT = '<6I'


#: Size of header in bytes.
BYTES = 24


class Header(typing.NamedTuple('Header', [('command', hints.Command), ('arg0', hints.Int),
                                          ('arg1', hints.Int), ('data_length', hints.Int),
                                          ('data_checksum', hints.Int), ('magic', hints.Int)])):
    """
    Represents the header of an ADB protocol message.

    A header is 24 bytes consisting of 6 32-bit words in little-endian format.
    """

    @property
    def connect(self) -> hints.Bool:
        """
        Indicates whether or not this header represents a connect message.

        :return: Bool indicating if it is a connect message or not.
        :rtype: :class:`~bool`
        """
        return self.command == enums.Command.CNXN

    @property
    def auth(self) -> hints.Bool:
        """
        Indicates whether or not this header represents an auth message.

        :return: Bool indicating if it is an auth message or not.
        :type: :class:`~bool`
        """
        return self.command == enums.Command.AUTH

    @property
    def open(self) -> hints.Bool:
        """
        Indicates whether or not this header represents a open message.

        :return: Bool indicating if it is a open message or not.
        :rtype: :class:`~bool`
        """
        return self.command == enums.Command.OPEN

    @property
    def ready(self) -> hints.Bool:
        """
        Indicates whether or not this header represents a ready message.

        :return: Bool indicating if it is a ready message or not.
        :rtype: :class:`~bool`
        """
        return self.command == enums.Command.OKAY

    @property
    def write(self) -> hints.Bool:
        """
        Indicates whether or not this header represents a write message.

        :return: Bool indicating if it is a write message or not.
        :rtype: :class:`~bool`
        """
        return self.command == enums.Command.WRTE

    @property
    def close(self) -> hints.Bool:
        """
        Indicates whether or not this header represents a close message.

        :return: Bool indicating if it is a close message or not.
        :rtype: :class:`~bool`
        """
        return self.command == enums.Command.CLSE

    @property
    def sync(self) -> hints.Bool:
        """
        Indicates whether or not this header represents a sync message.

        :return: Bool indicating if it is a sync message or not.
        :rtype: :class:`~bool`
        """
        return self.command == enums.Command.SYNC

    @property
    def okay(self) -> hints.Bool:
        """
        Indicates whether or not this header represents an okay response.

        :return: Bool indicating if it is an okay response or not.
        :rtype: :class:`~bool`
        """
        return self.command == enums.CommandResponse.OKAY

    @property
    def fail(self) -> hints.Bool:
        """
        Indicates whether or not this header represents a fail response.

        :return: Bool indicating if it is a fail response or not.
        :rtype: :class:`~bool`
        """
        return self.command == enums.CommandResponse.FAIL


# pylint: disable=redefined-outer-name
def new(command: hints.Command, arg0: hints.Int=0, arg1: hints.Int=0, data_length: hints.Int=0,
        data_checksum: hints.Int=0, magic: hints.Int=0) -> Header:
    """
    Create a new :class:`~adbwp.header.Header` instance with optional default values.

    :param command: Command identifier
    :type command: :class:`~adbwp.enums.Command` or :class:`~int`
    :param arg0: (Optional) First argument of the command
    :type arg0: :class:`~int`
    :param arg1: (Optional) Second argument of the command
    :type arg1: :class:`~int`
    :param data_length: (Optional) Length of the payload
    :type data_length: :class:`~int`
    :param data_checksum: (Optional) Computed checksum of the payload
    :type data_checksum: :class:`~int`
    :param magic: (Optional) "Magic" XOR of the command
    :type magic: :class:`~int`
    :return: Header instance created from values
    :rtype: :class:`~adbwp.header.Header`
    """
    return Header(command, arg0, arg1, data_length, data_checksum, magic)
# pylint: enable=redefined-outer-name


def magic(command: hints.Command) -> hints.Int:
    """
    Compute the magic value of a header that uses the given command.

    :param command: Header command
    :type command: :class:`~adbwp.enums.Command` or :class:`~int`
    :return: Magic value
    :rtype: :class:`~int`
    """
    return command ^ consts.COMMAND_MASK


def to_bytes(header: Header) -> hints.Bytes:
    """
    Create a :class:`~bytes` from the given :class:`~adbwp.header.Header`.

    :param header: Message header
    :type header: :class:`~adbwp.header.Header`
    :return: Header represented as bytes
    :rtype: :class:`~bytes`
    :raises :class:`~adbwp.exceptions.PackError`: when unable to pack instance into 6 bytes
    """
    try:
        return struct.pack(HEADER_FORMAT, *header)
    except struct.error:
        raise exceptions.PackError('Failed to pack header into bytes')


def from_bytes(header: hints.Bytes) -> Header:
    """
    Create a :class:`~adbwp.header.Header` from the given :class:`~bytes`.

    :param header: Message header in bytes
    :type header: :class:`~bytes`
    :return: Bytes converted to a header
    :rtype: :class:`~adbwp.header.Header`
    :raises :class:`~adbwp.exceptions.UnpackError`: When unable to unpack instance from bytes
    """
    try:
        command, *args = struct.unpack(HEADER_FORMAT, header)
    except struct.error:
        raise exceptions.UnpackError('Failed to unpack header from bytes')
    else:
        return new(enums.Command(command), *args)
