import sys
from typing import Literal

#coiso  que o robson ajudou e arrasou
TokenType = Literal["INT", "MINUS", "PLUS", "DIV", "MULT", "POWER", "OPEN_PAR", "CLOSE_PAR", "EOF"]


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

        #ajuste pro power
        if current == "*":
            if (
                self.position + 1 < len(self.source)
                and self.source[self.position + 1] == "*"
            ):
                self.next = Token("POWER", "**")
                self.position += 2
            else:
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
    def parse_factor() -> int:
        # Operadores unários + e -
        if Parser.lexer.next.type in ("PLUS", "MINUS"):
            operator = Parser.lexer.next.type

            # Consome o operador unário
            Parser.lexer.select_next()

            # Recursão permite entradas como +--++3
            result = Parser.parse_factor()

            if operator == "MINUS":
                result = -result

            return result

        result = Parser.parse_power()

        return result

    @staticmethod
    def parse_power() -> int:
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

        # Número inteiro
        elif Parser.lexer.next.type == "INT":
            result = int(Parser.lexer.next.value)

            # Consome o número
            Parser.lexer.select_next()

        else:
            raise Exception(
                f"[Parser] Expected factor, got {Parser.lexer.next.type}"
            )

        if Parser.lexer.next.type == "POWER":
            Parser.lexer.select_next()

            exponent = Parser.parse_factor()
            result = result ** exponent

        return result

    @staticmethod
    def parse_term() -> int:
        # O primeiro elemento de um termo é um fator
        result = Parser.parse_factor()

        # Multiplicação e divisão
        while Parser.lexer.next.type in ("MULT", "DIV"):
            operator = Parser.lexer.next.type

            # Consome o operador
            Parser.lexer.select_next()

            # Obtém o próximo fator
            factor = Parser.parse_factor()

            if operator == "MULT":
                result *= factor
            else:
                # Divisão inteira
                result //= factor

        return result

    @staticmethod
    def parse_expression() -> int:
        # O primeiro elemento de uma expressão é um termo
        result = Parser.parse_term()

        # Soma e subtração
        while Parser.lexer.next.type in ("PLUS", "MINUS"):
            operator = Parser.lexer.next.type

            # Consome o operador
            Parser.lexer.select_next()

            # Obtém o próximo termo
            term = Parser.parse_term()

            if operator == "PLUS":
                result += term
            else:
                result -= term

        return result

    @staticmethod
    def run(code: str) -> int:
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
    resultado = Parser.run(entrada)

    print(resultado)


if __name__ == "__main__":
    main()