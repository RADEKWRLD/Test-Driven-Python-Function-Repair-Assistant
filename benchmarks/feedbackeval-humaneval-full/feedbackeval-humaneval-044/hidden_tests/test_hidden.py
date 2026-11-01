import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[8, 3],
 [9, 3],
 [234, 2],
 [16, 2],
 [8, 2],
 [7, 2],
 [2, 3],
 [3, 4],
 [4, 5],
 [5, 6],
 [6, 7],
 [7, 8],
 [10, 5],
 [15, 4],
 [25, 6],
 [33, 7],
 [45, 8],
 [50, 9],
 [13, 5],
 [17, 3],
 [42, 8],
 [15, 2],
 [8, 4],
 [2, 3],
 [17, 8],
 [7, 8],
 [9, 5],
 [7, 6],
 [5, 8],
 [45, 7],
 [4, 9],
 [3, 3],
 [8, 8],
 [2, 8],
 [15, 7],
 [50, 5],
 [8, 7],
 [25, 5],
 [17, 9],
 [5, 9],
 [2, 6],
 [9, 9],
 [4, 4],
 [7, 7],
 [5, 4],
 [3, 7],
 [13, 7],
 [15, 3],
 [2, 2],
 [17, 7],
 [7, 5],
 [10, 8],
 [3, 6],
 [16, 8],
 [18, 2],
 [15, 5],
 [6, 6],
 [46, 8],
 [7, 9],
 [5, 6],
 [16, 2],
 [50, 2],
 [41, 8],
 [16, 4],
 [46, 5],
 [17, 2],
 [3, 2],
 [3, 9],
 [13, 8],
 [9, 6],
 [42, 7],
 [10, 4],
 [45, 6],
 [15, 8],
 [43, 7],
 [5, 5],
 [3, 5],
 [4, 3],
 [13, 9],
 [9, 8],
 [33, 9],
 [6, 3],
 [10, 7],
 [8, 9],
 [18, 7],
 [19, 7],
 [43, 5],
 [46, 7],
 [8, 5],
 [16, 7],
 [34, 3],
 [16, 6],
 [6, 4],
 [4, 6],
 [5, 7],
 [4, 5],
 [15, 6],
 [3, 4],
 [14, 5],
 [14, 6],
 [10, 9],
 [46, 6],
 [5, 2],
 [18, 9],
 [18, 8],
 [7, 4],
 [35, 9],
 [4, 8],
 [6, 5],
 [50, 7],
 [50, 8],
 [13, 4],
 [256, 5],
 [2019, 3],
 [34567, 9],
 [27, 3],
 [987654321, 8],
 [9999999, 9],
 [123456789, 3],
 [2669, 7],
 [48298461, 8],
 [245678, 7],
 [9999999, 8],
 [2019, 4],
 [987654321, 9],
 [245678, 8],
 [123456789, 8],
 [2019, 9],
 [6, 9],
 [2018, 9],
 [123456789, 4],
 [2, 4],
 [34567, 4],
 [9, 4],
 [256, 9],
 [48298461, 4],
 [245678, 3],
 [48298462, 9],
 [2669, 4],
 [1, 3],
 [2, 9],
 [48298462, 4],
 [2020, 3],
 [27, 2],
 [2669, 8],
 [4, 2],
 [2, 5],
 [245678, 9],
 [9, 7],
 [48298461, 2],
 [9999999, 6],
 [9999999, 5],
 [245678, 4],
 [26, 2],
 [7, 2],
 [2020, 4],
 [987654321, 3],
 [2018, 8],
 [34568, 9],
 [10, 2],
 [10, 3],
 [27, 8],
 [256, 4],
 [257, 4],
 [34568, 2],
 [9, 2],
 [34569, 2],
 [1, 2],
 [245678, 5],
 [2670, 7],
 [2, 7],
 [27, 9],
 [5, 3],
 [34567, 2],
 [34568, 4],
 [2669, 2],
 [26, 4],
 [123456789, 2],
 [2019, 8],
 [34569, 9],
 [6, 7],
 [34567, 3],
 [0, 3],
 [257, 8],
 [2669, 3],
 [26, 7],
 [2019, 5],
 [28, 3],
 [123456790, 8],
 [34567, 8],
 [257, 7],
 [48298461, 6],
 [256, 8],
 [2669, 6],
 [26, 6],
 [34568, 3],
 [27, 5],
 [26, 5],
 [9999999, 4],
 [48298460, 2],
 [2019, 6],
 [48298460, 9],
 [48298463, 6],
 [48298460, 7],
 [123456790, 9],
 [48298463, 9],
 [27, 6],
 [34569, 4],
 [27, 4],
 [34570, 9],
 [256, 3],
 [245679, 4],
 [245679, 8],
 [257, 9],
 [26, 3],
 [9999999, 2],
 [1, 6],
 [8, 3],
 [48298463, 8],
 [2669, 5],
 [123456791, 9],
 [257, 6],
 [0, 8],
 [123456790, 7],
 [257, 3],
 [245679, 9],
 [34570, 7],
 [1, 5],
 [123456790, 4],
 [48298462, 2],
 [9999999, 7],
 [34569, 3],
 [123456791, 4],
 [255, 5],
 [123456788, 4],
 [123456792, 4],
 [255, 6],
 [10000000, 8],
 [255, 9],
 [8, 6],
 [123456791, 3],
 [255, 2],
 [1, 8],
 [34568, 8],
 [10000000, 5],
 [255, 3],
 [48298461, 3],
 [48298461, 9],
 [123456790, 3],
 [34569, 7],
 [34570, 3],
 [123456789, 6],
 [123456788, 3],
 [257, 5],
 [987654321, 5],
 [2020, 9],
 [2018, 6],
 [1, 7],
 [48298461, 5],
 [6, 8],
 [48298462, 8],
 [34571, 7],
 [0, 7],
 [34571, 2],
 [28, 7],
 [34571, 4],
 [257, 2],
 [34569, 5],
 [11, 9],
 [48298461, 7],
 [48298462, 6],
 [245680, 4],
 [11, 6],
 [34568, 5],
 [10000000, 6],
 [48298462, 3],
 [2018, 3],
 [34569, 8],
 [245679, 5],
 [245680, 3],
 [10000000, 4],
 [10000000, 7],
 [9999999, 3],
 [34571, 6],
 [28, 9],
 [1, 4],
 [11, 7],
 [2670, 4],
 [0, 5],
 [123456791, 8],
 [123456788, 2],
 [9999998, 5],
 [34571, 8],
 [245679, 3],
 [123456792, 7],
 [34568, 7],
 [123456792, 5],
 [34568, 6],
 [123456788, 5],
 [2020, 2],
 [2670, 6],
 [48298460, 8],
 [245678, 6],
 [9999998, 3],
 [34570, 5],
 [48298460, 5],
 [10000000, 2],
 [123456792, 3],
 [2020, 8],
 [34571, 3],
 [245680, 8],
 [123456791, 7],
 [6, 2],
 [123456788, 8],
 [255, 8],
 [9, 3],
 [123456792, 2],
 [258, 5],
 [258, 9],
 [48298463, 3],
 [2671, 2],
 [245677, 4],
 [10000001, 2],
 [10000001, 8],
 [48298463, 4],
 [34570, 8],
 [34571, 9],
 [48298462, 7],
 [48298460, 4],
 [0, 9],
 [9999998, 2],
 [11, 3],
 [9999998, 6],
 [2671, 4],
 [2018, 2],
 [245676, 5],
 [123456791, 2],
 [9999998, 7],
 [28, 2],
 [28, 5],
 [10000001, 6],
 [34570, 2],
 [245676, 2],
 [11, 5],
 [2672, 5],
 [8, 2],
 [48298460, 6],
 [34570, 4],
 [256, 6],
 [123456790, 5],
 [48298464, 4],
 [2669, 9],
 [123456790, 2],
 [0, 2],
 [123456790, 6],
 [245677, 5],
 [2020, 7],
 [255, 4],
 [2019, 2],
 [28, 4],
 [10000001, 7],
 [48298464, 6],
 [30, 2],
 [25, 2],
 [123456788, 6],
 [258, 2],
 [26, 8],
 [245679, 6],
 [2018, 4],
 [0, 4],
 [34567, 7],
 [2018, 5],
 [27, 7],
 [10000000, 9],
 [987654320, 8],
 [245679, 7],
 [3, 8],
 [245677, 9],
 [34567, 6],
 [987654320, 6],
 [245677, 7],
 [245677, 6],
 [987654321, 6],
 [28, 8],
 [987654320, 9],
 [245677, 8],
 [987654320, 7],
 [987654320, 5],
 [4, 7],
 [245677, 3],
 [256, 2],
 [245678, 2],
 [26, 9],
 [245679, 2],
 [2670, 5],
 [2670, 8],
 [987654322, 6],
 [987654322, 2],
 [2017, 3],
 [2020, 5],
 [10000001, 4],
 [0, 6],
 [987654321, 2],
 [123456789, 9],
 [10000002, 6],
 [987654323, 2],
 [10000002, 7],
 [123456788, 9],
 [28, 6],
 [2017, 7],
 [25, 7],
 [2670, 9],
 [987654322, 8],
 [10000001, 9],
 [987654323, 4],
 [25, 3],
 [29, 2],
 [10, 6],
 [987654323, 7],
 [987654321, 4],
 [29, 3],
 [2020, 6],
 [987654320, 2],
 [245676, 3],
 [9999998, 9],
 [245676, 4],
 [245676, 9],
 [2016, 7],
 [987654319, 6],
 [987654319, 8],
 [10000002, 5],
 [2671, 6],
 [7, 3],
 [987654319, 4],
 [2017, 2],
 [987654319, 5],
 [2670, 3],
 [2018, 7],
 [25, 4],
 [987654319, 7],
 [10000001, 3],
 [256, 7],
 [2016, 5],
 [245677, 2],
 [34567, 5],
 [2017, 6],
 [29, 4],
 [10000001, 5],
 [29, 9],
 [48298462, 5],
 [987654320, 3],
 [9999998, 8],
 [48298463, 7],
 [987654323, 3],
 [2671, 8],
 [48298459, 2],
 [10000002, 2],
 [987654322, 4],
 [987654323, 6],
 [25, 9],
 [2016, 4],
 [245680, 7],
 [123456789, 7],
 [2668, 8],
 [123456789, 5],
 [987654322, 3],
 [245675, 4],
 [2017, 8],
 [987654321, 7],
 [48298463, 5],
 [48298459, 4],
 [987654322, 7],
 [48298459, 3],
 [12, 9],
 [2021, 2],
 [987654323, 8],
 [12, 8],
 [987654319, 9]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-qaqJJu{aa-'
    b'~@<RE?#iUU(azaUv}kUW<B9poLy7QDmt#*8a9<hW{LZ3rRAW_ns5s55R0c05in@^WXp1|Nejf+w(vF*MI)c|M(yO_rH6p?LYtH-'
    b'){0)c8Vdia;%)PMzz`V^d9bBb*5`Gw>drCJhyo$VTGP|xTDr>|M~y@=fD3S|M72S_uS&?x8<1lBLBae=bS7gpH|Wwd!{}{y8YNa^'
    b'@dX7@RWBty_DZ&R<9OYJu|K{(>kHLPcEB72)=!tlg3J8mb?1wme=u}RxXn#KlOK+Sy#O$w-'
    b'cQU<h^g3xpJG<b{WZ2seV^;p6Qf%_q}J17V-'
    b'>Zo)+#uFSB;zQB&Ec#aL<_qmSHIo+sTEc5F9<GfpXUgx#9QaA)zlvN1T(>pw4Z7_(mIDx=gn`{2D|zw2&B$;Qni-rMitJ<Dk)bh~'
    b'DG<g+cUmaYHuGQ6$vPHAVa-h8cod72RR<;_BkH`IKio-X*^^+r24<+!(%63RXQyi8_Tc5XS_K4n|*e&T4%%87k%Ph%|GVYIP#>>-'
    b'U%!^vi8)Vyww^Ebq0aq-'
    b'0vtub?U&rI&@W%kzAWp;_37F+hgv}qEGjlm$yox<w<_cXdM@5CicbIN^d@1Y(aw#<$bRIAlF?$|Yl%s}1|ays#xy{G+Vio4{Qd6P'
    b'DL^>i7a+wAaO1fw2d>~;=uQoT6wvn}pE&g@~-'
    b'v`6^oWhyh|JrWX^sSY>B9GJ3Ues1qMFtmm7BrNaEwKWFaLad?9S}XJSdm7)92XThjhzU;wT3+USGk2TEiHIA?Bf=@ga_iyR9$l}v'
    b'%Z&fLOqku5^B5zY?95hR+Gnq0#7&6w8#F|>1R^@bb!!`G*om={(>B}tH20Vu^7hiW8iN#-'
    b'(yfo(gO#z?@G;jVfKTVDg}<w<r;(JQzwjfz$h^Kr4AYObF`Q84wbM>>wv?7<Z?T_E@~x~8XA*BsfW)=;GNooNTo>_AfY(CI<*Z!T'
    b'=Q3^OlJ>zEq+-mYt+g2FHCGS3DH-tXWfFsDAi*N;?Uvp<(=dbQ70QVMvtg6}T0Q$=rdr<&*0z1uF0KDw>VhlL;+;J)%b5>Z9KGdJ'
    b'*Y;wofS37hkKKvxU71FndjPUK%w2yIo_6S-Q%#MGW1hiWH?y%B+LVZl$@Hgl=S<||xL{aFd}Fzt+T$-7%-'
    b'usKBuW9n^PB=Z;4lLN(N@i)2QTDwB=E}FYxfRZMd0SnvGTW3{1I&JI7eLGEP-'
    b'2X&si8P(odtk*Ghbzv50X$aoqhtV=3+!nHliqew*P$Sz60divfxOkm^3m$c>~_Q(O{_?UV=zwF}^cWF^kI1%u~hh5>PfBpw=!B%~'
    b'Yao|jzoeET$*r(C`Vq}A+mp0V~AjnFzX<TC7I5WQ9z`BU<m<ABs&&T3=9u;m=Tb>v29MX0vcTu*I8alT1x9)0w0nV~L#%THfh`Ey'
    b'{}O_-'
    b'gS$80(9Iw%1oK-4%CvZ91Q`UV1R@SmN(z0AK>6gvZk2Dt_G0ntI${WLG&N&`+nyk3xB*7rzgsguzWAu9G3u}Tzu8-5>YKRd-qlU0'
    b'GGTGLH6)RiJ?4QStB8JKnZj?i|U(FxPT90@_Y*I@o_GJG`Q|5{P}(Pci0n~#*J$O}XPfe+6m>SxLa?^rvNhp{=U7U+94-'
    b'WA)@M_J%p*)73k{TDZpr$k4L5DdOW9Gzo^+2NBZ@HDIS9Hl4PFsu-xNDy2C04s!s+}{rIN5TZjk@CDTba0?d619K?4U#@FUFgXp('
    b'?r~klMscy_2S0BTxb$FPTyYUqY3{?UVFh^HQ)$!SczeaDQcES9$;_LU-T53TWgVbPN&scYUnc@bl&f!dKt&k=20c4c-'
    b'aX!#odA=TCZG???#Zq91P>)gk;2wAU-'
    b'xq^kbj^%Lx5pLMEOlharXE?W6_#)=R=d&HQaUAlUATV6d7IMSG@Y-^!$qu=pc8&otiQH}k37xe}T@;C}MB>(n!i4=+tR_z-'
    b'FZyW+WqXd@(ek=tILO6hD=43C7uLG#&mCptt|D0)Ovu*S6+zDdR)#cdFFj3gOz>bI=P*tVJsFTndVo64IFYi@4KP>havtE-'
    b'fhQgN&px9W|5WhSiMccx-KGaAeWPB%=(nhKqc328BdtOEto8BtJvk2-)H-'
    b'dO6cnO?8{Ycd1w6YpF33P|aVbYJ8yis(jpVP3H8cy?N~uj*lM!k}_F2!%_BmtY75!omr|yhmpAtCa~XggjDiOwZ;uNl(%-'
    b'M=NzE!mp5d`}*s{vw=<t$XbSsU~EYzMhXj?&I*d;MiL=^id`lK5y#WJT@nHoTED0HXu%Gch8Smo?7&VubLDFWc_i-JnY7h+YanMC'
    b'=&?ooB5rP1Y6PG4M=&mAAz(=Ilr9(AH|@id)JTLa9K$`t@Mxu7G%2%CP*Vu~nu?t8Z-'
    b'}?u+!($NoT7vWES+NR#3};MvJC#xi>*Ww#Q`GhlG9$?eeaaM1<{Yf@1tb+*YcXN=HiS(Z#D$8{AIu+&bShoN%}A-'
    b'?T~J5#9Q<U;07}4T7?>;e7v~uO=<?@V<#JO-9y|!Is)0rU^4VU>b}R4Y~;-WXyUC{7!FuMrir)xiMF^WCM=E-'
    b'Gd7F+B{^q+G`Se#lwM*grT7}80yBx0@;rpn-0-'
    b'~&He+qZ64{p((nKG$W%?pB+_BcM6(fsZZ%kFO<ctp_Q7^3Vb9W&?qnMO3c|_=!fwYcvl%*Q59aB`H9dNPYzOSZVZUzR18=>L%rT8'
    b'FOV0>NKUkH|3F1O_$`6dHgY6PQZVZzCqfH+1inwGuW%TpiC)JN#IuX4o#$!b;%a>G@gdpBe*`p0Efplvp-'
    b'A0kI!I#j+81Uq2wKEp>7{*k=?*IJVQ=xIJOLLWi;M-'
    b'%>06n_Ni{hr43wR;=>xRKk|>VjJqNSA#zo<HR107L6HqVGkh3lY;Q+4I92@R`@*A!n1Y90>&xcUcF%KD{xoS7TL|{1I9M%;9zCmN'
    b'mjshi{qTqapqXwj}w81Oz!y+F(!&77`EA_KWI|b!H6aHsT-q7H`~Zc2j}?)$?83`Y5NqQt97JxT2~Vd56lhj<!fB8hsT-'
    b'(Yje(r!BNQX$tL;NdOZsS>w(q=yy#NOIyZd$Q$#rd7j!CN<&71>&#!u)v#=b$r|PMT4L0a-'
    b'X1}5b;mDmP`6AX<bc<e;accqC=QodBkI)k4$_d8PQdO%aioqG1aKFa>>s4(wgM6t@d+od3u9)mfiaR_Iw#>qNT^hG6|59UjuY+pO'
    b'@#P;y{6XJce{9zaN0b8uN^K%YJh(57T3?=;KQe2ns|<q#d#`YdCB(eMmBl@tI5lvrir+biLi5&M%@M;3%Bcp;Awkn>8v4B0a{`K{'
    b'}R*uO*nxuxc-ud-Z<InJT;Ds1TnspLxM%}H331yG9{vNfZj~ju0-'
    b'_@C?IJxhat>zuv3_yGZ%4Jj60BQ1BeRRB_+w2F0EvM&5=;l*2a97<iU+vnb*`1b=BKoROPrCodX6bSV)$wl^e2mhJXht_n(95@1|'
    b'R11PY!9p{D<?040Emzhhvb?7`TMtDO@wZghBB$RWy<Vu;=)`P5dy(F4ek&;f}Uq=<*wJpT3FZ{95y>=3v1A*Yo|R!k8w`CpVML|J'
    b'kjmahN>#x9{ngxO?TLdM_8g>`2#)1&3Jh+1!HTjdnx2cpbK$V^2}?#y7c+eV0qsUNYoTl-'
    b'ziLan8M3n+ZN+pz}t85ipBY7)XQgPWDhUor>Xb-hS?_6q8Rz<aEe&|Xk6!4RP8$}K~+8keu%*tD3mbsD)Nk7I2dxtuf+CWoBzgHP'
    b'nzybFm=#4$x7OP+!w{PR0gU|V9kZ2}ZTC6U+!$64lb0rS1_<<eS1`9>c40^|TsDuYB_KShE5i3~*q4n{X7;}m2NK&71<*Q1a<*v$'
    b'ZLg36$;GqcPmNp=ti-&QV2pRLIMug04Z!j+)|CGcis32KM2?sf6r<Pk(e?t;@iFs!xid{?irl4&y4kQi|Z@PL@-'
    b'fR<2fVD`xG;EoW^5E?Y$%w;rYmk;Io@t$wiH^8G*e6AfM+<~WW3mUDkUgmuZV!gCzM8t>%97Txk2q2Oa{_Un)$$3=blaV9Bv0SYq'
    b'Lzs<;k8s(tpndt13*dvGNB#|96~U?kpZXhO%n`82WC$NomKDkBSbAgy5e<O*sO3S8j<F-'
    b'g8m}b_7ZIGy`47_DQEdhMUHRjTE<P$ONE%Bm;~mf(YC1pwaf2cO1t8D^;?7>*qM}fAFMxN4lp0nDepT%OzIXHvxrbWMeuysI1@Yi'
    b'ca84+ljm$Z(6aWq2OR!(k5ew)<#6XspIFVcU)Uu=0MOqL%sguy=xSXSiy{|47#PfeV-'
    b'^o`?%<v!F97|?YcpLl$DRov@M~hQDd4xPsFv$SyS8aV1e(0=%?1VW)9#M{mcM2ES6g!=H0T%0UyI^8DlU%y$wkCqEy-'
    b'Q?B1!l0J4WJre9VO8*m%eyL5xXo2L0ka*>I>RpngTL}#FW^2{Zt!}U*Fj7sQphoI>OcfKe92R)DodP%hBNZqihG!QzpT>$jo=)1<'
    b'C+y6g6HXBAF55|Jn0Gerb{*Q3-}cD6fR0@_?<I2uNhX{dV>GqnR4P<O<<sw5KeAA!9s>R<wk($%7T3hQY{-'
    b'!Iq^7oH69gaQBaWIM?8<N0`~=D6^_?YFp@EJc1Cu0ON#7$mkoM7FJwyG~l9>DDz!f-'
    b'AZ}u`DEuKg`q=$+HeDEhy$`Bp1}1Ietn(96}7Ah`fVV4zZ**vePne2Ys5;1{fqW#@GH0~vJj(-'
    b'5=GPE1yaQZk$Me?M@ZwD)(fI|J(7``uDrvUyl@|?MH&q3M4m)#vL<H=ZpldKi~GRJR8R!T@~%+;Bpq?W%Zu3~PU>+X1RG>7y@Lcp'
    b'5%9X>82k$GZA`&H!;pOA+mgx($RLaGI@%lK0;Z5FC~4Re?9W>3YQVXXzj%TjFaz_DSz3Sdw`w&Y&2eD8z?Tn{pNUOt$l|EoBeZgv'
    b'a!90qiQ7OkZKfm%(Oi3avA6@nD(6CzLrq#+h(kEbOrTN-+L16ZL}x;-'
    b'w_{#mt&AxceCaib;4bp^2+bKspc~Ot&jtKDphKM2XNeYO*M9iKLg17ys-lwU{!?2#C6U>is?@-'
    b'Qgv3HA+5w=2KCLK@HlwL8R*A84YA~6GNkI3HP2xATkRR<NezaSLcDDI!EA#ybj?dfVz95O)5qO)t^^C67&=5o58FKURuEZG8{n|3'
    b'^7F}&(-Gn^E@$REl4CKfHsKc}BAz`P4e>T7T5I3Mi1Vn#hgCv1q$a}Q1p<ctSs{I;S){ub^8}e-'
    b'<<j7|xBO|ggFjs31{f**}IDC@u$ft$(Dq~3W0k<Frx(uxk*C4%BrZ$vw^THXxGuTLyVLs|BA+4zVQN)YPUrZ3M$QMkMfw%=2<jsl'
    b'8iEl<N&lU``=wm$3_bpF-R4edRRR<Hp_&qZikgc#ZcYzJ|vqXW_5Wr?^iOgk*!AsZ#zPIIOZ-zU5qbJP=%1(=9Oan$6U4$#bcs|v'
    b'r=aJ>uDn7OcV0_`cTNte05F@8RjwW*3i;pp<rpV{fK^7eAx#TT_l<!#4aL-;A@C7h}o3DfUs1%pnk9-'
    b'M*k45I2{D(Q3weslFw<DSgi(RWo<stz22Z=Q$cyIojsbC9(+O)_q&|46QYLfX^$l>rD1Q6CNNUk)gwyIh_AeOwx+Pq>PeCyB|mIO'
    b'_KWf6WKOdj%!SsGdq1i>)qstLx2!4gbVSmS6VJbYax&zDdY)~&gv8Ud=>FF0I+w%beLU$YjH6qTx$sL%(nf*J!y!s|6JbHUi%UY^'
    b'Wz6-'
    b'lH7(R5w}+npF1k_9I<_$VUktbqd!S}O8)jiS%N80QpF8KmfD_z^r>>KOH$X{bH~MMCHxXS9?H(1Nq`kfOx*n^SN?olrmFx~1qraI'
    b'CXzFLVhIGQFv$-'
    b'ubR0)i(MkAm~A&qBZh&#RP)FXQ%XdPykj8<1tHPWDu42HN%6=IxwAqP}+zMZm>6&{aqqkRkmOoLk}(3!Z{%cP$i~}gbOONi(Ddi$'
    b'40{>yyB4q9*E4>YktHG=*zy-Mq=^m{qVv>DpF{nJHTlC8>+rH%!p7Fh*3R3RN=tDaM!=B<7bBuxdC#c(dPo=qc&m&E;BJBppFwew'
    b'*bN10E|WW@?K0o$n>HgW~XoCr7;=AC#I<qEh>V^7>-'
    b'8N@t9M4kmxSJ^@`b6bqS6B_6QlC1)%qutYb_PB73+u6*+0$8$$*Z;d%+il+Z<JKJ*ks<f^Xug<lMK2oN1~4Fl{3k1c|Ch!>y~egV'
    b'O1@mx`<Xg{87bBWnX<TZ=`EoLr-'
    b'5&2pz1avwmt5S#{HVb;rg0@0Z%!NKK%v04~zpA{tRzH8?2ah2xp;6RpgMY_@0SZ!oaDAALu>sRlaPkREQV^Yff>uOvEpORil;vey'
    b'p*)@kI^h0f9vLvW($F^e$(VOoH)3!a{Fh?g8Y6X<ye2WW_4tF7w0Iv>YzJlMlA-%spaKxoh#sw7jAw0(WB~fQmLxvjXGl0C{4;--'
    b'5@FtAIEI+$2z4M*{sW%EJWR$Z2#gc?4MFZ94gRj|lZuEvJa~hjVL0r*;@laIw6y3Z%y-'
    b'}}$@5M;b|k`40ob9`?A_+tt&=_cIdkL~INiD-MA6WwQwcqsiTk=-F%*4*>0T9KCE@yu8^-'
    b'Wdlp(2t^Jd0T!XyM1KW6j?s&zn>OrKg`hKh5*P9!Mqg9LbmNvRB&b_HNHJbDX+1n{jf9;gBy42P)Ai6J&t1oJ3{_XAK$T0fqOxDX'
    b'Wif)pHmq6Gt(xU@t}6SfnYO}ui|R%z1m^jV9H1Eo`#E51u)_*y2Y@Z4RS30i9g>&8xHRq(CtGyv*5fgx<r21T&*+-'
    b'_^i%3G$~;P^BumJBx@C6_L9RYp*OqyaS~dDQeNfNb+R88rkIF5>C_GQ4&EEHjEqG^BUZav0h+W!^;l5vEP2rQLAM<^ovBCK!+C=V'
    b'_<?)$9kfdj~)fH=ua8aI_NO40!F@48(v3bRnTn5;3fxJfAzskv`#F1lI~3QV2-'
    b'F67dl%q{B=gNJsL8snzr%<RNe&*aad=?wq3Gd;1xPM6@dcbTmgrHtesKX55PQg3#SdD?U@(H%J%aN=QVEfvBpN`^^-'
    b'QqLjN}!<L^dbMa>?PT^G&I(v~03v8+CG71iLV-8epi)~B$b-'
    b'pJN`glBM@t_=m2Q4%rXi+05WHc<^e##U;r)Z=Lf(4$LiK=ho6LjC69Yelhg}_8KLT1D$*8HMrdAFjDQnYnd_n5Q+KnnJ|7J}XkHx'
    b'%$8N(E}#w15~G61<)0_G(2nfGkz!1BcJZYwMSf#IB9hcZIfURWLGMs?H&ZmFuuMre2#sIjaF{VM4Uol?tPklVeC^m~bucib<*%Ux'
    b'L14l%R4!5^_uB3-}!9^!O!-kY2D8A3~RP_!lpaAK(33TlUem`e}Wk6Ac-'
    b'h7z<EEt!Ze+4s+Gj$I?DDPr|Td@;tVF;AxOfyO%HCfKtT9tl|Yr5Vbnxu;Eu-'
    b'a`>a&g*}K^Futf)kXee_1WEE0FNc#y@rt2r<yDw404zw@f|k&o0XDiodn$bqV6YfL4oU<iO#Uef7-'
    b'XnQ%pgfZ&tU=FDi(367zG&snBJi^KMYJ?s)a0FdxhLQ0tz4N;(&T(V&Hwm(sYOyV!>XGQL$Glgai$*`h?KrCMyd3ApM>EZSPAN;K'
    b'0xz;d@3FwPBOt<&`iBSf(WXNxnc7Jnm4_WxzwOLFNOF{#It<4v>9NA>@?@R@5i(9SsrGm}#6Jo=Ey|HQqF5;setO*CWLJl}QTHjW'
    b'0uyxpe>rwB$X457dl`ubF$)6EIM<s{?-~B`<oj<!bMy+egWOU*F|`9S*1L%YY*_5$!eu_pIOprljVf-'
    b'Z|H<fqWmc)}MXk7yW!XP!QCilBA%Z*bXYAkhB9`_SQ}=Hpg%1A;k&v5DooezqSh0f8m#SO`ck<^PuNqzB2l)5QY=u0n}WScW7Gm;'
    b'4f5Ib6heB$kL|nZ-{rfqYM0UNn%Nr%8`61d3SW7X*smnM(5(rcTPfpY-?r!GSuG?2hg5)S?CSs<}yHlbM&hP<f|HE-'
    b'VuWXgDyU4+)c6p2g>|{mp}BYL3?anrC0@h*TIcWfFdJv*g!w=NE9TMJX{qo-dVFsPE~w7iRPaafQ(TU1ff4W(YVEc5#pgYsu~APu'
    b'CE?Z*2+rK3`^}Eq`ENe@onsu37iD&-'
    b'nu{`=#i8idL>E&qKKTud15!Uga)H9856*lYDKB+cR$>7%VJ|F3fC4)%V+}|ND`CRhB9xOW1RNAS2bv@h-'
    b'k13O7Y)Jk;Yfe+)k20F})ZvNvqVyRrAuq7`Bp?pnl(g+X&FGy68|ki25I-tK6j`Jes<s`GSg?Ktz<k)_?c2eK}n1-'
    b'NU&XP<F$!1rP>w<linzHKyA}zh_~PW{CeFe{k?wPeTMs;u0TDl)%vg0Mu;}@Y#@=zo$u{R8-'
    b'H)PS}`@!B`<Zdqe{mA9%Zi5r``0Wu_4Us{ZX*7p&24w|ol}@oF7u+$`sV)K~>~x8~KZO^#qh=M}YT=?n9TYnZ%ARy7OIN0R=jt$?'
    b'I|miBYVx?VV1qF4Vtz{n#WiC6S&M3v@I3B8J$<Dq5F-tsR5F<&6}F~ynxE~-'
    b'FN`NHffC`T2anE@>xW+2=96JEB_=ngFZ&`+X6MUvn;j5<4zjd+HpC-%OoI&z%Hk)Xiw-'
    b'^d^4SvnK=@wXW5slIJpTZBYls<2OiudzHsD-'
    b'j#!sMqQws8nwUvGetaLc{Ot3%?<5>If~&5%3?02apfktm~l0!#(+_P|4a|%5g3j$C_3f_lAl8Qj-AKYLEh>u{mn5g+yXAwbepy2-'
    b'k!lR8xULnt(;PfEW27?~eF+cZ4vdT?wm(LF^*l1U+1_I?Y^dxh}hjewZW)cbXFeMku>VY0h{nr2=$uF17~#I+H-'
    b'%XltAYmcGD_gDX$e1bPo@IQyu|1Qm$5Akbc*z-'
    b'f9H+Fq5oW9z4?U$W{c$8;w82%gXBU{SsZdHzwZjB&8==V0*1JS;qqaYmLl;%pFdd{RpZM_wkXR~$h$m1Ir-'
    b'X@&GmeZB?dC=hft3WwpSWoA2R%43$PYO=(KH*%t{fY2w09RGlpB(S&k@y<&ytuccDH-AJV5G%l>st)`qs|q^kfD8*yX(VFa%DfpC'
    b'SZL2P!`nNr6*@$;Jj~Yqtf5_=6EoV9Rxh5Cd@Bs9>WkaBAQJ}kwNse(k1H1nz>LAu#G;K0qu*57nzd0~)Z|T86}0r23zYy!AS-'
    b'<!TD7}b+qVn7q>c{b(IVorbYpnZ*{!TSRr>=frwnJbO}gV|Aty$r@JOeWi^Tm!G0qt%_NT-vE;N$%!nH=*M3O-'
    b'I8RItD8$#6DMG!R=6AYdhs{B?L-'
    b'=~?AkeLR0kP2M_RNJlUG1rDL8XkYhv{m&3ppRo~<oi}BxBV2w)&>U;+}j*G_pk}AwzP@l!?epI+PC;Lu`|xnFDWdHQ$~jFcUyfBy'
    b'oU+Q(mWovFVY|L)a1OMjg%{?4z~gG)o@T6F14}&)41DTGN_=GncbLTwA3szr;IHZELxpIi*X&qQP<id^br-'
    b'>yftLo=G)J}Kn1mlv@Q2m)$$2s@<oO~;c;;|xFl`6=@cgHYJp=Q7(Cee>w*5NU3h3iL_PjBjjEZ_#k6!4_+L|1lh%3%PQGZ90WiN'
    b'?TYYepDhPf#1-'
    b'K35vR09tSto7Uv|h0nASmGk=|yIK%G@tN#Z^OkRS#`py+w>5)?QGp`UAPdT@&nb9uPGRZtxu7rP5=lppel9Tn(Pj16kQm`nD%ApS'
    b'7Vvcm=Tz&#A<xSw2Y3-kCd{jfL<p+G4CjmV_5R&$@?-'
    b'N8Wx0C=teKViYSjF(s<`*$uMTz0XzeRZ*B}N{?FX2`{bTJO!?AWoAaEGIWD@U$Aq)AaZNeq9k=!EeQf3GPff#R>87FYB0umMY!Va'
    b'I%e|fC9YAHQ6SpO;yuu22hlIr%Iv8ZP<KfOqX$SRCQdKok9<L;k*rn%8AlNap~62!P}lETwJdVX6NuNelY{4E#31>lW;!7A-'
    b'GRokohxAmn!=h|u#3nE6sjZhxz4%dr8gBF5T-'
    b'l2@Esvq)hYEViZE4JeHHxhcNj8)dfGx@GqVSly<MAnS+&0vNCVs+>&1)t?=nf?vM_z1!BN<e6c7}6TX-'
    b'=TDyc`Oz+3@@#R>%}p{LJu0VZ$Z%&bs1Gzwx|of(AE!LznLOUBiKgn%C;gR^HEOb-rM!kO}a7GEh~;O>CAwXln!!ugPkL^h^gWwR'
    b'KPNk*YgUD^pmirJl@KPM2ZZ+8U&2Jkx5!>17xOLcEM$BM1qOLfF|XulYpT(yC$6KYUU_~@afr*BLDKjQF@`Zdv&+9iVZ&TU#YP=O'
    b'e9a!SJ~cWt+#yfQKw@q!g92L#6SYdd8lAU<AAx=nhM7&cWJ^1>}{rXWJ3Duw}Nw8b6p4q5OUP8;MoK!O@C<JEqAfMf$a0SNVrHr#'
    b'@NhJ0I91xOqxsCZY^G?Fx?lZX1%>Kn27E=uW`s!njB$)RYiUpVkjjx?fIZM~r2QP~^xht?;r(5G0&g8g0ZhU8N5U2+f`wXaeg9{8'
    b'w}=jf<2u>mUVXyp~7z4{<22mw70?y|n?#a?6X6HZ{B$;S?C?Ap+i;D25!+fOsq=N5pB&iEqj2mqCEwZE2Fpq9AWYPzYB$keK(YOG'
    b'Lh4E2519T^~9>PpG-kfJT-l9*a=>Hkq>Ah=1+LGeWQ!X!h-<OX&G#Kl6TqMGf~HwuiISSo^$lG9qsdlngwVJcEwL(*-'
    b'5RpefH>b)6efH!EvQerSp;{pVDQd6AwJofLUB7Ryc`C#J-YOcjl1?GvA(ULn@!Q>Fl+I_kVGjEj{pm|XpV7$LIw4g@So-'
    b'}+wTBFp`=@E&9XotX#_El98m{pF}p933!*s2;4m9GBAMuq?6NFbE8kseA=r3ksZRG$gp*9@Mu3*D5a%_Dr~g)&Z?K=gj&#uTqLAp'
    b'ZvOrru!H!cF`<7@R>Oq%)YfV7*ymRI+l>NbVCQ{?-'
    b'>`e6+2>M9x4ak;+pm!N88%W7Kkc7g@$Th_47v9CyC31#_HVpwRQDUI!iw<w3kLQ8jyT*bEY8pq;;cdIJbce9^=VSDYVXzSDag%23'
    b'=!RX((V(dHqvYJ?`>0&4aEHlQcSfEg@0kTX7PRka)u-'
    b'Wn5h{0Pt5JD)@KJ|%0|MICj3ePGJ5j35nfto59(b<(S)OSKT$yV6EX<fpOZ8kfU`0r6$up*F?s$jG6teniOBd1PqfiWnf3QDx3By'
    b'!#B1*xb?~2-'
    b'v$108gNTkW57oX=Sx!O;oo89guTD{R#eco+^&N0#DbLJJf(=&;pTR1X9adFX!RV4@2wV8#}Zs^iIMPiJ_v>Gy=b;F&O`7@JvhW<f'
    b'n917;RyjGHMC%9~b$q_G!1y#fgG+Nd(MVc?GRhzFNzGDXd^ngBZBPgT>33g{2c)h^vb^)EY24b4z_kosV=-'
    b';Xk}l<L=Vx4C%tG4x({a8%{Q<g!pM)Jx6=Ns_#f<!BnK~Ws3;ju_;=A#Wkwfc030=kgE~Nfp}1duB4Tgz>mNrf)DsEC>~LDwTSa$'
    b'O}x7{*5j$DXMi(f5;jlBB@q$@2d}L}YyzX7vGqL~${!BYhT7l0CT=9UCr}S$*Sgb9s;pAUsC6v#RskPZAj80Q+y>8)C2rB_{oVBl'
    b'Ds%valKS!rMvx57=Q%0^)=ryYKR^@#8RCvhI^woNt}h0wyw!&vRmr<ne`ZvVq$(zGkS%FfDxsD_+bZG}HtN(g)5<{5j_g``eIWf^'
    b'=nYWT!8E81X2N_bbtSjR$gTZnh8_{gG#OXqahXjVZY$~!Ah_N>7&O3?W>AqMw?xzg297_}-'
    b'dTp)AQ4rdF9$wApBunJE5ebZF3PtYBPfkGl!^VSIv)qYFd9G{2q#hv*VL2uzMBe^R@b|L9Aph%W4^^93^39XaB7l$ct{O7d_^!r;'
    b'|uQ7Ru?`Ejm%)Fb`Xi@wMHWTEsdK27q4ctjhj>fQc#O0qm2cemw1NY<>;l;)E*ez@qz{OSJagHOHB-uPDpu<=41j$ER+IZp3(mKI'
    b'hCwDeL2c>M$w7KR-'
    b'X|(Hr{?s=0ZIgxC?Z5+N9l{>e96Fm?#xtU~08v7Y7<Msgr@>io~imF@IxY0oBOp!I)W<%{h}ua)CeuTwpR_I>{BbP&@;8WP<iAXE'
    b'Db8JtVb5hG(M`mrgpel=&=A&Fpur!wVWz{@~?kb6TrN4!5X)c&0zGf7GufS`H=0ZpxPAWC32a7xmail}evXK102#%3A7YsM;#_^L'
    b'8CG_52C31TKNf+D=6oqGK8vsW#CCSv9qKs3s0+91EcaCc_)S-'
    b'cu^c9&Vm>KB^8=g;j_YupRToh%k$cV*of20P$8d5Z|6x#dkeu0pweGt)9$hrwM#$sy$H|4#sNafviGkb@V6*p!#?1Q=58#XFXF|r'
    b'mpgB!PQmspjw-_in;)_C^Z;dOur)uCnJ)s%6ef*fO`3e+F8+Fjq0-'
    b'BntiPv6WAmIep#}U%tAEi1Rq8bNJ00v0^FQBRehqK<cRM?ckTVIURQ|{W?cC>)EA=OvWs~`+iwY6yePOb^1@I+(wHX2s3sP@d|$e'
    b'I%6*7;WEo021)c9DS-Apfk2rH}pb>PDpt_7zRqa^CY^ixR{FlYd6xAfI&b*@&QJlC@AeEqXXqeyCJ*Z_=?TN>$V*U)%4IN_eF0CS'
    b'Px>Z24K}9k}KBLP1@cfLR^Zrvc5!zwT+76R!j;C$MazO*HOfpm70>YAeyYm|BL4~9?fuv(HpVOUkQj}lZB#@@w?uL6>DZkz7+sM5'
    b'sodg<Pa=1Q?32H`&TAl*KvJfu-CxAMtm0{!GbsW>H(&JWj8IKTkc0>RovuACm;CyRTBVFJYwG(m)d2x<3Jp8=Xf0O5WYiNs(;OGf'
    b'$x1|?^SO{$;c~vo*N~RO4BdSu0S5@UafLx_#<J*%cTOiHp>Dia9SaCE4h&T|zzzcex8&y(_zXlAkekc_!wb#9n&fj*AE-aL)zSOB'
    b'V8_5USt3Cl4tX=yAYUvzpP?MQ5Z4woPnCkI~|N7PneALO0nL$zm6&U3z+HYu8weADicr^6NK!@;B>IhTkW9*1!8Frm8^o~tH8KL$'
    b'dH)5`8feU$y-ZR}g--96<WyFibu%YF*V|~D-xOL3-'
    b'Yv*xGI>j4)#JxGzu;j9)&Me=(tDX$O%o{P@L&{6WRDIS+nX0gOK{U0YQx1y^lg{c)s4~|H3pyr&%v6PIQd0mE0XhRR2#OR{mxa!G'
    b'Pk^{#7wyOz=oVr$lqZ~{PQ1Z0b?(~$UvR5v3mLcZw5zFax2^Mz4R^h2D?$=!B~R^>(8x|Y8b;+fB{NV1piv3LHZ@wwcA{*rwDWtA'
    b'MAC6)6+|WsLOvwVvoHDV6JX>lYbgnIUKUmEO2}#5sA6!>^gj^&Xc<WF>e?fk1V6cN<U2qG)o7WyX#=lhV!a2Qd)QpfBWI$mw`w-'
    b'uCJi+C6BjbGa1uGi)8Lk1d&{>zhyE~4LzN0D+RZw;O`D__`LO=9ALDnCXy|zB>N`A3jd`lFH|@CZr!o=QjQGM_Hf$$S1v?W==eoQ'
    b'{C<ZMTw5`ril@m^I$|1+YWvgmdfpo;tLIHqjhRVUWnyZ=|T6=|w3Q>_6rJJY+&Zt?(E&wVjX~=Tt<U4+F2c7t#e8+oXXviJ^tE0d'
    b'q6G@S1Xetmb8x9cTk(k=ND>@G+Kdbq`S8IW*cLIAiH0600dWY%=0vZU1i+t8``FcrP2@>zB{F;h@sLwPq>p(vc#=fhO>u;sh1f8+'
    b'Xj!)2*R^tPJ@KY^$k-0OdQ*FEESR2e*j#)qnYJ#Z<uP$bSnzVmvatK5&k#>d}T$5V$)BsoTJL;BIQK423<VzsusGaWlE-pwNk>da'
    b'^1m$AAY4|*Cc$KRh1qM~84s`}?>t|98Mq|>H9Ph%54%tW5tG2%44IJRYw&PYI7!=3}F+^>Ir!duNC?U>sqPo|*ub<LF0x9X}2%>X'
    b'6XRRUz2pXh$N5obgmhRkPJxMbD(TN&V=Sz^hM{kPA)LgYXhW>7?aA|P{S&JIyOCS*_t@W0iby8U)!Cb9Ld@{b5fzVZ&Ks=sj;}@c'
    b'xjr@u#m?rSA>QI@%t2KzB&NQ@7o9f^z>U(_E)>Dwk^j(Bd(@LFU4A0aV(1W~G!<~AgYI%P00RTcIaFe4Bu>LLHFsHBvZUTaeTCgu'
    b'dlH5^f+J?!5hZ<!5Q4BkenxFv<*ET=$_uXYxQ|7KDK}hX6zJ=`2wnf*;7Os`0G)_W~4l)nQLjmesg{ck!9V7ki*@r}^D*IFwmX|8'
    b'v5u{m-;kA-%uKo%q^l&-)-'
    b'G*jlMg>m{$3K)SZ);;y`@&{8)w8J+Acli7SY8z~sWwIJkrij>=nJB|0()36o^r%LyqT)4M@8bv5D8iWA||E|3sHf3;NxoVMH3Y=R'
    b'x9)RB@n{uIcn#x0OFei)-pi}IB9nmueRkHwALHbK2Hav_6~IHwyD}s>l^UF)xOt&o$;-'
    b'In{N71i#sviU@$5wNH!sNvJPtV)zmFwY9}~a-jX6Fq;<fIVC+?*atnLu*nALub^*qy+9KZ*5iHn1%t6U&a&#0B-'
    b'|p(d&}Lw_^;W#-'
    b';52Xn+9L{`s0gYyIlFH)76T!vtqOM+bs4Oki?+t^s7LbjJ^57v2u6j~;UeO*>aY_X#;jAoprnb*EpAIaE@~hpX~l~{>kjsceUtKl'
    b'CzTUAJ)(e}c<19fNCZ&a$U>E9=8Lcd{DJKdcIJ72%>LG;!@Cz~QZ2#IfdVmxf|<utF`Kv-'
    b'6{U?nm4;otv%n{07<8;_LSp@u@k}`e*ch)3Q+d$bWt_@THMgpjL87hx)PgWbM0e9^v;$N=rTy^cRHa?xt~wV5tK?eE1s{f*4iBun'
    b'wOyq({^ECpx%S9yBHz@~{I>69OdROIpmHrHGOK6^c2bv9d&<gG=#U<i7ZYW~VOE_b_hHEYesU+Mr4HBTs+g*zLwuHgK~@#-'
    b'0|yJpylQY@%!3LX_tmCF_O-'
    b'^xzp;c`+iHs`Q@_QtkqUR}$6$ggxQF%#$Uzh*PpsYqRbrs+A{oe);(QIXwjQ58MmLD=q5&X)s;%$x6#i9obmM>0N+^=0mE3snl0&'
    b'^z{e|?WX)JRUOcz#4eNhvshYrs=n63})HwPTRRVy`CGv$pgej0(mwcpcVl2tRT<JYjSQ%x~yt>wLzKqB9yMhY-'
    b'yo&1ymkbY@D6_GmD^Hri+I)D|{E!uZ0C5NR>l%|SBVx-EMA@*<yOmdRxS1;jq{425XvgTHPpc`QArC(Djs_xw?Mju_)0TLTT5bOh'
    b'UiNW^M6{yXh^6o&Z=dY>yA<H`?z{#t&f_MfUfe6moc}hd%T~AY)`F^?z^L!R`-'
    b'yd?}`6l>1b$BD(aMj${RkEmqynyM_35srAb)!7kzB-wV=|s3;`+jtXScVBr?QZ1N((;WKIEfIL;-nE(W{*J~>M3+2kPZ`Klt}P)-'
    b'X5W-'
    b'bCcGy!E@8vT!=r>SycvSVs41&h8h_>R8RvwqN*kRnj7++<a}4Jhp<;G8Y*YPDOl6)fI;fO5=4H1?*n@G0Rq@<o!70vj}Gk}?+!H5'
    b'TSaQfl7z=iGc?SXKij%PRl<N*=U<Tzg_qBZ0GK3|4$kcZSp0h34=;tt(TO$qXbjz2+B{TaqiRKqwq=ooyxtVV6qVwlG58RoC9jvm'
    b'W7c^vpiv51z93+r`y_9R0~=%@*3wn^c#0}|(iVE@RK<vf`)d~liBxy#3z7oOYtrv!@g7~L(nYQQbz!njya04i{^tVwpaTEg{`RM^'
    b'YnX8&*t>Q-j}8~E@=&C=e$XWow;OOkGNuB|o`gsj^H{cbr45YJX5MBtw3DDi@>FnzE#f-'
    b'JF68GuSaO|Bsl$2e)i1}CDBpmxt#5Hi24bY3hsqn*vt}*2IXX-ys!3bFqob<Nsp34sr3(&;GNkcaUtClh7rXY}qmI}=N99)G%IvC'
    b'|Q3u+!@SIOLwFw9WR_(zJ_2lzBZ-->6au!QRn`-g;Y7tZmPC7VDy$k0#3G}p}dIoKcM4ih-'
    b'N)5bc|CW5Kz^v$;PaPqsMVN)w4(g9eGi%L3tEO_+1X$K`Q@v`wK{7;@kG_`y(=;4wa|6bfgwP?@#HqZ-'
    b'Brd!9bqTx2<bi7P*NK5XSjWF@^)b*#Fgp)Db-tDKG*&QZdmeJ>V(o$G)J7hWj=tGCF^lvrBmdQj?xjLtPyi3#xB~9=CY?N()y)X3'
    b'KzTZ@N76hlHCUhnnK`Wf`m5PjY1chVwPRDoXLGCQb(8b@8MfP3Q`fOs*NRY>LnUqr9$p6Jyj81bV_~%3sdHY{cMV&GUbOyD%_Jea'
    b'%4w%+ymibD_6&1ey9z_1y-'
    b'M_>q9UE)i>7E=Ngx`un8?WLN91(!tWL);=y|qXwEU5|o6hqFL3GY?euwy~rcJ%=s?LEuluQmlM0ag3x@?-'
    b'tTObe}kT)0+J6eH6z@n?(lZtpoV2uGKQgpbdPL=^i4?H*{&!EF2v{%tozY2WSqRm)t1xW3;G>!zBYF8HiVG+BI_3m)%Q)k?DkcW1'
    b'%!7Ip=*;6kiQ_vegjSiYW@@-'
    b'fKkWs&GfYQe@;Vh74U{1$4fF9cOz&G%S3uPRbWF)sXn3m40ea8l`p;MyO1jMWD2_badGvEh@x;n_gUjI>dslwX5X2q<ZpuNezpA>'
    b'{`Kvng3PxbG3;JT=(khB(kdKx;;LZ@3b?Z##SA5ymhK?x{$>;00>K?&ypb|^6)gXn=E9r_nmaFHyuR&`1hs11mys6xg8NPI<`HD|'
    b'a`%c7W;vML!m=rPp=Bz>ekMuuZ+g@WnVHj9~#u|t>b_mB;>nCq-DrsHY)c=~Ax9$=vA=%d1G$StbXLFYRNYw(VUf2iJLep8cgX|b'
    b'KZ*M`&FI;6j=8UrzORhkFRkaAE)Bsbd1Pc^nq7uHtHdq}Dco$XiELz<f)406G9jt0j7Q&~TIGoN;>J-'
    b'2#3hnDEqQCsONOw^dRH*=0|GZkcjyHg5eOznH<ut$GZjk}KD(i(7%>cC5?GlQ(&Q{zYt^mI3!IlS-'
    b'94$VPVT7fV%`7XtIkOFUwyQQtYeGrR0#5R7rU7_w4m7QPJuTN?1Bs@U$sZC8k`LT888246bHDD1jn&>-FS52Ac-'
    b'R8RfoX?XOM`DVMBbrs$nsuUBnVNlVYc-wOs$Nq=im5#2E^OCZY>(YX^QpoUM5$Z}yJ1|isPM+ga@DQth+Pco<Pt=qjver;P2%-'
    b'N@x|`wkj2Q$fkj32BRbMuvZLq{ha7AXI;|bG3-e5!`34}U+TyLS<F?w?Q&k<33eeHn?>Y{KI4qF8_6?)dfQlQFbGcP@-'
    b'Vo9Rb^X@t8*!jI6U>9k&{ce^(vFUa>g0&K{spo^@`2LV(3E8-'
    b')!MG*>2HXmHoJqGKxQhr0ktHqF~WTmfEhd2WX8f#PXJmI;uTIV{9k$<OjOafe&%Rn1^|szle&dq1qPC7a{Xe&B<Qr9=sMxDAakw|'
    b'TsiobaBDFbW|m{oZV&Is{g!H(NKizQMU|={49F?m57v$h+1iI~WxRzm@VgFpuXi!Q_?)SqK1Czy7XT4?$Muu7;Qau@986ja)>c9C'
    b')gIg12lE^x18OeFeCoGecvQVj)2UD@oljgA-B^fj?M$hzLp^K$6vz1cyR1_Aj>fzP6vn_KTGT@znT72)@=Z<p;2wVSY9gZYX-'
    b'`!MmiItMt?xEflq8;m59F?Tja^7l)%58%TGjUlWb<c^?}K)j@uebYnC#_nb!tfw>xjcql#WN;@-'
    b'oRuBWAgSLYR@cq&16H2X2KUhI)kFGo_S~z<O7!3o*<;=*;Y?0q)?Zjx08tdORQ#tC<Jpk+4enuKAu+^wH{d9D__IxRF~5EfsGDZD'
    b'}KcKpGu_0uJirXzk&EUOE}2YXuB=iSOz)qm;96DXw7{Len-'
    b'%B$2XyulT6bR|m5rPaz(y`*~5<oa%EbcB%i>ZAq17l`aQ02^Afu>oPnU8yJzw+(0R(fzp9fXFf+zE~QNU`zZsB$&jqBww4+NeI^L'
    b'@P94wyni1Jsd)POtHjD_?Nv=rJ09v%a0|B(zG=cjGWWtjq$3X}aYnT;+5}m)38u4Jgj&@w?{npPS>$u|fw|7_7c!3bciHbrylp@C'
    b'wbzX;G(?b$0Fi+8$h2%PTxt7|}TX@S&p-'
    b'G+Ni~ZnLw4;Pg(}5Eg!9dvQupm{>tL)HGhWgzOs9R<+ZFMgGl0j89MeWMk?9qXEz$T&RI`HX6xO;|l7Jsd3-'
    b'lT2^pp`sSgHCy2D`~H<sqn4>`baYvg7lE`c#Le!2t)80i4ycvwM*Mlur6YC_rD^>#M{~vANOe>#i#H*Ot#_>vsLsvZo8hUW_O(>?'
    b'<$kjffew0e}Be`uO^+JkXzEEW5f=UScl8Q!dLZT=o+;PL=g_8JhkDzo_EkmO|K6hj~~FpG1U>{^lUsLh@X;g{kS&LSU>(+qMF7Lc'
    b'+xe+w0j=j0#Da*m|Bg}Vh4n|m@Z<>9^<KPH&b_JB8zyPS#;QYlkkGXLq9KTP8~n6O&jOWnLMs8PZ-'
    b'd1&~^iw29Oy4JkL*M02oYFtOuPH-rvGt;|n_VB3`wo_SCiOF~=So2YprirWF<Stf^CXKgSE{fcT={nL(od)e7(pv?g3B`H_M=`IZ'
    b'zPTJTrXdOj(uZx0M2%H~xS(9(e`{SPRfvb-'
    b'74MpKIv#WhngA={T$2S_k2@!^4sDhR;fqbN$A2=V=23Lvh2MNRcnuHU0*<N0MARZgMfbYPW^VX@k>+5!m_TWXa9BBshr@?XIfet5'
    b'Qpet>eH-'
    b'c2|gVN>;Uq?is22o4%e2m2iIJKP9MJ&ieOyuI@Tw0=v@)qaTJuUo%LfVM`*4PvOOzvlkqj9wL1Vt$Dm=8S77z+ai9qh8^AwU9BWz'
    b'~gk)p$Gj4FP8ulkYGdQbXX}kd4=?xkE-tT{KuN0?bIP%TEir%bnbA{iK{TZB2}w|W!-'
    b'&r)(?upb%dDCr><4&SU>H@pKX*|&qJpQVc>O!W7UDcNr;Lb2LUf?1P+xT(JvCAl64fQ7GvJVC)q+V*oJ!(v%R&t4U<HjcKlS6b)9'
    b'i$I?iwyx&r7_NZ^&o`EP#@2HYGcAf{AxfX)HNv^Cxq&IOfrvzA0bh86Ncy(2dnf~#Z8yuoVkRt}H&Y%^e4kTOTB*9D*jdAhn;PPP'
    b'oPK+zy7e;+3pNIXK>nLxSUE-pL;W?JDEQR{Sg^&M){XiSp7>%Wc)+zL?q92GF0Qs=58x!_a5*7-mGf2}k*cm'
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
    candidate = change_base  # noqa: F405
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
