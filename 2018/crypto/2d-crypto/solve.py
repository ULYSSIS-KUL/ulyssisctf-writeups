from PIL import Image
from itertools import product

known = [
        "00000001                         10000000",
        "01111101                         10111110",
        "01000101                         10100010",
        "01000101                         10100010",
        "01000101                         10100010",
        "01111101                         10111110",
        "00000001010101010101010101010101010000000",
        "11111111                         11111111",
        "      0                                  ",
        "      1                                  ",
        "      0                                  ",
        "      1                                  ",
        "      0                                  ",
        "      1                                  ",
        "      0                                  ",
        "      1                                  ",
        "      0                                  ",
        "      1                                  ",
        "      0                                  ",
        "      1                                  ",
        "      0                                  ",
        "      1                                  ",
        "      0                                  ",
        "      1                                  ",
        "      0                                  ",
        "      1                                  ",
        "      0                                  ",
        "      1                                  ",
        "      0                                  ",
        "      1                                  ",
        "      0                                  ",
        "      1                                  ",
        "      0                         00000    ",
        "111111110                       01110    ",
        "00000001                        01010    ",
        "01111101                        01110    ",
        "01000101                        00000    ",
        "01000101                                 ",
        "01000101                                 ",
        "01111101                                 ",
        "00000001                                 "
        ]




def retrieve_key(img, key, known, keysize=13):
    for x, y in product(range(41), repeat=2):
        if known[y][x] == " ":
            continue
        value = int(known[y][x]) ^ (img.getpixel((x, y)) > 0)
        if key[y%keysize][x%keysize] > -1 and value != key[y%keysize][x%keysize]:
            return False
        key[y%keysize][x%keysize] = value

    return key


def xor(qrcode, key, keysize=13):
    for x, y in product(range(41), repeat=2):
        if key[y%keysize][x%keysize] == -1:
            continue
        pixel = (qrcode.getpixel((x, y))>0) ^ key[y%keysize][x%keysize]
        qrcode.putpixel((x, y), pixel)
    return qrcode


def showkey(key):
    for i in key:
        for j in i:
            if j == -1:
                print("#", end="")
            else:
                print(".", end="")
        print()


img_orig = Image.open("images/challenge.png").convert("1").resize((41, 41))


for i in range(1, 20):
    img = img_orig.copy()
    key = [[-1 for _ in range(i)] for _ in range(i)]
    key = retrieve_key(img, key, known, i)

    if not key:
        print ("It's not", i)
        continue

    print("It is", i)
    print()
    img = xor(img, key, i)
    showkey(key)

    show_img = Image.new("RGB", (450, 450), "white")
    show_img.paste(img.resize((410, 410)), (20,20))
    show_img.show()
    break

