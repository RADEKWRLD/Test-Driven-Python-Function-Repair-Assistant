import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[1],
 [2],
 [3],
 [4],
 [5],
 [6],
 [10],
 [12],
 [15],
 [20],
 [30],
 [8],
 [25],
 [100],
 [500],
 [29],
 [14],
 [26],
 [19],
 [13],
 [9],
 [101],
 [28],
 [21],
 [24],
 [7],
 [102],
 [99],
 [16],
 [501],
 [17],
 [22],
 [98],
 [11],
 [499],
 [1000],
 [1234],
 [9876],
 [31415],
 [1000000],
 [99999],
 [9877],
 [9878],
 [1235],
 [1001],
 [9879],
 [9880],
 [999999],
 [9881],
 [31414],
 [78],
 [999998],
 [999],
 [1002],
 [100000],
 [9882],
 [1233],
 [80],
 [999997],
 [1236],
 [1237],
 [1232],
 [79],
 [90],
 [31416],
 [31413],
 [31412],
 [31411],
 [1003],
 [999996],
 [68],
 [69],
 [1004],
 [97],
 [23],
 [9883],
 [89],
 [31417],
 [1231],
 [67],
 [100001],
 [50],
 [94],
 [82],
 [53],
 [52],
 [51],
 [9874],
 [31418],
 [77],
 [54],
 [9875],
 [76],
 [9873],
 [1000001],
 [96],
 [49],
 [1000002],
 [75],
 [998],
 [35],
 [39],
 [48],
 [34],
 [70],
 [38],
 [95],
 [997],
 [47]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-lpoyOJfh4TkN&dJM&mQ~*ivl5M7^P(bif%KZY46m7VAUw=5B?v<*hq&cVAB!K_M`R~8}{{7c~eE#|4$G^Y-'
    b'@}ECvvijruw^EL8^=q?T*<H>YH<v!dWuLNkF_WTsb@w5)iRv;x(pz%PP3*^CKmPpZ_ix$OS#$f9Qg^v3SBJ<PV_M!?ceT|@N~e`N'
    b'Qx~-{^p3_dO>({UYneIoxUM73qFSc6bXL1#S6*6l+-A*Exu?3QoKn25T2y3g>vFe$Ez@s1t(PU)eVdFmZ*N*x8AsPu-'
    b'&+$$JKgwYs&>xqxer}sif2t<%gE_FkCbiNaIxBYF7sYJ>o%3OQ<l0d`&v5--x+!H$QWnLJ(51P(J?l~I&A%lUR#p7FDW_I(tENw%'
    b'9^vaMzyk@QqRfV?n%^;J-4UC>*l?tufE%E%WT%Ok0;x!*L6;6wb-'
    b'>@hTNRWq7lMdi!_<l()?Pc+^y`0(wwy|<y;DFZb|CxtDd#AFbg_b9?g4Bo&BD!$HZvwzE7uGvy=BIMO@FUs$R~y#g3MnwB&nB_w9'
    b'WwOS?+1+0Lk=GZXcs{k6<U$;)6?c*K>#xD@hg^HcPslv+F6lo|5o9NFaXe{yfmZIoQnd#IwFv$9=EeCUjx$}I8XGS_6@v{jjRmo_'
    b'>d>ex%WcZT2FzRzwp{ig+LQ>aSsbRx|}Not$9FX|zwbvMs-q}tNTv(CkMv2-hId@Vy4(okw*P4m!xQtr3v{r^fO-Bj<IhdOH=qnK'
    b'20gTCK=)FnT=sk(hJF8d_Aa`qjy3_q7KW{q=t-'
    b'_&eTh;b*a&r5(^KAky9Jp8rH(KO9=_6oFVS>_2#bbhuqyr<I4*&L^(_{}r(lQ{kzJ?}Z+PNibK-'
    b's`LNu4|5cI3HMdYIBE5vLXUj=~%Dn6lS6Hd4!(Z0YA?a0|s!gOScw#xwWTul%iJ<Zq6!mu6}xJYbNFq%yn%o?PmS7XZ*TIzJtC}<'
    b'y0$Q9)MwQo4r_*!?4^6?3r|3e5F7#HyWtBSElemIA9(f;EB2=W?U(V(z>$@{;HB0whn30I7o@kW$(a5+-'
    b'O)^Pi=S~EDFe&W*aN#JDcCzngZ6WRIb-'
    b'{Yff@FKdXK|VK7uG?Rw^hU&3O=c0IO|th2!dRiL4E`mEl)Y|i2wE(Nj+B}|&lG&O%oH0mvkW9mnx*=XXljS&$R)3R$`sRK@dgJ<z'
    b'W7v-!(-EH0dER$%B&21~b2<|wf7TVl-ctChQ7JLB0jZ>7A3j;oDMFLg~v3@NRs9wcw!~H3qhbdB>7lgu~$pJ%8gNnH++ugM$AERy'
    b'F1tr&KH*0p#b~mS}DpX2z!TnpAv9@aJt!Dn6^Cn*2Q-!t-'
    b'a;`yxjP^^SR=iaxt<VNBs*z1+3_S$TaOS&q9rJi@&`>MT%|Qn(HAtyGe8Yd<49#h;MT*>W=PFud<c_`-&+Md+3-'
    b'Y?vHF^n2EV&)J8@%+Cc)Fa%@P)E2QwjoDnCHy5QHjwNCCIH#W!QXzTu1$y0AMNh%uR-;PRnc7-'
    b'hlzcn9DYE_J81*Yng>+%l$0zgrXf-CH1`yEnf8z7^R3z*S5`IQMP96{D>@sH&01N>!i1O4lv23rQkrm9WTG)4>b3!5HYMimm8B;7'
    b'T^@-5xzhbX&a1NvhF*@3MvgW4myH_G2Zpn@MZZRV=YPp-'
    b'$Q^R&=(Y8*45`OF_n8v2CfDzF##)IoW{*?$+Mfyq+2}z$r1S&whXJAl?wlyflNxzbMU&$(2Z+Qww(q!+G1-'
    b'jQ2^bJ_;)~)pxA>v>;oIXKyt)u<qULBY2Mwru#Zr9n$`+#-'
    b'~q#j^VkHE8FVvGM#~ew2`;@%4!?9>W)l;^8|iswnob(+7VodXfF<6aybf^E>FU5$P=kw|TB9<`SQN&kVj-YoSfFlrU_(0TML6<Y;'
    b'C-'
    b'Z&gYqT@M|y{UA>uA}a1A)E?S6W}FyZeo3g}eb>&C1+<9AcD@P0nP9J`X?EP=JliIEMAfYwHl&dLkI^#Kz?NHb1hZ>M<S;TsGn+eV'
    b'OVBUoEoq1hN5t%YSV0Z<O`POC!CkOiI)T3F8%o6209Zqf@5b{yG2_t1NoiGi}p4A$U%G{q=9a&9ms^B(AY#_t~NjRi?~MF0RGHJZ'
    b'Djk>L2|GvJ}{%U3x9<`|!VBbfCLzkKlQ21f!fqOc7ZKsJG1s0-'
    b'Z>soI)>LWuUsAU8M;p=07V<zYl0)22x26yzPMS+IdDd?6k}1%F#TWB71Q*(rP<FcQXf4Qg01i1^l@2!{+h8r8z331W^t+q9?gDBF'
    b'k*8KyL|p=Gj@f`f|vO(6{Fl{@N3|ANdH`@%Z5PBr0Fh9!r$$F}2ms_89!aQlW+fhs+ry$=@y9cVQCp6H0d*k~v=udlGxHwc{pfr>'
    b'dR+q@n3*-'
    b'*RTik`i+#U!!=F;pYS(_o2EfF^a|w+w`Ol&UXS=q`2yBY;(1#E(rTc`T&i1>w66e_^CUFi9FNvo~+liD4z!U^gI9EcHqN`2aT*C+'
    b'PINW*;-SLe=rWn8=%D<GPT_3<7Z@oz^#wUT}rO8k1Thdtu*+O0N}=!N(ry1f%$g3S<Z7rV~~e6LJA7;RV1JT%dE-U_SJ!zz27|<E'
    b'K1b_ZBR-'
    b'^g~{0<qQS@IISgHc6emBOf{ktC=JL0VrcL6^c;#XaIHiXV;_SEf<jUZbcJV?Y(v3tua1u_$FM<qmEvIEOGg~!1q0@es0ohoF_25f'
    b'mWj85>uiP{W`2f*ZeW!lTNbZulPFNP?ib+$RvdV51@%zycI=6OJn|x6Lv%qLgg!VyuAOM-'
    b'7tgl<C0dH<c<i;H9S5NXwVU%}K?Zo{oos*sjDY*W0HY3XF<Rwbp~%LoJwHT2r=z!#ImncH7ZApi6f_aWKIEW@^}#75+%}X-'
    b'SJRm*@kX-5dJv9L?!z%e&9OvEIZDmPkx~xMI9bF{#EaO@&_LpF69R}q5J;>%S+j(9SO98C3lq>{-zf&nmx6&-'
    b'E7`+GC_`ZD_6Xn$Vu7Gbeh^N52Y?g;U}R$5xh<l|yu@(a1Iv*O-'
    b'~<qTL%ea<5E0e{PZ(tP`Wt2r2ajE*J`>Jn#4D_MF;pN6GD4H#AJRJV9vVlQ!3|M3c>jSWFi9vcwiZE59DNc<i91*kT(r{WjpgRWx'
    b'0gBdWv$_hbWhibCQrj1K0<CG{=!d<jK`2bC=EiSY6bb^&>iZ)%r1<x+=9LgoFQ)e+0DjDC%n_l;Q)gtF>W4ikB9+feJ~N1BnAEf>'
    b'm=3zs|Z1lXzy>H`nZ?0f!$$Z)4I?#+c_-'
    b'+S9WvSQzo;CK+!vlL>L9kJ2kNUARIB+;vo)94<3zl;snJjk<980Z;Sjn9s*(tW+OZpEQqbe2aCR)GGr_qe#FsTd)xwHL~h*G(DxS'
    b'j3B%PFR7J-'
    b'yuJ9HZ!OKHKZ@Nq8I9_kzM}dzrBW`Uprfm`U?#JgNG#QtIe`gjl>yTgg=6)|;`1+nTFmT2u|Inj?|7gj;FhL*QIGbH2JWbpIO}HP'
    b'=<AVe4{f0z>F)D-=@yrYgMwQGPmm#C+Fbb-;+?<GH4VGr=aL{C-'
    b'PCUyk^`Geu)j@Di+?>EKnDe2C6EgkjDFl^yB&?;kU;%1HFdDOt2)GaX?TJ05!*SsS5}=9tfi~sFgT~d)!OevtwH?_6!6mWw%uG8@'
    b'<RJ?1l1Cw}VM2i^Hf<7$m}tRJ`366Z0Y>sRd_qTY=(gfBDuAhbI+cVvLgi3n22uzsOwcJ9y+&Xa^94MC%*A9tK8-'
    b'PxL743=l=fL>#$5!_CvN{JV9N(rvq+t%-'
    b'btJrdDBF}iEgi?B8*rV6lN6(;n_zuG3Xo0hYyWIr$a2F<$%3G;g&HaTE?K(@DKvu$e$a(Y=T_^s82{-'
    b'0!kpWLHYC(2QzCHxXR+5rl6vjH#oM3#YgSI&FYwr5ZL)ZlYmO>cN8`y(B@|<$rBr=Lpavp7+WPA+t?!#J~0S{;<Vcx^Q}$d=|YC$'
    b'4c2@^{MbJp#Vj$8BP>lh(}C@xE_F2OUpVO9i#f9O-a;1P@Twvi7MhJg!t`kk_XSK+sh5Z|iB#wpT<+v5qD_K{I)>xH6c|EB)A-'
    b'beT~I!}WY^-6$-`FxF2=CMXK;?zxO1Ikr-YgLX|D;6O6)EJ3ed_APr8XS?hFcVAY@=tfe#Lc-'
    b'DYw>Wy4&dnIpZI3(RcHB<fEE;jIOb6%PoIp<Gx`I?mEoBy%heHk?G{y~mB{>qK#UtN?c_qM#5hc|vF0JK-sW+*ybUR0VcrYXrD~Y'
    b'bYfy`4R+O-'
    b'gF0_;3edSJP1UjXiaoNXwyu1d<DBq<t>r31UWTC0J|Qv`CfILp_fuErUf{n@YrGr%K$#WMb^$N6&T9N8_IO#MFcC15|~eKr;H&2K'
    b'ZNRtH}r_q%`6k=;o7)!quCdL78=}r#4UXocqj!9S?P5Y!TQYL>b-'
    b'PMm?QhgZ4LIO6W0zTjrk`%07|S^WzG(18pjSPJ+(1P&xuFex(`|;aq;TKpjyQ`#YG}M3@%!mRF2|zfPD5@kRr=GhL+9W7#5f|4GK'
    b'#5+TgmKxID*}Wa6INP`U^s0|TH>j+hx90IY8;3z`%PwBwEebwNss<*e;O+u?gic02BJ3g!7!p8=~UVki{(*rZ+~DF^w_j2eP0@_&'
    b'i2Ms^@2k_^Zz_<EW6U0e&HgYZdR;8=O5czN8mct#qS`gyTL*t}zvK_c~p*N^0TC&stOmC-'
    b'5Ia|t;vIN+zmD=v6oMTY>i#icJgL1IDf(PMTFVZmc<3M}){3)}$4xibw&*fTf7<E|)^QRo87sf1k^7@swc<+&nEa0Id>{LP-'
    b'@A`frSW0#RXpV~mnP#Z=F7o5VBEsPS|VI*_w)#HK+bIR+MdvF|L1TasSsy6-gH<=_fB`euXiG~Tf3?iQ(b>Xr(jHe5qGrQm-'
    b'p?pMX<Vvt%^}UjZj+li@yWl{y0mF$7z|2r>BKO?5s)x+t>gROIbQH~5S?FPYiK3IqqD4xCCtWkD1{&Z7i~~;-'
    b'as7HsAxjqs>o&|~iEk=fe(f~_fw5=y;d06cbmLZS&{SmYS|lDkRVPdU@t_f2;2;iHUa`$jp2{h_c!tXO)<{GQL?L)<!9E;kvQY?A'
    b'V;Xyvgx7!w??Cv`@b?xH5D@-wLOH?;xwb`4iUBT^Rd0`5=JRnT7NkM!%zy%3B&3ym-@o0(?f>Fc3HioShw-Zu8yz=B^7(_o2wz1='
    b'Z@8@Buei$15&@+>hhkP36~k6+6p~Pm4^V)iWZ=1wtsRrr5gU>Mf(L<O#x7NaKI9b`&|2XbcpMoSATp0th3#>2_=j`FA73^HQAlE-'
    b'+)OI=CU(`*dntt#g5k+3o%0ew32~8FplvG+j-W&s!%51yV#xMEWhzm&oQP-'
    b'dq0mM=hxO<)3N0w)X^?YDk=OWvl8}Ko@7<)0_=^LPiU2^uk0|oyDMCtI%+ME5V>fFFnPbXqw-ad*y@7iRRtcL$E`XX(TvHHJ&-'
    b'=H#u}~B03Me}*ArgW|(m;mH;{Inx&S#!OwuOMnv>(dtdI_RZUSr~fbL%bR=BVq$_Ya&^xDFitQK$5qK0r!*bBwdHUqp@BzT@*J!1'
    b'LSx0B6>nPX'
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
    candidate = starts_one_ends  # noqa: F405
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
