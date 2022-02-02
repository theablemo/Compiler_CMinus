class SymbolTable:
    def __init__(self) -> None:
        self.table = []
        
    def add_to_table(self, row):
        self.table.append(row)

    def get_address(self, identifier):
        for row in self.table[::-1]:
            if row[0] == identifier:
                return row[2]
        raise Exception('ID not found in symbol table.')

    @property
    def size(self):
        return len(self.table)

    def collapse_symbol_table(self, to_keep):
        # Pop until the length of table becomes equal to 'remained'
        self.table = self.table[:to_keep]