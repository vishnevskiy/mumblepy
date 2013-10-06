class MetaCallback(object):
    definition = ('MetaCallback', 'addCallback', 'removeCallback')

    def __init__(self, meta):
        self.meta = meta

    def started(self, server):
        """Called when a server is started. The server is up and running when this event is sent,
        so all methods that need a running server will work."""
        pass

    def stopped(self, server):
        """Called when a server is stopped. The server is  already stopped when this event is sent,
        so no methods that need a running server will work."""
        pass


class ServerCallback(object):
    definition = ('ServerCallback', 'addCallback', 'removeCallback')

    def __init__(self, server_id):
        self.id = server_id

    def user_connected(self, state):
        """Called when a user connects to the server. """
        pass

    def user_disconnected(self, state):
        """Called when a user disconnects from the server."""
        pass

    def user_state_changed(self, state):
        """Called when a user state changes. This is called if the user moves, is renamed, is muted,
        deafened etc."""
        pass

    def user_text_message(self, state, message):
        """Called when user writes a text message."""
        pass

    def channel_created(self, state):
        """Called when a new channel is created."""
        pass

    def channel_removed(self, state):
        """Called when a channel is removed."""
        pass

    def channel_state_changed(self, state):
        """Called when a new channel state changes. This is called if the channel is moved, renamed
        or if new links are added."""
        pass


class ServerContextCallback(object):
    definition = ('ServerContextCallback', 'addContextCallback', 'removeContextCallback')

    def __init__(self, server_id):
        self.id = server_id

    def context_action(self, action, user, session, channelid):
        pass


class ServerAuthenticator(object):
    definition = ('ServerAuthenticator', 'setAuthenticator', None)
    fallthrough_values = dict(
        authenticate=(-2, None, None),
        get_info=(False, None,),
        name_to_id=-2,
        id_to_name='',
        id_to_texture=None,
    )

    def __init__(self, server_id):
        self.id = server_id

    def authenticate(self, name, password, certificates, certhash, certstrong):
        raise NotImplementedError

    def get_info(self, user_id):
        raise NotImplementedError

    def name_to_id(self, name):
        raise NotImplementedError

    def id_to_name(self, user_id):
        raise NotImplementedError

    def id_to_texture(self, user_id):
        raise NotImplementedError


class ServerUpdatingAuthenticator(ServerAuthenticator):
    definition = ('ServerUpdatingAuthenticator', 'setAuthenticator', None)
    fallthrough_values = dict(
        register_user=-2,
        unregister_user=-1,
        get_registered_users={},
        set_info=-1,
        set_texture=-1,
    )

    def register_user(self, info):
        raise NotImplementedError

    def unregister_user(self, user_id):
        raise NotImplementedError

    def get_registered_users(self, filter):
        raise NotImplementedError

    def set_info(self, user_id, info):
        raise NotImplementedError

    def set_texture(self, user_id, texture):
        raise NotImplementedError