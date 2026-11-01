import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [['5 apples and 6 oranges', 19],
 ['5 apples and 6 oranges', 21],
 ['0 apples and 1 oranges', 3],
 ['1 apples and 0 oranges', 3],
 ['2 apples and 3 oranges', 100],
 ['2 apples and 3 oranges', 5],
 ['1 apples and 100 oranges', 120],
 ['10 apples and 20 oranges', 50],
 ['3 apples and 4 oranges', 9],
 ['7 apples and 8 oranges', 30],
 ['2 apples and 0 oranges', 5],
 ['0 apples and 0 oranges', 10],
 ['0 apples and 1 oranges', 1],
 ['10 apples and 0 oranges', 15],
 ['3 apples and 5 oranges', 12],
 ['5 apples and 5 oranges', 12],
 ['8 apples and 2 oranges', 15],
 ['2 apples and 0 oranges', 12],
 ['2 apples and 0 oranges', 30],
 ['0 apples and 0 oranges', 9],
 ['0 apples and 1 oranges', 50],
 ['0 apples and 1 oranges', 15],
 ['0 apples and 1 oranges', 14],
 ['0 apples and 0 oranges', 30],
 ['0 apples and 1 oranges', 10],
 ['0 apples and 1 oranges', 12],
 ['10 apples and 20 oranges', 30],
 ['2 apples and 0 oranges', 13],
 ['3 apples and 4 oranges', 30],
 ['8 apples and 2 oranges', 10],
 ['0 apples and 1 oranges', 2],
 ['10 apples and 20 oranges', 51],
 ['3 apples and 5 oranges', 10],
 ['0 apples and 1 oranges', 3],
 ['5 apples and 5 oranges', 15],
 ['0 apples and 1 oranges', 9],
 ['0 apples and 1 oranges', 8],
 ['0 apples and 1 oranges', 13],
 ['0 apples and 0 oranges', 1],
 ['7 apples and 8 oranges', 15],
 ['3 apples and 5 oranges', 51],
 ['3 apples and 4 oranges', 8],
 ['3 apples and 5 oranges', 13],
 ['0 apples and 1 oranges', 51],
 ['2 apples and 0 oranges', 11],
 ['10 apples and 0 oranges', 30],
 ['2 apples and 0 oranges', 14],
 ['0 apples and 0 oranges', 29],
 ['10 apples and 20 oranges', 52],
 ['0 apples and 1 oranges', 4],
 ['2 apples and 0 oranges', 50],
 ['2 apples and 0 oranges', 51],
 ['0 apples and 1 oranges', 11],
 ['5 apples and 5 oranges', 11],
 ['2 apples and 0 oranges', 52],
 ['3 apples and 4 oranges', 12],
 ['3 apples and 4 oranges', 10],
 ['10 apples and 0 oranges', 29],
 ['2 apples and 0 oranges', 3],
 ['2 apples and 0 oranges', 6],
 ['3 apples and 5 oranges', 9],
 ['2 apples and 0 oranges', 29],
 ['2 apples and 0 oranges', 8],
 ['0 apples and 0 oranges', 12],
 ['2 apples and 0 oranges', 10],
 ['3 apples and 5 oranges', 14],
 ['2 apples and 0 oranges', 9],
 ['5 apples and 5 oranges', 13],
 ['0 apples and 0 oranges', 15],
 ['3 apples and 4 oranges', 13],
 ['0 apples and 0 oranges', 14],
 ['0 apples and 0 oranges', 0],
 ['3 apples and 4 oranges', 50],
 ['2 apples and 0 oranges', 15],
 ['10 apples and 5 oranges', 20],
 ['3 apples and 7 oranges', 15],
 ['15 apples and 8 oranges', 30],
 ['24 apples and 18 oranges', 50],
 ['50 apples and 50 oranges', 100],
 ['100 apples and 100 oranges', 200],
 ['1 apples and 99 oranges', 105],
 ['99 apples and 1 oranges', 105],
 ['20 apples and 0 oranges', 25],
 ['1 apples and 99 oranges', 100],
 ['99 apples and 1 oranges', 104],
 ['20 apples and 0 oranges', 199],
 ['50 apples and 50 oranges', 199],
 ['1 apples and 99 oranges', 199],
 ['50 apples and 50 oranges', 200],
 ['20 apples and 0 oranges', 198],
 ['24 apples and 18 oranges', 105],
 ['24 apples and 18 oranges', 100],
 ['99 apples and 1 oranges', 106],
 ['3 apples and 7 oranges', 20],
 ['3 apples and 7 oranges', 25],
 ['1 apples and 99 oranges', 104],
 ['97 apples and 1 oranges', 198],
 ['97 apples and 1 oranges', 105],
 ['20 apples and 0 oranges', 26],
 ['3 apples and 7 oranges', 198],
 ['50 apples and 50 oranges', 105],
 ['20 apples and 0 oranges', 197],
 ['50 apples and 50 oranges', 106],
 ['50 apples and 50 oranges', 104],
 ['15 apples and 8 oranges', 198],
 ['0 apples and 0 oranges', 11],
 ['24 apples and 18 oranges', 106],
 ['1 apples and 99 oranges', 103],
 ['99 apples and 1 oranges', 103],
 ['1 apples and 99 oranges', 197],
 ['99 apples and 1 oranges', 198],
 ['97 apples and 1 oranges', 200],
 ['50 apples and 50 oranges', 103],
 ['0 apples and 0 oranges', 199],
 ['15 apples and 8 oranges', 26],
 ['24 apples and 18 oranges', 49],
 ['15 apples and 8 oranges', 106],
 ['20 apples and 0 oranges', 99],
 ['99 apples and 1 oranges', 197],
 ['3 apples and 7 oranges', 21],
 ['3 apples and 7 oranges', 103],
 ['3 apples and 7 oranges', 101],
 ['24 apples and 18 oranges', 51],
 ['100 apples and 100 oranges', 201],
 ['20 apples and 0 oranges', 50],
 ['99 apples and 1 oranges', 199],
 ['20 apples and 0 oranges', 200],
 ['0 apples and 0 oranges', 106],
 ['97 apples and 1 oranges', 199],
 ['3 apples and 7 oranges', 16],
 ['20 apples and 0 oranges', 27],
 ['50 apples and 50 oranges', 101],
 ['97 apples and 1 oranges', 100],
 ['1 apples and 99 oranges', 106],
 ['0 apples and 0 oranges', 197],
 ['20 apples and 0 oranges', 107],
 ['10 apples and 5 oranges', 21],
 ['1 apples and 99 oranges', 196],
 ['24 apples and 18 oranges', 104],
 ['99 apples and 1 oranges', 102],
 ['20 apples and 0 oranges', 30],
 ['1 apples and 99 oranges', 101],
 ['97 apples and 1 oranges', 107],
 ['50 apples and 50 oranges', 102],
 ['24 apples and 18 oranges', 99],
 ['15 apples and 8 oranges', 197],
 ['97 apples and 1 oranges', 201],
 ['15 apples and 8 oranges', 105],
 ['15 apples and 8 oranges', 100],
 ['15 apples and 8 oranges', 28],
 ['0 apples and 0 oranges', 198],
 ['0 apples and 0 oranges', 50],
 ['24 apples and 118 oranges', 198],
 ['97 apples and 1 oranges', 103],
 ['10 apples and 5 oranges', 51],
 ['20 apples and 0 oranges', 104],
 ['24 apples and 118 oranges', 199],
 ['20 apples and 0 oranges', 31],
 ['15 apples and 8 oranges', 107],
 ['10 apples and 5 oranges', 30],
 ['3 apples and 7 oranges', 106],
 ['20 apples and 0 oranges', 106],
 ['24 apples and 18 oranges', 48],
 ['20 apples and 0 oranges', 48],
 ['1 apples and 99 oranges', 107],
 ['20 apples and 0 oranges', 101],
 ['0 apples and 0 oranges', 200],
 ['15 apples and 8 oranges', 49],
 ['1 apples and 99 oranges', 198],
 ['50 apples and 50 oranges', 197],
 ['10 apples and 5 oranges', 199],
 ['3 apples and 7 oranges', 197],
 ['20 apples and 0 oranges', 196],
 ['3 apples and 7 oranges', 12],
 ['3 apples and 7 oranges', 26],
 ['0 apples and 0 oranges', 25],
 ['3 apples and 7 oranges', 10],
 ['15 apples and 8 oranges', 199],
 ['99 apples and 1 oranges', 101],
 ['10 apples and 5 oranges', 15],
 ['15 apples and 8 oranges', 196],
 ['3 apples and 7 oranges', 22],
 ['97 apples and 1 oranges', 104],
 ['24 apples and 118 oranges', 196],
 ['1 apples and 99 oranges', 102],
 ['97 apples and 1 oranges', 196],
 ['24 apples and 18 oranges', 98],
 ['20 apples and 0 oranges', 105],
 ['20 apples and 0 oranges', 102],
 ['99 apples and 1 oranges', 200],
 ['24 apples and 11 oranges', 49],
 ['97 apples and 1 oranges', 197],
 ['24 apples and 118 oranges', 197],
 ['20 apples and 0 oranges', 28],
 ['0 apples and 0 oranges', 49],
 ['0 apples and 0 oranges', 99],
 ['20 apples and 0 oranges', 201],
 ['3 apples and 7 oranges', 105],
 ['10 apples and 5 oranges', 28],
 ['3 apples and 7 oranges', 27],
 ['3 apples and 7 oranges', 28],
 ['15 apples and 8 oranges', 104],
 ['24 apples and 18 oranges', 199],
 ['15 apples and 8 oranges', 48],
 ['0 apples and 0 oranges', 20],
 ['24 apples and 18 oranges', 196],
 ['24 apples and 18 oranges', 195],
 ['24 apples and 18 oranges', 103],
 ['15 apples and 8 oranges', 99],
 ['3 apples and 7 oranges', 104],
 ['10 apples and 5 oranges', 27],
 ['24 apples and 18 oranges', 97],
 ['99 apples and 1 oranges', 196],
 ['10 apples and 5 oranges', 101],
 ['15 apples and 8 oranges', 103],
 ['24 apples and 11 oranges', 107],
 ['15 apples and 8 oranges', 108],
 ['50 apples and 50 oranges', 201],
 ['10 apples and 5 oranges', 29],
 ['0 apples and 0 oranges', 105],
 ['0 apples and 0 oranges', 104],
 ['10 apples and 5 oranges', 105],
 ['3 apples and 7 oranges', 17],
 ['3 apples and 7 oranges', 14],
 ['10 apples and 5 oranges', 104],
 ['3 apples and 7 oranges', 29],
 ['1 apples and 9 oranges', 105],
 ['15 apples and 8 oranges', 31],
 ['1 apples and 9 oranges', 31],
 ['0 apples and 0 oranges', 100],
 ['3 apples and 7 oranges', 99],
 ['15 apples and 8 oranges', 32],
 ['1 apples and 9 oranges', 104],
 ['1 apples and 9 oranges', 28],
 ['1 apples and 9 oranges', 49],
 ['10 apples and 5 oranges', 106],
 ['3 apples and 7 oranges', 31],
 ['0 apples and 0 oranges', 31],
 ['1 apples and 9 oranges', 29],
 ['0 apples and 0 oranges', 28],
 ['10 apples and 5 oranges', 19],
 ['1 apples and 9 oranges', 50],
 ['99 apples and 1 oranges', 201],
 ['10 apples and 5 oranges', 22],
 ['3 apples and 7 oranges', 18],
 ['1 apples and 9 oranges', 27],
 ['20 apples and 0 oranges', 100],
 ['0 apples and 0 oranges', 17],
 ['0 apples and 0 oranges', 101],
 ['1 apples and 9 oranges', 14],
 ['1 apples and 9 oranges', 11],
 ['0 apples and 0 oranges', 22],
 ['1 apples and 9 oranges', 101],
 ['91 apples and 9 oranges', 105],
 ['10 apples and 5 oranges', 25],
 ['0 apples and 0 oranges', 16],
 ['1 apples and 9 oranges', 103],
 ['3 apples and 7 oranges', 19],
 ['03 apples and 7 oranges', 19],
 ['1 apples and 9 oranges', 20],
 ['10 apples and 5 oranges', 31],
 ['10 apples and 5 oranges', 16],
 ['3 apples and 7 oranges', 30],
 ['0 apples and 0 oranges', 18],
 ['1 apples and 9 oranges', 26],
 ['0 apples and 0 oranges', 103],
 ['1 apples and 9 oranges', 21],
 ['0 apples and 018 oranges', 103],
 ['50 apples and 50 oranges', 202],
 ['10 apples and 5 oranges', 48],
 ['1 apples and 9 oranges', 10],
 ['1 apples and 9 oranges', 22],
 ['10 apples and 5 oranges', 50],
 ['0 apples and 018 oranges', 105],
 ['0 apples and 0 oranges', 107],
 ['0 apples and 018 oranges', 201],
 ['1 apples and 9 oranges', 19],
 ['15 apples and 8 oranges', 27],
 ['1 apples and 9 oranges', 25],
 ['10 apples and 5 oranges', 18],
 ['03 apples and 7 oranges', 21],
 ['10 apples and 5 oranges', 202],
 ['0 apples and 0 oranges', 13],
 ['1 apples and 9 oranges', 15],
 ['0 apples and 0 oranges', 21],
 ['20 apples and 0 oranges', 29],
 ['0 apples and 018 oranges', 200],
 ['0 apples and 018 oranges', 49],
 ['1 apples and 9 oranges', 201],
 ['0 apples and 0 oranges', 102],
 ['0 apples and 018 oranges', 99],
 ['91 apples and 9 oranges', 103],
 ['0 apples and 018 oranges', 100],
 ['99 apples and 1 oranges', 107],
 ['03 apples and 7 oranges', 20],
 ['1 apples and 9 oranges', 32],
 ['0 apples and 018 oranges', 106],
 ['1 apples and 9 oranges', 13],
 ['3 apples and 7 oranges', 107],
 ['15 apples and 8 oranges', 29],
 ['0 apples and 0 oranges', 48],
 ['10 apples and 5 oranges', 99],
 ['03 apples and 7 oranges', 100],
 ['99 apples and 1 oranges', 108],
 ['10 apples and 5 oranges', 26],
 ['91 apples and 9 oranges', 106],
 ['3 apples and 7 oranges', 202],
 ['03 apples and 7 oranges', 51],
 ['0 apples and 018 oranges', 104],
 ['03 apples and 7 oranges', 18],
 ['50 apples and 50 oranges', 107],
 ['10 apples and 5 oranges', 200],
 ['1 apples and 9 oranges', 12],
 ['0 apples and 0 oranges', 19],
 ['1 apples and 9 oranges', 200],
 ['1 apples and 9 oranges', 18],
 ['03 apples and 7 oranges', 99],
 ['1 apples and 9 oranges', 100],
 ['1 apples and 9 oranges', 48],
 ['10 apples and 5 oranges', 100],
 ['91 apples and 9 oranges', 100],
 ['03 apples and 7 oranges', 98],
 ['3 apples and 78 oranges', 202],
 ['03 apples and 7 oranges', 28],
 ['03 apples and 7 oranges', 52],
 ['10 apples and 5 oranges', 49],
 ['03 apples and 7 oranges', 97],
 ['3 apples and 7 oranges', 51],
 ['99 apples and 1 oranges', 202],
 ['0 apples and 0 oranges', 52],
 ['3 apples and 78 oranges', 99],
 ['10 apples and 5 oranges', 103],
 ['15 apples and 8 oranges', 202],
 ['0 apples and 018 oranges', 20],
 ['1 apples and 9 oranges', 17],
 ['020 apples and 018 oranges', 49],
 ['1 apples and 9 oranges', 99],
 ['10 apples and 5 oranges', 52],
 ['03 apples and 7 oranges', 103],
 ['10 apples and 5 oranges', 17],
 ['3 apples and 7 oranges', 108],
 ['3 apples and 7 oranges', 49],
 ['1 apples and 9 oranges', 16],
 ['03 apples and 7 oranges', 201],
 ['1 apples and 9 oranges', 199],
 ['1 apples and 9 oranges', 30],
 ['1 apples and 9 oranges', 202],
 ['100 apples and 100 oranges', 202]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-qaJJCd%ck%l#fw3e|ZNG=I@+K3_q355LFz*u9oF-'
    b'B{@da`u>>RCV<)zQ&?PSsz0keBxYeDyzn{^$Sw{ZC*2{O$Mu{OvFQ{g0KK{{Guv?arok-'
    b'qli-v(~ETrfDiNURiR|UhkFMjxL?~4&n1@B<Z_$X}A9VzrX+EKYsgbI=!7Y(`q&uB8|Car}J(b`<0uX-nqB#*JR1tR$nUn^kddvZ'
    b'8Coi^G+VcZmT2r-'
    b'dmEoB(+wybxm!VYA>^`)B3*m=GD(SRkUg!U3$y0!|YY1wSD$^TYI;rSyR8M=C+erOK+Zbto4^zW?Si$x`*ww?(F-'
    b'>uVJK)+Rm0jT;|xdHtXxkOL^{+QqHA_EarQ+B~4q#S+^V?Gi6Kf*D(5wPi~o#@6(b@kE*P9GwCRU1)g@d)HA9P^fOa$X4*zC{Na6'
    b'O)A_5kllLU_Pjl6L?-'
    b'{2kLl1qcE;YS}@rJFeIkVDn_HEb7OTn3{xgQ3wlJ2vs=bU<ny>V)l+TJA!g(5m{ymrP|M{}3O2sx$trha0hbJp>W<W^U!wdQIslf'
    b'7%H&Bhm5+Fh23E#;WY9o;Cry~|-'
    b'nCANx#5<XdHEgoH~>8v?>Ej!<yPM$^UQ7dIGEsw^PsijJ{*;y+=RNDL3Fg($2Zlk@<kBSh=dH2r!Dr@O=i=8PfLS<xvIP!kAzIvW'
    b'{w0msAgBBH(sX`0q$^iZJe$S=D7G+XK-)Z-y!zN?S#24~qme(8wgz2Q$-~6B-'
    b'#hPu+%3~9cWEs0W0}<vt`>pw`(Oi^ws_WKlHJ3L=+jr_a=cQl6ti1=zzP%<L+A|L;1o$4lG=`m#Z4ijXoD%t4qiB*_LFY_Z^QUeK'
    b'S?F)mISp)h08s<c$!nQMr5w`JS6)ot+lVj7%WugpWf1?mKEq^DyDQCQ1cKq_yVPpWp0zPE0W#vfc9C~`dpgRjXXdiW?rZzkFn82M'
    b'5okViX3MHWj9`>}x(%NO^+b)dLV%TZb=?b$Q(A&G%p4oyb4vD1T3bu^C4>WLSoaQEmf;l;X?qgT+DbW8cb(9lB-'
    b'%NhnqoUVXg2RG)dh|=r5moT@vgl$t*o(4salz@%#!l;L9Z4q(r@jQ5Sh=hi>mcfa^z^ii)SRB`AQu#(Vw^4sm-'
    b'NEfur_J+LH*WyNM3t(LH@Se3U(?`_%66&olQoq>=HvmQ667nf6s?UuFU>Z76SB-kJvCdih5xiXik05^X2TwmWj8e5%c@w*dVwH%Y'
    b'JY@rH&__}9NztX2bH+gw}Q?Ys1E5M_bOUPnBLJyzIIN&JO687Pa|y$gGKatzEV)b_1ZLkFmN!2j#;kh%$~;>U=Mswz4=C`p(b3Mp'
    b'rYRMwx#+n8igK*DufE~aTogIuigv=h6ipt=Fk8)9oJ=+WT2y?}}~$~h1z>cCb<>b-'
    b'uqK3^lWIe}>kr!0d`VzD?#i3XKlnd*9TZ1BVfG@?-'
    b'Gi!vz?ezu4a9&y^6;IfgUmlI%`&mO3%Po`kMR}mVi>!sM7I@f?k`>Z|jJ#tMr3j;0Ge4he9BW3~Zy+tKf&{Bz4nnTi4+IW*CPXO3'
    b'(a!IYHN?Cj8Xn4#^LIb>(wi3YuEJ&;{2@-8VJr&dpL9H2-@F0^I6yhN35i}cJb(ib3O_U(W+aCRZmaQZQ9lFL^6P-'
    b'&_k_P}p4@{^os(9r1=wfKFIyRxwaQtKSi8e6C=q}3){F%3m*^j==MEVx#@DRec8(k%_uoWZ)f)*8|D1w?HXmcSd;W4)CXX%?DlNb'
    b'b|LBj-9aZqapCH!Y?O8u;1f?^Xyce}L)<Djr0?12(X6L-'
    b'H6(3vVr)Xc015LmC>x6r9HD)h$>q?QnNpYkh`_}FC~;9@hmyH26c+pcok6smYFK`kJ|sA1}K?z4S!-~mP&JIu%sDZ-'
    b'd$!X*s;17ZvzHVfhDF#&Q)8h2m0V`qX}`GoA<D*^r9l5ggclGQJ?^_<|y>fjQ%17m}pG}lS5qDvp)C;5B31Wr@PZ2e9+ybIW+O5-'
    b'sWd2aH`qaX9`4I#9sAu9`B@Vu|5aw<9=uuMh9w@OF<pOkkUQWe{e_o0bz?#yZ-'
    b'V0kk0r@9Ww)>G0NeE_6+A3V=Ku>=z(uVYv<s2PIlCJ54_q=2h$w;5$1>?U!k{UOgcMr592sCVCQ;x8GiiwdIQSDpDOFgJ7r(;d~&'
    b'`4_;UTZ%LumQQ!*D@=i!9w(!~7o8_b=xzrj+(o9b-'
    b'nYDticQdQ1&yEx7?YY4;d{PYLAVx1bzTO$?G~3U^=qfXw@gnbD7e0vaKN!Uw0B(`@#v^J=>D{E(?L<4UGkJN_0&Ex6FiIRtR~o!L'
    b'!X*s3c~CLo5Yx5_AJEw3+@p&MC4*75q)*-'
    b'BrHVnpi~n4RS8=IXX!}2k7jK{&IkRdFzrgKW{`E1yAjCbOdW;*;Mefnk9w=e=tpV!NT-4yZ0P$MpV%y_ZG-'
    b'#t_F5qOAhMN`gQ#mB2+*ggs4CuF0rEPVZ+1W)42pFO_Th$#&O#68adCQc8XWXmqp1aCnm$9x+U+DHAFdDSv4Me7H;r|3>}-'
    b'P2&$qc(B6Z%>q$Q7mOx^Gt1VF!8RiJpfTQ$ZxV6i;BLS5<B*FHU!S2?@&>}h-juH3%eRB2TuzujP8YzOR%5c4xR;j5c&eR-'
    b';@=GgKJ>Tq?E&A6f6k5uHvpr{Z3I}=SoD6L&w-'
    b'gx|+uHK7*Gpjh9dd2=ROj9%sq~O>FSmd5xA(~7KMS_4BHQ7t@Y|u8vh;BKk(PZ$U^w=HRppBQHBfuafx>lKw$7iYxKG>by_lE~JA'
    b'7^@Hw_G1|lZ3jhq)w}(G=c5(&ZqqPp)4Lk%Np9dF&9?XeK|;~jlEYWP8pT{KCTBh^;q6?S=tG}hr_8gnn4W}wniHC$vC|filuf!O'
    b'uja*FjL`G0S96PJv~0RaF<Pf<o-=i-9+6niHS|$O;K5oew#hpyr-'
    b'?&fLz=3acgS>5m{$F;?iWL)buNWcL3GnGn?kyc>vY{xyv5>sraTdzGhPc6aZZb9Uc_;o8wjha7z;c0eFD|v5P{!=SfoFB-jx4G33'
    b'Z$6{P#kJ{zikqsU5O4G#v&c$&@vCOwAp{8$e%H`Ovd1C{Y~K#DfRHC!qt`<X$4%gUB}_}@C#+dJsD3!9JV>t8?XoFNE{gJM$>IiM'
    b'IIN**h|*F7*!fT}Q~<jO)1aM@)7WGD?LK6bZe3L~aZ!Vy=<r+NuUVyUo{P>Dt=G0Z@&Fy=c35!bqEA<@@aY#J82-'
    b'tr+|v<n&x0XUJttEX)|3LM8^-'
    b'i)fL!}nV{iic2O1M?aimd5<c=4qeVK+M&%tz;7YL54A`chXXAGPydIkc8$kVpUW}S#7)4kc}F&Z%7Bq8j^8Qqz2wTRYH_}v!T=Rf'
    b'-?bo2O<ES1Eg<0YuUM^&=ZtM@ZMH$xRQ#szSM*O!j0t@n`kU;Ohlm6OOs~!%yrn8**WwTP6AktJ?2V}N<$i%3z}Ld(eD{vr$t<Vk'
    b'balDy*5L=L()3tnQ-'
    b'g2459X5%X)W4!8Q5^*^_9)Q6~vSNz)lrH1p`G`bGfcZ=Lei+g+8WgM^fiF79{=m@89vd3g?jYl_@P6<C)PQ_Ba<M>!V^x?Vpmx=d'
    b'A_1X_*lsURg9w5XtMpdf+)ZS)Knc9=Hk)(Y@VFa_J+aB-jtEe*m_2i>U^{Y4vN@71GW(R&mj*9L>s76hyAm**PCaTi}q4-'
    b'KTWKIDbq6&#_V0}L>KI-'
    b'o2>gfD>*_4`~C^Nmp%9bddN64kf25#fC`KcIwg2r_7AprQEos&BaXQwzn=vVB05aIeDrFu8u>oc9<HVc?H%s3$uhM?Fjr2@eC(7D'
    b'Jv6ps9H9X6&v&kV(8qfc{*%T!E?t&aV_N*tGV}#FSurj#Kx##M2tcgTZO5F-'
    b'Z9w5UkRx^M+*d+Y=3e1Uf5y`CXXpxo*5tNauVwiR4>AZ%;^|U>ZNec=Gs(p_%D#I8TmA<FS%ZpU9DlAAvF_HONr#-'
    b'A>)5CT5cuNUWmhfD-luKC1Ja;dUQ_hhwD`p)&2^RWF(k%SQWW6d<OpPjLMZh;Q-*rRl=!@|O~nuftNN@K8h~-!YZm#~R-'
    b'wL^KKCqy3Ji@nq){dz2Ft;-7V=4McJH!9i1;^!h!;ccIZbDX-'
    b'!%EVf)eP^0Z!RM|GLyZdz@n$Lpo`^8`}A!B|6BQ}h6*Nm1yFdli-5LP3B8tFFbx}79$NhmzG*;JI@mI-c#7}yF@Tcd8=<Kyc@-'
    b'#QgaoQa=ryZClA<lEP~6;wMnl|;gpdCq5FGi!>K*Fi@)LH8(vc9TkP?)E{T%F|d9EZ_u9wH|nYB3RF#<0NxYQ#*}}FM?Png1$=ZU'
    b'4fvBdQoS-j-VX~q;wf^GG(d-jqCd-z4&?Q!DTh{iXkyE=`0KaeBL?KL+oo<Ved1TS@C;w6f6<BlEw8cP+)Y#)j2>K-'
    b'|1aUr6T_*$%a~>%FnLf7iVC0yvu$Gg<2nqPi9KYWHl;Qj{@-'
    b'?s_wSOwIH$sy$lSX8&Gz!+7IDzagXl0GD7;OX6m))h7h7!`6(L+a}dCa!yUlqi(eRIO57}#!-'
    b'Fmc(@t`6yQq?l``ZI8=BNBb>)<y~)Zhf5h$of?5;as=O~Bjry85;rv(Qi!c)xS4-DD5HQ;C{s**zR(St&|v)^@t_(NH<F-'
    b'lTx|ET6imkLUurRe0`hZgF9e!5VL&qEpG>JgljX`_D}SYH=)9h-PH4&yES$&xEEQf)13TH_&hnfk}#=GBn>I8I-'
    b'+1iWo94Nue$221x7sJUpG*eTxxwnU}sfsdYfR!gighCgkTNm%cM^I765i+7g^eQiRJ0zIz=5qCd-'
    b'P!j=N!f$Xv#fJ~T?YR?ZJd^^JI80t464^cIS)2B^X|MK=uu=cmUDJQcmvpt@l2-'
    b'pI1Fi^KWtO`w5)!&9OwT>&?lk}|z8mX7W_Z^cUDG+pA5yat?JoUCKHVdgS3TE7UGoS9huS_J{MTO8}wF95;I(QbI%$z8eZ<*8%3k'
    b'LS8)QY}B_tyD3N{6n7e0<LzCx(x?pah+HK^$nuSpb&)jtw|~QeED!ums)`_NK)rD}p!)YG3FmzzZj^aE%3EzqrKVh`FNQ$_cuA&A'
    b'O9c76o#1o8T+;PEjy|<1Q?=dRJO$$<SirU7JX)IS%GOZc4@6OAnF)L24`L6}2E;9F(c37cGMbCPpUt+d7ofJon)17OuGX);%LOhf'
    b'_T6_}U<ME0(hxDk4xRNrV*L*kVuTgX%^yP?!i|@=ZC=ZBZQhr2~9}Sm=kIvH8C5MjWxffEyh{K~EijEGniogZ4y&U`r=rEIshB@M'
    b'N;7Mp+YEy1;Ef!=4+ua9}mSbTl&>67AS(VdAsL(%sLxP#)x9g7i($Y@&q8k9uP%>Se+h*!o$&x*=%WIq2S2*oCW*VSZMKgPI}gb>'
    b'SFA5mkOM7a)R;j)P2M&{f<7+Ch;G*uT&3$;&h_-'
    b'FNwkFbz7_n0KIP%VvRVxn*lZSUFzVZt%-JF<TwJYWk2YZ^Ry+mM6Ck=OdGVQokagFq7FdZv-pYM87@jCp5S88+?mwAmI9h2v}-'
    b'$|63NpeAFVckhxJpv?8MXGT|a_El8M7W@PDmzgVlk7`SQkPQFmF$=|INIuucZ@I*^LT9%4ZSK*JfY-'
    b's2XT`=4nvFI1Y;XmqEQw4Q+&<XU<dhIjFPX(19%%yFCkCv?iU<!r~^uHjB_bHgLbag0=-'
    b'pPdx*ZQpU^1++Ysj=>ko^6gz_^s<LS`9Hyh=GjmxIOx98QX&+N>d=^eCSI<h4(=mODv=Z9ajYPRM5F*kh=>KZ9$&lJb?bD#ZsXkR'
    b'IoWaUYrtYrI!3A>Fbz;;&&3o4|v89e=XB5x;_1ouNnniISBf#DnS?Zg0`Kbey3CnPeol0F+oKV=Z6R^EgisS5gnyYI`l6>gMvrs0'
    b'jAq4NZRmvdx^groaB!?v~a-z7CIU$EiA?1K_07-Pz6irD2U^trr@Q5^coP2=0`e@me_-(pY_|n4zh6yq+8Ns-mG}_GxGR?6w-'
    b'lyNOTM8>fc`%N0~&3t^iNpS5<=U-$ebARCTLRO2?@Uh_LlR<zix4yv&S41DD6-'
    b'TYkm2AHZ)iG2hQb8NA?31?}ty0R_!a{H56oswsNk=6DaV>enxnRGisGilA@m*QHTbj5=sk`lA!*hgh!}^_v)D=nmWf<<QTaxDViq'
    b'3P?)o{T*u*Pebhj-'
    b'V2ZtnqfT~XvFdgfmGl!c8}uuomE=AKK<&O*8I8!6y!aKo}lCW${+fM86bY{hO8=(DJ9AMe$i6B_cm~>{_fM8uI#f<Yr9t@F-'
    b'SEkl2B=@n_7PZ;pz{16#rhamNf{AqxL8Y$fpcLxQ-WJ`=Yn(ulAPrbxmp+U73dOg15{lsPF7Aax4nv#U?zcii3UuNf4w*@l=p7iN'
    b'RvP^|0y!qflzKK?ltV!l-&&h-'
    b'M61wZ#`3%AF*4tLOvVXn}uviQT>aS(jgf4r{}HPg{tArb&T><}Zk1H507ltmQBJPd(J7pI5bWfGYUO#h#H+ePG5O)YXgK1P{{10d'
    b';f#>t9^(#LN'
)))

def _is_floats(value):
    if isinstance(value, float):
        return True
    return (
        isinstance(value, (list, tuple))
        and bool(value)
        and all(isinstance(item, float) for item in value)
    )


def _framed(payload):
    return len(payload).to_bytes(8, 'big') + payload


def _stable_output_bytes(value):
    if value is None:
        return b'n'
    if isinstance(value, bool):
        return b'b1' if value else b'b0'
    if isinstance(value, int):
        size = max(1, (abs(value).bit_length() + 7) // 8)
        magnitude = abs(value).to_bytes(size, 'big')
        return (b'i-' if value < 0 else b'i+') + _framed(magnitude)
    if isinstance(value, float):
        return b'f' + value.hex().encode('ascii')
    if isinstance(value, str):
        return b's' + _framed(value.encode('utf-8'))
    if isinstance(value, dict):
        items = [(_stable_output_bytes(key), _stable_output_bytes(item)) for key, item in value.items()]
        items.sort(key=lambda item: item[0])
        return b'd' + b''.join(_framed(key) + _framed(item) for key, item in items)
    if isinstance(value, list):
        return b'l' + b''.join(_framed(_stable_output_bytes(item)) for item in value)
    if isinstance(value, tuple):
        return b't' + b''.join(_framed(_stable_output_bytes(item)) for item in value)
    raise TypeError(f'unsupported output type: {type(value).__name__}')


def _output_sha256(value):
    return hashlib.sha256(_stable_output_bytes(value)).hexdigest()


def test_humaneval_plus_suite():
    candidate = fruit_distribution  # noqa: F405
    for index, arguments in enumerate(INPUTS):
        output = candidate(*copy.deepcopy(arguments))
        comparison, expected = EXPECTED[index]
        if comparison == "sha256":
            if _output_sha256(output) == expected:
                continue
            raise AssertionError(f"HumanEval+ case {index} failed")
        try:
            exact_match = bool(output == expected)
        except (TypeError, ValueError):
            exact_match = False
        effective_atol = ATOL
        if effective_atol == 0 and _is_floats(expected):
            effective_atol = 1e-6
        if exact_match:
            continue
        if effective_atol != 0:
            if type(output) is not type(expected):
                raise AssertionError(f"HumanEval+ case {index} returned the wrong type")
            if isinstance(expected, (list, tuple)) and len(output) != len(expected):
                raise AssertionError(f"HumanEval+ case {index} returned the wrong length")
            if np.allclose(output, expected, rtol=1e-7, atol=effective_atol):
                continue
        raise AssertionError(f"HumanEval+ case {index} failed")
