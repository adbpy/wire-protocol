"""
    adbwp.hints
    ~~~~~~~~~~~

    Contains type hint definitions used across modules in this package.
"""
import typing

from . import enums


#: Type hint that defines multiple types that represent a command.
Command = typing.Union[int, enums.Command]  # pylint: disable=invalid-name
