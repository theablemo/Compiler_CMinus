class Memory:
    def __init__(self, word_length = 4) -> None:
        self.data_pointer = 100
        self.temp_pointer = 500
        self.word_length = word_length

    def get_temp_address(self):
        answer = self.temp_pointer
        self.temp_pointer += self.word_length
        return answer
    
    def get_data_address(self):
        answer = self.data_pointer
        self.data_pointer += self.word_length
        return answer
    
    