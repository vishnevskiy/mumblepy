class Channel(object):
    def __init__(self, server, channel):
        self.__server = server
        self.__channel = channel

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.__channel.name)

    def delete(self):
        self.__server.remove_channel(self.__channel.id)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self.__channel, key, value)
        self.__server.set_channel_state(self.__channel)

    def allow(self, permissions):
        acls, groups, inherit = self.__server.get_acl(self.__channel.id)
        acls[0].allow = acls[0].allow = permissions
        self.__server.set_acl(self.__channel.id, acls, groups, inherit)

    def deny(self, permissions):
        acls, groups, inherit = self.__server.get_acl(self.__channel.id)
        acls[0].allow = acls[0].allow = permissions
        self.__server.set_acl(self.__channel.id, acls, groups, inherit)

    def serialize(self):
        return {
            'id': self.__channel.id,
            'parent': self.__channel.parent,
            'links': self.__channel.links,
            'name': self.__channel.name,
            'description': self.__channel.description,
            'temporary': self.__channel.temporary,
            'position': self.__channel.position,
        }