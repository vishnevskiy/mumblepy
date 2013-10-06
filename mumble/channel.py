class Channel(object):
    def __init__(self, server, channel):
        self.__server = server
        self.__channel = channel

    def delete(self):
        self.__server.remove_channel(self.__channel.id)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self.__channel, key, value)
        self.__server.set_channel_state(self.__channel)

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