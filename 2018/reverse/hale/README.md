# hale

This was the hardest challenge of the entire CTF.

> We found [a sample of a virus](sample.elf) dating back from the
> Belgacom hack by GCHQ. It seems that it contains a secret used to
> communicate with GCHQ's servers, but it is very thoroughly hidden.
> Can you help us recover it?

## The concept

The binary calculates the flag and `int3`s when finished. But, a bunch
of anti-reversing tricks are used.

First of all, decompilers are fooled by messing with the stack:

```asm
    push next
    ret ; equivalent to mov eip, [esp] \n add esp, 4
    ; decompiler thinks the code ends here
next:
    ; but it actually continues here
```

```asm
    xor eax, eax
    jz normal
    add esp, 4 ; never executes, but confuses decompilers anyway
normal:
```

etc.

Secondly, hand-crafted ELF headers are used, confusing some inspection
tools:

```asm
bits 32
org 0x8048000

ehdr:
    db 0x7F, "ELF"  ; e_ident
    db 1            ; EI_CLASS
    db 1            ; EI_DATA
    db 1            ; EI_VERSION
    db EI_OSABI     ; EI_OSABI
    ; etc...
```

Result:

```
$ file sample.elf
main: ELF 32-bit LSB executable, Intel 80386, invalid version (SYSV),
    statically linked, corrupted section header size
```

Furthermore, checking `ptrace` is used to deter debuggers:

```asm
    ; in ELF header padding (offset 0x08)
_start: ; entrypoint
    mov al, 26
    xor ebx, ebx
    int 0x80
    jmp short _start2

    ; snip (ELF header stuff)

_start2:
    ; snip (anti-decompiler code explained earlier)

    cmp eax, 0
    jge nodbg
    xor eax, eax
    jmp exit
nodbg:

    ; snip

exit:
    mov al, 1 ; SYS_exit
    xor ebx, ebx
    int 0x80
```

This can be reversed by changing the code to nops. This, however,
is stopped by... using the code as encryption key.

As a final obfuscation measure, in the decryption code, instead of using a
switch, a jump table is pushed on the stack, and the code `ret`s. (I thought
people *liked* ROP? `:P`)

This looks more or less like this:

```asm
    ; 'branch IDs' (0, 1, 2, ...) are at edx
pusher:
    movzx eax, byte [edx]
    ; let's be kind and not use a lea
    shl eax, 2 ; imul cases_add - cases_ror
    add eax, fns
    push doxor
    push eax
    inc edx
    loop pusher

    mov eax, ebx
    ret ; jumpto the next case

doxor:
    ; xor byte [eax], byte [esi]
    mov bl, byte [esi]
    xor bl, byte [eax]
    mov byte [eax], bl

    ; fallthrough
next:
    inc eax
    inc esi
    ret

cases:
    ; of course, all the cases (except the last one) must have equal length
cases_ror:
    ror byte [eax], 2
    ret
cases_add:
    add byte [eax], 0x42
    ret
cases_xor:
    xor byte [eax], 0x7D
    ret
cases_inv:
    not byte [eax]
    ret
```

The best way to retrieve the flag is probably to reimplement the 'cipher' in
another program using `sample.elf` as key. (Or, break after the `ptrace` call
in a debugger, then set `eax` to 0.)

