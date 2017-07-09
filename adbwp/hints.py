"""
    adbwp.hints
    ~~~~~~~~~~~

    Contains type hint definitions used across modules in this package.
"""
import typing

from . import enums

#: Type hint that is an alias for the built-in :class:`~bytes` type.
Bytes = bytes  # pylint: disable=invalid-name


#: Type hint that is an alias for the built-in :class:`~bool` type.
Bool = bool


#: Type hint that is an alias for the built-in :class:`~int` type.
Int = int  # pylint: disable=invalid-name


#: Type hint that is an alias for the built-in :class:`~str` type.
Str = str  # pylint: disable=invalid-name


#: Type hint that defines multiple types that represent a command.
Command = typing.Union[int, enums.Command]  # pylint: disable=invalid-name


#: Type hint that defines multiple types that can represent a system type
#: used in a connect message.
SystemType = typing.Union[str, enums.SystemType]  # pylint: disable=invalid-name


#: Type hint that defines multiple types that can represent a message data payload.
Payload = typing.Union[bytes, bytearray, str, memoryview]  # pylint: disable=invalid-name
