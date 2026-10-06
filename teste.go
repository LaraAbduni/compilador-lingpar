// Testes do Roteiro 7

// Variáveis dos três tipos
var x int = 3
var y int = 4
var nome string = "Lara"
var ativo bool = true
var desligado bool

// Valores default: 0, "" e false
var contador int
var texto string

// Operações dos roteiros anteriores
var soma int = x + y
var dobro int = soma * 2
Println(soma)
Println(dobro + 1)

// Strings, booleanos e concatenação
Println(nome)
Println(ativo)
Println("nome=" + nome + ", soma=" + soma)
Println("ativo=" + ativo + ", desligado=" + desligado)

// Atribuições em variáveis previamente declaradas
contador = contador + 1
texto = "contador=" + contador
Println(texto)

// Leitura continua retornando int
var n int = Scanln()
var i int = 0
var acumulado int = 0

// Laço e operadores booleanos dos roteiros anteriores
for (i < n && !(i == n)) || i < 0 {
    acumulado = acumulado + i
    i = i + 1
}

if (acumulado > 0 && !(n < 0)) || n == 0 {
    Println("acumulado=" + acumulado)
} else {
    Println("acumulado=0")
}

// Testes de erro: descomente um por vez.
// var tipo_errado int = "texto"
// Println(1 - "texto")
// Println(true && 1)
// if "texto" {
//     Println("não deveria executar")
// }
// variavel_nao_declarada = 10
