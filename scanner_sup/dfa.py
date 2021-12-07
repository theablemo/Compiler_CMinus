from IO.file_IO import ErrorType as err
from scanner_sup.transition import Transition as tr


class Dfa:
    ERROR_STATES = {'e1': err.INVALID_INPUT,
                    'e2': err.INVALID_NUMBER,
                    'e3': err.UNMACHED_COMMENT,
                    'e4': err.UNCLOSED_COMMENT,
                    'e5': err.UNCLOSED_COMMENT}

    ACCEPTING_STATES = {'5', '7', 'c', 'f'}
    STAR_ACCEPTING_STATES = {'2', '4', '9'}

    def __init__(self):
        self.dfa = {
            '0': {tr.LETTER: '1',
                  tr.DIGIT: '3',
                  tr.SYMBOL: '5',
                  '=': '6',
                  '*': '8',
                  '/': 'a',
                  tr.WHITESPACE: 'f'
                  },
            '1': {
                tr.LETTER_OR_DIGIT: '1',
                tr.OTHER1: '2',
                tr.INVALID_TOKEN: 'e1'
            },
            '3': {
                tr.DIGIT: '3',
                tr.OTHER2: '4',
                tr.INVALID_TOKEN_OR_LETTER: 'e2'
            },
            '6': {
                '=': '7',
                tr.OTHER3: '9',
            },
            '8': {
                tr.OTHER4: '9',
                '/': 'e3'
            },
            'a': {
                '/': 'b',
                '*': 'd',
            },
            'b': {
                tr.OTHER5: 'b',
                tr.EOF: 'e4',
                tr.ENTER: 'c'
            },
            'd': {
                tr.OTHER6: 'd',
                '*': 'e',
                tr.EOF: 'e5'
            },
            'e': {
                '/': 'c',
                '*': 'e',
                tr.EOF: 'e5',
                tr.OTHER7: 'd'
            }

        }
        self.current_state = '0'

    def reset_current_state(self):
        self.current_state = '0'

    def is_accepting(self):
        return self.current_state in Dfa.ACCEPTING_STATES

    def is_accepting_with_return(self):
        return self.current_state in Dfa.STAR_ACCEPTING_STATES

    def is_error(self):
        return self.current_state in Dfa.ERROR_STATES

    def get_error(self):
        return Dfa.ERROR_STATES.get(self.current_state)

    def move(self, character):
        t = tr.get_transition(character, self.current_state)
        # TODO: CLEAR DEBUG PRINTS!
        # print(f'{self.current_state}: {t}')
        next_state = self.dfa[self.current_state].get(t)
        if next_state is None:
            self.current_state = "e1"
        else:
            self.current_state = self.dfa[self.current_state].get(t)
