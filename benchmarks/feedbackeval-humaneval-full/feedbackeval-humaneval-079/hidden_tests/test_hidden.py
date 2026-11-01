import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[0],
 [32],
 [103],
 [15],
 [100001],
 [255],
 [999999999],
 [1000000000000],
 [7],
 [1023],
 [1],
 [2],
 [3],
 [4],
 [1000000000],
 [6],
 [1000000001],
 [1000000000002],
 [5],
 [100002],
 [100000],
 [1022],
 [8],
 [1000000002],
 [0],
 [1024],
 [100003],
 [1000000000001],
 [999999998],
 [999999999999],
 [256],
 [257],
 [1021],
 [259],
 [1000000000003],
 [1000000004],
 [1000000000004],
 [1000000000005],
 [1000000005],
 [9],
 [1000000000006],
 [260],
 [1000000000007],
 [100004],
 [999999999998],
 [999999999997],
 [258],
 [1000000000008],
 [1000000006],
 [45],
 [100005],
 [99999],
 [1025],
 [999999997],
 [999999996],
 [1000000003],
 [44],
 [43],
 [1000000007],
 [42],
 [999999995],
 [46],
 [47],
 [254],
 [10],
 [999999994],
 [28],
 [1000000000009],
 [100007],
 [41],
 [1020],
 [27],
 [1026],
 [23],
 [999999999996],
 [253],
 [100006],
 [38],
 [100008],
 [39],
 [100009],
 [1027],
 [261],
 [26],
 [1019],
 [1000000008],
 [11],
 [251],
 [1018],
 [48],
 [22],
 [99998],
 [21],
 [40],
 [37],
 [20],
 [100011],
 [262],
 [25],
 [1028],
 [24],
 [999999993],
 [274877906943],
 [9223372036854775807],
 [10000000000000000000000000000001],
 [8892743],
 [1000],
 [274877906942],
 [10000000000000000000000000000002],
 [8892742],
 [8892740],
 [8892744],
 [10000000000000000000000000000003],
 [8892745],
 [8892741],
 [999],
 [8892739],
 [274877906941],
 [274877906940],
 [998],
 [9223372036854775806],
 [10000000000000000000000000000000],
 [274877906939],
 [1001],
 [1002],
 [9223372036854775808],
 [274877906938],
 [8892737],
 [8892746],
 [8892747],
 [274877906944],
 [1003],
 [9223372036854775805],
 [252],
 [8892748],
 [997],
 [274877906937],
 [8892736],
 [274877906945],
 [9223372036854775809],
 [274877906936],
 [274877906946],
 [8892735],
 [8892738],
 [1004],
 [10000000000000000000000000000004],
 [996],
 [10000000000000000000000000000005],
 [8892750],
 [8892749],
 [1006],
 [8892751],
 [99],
 [98],
 [9999999999999999999999999999999],
 [92],
 [1005],
 [9999999999999999999999999999998],
 [8892752],
 [1007],
 [9223372036854775804],
 [995],
 [16],
 [263],
 [53],
 [30],
 [274877906947],
 [29],
 [9223372036854775810],
 [67],
 [66],
 [9223372036854775811],
 [9999999999999999999999999999997],
 [63],
 [9999999999999999999999999999996],
 [81],
 [82],
 [80],
 [68],
 [9223372036854775812],
 [32],
 [31],
 [83],
 [79],
 [62],
 [61],
 [84],
 [65],
 [60],
 [9223372036854775813],
 [250],
 [249],
 [9999999999999999999999999999995],
 [85],
 [89],
 [9223372036854775814],
 [49],
 [78],
 [50],
 [88],
 [33],
 [90]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-pO-JCZiJaYZFVT7Xs|i-'
    b'C70JZ^*ro<Uz5kVR|E(SCJqv8#FmBqQeWPk;5HfXsW(1<?QdAOH7X{%_C!{`Tj8|M8#y^Y@Wz`}2>#mRb8bYur*Tjvj8>x870j3i'
    b'0$bV`wAfm4**~YNYMU_swT`vbuZy^B;fy{onuiYd(92#b@<HXQg!Ry1CSl`rfz9d2G&mVjHpFS;n$^#@?sS*e>7k^O%sbt(*GnXU'
    b'rZ>v{^&nW3_u)7<=_nXBuPmyfVX$*J?{4#xbLNIzNx8R>t+&Z6=><cVG8bzvii*R8zXX)99m&wnI3rE{`RwzUQ4irV)M~lgdmbpJ'
    b'e^Ccys34%jIA1N*?{*6!VQMg?#zXY1Zv=d5Xi@Y`b*(d5q=ii6QrSYno@L+GDvP_u@6qvU`d(*50!xFVojy7Sb%YMqkmw`%)TVX}'
    b'PTEy*Ea}zomUPpURd~zss8EGpmPDDicypC~1f2qwuclotw>jFb%y$i*wz=qK`G*){coWrakJ8&N8{Vx5a|4Y7CDVyR6vHV>Xkxav'
    b'm+k!qN_Jb+>X(t(gIyvAi7SzcMB3&Q?#$*T%Mfd0n^r^O(7MojaY<D33As_7HB}l|mWa!blW{Qvr(~Dk<)kLzq58b&uBW`%=Z2&f'
    b'IFQJypxiC~K;)*4u_(ANhn@X9;!Bk>lLOPO)()Y-Ta0cQhe1CbIA(-'
    b'=_p?aWl_8_^wz3#c{fiIb*N;rqlzY+iN&eP0jcGHbcFK%BNSt2)47&R2TocM#+<DX`9YE)<X7^+UTpT)$G)D>Ivt!Zf5p7z1m_5Y'
    b'c6w?66u%Pc&l`R^EV5#P_ZYh+N`d4a@v$TUzG3uc?`A31k%gFQ;m_i86lKKZCv^|QxC4E9sV@&@3HXWBah2OmDNXjn*jj`ZTDVBT'
    b'i5oz-EIlH=fP^tI?wURe@WhRIfFJD%-'
    b')DJU79J!pU0fc*iNuXvC?%dY>MLC8yjnHjqWNeS)NQ?XvcFkL}JCjST{5Gj;79QN99#~&7Shed+|=R1)UaWn3TipCD5^(?!F%A$v'
    b'U&`jVz4$j>f#^M%xEk-RQVHcSzfI*#V`igAd%qBk0M5&g`10qHZ<#>bJdhQ~1KxPG^aF&Y@Xb`OcKa&O78urDdik)|~f9rACCtV$'
    b'N;bSk(3Sc?><qr+A~_nV)ea08QE!Vy4GhAAT&xofE2*GR3@^;=7xc<;MH<RA{mE9#`zlKtpXQ{j`&(5Jq%b@wU>=qW5~3gC8h6G0'
    b'H^|7kd5YF}G1`g;{sEvJm#A#w(fP4&_8%CF31+&3ntHd-L$_vyNohn}_!?6eK^A=-+-K!oK1-'
    b'YD<~`BbbXdZ8UDQj<(il7d2;~R1rh5(7!4Em-tjf(<!dQ;&thjm)cnH7%%H#(tBP3t*{h!tIYEp*0W72R)X^C&Efr6qh3y;!mrT-'
    b'tJ|7`9_Fu%Br!uQnDrU@I+G#|bJdG**W$0;F#<%sTpr(dKNJ@()l%ct1I|U|(TLmcDv35awA(bAlL61Luf0CiS@2Q(gm^b&uV=6V'
    b'sO;K&SxgjR!GSv#ni<(f3DL=nj1_#dc>Z||{=q<7wwhv>^wn|E)PUgOu{NqX<%0ruH`L6j_}xcnEcourUcG58#4_pfh2G+c6zJM4'
    b'ov(Co$D8E<6a>Y6Je~?SoI2LR5?Q<X8q7*86P|+m)EN*h*y2=|e;dwLTjYJ$#xoE|gprnHpcWG~yw81wg2z@&aZ&Im?HZcXQgh*@'
    b'2hFvdeIUWkn|GF%66hl$i7*QbPt(56(8s{R3R4jf(TX=&Du%{XTCuN-'
    b'!6tXy?NTza<GLqj*vEFV_DMPqs5R}DZffOH2n@aZ#nY(&BsagKGnCYV`g4bQQ2z|7#c8bRE9sFzcKmwGyaIOB_FD8QqPdydbv8zT'
    b'm`^_xN^Qe33Ru+&EAvxt-M~)SsbfTm1<z^q$rsPA9`B5rWfsZEdND>Dx8XC31z#B%ed`7>r@GA+pJ1X3WxLW11-'
    b'YxEf=C7FqB|#$;Uh2-UNE^jnZjxB6w`xyn89}))x;Uggq+q!p5X-'
    b'mAh3`oQH@uv0C6%a`*y~^c70nD^I_s(Hjp%_ARwBCD6upPZ^6T<GAfe!2K`t*tdfO9>f>nP(;F}XuUJgS;N3IDCLJ;66(?q9ShKr'
    b'EqF!&d>yAAMC-XXypIz^0F1|?p;=IheV~0FTvWjS|e3*DFslzUdPqI!6U88Px9h(M1IN!NJjL{Tuh^nZuJ3tpHCTGzynuZ2m3cN8'
    b'_d>tZopxgwA0+lfIyWj@N0#twqu!q~-'
    b'NGqf!8Izu&Ju!jAm%c5nsmV_R#$9xVj=fdPjPVulYp+lsebZ2|)>3K{lm#8uR^5sdfTSUm8}qh|pozoQ=L{$;suj+$-'
    b'ti?9{A4*RdU3IYL=nvk9q&<OYB<M|E-(!|^cB(F>1L*J8DbwY?ot-'
    b'v0=i?x7PwedDnyQLRI0DC&p_b^Sc=Pk2uUjpoYIK|7hyyy>6-?Wctb)^-?7_njsF(wB43aw3I)L!k^c0q6e@)}*)rG-'
    b'^O3HBFeBewQ8}8P<P(939DPT!4$0xtU8jK7{F%RXlSF^!2R&=bRiTDM=CLMcNx3o*?-'
    b'(a=HxW*xaBd9<*<fK_p~x1SaI@|cC$EeT+(rCY-~yP|973Vncoq%S(D+%b4&diNJUx}SZg>VDFi8M|K3N@F%x2IkIb)FO03H-'
    b'SEWf8$r`H=r8c$=IXqK1#G6rR-VhGGUP6PbW?ie46fYF#2xPpiDouS+M6vmU)f<=DfUGPFEnL$h(DkVo_qK~*yM#7wLBbrctG$JH'
    b'fwUj)nWmssF2*!C|Dk6vwHDVbl`Q{i$q{Nut#N4D%2i(2IjA22$csU$^Y;<ONxqS!;hdcZmfB@&sB8p6HVUNy&P`*G4{*65Fbl~H'
    b'3Fo5)TJLZ?;ivoO<(aL%i5K#skofZHuSgby9VdxyA+*V3QM@AHEp!d`}5$>%Ur<Vze_yHK9A|fF$;YXB7RF2&|EWr(=6ZU4-'
    b'FVza)u<-'
    b'a*`{o8jScM8inQl2`pi>*7LRe^nC~`_(11}dK@?A`EzZB3gw243a?CvPE=FL<nmZBMa5hAxxenP}OG=uHn?xXr(O89p?lT0~)sCU'
    b'76BXTx>kd)mn5%>0~lHj8ykYHG8L=Lp<q?&WeqS=&0PTa@J3npnOSyt22a^v+`?1R^l^W+B%g2`%TO7ieM5(F25Qt%5)-'
    b'#;y8eG)mSUs4?n(d#*c4?}=SR#=ZL8_7YqlsE`28^I@7pWMNemqd3prj6y&JgEPu79mZgxd^btc`Cx0a3<{H+l<{XK02dOe_w|i0'
    b'Uc*)a0lR%`qRD%Km+vWK>lLcjqlAQO%h3qk!25s1i%F3{jpzT>d;;MYAcek*hr1AjQm27#TYTxM6o#P)6-'
    b'}SPHbx{!GHOi8`Qf+)DP~f+RCUb2qj0>O9>oT?2f}jQO(tg0YdZ4Pi}&a`w2y-'
    b'{IjSiwoW=`=6rVLE{cobL*WsA@)4FyTrp%6i?vTBvaoM6U@brzcFRHlN#u`(U3Uc8Y6U-'
    b'S0B8Z`0rmnh6UrrT=F+L3vFDc=g31x8bcN^w3m9e$dQu@!C#h@_xmjis(osyJH>i3NTBIPqthty!C=Qn+t};+as708JzHykuc_9F'
    b'>(EIywIeLq^2NEv<AJKU0Mw>OYpxX!=_(|hZs6<o6b>&7}W?;xHu0A(AGJ%)z=Xejn;pZ`<sUs7?Bssvats&)ykXb4*o>;x9f|Hz'
    b'=B2F_I#H9+(QPyq3t#5~`^D{hxZKIheRW<~PL^LHX0%}xwTppi+-'
    b'lg<Sx@KLqS?~oRN)NjayvwXq0%?d81KabVSTbXc&?j@itKtf@9Lhq0Z*5!E_(j%}At8bRjewhAeN4|VaS*D?bh?_O%!7R?%aZMbH'
    b'WOJ9fFpmjHI<J^)()OhQ%V^SMI{P31TfSdDECT+^)P*a8xs>(Xk<R1>@^s$iB!iQPy?NbrVIE%$|y;%STBGNMnGx^31BVnBynGgF'
    b'!n1HRoQzO(kQ0rkOI6z8U)EOi{PL|ry<I9#!@N{n-u#-'
    b')(7i+Uy9m>xi^SI=kkA3^d!iW{5wiNF^NKF48{gP6E`pI20u*H8RdAV7||t)nUEH=fn%U(*tco{DI^sDb%OCVXp;A%&5^Y0Bv{<O'
    b'zmkqq2VmNydWI9?{7#U&BVlz;prNyHFbb>iW@{mkfshwTa~Of2Z~tbYOme(J$Y-8Uk2Ey6OpAgc=-'
    b'f^n=tfYdww$%oG#o_@$U%Ao^ss`}gE7qgvjagVX!}I+vl7)fQ4!Xe+SQg&njMV4+JI&X%7+4EE@~7uyO&mnnOI12vbH-'
    b'}DWbxuGXFyn5@|qh1X3&7z_v^Kzb{1sBKXz_Vm$=4O*@vn`|65JXfOHpVjHa$pb6U85M)H?Iu!LLn8r$ITNVphp&~5AXtX7D0>(m'
    b'bc+?FDG=RK$Fw}%f-#w8EaqTZA1yVU)U$oH&;T4LP#-'
    b'c<Mw#g^3C{PlV8jmC%IJ<ftGfsv2*QWydpaeC6%nL4s#y@u<7RE`;boz&P21P5-JyH46GATVx12f<9L$O&-'
    b'U==5%Uk1ei?N5*p(zzQqfFRQ~UILQP_C<t*E(&z<pF2NHa%uw4U^1AB)CD?A%EN;JQiD|}l)_x|cPgtx3xTvSiEqt5zOljkU^&#G'
    b'th(}rgjN6xa13H(CY(^za80lSY$c4NH3Q~0mhpYef>T5ANk26Zm3YtK2=kdK0fX{Te=QQP>XUS9pssQv9=);QS48jNLnJ(+R^RIw'
    b'm{h?CM`Xyd0Y|OctHCYhqx_-'
    b'MVL)X=>`wJ>r;X56{WP3enoFJ^6!BJBFXCiHrxC3PyM|_P0W%b|MaIZ&<j?MQ04OVz4es`JC(!{}&oq8*i`=End_n-JsxWGX9gs-'
    b'0hh&MVymdnsFi2XP{@N@BZ7#M@X(-'
    b'A<p^rR;a=HQv@q`y{Ck&8Sn{lPT(PJXmh$Yd((eMCbby!FpJTVcTc9~W%m7k;OAPH@nGHlT9X3*g+zeQM&i8dpU>d*$IK2Qj$ikN'
    b'DW8aRyZu&CWGc`^QgBq5Y2$tzo^=8)eVq!Q^TJfShLBxKW^rOHH`iETj|yXO;9NJLnGDh6tQesi-'
    b'X1aP8J`V?2BgAFQg7&L(x&49573y#zuZA1=KX&+i;6l~MK#~{8)3;H(c76OsliU5uHEQT2<eQnJ0*1;$zdJD%V7t<^@y?m!-'
    b'BWve?XAPd{0#^EB6frl&w6sZEbru7z#~`OC>2>Cjxkf0z$Iz+Zk<^jQ(XAK4ZKt-FCIY$k$8zQ`jk?PVMyZ$=g^+e}9e2Iz$8^vu'
    b'^q)W;uyH$>3wRGj8&w4}VTdGW@Tl<(WeB(NoT2W0AG1-;MQLrF-d$}z?tob|av2$SDxea*Ns3_T)~Nv8BqVM=W1^H_N$>R8K-'
    b'3OWDUHMI$P_qIOb!oV$OARf2bnP5trRjIGv5+eJo~q~fM;fDs}YOI7YtZAH4^-'
    b'Fbi+$k+_2!Nq&@Sl{egVElW_s|Z>xi`0p6Go3K7=umFOBno$$T^k<j)+bc7JqGYEmibWUgVMCdPT68sO=h>C-'
    b'qglQd>z`hM^n3Mj3a1<|TJgNk;s8XaX8z$iP_{Oqx4#6vpL+<DcD#kQ)yui4_9_UM?A*V=NAdi?W{S??48FBf}V8Cl_0Ml+{P{IU'
    b'u67XrGLu1y)BniX;-FO;_kG>yETe*Zz^7{Is2X8na+{%ielDHI6kD1(XN++2?U6|noJDx<K<4fzg_6gF0ZuQ$02r;kQ;1-'
    b'Y}!f01pQJWx%e0U!LO&*b@>mD*`x@oUxFk%>St<ireJ&_qHWW1aJG*>1QL0R3j%Zc$`x|^Py=;M8k5HaSd?&4|R&c3o9-'
    b'FCH$7I<kmU9(eIp1C3hMY1M^>0FpOFOjd%z6;1tkn!*AZailgLwpDjV70|5F_U2l8DYXTX#f3mjE<t|5ab&>dydrJDJGSACmNtl7'
    b'rD{y*I4yAVq*wtl%%Z&%!Sr!UeyM-@-1`?G9ABzrKljNRl%NMHfp(RZ<Aa}b^-'
    b'uYhf4=ehq*_E;cW|~J8;KG{YaF8#`D3u4vp&U7_-'
    b'kT@KFU2oI=47qYg&2p~a)CvYGRuG1c{A5~bGGp=pH_6~odKi7DU_R=L`qY0|zEdR1jCL#>vAIHnAyg)e$AD`egZCroCf5#Ok;8CA'
    b'S+OhQRn7;WrmZ<fD8&|{I|Xpj@W(ac2hAy&H%xCkBn05lM-lMNe%1Y_}F1QV)8DjC&Ww~JYCfpy;Kq00es##R_Ka0e2Qj0Q1Z&}J'
    b'~`(0)#83?e1zmy{GYE?EEm4zkas5)g_zt<&xsImMP(K5SiwS`p=<Ls+Z4YGNRCPoO^2MB@FGt)WF#GGNJ0+h~;5D-'
    b'j+D0npaz04Q~})K1vQrk2V0={f0XzncqHM|V?OQWp)NuNp2zyl8O8tO-YkY?znT$P@!L;HOVv?s$v#9V}gAb~XXKo&(#?omexZtK'
    b'034ITqm%b&e?UM$Gy25f2VTI7N`&mkMAfQbw~rdtxL39yb$q0(|mJVx8ltC{LgV&MA|3f)*=LmvSh-'
    b'u9+1Fy~w4VbW?z9ZNTW#LDB9nD$7LhX@VZz8Ie9E6UGFDyso);DBl4h6<rO`s_Cjt+VIN>tj}$%eC!sqrQG2<(+vwe6;}CVYg?je'
    b'0``iu4LM&p9ciMNJMPxIPWNva2OEYqbXy_hr4r8?<+llb_VJd8%1|F&Ei2JJ0yzpxKiVS`S?ihvHU@@M5@5}7rngd~FYHUbi5}SC'
    b'jAvPI^fM`1mwQBfR31SHp3sa$VHWO3ylZIJO}|$T02hE<&?nAoI5AO<-'
    b'U^ihUa6_;y+W~(0tW<=dDD(J%B7<GHhTFUZ6@hDK*hD`P&}W^8AR!<Q3C5g(+-'
    b'>KV2Vi!h=q};Ba;2?`=KL^`h|eAZac)1c?USH>x`2?ybHmDo*=&%h8DHG6qGb|Wd3c~(c4?>*;K|l7u7*Fl2D88!E_zD_1RdY$V0'
    b')y+Q|<T6NH1ZeFsa7aqHYbWrnzPoq6bFleWPfFe-H$h)?N~iX&CU9IHCeu<;!MDo*F}NHr|bnoiSTcvm#C)nd?nqR<UbB-'
    b'V^1T}I=e^~p^8cU7eYK92hUB|7h%OzTZg-JPP_9CX$pxItx}X#e9Ui5D)=!hd`14u!Xat88WxH>9O>dx*Ek;DGW*5HSFD&YnRi#o'
    b'kkc&c!HMFyd_neh5$7ga~7j3yAJD>B<VqHxTZ2C__}vp(b2VI}c8(&;7!F^xs>4+BiJ86u3ko(h9^YpcoP?5UWC3jp${(c<&OVFY'
    b'GW9Sz8a3;kRR=J!hSCUut>bBiBemQ2p66Ug<Xqqzx1>i~dS5KgB^Y>%h~>ml=+hnV#iSDp;^7p<qqhmx&fbx+z!JRTrHCR3rjHWg'
    b'w{_1Ml9}i9iFfVEOc;OI$_<>!2PDC~9+E*Ftm*$*;m&QdH?zyKv)D6`%S^BLnNLgBwDmF%1R0+g<nft^gEUA21pWa0yq7WYnK)Vz'
    b'klcQ)u(l4)Da6i1z$vGDBaDgaO2AuVrEKRI}@hs_XO`52rhVT<p~w=&nMugnG0Eju7FH{$*y~>LQ*?R8a}unvN>k7h^g*ac9yX`|'
    b'BwSL%Y=^*3i(<qI63Pqh$$eHj8fKz~lso;xq|8IGQfX1(q<sD^<g^s;hi_gap+|ZXgYIboBWRTI|APTu=O<4qTB>8<2j})xq+v6y'
    b'GLT1b&#<20iZ+(Civ7rjI>6>4!?w#WUuvk_!_5bJi*Q`Hs1)z*nd`@`RsZCIp=T1M8j~W{!C}v##qa6cK9%Hy~#^OK4QsmwbtC2$'
    b'M&`8ZLlz<DF%p&;-)wEE-'
    b'|fy}d%*Tt~ZFN2ZtfPFU>QKGaQ#A)$V19=}@@hnO9bD&7?CX2T%wM*9#8pSqPqwld<ro%n5$jiBUxu4~(JQe)9rC8T%3=43DBR~7'
    b'MT;WnTPQo%UaUTwCye;>m-Vp2Miz_Wvr$GSRK2s30F5h=Sman?z<(ExiRSw;YZf4)Pv$w)C0j0^!*H-'
    b'UHmOyY$}jhLoxE2b<UDOfKap*w#U;~@t0SGJ;>p(w|Y2yh}@kINeYJG#snan!?nT65$9ULg-'
    b'{ZSEn2bSU!kU2&Saz8ho6jTng$Ms4Xp2$v|Flvh*H(Wh>gq4sDO+C+whn8?WEyI%~`;N6Bs!F5O`TAA#K3J@(4Z`JKBUGedyuvVZ'
    b'+#8Rg-`}eSxtiH%lq^Av>5hjg)BzNo;X<!}u>L?hH0F#N@a3wKMSC)ddr1v{F0cPqItsFtS<)9BZhGS-(fA%|wl~r4GQO7}-'
    b'b?Ukp%;-'
    b'sNAi@W2s9M&IBHcB!wC~iJK7R9Dj;w&sn5knq)Ifw3PSp7|<w2S8onI{DyLDd@Gm!fL&;WTMyTO1JZD6@mhYy(zu$b4W+H>h7bMm'
    b'x(>W2{^H<#+)kS$N4cjna&5Ct}MUXTf~ln7-yw6Ts%8h%${1?{rFIUMN)u4O~dB+e-ON;-`_x(_)9eoxFxsc-'
    b'F?3_=vxtcucR=XX~C_lXi2ZG`LY)zEJHB(*O}2O+0>?j#AH3FElxMmJb3vSwtJ&tRSnk)TMRBQg@%vq7Bk&YpDdhG^vQKC=%%RS&'
    b'v9tQ`Yw%>1?{c^a&Vl+s~6DR|vTa`>N~TGgiZbQd{ZHys=KA!+v>ZzQ9}lRvxj7N;&BrC~`Cm1ofgNID%|z?lo4I6!mn)M0qnxuo'
    b'tlk~mYek3_Xcx3q;0XohRL`swmSi^LJW_Ev>|rp~ox-LGzr068#;?ht*4wKkygECQh&a+%s7EILaMvty){pJwbZXoKT*8;h5(HE1'
    b'gg;P|dM6%3~_pF%>sp&;d5o8aWcRZ%)ils%ITW_I9IXO^tVpkv|h^1(iFo%tmKj#RW&(bPR4F;IUWjLb(@z_gF8oekF5wD+|KhE1'
    b'yYpp7t0kcBHzv&&ZpowDQqB)ct4P<IcFvQx;+yc3^qDn_j(GX6U^Rma{WpL{CodLp!Wsgq}C+0-'
    b'WE01$`1L_|t}dUf$vGe#gf`?~;v?RUfro@2R4u8{LgO!d@N9dx0tLL7kmuoudioJqoFH3-'
    b'FJeV3+TJOTi;#G6x8i$!rlyY3Bzp)?71Uu0UpY=QhBBAzA*qA_h`|9|Z-X;1{3KppjM-QeKm87rKJm+ChS3U)IP<t=2^4dJ`fB(}'
    b'qSQ#aRM+2T`K$F<K!0D<{xn++(9jc93-'
    b'zkmnzhxu^4on3c8De#Uv*YsTuxs0D^f^?^%QlwJ@qQokrb|}MDc0>V`nORnY??!Mus>JhMnl|&H(H<a6+o}zdpjlfIa4J#jS25a2'
    b'aF({v!k8HxrdyaV#}?lJP1<rF<ZznO4wX-'
    b'0b!Hi=V&0mrS+cT8mtJ*q3qeOJv`=%3?!mm!mSlc~89cgBw2>qF8UjE&VYd+phG9d46Yq%BFosJ{Pz1Vt^qp&F)7>N#iu|)DK;s='
    b'vN)#JYLF*(Z$7s8rO2L+yaji&hnr<@HTg9DVqPrMHH@+6FpS8Gn9DP7wV||)#%Z9AaF=b3KNULBFNqnDB9GrSEBAA}nCpwtLnwTR'
    b')7KxqcNXFoGXG-Vagkz=zeQao%wiDjEVT6=-!IaYs(WvoI5)>@0VjQ!SyXjZ(JWXY9DC-Qy&J$1ndP>*NGwCBF2jxK~AOPQmUI2{'
    b'N76!Y}=0l~duIu$WCY+>RO8dfB-=P}-'
    b'&Kzbwi~=V3hz=)pQ_<lZL>Yi&@qwQ<RqCJxRo8V1X`b(#0s1Pg%|}+f>sNS`GMcU|4xO~nh<rDi%s&;~^f)=l18#Jh`FC?cSFN{p'
    b'&}rmyb;n(sJl^%Ax&#dvGMv_RSv2Sy;9VUmBJSm;k8iT^1&t|22`X-'
    b')>#>M`lP$o3=#PW5x(uNUBDy6>%<EWf&^`6<U}+K915?@P=&)u-'
    b'*kCB(NzqoFezk>FB0@|8vwkgN>6d?W^B9;s@m;CQAClhqLhZ`#tc$A;jtSj(N8W^>h!s<@Ll-'
    b')*I*@Q^XFR2^it(><b;p;7z$2z(52j`5?gh(smFQ7rGMRo=%mU~|Wo=z|C@r7g-'
    b'Rqz{X0(nXVP%N}jf<>0MS_qwMQ;7hi+&#>VFyU}fLjo0;OqBlTp)kyKCf<pz`aYqM@8tQ3>u|&bj!CU5Bhxp*NrEkq7ERy6sG!>t'
    b')puZI`TQ2f>%vPs(tekx_thy@pBqLPCr(%XPq_yAiRIh&;6V8m;VP8W-;3'
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
    candidate = decimal_to_binary  # noqa: F405
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
