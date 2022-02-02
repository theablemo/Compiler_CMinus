class SymbolTable:
    def __init__(self) -> None:
        self.table = []
        
    def add_to_table(self, row):
        self.table.append(row)