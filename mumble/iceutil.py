import re


def ice_method(attr):
    # Convert event name from CamelCase to underscores.
    attr = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', attr)
    attr = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', attr).lower()
    # Strip out the `current` value which is the final one alwaus.
    return lambda self, *args: getattr(self.callback, attr)(*args[:-1])


def ice_callback(name, bases, attrs):
    def __init__(self, callback):
        self.callback = callback
    attrs['__init__'] = __init__

    # Detect Ice methods and wrap in more pythonic callbacks.
    for base in bases:
        for attr in dir(base):
            if attr.startswith('_op_') and not attr.startswith('_op_ice_'):
                attr = attr[4:]
                attrs[attr] = ice_method(attr)

    return type(name, bases, attrs)


_ice_class_cache = {}


def ice_init(from_, name, *args, **kwargs):
    try:
        cls = _ice_class_cache[name]
    except KeyError:
        class MurmurClass(getattr(from_, name)):
            __metaclass__ = ice_callback
        cls = _ice_class_cache[name] = MurmurClass
    return cls(*args, **kwargs)