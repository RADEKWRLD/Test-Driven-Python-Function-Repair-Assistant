import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[2],
 [4],
 [8],
 [57],
 [3249],
 [185193],
 [20577],
 [18],
 [10],
 [15],
 [28],
 [1024],
 [131],
 [33],
 [1000],
 [100],
 [123456789],
 [987654321],
 [1025],
 [11],
 [1026],
 [29],
 [1027],
 [14],
 [34],
 [13],
 [99],
 [132],
 [123456790],
 [1023],
 [123456788],
 [32],
 [31],
 [1022],
 [987654320],
 [123456791],
 [1028],
 [123456787],
 [123456792],
 [27],
 [39],
 [12],
 [30],
 [2147483647],
 [1207943],
 [112234369],
 [999983],
 [1003001001],
 [43121192843],
 [1073741789],
 [9999999967],
 [1003001000],
 [112234370],
 [56],
 [9999999966],
 [2147483646],
 [1003000999],
 [1207942],
 [999984],
 [79],
 [80],
 [1003001002],
 [78],
 [77],
 [112234368],
 [9999999965],
 [83],
 [76],
 [75],
 [112234367],
 [52],
 [112234371],
 [2147483645],
 [53],
 [9999999964],
 [112234372],
 [1003001004],
 [101],
 [6],
 [1003001005],
 [1073741788],
 [67],
 [123456786],
 [1003001003],
 [47],
 [57],
 [58],
 [26],
 [51],
 [55],
 [38],
 [37],
 [17],
 [125],
 [7919],
 [987654322],
 [43121192841],
 [43121192844],
 [987654323],
 [43121192842],
 [123456785],
 [112234366],
 [999982],
 [112234365],
 [43121192845],
 [2147483644],
 [1207944],
 [1073741790],
 [1073741791],
 [9999999969],
 [2147483643],
 [1207945],
 [43121192840],
 [1207946],
 [1003000998],
 [43121192839],
 [112234364],
 [9999999968],
 [987654324],
 [1207947],
 [999980],
 [999979],
 [999981],
 [43121192838],
 [987654319],
 [999985],
 [2147483642],
 [2147483641],
 [46],
 [43121192837],
 [999987],
 [987654325],
 [1003000997],
 [987654326],
 [1207948],
 [999986],
 [987654327],
 [50],
 [999978],
 [999988],
 [999977],
 [999989],
 [9999999963],
 [44],
 [43],
 [42]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-'
    b'pO+J+dgdZH4W?T8knV_)liqhyoHIO1U@SNP%j?(SG&e>aoWQuvD6o^zQ2>LExP4u<!r=*FXR9=l}Tm*I$4C^KXCppTF(g`tQH}Wz'
    b'Ka{<6kq`w%&c$EN9%ie6~CI(_(hh64iY2EbZLhZ`R?Z^pp1QfB*e&|M}ZrTAyQ=miw&bUP)KC&ZJ|=FdaEHzjgH1^IBqQu638KHn'
    b'x>&S#SOIn6!4ft*%mTsv@nc$=)+3EB!hTT>Ywz+m~EDUFx~HjgyX5KckdikLh<UFIvaVc6Kv%)yLMecIji>v~L+J=Vd8bJfh0JBd'
    b'@mC$zxyt^_acWv^x8uHrei-`>g4n(ph%OTq&veva*kO-&6Z-'
    b'E>$#B$aZsnwNd`E`QBv}Ny2tnuh%iu(lttan@MrDHtXuPy;8fi&(^-EbNls}qgPh#m(yVhbE%YEw)5_i)}+w7w$-'
    b'$U)m+RI)jM8!p=!IT>upN5=X_VT<YR0(?z3yoE`BJX`W8;C=I$&vU3aG;Zs$c>R-'
    b'SJ)^^Q2W>4nmb+Pq8K!dp`{Uo}^Dmv`=G<d)NEhu8I)htgT}#yjx4IlVC(6<Rb+%Xvtluy?1-'
    b'zvo%$%yueOttXWn9nq_$o>}*p^6N2W&*8)PaiO)2opn>uyJkIO=IL3LzsJFI3UX53of?hqW6x&%)UU_PGTKc!E63Alk>Sp2M`^=4'
    b'+YlO=Be!E$Cr#O8&$3%;HLb##yaV5T(z|Q7m9){lxp=FdQ}wDlGe^qsl)btZ8I_UZL~|Oo?_{&edrT^qvm0wil?$issoh&|>5aos'
    b'dMB4YDWJ+NrfjHM*Kyb2edX#aF-'
    b'6~(8V>qkR}QS5rkrXjtboDg=#7a?qfBMcN>Rpi+f+IA*qiXvw}{Lpei`#TWqRX<XVt6gtp3yY)7;t`Cd<6ta_6P1E7RZJYDV7(#b'
    b'v>jXCW$V%zBF9D|d9psvXuPQ)=NT<DWZfP<Pwc>YH%c{9kp5hI&z%_|tN2FA4o>v(9U27n=P{)ZiRO!xH`4vU<y(Y|-vEv-ps_v`'
    b'luK8PMu7%8|rYPhOI9?USZT*5@p8EQ{{G_PTFVEZ$dMDW<A*NsWg&jo6rpc6$-'
    b'&mO17lcd}Wr>lqzgnpo<$sT0cE`(S1~9Uibz6&moQ#I!TST{?QeT&R_l=pD{;?mX-'
    b'5{I@rn=;L8|oYxVHGV#~<RZb>LbqaTTE*X6<)@Va?KBjbz<S}XEZ3-'
    b'DsI=>^O$6}aRts+&c@xo3!ti}U40VLbBolq;Su^6GKUu{~c#ZIqf+QmTbnKR9{LM%q^Oj#UxrlK*}oXw4~nUZvGj#l1iicgz&jy|'
    b'szv<CG=H#WKvZ<{I83Als$TvBFd-fB;7el8=0@IPnRC_F87P!J386$B;>Nz<Xb86-'
    b'hI?`8=V)%y{>iC<**m1MmxUZ*179Ixj}CEB9%Tp5HMk}9hY+fxc^IB>I@cjB+FmiEf&%BMH{v|Jg}SrwLK+PCK9Sel+nQ6>|CcvA'
    b'Ah8(W#T$*qgOg^eMD-)QolPCuoct8HAioi$eS(|szh&y2!3b77`Q%-'
    b'Bq5@<xVH=<hM{gqe|Ux=Zv>R*J{D2zseq(M428H|oWlAGCN-_G(mb&x#&DEk-X91tf(L66fGKuu}z)D1B!-'
    b'D4Eo3Dmr>$;VoIhu);T-f<6&-4wMNtG!N6<($6X4b{dW(2zUB-'
    b'8N6HLEO6J}n9~L*G@hMaZJJFp{FTO)$*!0?TKzJKY<^P4gIFxByoPf}%pm}(zER7GAHFU|>z4Bej1oSaDV|Wo#^enF2a1R5%j8`Z'
    b'0~@(|Z-'
    b'`Ff99Z6~4LyODsq$V995A7_eWb&G0Fl~NI}Ia=>Ajb|pk(><NtJf6%j=tNRh!juGIh<X4s;9yTGuT0$C;L0>A_y`A6loNk3+&WnF'
    b'Xz1`~6rTPoEA|Kx&vJ?Wp+7j=w>DQNm`oZ9wNz|BkRQ;B<}G?=f@@Qao&hV<WFpj<d^-'
    b'wxFdt>60!DXO?YyAf#nZ)B;nu*2j8}0TC<^?c(eOtU)!I1Q-'
    b'X;ZZKG_Mw2_%G?JcU!aV#y3r&T$y}qIQv@m(j6yV7^`D>?*J8^Hi7YmmKwCyUDnID(grYG@U2a-'
    b'^^=bFL+Ar5O{ZMo9%_~YQXfRn;7B#>vZ2M_x~O*zYri5?7kbu{J)#m*4PQIsEdp-ZO2*@>goG;<540C?2399l8m%v|||pdB$y{_#'
    b'yUp}Co6Y-'
    b'Fsfmw(`KxIF+<D@bLW4CI2UW$Zb?qo$CPHtFxTDJb9NGMgRUS>gE=VO8L5z*l9%p2$;%JFFRvh@7T^J~0|J+!IkS^p2fNYnT!<Qy'
    b'9$dX00>E_(fX)AdmsTAfHes1IujIO{cO0{qUM;z#Vd72;djEnuZok4|dH4eT@RU@&C562R?xi>~q+Bf)4#{%A}`KTO2ZITd`%}h7'
    b'uE7c)@P2jKbW)(48AiGzxE9JOfi@ub)uh{|nE67QhemW-cn|04dntsT40As6AzGqX9Y@2@*PgvDN(!Jg=aCI*G|@jZ=5y+z$57u#'
    b'Ewg;*E<C5%vNfp<h|)E|6{ji2d~qy?2D@feMc~`NLWY=>i&n{o#$^DEcp$#}x(1RHk<94dDQ(KN2-'
    b'2Z$k=@h$12s8$O}jG;rT{RqT(^<rLAYx=@=Y%yW#*MK0cBXi^Tw@Bl~`9Ib3)H2}sK2^cQXJ%e!LXCkve*mfLb)*YhRzb+Pr#`DB'
    b'<QRI0G6aZs%PS1cpf>d}c>5_nAXgV+<w$bT@D)06VTp~njgV|`deR)1{i=tAV)}!4y=g2JpI`YNtH#w$Fk`=kiztuo3)E45IlXom'
    b'(5{(^@87BdtHri2c!!#}xN1P`b(=LN}7FONfFlg{0m<z2gbdP#)DCh(>LhrQWvKZ=tLSa#+1tWx>NKzVEE6p#KRoIN=N4!v|{;-'
    b'l}OkxMm87Hvs0Nik1i1I<o9P>1oB}M*vo4Ny_FP=9`L?H}SpPhuKcpRurMM`BVuu67?uM_<#7?yxA6YA~bVzdVFsBOlHv6>Z|;_Z'
    b'{+B!RozQj!Q65Ia^f)?#LR94U_a*<B_j473ehpl{(V3JuM(o(mZPe!H~m_*fkYyK<bqbgF4e`kzmWfeoapWUx=MUS3Cr2ZQOvU`I'
    b'AVm!ve1Ahk28JNS-$Gnu_L{YtC{i%U@z<^ZB#Zc%q7u|}n#oo<2f@LXpP#7U+HBjLcK@PBl1_OmN)B3(Fp;?%hGqA}E{x-'
    b'<CX@|pv|0p-R|;yR3;%{I$@M3EAy5-vlJu>MBc*4-M_AR<8KP{WMtlr=+^h-'
    b'73$xQ0xS7{0aMNx{?+oglk=E^ELLFPcM}alV7vLhjNeg^t4q6p&a8MAZoSAlR?RaGdPBQy1`PZxC^W4AAC0&&x%9JZ0z;z?iTOkL'
    b'Z9kKA%fi`Kt|Mh+o%$X!@pJ>~JEd-'
    b'B)x5Q=&2BNUvOk7XL^ojC_}h1$|c?0BhuOVf~UNE{y6ugJ}(Eg`9Sv5wrwS<kY1A>I^ss(^=U49up6bS;2=OQ6LhHhk?nRknTCKq'
    b'%clcS#Tu=PUgfvSS#mC%Rcq9g6C{}8P-bCnsJ-'
    b'a@eVv!puy{boU=juM!gTlnXRv2Hq+V9ll1Em)QE`;IHQINP(<dAJ~8A8C`yb!GSM}(_u?BEaf7>-'
    b'vg$AS%8rZ$OSmqgJEJ8h(TvN}rsB>{JJ<_4hH%M2p3obQDXQ}s3?XxpzanC04|?VO;H<{IO<Cwy`9WR8d=wtyw84s;oS9MnhkS9q'
    b'9QKVGJ1q(%6N*_z(n5;9&Jjj5PGRL_002j!V`c-CRs=*pNr&4T62)^`ZEye~rjR-'
    b'e?gT~Y!Gx^QkLaCqdd6_GW|R)ZYj0C$F|8nMTZ5!}dI;Q*K`NvXAU1jp9O;ViGt>kb{77k8bh;8r?|1QnEK!Z)p%?*;>^}2^VDK~'
    b'&UEBq&z9Vfi%?P?hd<b`lwb@%uzBKJA3KB$dr859onQK6@FLY{^9hXQMO)SLX4sN0&G~{IVyM00EFhYX}L`@;bO`w9SfEu2(h2XR'
    b'shSiweV8Mh|PsDqP0T<}>dkngOwqj%e75inAb>mJRe}LV=B*8NDobBA;uu?G6N_JKcOn(PnW8L`VVi-'
    b'Azg+P%$I7=ocZZ=cgp5-;^N1N=1ki=m^mHbKnZUunz7G$>w6+ibn6oHks1TciSlS#lBW()s__#)@d7zJG8D1rT%uc3Z%jf-_-NI{'
    b'w<VZ$^o6-'
    b'VzT=H+%Zk`0J)4+i0Luo~=sd^6Qx@C?oX6&|^lp9f72P5~8n*1(_uk21*BHOC>$cqhqZCvyFpa4?Z1h{+>aNJxq+uADs~%*0J3F%'
    b'^1E5DkQ?GU;RrJft&Wok9Koy}c%2ApIvB)X_>A;2(&AI|cRq$Q6eS>>;amBk}b^vOx_QAxz@`L=R>JAsW0c(ew$m6}iU<imaZxA@'
    b'{lBpxDga8*GIth)ZcX;q5)<q#k3$TNJu04OWy4W)tmh*gC@ua4$AfQK5qn2MM&CVD+Z2HXyj9!9VEo&?(%N8ALWqs1(z>A>CrMaM'
    b'zkg0&Yqp5z@4wPV(h&Oo0Pz3<`P@2mz`B2XViN3dY);h><F}@nCpZ{UR~l%p&i1mwtIijGm-QFvNAEJ%ngPVw@Kck;+QZ?oPK*Hw'
    b'+8Zr8gPz)YdbYLOtgUG(k&nO6IcW_}t+z3~{ZG$W1lA3@nBS-'
    b'@M2ypuEAN{BdzvcwyE8z*3LULH2}Wi_}>&4>|0B*<ePXW`~MBz8M4$c=-'
    b'eNdj!hLNG67x4nb7mwn@0fkT@aY;viDeQ<JP2H!7R}*&&j0+U@(!usm+}U??0DKAIYLU_l+wFoA=3fWt98wt}z-'
    b'U8o3I1dEEi|9#5Yvnb8WZkwzLGm!vSs^q5INeOY`hFCI8Wab_nGX%1Zi*wSTl#kLGoJ!B4iYZTvTTKS1Vg|wGzAuW{gr7L57pgKc'
    b'Il>6QBtDM+NjlV)(?LeHt+@8oN)%&(lmDv{=`NE7yx^%`g95?kAn&;Grut7PfK`nQtJoM^%W%du0g9Pve*SJ|$_gQ~-'
    b'3Y+W?hK%B%AX+a-'
    b'}Rvl$QP(C_z#Os@Y0TeUE=zL!c?Ns*%|u)3*v(cd5D~XDw7CETd%}yh{?t%1C^vvi8yY~p%c$*+%;i8yJ_6S=?$nxxhb250e&}ay'
    b'`s-'
    b'BQe4Q;T4ra2G!acnEJ&bI8QnNR&}w3hL~s&vvXOBm`98XZW;IAAY$QX0yo*yopXu8{ix7R|mU1E^E0!*RI?t}?yJA?+r#MJRi-'
    b'V~&ow$-'
    b'e;Pgd<6x8ML8ai>H(qwqNCEtP@Ew)SKx<x+`#qCc<h7Z6uI4Qg~%;QHE7(~YaccPsm#K)~Ykq5S7J~7EMJ}!1DLOA@nLyY?!T8pU'
    b'8sMC7J%x5~gt`V=G4e8_f1R9?fv4QUva&7#X_C`|TQX$tK6bPm>H#a^k7P&wi!4(>Sl{a;XAjb$#qV59|Y#MvwhXKwJag^o6731&'
    b'=2i&+fgxG>_;!6Un;=i+3*o9HKb$lm9?k6CgmUPuJBfB~g23icGp;O!ln};Kw$^#6~EFQxP>Tz(N-'
    b'oQg?1k*@^DV!!rgZ`{Ibm!HPdEv&O5fTIF8<YZ+uni3OIl~W`Li__ENs&tkNf}%S)H^gJp3J_Eaxlb;WckGR6t+xU^qpUc@ytGM<'
    b'4jWAG1Hky){Q&WS$b!-ag(^FWX{iA4TBz06%_3RIe(dfOhk1kF<n0sra==<j93Xi3Wh`&A+uly^ybB?$wp-'
    b'nJvd?#zylMAo9F>LV;Y;5snL(_Y-W~$W5t%BeVsHAXEAA>+g5y*ys?YdeysF|(jmM~2*js2&v|z}G%8sWR*p>LJs~-$5o;&}Eu-x'
    b'j|M!@?N;?=&DbZIWOSLdX4sg2%m}R=ZkTf$<uCZxC<&BT6J1<@3`IPeWJ(If83hD6$F22c<Yw4eh*1<ZsC+SE#KLa6caxV|2V&KV'
    b'rwZTM5@EA6`*OmYqg2J@~LR=ve262S~AqsT22gFbqj%ddv?N{O&pGWcruTzh2Sw>Se+7V$ZK&;XR^qk^A#tdEHBW|#jD6`thcmDA'
    b'uksjc^8fabNIc96=tf^mE4;~<91@ZAv%@L0_J<UT06jQ!$zVs|IBod!x46v#g0j}y*Q5MA@2wbq0dW&ytINt*03tFc*)%;d-'
    b'04D`XNCqTlD#{_W_?$!6qh2f?Hx2D6xCU&*aQ7OQnk)}4Oy5PX6H%g)00YLF(~n0WiV4Tr2%w&@Vlai-'
    b'V7Uck=4mtA0_)ymN=LFVI3UT4fi%j%jueWd77!eS9Un>~9RpE-'
    b'#q@h2miXMt{66*rE;cdjh*FLq5m=qLdvGB#(3r$H6pUFK@yWz#`boQjZUamHe#ZpKk08+-7`k>y6+xN-'
    b'T0nk$bsnTwR+mD_IRN%ZmP+yQ#CYWSE_xNQkBi*6gHUW4{;nFgvh)znUEKpAK}6(B<Ld$WBYbCL)%Cju8e}C>4XfrL;Ay9F*dHT`'
    b'V8G;cW8={Mii;Iu3oUK&?ViMRQrh1~exv!2R)}+UhHZmeQC09lfPqxwGg73{M)9PLOsMj~iKmDTA0}03jb&~u1NEZ1@fmuOJ|b<a'
    b'UyOfte3tSMv6z~95YIC520UQz@4^nkkB754avc!s>(-#SpKm`0c+&V3KD<~XCRg-'
    b'<&?6V*=P!PgzMzhcjW6RkP%fk<7#RAbVjOvV<>@pR&q)y1g`y-'
    b'>gfg%>{rW}`34UZ#O@W7M#0xkJkKBqR!y{xFV{v0(>0}xb&>^t^aWv8!hPW*vATjqC0M7v)BqX3ZPbBRr-'
    b'h$O+wux_*mghpbNJ=3T>q7xLku7md8eiOTY3!x+xV)0YFu}-'
    b';2pd;7PAr)RU0>CqS`1u2pW5x`m!D3Rw2#Iw#>8jt&fjctSp`u?E<Zig!{Uq3a#$s5y~79EcSD<))A)6*jQav=HGYMmqoxV?8bF&'
    b'zIgp1Fm)Jr-'
    b')cDk6O*h4Q&<4*lIq_vW2~r$iPkH}PNDlT2!E0Tx8rCy2eo4TBdW}&f5Rr1f_KSp@OJ}F$f}co9d`X@ME?DtvB(=xq7CQ1q8Yw+~'
    b'kxb*aUs?>|yUf)1)K31vF9Ab9J}z71Vu2B`kXD45m&51HLj<7Xfp$@c$$sCBNfMX@Q9?*ZARGRQXaJ+Yi;w6P-'
    b'b(NF@OW~+#6v5T8o!~@KG%#7893bVL>4L*mpAc?DvrxaO&U2V!g)eFK@S&G!xZ5t^4wWp)}*b${fXm@x#x(4w>!nnxLUsPYa<(}#'
    b'GLp~v@`}bBj-z8f%VUP<6;7Qj_b^_m493OVx7mO=nS<1egP<Gj*!hvfEx%$-1(f#dg?nVXx!qHH&GW&+58FZL+-'
    b'+TE3J|@$1jpDR!IunkXGDQqOUtrXpO$P|NSoszO2s'
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
    candidate = factorize  # noqa: F405
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
