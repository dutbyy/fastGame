#LOG_LEVEL='DEBUG'
LOG_LEVEL='ERROR'


def debug_print(string):
    if LOG_LEVEL == "DEBUG":
        print(string)


def red_debug_print(string):
    if LOG_LEVEL == "DEBUG":
        print(string)
    pass
