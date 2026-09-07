import sys
from abc import ABC, abstractmethod
from typing import List, Literal

#coiso  que o robson ajudou e arrasou
TokenType = Literal["INT", "MINUS", "PLUS", "DIV", "MULT", "OPEN_PAR", "CLOSE_PAR", "EOF"]


class Node(ABC):
    def __init__(self, value: str | int, children: List["Node"]):
        self.value = value
        self.children = children

    @abstractmethod
    def evaluate(self) -> int:
        pass


class BinOp(Node):
    def __init__(self, value: str, left: Node, right: Node):
        super().__init__(value, [left, right])

    def evaluate(self) -> int:
        left_value = self.children[0].evaluate()
        right_value = self.children[1].evaluate()

        if self.value == "+":
            return left_value + right_value
        elif self.value == "-":
            return left_value - right_value
        elif self.value == "*":
            return left_value * right_value
        elif self.value == "/":
            if right_value == 0:
                raise Exception("[Semantic] Division by zero")

            return left_value // right_value
        else:
            raise Exception(
                f"[Semantic] Unknown operator: {self.value}"
            )


class UnOp(Node):
    def __init__(self, value: str, child: Node):
        super().__init__(value, [child])

    def evaluate(self) -> int:
        child_value = self.children[0].evaluate()

        if self.value == "+":
            return +child_value
        elif self.value == "-":
            return -child_value
        else:
            raise Exception(
                f"[Semantic] Unknown unary operator: {self.value}"
            )


class IntVal(Node):
    def __init__(self, value: int):
        super().__init__(value, [])

    def evaluate(self) -> int:
        return self.value


class Token:
    def __init__(self, token_type: TokenType, value: int | str):
        self.type = token_type
        self.value = value


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.next = Token("EOF", "")

    def select_next(self):
        # Ignora espaços em branco
        while (
            self.position < len(self.source)
            and self.source[self.position].isspace()
        ):
            self.position += 1

        # Verifica se chegou ao final
        if self.position >= len(self.source):
            self.next = Token("EOF", "")
            return

        current = self.source[self.position]

        # Reconhece o operador +
        if current == "+":
            self.next = Token("PLUS", "+")
            self.position += 1
            return

        # Reconhece o operador -
        if current == "-":
            self.next = Token("MINUS", "-")
            self.position += 1
            return

        # Reconhece o operador de divisão
        if current == "/":
            self.next = Token("DIV", "/")
            self.position += 1
            return

        # Reconhece o operador de multiplicação
        if current == "*":
            self.next = Token("MULT", "*")
            self.position += 1
            return

        # Abre parênteses
        if current == "(":
            self.next = Token("OPEN_PAR", "(")
            self.position += 1
            return

        # Fecha parênteses
        if current == ")":
            self.next = Token("CLOSE_PAR", ")")
            self.position += 1
            return

        # Reconhece um número inteiro
        if current.isdigit():
            number = ""

            # Reconhece números com mais de um dígito
            while (
                self.position < len(self.source)
                and self.source[self.position].isdigit()
            ):
                number += self.source[self.position]
                self.position += 1

            self.next = Token("INT", int(number))
            return

        # Qualquer outro símbolo é inválido
        raise Exception(f"[Lexer] Invalid symbol {current}")


class Parser:
    # Atributo estático que será inicializado pelo método run
    lexer = None

    @staticmethod
    def parse_factor() -> Node:
        # Operadores unários + e -
        if Parser.lexer.next.type in ("PLUS", "MINUS"):
            operator = str(Parser.lexer.next.value)

            # Consome o operador unário
            Parser.lexer.select_next()

            # Recursão permite entradas como +--++3
            result = Parser.parse_factor()

            result = UnOp(operator, result)

            return result

        # Expressão entre parênteses
        if Parser.lexer.next.type == "OPEN_PAR":
            # Consome (
            Parser.lexer.select_next()

            # Calcula a expressão interna
            result = Parser.parse_expression()

            # Exige o fechamento do parêntese
            if Parser.lexer.next.type != "CLOSE_PAR":
                raise Exception(
                    "[Parser] Expected CLOSE_PAR, "
                    f"got {Parser.lexer.next.type}"
                )

            # Consome )
            Parser.lexer.select_next()

            return result

        # Número inteiro
        if Parser.lexer.next.type == "INT":
            result = IntVal(int(Parser.lexer.next.value))

            # Consome o número
            Parser.lexer.select_next()

            return result

        raise Exception(
            f"[Parser] Expected factor, got {Parser.lexer.next.type}"
        )

    @staticmethod
    def parse_term() -> Node:
        # O primeiro elemento de um termo é um fator
        result = Parser.parse_factor()

        # Multiplicação e divisão
        while Parser.lexer.next.type in ("MULT", "DIV"):
            operator = str(Parser.lexer.next.value)

            # Consome o operador
            Parser.lexer.select_next()

            # Obtém o próximo fator
            factor = Parser.parse_factor()

            result = BinOp(operator, result, factor)

        return result

    @staticmethod
    def parse_expression() -> Node:
        # O primeiro elemento de uma expressão é um termo
        result = Parser.parse_term()

        # Soma e subtração
        while Parser.lexer.next.type in ("PLUS", "MINUS"):
            operator = str(Parser.lexer.next.value)

            # Consome o operador
            Parser.lexer.select_next()

            # Obtém o próximo termo
            term = Parser.parse_term()

            result = BinOp(operator, result, term)

        return result

    @staticmethod
    def run(code: str) -> Node:
        # Cria o Lexer usando a expressão recebida
        Parser.lexer = Lexer(code)

        # Posiciona o Lexer no primeiro token
        Parser.lexer.select_next()

        # Analisa e calcula a expressão
        result = Parser.parse_expression()

        # Verifica se toda a expressão foi consumida
        if Parser.lexer.next.type != "EOF":
            raise Exception(
                f"[Parser] Unexpected token {Parser.lexer.next.type}"
            )

        return result


def main():
    # Precisa receber exatamente uma expressão pelo terminal
    if len(sys.argv) != 2:
        raise Exception(
            "[Parser] Expected exactly one input expression"
        )

    entrada = sys.argv[1]

    raiz = Parser.run(entrada)
    resultado = raiz.evaluate()

    print(resultado)


if __name__ == "__main__":
    main()