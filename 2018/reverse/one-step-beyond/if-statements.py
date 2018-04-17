#!/usr/bin/env python3

def t(f, *a):
    r = f(*a)
    while callable(r):
        r = r()
    return r


def f(i,p,pp):
    if i != 0:
        return lambda:f(t(d,i),p+pp,p)
    else:
        return p+pp


def r(c,n):
    if n != 0:
        n %= 95
        return lambda:r(chr((ord(c)-31)%95+32),t(d,n))
    else:
        return c


def d(z,m=3&5):
    if (~z)&m != 0:
        return lambda:d(z^m,((~z)&m)<<1)
    else:
        return z^m


def e(s,x=0,a=[]):
    if x < len(s):
        a.append(t(r,s[x],t(f,x,3&5,5^5)))
        return lambda:e(s,t(d,x,~0),a)
    else:
        return "".join(a)


dev = __import__('sys')
print(t(e,input("enter input: ") if len(dev.argv) < 2 else dev.argv[1]))
