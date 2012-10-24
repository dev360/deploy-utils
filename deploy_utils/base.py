import os

def configure(settings):
    """
    Configures OS environment variables to
    use internally for the deploy utils
    """
    for key, value in settings.items():
        os.environ[key] = value

