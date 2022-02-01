class PB:
    def __init__(self) -> None:
        self.code_memory = []
        self.i = 0

    def add_instruction(self, index, op, x1, x2, x3):
        while len(self.code_memory) <= index:
            self.code_memory.append('')
        self.code_memory.append(f'({op}, {x1}, {x2}, {x3})')

    def initialize_var(self, memory, symbol_table, lexeme):
        address = str(memory.get_data_address())
        symbol_table.add_to_table((lexeme, 'int', address))


    def initialize_array(self, memory, symbol_table, lexeme, length):
        addresses = []
        array_pointer_address = str(memory.get_data_address())
        for _ in range(length):
            addresses.append(str(memory.get_data_address()))
        self.add_instruction(self.i, 'ASSIGN', f'#{addresses[0]}', array_pointer_address)
        self.i += 1
        symbol_table.add_to_table((lexeme, 'array', array_pointer_address)) 

        
