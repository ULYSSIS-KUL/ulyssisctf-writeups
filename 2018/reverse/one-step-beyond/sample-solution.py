#!/usr/bin/env python3

def t(f, *a):
    r = f(*a)
    try:
        while 'False':
            r = r()
    except TypeError:
        return r
def f(i,p,pp):
    try:
        i/i
        return lambda:f(t(d,i),p+pp,p)
    except:
        return p+pp
def r(c,n):
    try:
        n %= 95
        n/n
        return lambda:r(chr((ord(c)-31)%95+32),t(d,n))
    except:
        return c
def d(z,m=3&5):
    try:
        m/((~z)&m)
        return lambda:d(z^m,((~z)&m)<<1)
    except:
        return z^m
def e(s,x=0,a=[]):
    try:
        '0'+s[x]
        a.append(t(r,s[x],-t(f,x,3&5,5^5)))
        return lambda:e(s,t(d,x,~0),a)
    except IndexError:
        return "".join(a)
dev = __import__('sys')
print(t(e,input("enter input: ") if len(dev.argv) < 2 else dev.argv[1]))
