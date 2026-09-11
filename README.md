# compilador-lingpar

![Compilation Status](https://compiler-tester.insper-comp.com.br/svg/Lara70987/compilador-lingpar)

![Diagrama Sintático](https://compiler-tester.insper-comp.com.br/ds?version=v2.0)

## EBNF

```ebnf
PROGRAM = { STATEMENT } ;
STATEMENT = ((IDENTIFIER, "=", EXPRESSION) | ("Println", "(", EXPRESSION, ")") | ε), "\n" ;
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = ("+" | "-"), FACTOR | "(", EXPRESSION, ")" | NUMBER | IDENTIFIER ;
NUMBER = DIGIT, {DIGIT} ;
DIGIT = 0 | 1 | ... | 9 ;
IDENTIFIER = LETTER, {LETTER | DIGIT | "_"} ;
LETTER = a | b | ... | z | A | B | ... | Z ;
```