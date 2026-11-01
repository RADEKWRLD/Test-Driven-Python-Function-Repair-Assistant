import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[5],
 [8],
 [10],
 [12],
 [1],
 [2],
 [3],
 [4],
 [6],
 [7],
 [9],
 [11],
 [15],
 [20],
 [5],
 [19],
 [21],
 [16],
 [17],
 [14],
 [18],
 [22],
 [10],
 [8],
 [0],
 [12],
 [13],
 [23],
 [24],
 [41],
 [25],
 [98],
 [26],
 [27],
 [82],
 [81],
 [80],
 [40],
 [99],
 [83],
 [84],
 [39],
 [100],
 [28],
 [29],
 [97],
 [85],
 [86],
 [30],
 [95],
 [87],
 [31],
 [32],
 [33],
 [34],
 [42],
 [43],
 [101],
 [79],
 [88],
 [96],
 [38],
 [94],
 [93],
 [89],
 [92],
 [37],
 [44],
 [35],
 [45],
 [102],
 [103],
 [36],
 [91],
 [105],
 [104],
 [106],
 [90],
 [50],
 [46],
 [49],
 [51],
 [47],
 [78],
 [77],
 [52],
 [48],
 [53],
 [76],
 [107],
 [54],
 [108],
 [109],
 [72],
 [73],
 [71],
 [74],
 [68],
 [67],
 [110],
 [70],
 [55],
 [500],
 [1000],
 [999],
 [998],
 [997],
 [1001],
 [1003],
 [498],
 [499],
 [1004],
 [1002],
 [1005],
 [996],
 [497],
 [75],
 [61],
 [62],
 [63],
 [64],
 [496],
 [501],
 [995],
 [502],
 [503],
 [66],
 [65],
 [504],
 [505],
 [495],
 [494],
 [493],
 [492],
 [1006],
 [491]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-qaHJ+dafZH2AC+KH<axk!-'
    b'UPv(s{AVH$OTpLj2Na1KlT9_VmP4{R46Ifqz=ic}2W`n>v&tdCt|M`!9{?~sz|NGw`fBE~L|N6%gZ9o40KP4r*qC>s+baM9L^X@J'
    b'Ew!K@gJKLGLA8UC?9X@1xtzM7YY0~?T|NHUBpW-q;rLKDV>HVH-Qr2BoM&D`o)rQUEcP4%zS8l)7O<UHwl6Rl==VgYTl8)|EbFH<'
    b'UHg}!g=e*t9s(E=WuI6rc4dpUd#58%CsoylyyPBi5wY2A&W$!a3^;22Fa7(v%HLKnD)tWa|nZA$7v?A5IsEqvcGP#bbXXjE+nq$|'
    b'h*4NFRWNzvvQcBLN*uC2lx69+KTTarklUVYfm+>Qm4{06Lt82=2<)m7+^_Fy5YrRZeNBh1!(CTOL{H?Y=dhRO!FIQuCYOC`uO*Nm'
    b'j*m^dAF3H2o$|vpRUPMn@ZOR>)&!>@c-?eAG?}iud)O{x{dS$Q?S-'
    b'A>bR_1BB9G1|REIK52N&F(a_{zJKQBSMutxaa#X{eN8Ja?5tJ4@x$CDQ|oT~6sLkEti+xPi?+s%xL#+`bYI+Ix+zyKM13qIfg6zS'
    b'Ofhwdy>}bSpf=?ZaaTQj=NKuZr!Tm#LKvSgF)I+P${9MY*M>TBt)gN33tLm^E5>)#ciDbz7@>T4j!}#L?H*nHt$zU1}7rn9WiwQ<'
    b'}7k@G#8k)ZDop7xudQw5_eQZ!~|)gv-wD%puvWoy-L$ZO4NQYFek=#?p7`<7V2lpL=vo)$9ANX)EiuQ=RIhG1$R0v*x{QEXH-SMY'
    b'ClzA@gv$WoYwUbF@t3U*po4{q5pp!%8ZRqSJTP^w=8SPVrmY(CJh*88e@k$Qe{sG6GO<N&C)UdPBt<6F>zLeM7sfRk$W?n^1_##d'
    b'#n_KJrFwR<Fv8aieB-'
    b'`R%(??rYXH=2oTmq6YL8b!s)4s;9du`%_0Y8HmiV5X0J?f8=E4Q@`Em>|>OlC$77);GWiAGAyB#c6MS>GW*n$+01^Cv?YG??*7$A'
    b'cP;TTrT9f<sT_@_mgMO3xXH6G9p|EatB!JLv#RNKn(Vgqo3;4&IKyvJzu)8xRwm^T?W}5L)L`b(_81h^c5etE^Ki#O1kaMoOpeCl'
    b'o$l(C>n$-`Q{+&CQO6#uGEA=g(3ewsD&aoX%%KlS508_XmBY$KXpd{}YR2hE0?SSerE-~@8e>E;I<-'
    b'QP&uGFA)W!@c;y=5m6d9d?ejiHGI4x9mo-Q=F_EBWv2|ReG?8d_gy5Fx)oxK+t&r%kebjq^#p-'
    b'SbCGn$Mm&6o>R55<w*5L23&ah^!Y+-'
    b'L8L0&Qe%B;>6ORO}TBzspC$K6>an7m`e~BReOttrZn1H<wx1+efkw{|!cvQc~5uKD(PGTjkC(wM%6RMy7L)a<Q*t#iJe0X8sc{XN'
    b'9L5YO`JX%GbY5I7;30<VH#MJ(wfwSV!C$)`c3&)II6ofll$%Y<#63E6un3E%99Zjmc~tMmsIb!WQ^xb~YVx=@W%UqwxcZ-'
    b'*%JR*j)O{nbCJO(VhADqFuY~yxUEf_&((b!pPDYPs9wbywu2iyXHpgw|w!d{gzmj$&+(^`NqR0^EJ!#nh=@ZnVs4$lJB<+e0YW?$'
    b'9~Rr&SI+G)l9A!?HNj*wXCi*|MASk+qiY{RI<uCc>)l8bL)_M1l!m6{p(ZOn7oPPj>JA<5{BH;{q*eg<Srp#a*m&ZA9oKU+CWTeC'
    b'~MC5?c!c<=1K|9$#<a?tQE<`%rGO}nLCtKU=tqew1fCbH^xQ+A3na3v&RNpYC`7B3x4Avh!s^;&56qL#N69OTFKE0nX&bA8`^8{L'
    b'sj}57c{nlUa?)kr4!}}Owr!>h2q`_ER-'
    b'~Cm9#KMTrBmrkCyrKGJLh+{wfL6rzUMLs7UC;*o?%0Lk778#wh~7uF+<bk~s*4X1t@x9<Gk+rlP1yE(^J1G?<DibfJpIq?mbQ<gR'
    b'y#$w!|LWCWr8ybNOyv$p~R6q~|ZyB{#4%bAr1#Q2=PywcX#a6oT#M&OK8?BOK}9-'
    b'$SeC+Xb>%CXUJMU{?JStwZInMZB&qU`iF1@E-HF7U5Gr(g7-'
    b'&6Lq=P+^)2I!d9)d9HDlpLRz$SEh&BVX>$KOTvv);Yp>hU+PDTJInwmP-+wyIHP%KRWwE^F-'
    b'|K@eRNi+iGL`9#rRTgeLbA<%2k3y#teC2QS68UPE7Z>faQ_h7MvPb%ODvVXPf<`^3e9zeggq!tNEcr-'
    b'i;6TbPX&kc)<lVGHW>$^)@WSHpUA&;);IvS7Jk1SosVfm`oH#ATgLo(wyu`TZ<d@l3H8XHpTbS=|YH#tELxdjXv3Jwx&QErq=?+('
    b'PA``J-iq?+{6ZXX%HV+hf(39F?YC8`X*dD-'
    b'{Q{<$hnHV_FOjYhn0elND#;~td#<Gvp_VJ0yCswy`nt7C_Mw!`_NcHCC3{i4<9Pb8W0D=LNhp24-'
    b'{eh;foA&<*{Ia_cHvMo9hH@on?gbvpeXQV<&80b7~9g16UQ4b4dOG9#<-'
    b'}vhr)b02}UP#yk+C6iKH>Cj{!Cr2O?}v|?hch3iANgOG(F*v0edq*o{?m<Aq@WO^c&kWY%z7>G~8_LXhIsxsH(neSB`Uc$W5Y836'
    b'oBua4jw+17z9~-4iP$MG4xC2#G1+oIAkiQLFH{cAPHI{w|1h1rfp=ki9gIAty!lVN@R@mvY*$nihBQXu48-'
    b'r4Vta%Z*(hZ+HZ*7FOg*jD-'
    b'o6)dna7RFa(FIBN+!`Sc*W$}yC_;Tv6kj0!w0XZ+CVaUPVBlA;gXczB<a9)IIj&nt8%8KB{oxnm5_$tr+1)|vd{=Y#O;Ja<h}I<x'
    b'v2B<LG}_sfx{<rW<#Uk&04;5b{V@hgW8zr*TMd?jEF^}nVSG$PP-u>v3Z-nuvomuNjtFKf{;+GLy|4-'
    b'?_DMR<G6|1x78cGf_RKU!k@Ca!4G-'
    b'i48$%87KRXC+OdNoXy!TVTbZX!aOVEZ6Eg)~OON(SAXx^qKWq1eWLefc$$b?OlEC}lh&|Dns=2l|>F*VeInkMN22;2;gxUiJcsEP'
    b'AY0yc(`>RqVNeeoJ2K(1&o<^iYfVZnykM>wy@T-'
    b'<i0)n_w!jfjN4@lWy%2!gP_(PLKHo8qDOoqeFHv?^HxG{Be%mO=ioXTKUHBz0s(O~$4C2+G^Vxu7y!Iup^mJ#@@9sKvHhB9a56gh'
    b'-SYI)X}v0Pe&G0yL60ztMESB&Q%n$jWKwO2pdy5>p54!xMszu5!D0RFXQ9My6nX?A<BQ*6B$o6R{K2vy<Ueqxmq+1k}?e#IK6LH^'
    b'X)oqbH=9b-'
    b'Ir6w%;Kv2*01wFy>NiMGQWM(9!n=E3BPiWdb4}ZI~6=Z3dVg_nBXxVjI8)o>M3wu5zU$G;E?)Y*J;YN6eueAU%iwh1Jmx5Ht4kv0'
    b'u&@-2uQT2)TVvEP(!5gSK#jD4N0uBr>eVKw~bn)uu;)a#HJe)IpOM&-Veo-X`iav7&wB7-'
    b'tAG4E>QG(xhHnpS$uKVtt_q+rJ6t2?=*hABj?U65Ocz0=yz5v-6cP?A+fXN(9eBEHos!p8)dp4ba)3rwl5rF;-'
    b'w3W<$`e0r?&MQ5*%^AT*|fHnGAJg+#n*sh5k%T3D|&ngL(tMp#iCm;fc14ZlEyfbM8KhJAu<Ia&m30Akj+Q)p_;4#_KoD0Ms%s1H'
    b'Oz2AC0KG!6|0vx^#$Kf{KAFfe&meP;^1pO`CM3=Z*F1ZKmEB@R^%tW4|YI3QRA8@7PD7sR-'
    b';VN?J(dUq;CF3T3wHc~4H@kGj)x&Xcr5IqLe0dOEwWzH}d22KW%`B#93C8*$vV4POq9s#vEol!!PnJiX|2*-'
    b'H|jk_yALBQqms8Fr<O)z_4YY%Fjsil__o~gH>gd`of0*N6SSZ`!QwK!tTT$mV0(^R#OC~)=$OpFLYAU_l6F*`mlSsH_<&>#RRufm'
    b'j|oDxX|*NaoC_o#y%ARJ!oEC!K_*dx}3%S2KLTgH%EA(RoYPlCHh6qo{6WQf0qVq8!_wg%B7E)bqmQVV!h>iis<WFt!zaZqk|hMq'
    b'7?yAy1ty~6-`hj?W6*2v;KV1ozZlnd%5YJ;x~2Z5xK!r`se5{a0uZeS6)<-'
    b'N>`6N=p8z=Q9gEe8U}NFSjiFu@r)O{PonEaZ>S%ZC%(3O|2`3wOZyXa|`I1O*Ak%|Z4IG!u*fv$GDpE!3U9oKmUs!3(2n8R%F2Sa'
    b'Efv?nbV*unrPx92fT#2MBQj5WZ34Y^hwHbC{BL;+$uqz3)slr$@7f;?eNfBq(AJ3xakt^e$Jpy>9~lU=vDC_Jm`Qd#-'
    b'n<#EIw%5Fw3?ZOq<76&P(INo6R>MmfanT+)rQM8Ki5p2=4IqVx{aRTj%u;A*rd(tJ_X$l?vyz2LRY$UJ}t?uDy)=y1eplE#ZkY1V'
    b'oWE*O_hA$M;YHc-z{`o20gHZu7S79<H^(oq~f7l|}X=c^5D4!bz+#6ao;Kyg^Ytkd-'
    b'*qO;1b>ju)1#d4fbBua;o_WmVbmN_Q%BV?hTy~P<MHHm{X)U&d+dg;8G&~z8Jh}4ykiUvDV^79>L0^*R-!<XG?-'
    b'PvmOcvayx>okDZ;=RN|mR5+FKqj{!7ocT+hk={otV2>9t$K3!84AXMjx3|UTZTVl*w797gcvAp=<dWeAk6PjN(MmUK$xPMsEe|(I'
    b'37=l=S@dLXtD_UhKvk4YsLXK_z`j9n<><s4UT>aou0_!ikLU8tC23q7_{4I^*KIATfvNcsFud562tmRI>Q`il{@gk&s}^}cZ?n*p'
    b'1R&1XGRz6j!h%JLS4dF97(M0en(`uZY9SqT7mtFcRHGp`7LoaauBCcAqhf+2e_lnk-oMdk1*ADm<cXmQ;rY;I)(n7i}a)T2N(y-'
    b'LSYg+8Lv2~8HCQtN&lcP`ZC^~qF*8)p}-'
    b'lrDuO+Nf`C<Tg^Fr5J1Or3^`kVIs1`3Fh$cA>{r5Wzv`T3^j(8C;^d=5aTaBznm}W}}&MY@dJQ-a()=-'
    b'jTG$6NzeqJq>z?XcO7phNIcimJaP7_dwR^y=S()_o?Ve(iw5Dx%?;7W4pC!$=F=rhV)_Fxe%F+280V2bx63_XdWGfENiLMSLD1;j'
    b'!lYP1hbZoHzX3k8Nj0{XCr3_&AkGuK0`$7a!E8fwu^`g~!7k0H13YG8-'
    b')STmT<{DbFQ*kDpZ6wEw`L|AE!)9WXkBN}i7s*Ev`HNM(FzU(s-0;o33P(T%^9UD0e>xP72+mlzkZz4vsArdE%cqDq#-'
    b'<@J<Q1R$xEjqjnDA9>(y|5!B@dYLkW;zW4sA9$$8zYDUiCM$Tz7n(ilM`E#;x)k-'
    b'QPJR}#4xUl^HicjD$f9qiySfq0!|=^`+Kp(${|a7HC_erP{>#ZGESf@^4+1uPHx}T5g&Xwj)dqSI<khue=nBE>={D>oS;vc81EtZ'
    b'URZuRR=toT1QnHtuA++(!-'
    b'(qSed=>wgyg%l)FYXQK7C&|3OeEtWg>9U31|v7_BhwTLT3P;lQ@YvAoi~}LW6wB0Am1G;*}I(giOak((OT=aXud}4Zt`i?Fq2)Xx'
    b'd=H{yIZW@lF$#r|Iz@5)87};+UZU>r)hLh6kDJiAPZ&n1HaHwx445jV2CH%B+`x&P0+CZ!WOeJ8?m#9y#q=C3fvXO~l9<L$Tsv@d'
    b'0^P<I$%iST=-'
    b'~k9Wgv4T^;<njn205h;tT)p#C^D3FIQU`LGpuunwk8tAk5Bq#+TfoC(`_L7BLrUgI*hl2&4P6y>jfOu*l_MlrIZ4okQWTisv4ciX'
    b'q7~5$L3;{pmO?c;-'
    b'0}Y)Z0Kc`$9ViUCQ`>hY8V6*~v(vyeQjuy)pmd5u&1xWPZih`W;F6hRm>L0#JbB|)%ePYmM~}!sY@4L>y6H}Cnz+~{hA}!(AjF-'
    b'*!Zxrea~Cu~_Cw*m)#O6k*91Y1%y>_d&s_t4hOJ|_xn+s>z)1S@0*r_m$uWc!hkP%y>qLV`5fTaIb-'
    b'(ep(bPSW_(+Zo$6}h8s4&TgK?x`%K#R-2m#O2T{Shbt3Vw`0*WwKy^@1*8&q@X8k%6YinJlwUEFhH-'
    b'2QaI*Zwzg04%k4JnQ+D*!JtwzU5zE>&R560Gp@Lyr^0PI^4|lDz71z?z@0<(rOy*xmxS0(C}^nbMY<PBKHljk#;%=5tMO-mX%M<U'
    b'F2+u<2C}}#8z^!#sE&kFQSEUy3_~1ZPpDqP;aeQbI0|K`eq8^1TXu0;+8hAS(R%Ujg-'
    b';Soa}LlkZ^(U|B*tlS(?Y6WmwMCnD9PJ5NEpM+$fJ&%+)m()1D6};8O$Gy#dql>VmfgPvmAUFNWr_L?(ZGUF@gqO#ukxNE!2<rP7'
    b'Np2M!Qt>h$T8nN8|0L$BPO^?27jJk?3*=BzcWjCxv~cu55U~e?_vQXVwfV+`g{Dp{1Z6gA2sM+Xp5A`|X|(WYh#SB=!%&JV`lo4R'
    b'&$hFt|9gf8uS=iT`uVO>vN|zh32(Lk~0e0M3c`CRO72_&!`~VvvzM=R|c`-'
    b'Y8k2R68@S6@gmc*%qA^uiFt>rZ#c|c&oG5IOL)C54<Gz(knO$bGGm`Os-@mx+Z<j((ix&3tg=4LI'
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
    candidate = fib4  # noqa: F405
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
