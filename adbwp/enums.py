"""
    adbwp.enums
    ~~~~~~~~~~~

    Contains enumeration types used by the protocol.
"""
import enum


class Command(enum.IntEnum):
    """
    Enumeration for command types used by the ADB protocol.
    """
    SYNC = 0x434e5953  # Internal only.
    CNXN = 0x4e584e43
    AUTH = 0x48545541
    OPEN = 0x4e45504f
    OKAY = 0x59414b4f
    CLSE = 0x45534c43
    WRTE = 0x45545257


class CommandResponse(enum.Enum):
    """
    Enumeration for response message types from ADB connection requests.
    """
    OKAY = 'OKAY'
    FAIL = 'FAIL'

    def __str__(self):
        return str(self.value)


class AuthType(enum.IntEnum):
    """
    Enumeration for authentication types used by the ADB protocol.
    """
    TOKEN = 1
    SIGNATURE = 2
    RSAPUBLICKEY = 3


class SystemType(enum.Enum):
    """
    Enumeration for "systemtype" values used by the ADB protocol for the "system-identity-string"
    value in a CONNECT message.
    """
    BOOTLOADER = 'bootloader'
    DEVICE = 'device'
    HOST = 'host'

    def __str__(self):
        return str(self.value)
