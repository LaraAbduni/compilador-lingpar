import re
import sys
from abc import ABC, abstractmethod
from typing import Dict, List, Literal

#coiso  que o robson ajudou e arrasou
TokenType = Literal[
    "INT",
    "MINUS",
    "PLUS",
    "DIV",
    "MULT",
    "OPEN_PAR",
    "CLOSE_PAR",
    "EOF",
    "ASSIGN",
    "END",
    "PRINT",
    "IDEN",
    "CONST",
]


class Variable:
    def __init__(self, value: int):
        self.value = value
        self.read_only = False


class SymbolTable:
    def __init__(self):
        self.table: Dict[str, Variable] = {}

    def set_value(self, name: str, value: int):
        if (
            name in self.table
            and self.table[name].read_only
        ):
            raise Exception(
                f"[Semantic] Variable {name} can not be changed"
            )

        self.table[name] = Variable(value)

    def get_value(self, name: str) -> int:
        if name not in self.table:
            raise Exception(
                f"[Semantic] Undefined variable: {name}"
            )

        return self.table[name].value


class Node(ABC):
    def __init__(
        self,
        value: str | int,
        children: List["Node"],
    ):
        self.value = value
        self.children = children

    @abstractmethod
    def evaluate(self, st: SymbolTable):
        pass


class BinOp(Node):
    def __init__(
        self,
        value: str,
        children: List["Node"],
    ):
        super().__init__(value, children)

    def evaluate(self, st: SymbolTable) -> int:
        left_value = self.children[0].evaluate(st)
        right_value = self.children[1].evaluate(st)

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
    def __init__(
        self,
        value: str,
        children: List["Node"],
    ):
        super().__init__(value, children)

    def evaluate(self, st: SymbolTable) -> int:
        child_value = self.children[0].evaluate(st)

        if self.value == "+":
            return +child_value
        elif self.value == "-":
            return -child_value
        else:
            raise Exception(
                f"[Semantic] Unknown unary operator: {self.value}"
            )


class IntVal(Node):
    def __init__(
        self,
        value: int,
        children: List["Node"],
    ):
        super().__init__(value, children)

    def evaluate(self, st: SymbolTable) -> int:
        return int(self.value)


class Identifier(Node):
    def __init__(
        self,
        value: str,
        children: List["Node"],
    ):
        super().__init__(value, children)

    def evaluate(self, st: SymbolTable) -> int:
        return st.get_value(str(self.value))


class Print(Node):
    def __init__(
        self,
        value: str,
        children: List["Node"],
    ):
        super().__init__(value, children)

    def evaluate(self, st: SymbolTable):
        print(self.children[0].evaluate(st))


class Assignment(Node):
    def __init__(
        self,
        value: str,
        children: List["Node"],
    ):
        super().__init__(value, children)

    def evaluate(self, st: SymbolTable):
        variable_name = str(self.children[0].value)

        # Impede a alteração de uma variável imutável
        if (
            variable_name in st.table
            and st.table[variable_name].read_only
        ):
            raise Exception(
                f"[Semantic] Variable "
                f"{variable_name} can not be changed"
            )

        variable_value = self.children[1].evaluate(st)

        # Declara uma variável imutável
        if self.value == "const":
            variable = Variable(variable_value)
            variable.read_only = True
            st.table[variable_name] = variable
        else:
            st.set_value(variable_name, variable_value)


class Block(Node):
    def __init__(
        self,
        value: str,
        children: List["Node"],
    ):
        super().__init__(value, children)

    def evaluate(self, st: SymbolTable):
        for child in self.children:
            child.evaluate(st)


class NoOp(Node):
    def __init__(
        self,
        value: str,
        children: List["Node"],
    ):
        super().__init__(value, children)

    def evaluate(self, st: SymbolTable):
        pass


class Token:
    def __init__(
        self,
        token_type: TokenType,
        value: int | str,
    ):
        self.type = token_type
        self.value = value


class PrePro:
    @staticmethod
    def filter(code: str) -> str:
        # Remove comentários
        code = re.sub(r"//[^\n]*", "", code)

        constants = {}
        filtered_lines = []

        # Encontra e remove as diretivas define
        for line in code.splitlines(keepends=True):
            stripped_line = line.strip()

            if re.match(r"^define(?:\s|$)", stripped_line):
                match = re.fullmatch(
                    r"define\s+"
                    r"([A-Za-z][A-Za-z0-9_]*)"
                    r"\s*=\s*(-?\d+)\s*",
                    stripped_line,
                )

                if match is None:
                    raise Exception(
                        "[PrePro] Invalid define directive"
                    )

                name = match.group(1)
                value = match.group(2)

                constants[name] = value

                # Mantém o avanço de linha
                if line.endswith("\n"):
                    filtered_lines.append("\n")
            else:
                filtered_lines.append(line)

        code = "".join(filtered_lines)

        # Substitui as constantes no restante do programa
        for name, value in constants.items():
            code = re.sub(
                rf"(?<![A-Za-z0-9_])"
                rf"{re.escape(name)}"
                rf"(?![A-Za-z0-9_])",
                value,
                code,
            )

        return code


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.next = Token("EOF", "")

    def select_next(self):
        # Ignora espaços em branco, mas não ignora a quebra de linha
        while (
            self.position < len(self.source)
            and self.source[self.position] in (" ", "\t", "\r")
        ):
            self.position += 1

        # Verifica se chegou ao final
        if self.position >= len(self.source):
            self.next = Token("EOF", "")
            return

        current = self.source[self.position]

        # Reconhece a quebra de linha
        if current == "\n":
            self.next = Token("END", "\n")
            self.position += 1
            return

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

        # Reconhece o operador de atribuição
        if current == "=":
            self.next = Token("ASSIGN", "=")
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

        # Reconhece identificadores e palavras reservadas
        if current.isalpha():
            identifier = ""

            while (
                self.position < len(self.source)
                and (
                    self.source[self.position].isalnum()
                    or self.source[self.position] == "_"
                )
            ):
                identifier += self.source[self.position]
                self.position += 1

            # Separa as palavras reservadas
            if identifier == "Println":
                self.next = Token("PRINT", identifier)

            elif identifier == "const":
                self.next = Token("CONST", identifier)

            else:
                self.next = Token("IDEN", identifier)

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

            result = UnOp(operator, [result])

            return result

        # Expressão entre parênteses
        if Parser.lexer.next.type == "OPEN_PAR":
            # Consome (
            Parser.lexer.select_next()

            # Monta a AST da expressão interna
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
            result = IntVal(
                int(Parser.lexer.next.value),
                [],
            )

            # Consome o número
            Parser.lexer.select_next()

            return result

        # Identificador
        if Parser.lexer.next.type == "IDEN":
            result = Identifier(
                str(Parser.lexer.next.value),
                [],
            )

            # Consome o identificador
            Parser.lexer.select_next()

            return result

        raise Exception(
            f"[Parser] Unexpected token {Parser.lexer.next.type}"
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

            result = BinOp(
                operator,
                [result, factor],
            )

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

            result = BinOp(
                operator,
                [result, term],
            )

        return result

    @staticmethod
    def parse_statement() -> Node:
        # Linha vazia
        if Parser.lexer.next.type == "END":
            Parser.lexer.select_next()

            return NoOp("", [])

        # Declaração de variável imutável
        if Parser.lexer.next.type == "CONST":
            # Consome const
            Parser.lexer.select_next()

            # Exige o nome da variável
            if Parser.lexer.next.type != "IDEN":
                raise Exception(
                    f"[Parser] Unexpected token "
                    f"{Parser.lexer.next.type}"
                )

            identifier = Identifier(
                str(Parser.lexer.next.value),
                [],
            )

            # Consome o identificador
            Parser.lexer.select_next()

            # Exige o operador de atribuição
            if Parser.lexer.next.type != "ASSIGN":
                raise Exception(
                    f"[Parser] Unexpected token "
                    f"{Parser.lexer.next.type}"
                )

            # Consome =
            Parser.lexer.select_next()

            # Monta a AST da expressão atribuída
            expression = Parser.parse_expression()

            # Toda instrução precisa terminar com uma quebra de linha
            if Parser.lexer.next.type != "END":
                raise Exception(
                    f"[Parser] Unexpected token "
                    f"{Parser.lexer.next.type}"
                )

            # Consome a quebra de linha
            Parser.lexer.select_next()

            return Assignment(
                "const",
                [identifier, expression],
            )

        # Atribuição de variável
        if Parser.lexer.next.type == "IDEN":
            identifier = Identifier(
                str(Parser.lexer.next.value),
                [],
            )

            # Consome o identificador
            Parser.lexer.select_next()

            # Exige o operador de atribuição
            if Parser.lexer.next.type != "ASSIGN":
                raise Exception(
                    f"[Parser] Unexpected token "
                    f"{Parser.lexer.next.type}"
                )

            # Consome =
            Parser.lexer.select_next()

            # Monta a AST da expressão atribuída
            expression = Parser.parse_expression()

            # Toda instrução precisa terminar com uma quebra de linha
            if Parser.lexer.next.type != "END":
                raise Exception(
                    f"[Parser] Unexpected token "
                    f"{Parser.lexer.next.type}"
                )

            # Consome a quebra de linha
            Parser.lexer.select_next()

            return Assignment(
                "=",
                [identifier, expression],
            )

        # Impressão
        if Parser.lexer.next.type == "PRINT":
            # Consome Println
            Parser.lexer.select_next()

            # Exige (
            if Parser.lexer.next.type != "OPEN_PAR":
                raise Exception(
                    "[Parser] Expected OPEN_PAR, "
                    f"got {Parser.lexer.next.type}"
                )

            # Consome (
            Parser.lexer.select_next()

            # Monta a AST da expressão que será impressa
            expression = Parser.parse_expression()

            # Exige )
            if Parser.lexer.next.type != "CLOSE_PAR":
                raise Exception(
                    "[Parser] Expected CLOSE_PAR, "
                    f"got {Parser.lexer.next.type}"
                )

            # Consome )
            Parser.lexer.select_next()

            # Toda instrução precisa terminar com uma quebra de linha
            if Parser.lexer.next.type != "END":
                raise Exception(
                    f"[Parser] Unexpected token "
                    f"{Parser.lexer.next.type}"
                )

            # Consome a quebra de linha
            Parser.lexer.select_next()

            return Print(
                "Println",
                [expression],
            )

        raise Exception(
            f"[Parser] Unexpected token {Parser.lexer.next.type}"
        )

    @staticmethod
    def parse_program() -> Node:
        statements: List[Node] = []

        # Monta um bloco com todas as instruções do arquivo
        while Parser.lexer.next.type != "EOF":
            statements.append(
                Parser.parse_statement()
            )

        return Block("", statements)

    @staticmethod
    def run(code: str) -> Node:
        # Cria o Lexer usando o programa recebido
        Parser.lexer = Lexer(code)

        # Posiciona o Lexer no primeiro token
        Parser.lexer.select_next()

        # Analisa e monta a AST do programa
        result = Parser.parse_program()

        # Verifica se todo o programa foi consumido
        if Parser.lexer.next.type != "EOF":
            raise Exception(
                f"[Parser] Unexpected token "
                f"{Parser.lexer.next.type}"
            )

        return result


def main():
    # Precisa receber exatamente o nome de um arquivo pelo terminal
    if len(sys.argv) != 2:
        raise Exception(
            "[Parser] Expected exactly one input file"
        )

    file_name = sys.argv[1]

    # Lê o conteúdo do arquivo de entrada
    with open(file_name, "r", encoding="utf-8") as file:
        entrada = file.read()

    # Garante uma quebra de linha no final do programa
    entrada += "\n"

    # Remove comentários antes da análise léxica
    entrada = PrePro.filter(entrada)

    raiz = Parser.run(entrada)

    # Cria a tabela de símbolos e executa a AST
    st = SymbolTable()
    raiz.evaluate(st)


if __name__ == "__main__":
    main()