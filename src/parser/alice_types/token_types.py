class Token:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return "Token({})".format(self.value)

    def __repr__(self):
        return self.__str__()

    def is_text(self):
        return not (self.is_option() or self.is_command()) and self._is_not_block()

    def is_option(self):
        return self.value.startswith("#")

    def is_command(self):
        return self.value.startswith("@") and self.value.endswith("@")

    def _is_not_block(self):
        return not (self.value == "{" or self.value == "}")


class Tokens:
    def __init__(self, tokens: list[Token], pointer: int = 0):
        self.tokens = tokens
        self.pointer = pointer

    def next(self):
        if self.pointer >= len(self.tokens):
            raise StopIteration
        self.pointer += 1
        token = self.tokens[self.pointer]
        return token

    def get_current(self):
        if self.pointer >= len(self.tokens):
            return None
        return self.tokens[self.pointer]

    def get_next(self):
        if self.pointer + 1 >= len(self.tokens):
            return None
        return self.tokens[self.pointer + 1]

    def __len__(self):
        return len(self.tokens)

    def __getitem__(self, index):
        return self.tokens[index]

    def __iter__(self):
        return iter(self.tokens)

    def __setitem__(self, index, value):
        self.tokens[index] = value

    def __delitem__(self, index):
        del self.tokens[index]

    def append(self, value):
        self.tokens.append(value)

    def __str__(self):
        text = ""
        for token in self.tokens:
            text += str(token) + " "
        return text.strip()

    def __repr__(self):
        return self.__str__()
