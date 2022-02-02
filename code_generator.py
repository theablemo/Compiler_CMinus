from generator_sup import *
from generator_sup.PB_helper import PB
from generator_sup.memory_helper import Memory
from generator_sup.symbol_table_helper import SymbolTable

program_block = PB()
memory = Memory()
symbol_table = SymbolTable()
semantic_stack = []
scope_stack = []


def code_gen(token, action):
    return {
        "numeric_label": numeric_label,
        "start_break": start_break,
        "end_break": end_break,
        "until": until,
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

        "label": label,
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
        "access_array_index": access_array_index,
        "mult": mult,
        "output": output,
        "call_function": call_function,
        "assign_array_index": assign_array_index,

    }.get(action)(token)


def pid(identifier):
    if identifier == 'output':
        return 'output'
    semantic_stack.append(symbol_table.get_address(identifier))


def pnum(num):
    semantic_stack.append('#' + num)


def start_scope(*args):
    semantic_stack.append(symbol_table.size)


def end_scope(*args):
    # Used to remove all scope-related variables from scope stack
    to_keep = scope_stack.pop()
    symbol_table.collapse_symbol_table(to_keep)


def push_lexeme(lexeme):
    semantic_stack.append(lexeme)


def set_var(lexeme):
    program_block.initialize_var(memory, symbol_table, lexeme)


def set_arr(*args):
    length = int(semantic_stack.pop()[:1])
    lexeme = semantic_stack.pop()
    program_block.initialize_array(memory, symbol_table, lexeme, length)


def save_func_add(*args):
    i = program_block.i
    program_block.forward()
    func_name = semantic_stack.pop()
    semantic_stack.append(i)
    semantic_stack.append(func_name)


def stop_symbol(*args):
    # Add a STOP flag to the symbol table for future use
    # TODO: Use sth else instead of STOP
    symbol_table.add_to_table('STOP')

