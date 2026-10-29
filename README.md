# compilador-lingpar

![Compilation Status](https://compiler-tester.insper-comp.com.br/svg/LaraAbduni/compilador-lingpar)

![Diagrama Sintático](https://compiler-tester.insper-comp.com.br/ds?version=v2.3)

## EBNF

```ebnf
PROGRAM = { (VARDECLARATION | FUNCDECLARATION), "\n" } ;
FUNCDECLARATION = "func", IDENTIFIER, "(", (Ε | IDENTIFIER, TYPE, { ",", IDENTIFIER, TYPE }), ")", (Ε | TYPE), BLOCK ;
VARDECLARATION = "var", IDENTIFIER, TYPE, (Ε | "=", BOOLEXPRESSION) ;
BLOCK = "{", "\n", { STATEMENT }, "}" ;
STATEMENT = (VARDECLARATION | ("Println", "(", BOOLEXPRESSION, ")") | ("for", BOOLEXPRESSION, BLOCK) | ("if", BOOLEXPRESSION, BLOCK, (Ε | "else", BLOCK)) | BLOCK | IDENTIFIER, ("=", BOOLEXPRESSION | "(", (Ε | BOOLEXPRESSION, { ",", BOOLEXPRESSION }), ")") | "return", BOOLEXPRESSION | Ε), "\n" ;
BOOLEXPRESSION = BOOLTERM, { "||", BOOLTERM } ;
BOOLTERM = RELEXPRESSION, { "&&", RELEXPRESSION } ;
RELEXPRESSION = EXPRESSION, { ("==" | "<" | ">"), EXPRESSION } ;
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = NUMBER | BOOLEAN | STRING | IDENTIFIER, (Ε | "(", (Ε | BOOLEXPRESSION, { ",", BOOLEXPRESSION }), ")") | ("+" | "-" | "!"), FACTOR | "(", BOOLEXPRESSION, ")" | "Scanln", "(", ")" ;
TYPE = "string" | "int" | "bool" ;
BOOLEAN = "true" | "false" ;
STRING = '"', { "..." }, '"' ;
NUMBER = DIGIT, { DIGIT } ;
DIGIT = "0" | "1" | ... | "9" ;
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
LETTER = "a" | "b" | ... | "z" | "A" | "B" | ... | "Z" ;
```
