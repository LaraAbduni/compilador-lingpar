import sys


def calcular(entrada):
    resultado = 0
    numero = 0
    operador = "+"

    tem_numero = False
    teve_espaco = False

    for c in entrada:

        if c >= "0" and c <= "9":
            if teve_espaco:
                raise Exception()

            numero = numero * 10 + int(c)
            tem_numero = True

        elif c == " ":
            if tem_numero:
                teve_espaco = True

        elif c == "+" or c == "-":
            if not tem_numero:
                raise Exception()

            if operador == "+":
                resultado = resultado + numero
            else:
                resultado = resultado - numero

            operador = c
            numero = 0
            tem_numero = False
            teve_espaco = False

        else:
            raise Exception()

    if not tem_numero:
        raise Exception()

    if operador == "+":
        resultado = resultado + numero
    else:
        resultado = resultado - numero

    return resultado


if len(sys.argv) != 2:
    raise Exception()

entrada = sys.argv[1]

print(calcular(entrada))