from generator_sup.special_symbols import SpecialSymbol


class SymbolTable:
    def __init__(self) -> None:
        self.table = []
        
    def add_to_table(self, row):
        self.table.append(row)
    
    def pop_from_table(self):
        return self.table.pop()

    def get_address(self, identifier):
        for row in self.table[::-1]:

            if row is not SpecialSymbol.SYMBOL_TABLE_STOP and row[0] == identifier:
                return row[2]
        raise Exception('ID not found in symbol table.')

    @property
    def size(self):
        return len(self.table)

    def collapse_symbol_table(self, to_keep):
        # Pop until the length of table becomes equal to 'remained'
        self.table = self.table[:to_keep]
    