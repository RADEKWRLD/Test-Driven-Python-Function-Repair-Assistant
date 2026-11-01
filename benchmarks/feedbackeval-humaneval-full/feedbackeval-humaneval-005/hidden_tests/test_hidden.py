import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[[], 7],
 [[5, 6, 3, 2], 8],
 [[2, 2, 2], 2],
 [[1, 2, 3], 0],
 [[2, 4, 6, 8], 1],
 [[9, 9, 9, 9, 9, 9], 7],
 [[10], 5],
 [[5, 7], 2],
 [[1, 3, 5, 7], 4],
 [[2, 3], 1],
 [[5, 10, 15], 0],
 [[0, 0, 0], 7],
 [[1, 9, 5, 6], 3],
 [[2, 3], 0],
 [[0, 0, 0], 8],
 [[1, 2, 3, 2], 0],
 [[7], 2],
 [[3], 1],
 [[5, 7], 3],
 [[5, 7], 5],
 [[], 2],
 [[9, 9, 9, 9, 9, 9, 9], 7],
 [[5, 7], 15],
 [[3], 0],
 [[1, 9, 5, 6, 5], 3],
 [[2, 2], 1],
 [[0, 0, 0, -1], 7],
 [[7, 9], 15],
 [[2, 3, 2, -46], 0],
 [[], 1],
 [[3], 7],
 [[1, 1, 1, 1, 1, 1], 0],
 [[-2, 5, 10, -5, 2], -8],
 [[3, 6, 2, 5, 1, 9], 0],
 [[7, 3, 6, 8, 4, 2, 1], -1],
 [[4, 1, 2, 3], 4],
 [[1, 2, 3, 4], 4],
 [[4], 4],
 [[-1, -2, -3], -4],
 [[1, 2, 3, 4], 10000],
 [[], 8],
 [[3, 4], 10000],
 [[3, 4], -8],
 [[3, 6, 2, 5, 1, 9], 1],
 [[-2, 5, 10, -5, 2], -7],
 [[3, 6, 2, 3, 5, 1], -1],
 [[1, 1, 1, 1, 1, 1], -5],
 [[4], -5],
 [[1, 3, 4], 10000],
 [[2, 3, 4], 10000],
 [[-2, 3, 4], -8],
 [[-2, 5, 10, -5, 2, 5], 5],
 [[4, 4], -5],
 [[1, 3, 4, 1], 6],
 [[1, 2, 3, 4], 6],
 [[3, 6, 5, 1, 9], 0],
 [[-2, 2, 5, 10, -5, 2], -7],
 [[7, 1, 1, 1, 1, 1, 1], -5],
 [[3, 7, 5, 1, 9], 9],
 [[1, 2, 3, 4], 9],
 [[3, 2, 4], -8],
 [[2, 3, 4], 5],
 [[7, 1, 1, 1, 1, 1], -5],
 [[3, 7, 5, 6, 1, 9], 9],
 [[2, 3, 4], 10001],
 [[-2, 2, 4, 4], -8],
 [[4, 4], -4],
 [[7, 1, 1, 1, 1, 1, 1], -3],
 [[3, 3, 4], 5],
 [[3, 7, 2, 1, 9], 1],
 [[6, 3, 7, 5, 1, 9, 3], 7],
 [[1, 2, 3, 4], 9999],
 [[3, 7, 5, 7, 9], 9],
 [[6, 3, 7, 7, 1, 9, 3], 7],
 [[], -5],
 [[1, 1, 1, 1, 1, 1, 1], 10000],
 [[3, -4, 6, 5, 1, 9], 1],
 [[7, 3, 6, 8, 4, 2, 1], 10],
 [[-2, 7, 2, 1, 9], 2],
 [[5, 15, 63, 2, -2, 5, 9, 100, 5, -9], 8],
 [[1, 2, 4, 4], 6],
 [[3, 4], -5],
 [[3, 6, 5, 1, 9, 6, 1], 0],
 [[7, 1, 1, 1, 1, 1, 7], -5],
 [[1, 1, 1, 1, 1, 1], -6],
 [[7, 1, 1, 1, 1, 1, 1], -4],
 [[-2, 7, 2, 1, -1], 2],
 [[3, 6, 5, 1, 9, 6, 1], 10001],
 [[-4, -4, 6, 5, 1, 9], 1],
 [[-6, 4], 4],
 [[-4, -4, 6, 5, 1, 9], 2],
 [[3, 63, 3], 10000],
 [[3, 63, 3, 3], 10000],
 [[4], 63],
 [[3, 6, 5, 1, 9, 1], 0],
 [[4, 1, 2, 3, 2], 2],
 [[-2, 2, 4, 4], -7],
 [[7, 3, 6, 8, 4, 2, 2], 10],
 [[5, 15, 63, 2, -2, 5, 9, 100, 5, -9, 100], 8],
 [[15, 63, 2, -2, 5, -93, 100, 5, -9], 9],
 [[7, 1, 1, 1, 1, 2], -4],
 [[4, 4, 4], -5],
 [[], 4],
 [[4], 8],
 [[9, 3], 6],
 [[5, 5], 5],
 [[1, 1, 2, 2, 3, 3], 4],
 [[2, 3, 3, 2], 3],
 [[], 0],
 [[5], 2],
 [[2, 3, 4], 1],
 [[5, 6, 7, 8], 5],
 [[1, 2, 4, 4], 3],
 [[1, 2, 3, 4, 1], 0],
 [[1, 2, 4, 4], 2],
 [[7, 3, 6, 8, 4, 2, 1, 3], -1],
 [[4, 1, 1, 2, 3], 4],
 [[3, 6, 2, 5, 1], 0],
 [[-1, 1, -2, -3], -3],
 [[1, 2, 3], 4],
 [[4, 1, 2, 3, 3], 7],
 [[10, -2, 5, 10, -5, 2, 10], -8],
 [[1, 1, 1, 1, 1], 0],
 [[4, 4], 4],
 [[4, 1, 2, 3], 6],
 [[1, 1, 4, 4], -2],
 [[4, 1, 2, 3, 3, 4], 3],
 [[-1, -2, -3], 2],
 [[4, 1, 2, 3, 3, 4], 10000],
 [[3, 1, 2, 3, 4], 10000],
 [[3, 4, 4, 4], 3],
 [[-1, -2, -3, -3], 2],
 [[3, 2, 3, 4], 10000],
 [[-48, 4, 1, 2, 3], 3],
 [[3, -8, 3, 4], -48],
 [[4, 1, 2, 3, 3, -5], 10000],
 [[-22, 1, 2, 18], 5],
 [[7, 3, 6, 8, 4, 2, 1, 3, 4], -1],
 [[1, 2, 4], -1],
 [[4], 9],
 [[1, 2, 4, 4, 1], 2],
 [[1, 2, 4], 0],
 [[4, 4, 4], 4],
 [[1, 2], 0],
 [[1, 1, 2, 3], 0],
 [[3, -8, 4, 4], -48],
 [[2, 3, 4], 4],
 [[3, 2, 3, 4, 3], 19],
 [[10, -2, 5, 10, -5, 2, 10], -9],
 [[-1, 1, -2, -2, -3], 10000],
 [[-22, 1, 2, 18, 1], 5],
 [[3, -8, 3, 4, -8], -48],
 [[-22, 1, 2, -52], 5],
 [[1, 2, 4, 4], 0],
 [[1, 2, -9, 4, 4], 0],
 [[1, 1, 1, 2, 1], 0]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-pO+OO7PD4TkN7eHH@-3_U1`+RYJs0Wb6*F?(OYE3bOlb6<Z<S43Z+x-'
    b'saQtjq|B{P{l=`Jcc1@z1~i>GS7bKmYdQumApimDYd$_-&naw4Y=>&9i3e-'
    b'fP*(%3bH2UG^Ba@Io)yOR{ap@)E6W&+6UN&;S1X{m(ys+e@dbuHEYPX`cG%duryDGmkGTSxcK!kE}aV@x<jti`q1uEq`5R`P^sKb'
    b'(>jEWu?A%O@4QCmo%2<F}U>be%rZut=e0W-fFjYPkJt+t7pB+b#B@vRXg*Jw(HPS*J+-T>L|K<@-'
    b'}MI#hPl>eoN1*+x)tW4No@OX=!Uon<Z;bx=Tx*Bp>N>tu?I=ZZ<|~S^Dm~_SBA8&-Lpvy=R-'
    b'E>5gstin!ZubMJXfuk<RE?lz_3Y`V_I3wg^u?W|I{>{A=vX5w?@qn`Jz^U7RJ#i&c+j@N{?c}}TVDc$SMcP8o5(rWV5rq5wjZr;@'
    b'1?&-&K-g>9f(L{A7ADb+XrYy<%?(KC*mNresEd9C6aMRQ3vE$9=Nv)lnDTd`<#u4ddc0S;mPrtd#O1#UK+7KyqKbI-'
    b'16bf_N03RSo+NII6tL}XAnQQv--N)%Q(V0_pj^bm943qZM#*EsHW_~S~wYh28_4e+ww!@Z6Zk@FQPpLNMkkqbG$hx)WG}2q*Uj5k'
    b'gw)S8aE^uGmPE_<JT1W3z$=0av_67byK#_HJI$q1u@LE}LEvEs7(oP@g-'
    b'Z^E@dn%P>xKf!jPwh>?aoaLSK7L1DgCSdAmq|?A@Kf@!<O0suumiaAI@u18AAM2#o#ve7P&Aub3hx=KF(CGJnF3%%`&Mu|m`c4KB'
    b'`-'
    b'sqL2Sx|fTOI{!TzN<duPgiCj$%>ysM!%>Fle{WECco(Hhoc62U%|pqjp<YcfAKF~miSQ_jUzSDP<xDs4NfjddZ7#c!fNM*%#rGsw'
    b'sV3K*AtfMv?lN=lZ&p=W<kJeM{$T{92`JGZTL7?6=`=5;NS1fFP61Q%u~Wp3)|4NO1^`N7T1d-xR3l?7B!r&?lYz{x6C%-'
    b'7D<XBs{4xocb8)k>{vjH6nA@r}U~!!qDnG_f8goLK>po8{b;j<$PS$+E5S^EnVsuS@UU<L(DH-'
    b'^Il;67vV?j$4`E9YreI*cqcyWn>1jGA6JY%e~a8voq^E6(~x+E|d8Y^yZ%LJzxc3F+Qs@3&SZIRK^I7%gUIV4wo2rmJ8p^b)<Z6r'
    b'xXR)yaz@D-09jr3`gu5>SW-HpFzD>ZKIR|9r&;ntWPnvF8#VpQ!wOoyBWL62|-G`s-'
    b'F#!H%7nas1llzq)9Q0V(VShzOvM(Q!>>X6R`44g^%<z&>0#w&47?W7<EeP{K)6&qpXb#RJ(N}i1X!}R#q^#Lr<^;Qbmb&wyh$I-'
    b'Hpv0G3krlr2$C*kQr^8+;+T_9vlH_({Rd^(N<->Fe{zvC>Nr2ccKm4jq-'
    b'N1G*AagHgwF(_rmX+8ZLLO0d>rL5o%$?s3`(~Hl7U~pcx0@k6Gke6R_^i0Cr@*7dcO-'
    b'(8Ey&n=cvA;3=ZvwC>iVYofdz$5C@P=({&DWio|MN=Z`sepb_(0_`B`Hgl^~ZphdZ*DxCw%IYN#o7v6!L0c}git6z1hE?);YBLl7'
    b'u#-{^J(EiBPlY;rt+7+KG19zcE0e`^N$yHr_P+FH`+k*SINiXkT-m6?K4~s6Kanb6mglX-FYMYsnzcea3*4T$|3y5XnaY+?zvD$('
    b'P(P5in?PfV%Fn$7m1CTvpv4#OrsWkZ*HhA{5B$7=Mts?rVYtNT17fl!V^_vpH_1fwMgl8t3ul9Z7@cglNk@eq)$CX^Km+Aor?a6|'
    b'4AVMeND;$*RVsq58Ov)!z5synJ_Gq({h6u3;1xgyBH28<ZI}Ps=F>rqmupxRmcdOJ4#f+F{}ZDEE4OmKcNmaoL>;MMnRo;~h7nxU'
    b'@=p2{Qo{umFUQ_?#gJw0b0BB79B%F@@fKm|&$WW0U<PEA+p$7u&bmvyW9#@_^NA1Mrj?1ukmj(j)bp*4xQ0<IqqXHMstg4#7$v_+'
    b'X=^=jJ$|kLs7{6Fz7u?glWgg^3{Xl~&@AD~d?)%Dg225OQo<~6HZ@|q=qVIRTPvOmRtBthJ-'
    b'9(l1OZIwIv*^Igvl}l2e&hOSRGUCR#q+p3&9l3l*kj_U}T%GF#(MD`p)>VOgec!D61EXzCS)0G}j|Dq2;H8yuNB4lq%O=U%vS!6w'
    b'{-Iy^=#1sE((AeE<-'
    b'ZM(!Kd7U3`6KthJ$Ix%D+AMjztFH^3E{p!_;al}W}#ioJsfY>RFuzCzwLvv^*Tt=Fyrbrd{@_G41KQB?RT|^B<&IA|~1541*Ec!i'
    b'FFA*pPtB-'
    b';!2s3JgAgW6<c#R16bV`ATvl7LcP2fgoxQjhR+9`DU`oRq$z!{#TO5nM4$#?}Obw7^6;+OlneU_tibFAd_<`5)mAv>Ic$0FEZ&p}'
    b'`zeK=)E9{%#xDacXB!OmmQkUCh&vIgTe-i?J1-k6l?SQ{BG4+Df-poEK(w#N!UcfD=iVh&|uoF}7t8>!{4Yw)h}d%Oh7a>=VQEBc'
    b'Ht*r@1OuW4iFitivfI#~dMnRFRC!kk#|tyN$Z8k0~Ln8#7Vl0Js(Y`pTrH@Vhel?~X=xmbXZ`<?Kl)T*Q5><K+jSS-ey$cA<it^^'
    b'x~Nt+LD#wj>GoWPmA&XAKvGLeEnLYXVwL?R?)vFNUZKN&<0(i!r#x9kVSuxbkJUI0E10s{kpxSkB<FtL^GuvR1)a5t@Nn4KX*By$'
    b'F(y|_XASjQp;N+h9lm~LQt3#NZZKUPZQR|q<SH!0<?`wD}Rt;Uo$vO?Hcxzus#2VC_uf{+#-'
    b'Hxs!@R&pY*W@tP&(#yJdrrwapPO5p}=T7+)wN6p{d6|A9Jaby%#o){h1ETYT>4mNd9>T`Kp0nNcz^@P)MUI{l7K)nD%b7GGNQK}f'
    b'#4*No6Wk2T&1l7*GrXE%{@S0>yv)YI<55Q%UneOZlY#6s?R*Tf%J9U&?X3v3@JK<33Cch<0p|yPZkHHXGf|!o59n$^@QFILesAfz'
    b'7z(B}b+m~HK-Rm+JwriANaH<tfn4y?*yCmNb{0BQ?tulkCH#U?Mvg~n3!_w`nTYX(j3-{Dyl$(6-'
    b'`X^c5A*?=GXZ{VLZZUtgd+G0%rqx>(x{dqYJx);k>x$Z023^f86U#XVQprdt}w~)H;j%wYDmg8mCoyqpUS&!I2!XnQh9W0hSw=o%'
    b'OqTO(~Y>I)}gzMS~)X9+=i4UizXQmaL_vJ#bWNTdQWXCnhH-'
    b'6ez)VN1Y{Mvo4{le?But?oe&iFfrFg>gK{82ecEeGP!&^%z|t*DaLsVUW*Duqu8Y$TFm^ePiYc5P1T=jVoC~6IU)*dM1i!}zxO#)'
    b'ty)s85IU*Ei4Uxhtu7GrAc(xXNC3uigJAa<bfMC3}<#wkKS_nk5GZ%;nAdEX>P@AuYlO)sY9gsb?8iPJbuIV9)U7_C5<6;{yNQ7h'
    b'rxdgSvK~1m3nZ+j;v``GE9Y+t97KDh_@x5-'
    b'Vd`|O_WP(zr!3&~esP7$IMu}SFZknV_#faPnVUtk=AgAD%_Y@Li&=Snu<2*zT28ZZG^6c8fOMpIxD^~_nCNpC2Y{rt&C^vl3Q(`6'
    b'rGA@jaIN8C>m!fkWBZNvcK5;WU4(SJA<ud`HMjQXs#*3SBP~ARfMEZo`YxO{S!DacP7T7o_Y(W;NE~?j&s0%D9Gvzvuz`#{FpTnf'
    b'of}CSoFwI6R+cyj#&bNdpY*{Qzu#T`bi5QCwr`mWrMf>ngc<>P?MWlWdH(^7YmN*e4zfDE}EVnom+l?_Hf`w#i*pFv52@7O#@_H}'
    b'61LH;PzBBy1pV()HZ&gB(;C8ql9Atb#0e@)ldMMo~Dgr6tS&?f>Irt0+vuS84%$VbF6ieC%L`Z0=iO7edalKQX%YX<E%gAR~DFG7'
    b'kje}L+I6Q_P^MjnrR^n4wXNY3l8I~(%Q65K;iE4Oo;r{SwWS5D=q6N%)j}ta5O$isE#z^CI2Lv%3{<P1fp9v?UWJSUSpT|$g0SpA'
    b'WU4U#g&Tl^~yo~-qQ>>ipVHJTfCh+BAyzQYIhy?;-pd;SitT5ALjEUug6CmIOc*q`5b18@m{%bMgPs0twdt_yz;-'
    b'V{%lMCT*usQZNnaUOC^w<q{p$Yu)tHd%3TIG)w&^`$pacrJr_&hr#hIC=pQw`&{LH%j!8<n9_35o;Fg>LcA*X$z*SciDRAW$!^CZ'
    b'h!%wA|Qw9I-7Rj~68^sW~Z~Y!a3bPo6LluiGkyWFqm2vBE_0c0*#@YD5jpqc-dp_1_JPQrIWziU*+f4d?pQCXz><g+^{B9S$a(RH'
    b'QP_kQ!3~HmXwh3Rh9%9QF>&jU^o3ak0;35H?hIp(EHLmL|wETzTV!-'
    b'h|6Ru;2~<bF75944B4YUeMJ3<{XZ{9Ou?Jfu(6s2`(KIyyD1+4w1_t%p3>A7!0Nu9o>2i?P=)Wel{g#Sjps`P)n8?r-'
    b'@J;Rwc=ZLk<X(oUYs*F@)A|BXh6=8nK$a%3yk&{8Y)D4ctIhI@Oow1gl>QS}kEUpaw)G&ddZe!MNjbe;tu=pG?%QL>}%&T!z7N&>'
    b'-`9!yYhQXaPu&aJ3W0a77%uwy55lr>F;vgeStT@gpYEk-ShM<iDaQAU_VZ@hwa&zFQ|wM=<-'
    b'7)cp*@1^Bl^hd>5vUL(2E_&C7nlh{v$xEaqEkH;#e7a>G3Fb4^~k@l<xgFimYwu2!q$L_gfAo39)?!;h;Eu5-x4MH9+QVwo2k-'
    b'FzD{@ClY=^@xSz!Y%0FoEb8go6wqUpdx=W`Z;=m6zZ@$^*MQ3Zw0NHT;`Ud{`}ZV5bI4Vz%&gL|iN+p|huWY*mZLgBbjx@dv92Az'
    b'QHB#$wA`V!}ooW5l^(P0EzYgtt<pC=#*|f@VAl61s<Rtog%MXye6`_xBK-h1H!LGXehwRdc`HLJ=n}3o%4sO7Da-'
    b'W+X=fBDuAz3_fb`Y>MQ=f^_nGmc9(TY9^QqRYFS~HlWRP2l2+q*S>HDmjb$lJ#6Wl4|++X^h(O@u1X+Pu&2W@6e0J7Dfk@K?ciLP'
    b'S4W!T!6Us}d;U6wL^KvmP~)5yTLk%yIGPtEL2`x?c$F>@uX`MrRg-'
    b'Z@wPBZ29Z&M5Cs?xu8zXKzPS0i04D=GEfGt~?rv#hXZe+rUJ2<V3oTuXm;Y$?ge<C76{+b}EO}Iy*i{#islQ<}eXF1RyBaTH{6I)'
    b'T@Q6HoDvY%iEaTQ85sF)%WDG(vm<$)pQFCN|THIx;*)+Y)Jg)JpQ0-p1Dzqk|Y{Zu|CprIOZZbAF-w-'
    b'f!rrO~S;nc~ND&d3*V5ZSU~zhB&7fWd7Hb7AScgQ1}JH$-'
    b'MbG(AN&BbH#9c04q~;5x>KJOjMmkl5e>_;=_z17o7#b9Hi%{=eK)8<W&Q4)Y6)ONwVB^z4*4LU<Z}KUp7}hu6JlktLNlviY1>_Je'
    b'I6yTo~(Byf<343{Fa?|QJQuc0NEw2s`OM;&F>4J3jd_y9>Zo|{yR8)Je!Jt?GpkO#5<y><e^bD6;$chY9W)+wYa*crbo0;FrS3O^'
    b'YSa}c~TqK^es(MGK1(C+Uu7;0=|l9Kc$5;<Pj;pK+$a}<mLn2q(}85t?80k)o6mNOdMb6#VDONg_;gT)zf;0=Js1uAhwh$V{3n#3'
    b'Vlit{Gy)|FJv@relQdzjhna~wy$M?Jj}Q!%S}+z7~iC_$V(DV~UyRrIS|xU*8TjA_SrKJZ(`5*}WVPJ%4(mW3h0<~ehMLZwr8C9l'
    b'K-Y{4J(eNTylw~0EuhL#o~AqOfY;lxDNF5Fc3C(F(eWJIxhW?|;YX*D$ZG?~l^Gxiu0Rtq$o=$`4=1b--c4-'
    b'NHwfPBMaXsk|g%2>Ocn3L-su9fKX2uz#-'
    b'2IB*u=@<U`9B3v=i&&F{F&pt<7VIuilNWEt)KW_TQuJXzBE>SCCvz)lwRrFZ^~cv+@D3<8a6NG%V7JAw6l3H3;z0HzJnZ`gh>e>?'
    b'Sb}{!tiUbVC8EIm8NP-fbK_A)oF!AfIhtct+HlMgHtC_QVEp`vM~dY{foMc-LlyQO5|5lmlhA9-'
    b'e#C_Fd8i)8JP7RFZ)Vscw?|M7h(J(o@eK^dnk0b+G<c`FGFK#mcruQtDPCd(U6dDoHsXO;Q1J|W0_huZ8V3TQGACVU0BhDmcLr}1'
    b'4}wL!K&8KrxxmNB4qa1_f!YHF3>Q_=4{f9O=<<%|I_na;YNQ~cSdvrl+<woCNkA$5)QuVLIpzl&G>{BYN^=uwkf?THjmYmFUw2tM'
    b'j&ER-_emlH2Mezf(}^Et`aHg#apE~4q7l4G+(kkma|{-IRO6{0BM!Zdr^L)Dk!-~IQ~sRM)i_t~>!3}op-'
    b'8wstWJ(+Qt@RaT}&YE<s$|CZMc)IU||FmOG5E*97pMlMoWkvJx&%EY=qBcE!+q~qqvML7yNaW9v%wlF?0??rL7fLz^ZSKvk5jKrD'
    b'9$BjPs6;QH(>;6x_Zjz$14hj;VHhndht+?Tc)aexdkQiEP)_`gqS;#fabzL*PoF7rYiyV&CiidN4lB5)Y3tueAlmpZK~D@PqUY{I'
    b'%lAK2i8&k^xK^-'
    b'i}RcrsI#?VJILbu1?b%q5cwHpn2X%xhLeY$iUDuBjzw{L_8!71ZW(~JPBqd)kw;O69zXPKy~;Ajm>L^nk2(Y6GT?91I0&OlvqlX*'
    b'Z}-'
    b'ZcZD$%`~vbJ?B5jI8qbU&A(X<1txUIKed_YUNQLb~&?ikLl=*rE#z!~s)eNR*V@Mj**YZYauoHZ&Cl!x#02FvZEC$<>+q?PHccyl'
    b'Hfh0#c;q?aRa>4j!2s4FGTbLoow;q}@QD>5v#v=_X76bp<B=ilL>@{sDZ*Z;nrWu?-'
    b'Ui5f?hbTZj5zw2)2`z=PQy7jJQji{({sCruG2%ehptiM8^-'
    b'Ly*W7ri|41!^eC55O6As?>BJ!%MY*Vm=*Tu~D4NX)@mL${HGnCs<}8xVT|EW~kwKt88}D_35P6TJ5s%-'
    b'Pvc)f{J2AfC=9w1_pN6;H+DnL!zGV86f+_=285D&lidLh{7ZDX5wpoEe+N{TVlp!vG50H<<==i5E@+m%{`Z0oL8)8;Y%$3MV|5VT'
    b'2|YQsRsfvE2q~5+f7UY>L5;5E&@}Q&vvl3d}0{4VH=G{e6^Eg*`Njhg+Cq@&Xt87+0=N@mHuP$nWty{qvu<afJG;#^m+-'
    b'OBt{vgoIA0iu0W~u`||%Di-{Bf%1aRa;6JR9Ck0hLrS~qf>rZ-VuFL1C(fD}2eNF&{Ec`Z)#Cu6=g;?WM%+RLPZgWH{M{cSdUXm('
    b'%yIIE*CGIcinPg%r0xqxE{l_TOcyAp1&jQh<8h3m!55N+-MEbX<9|6*g>L'
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
    candidate = intersperse  # noqa: F405
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
