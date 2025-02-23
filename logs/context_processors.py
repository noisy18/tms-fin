import threading as th

_current_user = th.local()

def get_current_user():
    return getattr(_current_user, 'user', None)

def set_current_user(user):
    _current_user.user = user