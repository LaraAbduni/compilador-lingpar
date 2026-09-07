# compilador-lingpar

![Compilation Status](https://compiler-tester.insper-comp.com.br/svg/Lara70987/compilador-lingpar)

![Diagrama Sintático](https://compiler-tester.insper-comp.com.br/ds?version=v1.2)

## EBNF

```ebnf
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = NUMBER | ("+" | "-"), FACTOR | "(", EXPRESSION, ")" ;
NUMBER = DIGIT, { DIGIT } ;
DIGIT = "0" | "1" | ... | "9" ;
```