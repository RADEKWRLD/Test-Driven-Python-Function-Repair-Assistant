import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[''],
 ['three'],
 ['three five nine'],
 ['five zero four seven nine eight'],
 ['six five four three two one zero'],
 ['four eight two'],
 ['nine'],
 ['one six two four nine'],
 ['two seven eight zero five'],
 ['nine zero'],
 ['seven three one'],
 ['two two three three four five six'],
 ['zero five four one seven eight two six'],
 ['nine eight seven six five four three two one zero'],
 ['two zero nine four five six'],
 ['nine eight seven six five four one zero'],
 ['two zero nine'],
 ['four eight'],
 [''],
 ['zero five four one seven'],
 ['six'],
 ['two two four five six'],
 ['zero five four one'],
 ['zero five seven'],
 ['four two'],
 ['four'],
 ['two six'],
 ['two two five six'],
 ['seven'],
 ['zero five four zero five four one seven eight two six'],
 ['zero five one seven eight two six'],
 ['four four eight two'],
 ['seven three'],
 ['nine eight seven five four three two one zero'],
 ['two four five six'],
 ['zero four one'],
 ['zero seven eight two six'],
 ['zero five eight two six'],
 ['zero'],
 ['three'],
 ['one six'],
 ['nine six'],
 ['two seven eight five'],
 ['two'],
 ['two three three four five six'],
 ['zero five four seven'],
 ['nine eight seven one zero'],
 ['four five six'],
 ['two nine'],
 ['two two three'],
 ['nine eight seven six five two one zero'],
 ['zero five six'],
 ['zero five'],
 ['zero five two six'],
 ['zero five four zero four one seven eight two six'],
 ['four eight two two three'],
 ['five four one seven eight two six'],
 ['nine seven six five two one zero'],
 ['nine eight seven six zero'],
 ['two nine seven six five two one zero'],
 ['two four six'],
 ['nine one zero'],
 ['four six'],
 ['zero five four'],
 ['zero two six'],
 ['zero five one'],
 ['nine six five two one zero'],
 ['two nine eight seven six five four one zero'],
 ['zero four one seven'],
 ['two zero nine four zero four one'],
 ['one zero five six'],
 ['nine seven six five two zero'],
 ['two nine eight seven six five four one zero one zero'],
 ['two nine seven six five two one zero five two six'],
 ['one'],
 ['nine eight seven five four three two one'],
 ['two seven'],
 ['nine eight seven six'],
 ['zero five one seven six'],
 ['nine one zero five four one seven eight two six'],
 ['zero two'],
 ['two four zero four one'],
 ['zero five four zero five four one seven'],
 ['two two four five'],
 ['zero one seven eight two six'],
 ['nine two six'],
 ['nine one zero five four one six'],
 ['two two seven eight zero five four five six'],
 ['two four zero four'],
 ['two zero six'],
 ['two three'],
 ['two nine seven six five two one zero four five six'],
 ['nine six five two three three four five six one zero'],
 ['nine eight one zero'],
 ['two four'],
 ['four two nine eight seven six five four one zero'],
 ['two two'],
 ['nine seven six five two one'],
 ['one six two nine'],
 ['zero five four one seven eight six'],
 ['nine seven four six'],
 ['five six'],
 ['two zero nine four one'],
 ['zero five four one eight two six'],
 ['nine one zero five four one'],
 ['one two three four five six seven eight nine'],
 ['nine eight seven six five four three two one'],
 ['five seven eight six nine four zero two one three'],
 ['four six nine eight seven one five zero two three'],
 ['seven one zero five two four eight six nine three'],
 ['zero one two three four five six seven eight nine'],
 ['two four six eight zero one three five seven nine'],
 ['nine seven five three one eight six four two zero'],
 ['one zero three four two six five seven eight nine'],
 ['seven five zero four nine eight two six one three'],
 ['five'],
 ['eight'],
 ['four six nine eight five zero two three'],
 ['one two three three'],
 ['two nine eight seven six five four three two one seven nine'],
 ['zero one two five six seven eight nine'],
 ['five four six nine eight seven one five zero two three two one three'],
 ['nine eight seven six five four two one'],
 ['one two one four'],
 ['one one one one one'],
 ['one two'],
 ['four four two six nine two zero'],
 ['nine eight seven six five two three two one'],
 ['nine eight seven two one'],
 ['one zero three nine'],
 ['nine eight'],
 ['seven one zero five three'],
 ['zero two three']]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-rlnJC<cR5k<j(kzio4LZ8sb>xp0}q|j=g31DHhS&Wk@u;Y>U76V8R3c9;iX1@C*MZ`J#=;h!4@Xvq!>35$$fBo_2-~RZwUsu-'
    b'l<F{XW+pFnaTC!hX`Sjv-Tkc)&Z2MYMIl9N5$E**XbxFE)-(gnl`j3D7`1SX{{W6;FK6@&;+16EiZhN}VbG#;(q^GYcP275(v-'
    b'D~wt+K7na@zLv^_cB*_A1)^xSME^VW;+eY*?=8vpC(Rr=-oFwKT7@R-GxUjorT<Q&Ng=Y%j`xdtPPL+q=k+(pIgd<+;;H-'
    b'j>haq?9u|Z@uasa>{;I)0gjah9%p+*x#74`nIm3S@hI&ZK=$h>XCX@G4sLhcb<KeqtDsw!m{fbY2`Hc%`)y-'
    b'DQ)+W_Pk?oZnwwFWessT^<>>5*>g+nIU6=19DWn6c8}JvN4+PtEoIcR)3nn(jYVPaI(0_r#wt9%`OW&QhIcrs=Cyd?trm+(-'
    b'c|2Tlx5qrQEipx+1p8To?4sivqzS0HQU!?`YxxIn@e7~-`j4|JzH+KO%DH1^IB`J_iE?JvYoRzuxYc=Sw-ck)YM%3TB+80nJjmnR'
    b'ycFHqMSfg?e46XJ*^_tqotCh_1)&CO}`!^N^y1-'
    b'XW8r6OnsiKgY}=B*6~#vTT1B+N`KaLVa;>0pH)*H=j$<bjwF>P>3daQt)G7RTS;rVx6WTm9sTI=Bf>kDBgc3wwc2%zXH&hW%f{%;'
    b'S$A`7>3A-)*64TMm(%Yh)jQ6OBR1JIJZs$Rrn}Pmddy9I$Yc~`(7%Nrn06)aRXSsMSF4s!>D@H-J!5KO6_g;)B(~?*V-'
    b'g#wMVOewl#Eik)Wp6Di|Mv&_R+Fb6JI9uj`3WEaJEx)r}P{#U(|kiyi@E>Vbfs;g-OsBgS<`|E;-XLyu*$aCuXEGbNs-'
    b'0&Zf~(OEob&l8zW{-?VcIcg)=yQ!E?>?PiCsve$9vmK4>HSxWnQj57y^0;Hz(%-'
    b'Uy>I1&zX%0W~TCE9eZCZh`J#^8?JQ(oGblKWKZd(^MdrIYF2s0C}!=lWdj3RUsbj#~24+U_+bF;VxvD8y{^V)ynQF}k>toO>B5R<'
    b'cmZJ;$o%4S`u%Jder?JzrPqnHTL7av8%p?z1V&%k%C%r#%$0Vs2=gGIBba7?XuiXI-'
    b'4>V4k<`t5aMTI!c?@xBXb!tt*?~zP0eJOc$-2GgU5SO6WbKz&W(hTC<bK76gQS-JQp)#o4=`aT*=gOFJ%wm5eiHslMr5M4VynMO#'
    b'm`3+H#~fqO3FQy=v^+IbHb+G;hrZFHkI=knw{tPj+y()ZOmGlaFEj%aRir6fD+GvP*SNFQ^wQrBW0G`W?LisA&G4{t27$krDwv+K'
    b'>KjlN9A^2O^j49G8~$~$*zg@Kh^3~R|qOihgbKIj2e;w0|s>DZ+{%LfJJZJ)DAN~@}m&Y67FLA|yq<79Lz*PPe|<Eyhw{$P64k?F'
    b'Tv`ZXJ``A){A;V8{k8?~}_gejz9Fw=+;!=vbw-({E$Q_WOW=4Y*ojy|r5j%-'
    b'ApamlW;mFw<htN2)c3@29OyQuqS=qVCie2ZRc#;eA7x>$R1jt)0K4mjOJ%f_7X8slsVriDoOuIJ`9yjQOo!{Q(;I`UZ!Dy1#}M5v'
    b'SX-av~Gf}L{9Hm16@tJ}p81__Y3_y}Hu<O*u?oK0o`k5Hj9cbN9&ZSc>63>n@tj4!uK)!aJ;V`H=hE^z3dRLV09j$n>4^vpSK8Mv'
    b'A?pJ|2)^+}J=;w-'
    b'~0v(S@l?WASPN{w>tr~Rbig4c8=q`xaOlVTp(**g4d^lVg%{l&a9{+*4kc@GT{4*2>Mn&>FywJgPX*=gzGn^+RfZ20)4Oxig9?ex'
    b'-e`i>g0$SF+C*JCnL&!A*YA+6aMD)g?c%M2CHiDqH!8ET3~@#(C!X$(#+(@*kXQb+lOJ&jU}LTZENV})37O$xI(^QD9DB_?<bsBo'
    b'b>NmA!H@Vuw}I8n3=j6kx{=$&XmP-GdX!#r{7rQn>i7lgI!jyzLsW?|4q`F<~nE<{w+@qnb^iuEuP^;8MjI=LXKV46W#$|<92G_V'
    b'iK)G$9^&uH!j@fc!xz$_pX!5IwcmW(a(jya45jX!g*i7)!j8L`KLbOcpAXJa=Gh9b2LEh+>`!GX*b!@!U8N;U(3!8EcFQ=^(lb%1'
    b'm^&oIzjlR=<VAA^N%7)>TiD+Q%nQ!W9VAd5992=%{|4%)?jLy%ve!W&0}%Dc0jOJ6N!KERcB4fhlr%4}YkRs+2*?8ka@p#t`hDE='
    b'b1-U>$OKwz;&qyylx-LR+J#nBGw4xvT&bOuW}%5|6-'
    b'e(V`dh5>En?XV}kz<dV>z$gy3VryU}D&G;mi*cX@fH<;&(EtQ+^edvkd#0NJ-'
    b'~bT>Dqe97%SSXLZqPC)b*K7uwFHnLV2l>?UE~21x&frv4M18mJA4FW-aCM2DuN-?bZcS$A%QwF6P5ii9|#HGd(^LD)j(5505-'
    b'~hRtmafdT^y<AHkwoaYJy}3P#obgSH3~o!IpSlOj;S25xr3;KnJ?7sm{K;XRcEVbPPDiGvxt3CRfN+{7<B`#EA=AS;E05)HW-'
    b'J*WUl!3J*=n%-dXjue%QWYkmqTmY;ny{YzUF>J$z5c-'
    b'%%Jf=8|(mnG65D=ik)+W@3znK)Y4Ua)trZIww=DuA_ri11JB5NlPhKVmmbuqr|<W|C>3dc8ij}@^madyoHk<VUCirxYp*Z{lhgdq'
    b'fX<w1Ij1=0F)3-CZ45I_US3{gV^pf+mSo=PPGPrhhkw8;IiBl<&F!(&@j;^w8vQ3`?>_-'
    b'>zkMmzhRwEey>?BCH+oxpRmYa1I#Xw*TS(7!k(K!Xs9zE%jFh?zlt*`U;t{Ngq2LeDznbkR()=upxC59vI;rj3h$-'
    b'N7xPYZw$oYeB2gw6DP&<{*-Q9NLH8WDFSpNm?MkG0r&wqlU7?c+P5662C$N@Ib-Wo-RhqI4)+U(>55Z4UW~qf>_=_DA9{t7yS<dA'
    b'{l_F(cv6UBUL^}EOPmSL4xv@Ns2VzoHsi*3yInV>6n9wxDC=Iay(<0GH-42U&Da3K>)mjZP5N0A`ndzF)$rUWF4?KNu2GWy^-'
    b'Rsbf8M{)4HE7&L1ZLYBCu(qhJVV$Qt^Q5oD5FM)K(zh1xV!l5SyaKw?DmB??aVQa7Gccfl-'
    b'E-W4h6At=acC5IZXRHP&%xgmo+1ubN<8O{Cz?FpGiQxF*Hp;CdoOgJ8-G<b3mxA9>NWFz!QB|k&e*epq_mDj_`>U0+^5nf-QXJ~h'
    b'k)^-a7oNxkDa<C7My@c_^w1Ug=y7|)9Bs=@0($m?Q8sx~xb$ASyF7`?9jx-'
    b'F7&~bAO`weWHSm1i^Z=7TAk@^bC81Zn$+ZWun84e2*Wtg3%VWT{9?}S@XM%+1WBp#m{4IPSvOqWwFvLJvI2acgpiOrh$7H`c+r<i'
    b'M}B?T~CfMt6ysh=>N6!s3{>x?u+QpOB0Asz)HAl_G48bULPp!5w|t(Tu?a2}#K=7*3^80O)?ryWP>ActZDb&H_KJc2m@K+Fw<B#b'
    b'gV&$QR)h^d~A5kblDl{-@#%pM(rR&lhj%Hi~;a_)@;aq5okwpy!4a(nM@2H`Jr0O-81w~%CV3h0l144_RF(F>)j1kM#VB?Hr`hI-'
    b'Js&toj^5@t9aEdpnfq4_CjjsLkVMny^@5*HHIT_Tkv4bn#+(<vjpmkTAv06d3em~zg0Gp1Pi0`kx;bU1jM=oBeW@wnlHeF6%^<ob'
    b'rhKo|5O=Jy1$;}h2@Sl$OpCs;>k5khj$6yk0wPJV;)3Yz;o<}!)}Rb}m${7#-OXdDmY<-'
    b'SImac{v8kb6Kk@(w6~Ou!E*;O^;SrNsb>Ntirsk=rg-Otrxh!Z;a2)7dxU184z~%)8x2XJWuk+<hfoV?$kL&e8Uzj1@N#&^`2GL3'
    b'o62U{>Oq0-b?4=Il%f!wg0Fdkw^3Blu*zzKJDw&l~VtaH-'
    b'q^gs2pOB&>Fxw7VcBj!s8(B`7}=zGg#Gz^v`K70O0hr%P}ZEK*73((z4QH^s$csTvnTpBaw(%Xg-*K_-'
    b'Z5ri!3+2dob~c#uy56ESd*fq3BrC`c%@Ie0!3E=$L~7j`m2I5WQ1Nl|z(seFR-'
    b'4uD(>j0KADx{&@67Y)1O>MJgOIj=VeO}^%Qq0@z}cLW!!BfoTf0fynkP<;MhAVTOVjDtn-k7fK=-'
    b'T)m&3G?<GxqAnwF_S<KvWrLxKw6O1KH?%yJh+L+7s*Xzt@>y&EWRXKnB8VHM1zH3lmRWE>&ze|Y&R5u14R^5uaKdDK8#IzM)Qmlk'
    b'w7<|ufgjq;^f#vLv~4q?RH~ESl#iUOs%jlak(B+bbDQsFm2FA0b})onRIdjGx;y)5{iKum`}8xp1}|kJxB{d{fks}UlgFApc%>t%'
    b'p(HSb}hUs7?e389bo4kIY;p#at#pR$Iz038OrzC9mh?3AN<b4AAI5)DPeCbgo6i<9bvX|WSww>kC3Z?3h>b4vgPR;nililI00=hP'
    b'I8WGq=Q_sw*t2k%r{fXUcn*<euLwwH53Jqzv@Rv=J=toGA19h2beAo0j>nBf`s8CdJ>eXG&mf7O7YnWe|<!hgu~d!4bozX>`MXwn'
    b'VfkFj?v>5Asc;wYH1@olO>U6z%$dLxqt6X8}a~ZLb0uGT!`0nkQJmlEk2l`vZ#1kC~cTHLPlm6Xd~<y`Fkog(M}{AQE)g5r^A>ih'
    b'Q@VwTvl<wgOMdnA8-}GZ=+hR%nzd6&x1)*<4%<LTk&pO1H8cumK>;k^b)xDiLU4aS#A<8I{8CB*R0CVKf|!GXIhD{d7R9-'
    b'Di30ua2dS5oyra>oyd>S!f4u<h2ok3k`!mZ&Hx7}UM9?=&U~1b6IXgUwT~-|vEnwWGnjA=-'
    b'i^aD&ukrat?x`B5{@F`A$1a^1d<1d3oS|~j-fP)#D`6c29`=g-3~)HP4lz5XBdzP898o)N8E$L8@xAGMBIqGOeFMHpp8-'
    b'NNL6Ez@c{y@kPm|Ueg=cRfyD)6<{)VWYK~?S6bPNb|E+A3;UGJB)`o;K$lzAiS{dgjhb!F=x`@R^2`P~?B!gQx+_1vFJT4;vQA!i'
    b'{(})op`jD|Uy!fH5OY8AQ*!b;qOryc!G8|wrWr!y8-'
    b'veOL9}cg!t0cUI9>;jTnc*hHibzJM!jGg~z0`pdfb8JJwBxo+2!1Rht_a{t<~r{AQ!s;k_hY{06QTb<=6~!l3?0<k_~|u~kG&#cB'
    b'YhGVH86r<jp_0p5phVtolIRK2u9lfnHiu%K>_hZlox9x;{?~vxJW;%#K-'
    b'nF5cl|CQ?R(R`{(;J779&0>8_N9G=i(6Ya<N+GI3)@h|`YS(C={peB+agYzuPY%jAAC&?k>Rl3sZ&$)F*P5JcPMLV6!Kh$NwL&5B'
    b'*$L$V^mxA<I<7`StTf@^;CX2nMmaWjMP;;$JKErh%Xn1Y_{xS`w#4>1hUx-)KPJL>8USz*WDd($Sd{3+6^0)aRde90;2Om&x&m-'
    b'|GfxA27_>^(k)jvG>Z2esYly_CYv$e4#fm7%=aK>YYD0x<XZu<1<lfPv15+?V3R)Fkow%58w9KYbG)BvcmE3x||AZZaOVCE7>MTR'
    b'Juh51&m5j0h+L+nT|)R-neG;B;0)Z*SaHRVY*9moDG|g4vAEtSBC!qtM`pyF5UW!v-'
    b'DPf+Kf+H)TLl7$<uFq36xg;)4!WoM=bRqmYt-E)o-'
    b'p4yNKFMEkgU`1#>Ur?tR%DBP4@A;!Q(Xz^vn;(C+!g=e>Jknj@e3$e@4?8*^gc<--'
    b'cK!i6wPma(0aPk4C&&>IrPQ77vIts9Yizb04mT-HYzO6@keQ%Tc2EItBeG>mte3-U3|ImFLY+-'
    b'`hF{0e22U~o|dlmC_tytasc_sh()e_udGvVY=psdddwlRu<YXDBwcy`_QGDg5lTroD#ZpDX|@73yEY(74*8_I|*UUzU~G8mZ)5Tl'
    b'7R-_KJEcFDeA!q2a~uvL@&_!J?7aok20n3!w_b8tVR-n8D~E9LYtc$w-HhX57e-'
    b'9Eo8K(>FAZ}SbP9Xlkj+s10x=A<BN!=O|L()bYh-Kfi645<T5>C>jnMVyWQ<=+W+o8J'
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
    candidate = sort_numbers  # noqa: F405
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
