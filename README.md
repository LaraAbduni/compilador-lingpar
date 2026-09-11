# compilador-lingpar

![Compilation Status](https://compiler-tester.insper-comp.com.br/svg/Lara70987/compilador-lingpar)

![Diagrama Sintático](https://compiler-tester.insper-comp.com.br/ds?version=v2.0)

## EBNF

```ebnf
PROGRAM = { STATEMENT } ;
STATEMENT = ("Println", "(", EXPRESSION, ")" | IDENTIFIER, "=", EXPRESSION | Ε), "\n" ;
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = NUMBER | IDENTIFIER | ("+" | "-"), FACTOR | "(", EXPRESSION, ")" ;
NUMBER = DIGIT, { DIGIT } ;
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
DIGIT = "0" | "1" | ... | "9" ;
LETTER = "a" | "b" | ... | "z" | "A" | "B" | ... | "Z" ;
```