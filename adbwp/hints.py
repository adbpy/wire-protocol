"""
    adbwp.hints
    ~~~~~~~~~~~

    Contains type hint definitions used across modules in this package.
"""
import typing

from . import enums


#: Type hint that defines multiple types that represent a command.
Command = typing.Union[int, enums.Command]  # pylint: disable=invalid-name


#: Type hint that defines multiple types that can represent a system type
#: used in a connect message.
SystemType = typing.Union[str, enums.SystemType]  # pylint: disable=invalid-name


#: Type hint that defines multiple types that can represent a message data payload.
Payload = typing.Union[bytes, bytearray, str, memoryview]  # pylint: disable=invalid-name
