import sys
from typing import Literal

#coiso que o robson ajudou e arrasou
TokenType = Literal["INT", "MINUS", "PLUS", "EOF"]


class Token:
    def __init__(self, token_type: TokenType, value: int | str):
        self.type = token_type
        self.value = value


# Transforma caracteres em tokens e ignora espaços em branco
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

        # Verifica se chegou ao final da expressão
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
    lexer: Lexer

    @staticmethod
    def parse_expression() -> int:
        # A expressão precisa começar com um número
        if Parser.lexer.next.type != "INT":
            raise Exception(
                f"[Parser] Expected INT, got {Parser.lexer.next.type}"
            )

        # Guarda o primeiro número no resultado
        result = int(Parser.lexer.next.value)

        # Consome o primeiro número
        Parser.lexer.select_next()

        # Continua enquanto encontrar + ou -
        while Parser.lexer.next.type in ("PLUS", "MINUS"):
            # Guarda o operador antes de buscar o próximo token
            operator = Parser.lexer.next.type

            # Consome o operador
            Parser.lexer.select_next()

            # Depois do operador precisa existir um número
            if Parser.lexer.next.type != "INT":
                raise Exception(
                    f"[Parser] Expected INT, got {Parser.lexer.next.type}"
                )

            number = int(Parser.lexer.next.value)

            # Realiza a operação
            if operator == "PLUS":
                result += number
            else:
                result -= number

            # Consome o número
            Parser.lexer.select_next()

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