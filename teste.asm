section .data
    format_out: db "%d", 10, 0
    format_in: db "%d", 0
    scan_int: dd 0

section .text
    extern printf
    extern scanf
    global _start

_start:
    push ebp
    mov ebp, esp

    ; aqui começa o codigo gerado:
    sub esp, 4 ; var i int [EBP-4]
    mov dword [ebp-4], 0
    sub esp, 4 ; var n int [EBP-8]
    mov dword [ebp-8], 0
    sub esp, 4 ; var f int [EBP-12]
    mov eax, 1
    mov dword [ebp-12], eax
    push scan_int
    push format_in
    call scanf
    add esp, 8
    mov eax, dword [scan_int]
    mov dword [ebp-8], eax
    mov eax, 2
    mov dword [ebp-4], eax
loop_101:
    mov eax, 1
    push eax
    mov eax, dword [ebp-8]
    pop ecx
    add eax, ecx
    push eax
    mov eax, dword [ebp-4]
    pop ecx
    cmp eax, ecx
    mov eax, 0
    mov ecx, 1
    cmovl eax, ecx
    cmp eax, 0
    je exit_101
    mov eax, dword [ebp-4]
    push eax
    mov eax, dword [ebp-12]
    pop ecx
    imul ecx
    mov dword [ebp-12], eax
    mov eax, 1
    push eax
    mov eax, dword [ebp-4]
    pop ecx
    add eax, ecx
    mov dword [ebp-4], eax
    jmp loop_101
exit_101:
    mov eax, dword [ebp-12]
    push eax
    push format_out
    call printf
    add esp, 8

    ; aqui termina o codigo gerado

    mov esp, ebp
    pop ebp

    ; chamada da interrupcao de saida
    mov eax, 1
    xor ebx, ebx
    int 0x80
