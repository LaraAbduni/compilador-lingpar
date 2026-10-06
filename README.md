# compilador-lingpar

![Compilation Status](https://compiler-tester.insper-comp.com.br/svg/LaraAbduni/compilador-lingpar)

![Diagrama Sintático](https://compiler-tester.insper-comp.com.br/ds?version=v2.2)

## EBNF

```ebnf
PROGRAM = { STATEMENT } ;
BLOCK = "{", "\n", { STATEMENT }, "}" ;
STATEMENT = ("var", IDENTIFIER, TYPE, (Ε | "=", BOOLEXPRESSION) | ("Println", "(", BOOLEXPRESSION, ")") | ("for", BOOLEXPRESSION, BLOCK) | ("if", BOOLEXPRESSION, BLOCK, (Ε | "else", BLOCK) | ) | BLOCK | IDENTIFIER, "=", BOOLEXPRESSION | Ε), "\n" ;
BOOLEXPRESSION = BOOLTERM, { "||", BOOLTERM } ;
BOOLTERM = RELEXPRESSION, { "&&", RELEXPRESSION } ;
RELEXPRESSION = EXPRESSION, { ("==" | "<" | ">"), EXPRESSION } ;
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = NUMBER | BOOLEAN | STRING | IDENTIFIER | ("+" | "-" | "!"), FACTOR | "(", BOOLEXPRESSION, ")" | "Scanln", "(", ")" ;
TYPE = "string" | "int" | "bool" ;
BOOLEAN = "true" | "false" ;
STRING = '"', { "..." }, '"' ;
NUMBER = DIGIT, { DIGIT } ;
DIGIT = "0" | "1" | ... | "9" ;
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
LETTER = "a" | "b" | ... | "z" | "A" | "B" | ... | "Z" ;
```
