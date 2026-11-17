import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[5],
 [6],
 [10],
 [100],
 [1],
 [2],
 [3],
 [4],
 [7],
 [12],
 [15],
 [20],
 [25],
 [30],
 [29],
 [16],
 [19],
 [18],
 [17],
 [21],
 [26],
 [31],
 [11],
 [22],
 [8],
 [6],
 [27],
 [24],
 [32],
 [28],
 [33],
 [5],
 [10],
 [23],
 [9],
 [14],
 [13],
 [34],
 [35],
 [36],
 [49],
 [37],
 [73],
 [77],
 [50],
 [74],
 [75],
 [76],
 [38],
 [78],
 [48],
 [51],
 [52],
 [98],
 [79],
 [53],
 [72],
 [42],
 [41],
 [99],
 [80],
 [54],
 [100],
 [40],
 [68],
 [39],
 [81],
 [67],
 [69],
 [43],
 [61],
 [70],
 [65],
 [71],
 [102],
 [101],
 [82],
 [47],
 [46],
 [66],
 [45],
 [57],
 [60],
 [58],
 [59],
 [103],
 [97],
 [56],
 [104],
 [96],
 [44],
 [105],
 [83],
 [95],
 [94],
 [64],
 [84],
 [85],
 [63],
 [86],
 [55],
 [87],
 [62],
 [200],
 [199],
 [201],
 [198],
 [202],
 [90],
 [91],
 [92],
 [203],
 [93],
 [197],
 [196],
 [195],
 [194],
 [204],
 [88]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-pO*JF;y#4Td3rj6skQQMP5vR@M_CkYCj~6Cfh$@G@UM?R(Zb6S!S<x~uoY%a-)Ny#Mo;|NZUnfBO9MuOI*T<FEhz-AmISfBaVK'
    b'nLE$hyx+7(I&N3$ur$*?b?w?(s#(^U(~|a-'
    b'^J?>?(aX%zQ~UAXAHV<kkKZJvbxIrU_MUdmcU(JjmVR_j?RDn0E%&`Nk5b1SW!_qE-FIy*y?-'
    b'rpX32ZEJ@4|Jc=D*GQwL9O$?oX2^;D}b7nRk=IeNN`#b!0{EMLp?GfW5Dzv^>LKe^04)pluXUKP(H>oUnY^0eK2^mRwwta<vl>uZ'
    b'^n%1YC;om9l<IU|i*W~*b5-Li>~*-Ei_^hz$-^=3U~*X*_0lwZ3{rWjNvOWn!FthKGq$!_ACl)n^_oShS#xss-'
    b't$Mz#sam?7j{aWT1H9YO!_O;|~nX{u|Gqb`yJnqU#SC7$oo|8S_x#~?aHv_QxtsMGmnQ1xAvJWe*B%??7`<!d$bmiVWbQ>?`p8Js'
    b'Li$6KN_0s$ft>r24X74lE;t|q$a2hhIc-6|sv}nsW7nRLah#zJy<#yIAbNM<cJ>!?pxJ?IT@YQ9Dav~;0bF00Y)zU{<I{M6-'
    b'y12<MUhk>Wtjc_9bI<5q>#6K8o>k<W;={bFC05<z4A$Or4W0d@sh|DmS=N1MdmCOD6lQ(K;L4ziuFQ0qoKviiJ-'
    b'7Dla~CjmXu_P*640Sp#ouMLjbeRP*9qK4roip=T6ETwr>DE;0S9Z{qr!;Jvw6QIiU8R1b0}J**4Bz`8QZAzxaaDlx*c$S+L2_wYP'
    b'O@>$345Nm*w3ONBmmG&ltApQxQu!b>=4n(?N$*7SPPbA%@Mn>CRmTLw{(WwnlC4b0}k08d##A3XE4_?s(y{g)vX<NlVIob~@9~Ua'
    b'~1&W<+_ku6!PZ@4Bny%%RhTY3@kg_n@56nbYUSa2%Sy@6XrsjLysMOiE!Go)Yg?D3^jthH!2H1KL!#P=PkU<s4OQb%r#jq`Sj6bW'
    b'5AH7=-'
    b'6g3(WOvHdnEssg*PB3~8mN?fcSgJ8Mn$(no{ZE+px6lrhPxKDALly2gb(d%0uR!fLyjvKLLYP|=Y~&;%UH#=TI1N{Q#E8rELgf)y'
    b'8}d3N>ekce2URBu}jm$3)a92?uWFrP==YGrf^{599JOkHj~g99a5*C7$-'
    b';6lIi2N?o?bIQXI+fLF1qNENrrW2BS*l%ws<&?9UGsnllx7%>YlmX$vI__@MTCv&$jKMf&<*+|0zH9omI>kVDv2%NjRbn!EV5+w`'
    b';Nm4}OwSr4a92%by9GDpnpba?ufFUj0)}pB6X@-'
    b'Gl~c;p<iPK2b`8IGa3oYi4gM;CkfzcFUzFpi&GZV5vRL#G?J(F!I6zC8u^9~f(cBmBL)uzQ_exG#5SY9B%YN%Z(E~MwSy-J$)M-'
    b'){dXlW9K2Qi3YAs3g3L0b4*&x5+@Yqx08A=DSkJAkV)Y%t0wrDO>X6j6)p-?$#9ff-'
    b'9RaAlEf_Y#0*Xq<Saui_T#8<LVxLqrH2KAn*w^4@vlcM+^ktDY5Sh03JpMFCO%ENwW*w}~Noe{fF<y`of8Xorr^g`b|CGHN-uG8j'
    b'(oL6Bapm65vX?Q{vgG25FTMA=X-H2`N$WpyGT|muaM(NlbL<sRvW;3{l+C8)dZik-'
    b'a=xX99t3{_Zj^b!~3>$jb_jVkLEI6aiG4LN=E{C}K${oxJ)7KT^3|O4D-'
    b'`kVqnCP^0<~Ce`=|PJ*Y67nCz*y+ue2mF4pGfVnYd&Ja>zLBJIV1}C>gDUZuffzZU}xd)ATMY7wzKJHH|(L8ib0yawSkIv0LJK2A'
    b'y%iU%R(M3xI(sj3|UX>A`(p0d`f%^jkJPmXbWVwnoEpF?;g8jBRh})Gy!HhU>+31?o?X?#n1S4fnSnAayYes!l;n7KnrY1ol>?bm'
    b'^`Hc)U>&pCvDI<b8_tIRM~qVs|bI^B38Q3zi$u1Yh}P%8F#QTDWlROKE^ERoeaA$@%h2jKFCcSv1=F|pE%Kw)k;sLQpqDZ_F&8+t'
    b'`Zw{kX&il09@Si*CsKuYH~^rQ+<`~8%~<$ri%M>&nr)Xj^RYK|AwVGm5<}N;H6{lGSCh5GudpFy<<<8S-g;E*mMR-'
    b'C^kMRY%UVjr?3@1)tDZ8`DOuN6{BF_TrAw~hR|1I>ToEq@1AvUz`Pixgf#lB2u`MM)gMalgM~XXp73(eK$8SnT8GC5WLJ;p3Qu?u'
    b'h0Sbo-ZC&n($EaZ?XdzgO$-'
    b')bh1>`qIGMh21t3v#32wzYI2IxV1X&hP$KnMJ#NhYGn6Qu4POgoDw9NyqhQsgpAYGdpMu6C~W!K(=C54Ew+GYJYhdf}QUf%rBO%B'
    b'7R=cTUM%18_NB^(hlxg&=_#--kc-~EvPLV*1R182flpAB<D10mmo1CHB4FV-JX)kqvzuZoEe^Vd)ZKOV%0lX)Bkcq%jz3(HJmWlh'
    b'+4B@Y#rPdM5Xijy!UYDlxWA$NAEJ)Gfhi93iv#jB>YaTAo;2nm?eN~j`%uwCdAC^W!}J;g&~-'
    b'X=hSpW8#})j2#k!j(I%ObJVqC~J_9gR5Tfqxj)<7)vw++oZflmFH;0uV)$HL6<HLwD!|CU>Hy&55@Gea>lJpV5ppNn}g#ORf7>`E'
    b'v-'
    b'M$#2!tItJDRL1Y0_$EX4~b>q$&;BGjUhjfSG%SZHA$gJ~;keLD(RVB=YF;>x64vJa%OO86bcMxc$Tfn$*=M!P6z!*un<fLtu_Gk%'
    b'N|X#sf;Kw-on$_hamIitfhY`$y^dV*w_;43->lZTp-KRNhA=~#O9cM!oyxR^4$0egpX7p??<LPCOInD9izL8no)rYKfv<)&{7i6F'
    b'}SECTppNK!ib$y^`Q7HZ%**e85Vfg8P_d-'
    b'9@j@DJAKzGnXz;=yphb1uZT49Q<)yTe!*oOK{^Tmt#XrJSHbWR83tUTCFXd$~}7$BtP*yGeng<1j-'
    b'X*uq6>TE^iP3^N<aCDtflIjpNlrwsW80|ta<NXD<D9Ki7iCgR}pE`YBQlfvdMFN7eNbHR#>DP#BD{aFU${y6N#^bpc<1wUb$*vLM'
    b'R4UC0@CypTV2lhI5LGF+=j5J<j65LI$qt6{MFt1x(z~KZQpwJI)An))GsQ2k}1gjqW5{*dmA{@aa8&lFlHs0L|!HrqQK#nd@9ThU'
    b'W&4>`#^~<ne4?KLTC+6@G7^|QF&ob(r*k;7z+?XGj0;aLs2M1Cp1KR?>5*{;wEUgH`IIAa5@kjwEQNDeQ;kaaH7?%d2v4?a7wArf'
    b'<I*^(&(TSNQhLw$HeJ~YuAWET;v;u?H8h$6DIFy0ACj{*XKDc|zsv#tX$;M0M*uc|pzMLV41MewjZV<*W4Ukzr7%todBeLX>KqoR'
    b'ml!+)!f#Ci@Y_r#GUD&dbBE*fR$Xbw&aY({1F8yM|_JX}TxaW1+ANNyeOTg=`%^?vlMdKwdZxl;a%vfOpH3&k&FH$q;gRBJg!@~r'
    b'>8uvRn-0gRs0@Nt=Knc^R)G`yrE8RgJm7s9Q!_ogVal3JOQRg9uGJe>|hbYiiCEHmW7yz(SGmnO?nYMy5q_{2M6J!U*(nLu-'
    b'39AlC6efDVwYfBs@t$P{&KrIQJH|Ny(W)FU1QN!JYa4`#Z6-'
    b'q+&nAYCRv(0O;N=mxKpjDM0wt#Y<^+~=w~8N!VS1PZcy&aIGv+c8B!mHbi2@bCI>!|cl+WQ{0&0Ub&$yTqS3RYH55wtss0PqOeZq'
    b'x1ng5Zy$=qtq1f_$QA4D`vB!Rx&##E%ZNX!v3V@@!W(gp*<*;p6kjrv}72oM6(fSZ(YFD2zWtcEla`zjW_GRuH+?!t79Fokjb1>4'
    b'cg?<=x%gsR7hJ6QlyCmLa5*>M^<BFu#>P);ZeRgeu=rwB}h6O;EgiBU)5b6g)5o)A~7eXL~!J2+D_(scPm^AA5Fa|VjZI~_Lc{`w'
    b'mU&kQZ<#P@ChPSDHY{u75ABZ6LKcKGX+s(A=92Bj(vexJ8fiX*2Aq!ES;Hiyg+Gpctpd3PBj+i(ls;V{E}G4{9=Obj+;<~PAmy%I'
    b'eEpbE9*OokcEzTij*^F`6y#D8KI&{ZN+yFG4CFfi}<<&6ckV4y?=G9FkHbO1S{H*6lLZ%__4U<hZke83>Bi?e4tPxMHOpu8Ej;7t'
    b'vMrad#R!eAv}*mLV6cLp4<wr<9sUQ8Ai2k*=@yvt0<1=j(xnT>`(dWlj<9v#_3W6}SL0;R!Q9@kD2%{VwV^YvbWv+K**@h0dpa76'
    b'AeojY+K2Iu)F)4>mDDN*9!&8Zel&(uO2^WkFh1~CU0ii7T%dS_f7uOgm7-'
    b'a+Rm(~)pkXcId)nRu9}6Dt37%1b1i1v%56aqy%&q9*)|pGE=*x+9W(W9chof6|AASs18;ytmibFF-'
    b')#MMJcYElB^tgdQqO1jg88HihYc2Q*?t+^j1q9{uX?)heDZ<Fv{OuZbA-Ygk9z)R8bsjIo5nF5yDLlf-4P-'
    b'?&I8oOBuQ_+<>xZlm)Bl!(HxMk2-V<u%FdNwi=aUGdlnpFzi0l9Dce<snh8aj!;j1-'
    b'bBpDM7C*b=f319H8Ux9P@Qh7VI>Gl%P={xM3-'
    b'r;ZvK4nfQeT>NWEQA8u>}jTrMVE$AK6kEKQ8ZYcLjxKo~p;sBE;ddTr6Vd!*&&zp!2WH=@lPPW!N#?ixJK<IG$u0boXL0lwQS<j('
    b'J@!0d#AoLrCoG&hv1b;&|hZkXPl#t#N^)?(1<8^EzWJ%OvyWh~ne3HP3{hV*<7#8hSHby79larBb%zbn@1wJ{L6_2Wq_ri_>dI%i'
    b'#hie;gh~tfw9O*UQE1M(q@TV=nKn$mVS^ykMUcN8E;Sr>HNUp>L2q5G-'
    b'ZkuR@#qUS78^6L_ZD#wN41hIv=DlPD<z+w40dm2>nsIrPOI$b)jTpy_5nxIvrqD4Z2UY5a1R@C~y!?J?YsK$K7;CBsRbYh&4Ai1u'
    b'7hcsSx$7OMy7UycW-FpTUI-Jzo*tq=%z9?(Til)oukV018TEeHrBPv{a~!J+2Zbq^rQI@{iwm&lN<MxuAT4OPS{y%k!C=Kj`HmYZ'
    b'9RJOci6}&eVUwaMklu}-'
    b'vUd2zC*4)tUWQefd|(@?7m|U3$r9upuo<_Df?bJFPkf0BX|hG#<R|jTvrL=uo0Y;`*L>b&kO)yX6K0TsHpzH$Q1nz3LJYg0k)?(s'
    b'$s_r@43cgH-'
    b'y65Ro9RQ17bXN$9+(+x`}rZv*bR>2;OgU|O><nwV0Yh6jcieKh?SY>D4Z>b3Y9H+FRPSM97NB;7GZ%^N90gyxNu1iZ5dqB!cElJ7'
    b'9c@p6QmsO&w|JC?r0V<p+O;dng;&R2L{p@=Ep)p`V^I_g=t7#EpC?A$DWZ%u<3%mHh2O<rYLLtd<JA-WjM3FS(8jNDh7?w3<!RHe'
    b'hUM5PQ&>VUMVg0nE`$%Iv9-'
    b'E6f7_!^?iHoiOOP{HSU1WRZ5IkA&U|7KffvxmI;X@`a76Sj*(Z~F_X=Z_WP(N=^w9$6ZK7$f}S{aT=x}3y&{$d8!^v@ALen4Def3'
    b'dtT<i5zP;%Vk<|Ew4djIMwT&%Fc;B_8N?bPgKoXG)nIn3{4mqvUUm+MjyV-=O6u)kj13_xsc}hnfc-'
    b'W%A@l!_4r1^t;!iy&9;X03mFQ60;Q4lBzq>@p`!mc_r#{<bPC>^eRmB~ZlrzM><jm*bS*eC8tKh1b{!;}rdk^^mWg>dFUw&Y>VtS'
    b'$k#j2jUs5&%Y2;|?3*?{RhPA55Kp{vQkJiaY'
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
    candidate = get_max_triples  # noqa: F405
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
