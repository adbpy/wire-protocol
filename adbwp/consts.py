"""
    adbwp.consts
    ~~~~~~~~~~~~

    Contains constant values used by the protocol.
"""

#: Protocol version.
VERSION = 0x01000000

#: Maximum message body size.
MAXDATA = 256 * 1024

#: Older ADB version max data size limit; required max for CONNECT and AUTH messages.
CONNECT_AUTH_MAXDATA = 4096

#: Size of a serialized ADB message in bytes.
MESSAGE_SIZE = 24

#: Bitmask applied to the "magic" value of ADB messages.
COMMAND_MASK = 0xffffffff
