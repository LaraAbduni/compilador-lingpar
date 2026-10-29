# compilador-lingpar

![Compilation Status](https://compiler-tester.insper-comp.com.br/svg/LaraAbduni/compilador-lingpar)

![Diagrama Sintático](https://compiler-tester.insper-comp.com.br/ds?version=v3.0)

## EBNF

```ebnf
PROGRAM = { (FUNCDEC | VARDEC | Ε), "\n" } ;
FUNCDEC = "func", IDENTIFIER, "(", (IDENTIFIER, TYPE, { ",", IDENTIFIER, TYPE } | Ε), ")", (TYPE | Ε), BLOCK ;
VARDEC = "var", IDENTIFIER, TYPE, ("=", BOOLEXPRESSION | Ε) ;
BLOCK = "{", "\n", { STATEMENT, }, "}" ;
STATEMENT = ("return", BOOLEXPRESSION | ("Println", "(", BOOLEXPRESSION, ")") | ("for", BOOLEXPRESSION, STATEMENT) | ("if", BOOLEXPRESSION, BLOCK, (Ε | "else", BLOCK)) | (IDENTIFIER, ("=", BOOLEXPRESSION | "(", (BOOLEXPRESSION, { ",", BOOLEXPRESSION } | Ε), ")")) | BLOCK | VARDEC | Ε), "\n" ;
BOOLEXPRESSION = BOOLTERM, { "||", BOOLTERM } ;
BOOLTERM = RELEXPRESSION, { "&&", RELEXPRESSION } ;
RELEXPRESSION = EXPRESSION, { ("==" | "<" | ">"), EXPRESSION } ;
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = NUMBER | STRING | BOOLEAN | IDENTIFIER, ("(", (BOOLEXPRESSION, { ",", BOOLEXPRESSION } | Ε), ")" | Ε) | ("!" | "+" | "-"), FACTOR | "(", BOOLEXPRESSION, ")" | "Scanln", "(", ")" ;
TYPE = "string" | "int" | "bool" ;
BOOLEAN = "true" | "false" ;
STRING = '"', { "..." }, '"' ;
NUMBER = DIGIT, { DIGIT } ;
DIGIT = "0" | ... | "9" ;
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
LETTER = "a" | ... | "z" | "A" | ... | "Z" ;
```
