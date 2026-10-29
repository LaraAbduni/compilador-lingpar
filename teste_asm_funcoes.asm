section .data
    format_out: db "%d", 10, 0
    format_in: db "%d", 0
    scan_int: dd 0
    global_base: dd 0

section .text
    extern printf
    extern scanf
    global _start
func_subtrai:
    push ebp
    mov ebp, esp
    mov eax, dword [ebp+12]
    push eax
    mov eax, dword [ebp+8]
    pop ecx
    sub eax, ecx
    jmp return_15
return_15:
    mov esp, ebp
    pop ebp
    ret

func_fibonacci:
    push ebp
    mov ebp, esp
    mov eax, 2
    push eax
    mov eax, dword [ebp+8]
    pop ecx
    cmp eax, ecx
    mov eax, 0
    mov ecx, 1
    cmovl eax, ecx
    cmp eax, 0
    je exit_26
    mov eax, dword [ebp+8]
    jmp return_38
exit_26:
    mov eax, 2
    push eax
    mov eax, dword [ebp+8]
    pop ecx
    sub eax, ecx
    push eax
    call func_fibonacci
    add esp, 4
    push eax
    mov eax, 1
    push eax
    mov eax, dword [ebp+8]
    pop ecx
    sub eax, ecx
    push eax
    call func_fibonacci
    add esp, 4
    pop ecx
    add eax, ecx
    jmp return_38
return_38:
    mov esp, ebp
    pop ebp
    ret

func_soma_global:
    push ebp
    mov ebp, esp
    mov eax, dword [ebp+8]
    push eax
    mov ecx, dword [global_base]
    mov eax, dword [ecx-4]
    pop ecx
    add eax, ecx
    jmp return_48
return_48:
    mov esp, ebp
    pop ebp
    ret

func_main:
    push ebp
    mov ebp, esp
    mov eax, 3
    push eax
    mov eax, 10
    push eax
    call func_subtrai
    add esp, 8
    push eax
    push format_out
    call printf
    add esp, 8
    mov eax, 6
    push eax
    call func_fibonacci
    add esp, 4
    push eax
    push format_out
    call printf
    add esp, 8
    mov eax, 5
    push eax
    call func_soma_global
    add esp, 4
    push eax
    push format_out
    call printf
    add esp, 8
    mov eax, 0
return_62:
    mov esp, ebp
    pop ebp
    ret


_start:
    push ebp
    mov ebp, esp
    mov dword [global_base], ebp

    ; aqui começa o codigo gerado:
    sub esp, 4 ; var global int [EBP-4]
    mov eax, 10
    mov ecx, dword [global_base]
    mov dword [ecx-4], eax
    call func_main

    ; aqui termina o codigo gerado

    mov esp, ebp
    pop ebp

    ; chamada da interrupcao de saida
    mov eax, 1
    xor ebx, ebx
    int 0x80
