import time


class User(object):
    def __init__(self, server, user):
        self.__server = server
        self.__user = user

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.__user.name)
        
    def ban(self, reason='', bits=128, duration=360):
        from Murmur import Ban
        bans = self.__server.get_bans()
        bans.append(Ban(
            reason=reason,
            bits=bits,
            duration=duration,
            start=int(time.time()),
            address=self.__user.address,
        ))
        self.__server.set_bans(bans)

    def serialize(self):
        return {
            'session': self.__user.session,
            'id': self.__user.userid,
            'priority_speaker': self.__user.prioritySpeaker,
            'mute': self.__user.mute,
            'deaf': self.__user.deaf,
            'suppress': self.__user.suppress,
            'channel': self.__user.channel,
            'name': self.__user.name,
            'online_secs': self.__user.onlinesecs,
            'comment': self.__user.comment,
            'self_mute': self.__user.selfMute,
            'self_deaf': self.__user.selfDeaf,
            'idle_secs': self.__user.idlesecs,
            'ip': '.'.join(map(unicode, self.__user.address[-4:])),
            'os': self.__user.osversion
        }
