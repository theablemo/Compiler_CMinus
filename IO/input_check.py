SYMBOLS = [';', ':', '[', ']', '(', ')', '{', '}', '+', '-', '<']


def is_newLine(a):
    if ord(a) == 10:
        return True
    return False


def is_EOF(a):
    if str(a) == '':
        return True
    return False


def is_symbol(a):
    return a in SYMBOLS
