# compilador-lingpar

![Compilation Status](https://compiler-tester.insper-comp.com.br/svg/LaraAbduni/compilador-lingpar)

![Diagrama Sintático](https://compiler-tester.insper-comp.com.br/ds?version=v2.2)

## EBNF

```ebnf
PROGRAM = { STATEMENT } ;
BLOCK = "{", "\n", { STATEMENT }, "}" ;
STATEMENT = (("Println", "(", BOOLEXPRESSION, ")") | ("for", BOOLEXPRESSION, BLOCK) | ("if", BOOLEXPRESSION, BLOCK, ("\n", "else", BLOCK) | Ε) | VARDEC | (IDENTIFIER, "=", BOOLEXPRESSION) | BLOCK | Ε), "\n" ;
VARDEC = "var", IDENTIFIER, TYPE, (("=", BOOLEXPRESSION) | Ε) ;
BOOLEXPRESSION = BOOLTERM, { "||", BOOLTERM } ;
BOOLTERM = RELEXPRESSION, { "&&", RELEXPRESSION } ;
RELEXPRESSION = EXPRESSION, { ("==" | "<" | ">"), EXPRESSION } ;
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = NUMBER | BOOLEAN | STRING | IDENTIFIER | ("+" | "-" | "!"), FACTOR | "(", BOOLEXPRESSION, ")" | "Scanln", "(", ")" ;
TYPE = "int" | "bool" | "string" ;
BOOLEAN = "true" | "false" ;
STRING = '"', { ... }, '"' ;
NUMBER = DIGIT, { DIGIT } ;
DIGIT = "0" | "1" | ... | "9" ;
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
LETTER = "a" | "b" | ... | "z" | "A" | "B" | ... | "Z" ;
```

## Programa de testes

O arquivo `teste.go` cobre:

- declaração de variáveis `int`, `bool` e `string`;
- valores default;
- atribuição em variáveis previamente declaradas;
- operações dos roteiros anteriores;
- concatenação de strings com inteiros e booleanos;
- `Scanln`, `for`, `if`, `else`, `&&`, `||` e `!`;
- exemplos comentados de erros de tipo e condição não booleana.

Execute com:

```bash
printf '3\n' | python3 main.py teste.go
```
