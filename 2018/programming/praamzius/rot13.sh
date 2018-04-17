#!/usr/bin/env bash
sed 2d "$0" | python3 -c "import os,sys,codecs;exec(codecs.decode(sys.stdin.read(),'$(basename -s .sh "$0")'))";exit

vzcbeg flf;P = '70(3O:3Q(37:30(7R?29)31$16_7R~61:2Q)37~36?2N,7R~27$2P?2N(7R)31!2N$7R,3N_3O_2N!30(3S?29:7R_32$32(37$2N~2Q:7R$2O;31@27~7R~72$36_11[5R^q2%8{40+7S&40+80%i20.]';
qrs h(p):
    b = beq(p);
    vs b >= beq('0') naq b <= beq('9'): erghea b - beq('0');
    vs b >= beq('N') naq b <= beq('S'): erghea b - beq('N') + 0kN;
    erghea Abar;
qrs g(fge):
    ahz = 0; ce = Snyfr;
    sbe p va fge:
        a = h(p);
        vs a vf Abar:
            vs ce:
                lvryq ahz;
                ahz = 0; ce = Snyfr;
            lvryq p
        ryfr: ce = Gehr; ahz = (ahz << 4) | a;
qrs r(g):
    cp = 0; fc = []; pf = []; ei="";
    juvyr cp >= 0 naq cp < yra(g):
        v = g[cp];
        vs glcr(v) == glcr(0): fc.nccraq(v);
        ryvs v == 'q': fc.nccraq(fc[-1]);
        ryvs v == 'k':
            n = fc.cbc(); o = fc.cbc();
            fc.nccraq(n); fc.nccraq(o);
        ryvs v == '+': fc.nccraq(fc.cbc()+fc.cbc());
        ryvs v == '-':
            n = fc.cbc(); o = fc.cbc();
            fc.nccraq(o-n);
        ryvs v == '*': fc.nccraq(fc.cbc()*fc.cbc());
        ryvs v == '/':
            n = fc.cbc(); o = fc.cbc();
            fc.nccraq(o/n);
        ryvs v == '%':
            n = fc.cbc(); o = fc.cbc();
            fc.nccraq(o%n);
        ryvs v == '&': fc.nccraq(fc.cbc()&fc.cbc());
        ryvs v == '|': fc.nccraq(fc.cbc()|fc.cbc());
        ryvs v == '^': fc.nccraq(fc.cbc()^fc.cbc());
        ryvs v == '.': ei=ei+pue(fc.cbc());
        ryvs v == '[':
            fg = 1; pf.nccraq(cp);
            vs yra(fc) == 0:
                sbe vv va enatr(cp + 1, yra(g)):
                    vs g[vv] == '[': fg = fg + 1;
                    ryvs g[vv] == ']':
                        fg = fg - 1;
                        vs fg == 0:
                            cp = vv
                            oernx
        ryvs v == ']': cp = pf.cbc()-1;
        ryvs v == '{':
            b = fc.cbc(); i = fc.cbc();
            vs i >  0: cp = cp + b;
        ryvs v == '}':
            b = fc.cbc(); i = fc.cbc();
            vs i <= 0: cp = cp + b;
        ryvs v == '=': cp = cp + fc.cbc();
        ryvs v == 'i': fc.cbc();
        cp = cp + 1
    erghea ei
vs __anzr__ == '__znva__':
    k=r(yvfg(g(P)));
    vs yra(k)!=0: flf.fgqbhg.jevgr("SYT:{"+k+"}\a");

