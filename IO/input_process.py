keywords = ['if', 'else', 'void', 'int', 'repeat', 'break', 'until', 'return', 'endif']


def truncate_unclosed_comment(comment):
    return comment[:7] + '...'


def write_keywords():
    res = ''
    i = 1
    for keyword in keywords:
        res += str(i) + '.' + chr(9) + keyword + chr(10)
        i += 1
    return res


def number_of_keywords():
    return len(keywords)


def is_keyword(lexeme):
    return lexeme in keywords
