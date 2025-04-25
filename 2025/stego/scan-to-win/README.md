You’re given a challenge with a bunch of random QR codes, each linking to some random website that Shuna found. However, one of them contains the actual flag.

You need to write a script that goes through all the QR codes, reads them using a library, and try to find the flag.

grep -o "base64,[^']*" dechallenge.html | cut -d, -f2 | sed 's/"\/>//g' | sed 's/${base64}//g' | xargs -L1 -I{} sh -c "echo {} | base64 -d | zbarimg --quiet --raw -"

A few notes:

    The order of the QR codes is shuffled randomly every time, so brute-forcing might mean scanning over 2000 QR codes before hitting the right one.

    Pop-ups don't matter—they're just there to make things more cursed. You can ignore them completely.

    There is a fake flag.

    The real flag doesn't include FLG{}.