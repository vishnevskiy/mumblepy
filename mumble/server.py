from .user import User
from .channel import Channel


class Server(object):
    def __init__(self, meta, server):
        self.id = server.id()

        self.__meta = meta
        self.__server = server

    def __len__(self):
        return

    @property
    def running(self):
        return bool(self.__server.isRunning())

    def start(self):
        if not self.running:
            return self.__server.start()

    def stop(self):
        if self.running:
            return self.__server.stop()

    def delete(self):
        self.stop()
        return self.__server.delete()

    # Conf

    def get_all_conf(self):
        conf = self.__meta.get_default_conf()
        conf.update(self.__server.getAllConf())
        return conf

    def get_conf(self, key):
        return self.__server.getConf(key)

    def set_conf(self, key, value):
        return self.__server.setConf(key, value)

    # Channels

    def get_channels(self):
        return [Channel(self, channel) for channel in self.__server.getChannels().values()]

    def get_channel(self, channel_id):
        channel = self.__server.getChannelState(channel_id)

        if channel is None:
            return None

        return Channel(self, channel)

    def set_channel_state(self, channel):
        self.__server.setChannelState(channel)

    def add_channel(self, name, parent):
        return self.__server.addChannel(name, parent)

    def remove_channel(self, channel_id):
        self.__server.removeChannel(channel_id)

    # Users

    def get_users(self):
        return [User(self, user) for user in self.__server.getUsers().values()]

    def get_user(self, session):
        user = self.__server.getState(session)

        if user is None:
            return None

        return User(self, user)

    def kick_user(self, session, reason=''):
        self.__server.kickUser(session, reason)

    # Bans

    def get_bans(self):
        return self.__server.getBans()

    def set_bans(self, bans):
        self.__server.setBans(bans)

    # Hooks

    def add_hook(self, cls):
        self.__meta.add_hook_to(self.__server, cls, self.id)

    def remove_hook(self, cls, hook):
        self.__meta.remove_hook_from(self.__server, cls, hook)