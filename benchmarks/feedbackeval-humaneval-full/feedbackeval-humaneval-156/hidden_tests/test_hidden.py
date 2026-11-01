import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[19],
 [152],
 [251],
 [426],
 [500],
 [1],
 [4],
 [43],
 [90],
 [94],
 [532],
 [900],
 [994],
 [1000],
 [111],
 [888],
 [2],
 [10],
 [39],
 [100],
 [399],
 [871],
 [3],
 [5],
 [37],
 [1],
 [870],
 [38],
 [889],
 [400],
 [4],
 [872],
 [110],
 [6],
 [8],
 [7],
 [101],
 [109],
 [40],
 [36],
 [41],
 [35],
 [102],
 [34],
 [112],
 [113],
 [114],
 [9],
 [873],
 [874],
 [33],
 [891],
 [103],
 [42],
 [108],
 [868],
 [11],
 [869],
 [99],
 [22],
 [51],
 [43],
 [887],
 [52],
 [890],
 [63],
 [12],
 [62],
 [55],
 [54],
 [14],
 [21],
 [45],
 [107],
 [13],
 [20],
 [398],
 [106],
 [98],
 [53],
 [23],
 [115],
 [105],
 [44],
 [56],
 [32],
 [104],
 [97],
 [19],
 [57],
 [892],
 [31],
 [397],
 [886],
 [875],
 [90],
 [64],
 [30],
 [26],
 [50],
 [96],
 [91],
 [46],
 [867],
 [885],
 [866],
 [18],
 [89],
 [88],
 [883],
 [15],
 [884],
 [29],
 [276],
 [388],
 [877],
 [935],
 [999],
 [864],
 [923],
 [603],
 [843],
 [936],
 [934],
 [865],
 [878],
 [937],
 [389],
 [933],
 [876],
 [95],
 [94],
 [932],
 [998],
 [924],
 [997],
 [938],
 [386],
 [925],
 [385],
 [922],
 [387],
 [602],
 [842],
 [921],
 [275],
 [863],
 [840],
 [277],
 [931],
 [930],
 [844],
 [274],
 [927],
 [384],
 [928],
 [845],
 [841],
 [27],
 [996],
 [926],
 [28],
 [604],
 [279],
 [601],
 [278],
 [273],
 [929],
 [272],
 [280],
 [281],
 [600],
 [271],
 [605],
 [1000],
 [93],
 [879],
 [24],
 [995],
 [383],
 [25],
 [839],
 [382],
 [606],
 [390],
 [599],
 [598],
 [939],
 [48],
 [391],
 [78],
 [392],
 [994],
 [992],
 [79],
 [76],
 [71],
 [862],
 [77],
 [861],
 [75],
 [80],
 [993],
 [70],
 [72],
 [61],
 [282],
 [81],
 [69],
 [73],
 [859],
 [74],
 [846],
 [393],
 [860],
 [920],
 [847],
 [858],
 [49],
 [82]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-pO-IkGJ|azsgil(`H_Gz@`BpjmH(0s@1z&J9qaRATjhc|7Z9J}%(1*<JOAmp1`KxE}{_|L0%+@o)e6PtX7T*Ps9X$G`sf-'
    b')AcI&p-Y)!&u4ph|NmMzVGQN#IXFFdv9E^_q;8Xa;=t~=a@IGR@Z6QZ;J8H|NZmt|NO__dQNeb6?d~7W42n8r4sD+T}Io!Pn>y-'
    b'a_@>a_PvsowOjX)V^6pIddxUC-'
    b'#NUGv2JMAPj0#7wa+cN$K3WhbF{UCH&4y%SWjNcDtGqk_t#@iA9I`aGHO2|<+`emv`5NT!fBzMo%wf<X32Wk)6WPySlG@OoBeu>?'
    b'P?=ct1a?AsXD)`F~zZsX)3M8;?Z*q!J<`fx6jk+IAhg2)_w;yH}g5l@^tD>z2;cjoNdK;O6{SXdeYz{&d9Ze(Yh5cZJfo2_#OS%W'
    b'9lkr-mq6&D<$Tnhn{BGyObDv9P<QzC*G0cZJuow^AK9CED2BB?@Fc9Z#+Ai=hbVg!FJfDg=V75NqvnqN4CrIwz`c)=2xklU5AzV>'
    b'oHEj)HTjz^rZ|Rv8F*4?b^G|dP@k&D?ddIwa7FVrY}%pR7vpOem$nyGP`-MnR9QeAM-j>>MXpkz30lI`wW-'
    b')kBz~_Vy*aH)pAX@zU9}_zKsvJJ-n?ksMS959Vu+pMvH5PWAWzR-DByL9}7<*>@)MSw{G10-'
    b'cTYd5&}ayb=@?A<$JeYn(0q=nBACnuI9&DEi>+TR<2{_cfoTzOhIiYoKfniMyapVXrESD82-'
    b'~wis`ECW|?8xTKQV)blTeQpp5D5tHe6m@Wtx%YSW7aJH66<cjwbXWaNA}QxfwDt(Sgo&-'
    b'7S*d+M(3z0hcbUSVaZmYHVREiD=<JB6D^FD!SNyv=GOwNbn?*p|xsHhJ>+TRfG$b6}Y_le<?aTa!Z_GT4yYOuhBKyaZOKS4yYUv?'
    b'%mnj|miK;Ds&IXSNSh*v6RiP=CE`wJiO!w@(%+?G=O5z%9i+3gUC#x5>P7oEB=}5hd?Z*B;$&q4%xM%uBL(?o{&f#gY~3g5TIo^R'
    b'Tz4`m(@eSvUR)9l21Z#<PymsI;}CgK^GrZ}k;R{!1;RJB>51g<p>;lV9Z-'
    b'*Xg^d7Y;q1LcMdwSoY%8#%hh%^_<$FA!>=~1PbU<{omVI3REs)(I)+s``q;Ho_im!=-'
    b'yZe>RgFe=(((scuTaq#kAHz4&Nz8a&6_2Xychn^6QpoIV}bnxoz5F(vGu5N~PxR#~CpTn-24n-'
    b'zm1lXQq(&pm~aooo>zv<tfF_wL@Etz|i8YcE_Q`I`57ms$x@k=Vpyd2b7c72z~XmXH7NdSxZ_Gfjda1@jAR$)r^epXnF{%G&`rPS'
    b'JHzPcA^pVXfQrwqLyb`MF}h8$8=^N{dy0J58Rt6rVE4DYJIKWtHry-'
    b'Qdqo@P{)vX`4swi`V3L+v1g_MG1}59q_$IrsCSPIYiK3CZ-eyaQOZupfzg_FoZ{GpqD!MPO=(e0hKgc2740gtD>G&xUF6}dn^?l8'
    b'2vB3H9g{+n@!xw(LOgNQbtCQ&s1#&<v``VS(`{U);GVa`M^(jEJZw?lH#4)+$37xsK&UAtDRPM{+K}$elkRbwba5Xi|6ZRucgmDv'
    b'h>-<f3yDvC(ucS-'
    b'W6JkXkXSGUdq5PL6IaK*?v|je_b~`7riIq@;ot(Q%L4J4`9YkP`2R9OxU(JVzrqo<F1mI~s>}Wsd{F6)xu<w`r@tqTW;lL#L>(vC'
    b'mk(-'
    b'JykRS$M{z(Jckfg$WBB!$h~Cg>zz9~h&dE$Mq6s8bl{O3GXO`winvWOTmhZ&acm@;rE;!~#wb2R*)KI;}h+M@g{c%(p*4h1L89jq'
    b'X|8TsVBQovxtnki_&CsDF!@1i=`Uje8aWbzF&^c)3bRaJr6wJn;TX6CPiD?P&{CA3ljuQ)92v%<gKDt0wKhx1g+^WG)yCC?uLn;~'
    b'75K^HoEFEqA){U*{hD)k4C&tMtYq5|Vr)OMtK6c=V9du<8k!C+gVQb;W_zns}%=&0&*1h)00)+rvETnq@B)1^)Ow|ZkgUi?pEf2l'
    b'e5qZ4OwrG6p7&Duf(Nny`f(!<+Tl}0Kj8-'
    b'tw>cy8M4O(|(R?PXp&+ZN~oSGw{nN|WOyzV(tkG0WAC`&%LBmM?9RaDKW98?5Y&JlrHKX`p=Z#e;NTKh0rsEYvSxqWy6D5you5|='
    b'Ci9ElRei1wa#nB`Y*8Wple57)AdL!GUHzSlY6>3NxQj2#Od6?08ce!Pa7te9ZGQ{E0wNK|eJFe>6{Qtb`n-'
    b'N52TyBH58l+n35BJR{L0DzYJjF>$N_|}bK8IE-'
    b'3h%V7~7z0Ux(q)E|CyVIVq$C<k#yi<Y8x!Dk;BRZ`eGJe&m`}<Wpf7_Fo|UM>2XqnctA@iWyzob9c2tP^ULKm?_~V)pSO5zd*^GV'
    b'Qnuf41{{E$vurPy{gbSpEHL=@xs6Pe<NL7P{-'
    b'?~8;u*$SOcRFRVZq#tY%ukuestRHYmQXaL3Y*50G1Id!>G1K5Z6E`6rN##A!ozw`6;X=wLK_cVOrvvIC?ZK9R+-'
    b'WGxH(GVufed6r|H+erWzVSW_iybEzx491`>dNa3Yu&SPv0e9I%No?D&~4nuqv~3Vc@ZuwCSGDCiLqq0-'
    b'1Kp?gp$1CKxnd~|FHT6SD@zjY%dn})jV3Ox`fQJGv1b-#HJhevV%c^gYtkA7~^n`F`|@>}+<6cySoy5L41U@09{NFy-'
    b'?31ni~HWOi&yyt_$zKJXdJ7A0#Rt)I_lPJU?Ga$V{KB_<YJ5icNV5lrFRD#Dv920RyJdl7U@MnqR{5-'
    b't1$CsfW7%PQ|luG)dimNEAGD<}nKO|{cOyk2c&h_NZ_c55pLZ|>FS}w2<<!*2)MF;_N1GunmBF~VYt(*6nRQ8ylU@9Nb-'
    b'g0AdoPMgOcoj@0qP`3j$HI#@jWFRpei%%-'
    b'@NvB78LD;o>vK)DB2|TK5)NZT_ae`kN_7WG1P3sLK_80Z;V}8L2Yq^@gx;RY#+ne80CYYXd!}6wKT49nm`@})gTeF%`in|BRR(Id'
    b'p3h~%UM<GpG0rD_cGi!Hnt>OFax(nn;}SG&@f$1=LxFkf?uW+UPj30N_%|hAS|ctjVAI>=S>?Eg-'
    b'F!jV2@1<o+}|n{x`>Whjs$(t5w!b$vt~r0SjNn9f{`xahpGv^hVP*j-'
    b'U?RPfOh2N49Ifcei&~Ap8?xfi%~m18_p$h)3KyH=pkS=azIq&;%+Fd=YfzCrziD97{(y(sOi<4#7Y)gwgW-hrJ;l=BWxD{qp>z`Z'
    b'`6uS$>gS_8cR(p6ykQz`KudfHN|s-'
    b'A|=Qh60be9FXG@5WJTvxN)1&~74r~SC^T$=5+?P$a{~e(nMCtNq9w1x^k`<Jzyw>`ufpvH9h6B5ESTdPV5mh@h_Ldm6mEN{?iva8'
    b't7b+*z=-q<?x8TFu=qq#7-O3AxIUnP#YB_4;+LoL-'
    b'Ey$FDNHOOh)ga^1vK(gU;@w%6-=TqHtHzkpuHoal;^kAaj-y~1xxAxRN%+f<84M`24qVGPdUnQa7q&Yg-zm?-'
    b'QB?ay>nwU0|<>=;SM~oqs;~Ipko*Vfp0+v1R?P)LxDmKLmkS9im>n86g_~zK<)4$U>LmNU{TDMhx0>mU0nY5My@3pP(F^dLsh(Sf'
    b'9r;cVAh^p!_u}C{K6KnGG3z{pBOODOqx<JP)P9pg>I<)JrvD8Fqsf>$5DVH=7;iIGZQTib4^@bb^wV0$vL46rk_XIi|pojioGi(O'
    b'AI`zk`Q4OO1cvLAT7c|AnwpPWzoN>fJRguO~Ig{X{mc1uWTXVNCe)BB{3S_V8P|sF|b}UIlM3;qC8DU)g_=xqQ{$(Suw%)Z2&nMg'
    b'{)k)d)NX}T%D=G`PyH!gBwqb8@kG(OF{}Of#@_Qx_)tf2GaNKOeeg^Oarxow9T6*riqE9lmZYX${`2TkZ{o0DFpK8J1DZH(c1hMr'
    b'ef+z4p`K^<3eedAXMp;$#4OmK?#woW&ob(al*kT>CQVV&|Fts+Wf3GQDIybjz74l$|egk4zwT%vcv`;2jk;~;<rVH)PP5gCxm;RI'
    b'$@nfGBXTmDr=0^)k6LW^s14oK;A~p5{5q6LK*4az``hdIc5y2@IRdl0Vr1q0I9`srwRL0Q(2N-'
    b'TOvG_cZyXUm`2K!F4Soimm+R}YL)*b`*gBtmlUE>1eb<36Pc=ZjIg3twtxjdj$}YYdBC5ShXji;LkIfWR5%NHsJ<*_)W+M|un%yE'
    b'ki5<y*{DpwWhLRcNv5M_Ll>5SS>V?o|4<}YKM(~Z6Bj{n0w*^5O|g<P&6Ww6%tXN`CrXX(-'
    b'9fvd>98J9bhUF{$OK?Jl0ab=S_cdJ^oG^bEHaxb9A<-Ma&!Pe1?SL1m4Rt9C>c=z<K=Ho;sU|fzRiW-'
    b'bk0CA(c3uT0OecGQ_HLz5#g0qj&|WuE8LIP;>{>z=vO;pFn#!Ziqu33t3wSe!X6}OL@jxw)F^nokOc-mdxPCFd6D(;kk@r4@4i|L'
    b'q9L@i80jA_zUl0vD$dm}Z&npTig~H5JpM&2g;t7dM*9GE-'
    b'p3q9JSHSg?{#1J)kW#HvfF0qP;+_^1lqtMt9i6Vx(MZ9D3kFWp6pHfI-XGkB?^Ke-'
    b'l|;!TmidPrnZQLO>CXj4#nY=9<%|I>F2kKk2YldptstcMby?n8#=8)d_`_DNs0(6C}FwrEE3Ssh7xAdeEi-60?NE9o-'
    b'9FO0e)Bqx>Sz21AbELE)i!&+85?a8iq$xKvQGPv46YQG%htp=P|vg>;;sC!%PAh71{0;V}rnR1Ri0#jKDJZ5t!}yoil*Cj1~yMiL'
    b'}!Jd!C#drc@Add>^t}+I)=-'
    b'a;FBEb^K3hnaGyjy5Uz8II)k1H7tO{h2Alz5<eOc0fqCi@IjVm&G45Vq$eJdPQ_lJ1$)qfO}P|A4goG`;a16oqJub!1Jtfq#=%{|'
    b'ZCErBtmq38@Y@Wj@DnGbSe_lYHdN3_fGu$%t`=mgs7wlYh>R5=oWgvVvwWu>yvSs2L&u|~oRLKC#L>XuVKn^0Hdzs@I64EQ(}^BQ'
    b'A%xxv^=$?ODp0df6kUS-'
    b'7v(>LZ6+UyO9XlxM5)@l=n3LRBf+Ldq(l(>s~cHC%SDF@N?=hZBWtRbjj&zuIPDZt)omn#p|%=mtrl4iJUxARip0uKp_jEsSUg)p'
    b'$4KI+;V2Ug+)(t^GSV-+I!gwvsZFSM`wo_(B!X29@*|RdW=WZKsROQaOuIExL0=Yha8W)HjapCKe-'
    b'}KAIQ|MKbWuVhMyn0NZ=Ui9P>-YBc63nMXgURs4m|97iR?7-E9ua1Mv>aHp-'
    b'P`P)ohz!T4{WyiM&IY*qW<B@Z#f0n}r`rLt*zVKLm%DMDfsTP>tk|UgO940;t|sNAg0W1qKMaI>Psywvfmwi+sPs6Bzvozrl$+tp'
    b'D7sH1U$(=`7ERO;8UNW|!X*LiUq?o3<*yGvA$^XhD=$29s+5EuDyvP8&w{-'
    b'_No1;x8=+`#1HoC}*l&?)yHb!WYo#)QK3{Fh^wysS+`kU}L7m`jT69`cettlr=UF>JYF&tM9nt>W~kYP4;Z7p%_?y-'
    b'(lv7(3NA`y8;!$w)olnz|x>eiSFYqzcJcD(x4>myE<lcm+}=L$m4w#%#Zd4F_E)NN)s0!psh9LqJ{4$ClnSu;qNq2S!)^G*s`{ni'
    b'Ex)VwwOMn#3^P;^dV;%wV1*7_&#PJYZpReHup#@$PTd3L?4NlGeK~!?W1t9ze3orCFTIFO5o>@-'
    b'3{KI%50MG1A0;!<!Emm@1m6>qRwb5;>yoJmlhqPqqu3?l)sQTwO0;*W-'
    b'%v)3ciL}g@N!46h~2NKZ$>C#|U*IsPZjDd62DtZ*#kh79&K5#}>h21(*0g7gNF<+=7}h_aqQt@1#T`FGxz$PRqBOMBVZe4u%{}B-'
    b'ySI#A$0nSSi{rn*w}X0HFzJQarpgK|>t=!+tF<q*HrzR1TU?`>7EzwT%?A0LU<<UO-mF|LRBvK1OMlj)uM++TMU%;w-'
    b'B|Qx>IlyfHTVp1(~3QpH^pw@Dzz1q$d28eRL-'
    b'=i9Jr{B6gibS_V^ovplGIzbm((lrj+h?fNBF3W^aG+GibX`+GmZJ3A@bR@?NgT{Cj{p1<P0gno56j!=93dOd>ga^&YQ(*+a1fbu?'
    b'XjX*0r>NZ+yJ5lGbj8CQ(R88YWWu!Tys!!yL=1?l60p811|xI|f}5cWO}m4Wd{52Hq6sA`FjSmo()qivc2pw*Ph~NLa=&dLFBdfe'
    b'dJgjeeWRLNn~;N%VReuisaj`2J0bvZ7g6!>AzPabZ=Tw$f7RB7_Ja8Y=(pg}&;zYZ<;mQ2!=={bIzn{>gCg7A9rOAQ2x<k7&>J9B'
    b'#$R+s)`P)U5Cy$lDe4Ipf$KG~&Rrwdo-NB-'
    b'>Un$Wrl<LDRTAC#PVGWRU7w)0Xa(BaItx$B6AwWIri@Rdr+}jR9W4E(TODv&ILZ}Z1F9uz#twB3cVHVGN&s~2*{I&P(dXnxUiz~3'
    b'RrCGY-GGKrTP6VqhdV<9h)AhU!;%%MR$rR|DC_PdV1U(Z5vlmk&+av@zW4;9hf?jLDGD9qPKjzGl%m@QcW~wLRxju`sB5x+Ooe`Z'
    b'-=<Og#0X$<?&#=Xg=kVj_nYas6HV0(0OD0mNaPM_NztX<3z+#N{fhRmiYUB9^A1@+bx+5d4##4n<FHaJl>SU;p>|BK9EIk5DLoU6'
    b'4xwP_h<>3~oeG4oq#dA5q}B7*wiJ^H6ySypEs!S71`2<NCr~ANhZTTD{YGujF$w~)4tI3D1*#?;wCU?mTL7Ix2$C45So5voq>BX!'
    b'{XDv-h5D4P+Ygl)LqZ5KASp9NL14pxi%#Bp#MR88vv-'
    b'QMUz%BSBy<lnozTnL(>XzgvvkuXK}mS<d{_kIAheN_t1hMFHwabog*CBAM5>N~UK9<#3%Y8XR~yU-sCKnUkMIHwhg@KKskU`Lgyc'
    b'h2W*r0HhIdyd^w6ff@;E#jl<nH>$D0WPqOU9cQoq^xwt>(YMgIzV$Kz3VYP8#0cF)gg;sl!c5#Y$^Hga#ns0P1M`a*GDXW&(J(TI'
    b'psbOQ>1z7RITi6mxSo2Z8#Cyrljic?nF4?y0rNbMZFQ+!aAqbntuAfBVp|58C1ixF*{6cu<(A`fYPz)>qyL%HNBbiDs;1MxQ@cTv'
    b'pNg^v}=&`x16BHYn&CjuRH9YI1y3NY$EO()mTa&Hym=ZH!=%FtN{hn2DG&JA@$&VnM+qF|`<PJ06yOm||QSUv4Nd_*w`+VDT0w7`'
    b'OpSe}U^5XI?h%1-BN!SI<#=F<ii%b;v8-'
    b'Trpk3;+TA96{Id76YozYvDT`ZS@PK@MP8{Xp@=hb4nr)8weyBZ+&;#u!BZjAtjk0L?=F%O^6ZvlX6{Ko0Q}Se1V^fI{B@xqmhXEw'
    b'eM09ONR-aL^1(U;49QS2*E)2{p{&RD_ax%97B$VH}9&`*F~oJ&S0=w+GHq)QMdutb8U`dIy5%{R=1U|jxFG0WicJa3QU>~o4)|<8'
    b'5=`%(!PZKuG=?z=_*jfnvxDXHX%xlO7Tch<Jc%zSDpsm-kw78#~rLGxo>uzD#83rtK9#oo}z$SMDoDX(B8HS=OBu`$14;#b|TPGs'
    b't}GY0Cc*P*j^?SY+0wlHKX1TGDJ&<CJE`h1Z%4NenF@m^zy(m+AbB#(CBz~9Tv+I&aN(mfy_GDL_5&EXOkA$X6nkfwF-NYmgtrXt'
    b'pj82MxC%^?cw7nO?PIDsH`25J#=HGVT;5>C7jo%(9N(Ad$AJrGRd~|DJ{~h>HZ^HPN5^>x?zS4CxA~EP%Pof6zn^w3Umvpu!9O~d'
    b'(qyiM+B-R<SZO!qZ|ky&ew4*77*w-p2A-%Z--;ju4AwzVBEZ?hPa;#4lLm!>XRV7(+`NML-'
    b'F}EQ5`7B`+YYTmccFPgVLBT9Uzri+p9zSWdI~{3cApuh-'
    b'+RtswT|?VcMKJ;d}>@rkG4~jt1h(_;(qE25qrZ$^7_pMdI1W$TZ8<>5eDeViD86u1O~$SizF6*mZ4M$4QbrIRT1Sd#Z~Gxjj3GwR'
    b'Hb&I5o3%K0Nw&GgB9L#59DIi9e}l0!ccPGl*7OhY*yfQRF(Nq1z}OG-%P#`^Nl%iSEHE7*!oEgiH}$*w^<8XgII++-'
    b'uWCXWyahp{)s8^R7%&p%&j=$f$)QBqzXGhgzlsS?~fvChJVP1%J{AOs7t)+3Y$)#Fl)0ryewO&?HQtr|L4yU^Z>e5-'
    b'HKH8@Kf4!1$)=m?c2$PN)EJfHvafJ1E-jW+^O2t+O(7d>psA2ylX|aIQv)n36c5{yecC=B5-'
    b'Nobm17Py!cB47!d*NFm(=>w)oYIF5#z?LuR+t5v2poKnE8(j|zF@0d$hJ{bUWxe+HM9Fl=%7$xz&LX=n*6HI9jltPz7d*k1<gV=G'
    b'+pKHoJjIBX1f1wW)fp^m;0);li@=gMA-d<PQ;KBtDkso0x73g;r_tX<fWq1&9L&x!fye-~||5AccmzSYaUJ%El-xf}f^XlFOWHo+'
    b'(_ROOF^r+1}ZFFhE845vL*S!#rq1@ewUA%+NUaM|FR3iIo`TpK($`JZZS3G^dfT0$L6v?Pqk@n3%YXC>>T*=){4*|RtKXl$=-'
    b'^Ce_xX&0mIN=mr*JdICPK+1fa=88IMlE1-'
    b'pDW?#Iq@bl;&AI5)EVeYCmQIE0o|#sN;;TFhOPv4bx;YDCON5gopi%a8~e{j+IOyrpz0($-'
    b'K9b<3lo4NQ3GZMI3dGSga{|Nhnk=knxjXpJMW!|#NW2_)4U6Nr#t6FW_k)|QrS~Z@mw1w#q)YDN@ad<sI8r6ozA?2!WfL|g^Fny#'
    b'IZ+Hj4TU#SeFRfpmmEY>q1Sa$5ui{dy8O7U;a+<p__PPT`Al;jUahes20~z2E`y0dRQ>R<|529M7xwMlB3(;@qR)viGPSV4cHwir'
    b'v3?Om=ie%b5AIAq4eQETfC5hIlcx55o7kZMb@I7!jG)ZtDB<OAps%h6eJxIb;vtt9yc&W8HIJ%#wS<-'
    b'?R+<0nEl+>m=KOO61I+&DzurG4!WM}-'
    b'&rSKI5EmPwB+>oL9xyx1bin#T`o#i#<qzHOsrFdyG~tgW%NzQN?kWaVI*LiflqvevOv4@hu16#zTI{7=NPS02F=LIVI`A)@;DkyS'
    b'1rmYbhoZ~rRR`{xVGYlkfxKC_}nU`LxF7@nub$N_Zf6YkjB`wIkZdkA(B^}RO0ttmnFVE3iKaf!7Ow&52~rUPnHxS8X3W~^;hd&X'
    b'=)R+>WT@ihRukIzD+4d?SgLW1br!j+9*r6%rH3}yF}W7*K(bf^1`%m(QRaeM)wwUedO(_Jo%FzbeEU4N>i8owywP}Pp<7{9Z5}6C'
    b'Mqqvq<m?y#EOD%-x&;14k5Uq5~SL|skH+dDHB3gmgpjKD4I^~x^9oU&Vw^B%bMr>rMutsU5}(Yp^V3LsSh9`GxINaf{se(K<&U9-'
    b'3;M<Aq{v~mm^preWT#^?+z_uMiuS-+<q+$bJl%V9okAM8vYM(U0p@MU_pMKi!3wtJ5T&%i+<5Q;d9b;8Xt-'
    b'M;A@#C&`wV?eFp)1hi7I?UH3h=ZYk?d!vXrg$J{(<ovcimn9Jw8H_)WE#EZUh!h$>vP46-'
    b'uz;?iQ(X_Qv*Sk`8$$ME8{E}qmxv>HuiZ<o=cv1r~CD6QyrbC#ozU5HXHr?Bs;q56V^JE<xOo9}nqQ&$T0oP_X0S|_4P$};y%z3^'
    b'7qPz5$05EiH_H7^f2?J%#I`^45?WC`hVfVUdjGZMW=Pm%Jd)4hfkW!Ps>uyA<`SZo6qCEnzLHB{Mapj??{05y&S(9!6)VK<1Ze(a'
    b'+4|^!l_y5~?VOkE|xgXADrC=ZJJ4Ho3RjeM0YL5EYyX*X3cL8*PA5{5VlQii3c}Xeb;kZZ!>UHIRBbd4+g)ClZjW~^mw}gCUW=)&'
    b'_NZj|e2;o|U0Q4=t)OFtw8gS4NmPVM`fJzIAf>Ol0wKuUV=!0$6l=J+2YU{@14p=VXcrbN=m1??+$q;qwCtJ{^nh6Z(dRQlHm#JO'
    b'l1F*i2;pspGsVyPg@kAyXBO-R-XQsD|VH57FZXQnE62YC0(8{z)^CjO+=jyv<uJ0d)pp#9wkN2qhk`%$FHVli<;pl@OR1{($SLl5'
    b'1esMnPDlCHL=1XTQd=8Zd^SbWS9=~Ved`Jv|u^qza1m8(k+Dp=o-'
    b'RI%D)E!arnX#auubxp>*hwS%_M<NhP<2QfTpaY(CGwHJ<%LnxIX?#k^j$YypSU_b4O=%+wzhwexSkS!wsi(=y7(QJgb*I4OZN!d_'
    b'jeU{C{E}rO^JfoNc+`%9czmqF-'
    b'j`ib+X_}V>l@gsY8W{O68wx$^$4Ti=ccLA`{GaXpPrmaw*cPd)RTt<+}QLvSHgidk+~TKlL4+%u0BV{b`_yB?L(-p-'
    b'@}U{pwyD$cEY!UE|6b-'
    b'dI=XHc+S4A86Az2d9n?@!8q(fZ6NPxu|xA2YRXsx<hvvb>x*jSwnYe(4?^c?fVUkxkV~w03(r5UMr#dKxNO@d8F-'
    b'K8zxS8+*oHYYT0z~p{w{`Yw8Gu$ct25tI8d)M{T5@s)I8knd@kop{h%CISI?%k(pcJXRBk0p>QdRsgg@!C90O-'
    b'ZKO4#ILxkV##Kd2Ns`csgHXUmPhiE_KQ6|VKw$D4JtLE(pM+VlJeNdLS=#c~H+LKA1{2mz)!_1K_3>Td<|8NLUb+pCRKMGF6wzGH'
    b'RUZqF&)pN9d!pzq7s!KP`g~pNZOw>7BG3%Gi}!UKr39RoNDkYg(xvO@4h=3BsMfYh!~?XahHg()@%fMc1Lbg-A^'
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
    candidate = int_to_mini_roman  # noqa: F405
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
