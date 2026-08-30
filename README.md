# compilador-lingpar

![Compilation Status](https://compiler-tester.insper-comp.com.br/svg/Lara70987/compilador-lingpar)

![Diagrama Sintático](https://compiler-tester.insper-comp.com.br/ds?version=v1.1)

## EBNF

```ebnf
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = ("+" | "-"), FACTOR | "(", EXPRESSION, ")" | NUMBER ;
NUMBER = DIGIT, { DIGIT } ;
DIGIT = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 ;
```