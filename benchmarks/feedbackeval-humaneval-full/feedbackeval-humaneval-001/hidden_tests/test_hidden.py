import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [['(()()) ((())) () ((())()())'],
 ['() (()) ((())) (((())))'],
 ['(()(())((())))'],
 ['( ) (( )) (( )( ))'],
 ['()'],
 ['(())'],
 ['((()))()'],
 ['()()()'],
 ['()(()())()'],
 ['(((()()((())))))'],
 ['((()()))(())'],
 ['()(()()((())))'],
 ['()()()(((()())))()(())'],
 ['(((())))()((()()))'],
 ['(((())))()(((())))()((()()))((()()))'],
 ['((((((())))()(((())))()((()()))((()())))()))(())'],
 ['()(()())()(()()((())))()'],
 ['()(()()((()))(((()()((()))))))'],
 ['()()((((()()((()))))))'],
 ['()()((((()()((()))))()()()))'],
 ['()()()(((()())))()((()))'],
 ['((()()((((((())))()(((())))()((()()))((()())))()))(())))(())'],
 ['()()()(()()()(((()())))()((()))((()())))()(())'],
 ['()()(()())()(()())()'],
 ['(((()))())()((()()))'],
 ['()()(()())()(()()((()))())()'],
 ['()()((((()()((()))))))()(()())()(()()((())))()'],
 ['()()(((((()()((()))))))()(()())()(()))()'],
 ['((() ((()()((((((  )))))))()()))) (()(()))()(()())'],
 ['((( ) ((( )) () (( ))))) (((( )))) (( ))'],
 ['(()) (()) ((() ((())))()) ((())(()))()'],
 ['((()) ()) ()(()) (()(())())'],
 ['((()) (())() (())(()))()(((())))((()()))((()))'],
 ['(((())))(((())))(((())))(((())))(((())))(((())))(((())))(((())))(((())))(((())))'],
 ['(((())))(((())))(((())))(((())))(((())))(((())))(((())))(((())))(((())))(((())))()()()()()'],
 ['()()()()()()((()))()()()((()))()()()((()))()()()((()))()()()((()))()()()((()))()()()((()))()()()'],
 ['() ( ) (( )) ((( )))()(()()()) ((()())())() (()()()()()())'],
 ['((( ) (((()) (()) ((() ((())))()) ((())(()))()( )) () (( ))))) (((( )))) (( ))'],
 ['(()()()()()())'],
 ['(()) (()) '],
 ['((( ) (((())) (()) ((() ((())((((((() ((() ((() ())))))))))))()) ((())(()))()( )) () (( ))))) '
  '(((( )))) (( ))'],
 ['(()) ((((() ((()()((((((  )))))))()()))) (()(()))()(()()))) '],
 ['((( ) (((()(())())) (()) ((() ((())((((((() ((() ((() ())))))))))))()) ((())(()))()( )) () (( '
  '))))) (((( )))) (( ))'],
 ['()(())'],
 ['(())()'],
 ['(()(()))'],
 ['((( ) (((()(())()) (()) ((() ((())((((((() ((() ((() ())))))))))))()) ((())(()))()( )) '
  '(())(()))()((((()))((())))((()()))((())))() (( ))))) (((( )))) (( ))'],
 ['(())(())'],
 [' (()) (()) ((() ((())))()) ((())(()))()'],
 ['((())(()))()'],
 ['()((()()()()()()((()))()()()((()))()()()((()))()()()((()))()()()((()))()()()((()))()()()((()))()()()))'],
 ['(()(())())'],
 [''],
 ['((( ) )(((())) (()(())(( ))))) (((( )))) (( ))'],
 ['((()) ()) ()(( )) (()(())())'],
 ['(()()()())'],
 ['()(()())()(())'],
 ['()()()()()()((()))()()()((()))()()(())'],
 ['(()(()))()(()())'],
 ['((()())())()'],
 ['((( ) (((()) (()) ((() ((()))))()) (()()()()()())((())(()))()( )) () (( ())))) (((( )))) (( ))'],
 ['((( )) ()) ()(()) (()(())())'],
 ['((((((()) ((() ((() ())))))))))'],
 ['(((()) ()) ())'],
 ['(())((()(((())))((()()))(((((()) (())() (())(())((())((( ) (((()) (()) ((() ((())))()) '
  '(()()()()()())((())(()))()( )) () (( ())))) (((( )))) (( )))))()))((())))))'],
 ['( ) (( )) (( )( ))       ()()()'],
 ['(())(()())()((((((()))))))'],
 ['( )'],
 ['((()))'],
 ['((( ) ((( )) () (( )))))  (((( )))) (( ))'],
 ['((( ) ((( )((( ) ((( )) () (( ))))) (((( )))) (( ))) () (( ))))) (((( )))) (( ))'],
 ['() ( ) (( )) ((( )))()(()()()) ((()())())()(()()()()()())'],
 ['(((())))(((())))(((())))(((())))(((())))(((())))(((())))(((())()(())))(((())))(((())))()()()()()'],
 ['((()())())()(()()()()()())'],
 ['((()))(()()())'],
 ['((( ))) (( ))'],
 ['(((())))'],
 ['((() ((()()))))()(()()())()(()())'],
 ['(((((((() (((()()))))))))))'],
 ['((()))()(())'],
 ['()()()()()()((()))()()()((()))()()()((()))()()()((()))()()()'],
 ['(()())()'],
 ['((())(()(()(()))()(()())()()((()))()()()((()))()))()'],
 ['((( ) ((( )) () (( ))))) (((( )) )) (( ))'],
 ['((()())())()(()(((()())()(()()))()(()())()()((())))()()()((())())()()()())'],
 ['(((()())))'],
 ['(())()()()((()))()()()']]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-'
    b'pO)JF;!JjfUGn_ZWHzPV53mf+Vt@NC$iXrQ8#6<Vc}<zWwp~?yU)2RjEokdo3;!_+Q{Z|MUO;_TT^U<DdWi<FCK}*FSz+#rhw=|I'
    b'hZj-'
    b'N%kH*7n+K%8A>>j%457?ZjA1rA?2~kBl*gmOX|Hb8q&?zyA2`FD!Gi>0Z+B>~>|%8N2&?Px_R)wD@d&?s4T>^mXL!Iz@e+7VVCo%'
    b'cP8yc|?Zp9?K$mb7ZcxENio-wg`)Qd`rwW&5BHZZFa1;@^hIUKJMM^aIh^`yUcL6xH_UOR=&6He$Q<~=NkL0D7Mr_j<VeLXPLSC8'
    b'K>{Hb7yPX*GL;@4eM$;Bd1BvsIix=y^0t$DfO1sV%q)GrU~0PN3HJL-KzCo_}kdphu`8wcT(Ltmu<G~Gf%%gsCKOO=WeQ(rkO=bQ'
    b'rg(Ov8ko=wN|Tklc~G)9Jb2!y!EznYDfv?gz|HlmRftM=Xkm0lwso6#O^M1-'
    b'^RE`iPvJm8|EcP__0_wcT@3|KbN6(%_qm@EWLI5Qnu+5*{r6`wCnZT$K(gS9KBleY|FF;<^D8W9x}EJS~90olB%}X?NwCR(Yy&h`'
    b'`YyD+R1x|=H794u81=}wXvZ`*3j1*5adh3sZj&fz3}5`I?`LOycn%zZPclq<~D#EMELhIC9cgfEf@Vf?rE~yc4=qcZKa<ko^#On!'
    b'*e1+M_I0yJC5`HZ;3N`Uc^-'
    b'?XdgQ>wu+vpO&x;y)j3za=D;WV47j)NlwLas`?*ZaOC<nkMC&&x6s6&Bv!_=*1A26`#+LaUKT4g^z^Uw&tLgc<jP9ESy1t)I=s7#'
    b'iz7&R|Kp^;+1+pJ#Hk0aKhsdl@E;wB`J}53{H=srZi&E4yh{5ktmR#s5ol4vi6;#LqH`%ge3^iJaBz$Vq2C`A^nORzYmFTF0ZJ^V'
    b'phC+(zHXCr`wB<^mMxABqm{r<`Q>DDJS1lm{wf5GAG68xdXaonfMcF1TSj+pUH>9Hnz`n+c{t*f!tyStU1yDJ~5lZ8)FHqdAthqg'
    b'@*SXZM27(3%3{k9pNBL3{1=U^DM_qNGIkP?~3A@m}0JgE)q7ACiIY?d8O1$#$9c@xS4R5|Dy{Y^3dC=fN!<+S0HlL&8ojulD4`_i'
    b'BZNao6dRJL`_wf%kXS!EDNpE#jl(BZu4+^(cZ#nlweRdh}3>;YNiXPsTQ+RRMr{QzL;IIxmAF@^sWE2t!?E$uRh$hU!K-'
    b'xf5kMepyRZ#f0>iR6hcD1x>3-'
    b'WrcoXcn<iheB5+Vi}<(L`WS0O}L4&9)D~X=$c^iYWLyi>=2gfT)M+tiB+FDb<`P%%uKhv~+QBc5={zj%2PnKOzbtMP47CMvf>f(;'
    b'XzWu{w3Ev@H<fNh_OO?1{2vM^w>dROusIjuUFw3VexvwsY5kD>mBo6S$Zmu=e!MAv%U7^qXGu*?#ovQy5f*vmMi!_=4gbj^%Lx=p'
    b'k%yf@i**x3_a>wsH0+_H=RYk8CL(`y^eKAFq4^^Tw;XZI9HW6L3IMKR_?=POPl@F4Og(b?1X(uNm+MjXWzGqCQmUYumd(vn<`-'
    b'cOz>l^ayFLFm(CC$npFyHIWF(g*O#+Wym_CFS?Z0<%w3+A*Eob=uiO81#d3p<*ywcj`&iOgp%y?wACis)%DcWUR5w@41MAMG<RM^'
    b'WX#5i1uY$NZ`3h9xT$U9v8U`n*$}oq`OkIsNCE(@dS-bdpTRY}zD#g{lySB(yL>qXrFRi})j0A57wq{Uhpu*O_B3GUgFXNtj+nlI'
    b'2eKe@6zTH84cc8={=gory>94sZAf6yyZ`~?uD%|<(454A*?wMphGX?I>!;xcF_%s#B^5LnVPQ)l1CeHWLp&%Mj3+_(RCbA|<jsVu'
    b'P7}Tj4>mCK85`EV?OH2vs3ggVHPG18Ue3chW<`$3Ih)-gV^I<O{2C0-'
    b'k5&u^5Tg`Oh7oLI5wZ=v?@*&6dAI_h!}!DtJf{|Fu%dl9bw?vUY%Nm`2?DsK-~-'
    b';(k3#dYUt}UWj>)4muDK547XEpOET4w2iCQ_5McrhF>|<pv=t&Uhx6Dqswfpi<PShUYB2B{)p-'
    b'M8kf06+++54WyD;|p3F*f9(BoHXXN*sVf8K5HJjMm9Q1m3Gqcz$bx5M8!FS1@W)7A}v^*H#LzPQjt#M3Cw>9D^~40SN?8gF99}4U'
    b'd<#HrQDux||ccUhiP6LQg@M3g$)roVXOWZ7)_WN6?EAlkHoZ=|o0^ZLrM3o%XZv^#U$TLKdy9-'
    b'ZnXfC|hAk^F@Bao6l%uouA9_HuUXqn6O&N(y*v)qB!C(o=i>5$m!6JXDrFym#-'
    b'jyh@gC<0FrvZ@o=;X(GkM!SUwI(13RKwyiUq;T@!MUZ%Y#XVJ7MyVB?G8iRn7IGU*QCbx;q_(0b_vjt*icabk#}RD|fz$??1LKS+'
    b'uHTHO31^&??bKjXgCFq@ynK;Q(l&9kgG7p?_h2s6x4XOq9Mhz(K^bqoE#?*Vg9CY_Bqy!2MhLYS5+@mE&E1Li9%hG+Oc0~TfLs+5'
    b'g%eLuB9Xn7vcA6+=yCBf1P!eW6A^p3(&HGBp>z;vbp0L+*uFZ8!>N~e}*zNrRbJ<D-'
    b'6fXf_LFi$evn<^0<@LUx4V=qJpgbY>jr?K)Kgdjix7)iiW;cc=b5>)5QgrvRB$b;#wN*t*h^-N?@h(q<IK>4)>L-'
    b'L@6DhJ_%Ct!quhJ=;~mMYrb2HJ~w+)(lyR$n@SIgC70Yx{KSLdv`Z3IYjxWvE&g0-4cpxXiq1L=q-'
    b'e;7j(g<)opTg1Lah{fUqm50fYlFjWv0m?GzM397`Xx$%NcNDj<_aF_l<Iw3c02`X*=tqm~~2N;Wt24+dBhj7K1$-'
    b'&<Uu_ty}DG&IkIKY94u`?ts2zc<K4~mJXLE*q0ZVQy}0}<IT3289#1*aFX7~L@t>ipVBV8M|P`LDt3H^Pic-'
    b'V5U5Ax=RC;;&+or&S_j#WCR_y<iu91*zB!L?M^yWB%HPGw>1x?8Q%k$1h64QDtD@xl)rgEBZ@}N0XT-H!m;B-'
    b'60F((sxJ%+Bjx5!U<AU0(3f4h`pgR;kF|PNKimh&`XkAZ+I}gpFH*z3VK9f<gEeGzy)CF3~w0XK-'
    b'>867;ic{_%;lwf+D~ll{fWI*7}%l8Yjh>267OLON5;I?iOw*5jOKwKncYdwopy9`jR=(F#diC@gIi60W!PhyHX%*VcbYCyx*_e)d'
    b'8{NIf#sd;ChUCn9zwGX6lOiYcF2X-v~%Y7(hxRJ7Yn$FlDWG&6AiEsM_^M-'
    b'<bKSej`6m3PGgGx_)ggCKu&k5}vJqj5BMS%*XO9B$ZJ0#;fsehvXT8ya`#GvZk-NOw_+Nv|UD?HyyS&;0R+Mv}tc<B#^!+Vf)NCU'
    b'sH6V3Y=h*B+d0Ep8`QYoFeyj3=@XV9kl&Iy+oMbP|12>PLe~2S3_TjN=Kh(y;maaiyP?5E>$@RK?7;45`g+KW`H^3z+CyR9f=(5p'
    b'uH<Ff)CqsTuRC}Q2;l6*FXb=@Nah<@ktL8AWUaZhn$*~Tmnsd3;dLx-'
    b'C%ST`6SUFN??uvGa_78a|DX#P$x8$(*eW90iIt4GozTEC#o`eio$(L{4#eu1@2^F=#H}ETw`;{(HIXHjhnUxZYA;1bH}@7+jw^Rj'
    b'q@!r!vM*X!2y{~%ux-'
    b's=BdleYrPwSieG9+2;bF>!dkK;lG^Cbr#4$ALv>*gATB@%H;M~d4|u1(PcV~s$naw?tRHeD3KC|NfmHE9@n!Bo8+BZ=1Rnfu2Y|y'
    b'Z4EW4KSOxSc7fFUHNGpLhUj2fZ9jRE~+aw4UmjIO&=~22x_Yoflw~WB&-'
    b'68Il3ye^!!^GZuGt>f)SN#|at;6hz28<i;#sf75iHA6}(W{M8&|zXkvG(p%-'
    b')&~~@e%^I(VP5QhQ}d+Wj&P^L+pSOIJUEo>cYJC!`_#X@(5T=E-;^t!<CS>{uEKe!WjrlhY?_oLu@2ad5ol24|5c0dt+6Yd8y-'
    b'W)<cPzYs;OS;(IBD-W*&=$|wpq=^OYZ7QCw^G%)aj?3N6@mDsy+Kg#ms-UPvUwTZv~KO7+q8v'
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
    candidate = separate_paren_groups  # noqa: F405
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
