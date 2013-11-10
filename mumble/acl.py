# Write access to channel control. Implies all other permissions (except Speak).
PERMISSION_WRITE = 0x01
# Traverse channel. Without this, a client cannot reach subchannels, no matter which privileges he has there.
PERMISSION_TRAVERSE = 0x02
# Enter channel.
PERMISSION_ENTER = 0x04
# Speak in channel.
PERMISSION_SPEAK = 0x08
# Whisper to channel. This is different from Speak, so you can set up different permissions.
PERMISSION_WHISPER = 0x100
# Mute and deafen other users in this channel.
PERMISSION_MUTE_DEAFEN = 0x10
# Move users from channel. You need this permission in both the source and destination channel to move another user.
PERMISSION_MOVE = 0x20
# Make new channel as a subchannel of this channel.
PERMISSION_MAKE_CHANNEL = 0x40
# Make new temporary channel as a subchannel of this channel.
PERMISSION_MAKE_TEMPORARY_CHANNEL = 0x400
# Link this channel. You need this permission in both the source and destination channel to link channels, or
# in either channel to unlink them.
PERMISSION_LINK_CHANNEL = 0x80
# Send text message to channel.
PERMISSION_TEXT_MESSAGE = 0x200
# Kick user from server. Only valid on root channel.
PERMISSION_TICK = 0x10000
# Ban user from server. Only valid on root channel.
PERMISSION_BANK = 0x20000
# Register and unregister users. Only valid on root channel.
PERMISSION_REGISTER = 0x40000
# Register and unregister users. Only valid on root channel.
PERMISSION_REGISTER_SELF = 0x80000


class ACL(object):
    def __init__(self, acl):
        self.raw = acl

    def __repr__(self):
        return '<%s>' % self.__class__

    def __add__(self, other):
        self.raw.allow = self.raw & other
        self.raw.deny = self.raw | other

    def __sub__(self, other):
        self.raw.allow = self.raw | other
        self.raw.deny = self.raw - other

    def serialize(self):
        return {
            'apply_here': self.raw.apply_here,
            'apply_subs': self.raw.apply_subs,
            'inherited': self.raw.inherited,
            'user_id': self.raw.userid,
            'group': self.raw.group,
            'allow': self.raw.allow,
            'deny': self.raw.deny,
        }