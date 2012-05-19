def get_top_directory():
    import myriad                                                                                                                                                                 
    return myriad.__path__[0]


def get_test_module():
    return get_top_directory().replace("/", ".")

