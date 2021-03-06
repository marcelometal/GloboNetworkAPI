# -*- coding:utf-8 -*-
import logging
import functools


class cached_property(object):
    """
    Decorator that converts a method with a single self argument into a
    property cached on the instance.
    # https://github.com/django/django/blob/2456ffa42c33d63b54579eae0f5b9cf2a8cd3714/django/utils/functional.py#L38-50
    """
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, type=None):
        if instance is None:
            return self
        res = instance.__dict__[self.func.__name__] = self.func(instance)
        return res

def deprecated(new_uri=None):
    """This is a decorator which can be used to mark functions
        as deprecated. It will result in a warning being emitted
        when the function is used.
    """
    def outer(fun):
        @functools.wraps(fun)
        def inner(*args, **kwargs):
            import os
            basename = os.path.basename(fun.func_code.co_filename)
            log = logging.getLogger(basename)
            message = "%s:%s: %s is deprecated. Use the new rest API." % (
                basename,
                fun.func_code.co_firstlineno + 1,
                fun.__name__,
            )

            if new_uri:
                message += " Uri to access: %s" % new_uri

            log.warning(message)
            return fun(*args, **kwargs)
        return inner
    return outer