from __future__ import absolute_import

from functools import wraps

from django.core.exceptions import PermissionDenied

from .rcore import is_ratelimited


__all__ = ['ratelimit']

ALL=('GET', 'OPTIONS','POST', 'PUT', 'PATCH', 'DELETE')

UNSAFE=('POST', 'PUT', 'PATCH', 'DELETE')

def ratelimit(group=None, key=None, rate=None, method=ALL, block=False):
    def decorator(fn):
        @wraps(fn)
        def _wrapped(request, *args, **kw):
            old_limited = getattr(request, 'limited', False)
            ratelimited = is_ratelimited(request=request, group=group, fn=fn,
                                         key=key, rate=rate, method=method,
                                         increment=True)
            request.limited = ratelimited or old_limited
            if ratelimited and block:
                raise PermissionDenied()
            return fn(request, *args, **kw)
        return _wrapped
    return decorator






