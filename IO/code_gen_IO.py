import os


class CodeGenIO:
    def __init__(self, file_name="output.txt") -> None:
        self.file_name = file_name
        if os.path.exists(file_name):
            os.remove(file_name)

    def save_output(self, program_block):
        with open(self.file_name, 'w') as file:
            for inst in enumerate(program_block.code_memory):
                file.write(f'{inst[0]}\t{inst[1]}\n')
