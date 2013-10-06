import Ice
import IcePy
import sys
import tempfile
import os
import logging
from .iceutil import ice_init
from .server import Server


class Logger(Ice.Logger):
    def _print(self, message):
        logging.info(message)
  
    def trace(self, category, message):
        pass

    def warning(self, message):
        logging.warning(message)

    def error(self, message):
        logging.error(message)


class Meta(object):
    def __init__(self, secret=None):
        self.secret = secret

        self.__meta = None
        self.__ice = None
        self.__adapter = None

        self.connect()

    def __del__(self):
        self.disconnect()

    def load_slice(self, proxy):
        mumble_slice = IcePy.Operation(
            'getSlice',
            Ice.OperationMode.Idempotent,
            Ice.OperationMode.Idempotent,
            True,
            (),
            (),
            (),
            IcePy._t_string,
            ()
        ).invoke(proxy, ((), None))

        _, temp = tempfile.mkstemp(suffix='.ice')

        with open(temp, 'w') as slice_file:
            slice_file.write(mumble_slice)
            slice_file.flush()
            Ice.loadSlice('', ['-I' + Ice.getSliceDir(), temp])

        os.remove(temp)

    def connect(self):
        init_data = Ice.InitializationData()
        init_data.properties = Ice.createProperties(sys.argv)
        init_data.properties.setProperty('Ice.ImplicitContext', 'Shared')
        init_data.logger = Logger()

        self.__ice = Ice.initialize(init_data)

        if self.secret:
            self.__ice.getImplicitContext().put('secret', self.secret)

        self.__adapter = self.__ice.createObjectAdapterWithEndpoints('Callback.Client', 'tcp -h 127.0.0.1')
        self.__adapter.activate()

        proxy = self.__ice.stringToProxy('Meta:tcp -h 127.0.0.1 -p 6502')

        self.load_slice(proxy)

        import Murmur
        self.__meta = Murmur.MetaPrx.checkedCast(proxy)

    def disconnect(self):
        self.__ice.shutdown()

    def add_callback(self, callback):
        import Murmur
        callback_prx = Murmur.MetaCallbackPrx.uncheckedCast(self.__adapter.addWithUUID(callback))
        self.__meta.addCallback(callback_prx)

    def remove_callback(self, callback):
        self.__meta.removeCallback(callback)

    def get_version(self):
        return self.__meta.getVersion()

    def get_booted_servers(self):
        return [Server(self, server) for server in self.__meta.getBootedServers()]

    def get_all_servers(self):
        return [Server(self, server) for server in self.__meta.getAllServers()]

    def get_default_conf(self):
        return self.__meta.getDefaultConf()

    def new_server(self):
        return Server(self, self.__meta.newServer())

    def get_server(self, server_id):
        server = self.__meta.getServer(server_id)
        if server:
            return Server(self, server)
        return None

    def get_uptime(self):
        return self.__meta.getUptime()

    def add_hook(self, cls):
        return self.add_hook_to(self.__meta, cls, self)

    def add_hook_to(self, target, cls, *args, **kwargs):
        import Murmur
        name, add_func_name, _ = cls.definition
        hook = ice_init(Murmur, name, cls(*args, **kwargs))
        hook_with_uuid = self.__adapter.addWithUUID(hook)
        hook_prx = getattr(Murmur, '%sPrx' % name).checkedCast(hook_with_uuid)
        return getattr(target, add_func_name)(hook_prx)

    def remove_hook(self, cls, hook_prx):
        self.remove_hook_from(self.__meta, cls, hook_prx)

    def remove_hook_from(self, target, cls, hook_prx):
        _, _, remove_func_name = cls.definition
        if not remove_func_name:
            return
        getattr(target, remove_func_name).addCallback(hook_prx)
