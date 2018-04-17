# snaartheorie

> j00 w3 4r3 b4ckz0rz w1th [Th3 l4t3St 4sKEE t3kKn0lOg1z0Rz](askee.elf)!!
>
> bUt!!1 w33 h43V pr0t3Kkt3d 1t w1tH 4 p4sSwOrdz0r!!! 4rE y00 |_337 |\|UfF
> t0 g3t 1N?

## The concept

The binary asks for a password (the flag), and prints some ascii art when
it's correct.

The password is stored in plaintext, and this challenge can be solved using
`strings` (pun in the name is intended).

Never, ever store passwords in plaintext. Always check with a (salted!) hash.

```
                                             ______ _______ ______
 __  __ __     __  __ ______ ______ __ ______\  ___\\__  __\\  ___\
/\ \/\ \\ \   /\ \_\ \\  ___\\  ___\\_\\  ___\\ \__//_/\ \_/ \  _\/
\ \ \_\ \\ \____\__  / \___  \\___  \\ \\___  \\ \____\ \ \ \ \ \/
 \ \_____\\_____\_/\_\\ \_____\\_____\\_\\_____\\_____\\ \_\ \ \_\
  \/_____//_____/ \/_/ \/_____//_____//_//_____//_____/ \/_/  \/_/
```

