import os


def home_path(extra=None):
    """
    Returns the home path of the user
    """
    extra = extra or []
    return os.path.join(os.environ.get('HOME'), *extra)


