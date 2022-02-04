from generator_sup import *
from generator_sup.PB_helper import PB
from generator_sup.memory_helper import Memory
from generator_sup.special_symbols import SpecialSymbol
from generator_sup.symbol_table_helper import SymbolTable

program_block = PB()
memory = Memory()
symbol_table = SymbolTable()
SS = []
scope_stack = []

break_stack = []
return_stack = []


def ss_top():
    return len(SS) - 1


def code_gen(token, action):
    print(action)
    return {
        "numeric_label": numeric_label,
        "break_start": start_break,
        "break_end": end_break,
        "until": until,
        "label": label,
        "break_func": break_func,
        "pid": pid,
        "pnum": pnum,
        "start_scope": start_scope,
        "end_scope": end_scope,
        "push_lexeme": push_lexeme,
        "set_var": set_var,
        "set_arr": set_arr,
        "save_func_add": save_func_add,
        "stop_symbol": stop_symbol,

        "get_temp": get_temp,
        "start_return": start_return,
        "end_return": end_return,
        "return_address": return_address,
        "save_func_atts": save_func_atts,
        "func_backpatching": func_backpatching,
        "pop": pop,
        "save": save,
        "jpf": jpf,
        "jpf_save": jpf_save,
        "jp": jp,
        "return_func": return_func,
        "assign": assign,
        "operation": operation,
        "mult": mult,
        "output": output,
        "call_function": call_function,
        "access_array_index": access_array_index,
        "assign_array_index": assign_array_index,
    }.get(action)(token)


def pid(identifier):
    if identifier == 'output':
        SS.append('output')
    else:
        SS.append(symbol_table.get_address(identifier))


def pnum(num):
    SS.append('#' + num)


def start_scope(*args):
    scope_stack.append(symbol_table.size)


def end_scope(*args):
    # Used to remove all scope-related variables from scope stack
    to_keep = scope_stack.pop()
    symbol_table.collapse_symbol_table(to_keep)


def push_lexeme(lexeme):
    SS.append(lexeme)


def set_var(*args):
    lexeme = SS.pop()
    program_block.initialize_var(memory, symbol_table, lexeme)


def set_arr(*args):
    length = int(SS.pop()[1:])
    lexeme = SS.pop()
    program_block.initialize_array(memory, symbol_table, lexeme, length)


def save_func_add(*args):
    i = program_block.i
    program_block.forward()
    func_name = SS.pop()
    SS.append(i)
    SS.append(func_name)


def stop_symbol(*args):
    # Add a STOP flag to the symbol table for future use
    symbol_table.add_to_table(SpecialSymbol.SYMBOL_TABLE_STOP)


def numeric_label(*args):
    SS.append('#' + str(program_block.i))


def label(*args):
    SS.append(program_block.i)


def until(*args):
    condition = SS.pop()
    l = SS.pop()
    program_block.add_instruction(program_block.i, 'JPF', condition, l, '')
    program_block.forward()


def start_break(*args):
    break_stack.append(SpecialSymbol.BREAK_CHECKPOINT)


def break_func(*args):
    break_stack.append(program_block.i)
    program_block.forward()


def end_break(*args):
    for j in break_stack[::-1]:
        if j is SpecialSymbol.BREAK_CHECKPOINT:
            break_stack.pop()
            break
        break_stack.pop()
        program_block.add_instruction(j, 'JP', str(program_block.i), '', '')


def get_temp(*args):
    SS.append(memory.get_temp_address())
    # todo: ask for zero in PB


def start_return(*args):
    return_stack.append((SpecialSymbol.RETURN_STACK_START, "#0"))


def end_return(*args):
    top = return_stack.pop()
    while top[0] != SpecialSymbol.RETURN_STACK_START:
        program_block.add_instruction(top[0], 'ASSIGN', top[1], SS[ss_top()])
        program_block.add_instruction(top[0] + 1, 'JP', str(program_block.i))
        top = return_stack.pop()


def return_address(*args):
    func_name = SS[ss_top() - 3]
    if func_name.lower() != 'main':
        value = SS[ss_top() - 1]
        program_block.add_instruction(program_block.i, 'JP', f'@{value}')
        program_block.forward()


def save_func_atts(*args):
    atts = []
    symbol_table_top = symbol_table.pop_from_table()
    while symbol_table_top != SpecialSymbol.SYMBOL_TABLE_STOP:
        atts.append(symbol_table_top[2])
        symbol_table_top = symbol_table.pop_from_table()
    attribute_one = SS.pop()
    attribute_two = SS.pop()
    tmp_add = SS.pop()
    func_name = SS.pop()
    atts.append(tmp_add)
    atts.reverse()
    atts.append(attribute_two)
    atts.append(attribute_one)
    symbol_table.add_to_table((func_name, 'function', atts))


def func_backpatching(*args):
    end_of_func = SS.pop()
    func_name = symbol_table.table[len(symbol_table.table) - 1][0]
    if func_name.lower() != 'main':
        program_block.add_instruction(end_of_func, 'JP', str(program_block.i))
    else:
        program_block.add_instruction(end_of_func, 'JP', str(int(end_of_func) + 1))
        program_block.forward()


def pop(*args):
    SS.pop()


def save(*args):
    SS.append(program_block.i)
    program_block.forward()


def jpf(*args):
    i = program_block.i
    top_if = SS.pop()
    after_if = SS.pop()
    program_block.add_instruction(int(top_if), 'JPF', after_if, str(i))


def jpf_save(*args):
    i = program_block.i
    top_if = SS.pop()
    after_else = SS.pop()
    program_block.add_instruction(int(top_if), 'JPF', after_else, str(i + 1))
    SS.append(i)
    program_block.forward()


def jp(*args):
    after_else = SS.pop()
    program_block.add_instruction(int(after_else), 'JP', str(program_block.i))


def return_func(*args):
    value = SS.pop()
    return_stack.append((program_block.i, value))
    program_block.forward()
    program_block.forward()


def assign(*args):
    value = SS.pop()
    assignee = SS[ss_top()]
    program_block.add_instruction(program_block.i, 'ASSIGN', value, assignee)
    program_block.forward()


def operation(*args):
    t = memory.get_temp_address()
    i = program_block.i
    x2 = SS.pop()
    op = SS.pop()
    x1 = SS.pop()
    if op == '+':
        program_block.add_instruction(i, 'ADD', x1, x2, t)
    elif op == '-':
        program_block.add_instruction(i, 'SUB', x1, x2, t)
    elif op == '==':
        program_block.add_instruction(i, 'EQ', x1, x2, t)
    elif op == '<':
        program_block.add_instruction(i, 'LT', x1, x2, t)
    SS.append(t)
    program_block.forward()


def mult(*args):
    t = memory.get_temp_address()
    i = program_block.i
    x1 = SS.pop()
    x2 = SS.pop()
    program_block.add_instruction(i, 'MULT', x1, x2, t)
    program_block.forward()
    SS.append(t)


def output(*args):
    name = SS[ss_top() - 1]
    if name == 'output':
        top = SS.pop()
        program_block.add_instruction(program_block.i, 'PRINT', top)
        program_block.forward()


def call_function(*args):
    if SS[ss_top()] == 'output':
        return
    atts = []
    counter = ss_top()
    for i in range(counter, -1, -1):
        if isinstance(SS[i], list):
            atts = SS[i]
    args_length = len(atts) - 3
    # args
    for i in range(args_length):
        program_block.add_instruction(program_block.i, 'ASSIGN', SS[len(SS) - args_length + i], atts[i + 1])
        program_block.forward()
    # return add
    program_block.add_instruction(program_block.i, 'ASSIGN', f'#{program_block.i + 2}', atts[args_length + 1])
    program_block.forward()
    # jp to func
    program_block.add_instruction(program_block.i, 'JP', atts[0])
    program_block.forward()
    # pop all from SS
    for _ in range(args_length + 1):
        SS.pop()
    # function output
    t = memory.get_temp_address()
    program_block.add_instruction(program_block.i, 'ASSIGN', atts[args_length + 2], t)
    SS.append(t)
    program_block.forward()


def access_array_index(*args):
    pass


def assign_array_index(*args):
    pass
