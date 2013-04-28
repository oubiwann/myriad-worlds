import os

def get_top_directory():
    import myriad
    return os.path.basename(myriad.__path__[0])


def get_test_module():
    return get_top_directory().replace("/", ".")
