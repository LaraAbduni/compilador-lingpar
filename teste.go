// Teste do Roteiro 6

// Operações do roteiro anterior
x1 = 3
y2 = 4
z_final = x1 + y2
Println(z_final)

dobro = z_final * 2 // sai 14
Println(dobro + 1)

// Leitura do terminal
n = Scanln()
i = 0
soma = 0

// Laço utilizando AND, OR e NOT
for (i < n && !(i == n)) || i < 0 {
    soma = soma + i
    i = i + 1
}

// Condicional utilizando AND, OR e NOT
if (soma > 0 && !(n < 0)) || n == 0 {
    Println(soma)
} else {
    Println(0)
}