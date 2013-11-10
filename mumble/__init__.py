from .meta import Meta
from .hooks import *
from .server import Server
from .acl import *


def connect():
    """Connects to local Murmur server."""
    return Meta()