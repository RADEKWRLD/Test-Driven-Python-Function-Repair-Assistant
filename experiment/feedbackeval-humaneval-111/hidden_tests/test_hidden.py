import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [['a b b a'],
 ['a b c a b'],
 ['a b c d g'],
 ['r t g'],
 ['b b b b a'],
 ['r t g'],
 [''],
 ['a'],
 ['x y z x y z x'],
 ['c a r s'],
 ['h e l l o'],
 ['a b b b b b'],
 ['p u z z l e'],
 ['a a a a a a a b b b b b b b'],
 ['c c c c b b b a a a'],
 ['p p p r r r'],
 ['a b c d e f g'],
 ['h i j j k l m m m n o o o o p'],
 ['a b b  b b b'],
 ['h i j j k l m m m p'],
 ['a a a a a a a b b b b b b'],
 ['a b h i j j k l m m m n o o o o p'],
 ['h i j j k l m m m n o o o o  p'],
 ['a'],
 ['a b b  b b  b'],
 ['h i j j  k l m m m n o o o o  p'],
 ['a b c  d e f g'],
 ['p  l  e'],
 ['h i j j   k l  m m m n o o o o  p'],
 ['p u z l e'],
 [' p p p r r r'],
 [' p p p  r r r'],
 ['a a a a a a a b b  b b b b'],
 ['p l  e'],
 ['h i j j   k l  m  o o  p'],
 [' p r'],
 ['a b b b b b  b'],
 [' p '],
 ['a b c  d  e f g'],
 ['a b b b b'],
 ['h i j m m m p'],
 ['h i j j   k l  m  p'],
 ['h  i j j   k l  m  o o  '],
 ['h i j j    k l  m   p'],
 ['a a a a a a a b b  b'],
 [''],
 ['a b b  b b   b'],
 [' p  '],
 ['  p p r r r'],
 ['h  i j j   k l  m  o  '],
 ['h i j j k l m m m n  o o o o  p'],
 ['h  i j j k l  m  o  '],
 ['h i j j   k l  m  o p'],
 ['x y z x y  z x'],
 [' p h  i j j k l  m  o  '],
 ['h  i j j   k l  m  o   '],
 ['a b c  e f g'],
 ['c c c c b b b a  a a'],
 ['p u z z  l e'],
 ['h i j j k l m m m n o  o o o  p'],
 ['a b c d e  p  f g'],
 ['a b h i j j m m m n o o o o p'],
 ['x y z x y  z x '],
 ['h i j j k l m m m n o o p'],
 ['a b  b b b b'],
 ['h   i j j   k l  m  o   '],
 ['p  l h i j j k l m m m p e'],
 ['a b b  b b b  b'],
 ['h e'],
 ['h i j j k l m m m n o  o o   p'],
 ['p  l h i j j k l m  e'],
 [' p p p r r r p '],
 ['  p p  r r r'],
 ['a b c h  i j j k l  m  o  d e  p  f g'],
 ['p u z z  e'],
 ['p  u z z  e'],
 ['p u z z  l  e'],
 ['  p  '],
 ['  s'],
 ['h i j j k  h i j j   k l  m  o o  p p p p r r r m m n o o o o  p'],
 ['h  i j m m m p'],
 ['p  l h i j j k  l m  e'],
 ['  p p r h i j j k l m m m n  o o o o  p r'],
 [' p'],
 [' a b b  b b   b'],
 [' a b b  b b    b'],
 [' a  b b  b b   b'],
 ['h  i j  p p r r r j   k l  m'],
 ['c c c c b b a a'],
 [' p p p r  r r'],
 [' r'],
 ['a b b  b'],
 ['h  i  j m m m'],
 ['h  i j j k l   m  o  '],
 ['h i j j k  h i j j   k l  m  o o  p p p p r r r m m n  o o o o  p'],
 ['a a a a a a a b b b  b'],
 ['  p p p  r r r '],
 ['p  l  h i j j k l m  e'],
 ['p  p p r h i j j  p p p r r r p k l m m m n  o o o o  p r  u z z  e'],
 ['a  b c d e f g'],
 ['  p'],
 ['   p  '],
 ['a a p h  i j j k l  m  o   a a a a a b b b b b b'],
 ['a  a a a a a a b b  b b b b'],
 ['  p   p '],
 ['p   l  e'],
 ['h  i p p r h  i j j   k l  m  o o   r r j   k l  m'],
 ['c a a a a b b d d d d f f f g h i'],
 ['p p q q q r r r s s s t t t u u u v v w w x x y y z z'],
 ['o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t u u u u u u v v v v v v '
  'w w w w w w x x x x x x y y y y y z z z z z'],
 ['l m m m m m m m m n n n n n n n n n n n n n n o o p p q q r r s'],
 ['     a a a a b b d d d d f f f g h i  '],
 ['x y z x y z x y z x y z x y z x y z x y z x y z x'],
 ['    a b        c d e f   a g g h h h i j j j k k k l l l l m n o p q r r r s s s s s s s t t t '
  't t t t t u v w x y z'],
 ['a b c d e f g h i j k l m n o p q r s t u v w x y z a b c d e f g h i j k l m n o p q r s t u v '
  'w x y z a b c d e f g'],
 ['x y a a a b b d d d d f f f g h i i i i i j j j j k k k k l l l l m n o p q r r r s s s s s s s '
  't t t t t t t t u v w'],
 ['    x      a b c d e f   a g g h h h h i j j j k k k k l l l l m n o p q r r r s s s s s s s t '
  't t t t'],
 ['h'],
 ['l'],
 ['x y a a a b b d d d d f f f g h i i i i i j j j  j k k k k l l l l m n o p q r r r s s s s s s '
  's t t t t t t t t u v w'],
 ['d'],
 ['u'],
 ['b'],
 ['    a b        c d e f   a g g h h h i j j j k k k l l l l m n o p q r r r  s s s s s s s t t t '
  't t t t t u v w x y z'],
 ['p'],
 ['z'],
 ['x y a a a b b d d d d f f f g h i i i i i j j j j k k k k l l l l m n o p q r r r s s      a a '
  'a a b b d d d d f f f g h i  s s s s s t t t t t t t t u v w'],
 ['g'],
 ['x y a a a b b d d d d f f f g h i i i i i j j j  j k k k k l l l l m n o p q r r r s s s s s s '
  's t t t   t t t t t u v w'],
 ['s'],
 ['x y a a a b b d d d d f f f g h i i i i i j j j  j k k k k l l l l m n o p q r r r s s s s s s '
  's t t t   t t t t t u v  w'],
 ['c'],
 ['x y a a a b b d d d d f f f g h i i i i i j j j j k k k k l l l l m n o p q r r r s s s s s s s '
  't t t t t t  t t u v w'],
 ['n'],
 ['v'],
 ['x y z x y z  x y z x y z x y z x y z x y z x y z x'],
 ['f'],
 ['o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t u u u u u u v v v v v v '
  'w w w w w w x x x x x x y     a a a a b b d d d d f f f g h i   y y y y z z z z z'],
 ['i'],
 ['    a b        c d e f   a g g h h h i j j j k k k l l l l m n o p q r r r  s s s s s s s t t t '
  't t t t t u v  w x y z'],
 ['    a b   k k l l l l m n o p q r r r  s s s s s s s t t t t t t t t u v w x y z'],
 ['    x      a b c d e f   a g  g h h h h i j j j k k k k l l l l m n o p q r r r s s s s s s s t '
  't t t t'],
 ['t'],
 ['    a b   k k l l t t t t t t u v w x y z'],
 ['o'],
 ['x y a a a b b d d d d f f f g h i i i i i  j j j  j k k k k l l l l m n o p q r r r s s s s s s '
  's t t t t t t t t u v w'],
 ['m'],
 ['o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t u u u u u u v v v v v v '
  'w w w w w w x x x x  y y z z z z z'],
 ['x y z x y z  x y z x y z x y z x y z x y z x y z  x'],
 ['     a b   k k l l t t t t t t u v w x y z'],
 ['w'],
 ['x y a a a b b d d d d f f f g h i i i i i j j j  j k k k k l l l l m n o p q r r r s s s s s s '
  's t t t   t t t t     x      a b c d e f   a g  g h h h h i j j j k k k k l l l l m n o p q r r '
  'r s s s s s s s t t t t t v w'],
 ['x'],
 ['r'],
 ['j'],
 ['    a b        c d e f   a g g h h h i j a b c d e f g h i j k l m n o p q r s t u v w x y z a '
  'b c d e f g h i j k l m n o p q r s t u v w x y z a b c d e f g m n o p q r r r s s s s s s s t '
  't t t t t t t u v w x y z'],
 ['o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t u u u u u u v v s x x x '
  'x y     a a a a b b d d d d f f f g h i   y y y y z z z z z'],
 ['    a b        c d e f   a g g h  h h i j j j k k k l l l l m n o p q r r r s s s s s s s t t t '
  't t t t t u v w x y z'],
 ['e'],
 ['x y a a a b b d d d d f f f g h i i i i i  j j j  j k k k k  l l l l m n o p q r r r s s s s s '
  's s t t t t t t t t u v w'],
 ['l     a a a a b b d d d d f f f g h i  '],
 ['x y z x y z  x y z x y z x y z z x y z x y z x'],
 ['    x      a b c d e f   a g   g h h h h i j j j k k k k l l l l m n o p q r r r s s s s s s s '
  't t t t t'],
 ['x y a a  a b b d d d d f f f g h i i i i i j j j  j k k k k l l l l m n o p q r r r s s s s s s '
  's t t t   t t t t     x      a b c d e f   a g  g h h h h i j j j k k k k l l l l m n o p q r r '
  'r s s s s s s s t t t t t v w'],
 ['  l  a b   k k l l t t t t t t u v w x y z'],
 ['    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t '
  'u u u u u u v v v v v v w w w w w w x x x x  y y z z z z z a g g h h h h i j j j k k k k l l l '
  'l m n o p q r r r s s s s s s s t t t t t'],
 ['x y z x y z x y z x y z x y  z x y z x y z x  y z x'],
 ['     a b        c d e f   a g g h  h h i j j j k k k l l l l m n o p q r r r s s s s s s s t t '
  't t t t t t u v w x y z   x      a b c d e f   a g   g h h h h i j j j k k k k l l l l m n o p '
  'q r r r s s s s s s s t t t t t'],
 ['x y z x y z  x y x y z x'],
 ['    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t '
  'u u u u u u v v v v v v w w w w w w x x x x  y y z z z z z a g g h h h h i j j j k k k k l l l '
  'l m n o p q  r r s s s s s s s t t t t t'],
 ['    x      a b c d e f   a g   g h h h h i j j j k k k k l l l l m n o p q r r r  s s s s s s s '
  't t t t t'],
 ['l m m m m m m m m n n n n n n n n n n n n n  p p q q r r s'],
 ['     a b    s s s s s t t t t t t t t u v w x y z'],
 ['x y a a a b b d d d d f f f g h i i i i i j j j  j k k k k l l l l m n o p q r r r s s s s s s '
  's t t t   t t t t   x      a b c d e f   a g  g h h h h i j j j k k k k l l l l m n o p q r r r '
  's s s s s s s t t t t t v w'],
 ['x y z x y z x y z l     a a a a b b d d d d f f f g h i  x y z x y z x y z x y z x y z x'],
 ['k'],
 ['    x      a b c d e f   a g g h h h h i    a b        c d e f   a g g h h h i j j j k k k l l '
  'l l m n o p q r r r  s s s s s s s t t t t t t t t u v w x y z j j j k k k k l l l l m n o p q '
  'r r r s s s s s s s t t t t t'],
 ['l     a a a a b b d  d d d f f f g h i  '],
 ['o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t u u u u u u v v v v v v '
  'w w w w w w x x x  z z'],
 ['l     a a a a b b d  d d d f f f g h i'],
 ['x y a a a o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t u u u u u u v '
  'v v v v v w w w w w w x x x x  y y z z z z z s s s s s s s t t t t t t t t u v w'],
 ['y'],
 ['    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t '
  'u u u u u u v v v v v v w w w w w w x x x x  y y z z z z z a g g h h h h i j j j k k k k l l l '
  'l m n o p q r r r s s s s s s s t t t t t   a a a a b b d d d d f f f g h i  '],
 ['x y z x y z  x y z x y z x y z x y z  x'],
 ['    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t '
  'u u u u u u v v v v v v w w w w w w x x x x  y y z z z z z a g g h h h h i j j j k k k k l  l l '
  'l m n o p q r r r s s s s s s s t t t t t   a a a a b b d d d d f f f g h i  '],
 ['l a b b d  d d d f f f g h i'],
 ['x y z x y z  x y z x y z x y z x y z e y z  x'],
 ['    x      a b c d e f   a g g h h h h i j j j k k k k l l l l m n o p q r r r s s s s s s s t '
  't t  t'],
 ['x y z x y z  x y z o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t u u '
  'u u u u v v v v v v w w w w w w x x x x x x y y y y y z z z z z y z e y z  x'],
 ['x x y y z z'],
 ['     a a a a b b d d d d f f f g  h i  '],
 ['    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t '
  'u u u u u u v v v v v v w w w w w w x x x x  y s s t t t t t'],
 ['     a a a a b b x y z x y z x y z l     a a a a b b d d d d f f f g h i  x y z x y z x y z x y '
  'z x y z x'],
 ['x y z x  z x y z x y z x'],
 ['l     a a a a  b b d d d d f f f g h i  '],
 ['x y a a a b b d d d d f f f g h i i i i i j j j  j k k k k l l l l m n o p q r r r s s s s s s '
  's t t t   t t t t   x      a b c d e f  x y a a a b b d d d d f f f g h i i i i i j j j  j k k '
  'k k l l l l m n o p q r r r s s s s s s s t t t   t t t t     x      a b c d e f   a g  g h h h '
  'h i j j j k k k k l l l l m n o p q r r r s s s s s s s t t t t t v w a g  g h h h h i j j j k '
  'k k k l l l l m n o p q r r r s s s s s s s t t t t t v w'],
 ['    a b   k k l l l l m n o p q r r r  s s s s s s s t t t t  t t t t u v w x y z'],
 ['x y a a a b b d d  d d f f f g h i i i i i j j j  j k k k k l l l l m n o p q r r r s s s s  s '
  's s t t t   t t t t t u v w'],
 ['p p q q q r r r s s s t t t  u u u v v w w x x y y z z'],
 ['o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t u u u u u u v v v v v '
  'z'],
 ['x y z x y z  x y z x y z x y z z x y z x  y z x'],
 ['x y a a a b b d d d d f f f g h i i i i i j j j  j k k k k l l l l m n o p q r r r s s s s s s '
  's t t t   t t t t   x      a b c d e f   a g  g h    a b   k k l l l l m n o p q r r r  s s s s '
  's s s t t t t t t t t u v w x y z h h h i j j j k k k k l l l l m n o p q r r r s s s s s s s t '
  't t t t v w'],
 ['x y a a a b b d d d d f f f g h i i i i i j j j  j k k k k l l l l m n o p q r r r s s s s s s '
  's t t t   t t t t     x  j    a b c d e f   a g  g h h h h i j j j k k k k l l l l m n o p q r '
  'r r s s s s s s s t t t t t v w'],
 ['o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t u u u u u u v v v v v v '
  'w w w w w w x x x x x x y     a a a a b b d d d d f f f g h i  p y y y y z z z z z'],
 ['    a b   k k l l l l m n o p q r r r  s s s s s s s t t t t t  t t t u v w x y z'],
 ['x y z x y z  x y z  x y z x y z z x y z x  y z x'],
 ['    x      a b c d e f   a g   g h h h h  i j j j k k k k l l l l m n o p q r r r s s s s s s s '
  't t t t t'],
 ['    a b       a b    s s s s s t t t t t t t t u v w x y z k k  l l l l m n o p q r r r  s s s '
  's s s s t t t t t t t t u v w x y z'],
 ['x y z x y z  x y z x y z x  y z z x y z x y z x'],
 ['x y a a a b b d d  d d f f f g l m n o p q r r r s s s s  s s s t t t   t t t t t    a b        '
  'c d e f   a g g h h h i j j j k k k l l l l m n o p q r r r  s s s s s s s t t t t t t t t u v '
  'w x y z v w'],
 ['x y z x y z  x y z  x y z x y z z x y z    x      a b c d e f   a g g h h h h i j j j k k k k l '
  'l l l m n o p q r r r s s s s s s s t t t  t x  y z x'],
 ['    x      a b c d e f   a g   g h l     a a a a  b b d d d d f f f g h i  h h h i j j j k k k '
  'k l l l l m n o p q r r r  s s s s s s s t t t t t'],
 ['x y a a a b b d d d d f f f g h i i i i  i j j j j k k k k l l l l m t t t u v w'],
 ['c a a a a i'],
 ['    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t '
  'u u u u u u v    a b       a b    s s s s s t t t t t t t t u v w x y z k k  l l l l m n o p q '
  'r r r  s s s s s s s t t t t t t t t u v w x y z v v v v v w w w w w w x x x x  y y z z z z z a '
  'g g h h h h i j j j k k k k l l l l m n o p q  r r s s s s s s s t t t t t'],
 ['    x      a b c d e f    a g   g h h h h  i j j j k k k k l l l l m n o p q r r r s s s s s s '
  's t t t t t'],
 ['c a a a  a i'],
 ['x y z x y z  x y z x y z x  y z x'],
 ['x y z x y z x y z x y z x y z x  z x y z x y z x z x y z x y z x y z x'],
 ['l    a b   k k l l t t t t t t u v w x y z'],
 ['     a b   k k l l t t t t t t u v w    x      a b c d e f  o o o o o o p p p p p p q q q q q q '
  'r r r r r r s s s s s s t t t t t t u u u u u u v v v v v v w w w w w w x x x x  y y z z z z z '
  'a g g h h h h i j j j k k k k l  l l l m n o p q r r r s s s s s s s t t t t t   a a a a b b d '
  'd d d f f f g h i  x y z'],
 ['    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t  t t t '
  't u u u u u u v v v v v v w w w w w w x x x x  y y z z z z z a g g h h h h i j j j k k k k l l '
  'l l m n o p q r r r s s s s s s s t t t t t'],
 ['     a b    k k l l t t t t t t u v w x y z'],
 ['x y z x y z x y     a b   k k l l t t t t t t u v w x y z z x y z x y z x y z x y z x y z x'],
 ['    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t '
  'u u u u u u v    a b       a b    s s s s s t t t t t t t t u v w x y z k k  l l l l m n o  p q '
  'r r r  s s s s s s s t t x x  y y z z z z z a g g h h h h i j j j k k k k l l l l m n o p q  r '
  'r s s s s s s s t t t t t'],
 ['x y z x y z  x y z  x y z x y z z x y z    x      a b c d e f   a g g h h h h i j j j k k k k l '
  'l m n o p q r r r s s s s s s s t t t  t x  y z x'],
 ['l     a a a  a b b  f f g h i  '],
 ['x y z x y z  x y z x y z x y z x y z e y z  '],
 ['c a a a  a i    a b        c d e f   a g g h  h h i j j j k k k l l l l m n o p q r r r s s s s '
  's s s t t t t t t t t u v w x y z'],
 ['x y z x y z x y z x y z z x y z x y z x y z x'],
 ['l     f f f g h i  '],
 ['x y z x y z  x y z x y z x y z z x y z x  y z  x'],
 ['o o o o o o p p p p p p q q q q q q r r r r r    x      a b c d e f  o o o o o o p p p p p p q '
  'q q q q q r r r r r r s s s s s s t t t t t t u u u u u u v    a b       a b    s s s s s t t t '
  't t t t t u v w x y z k k  l l l l m n o  p q r r r  s s s s s s s t t x x  y y z z z z z a g g '
  'h h h h i j j j k k k k l l l l m n o p q  r r s s s s s s s t t t t t r s s s s s s t t t t t '
  't u u u u u u v v v v v v w w w w w w x x x x x x y y y y y z z z z z'],
 ['x y a a a o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t u u u u u u v '
  'v v v v v w w w w w w x x x x  y y z z z z z s s s s s t t t t t t t t u v w'],
 ['     a b   k k l l t t t t l     a a a a  b   b d d d d f f f g h i  t t u v w x y z'],
 ['x y z x y z x y     a b   k k l l t  t t t t t u v w x y z z x y z x y z x y z x y z x y z x'],
 ['x y z x y z   x y z o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t u u '
  'u u u u v v v v v v w w w w w w x x x x x x y y y y y z z z z z y z e y z  x'],
 ['    o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t u u u u u u v v v v '
  'v v w w w w w w x x x x  y y z z z z z a a a a b b d d d d f f f g  h i  '],
 ['x y a a a b b d d d d f f f g h i i i i i j j j  j k k k k l l l l m n o p q r r r s s s s s s '
  's t t t    t t t t t u v  w'],
 ['x y a a a b b d d d d f f f g h i i i i i j j j  j k k k k l l l l m n o p q r r r s s s s s s '
  's t t t   t t t t     x  j    a b c d e f   a g  g h h h  j j k k k k l l l l m n o p q r r r s '
  's s s s s s t t t t t v w'],
 ['x y z x y z  x y z  x y z x y z z x    a b        c d e f   a g g h h h i j a b c d e f g h i j '
  'k l m n o p q r s t u v w x y z a b c d e f g h i j k l m n o p q r s t u v w x y z a b c d e f '
  'g m n o p q r r r s s s s s s s t t t t t t t t u v w x y z y z    x      a b c d e f   a g g h '
  'h h h i j j j k k k k l l m n o p q r r r s s s s s s s t t t  t x  y z x'],
 ['x y a a a b b d d d d f f f g h i i i i i j j j  j k k k k l l l l m n o p q r r r s s s s s s '
  's t t t   t t t t     x  j    a b c d e f   a g  g h h h h i j j j k k k k l l l l m n o p q r '
  'r r s s s s s s s t t t t t v  w'],
 ['l      a a a  a b b  f f g h i  '],
 ['c a a a a b b d f g h i'],
 ['    a b        c d e f   a g g h h h i j j j k k k l l l l m n o p q r r r  s s s s s s s t t t '
  't     a b   k k l l t t t t l     a a a a  b   b d d d d f f f g h i  t t u v w x y z t  t t t '
  'u v w x y z'],
 ['l     a a a  a b b  f f g  i  '],
 ['    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s s    x      a b c d '
  'e f   a g g h h h h i j j j k k k k l l l l m n o p q r r r s s s s s s s t t t  t s s s t t t '
  't t t u u u u u u v v v v v v w w w w w w x x x x  y y z z z z z a g g h h h h i j j j k k k k '
  'l l l l m n o p q  r r s s s s s s s t t t t t'],
 ['    a b   k k l l  l l m n o p q r r r  s s s s s s s t t t t  t t t t u v w x y z'],
 ['    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t '
  'u u u u u u v v v v v v w w w w w w x x x x  y y z z z z z a g g h h h h i j j j k k k k l l l '
  'l m n o p q r r r s s s s s s s t t t t t   a a     x      a b c d e f  o o o o o o p p p p p p '
  'q q q q q q r r r r r r s s s s s s t t t t t t u u u u u u v v v v v v w w w w w w x x x x  y '
  'y z z z z z a g g h h h h i j j j k k k k l l l l m n o p q r r r s s s s s s s t t t t t   a a '
  'a a b b d d d d f f f g h i  a a b b d d d d f f f g h i  '],
 ['l     a a a  a b b d  d d d f f f g h i  '],
 ['x y z x y z  x y z  x y z x y z z x y z    x      a b c d e f   a g g h h h h  i j j j k k k k '
  'l l l l m n o p q r r r s s s s s s s t t t  t x  y z x'],
 ['    x      a b c d e f  o o o o o o p p p p p p  q q q q q q r r r r r r s s s s s s t t t t t '
  't u u u u u u v    a b       a b    s s s s s t t t t t t t t u v w x y z k k  l l l l m n o p '
  'q r r r  s s s s s s s t t t t t t t t u v w x y z v v v v v w w w w w w x x x x  y y z z z z z '
  'a g g h h h h i j j j k k k k l l l l m n o p q  r r s s s s s s s t t t t t'],
 ['l     a a a  a b b  f f g  i '],
 ['x y z x y z  x y z  x y z x y z z x    a b        c d e f   a g g h h x y a a a b b d d d d f f '
  'f g h i i i i i j j j  j k k k k l l l l m n o p q r r r s s s s s s s t t t   t t t t t u v w '
  'h h i j j j k k k k l l m n o p q r r r s s s s s s s t t t  t x  y z x'],
 ['    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t '
  'u u u u u u v    a b        a b    s s s s s t t t t t t t t u v w x y z k k  l l l l m n o  p '
  'q r r r  s s s s s s s t t x x  y y z z z z z a g g h h h h i j j j k k k k l l l l m n o p q  '
  'r r s s s s s s s t t t t t'],
 ['      a b   k k l l t t t t t t u v w x y z'],
 ['x y a a a b b d d d d f f f g h i i i i i  j j j  j k k k k l l l l m n o p q r r r s s s s s s '
  's t t t t t t t u v w'],
 ['    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t '
  'u u u u u u v    a b       a b    s s s s s t t t t t t t t u v w x y z k k  l l l l m n o p q '
  'r r r  s s s s s s s t t t t t t t t u v w x y z v v v v v w w w w w w x x x x  y y z z z z z a '
  'g g h h h h i j j j k k k k l l l l m n o p q  r r s s s s  s s s t t t t t'],
 ['    a b   k k l l l l m n o p q r r r  s s s s s s s  t t t t t t t t u v w x y z'],
 ['l      a a a  a b b d  d d d f f f g h i  '],
 ['    x      a b c d e f   a g g h h h h  i    a b        s s t t t t t t t t u v w x y z j j j k '
  'k k k l l l l m n o p q r r r s s s s s s s t t t t t'],
 ['x y a a a b b d d d d f f f g h i i i i i j j j  j k k k k l l l l m n o p q r r r s     a a a '
  'a b b x y z x y z x y z l     a a a a b b d d d d f f f g h i  x y z x y z x y z x y z x y z x '
  's s s s s s t t t   t t t t t u v  w'],
 ['    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t  t t t '
  't u u u u u u v v v v v v w w w w w w x x x x  y y z z z z z a g g h h h h i j j j k k k k l l '
  'l l m n o p q r r r s s s s s s s t t    a b   k k l l l l m n o p q r r r  s s s s s s s t t t '
  't t t t t u v w x y z t t t'],
 ['x y a a a b b d d d d f f f g h i i i i i  j j j  j k s s s s t t t t t t t t u v w'],
 ['    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t '
  'u u u u u u v    a b        a b    s s s s s t t t t t t t t u v w x y z k k  l l l l m n o  p '
  'q r r r  s s s  s s s s s t t t t t'],
 ['x y a a a b b d d d d f f f g h  i i i i i j j j  j k k k k l l l l m n o p q r r r s s s s s s '
  's t t t   t t t t t u v w'],
 ['    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t  t t t '
  't u u u u u u v v v v v v w w w w w w x x x x  y  y z z z z z a g g h h h h i j j j k k k k l l '
  'l l m n o p q r r r s s s s s s s t t    a b   k k l l l l m n o p q r r r  s s s s s s s t t t '
  't t t t t u v w x y z t t t'],
 ['    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s s    x      a b c d '
  'e f   a g g h h h h i j j j k k k k l l l l     a a a  a b b  f f g  i  l m n o p q r r r s s s '
  's s s s t t t  t s s s t t t t t t u u u u u u v v v l l l m n o p q  r r s s s s s s s t t t t '
  't'],
 ['x y z x y z x  y z l     a a a a b b d d d d f f f g h i  x y z x y z x y z x y z x y z x'],
 ['x y a a a b b d d d d  f f f g h i i i i i j j j  j k k k k l l l l m n o p q r r r s s s s s s '
  's t t t   t t t t t u v  w'],
 ['x y z x y z  x  y z  x y z x y z z x y z x  y z x'],
 ['    x      a b c d e f   a g g h h h h i    a b        c  d e f   a g g h h h i j j j k k k l l '
  'l l m n o p q r r r  s s s s s s s t t t t t t t t u v w x y z j j j k k k k l l l l m n o p q '
  'r r r s s s s s s s t t t t t'],
 ['l a b b d  d d d f f    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s '
  's s s s t t t t t t u u u u u u v v v v v v w w w w w w x x x x  y y z z z z z a g g h h h h i '
  'j j j k k k k l l l l m n o p q r r r s s s s s  s s t t t t t   a a     x      a b c d e f  o '
  'o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t u u u u u u v v v v v v w '
  'w w w w w x x x x  y y z z z z z a g g h h h h i j j j k k k k l l l l m n o p q r r r s s s s '
  's s s t t t t t   a a a a b b d d d d f f f g h i  a a b b d d d d f f f g h i   f g h i'],
 ['x y z x y z  x y z x y z x y z x y z x y z x y z u x'],
 ['l     a a a  a b b      a b   k k l l t t t t t t u v w x y z f f g h i  '],
 ['t    a b   k k l l  l l m n o p q r r r  s s s s s s s t t t t  t t t t u v w x y z'],
 ['x y a a a b b d d d d f f f g      a a a a b b x y z x y z x y z l     a a a a b b d d d d f f '
  'f g h i  x y z x y z x y z x y z x y z x i i i i  i j j j j k k k k l l l l m t t t u v w'],
 ['x y z x y z   x y z o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t u u '
  'u u u u v v v v v v w w w w w w x x x x x x y y y y y    x      a b c d e f  o o o o o o p p p '
  'p p p q q q q q q r r r r r r s s s s s s t t t t t t u u u u u u v    a b        a b    s s s '
  's s t t t t t t t t u v w x y z k k  l l l l m n o  p q r r r  s s s  s s s s s t t t t t z z z '
  'z z y z e y z  x'],
 ['    a b   k k l l l l m n o p q r r r  s s s s s s s t t t t t  t t t u v  z'],
 ['x y z x y z x y     a b   k k l l t t t t t t u v w x y z z x y z x y z x y z x y z x y z     a '
  'b   k k l l t t t t t t u v w x y z'],
 ['    x t t t t t'],
 ['x y z x y z  x y z x y z  x  y z x'],
 ['x y z x y z  x y z x y z x y z z x y  z x  y z x'],
 ['x y z x y z  x y z  x y z x y z z x    a b        c d e f   a g g h h h i j a b c d e f g h i j '
  'k l m n o p q r s t u v w x y z a b c d e f g h i j k l m n o p q r s t u v w x y  z a b c d e '
  'f g m n o p q r r r s s s s s s s t t t t t t t t u v w x y z y z    x      a b c d e f   a g g '
  'h h h h i j j j k k k k l l m n o p q r r r s s s s s s s t t t  t x  y z x'],
 ['    o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s  t t t u u u u u u v v v v v v '
  'w w w w w w x x x x  y y z z z z z a a a a b    x t t t t t b d d d d f f f g  h i  '],
 ['l     f f f g h  i  '],
 ['x y z x y    x      a b c d e f    a g   g h h h h  i j j j k k k k l l l l m n o p q r r r s s '
  's s s s s t t t t t z  x y z x y z x y z z x y  z x  y z x'],
 ['    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t '
  'u u u u u u v    a b        a b    s s s s s  t t t t t t t t u v w x y z k k  l l l l m n o  p '
  'q r r r  s s s  s s s s s t t t t t'],
 ['    x      a b c d e f  o o o o o o p p p p p p  q q q q q q r r r r r r s s s s s s t t t t t '
  't u u u u u u v    a b       a b    s s s s s t t t t t t t t u v w x y z k k  l l l l m n o p '
  'q r r r  s s s s s s s t t t t t t t t u v w x y z v  v v v v w w w w w w x x x x  y y z z z z '
  'z a g g h h h h i j j j k k k k l l l l m n o p q  r r s s s s s s s t t t t t'],
 ['o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t u u u u u u v v v v v v '
  'w w w w  z'],
 ['l     a a a  a b b      a b   k k l l t  t t t t t u v w x y z f f g h i  '],
 ['   h x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t '
  't u u u u u u v    a b       a b    s s s s s t t t t t t t t u v w x y z k k  l l l l m n o p '
  'q r r r  s s s s s s s t t t t t t t t u v w x y z v v v v v w w w w w w x x x x  y y z z z z z '
  'a g g h h h h i j j j k k k k l l l l m n o p q  r r s s s s  s s s t t t t t'],
 ['x y z x'],
 ['o o u u u v v v v v v w w w w w w x x x  z z'],
 ['x y z x y z x y z x y z x y z x  z x y z x y z x z x y z x y z x'],
 ['    a b        c d e f   a g g h h h i j a b c d e f g h i j k l m n o p q r s t u v w x y z a '
  'b c d e f g h i j k l m n o p q s t u v w x y z a b c d e f g m n o p q r r r s s s s s s s t t '
  't t t t t t u v w x y z'],
 ['x y z x y z   x y z o o o o o o p p p p p p q q q q q q r r r r r r s s s s s  s t t t t t t u '
  'u u u u u v v v v v v w w w w w w x x x x x x y y y y y z z z z z y z e y z  x'],
 ['x z x'],
 ['x y z x y z  x y z x y z z e y z  x'],
 ['x y z x y z   x y z o o o o o o p p p p p p q q q q q q r r r r r r s s s s s  s t v v v v v w '
  'w w w w w x x x x x x y y y y y z z z z z y z e y z  x'],
 ['s    a b   k k l l  l l m n o p q r r r  s s s s s s s t t t t  t t t t u v w x y z'],
 ['x y y z x y z  x y z x y z x  y z z x y z x y z x'],
 ['x y z x y z  x y z  x y z x y z z x y z    x      a b c d e f   a g g h h h h i j j j k k  k k '
  'l l l t x  y z x'],
 ['l      a a a  a   f f g h i  '],
 ['x y z x y z x y z x y z x y  z x y z     a a a a b b x y z x y z x y z l     a a a a b b d d d '
  'd f f f g h i  x y z x y z x y z x y z x y z x x y z x  y z x'],
 ['x y z x y z   x y z o o o o o o p p p p p p q q q q q q r r r r r r s s s s s  s t v v v v v w '
  'w w w w w x x x x x x y y y y y z z z z z y  z e y z  x'],
 ['     a a a a c a a a  a i    a b        c d e f   a g g h  h h i j j j k k k l l l l m n o p q '
  'r r r s s s s s s s t t t t t t t t u v w x y z  h i  '],
 ['p p q q q r r r s s s  y y z z'],
 ['x y z x y z  x y z x y z   x  y z x'],
 ['    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t '
  'u u u u u u v    a b       a b    s s s s s t t t t t t t t u v w x y z k k  l l l l m n o  p q '
  'r r r  s s s s s s s t t x x  y y z z z z z a g g h h h h i j j j k k k k l l  n o p q  r r s s '
  's s s s s t t t t t'],
 ['c a    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t  t t '
  't t u u u u u u v v v v v v w w w w w w x x x x  y  y z z z z z a g g h h h h i j j j k k k k l '
  'l l l m n o p q r r r s s s s s s s t t    a b   k k l l l l m n o p q r r r  s s s s s s s t t '
  't t t t t t u v w x y z t t t a a a b b d f g h i'],
 ['x y z x  x y z x  y z x'],
 ['     a b   k k l l t t t t l     a a a a  b   x y z x y z  x y z x y z x y z x y z e y z   u v '
  'w x y z'],
 [' x y z x y z x  y z l     a a a a b b d d d d f f f g h i  x y z x y z x y z x y z x y z x   '
  'x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t u u '
  'u u u u v    a b        a b    s s s s s t t t t t t t t u v w x y z k k  l l l l m n o  p q r '
  'r r  s s s s s s s t t x x  y y z z z z z a g g h h h h i j j j k k k k l l l l m n o p q  r r '
  's s s s s s s t t t t t'],
 ['    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t '
  'u u u u u u v    a b        a b    s s s s  s  t t t t t t t t u v w x y z k k  l s t t t t t'],
 ['     a b   k k l l t t t t l     a a a a  b   x y z x y z   u v w x y z'],
 ['     a b   k k l l t t t t l     a a a a  b   x y z x y z  x y z x y z x y z x y  y z'],
 ['x y z x y z x y z x y z x y z x y z x y z x'],
 ['x y z x y z  x y z  x y z x y z z x y z    x      a b c d e f   a g g h h h h i j j j k k k k l '
  'l m n o p q r r r  s s s s s s s t t t  t x  y z x'],
 ['x y  z x y z  x y z x y z x y z z x y z x  y z  x'],
 ['    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t  t t t '
  't u u u u u u v v v v v v w w w w w w x x x x  y  y z z z z z a g g h h h h i j j j k k k k l l '
  'l l m n o p q r r r s s s s s s s t t    a b   k k l l l l m n o p q r r r  s s s s s s s t t t '
  't t t t t u v w x y z t t '],
 ['l     a a a  a b b      a b   k k l l t  t t t t t u v w     a b   k k l l t t t t l     a a a '
  'a  b   x y z x y z  x y z x y z x y z x y z e y z   u v w x y z x y z f f g h i  '],
 ['x y z x y z  x y z  x y z x y z z x y z    x      a b c d e f   a g g h h h h i j j j k k k k l '
  'l m n o p q r r r s t x  y z x'],
 ['x l     a a a a  b b d d d d f f f g h i  y z x y z  x y x y z x'],
 ['c a    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t  t t '
  't t u u u u u u v v v v v v w w w w w w x x x x  y  y z z z z z a g g h h h h i j j j k k k k l '
  'l l l m n o p q r r r s s s s s s s t t    a b   k k l l l l m n o p q r r r  s s s s s s s t t '
  't t t t t    a b   k k l l t t t t t t u v w x y z t u v w x y z t t t a a a b b d f g h i'],
 ['x y a a a o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t u u u u u u v '
  'v v v v v w w w w w w x x x x  y y z z z z z s s s s  u v w'],
 ['    a b   k    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s '
  't t t t t t u u u u u u v    a b        a b    s s s s  s  t t t t t t t t u v w x y z k k  l s '
  't t t t t k l l t t t t t t u v w x y z'],
 ['x y z x y z   x y z o o o o o o p p p p p p q q q q q q r r r r r r s s s s s  s y z  x'],
 ['o o u u u v v v v v v w w w w w'],
 ['p p  s t t t u u u v v w w x x y y z z'],
 ['x y z x y z  x y z  x y z x y z z x    a b        c d e f   a g g h h h i j a b c d e f g h i j '
  'k l m n o p q r s t u v w x y z a b c d e f g h i j k l m n o p q r  s t u v w x y z a b c d e '
  'f g m n o p q r r r s s s s s s s t t t t t t t t u v w x y z y z    x      a b c d e f   a g g '
  'h h h h i j j j k k k k l l m n o p q r r r s s s s s s s t t t  t x  y z x'],
 ['x y z x y z     a b   k k l l  l l m n o p q r r r  s s s s s s s t t t t  t t t t u v w x y z '
  'y z x y z x y z x y z x y z x y z u x'],
 ['    x      a b c d e f  o t u u u u u u v    a b        a b    s s s s  s  t t t t t t t t u v '
  'w x y z k k  l s t t t t t'],
 ['x y z x y z x y     a b   k k l l t  t t t t t u v w x y z z x y z x y z x y z x  y z x y z x'],
 ['l  f f f g h  i  '],
 ['    a b   k k l l l l m n o p q r r r  s s s s s    x      a b c d e f   a g g h h h h  i    a '
  'b        s s t t t t t t t t u v w x y z j j j k k k k l l l l m n o p q r r r s s s s s s s t '
  't t t t t t t u v  z'],
 ['c a a a a b b d d d d f f  f g h i'],
 ['x y a a a b b d d d d f f f g      a a a a b b x y z x y z x y z l     a a a a b b d d d d f f '
  'f g h i  x y z x y z x y z x y z x y z x i i i i  i j j j j k k k k l l l l m t t t u v w   a a '
  'a  a b b      a b   k k l l t  t t t t t u v w x y z f f g h i  '],
 ['l     a a a  a b b  f f g x y a a a b b d d d d f f f g h i i i i i j j j j k k k k l l l l m n '
  'o p q r r r s s s s s s s t t t t t t t t u v w i  '],
 ['x y z x y  z  x y z x y z   x  y z x'],
 ['    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t '
  'u u u u u u v v v v v v w w w w w w x x x x  y y z z z z z a g g h h h h i j j j k k k k l l l '
  'l  m n o p q  r r s s s s s s s t t t t t'],
 ['    a b   k k l l l l m n o p q r r r  s s s s s s s   v w x y z'],
 ['    a b        c d e f   a g g h h h i j a b c d e f g h i j k l m n o p q r s t u v w x y z a '
  'b c d e f g h i j k l m n o p q r s t u v w x y z a b c d e f g m n o    x      a b c d e f  o '
  'o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t u u u u u u v    a '
  'b        a b    s s s s  s  t t t t t t t t u v w x y z k k  l s t t t t t p q r r r s s s s s '
  's s t t t t t t t t u v w x y z'],
 ['    o o o  v w w w w w w x x   h i  '],
 ['     x t t t t t'],
 ['    a b   k k l l  l l m n o   t t t t u v w x y z'],
 ['o o o o o o p p p  r r r s s s s s s t t t t t t u u u u u u v v v v v z'],
 ['    x      a b c d e f   a g g h h h h i    a b        c  d e f   a g g h h h i j j j k k k l l '
  'l l m n o p q r r r  s s s s s t t t t t'],
 ['    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t '
  'u u u u u u v v v v v v  w w w w w w x x x x  y y z z z z z a g g h h h h i j j j k k k k l l l '
  'l m n o p q  r r s s s s s s s t t t t t'],
 ['x y z x y z  x y z  x y z x y z z x    a b        c d e f   a g g h h h i j a b c d e f g h i j '
  'k l m n o p  q r s t u v w x y z a b c d e f g h i j k l m n o p q r s t u v w x y  z a b c d e '
  'f g m n o p q r r r s s s s s s s t t t t t t t t u v w x y z y z    x      a b c d e f   a g g '
  'h h h h i j j j k k k k l l m n o p q r r r s s s s s s s t t t  t x  y z x'],
 ['l     a a a  a b b  f f g  '],
 ['x  x'],
 ['l     a a a  a b b      a b   k k l l t t t t t t u v w x y z f f g h i '],
 ['x y a a a b b d d d d f f f g h i i i i i j j j  j k k k k l l l l m n o p q r r r u v w'],
 ['    a b        c d e f   a g g h h h i j j j k k k l l l l m n o     a b    k k l l t t t t t t '
  'u v w x y z p q r r r s s s s s s s t t t t t t t t u v w x y z'],
 ['    x      a b c d e f    a g g h h h h i    a b        c  d e f   a g g h h h i j j j k k k l '
  'l l l m n o p q r r r  s s s s s s s t t t t t t t t u v w x y z j j j k k k k l l l l m n o p '
  'q r r r s s s s s s s t t t t t'],
 ['    x    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t '
  't t t u u u u u u v v v v v v  w w w w w w x x x x  y y z z z z z a g g h h h h i j j j k k k k '
  'l l l l m n o p q  r r s s s s s s s t t t t t      a b c d e f  o o o o o o p p p p p p q q q '
  'q q q r r r r r r s s s s s  s t t  t t t t u u u u u u v v v v v v w w w w w w x x x x  y  y z '
  'z z z z a g g h h h h i j j j k k k k l l l l m n o p q r r r s s s s s s s t t    a b   k k l '
  'l l l m n o p q r r r  s s s s s s s t t t t t t t t u v w x y z t t '],
 ['x y z x y  z  x y z x y z   x  y z '],
 ['x y a a a b b d d d d f f f g h i i i i i j j j  j k k k k l l l l m n o p q r r r s s s s s s '
  's t t t   t t t t   x      a b c d e f   a  g  g h h h h i j j j k k k k l l l l m n o p q r r '
  'r s s s s s s s t t t t t v w'],
 ['c a  a a a b b d f g h i'],
 ['    x t t t t'],
 ['p p  s t t t u u u v    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s '
  's s s s t t t t t t u u u u u u v v v v v v w w w w w w x x x x  y y z z z z z a g g h h h h i '
  'j j j k k k k l l l l m n o p q r r r s s s s s s s t t t t t v w w x x y y z z'],
 ['l     a a a  a  '],
 ['     a b   k k l l t t t z'],
 ['p p  s t t t u u u v    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r r r r r s s '
  's s s s t t t t t t u u q r r r s s s s s s s t t t t  t v w w x x y y z z'],
 ['    a b     a b    s s s s s t t t t t t t t u v w x y z       a b    s s s s s t t t t t t t t '
  'u v w x y z k k  l l l l m n o p q r r r  s s s s s s s t t t t t t t t u v w x y z'],
 ['x y z x y z x x y z x y z x y z x y z  x'],
 ['l    p p q q q r r r s s s t t t u u u v v w w x x y y z z a a a a  b b d d d d f f f g h i  '],
 ['t    a b   k k l l  l l m n o p q r r r   s s s s s s s t t t t  t t t t u v w x y z'],
 ['    x      a b c d e f   a g g h h h h i    a b        c  d e f   a g g h h h i j j j k k      '
  'a b   k k l l t t t t t t u v w    x      a b c d e f  o o o o o o p p p p p p q q q q q q r r '
  'r r r r s s s s s s t t t t t t u u u u u u v v v v v v w w w w w w x x x x  y y z z z z z a g '
  'g h h h h i j j j k k k k l  l l l m n o p q r r r s s s s s s s t t t t t   a a a a b b d d d '
  'd f f f g h i  x y z o p q r r r  s s s s s t t t t t'],
 ['x y z x  z x y z x  y  x'],
 ['x y z x y z  x y z  x y z x y z z x y z    x      a b c d e f   a g  g h h h h  i j j j k k k k '
  'l l l l m n o p q r r r s s s s s s s t t t  t x  y z x'],
 ['x y z x y z  x y z x y z x y  z z x y z x  y z  x'],
 ['a a b b c c d d'],
 ['x x x x x'],
 ['a b c d a b c d a b c d'],
 [' a'],
 ['ä å ö'],
 ['    x      a b c d e f   a g g  t t'],
 ['    x      a b  c d e f   a g g  t t'],
 ['l m m m m m m m m n n n n n n n n n n n n n n o o p p q  q r r s'],
 ['    x      a  b  c d e f   a g g  t t'],
 ['c a a a a b b d d d d f f f  g h i'],
 ['    a b        c d e f   a g g h h h i j j j k k k l l l l m n o p q r r r s s s s s s s t t t '
  't t t t t u v w x y '],
 ['      g h i  '],
 ['o o o o o o p p p p p  p q  q q q q q r r r r r r s s s s s  y y y z z z z z'],
 ['x y a a a b b d d d d f f f g h i i i i i j j j j k k k k l l l l m n p q r r r s s s s s s s t '
  't t t t t t t u v w'],
 ['c       g h i  '],
 ['  o t x      a b c d e f   a g g  t t'],
 ['     a a a a b b d d d d f f f g h    a b        c d e f   a g g h h h i j j j k k k l l l l m '
  'n o p q r r r s s s s s s s t t t t t t t t u v w x y   '],
 ['    x b     a  b  c d e f   a g g  t t'],
 ['l m  m m m m m m m n n n n n n n n n n n n n n o o p p q q r r s'],
 ['o o o o o o p p p p p p q q q q  q q r r r r r r s s s s s s t t t t t t u u u u u u v v v v v '
  'v w w w w w w x x x x x x y y y y y z z z z z'],
 ['    a b        c d e f   a g g h h h i j j j k k k l l l l m n o p q r r r s s s s s s s t t t '
  't t  t t t u v w x y z'],
 ['x y a a a b b d d d d f f f g h i i i i i j j j j k k k k l l l l m n p q r r r s s s s s s s t '
  't t t t    a b        c d e f   a g g h h h i j j j k k k l l l l m n o p q r r r s s s s s s s '
  't t t t t  t t t u v w x y z t t t u v w'],
 ['    x      a b c  d e f   a g  g h h h h i j j j k k k k l l l l m n o p q r r r s s s s s s s '
  't t t t t'],
 ['q'],
 ['  o t x  t    a b c d e f   a g g  t t'],
 ['     a a a a b b d d d d f f f g h i  e'],
 ['o o o o o o p p p p p  p q  q q q q q r r r r r r s s s    x      a b c d e f   a g g  t t s s  '
  'y y y z z z z z'],
 ['       a a a a b b d d d d f f f g h i    x      a b c d e f   a g g  t t'],
 ['l m m m m m m m m n n n n n n n n n n n n  n n o o p p q q r r s'],
 ['c a a a a b b d d d d  f f f g h i'],
 ['    a b        c d e f   a g g  h h h i j j j k k k l l l l m n o p q r r r s s s s s s s t t t '
  't t  t t t u v w x y z'],
 ['o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t u u z z z z z'],
 ['a b c d e f z b c d e f g'],
 ['l m m m m m m m m n n n n n n n n n n n n m n n o o p p q q r r s'],
 ['    a b        c d e f   a g g h h h i j j j k k k l l l l m n o p q r r r s s s t t t t t t t '
  't u v w x y '],
 ['    x b     a  b  c d e f   a t t'],
 ['    x      a  b  c d e  f   a g g  t t'],
 ['    x      a  b  c d e f e  a g g  t t'],
 ['o o o o o o p p p p p p q q q q q q r r r r r r s s s s s  s t t t t t t u u z z z z z'],
 ['    a b        c d e f   a g g h h h i j j j k k k l l l l m n o p  v w x y '],
 ['o o o o       a a a a b b d d d d f f f g h i    x      a b c d e f   a g g  t t o o p p p p p '
  'p q q q q q q r r r r r r s s s s s s t t t t t t u u z z z z z'],
 ['o o o o o o p p p p p p q q q q q q r r r r r r s s s s s  s t t t t t t u  u z z z z z'],
 ['o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t u u u u u u v v v v v v '
  'w w w w w w x x x x x x y y y y y z z'],
 ['  o o o o       a a a a b b d d d d f f f g h i    x      a b c d e f   a g g  t t o o p p p p '
  'p p q q q q q q r r r r r r s s s s s s t t t t t t u u z z z z z d e f   a t t'],
 ['    a b        c d e f   a g g h h h i  j j j k k k l l l l m n o p q r r r s s s s s s s t t t '
  't t t t t u v w x y z'],
 ['o o o o o o p p p p p p q q q q q q r r r r r s s s s s  s t t t t t t u u z z z z z'],
 ['    x      a b  c d e f   a g g  t'],
 ['o o o o o o p p p p p p q q q q q q r r r r r r s s s s s  s t t  t t t u  u z z z z z'],
 ['  o  t x      a  b c d e f   a g g  t t'],
 ['    x      a b  c d e f   a g g t'],
 ['a b c d e f g    x b     a  b  c d e f   a t t h i j k l m n o p q r s t u v w x y z a b c d e '
  'f g h i j k l m n o p q r s t u v w x y z a b c d e f g'],
 ['l m m m m  p p q q r r s'],
 ['    a b        c d e f   a g g h h s s s t t t t t t t t u v w x y z'],
 ['x y a a a b b d d d d f f f g h i i i i i j j j j k k k k l l l l m n p q r r r s s s s s s s t '
  'z t t t u v w'],
 ['    a b        c d e f   a g g h h h i j j j k k k l l l l m n o p q r r r s s s t t t t t t t '
  't u  v w x y '],
 ['    x      a b   c d e f   a g g t'],
 ['    a b        c d e f   a g g  h h h i j j j k k k l l l l m n o p q r r r s s s s s s s t t t '
  't      a a a a b b d d d d f f f g h    a b        c d e f   a g g h h h i j j j k k k l l l l '
  'm n o p q r r r s s s s s s s t t t t t t t t u v w x y   t  t t t u v w x y z'],
 ['x y a a a b b d d d d f f f g h i i i i i j j j  j j j k k k l l l l m n o p q r r r s s s s s '
  's s t t t t t  t t t u v w x y z t t t u v w'],
 ['o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t  u u z z z z z'],
 ['l m m m m m m m m n n  n n n n n n n n n n n n o o p p q q r r s'],
 ['l m  m m  m m m m m n n n n n n n n n n n n n n o o p p q q r r s'],
 ['  g    g h i  '],
 ['o o o o       a a a a b b d d d d f f f g h i    x      a b c d e f   a g g  t t o o p p p p p '
  'p q q q q q  q r r r r r r s s s s s s t t t t t t u u z z z z z'],
 ['o o o o  b     a a a a b b d d d d f f f g h i    x      a b c d e f   a g g  t t o o p p p p p '
  'p q q q q q q r r r r r r s s s s s s t t t t t t u u z z z z z'],
 ['p p q q q r r r s s s t t t u u u v v  g    g h i   w w x x y y z z'],
 ['  o o o o       a a a a b b d d d d f f  f g h i    x      a b c d e f   a g g  t t o o p p p p '
  'p p q q q q q q r r r r r r s s s s s s t t t t t t u u z z z z z d e f   a t t'],
 ['    a b        c d e  f   a g g h h h i j j j k k k l l l l m n o p q r r r s s s s s s s t t t '
  't t  t t t u v w x y z'],
 ['    x      a b c d e f   a g g    t'],
 ['o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t u u u u u u  v v v v v '
  'v w w w w w w x x x x x x y y y y y z z'],
 ['  o o o o        a a a a b b d d d d f f  f g h i    x      a b c d e f   a g g  t t o o p p p '
  'p p p q q q q q q r r r r r r s s s s s s t t t t t t u u z z z z z d e f   a t t'],
 ['d      g h i  '],
 ['o o o o  b     a a a a b b d d d d f f f g h i    x      a b c d e f   a g g  t t o o p p p p p '
  'p q q q q q q r r r r r r s s s s s s t t t t t t u u z z z z'],
 ['o o o o o o p  x x x x y y y y y z z'],
 ['p p q q r r r s s s t t t u u u v v w w x x y y z z'],
 ['o o o o o o p p p p p p q q q q q q r r r  z z'],
 ['a    x      a b c d e f   a g g h h h h i j j j k k k k l l l l m n o p q r r r s s s s s s s t '
  't t t t'],
 ['p p q q r r r s s  s t t t u u u v v w w x x y y z z'],
 ['l m m m m m m m m n n n n n n n n n n n n n n o o p p q o o o o o o p p p p p p q q q q q q r r '
  'r r r s s s s s  s t t t t t t u u z z z z z q r r s'],
 ['p p q q r r r s s s t t t u x x y y z z'],
 ['x y a a a b b d d d d f f f g h i i i i i j j j j k k k k l l l l m n p q r r r s s s s s s s t '
  't t t t    a b        c d e f   a g g h h h i j j j k k k l l l l m n o     a b        c d e '
  'f   a g g h h h i j j j k k k l l l l m n o p q r r r s s s s s s s t t t t t t t t u v w x y p '
  'q r r r s s s s s s s t t t t t  t t t u v w x y z t t t u v w'],
 ['    x b     a  b  c d e f    a g g  t t'],
 ['l m m m m m m m m n n n n n n n n n n n n n n o o p p q o o o o o p p p p p p q q q q q q r r r '
  'r r s s s s s  s t t t t t t u u z z z z z q r r s'],
 ['  o o o o        a a a a b b d d d d f f  f g h i    x      a b c d e f   a z s s t t t t t t u '
  'u z z z z z d e f   a t t'],
 ['    a b        c d e f   a g g h h h i j j j   o o o o       a a a a b b d d d d f f  f     a a '
  'a a b b d d d d f f f g h i  w x y z'],
 ['    x      a  b  c d e f  t'],
 ['    x      a  b  c d e f   a  g g  t t'],
 ['    x      a  b c d  e f   a g g  t t'],
 ['  o o o o       a a a a b b d d d d f f f g h i    x      a b c d e f   a g g  t t o o p p p p '
  'p p q q q q q q r r r r r r s s s s s s t t t t t t u u z z z z z d e f   a t  t'],
 ['    x       a  b  c d e  f   a  t t'],
 ['l m m m m m m m m n n n n n n n n n n n n  n n  o o o o        a a a a b b d d d d f f  f g h '
  'i    x      a b c d e f   a z s s t t t t t t u u z z z z z d e f   a t t r r s'],
 ['d      g h i d '],
 ['    x      a b  c d e  f   a g g  t t'],
 ['o o o o       a a a a b b d d d d f f f g h i    x      a b c d e f   a g g  t t o o p p p p p '
  'p q q q q q q r r r r r r s s s s s s t t  t t t t u u z z z z z'],
 ['o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t u u u  z z z z z'],
 ['o o o o o o p p  s s s s  y y y z z z z z'],
 ['    c d e f   a g g t'],
 ['    a b        c d e f   a g g  h h h i j j j k k k l l l l m n o p q r r r s s s s s s s t t t '
  't      a a a a b b d d d d f f f g h    a b        c d j j j k k k l l l l m n o p q r r r s s '
  's s s s s t t t t t t t t u v w x y   t  t t t u v w x y z'],
 ['    x b     a       a a a a b b d d d d f f f g h    a b        c d e f   a g g h h h i j j j k '
  'k k l l l l m n o p q r r r s s s s s s s t t t t t t t t u v w x y   b  c d e f   a g g  t t'],
 ['o o o o o o p p p p p p q q q q q q r r r    a b  s s s s s s t t t t      a a a a b b d d d d '
  'f f f g h    a b        c d j j j k k k l l l l m n o p q r r r s s s s s s s t t t t t t t t u '
  'v w x y   t  t t t u v w x y z r r r s s s s s s t t t t t t u u u  z z z z z'],
 ['l m m m  o t x  t    a b c d e f   a g g  t t m m m m m n n n n n n n n n n n n n n o o p p q o '
  'o o o o p p p p p p q q q q q q r r r r r s s s s s  s t t t t t t u u z z z z z q r r s'],
 ['    x      a g g    t'],
 ['    a b        c d e f   a g g h h h i j j j k k k l l l l m n o p q r  r r s s s t t t t t t t '
  't u v w x y '],
 ['p p q q q r r r s s s t t t u u u v v w  w x x y y z z'],
 ['c a  a a a b b d d d d  f f f g h i'],
 ['o o o o       a a a a b b d d d d f f f g h i    x      a b c d e f   a g g  t t o o p p  p p p '
  'p q q q q q  q r r r r r r s s s s s s t t t t t t u u z z z z z'],
 ['    a b        c d e f   a g g h h h s t t t t t t t t u v w x y '],
 ['o o o o o o p p p p p p q q q q q  q r r r r r r s s s s s s t t t t t t u u u u u u  v v v v v '
  'v w w w w w w x x x x x x y y y y y z z'],
 ['      a  b  c d e  f   a g g  t t'],
 ['     c a  a a a b b d d d d  f f f g h i g h i  '],
 ['o o o o o o p p p p p p q q q q q q r r r r r r s s s s s  s t t t t t t u u u  z z z z z'],
 ['    x       a b c d e f   a g g h h h h i j j j k k k k l l l l m n o p q r r r s s s s s s s t '
  't t t t'],
 ['l m m m m  p  p q q r r s'],
 ['o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t u u u u u u  v v v v x '
  'x x x y y y y y z z'],
 ['     b c d  e f   a g g  t t'],
 ['       a  b c d e f   a g g  t t'],
 ['    a b        f   a g g h h h i j j j k k k l l l l m n o p q r r r s s s t t t t t t t t u v '
  'w x y '],
 ['o o o o o o p p p p p p q q q q q  q r r r r r r s s s s s s t t t  z z'],
 ['    x    a b        c d e f   a g g h h h i j j j   o o o o       a a a a b b d d d d f f  '
  'f     a a a a b b d d d d f f f g h i  w x y z      a b c d e f   a g g  t t'],
 ['d       g h i d '],
 ['    x      a g g t'],
 ['x y a a a b b d d d d f f f g h i i i  i i j j j  j j j k k k l l l l m n o p q r r r s s s s s '
  's s t t t t t  t t t u v w x y z t t t u v w'],
 ['     a a a a b b f f g h i  e'],
 ['    a b        c d e f   a g g  h h h i j j j k k k l l l l m n o p q r r r s s s s s s s t t t '
  't  v    a a a a b b d d d d f f f g h    a b        c d j j j k k k l l l l m n o p q r r r s s '
  's s s s s t t t t t t t t u v w x y   t  t t t u v w x y z'],
 ['    x  o o o o        a a a a b b d d d d f f  f g h i    x      a b c d e f   a z s s t t t t '
  't t u u z z z z z d e f   a t t      a b c d e f   a g g  t t'],
 ['   g h i  '],
 ['   f   a g g h h h i j j j k k k l l l l m n o p q r r r s s s s s s s t t t t t t t t u v w x '
  'y z'],
 ['a    x      a b c d e f   a g g h h h h i j j j k k k k l l l l m n o p q r r r s s s t t t t '
  't'],
 ['    x        a  b  c d e  f   a  t t'],
 ['     a a a a  e'],
 ['x y a a a b b d d  j j j j k k k k l l l l m n p q r r r s s s s s s s t t t t t t t t v w'],
 [' p p q q r r r s s  s t t t u u u v v w w x x y y z z    a a a a b b d d d d f f f g h i  '],
 ['     a a a a b b d d d d f f f g h o o o o o o p p p p p p q q q q q q r r r    a b  s s s s s '
  's t t t t      a a a a b b d d d d f f f g h    a b        c d j j j k k k l l l l m n o p q r '
  'r r s s s s s s s t t t t t t t t u v w x y   t  t t t u v w x y z r r r s s s s s s t t t t t '
  't u u u  z z z z z  '],
 ['    x      a g g    x      a b c  d e f   a g  g h h h h i j j j k k k k l l l l m n o p q r r '
  'r s s s s s s s t t t t t'],
 ['o o o o o o p p p p p p q r r  z z'],
 ['    x      a b  c d e f g  a g g  t t'],
 ['     b c d  e f   a g g  g t t'],
 ['p p q q r r r s s  s t t t u u u v v w     a a a a b b f f g h i  e w x x y y z z'],
 ['a    x       a b c d e f   a g g h h h h i j j j k k k k l l l l m n o p q r r r s s s s s s s '
  't t t t t'],
 ['x y a a a b b d d  j j j j k k k k l l l l m n p q r r r s s s s s s s t t t t t t t t v     a '
  'a a a b b d d d d f f f g h o o o o o o p p p p p p q q q q q q r r r    a b  s s s s s s t t t '
  't      a a a a b b d d d d f f f g h    a b        c d j j j k k k l l l l m n o p q r r r s s '
  's s s s s t t t t t t t t u v w x y   t  t t t u v w x y z r r r s s s s s s t t t t t t u u u  '
  'z z z z z   w'],
 ['c a a a a b b    x b     a       a a a a b b d d d d f f f g h    a b        c d e f   a g g h '
  'h h i j j j k k k l l l l m n o p q r r r s s s s s s s t t t t t t t t u v w x y   b  c d e '
  'f   a g g  t t d d d d f f f g h i'],
 ['    a b        c d e f   a g g  h h h i j j j k k k l   a b        c d j j j k k k l l l l m n '
  'o p q r r r s s s s s s s t t t t t t t t u v w x y   t  t t t u v w x y z'],
 ['o o o o o o p p p p p p q q q q q q r r r r r s s s s s  s t t t t t t  u u z z z z z'],
 ['    a b        f   a g g h h    x      a g g t h i j j j k k k l l l l m n o p q r r r s s s t '
  't t t t t t t u v w x y '],
 ['    a b        f   a g g h h    x      a g g t h i j j    x      a  b  c d e f   a g g  t t j k '
  'k k l l l l m n o p q r r r s s s t t t t t t t t u v w x y '],
 ['c a a  a a b b d d d d f f f  g h i'],
 ['       a a a a b b d d   t t'],
 [' p p q q r r r s s  s t t t u u u v v w w x x y y z z     a a a a b b d d d d f f f g h i  '],
 ['     a a a a b b d  d d d f f f g h i  e'],
 ['       a     c a  a a a b b d d d d  f f f g h i g h i   f   a g g  t t'],
 ['a b c d e f g h i j k l m n o p q r s t u v w x y z a b c d e f g h i j k l m n o p q r s t u v '
  'd e f g'],
 ['o o o o o o p  x x     a a a a  e x x y y y y y z z'],
 ['       a a a a b b d d d d f f a g g  t t'],
 ['  o o o o       a a a a b b d d d d f f f g h i    x      a b c d e f   a g g  t t o o p p p p '
  'p p q q q q q q r r r r r r s s  s s s s t t t t t t u u z z z z z d e f   a t  t'],
 ['    x     x      a g g t     a b  c d e f   a g g t'],
 ['d       g h i  '],
 ['     a  a a a  e'],
 ['l m m m  o t x  t    a b c d e f   a g g  t t m m m m m n n n n n n n n n n n n n n o o p p q o '
  'o o o o p p p p p p q q q q q q r r r r r s s s s s   s t t t t t t u u z z z z z q r r s'],
 ['o o o o       a a a a b b d d d d f f f g h    x      a g g    t r r r s s s s s s t t t t t t '
  'u u z z z z z'],
 ['x y a a a b b d d  j j j j k k k k l l l l m n p q r r r s s s s s s s t t t t t t t t v '
  'w       a  b c d e f   a g g  t t'],
 ['o o o o       a a a a b b d d d d f f f g h i    x      a b c d e f   a g g  t t o o p p p p p '
  'p q q q q q q r r z z'],
 ['  g    g h i      x     x      a b  c d e f   a g g  t t  c d e f   a g g  t t'],
 ['  o o o o        a a a a b b d d d d f f  f g h i    x      a b c d e f    a g g  t t o o p p p '
  'p p p q q q q q q r r r r r r s s s s s s t t t t t t u u z z z z z d e f   a t t'],
 ['o o o o o o p p p p    x      a  b  c d e f  t p p q q q q q q r r r r r r s s s s s  s t t t t '
  't p p q q r r r s s  s t t t u u u v v w w x x y y z z    a a a a b b d d d d f f f g h i   t u '
  'u u  z z z z z'],
 ['a b c d e f g    x b     a  b  c d e f   a t t h i j k l m n o p q r s t  u v w x y z a b c d e '
  'f g h i j k l m n o p q r s t u v w x y z a b c d e f g'],
 [' p p q   a a a  d d d f f f g h i  '],
 ['c a a a a b b    x b     a       a a a a b b d d d d f f f g h    a b    r s s s s s s s t t t '
  't t t t t u v w x y   b  c d e f   a g g  t t d d d d f f f g h i'],
 ['  o o o o       a a a a b b d d d d f f f g h i    x      a b c d e f   a g g  t t o o p p p p '
  'p p q q q q q q r r r r r r s s  s s s s t t t t t z z z d e  f   a t  t'],
 ['    x   o o o o o o p p p p p p q q q q q q r r r r r r s s s s s  s t t  t t t u  u z z z z '
  'z   a  b  c d e f e  a g g y t t'],
 ['    a b        c d t t t u v w x y '],
 ['   a b        c d e f   a g g h h h s t t t t t t t t u v w x y '],
 ['  o o o o         a a a a b b d d d d f f  f g h i    x      a b c d e f   a z s s t t t t t t '
  'u u z z z z z d e f   a t t'],
 ['    n   a  b c d e f   a g g  t t'],
 ['     a a a  a b b f f g h i  e'],
 ['o o o o o o p p p p p p q q q q q q r r r r r r s s s s s  s t t t t t t u u z     a a a a b b '
  'd d d d f f f g h    a b        c d e f   a g g h h h i j j j k k k l l l l m n o p q r r r s s '
  's s s s s t t t t t t t t u v w x y    z z z z'],
 ['o o o o o o p p p p p p q q q q q q r    x b     a  b  c d e f   a t t r r r r r s s s s s  s t '
  't t t t t u u u  z z z z z'],
 ['d      g h  i  '],
 ['d    x      a b c d e f   a g g  t t      g h  i  '],
 ['o o o o o o p p p p    x      a  b  c d e f  t p p q q q q q q r r r r r r s s s s s  s t t t t '
  't p p q q  r r r s s  s t t t u u u v v w w x x y y z z    a a a a b b d d d d f f f g h i   t '
  'u u u  z z z z z'],
 ['o o o o o o p p p p p p q q q q q q r r r r r s s s s s  s t t t t t t  u u z z z z'],
 ['p p q q q  r r r s s s t t t u u u v v  g    g h i   w w x x y y z z'],
 ['o o o o       a a a a b b d d d d f f f g h i    x      a b c d e f  a a g g  t t o o p p p p p '
  'p q q q q q q r r z z'],
 ['o o o o o o p  x x     a a a a  e x x y  y y y y z z'],
 ['  o o o o         a a a a b b d d d d f f  f g h i l m m m  o t x  t    a b c d e f   a g g  t '
  't m m m m m n n n n n n n n n n n n n n o o p p q o o o o o p p p p p p q q q q q q r r r r r s '
  's s s s   s t t t t t t u u z z z z z q r r s   x      a b c d e f   a z s s t t t t t t u u z '
  'z z z z d e f   a t t'],
 ['o o o o       a a a a b b d d d d f f f g h i    x      a b c    x b     a       a a a a b b d '
  'd d d f f f g h    a b        c d e f   a g g h h h i j j j k k k l l l l m n o p q r r r s s s '
  's s s s t t t t t t t t u v w x y   b  c d e f   a g g  t t d e f   a g g  t t o o p p p p p p '
  'q q q q q q r r z z'],
 ['    a b        c d e f   a g g  h h h i j j j k k k l l l l m n o p q r r r s s s s s s s t t t '
  't      a b        c d t t t u v w x y  v w x y z'],
 ['   o o o o o o p p p p p p q q q q q q r r r r r s s s s s  s t t t t t t  u u z z z z x      a '
  'b   c d e f   a g g t'],
 ['    x b     a       a a a a b b d d d d f f  t t t t t t t u v w x y   b  c d e f   a g g  t t'],
 ['    x      a b c j d e f   a g  g h h h h i j j j k k k k l l l l m n o p q r r r s s s s s s s '
  't t t t t'],
 ['    x      f   a g g    t'],
 ['l m m m m  p  p q q r s'],
 ['p p q q q r r r s s s t t t u u u v v  g    g h i    a b        f   a g g h h    x      a g g t '
  'h i j j j k k k l l l l m n o p q r r r s s s t t t t t t t t u v w x y    w w x x y y z z'],
 ['  o o o o        a a a a b b d d d d f f  f g  h i    x      a b c d e f   z z d e f   a t t'],
 ['x y a a a b b d d d d f f f g h i i i i i j j j j k k k k l l l l m n p q r r o o o o o o p p p '
  'p p p q q q q q q r r r r r r s s s s s s t t t t t t u u u u u u  v v v v x x x x y y y y y z '
  'z z t t t u v w'],
 ['    x b     a  b  c d e f    a  g g  t t'],
 ['    x       x b     a  b  c d e f   a t t   a  b  c d e  f   a g g  t t'],
 ['p p q q q r r r s s s t t t u u u v v  g    g h i    w w x x y y z z'],
 ['l m m m      a a a a b b d d d d f f f g h o o o o o o p p p p p p q q q q q q r r r    a b  s '
  's s s s s t t t t      a a a a b b d d d d f f f g h    a b        c d j j j k k k l l l l m n '
  'o p q r r r s s s s s s s t t t t t t t t u v w x y   t  t t t u v w x y z r r r s s s s s s t '
  't t t t t u u u  z z z z z  m  p  p q q r s'],
 ['    n   a  b c d e f   a g g l'],
 ['    x      a b c j d e f   a g  g h  h h i j j j k k k k l l l l m n o p q r r r s s s s s s s '
  't t t t t'],
 ['l m m m m  p  p q q r s    x      a b  c d e f   a g g  t'],
 ['    x     a b c d e f g h i j k l m n o p q r s t u v w x y z a b c d e f g h i j k l m n o p q '
  'r s t u v d e f g a b c d e f   a g g  t t'],
 ['  a b  c d e f   a g g t'],
 ['l m m m  o t x  t    a b c d e f   a g g  t t m m m m m n n n n n n n n n n n n n n o o p p q o '
  'o o o o p p p p p p q q q q q q r r r r r s s s s s  s t t t t t t u u    a b        f   a g g '
  'h h    x      a g g t h i j j j k k k l l l l m n o p q r r r s s s t t t t t t t t u v w x y  '
  'z z z z z q r r s'],
 ['d        g h i d '],
 ['l m n n n o o p p q o o o o o o p p p p q q q r r r r r s s s s s  s t t t t t t u u z z z z z '
  'q r r s'],
 ['    x b     a  b  c d e f    a  g  t t'],
 ['    a b        c d e f   a g g h h h i  j j j k k  k l l l l m n o p q r r r s s s s s s s t t '
  't t t t t t u v w x y z'],
 ['    x b     a       a a a a b b d d d d f f f g h    a b        c  d e f   a g g h h h i j j j '
  'k k k l l l l m n o p q r r r s s s s s s s t t t t t t t t u v w x y   b  c d e f   a g g  t '
  't'],
 ['    a b        c d e f   a g g  h h h i j j j k k k l   a b        c d j j j k k k l l l l m n '
  'o p q r r r s s s s s s s t t t t t t t t u v  w x y   t  t t t u v w x y z'],
 ['    x      a b   c d e f     o o o o o o p p p p p p q q q q q q r r r r r s s s s s  s t t t t '
  't t  u u z z z z x      a b   c d e f   a g g t a g g t'],
 ['    a b        c d e f   a g g h h h i j j j k k k l l l l m n o p q r r r s s s o o o o       '
  'a a a a b b d d d d f f f g h i    x      a b c d e f  a a g g  t t o o p p p p p p q q q q q q '
  'r r z z s s t t t t t  t t t u v w x y z'],
 ['p  p q q r r r s s s t t t u u u v v w w x x y y z z'],
 ['     a a a a b b d d d d f f f g h    a b        c d e f   a g g h h h i j j j k k k l l l l m '
  'n o p q r r r s s s s s s s t t t t t t t t u v '],
 ['    x      a b  c d e f g  a g g   t'],
 ['l m m m m m m m m n n n n n n n n n  n n n  n n o o p p q q r r s'],
 ['d      g   '],
 ['d       g h i  d '],
 ['x y a a a b  b d d  j j j j k k k k l l l l m n p q r r r s s s s s s s t t t t t t t t v w'],
 ['      g h i  t'],
 ['p p q q r r r s s s t t t u x x y y  z z'],
 ['    a b        c d e  f   a g g h h h i j j j k k k l l l l m n  o p q r r r s s s s s s s t t '
  't t t  t t t u v w x y z'],
 ['    n   a  b c d e f   a g g   t t'],
 ['o o o o       a a a a b b d d d d f f f g h i    x      a b c d e f   a g g  t t o o p p p p p '
  'p q q q q q q r r r r r r s s     x b     a       a a a a b b d d d d f f f g h    a b        '
  'c  d e f   a g g h h h i j j j k k k l l l l m n o p q r r r s s s s s s s t t t t t t t t u v '
  'w x y   b  c d e f   a g g  t t t t t t t u u z z z z z'],
 ['  x y z x y z x y z x y z x y z x y z x y z x y z x  x      a b  c d e f   a g g t'],
 ['     a a a a b b    a b        c d e f   a g g h h h i j j j k k k l l l l m n o p q r r r s s '
  's t t t t t t t t u v w x y  f f g h i  e'],
 ['    x   o o o o o o p p p p p p q q q q q q r r r r r r s s s s s  s t t  t t t u  u z z z z '
  'z   a  b  c d e f e  a g g y t '],
 ['  o o o o        a a a a b b d d d d f f  f g  h i    x      a b c d e f   a z s s t t t t t t '
  'u u z z z z z d e f   a t t'],
 ['a b c d e f z b c d e  f g'],
 ['    a b        c d e  f   a g g h h h i j j j k k k l l l l m n o p q r r r s s s t t t t t t t '
  't u  v w x y '],
 ['  o o o o        a a a a b b d d d d f f  d e f    a g g  t t o o p p p p p p q q q q q q r r r '
  'r r r s s s s s s t t t t t t u u z z z z z d e f   a t t'],
 ['    a b         c d e f   a g g h h h i j j j k k k l l l l m n o p  v w x y '],
 ['o o o o       a a a a b b d d d d f f f g h i    x      a b c d e f   a g g  t t o o p p p p p '
  'p q q q q q q r r z  z'],
 ['l m m m  o t x  t    a b c d e f   a g g  t t m m m m m n n n n n n n n n n n n n n o o p p q o '
  'o o o o p p p p p p q q q q q q r r r r r s s s s s  s t t t t t t u u   w x y  z z z z z q r r '
  's'],
 ['    x      a g g    x      a b c  d e f   a g  g h h h h i j j j k k k k l s s s s  t t'],
 ['   o o o o o o p p p p p p q q q q q q r r r r r s s s s s  s t t t t t t  u u z z z z x      a '
  'b   c d e f   a g  g t'],
 ['x y a a a b b d d  j j j j k k k k l l l l m q r r r s s s s s s s t t t t t t t t v w       a  '
  'b c d e f   a g g  t t'],
 ['    a b         c d e  f   a g g h h h i j j j k k k l l l l m n  o p q r r r s  t u v w x y z'],
 ['     b  c d  e f   a g g  g t t'],
 ['    a b        c d e f   a g g h h h i  j j j k k k l l l l m n o p q r r r  s s s s s s  y z'],
 [' p p q q r r r s s  s t t t u u u v v w w x x y y z z     a a a a b b d d d d f f f g h i    a '
  'b        f   a g g h h    x      a g g t h i j j    x      a  b  c d e f   a g g  t t j k k k l '
  'l l l m n o p q r r r s s s t t t t t t t t u v w x y   '],
 ['      a      a b         c d e f   a g g h h h i j j j k k k l l l l m n o p  v w x y b  c d e  '
  'f   a g g  t t'],
 ['     a a a a b b d d d d f f f g h o o o o o o p p p p p p q q q q q q r r r r r s s s s s  s t '
  't t t t t u u z z z z z   a b        c d e f   a g g h h h i j j j k k k l l l l m n o p q r r '
  'r s s s s s s s t t t t t t t t u v '],
 ['    x b     a  b  c d e f    a   g g  t t'],
 ['      g h i   '],
 ['  a  b c d e f   a g g  t t'],
 ['a b c d e f g    x b   i j k l m n o p q r s t  u v w x y z a b c d e f g h i j k l m n o p q r '
  's t u v w x y z a b c d e f g'],
 ['  o o o o       a a a a b b d d d d f f  f g h i    x      a b c d e f   a g g  t t o o p p p p '
  'p    x      a g g    x      a b c  d e f   a g  g h h h h i j j j k k k k l s s s s  t t a t t'],
 ['l m m m m m m m m n n n n n n n n n n n n n n o o p p q p p p q q q q q q r r r r r s s s s s  '
  's t t t t t t u u z z z z z q r r s'],
 [' d   x       x b     a  b  c d e f    a t t   a  b  c d e  f   a g g  t t'],
 ['o o o o o o p p p p p p q q q q q q r r r r r s s s s s  s t t t t t t  u u z z z z x y a a a b '
  'b d d d d f f f g h i i i i i j j j j k k k k l l l l m n p q r r r s s s s s s s t t t t t    '
  'a b        c d e f   a g g h h  j k k k l l l l m n o p q r r r s s s s s s s t t t t t  t t t '
  'u v w x y z t t t u v w'],
 ['c a a a a b b    x b      a       a a a a b b d d d d f f f g h    a b    r s s s s s s s t t t '
  't t t t t u v w x y   b  c d e f   a g g  t t d d d d f f f g h i'],
 ['l m m m m  p m p q q r s'],
 ['    x       a  b     t t t t t u  v w x y    a g g    t'],
 ['o o o o o o p p p p p p q q q q q q r r r r r r s s s s s o o o o o o p p p p p p q q q q q q r '
  'r r  z z s t t t t t t u  u z z z z z'],
 ['d      g h i d l'],
 ['    a b        c d e f   a g g h h h i j j j k k k l l l l m n o p q r r r s s s s s s s t t '
  't    a b        c d e f   a g g  h h h i j j j k k k l   a b        c d j j j k k k l l l l m n '
  'o p q r r r s s s s s s s t t t t t t t t u v w x y   t  t t t u v w x y z t t t t t u v w x y '
  'z'],
 ['    x      a b   c d e f   a g g  t'],
 ['    a b        c d e  f   a g g h h h i j j j k k k l l l l m n o p q r r r s s s t t t t t t t '
  't u  v w x y h'],
 ['   g     a a a a b b d d d d f f f g h i  e h i  '],
 ['      x   a   a  b  c d e f  t'],
 ['    t'],
 ['o o o o o o  p p p p p p q q q q q q r r r r r r s s s s s  s t t t t t t u u  u  z z z z z'],
 ['   o t x      a  b c d e f  t t'],
 ['a b c d e f g    x b  d       g h i  d  c d e f   a t t h i j k l m n o p q r s t  u v w x y z '
  'a b c d e f g h i j k l m n o p q r s t u v w x y z a b c d e f g'],
 ['l m m m  o t x  t    a b c d e f   a g g  t t m m m m m n n n n n n n n n n n n n n o o p p q o '
  'o o o o p p p p p p q q q q q q r r r r r s s s s s   s t t t t t t u u z z z z z q r  s'],
 ['  o o o o       a a a a b b d d d d f f  f g h i    x      a b c d e f   a g g  t t o o p p p p '
  'p p q q q q q q r r r r r r s s s s s s t t t t t t u u z z z z z d e f   a t t     a a a'],
 ['s    a b         c d e f   a g g h h h i j j j k k k l l l l m n o p  v w x y '],
 ['  o o o o        a a a a b b d d d d f f  d e f    a g g  t t  o o p p p p p p q q q q q q r r '
  'r r r r s s s s s s t t t t t t u u z z z z z d e f   a t t'],
 ['l m m m m  p  p q o o o o o o p p p p p p q q q q q  q r r r r r r s s s s s s t t t  z z r s'],
 ['x y a a a b  b d d  j j j j k k k k l    x b     a  b  c d e f    a g g  t t l l l m n p q r r '
  'r s s s s s s s t t t t t t t t v w'],
 ['l m m m m m m m m n o q q r r s'],
 ['    x     x  g    a g g t     a b  c d e f   a g g t'],
 ['  o o o o   d     a a a a b b d d d d f f  f g h i    x      a b c d e f   a g g  t t o o p p p '
  'p p p q q q q q q r r r r r r s s s s s s t t t t t t u u z z z z z d e f   a t t'],
 ['     x      a b  c d e  f   a g g  t t'],
 ['  x y z x y z x y z x y z x y z x y z x y z x y z x  x      a b  c d e f   a  g g t'],
 ['o o o o o o p p p p p p q q q q q q r    x b     a  b  c d e f   a t t u  z z z z z'],
 ['   e c d e f   a g g t    a b        c d e f   a g g  h h h i j j j k k k l l l l m n o p q r r '
  'r s s s s s s s t t t t      a a a a b b d d d d f f f g h    a b        c d j j j k k k l l l '
  'l m n o p q r r r s s s s s s s t t t t t t t t u v w x y   t  t t t u v w x y z'],
 ['    x      e c d e f   a g g t    a b        c d e f   a g g  h h h i j j j k k k l l l l m n o '
  'p q r r r s s s s s s s t t t t      a a a a b b d d d d f f f g h    a b        c d j j j k k '
  'k l l l l m n o p q r r r s s s s s s s t t t t t t t t u v w x y   t  t t t u v w x y z   a b '
  'c d e f   a g g    t'],
 ['  o t x  t    a  b c d e f   a g g  t t'],
 ['a b c d e  f g h i j k l m n o p q r s t u v w x y z a b c d e f g    x      a b  c d e f   a g '
  'g  t h i j k l m n o p q r s t u v w x y z a b c d e f g'],
 ['o o o o o o p p p p p p q q q q q q r r r r r r s s s s s  s t t t t t  t u u u  z z z z z'],
 ['o o o o o o p p p p p p q q q q q  q r s s s s t t t  z z'],
 ['o o o o o o p p p p p p q q q q q q r r r r r r s s s s s o o o o o o p p p p p p q q q q q q r '
  'r r  z z s t t t z z z z'],
 ['o o o o o o p p p p p p q q q q q q r r r r r r s s s s s s t t t t t t u u u u u u  v v v v v '
  'v w w w w w w x x x x x x y y y y  z z'],
 ['    a b        c d e f   a g g  h h h i j j j k k k l l l l m n o p q  r r r s s s s s s s t t '
  't t t  t t t u v w x y z'],
 ['d       g h i  d'],
 ['      g h'],
 ['    x      a b  c d e f     a b        c d e f   a g g h h h i j j j k k k l l l l m n o p q r '
  'r r s s s t t t t t t t t u  v w x y g  a g g   t'],
 ['x y a a a b  b d d  j j j j k k k k l    x b     a  b  c d e f    a g g o o o o o o p p p p p  '
  'p q  q q q q q r r r r r r s s s    x      a b c d e f   a g g  t t s s  y y y z z z z z t t l '
  'l l m n p q r r r s s s s s s s t t t t t t t t v w'],
 [' p p q q r  r r s s  s t t t u u u v v w w x x y y z z    a a a a b b d d d d f f f g h i  ']]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-q~aIkIfYvX()Bu^?g5HyRT`2#?0lnE(<J;$tj~iaGH8$=g{Ia3SrTD!X;=-'
    b'kGtYasQj>*8lhq|NH;`pMUrH^I!kvKmD)&_}~BAO11sV|N1Yd>^nRErqf4?-'
    b'R7P*y?d+O{AO9TmK5eFmdh>2Ua~mri?dH#DYk$4pa1gT{=Hi<HqNy3=F6qTnL`Y><WY@M*KBRB)bd=thF)(^E!Z2Q?2}_CXSMeJw'
    b'V2d%%K7cF_d98f9mZb!Wg9oIGgr-Rr;zhG<IXYXdp)l=a#*j&yUM>7Gr|a`_A*X8H|;UUTj#XU-&`k$Y?k|8A-'
    b'$UFthHNBv!uI*)jCT!zO{*C?R<MK`GwfV47<`jlitlWwHVtxlfJI4mfT936!6vyGnZH1xPQgaSNV)LsK5w!ZN3st>ah>A{Z{Y2mG'
    b'j~nBh1;0%~e{dF_oCZ&NKb>P0rR*Kk3$RQ;pAhq)Km5pB;OyD~xpFiL=l}^QCILygtt;y-'
    b'fQX@SWx>ZC8eK&Yhc8vr%#=#meNXcLb_h_-B^NmuEg9wYuvKwEF!OQ{TyVQ+#N*#Y?b^bl-TJE<M{yw{@DeS3=3D+}F#A)F-'
    b'BTh|f{~wHO|iTAGc%qZ7|ArSmk#;*P{O;>*O`t3&}`Osl7{QtxK9wKOdL6+?H1m+v@-'
    b'h`&}wJh|@op0!x#?JbZO>+MN2q(<{1l@6<)yL+29|B4wgjh@VoA}!h)WrW)DC9w!i8hlbn(N1``-q=XBYZl%M>E6BW-'
    b'$+@BbXaOsqU{qH!#6{$dD*5!k~Ge=#u+JxR{Cpi#hu4z#M2JnVoK<9-&jZEfvF6tzX{=VbL}bA5>Mi5_dW~z5>2Jk(??-'
    b'Vl)v@YsJKqIY_qLSkKDJ*nt?bcw29M1rHqzF@MD}iU%a0{-`003cK-'
    b'S%zVq(sEm6nx&JNZI)7y5m1VEI$E@PPOQevWxYsVKF2*h7|?ZbD#`+S|WOD~pIM{Mnea`&c(vYk<rt=ovQP)P5b?w)zoYc=0^X30'
    b'5xQ<DHmnWyzRRv9m)X2(k7i7Q6_Kh?;i^Zh>SB9a+T9@63{v*+vEH%`Sk;f>QsIW@{DifhR90(I$O!z~+_Dpotl8R9fBoJ6e;pb*'
    b'=w&@El!p^w)hm3-'
    b'ZKq{!D*`Ce}z@k)CwDt1z)==y3AFw8hYd<z79Go^G0^FxmVwW0U|g;Oz3Ips7`YJlp&Ac5_nfxm~Z<&tVxj8i}fyj#}0YfbnZkw6'
    b'JHpm(^nev^TGq0MjC*%xHMNFNddx<yKa*h#r*c_kyaHmp*gt(rPxi#nL;k2O1#Xd~twR?evdMFm|&xaM0)q7w4U8|~8xn8s%;W`q'
    b'aPmPEDfFQ+UVMyU)0npN6Dwm&*Jbr=|RP;RId9h1tdWD5cyq3HMoSz6-'
    b'$M?(7Kl#^(4g7lJdM}q)C7Fw7swnauJnoZO4%|`eX8x`e;n0*Igjv%6<mNM`5jT@)hc=42vpmkyfrzj@K(%5625GrP-'
    b'r9uZqN<16H1PK-$vaHF%j1}U3L}uF^=q@vTb+OY(IWdD%ZJdg6vL3(HC~zr;u$#~YuuUKqB$jc^h2#!!;ISD-CCLGRwZcxAoJy<6'
    b'c_PqP>^nIar|=8c80r}p<D0?XSq>~#DH=qe4*b1|hZp`4-'
    b'Es=1Z@_$Qx0>T~7PL;`=R`10=;sv0PK|OBCS{NgxaGa;vcBvS@pluvuWXEUPDl<)N}H%?3(UWaycOjSYWJ&)OQE6@0a&ou#Ji2n('
    b'_&nxjuiHW<yxK*Iku&jn}ylIcCh{_CjXdWLy!RiIp?BSFWRlg6gp#eklm*rB;~jb0YpDh?1NrL-lg|Y`uRGT*h#%rHJ?#%QHbN(k'
    b'VWg(v=|T654}W(AP_CR9Ox6O-7~#ob)}!=DX$rmpDM;lQ8Z*-'
    b'CB~3XJZ1nfBT$=sN&7&+l#@__l!EUG6M>b0vYdO}$%yYiW~jKMKGKdGF464jx$QnpF@hM1wuoR1#Af5q=npL>VMdItmu?Hb8Sa$~'
    b'K9KG-QchU>Tg5m5#c$0*!X-'
    b'7>q{cbid;)60YyhDhF5#IV{*9V}4x5mK;U6|09flGkQs3V?L)fUYn1huZu|chzHeWa;pw}#<$YbzdKymMxCc<1RnkI6wp)tJplU~'
    b'yaD4a~9(|~*74I^s|CQS;p@77-F<DEDZx`6RnR5T1kpq4Ho8i3d;c`QBvh<D$q4ky@hD#mHRor(dYZm9%EUTfQ-'
    b'Q)eQxj%nJ5#01ag+Vx?%E^HalY!#+Y>D<xM9=`K_NqRB2Uha5CCgKc0m&R8KYpMl@+nZ5(moV4?pJO>cex$jOZ=)zaZqPWaOEBA}'
    b'^BEP&nwP&(l{F(ldkdYy7?Hj3{~Scjh@<82g5;pN4DBgJ8mALgp<kiRL*C?7a>~U%OSX(JDttG~r4rn)cJ%b0Fp(;Gy#zk`3XRgY'
    b'w4i1u#SW>=@*0m#7bGXgHuWj=N+@+BW&UatA?F!0B}k9M*>+Qd!tXuztedcSP!s(}FPBNB`a$jNyR~w6zp3feHwPPl7vKEv9V2#F'
    b'fw1R!1W}0Tvnsg&oCO)!?z>EB5cGKKosazuIB9Y!NuA3J0lR=^>?C`5C7m}iJTNjLw5Uzm&@*t>hbAL$I+Ggz5ln|kPgoTu8ftYO'
    b'SPO-cT?Ph(?~^)0?RV#fMH!jOoTxd2v&QzV4N12^Dl-Eq9;5*_*sy*R0TVNHIy26QeqjvwB(ONsS@aH2i241S%!D)cKE%g?X;7)u'
    b'9_>uJmUSViTII|-'
    b'BL>LOO!}IrIWr2;_xc;~TP_u@^&!;T>@7xvk`@DXwIsUcVO01;s_7JXSqi6}*4Mr9l^A{drrimpq&T49)hYut;i^jZTHZun>;Wt_'
    b'(y7fos0ljtk@k!%hA#g>x;ms|c%OPNzfChHEROu(J9)u8wl9>jXSmA7)=(1bzILEN`s-hdQ9KSQg{kMZz0L$y-'
    b'pj(nw$kJ26l4kA0W0=J|5QTDR^F?u?Ate93j}lp?HG{ttkkm}WJ!Y{A2lL0(M+ZG^C>_U{o%&qMUz@3<!}8)F_DD)?+gGChEg3iX'
    b'-QXBB@_hEjdezeb#*F;UMPxy+!D;`JGI(L!He>_v()i|-'
    b'OIr2L$}5;$k!UEFWI07=AVlJF9i*K!L7E7bNKm~M5o%6HAE^;KMqQQN$}E5aLcUI5?M%@ZAh}+gN%&y<N@3jf#o@e-'
    b'^3!Kp3`cK6+9LnbO58|YrxY8D9o;Tlgp?<FDnexymbF2CxDW#qL`%}hH*)D$9rgAsZ%+nqy!cly0YW{0jss32J-'
    b'D<OCio3YxgCX89_4OGRLv7QiFgeT_E4LtYV!aRiczLF*PHsQw_4))D^g<f#%HNeX7p#Jz65pJb|h%G74W~R1^V4Zq-ZD;!TDqi^B'
    b'V*&v0PLcffy(?w)`MM>e&GZ3klT?95+M02%_FvcSV!Q6^zgQK;|IJ9s@vYVPl3CgBvQB(8`0tOc5!3*rObp<~SUha!j~?D>pFSRt'
    b'$8c^8SfusGkjt%vd0t&A4IQHb#s;0QK&Xy2_UsTsox#RN0lh!L--'
    b'=C0*q=*@h)I3Fy2&xAdpgNf6AuQdi9`M%kDo?6Zxgvpful!wmn1mSsWd$Im8L&`|*4&d$qgv63dLqE0^g7(ujss!NEYH(i@Kk+k5'
    b'oEXQT$&OllQ`2dr0MIi*n}Nog@D#dy=ZjmsWO69eE~(TcAV__TPOX{lDIsSVhbsN`&4PreZAE5ihWhdMbwg~W;F9s}^mGKKcn(%5'
    b'5TN8|K44fwj)y-i-gw&rWdbx9eH1B?f}`TQy*`YM<yqSTH*3>Q(6F@CZtr2#oCvwT6E8!1Dq+|V?`Oe<s3Vo)F5-'
    b'~di#W&PIS8b_4mEnS?{hX*N-E<Iwits-'
    b'a!#c{C9zk;Y!Vu1I6~00A#=!!VVFWq*s(k#((JxUbmqRDfx;)J;%UTxN;Ag@xA9p_v$k9z2Jn;Tprl)Ts}yY-'
    b'(P~I2+Y}Ou4zu7}8z);fq?WPi(8|ixJLETQ4YG4d+MI9!g)Wx}Mo<R5O#P|Q)sE1A_CorMlvhsq00ogb;h2a0$%xQeSMDolE*C>j'
    b'^>O&<?1za++6n^`VJR?76O(jv8NTS})Hj+{e*6gJMmO@TK=hy^0-'
    b'ABm07D@l0E~dAB7Y+hMTq8FwE`1+^z9p`xCxqY!sZgbcte3FjvboH7BEMn&1Mmg+kx@1L9C0lp}$(3_hKraZ)!S?lvCWav-&E0-'
    b'Y{9CXkQk?T`!VTW4z@dD?dDj?hFv(h?uh|<EGWw>f0!<nKmC`;#3=n`^oRuUMPJz@q(4+hj*u)!W(o)#U|!`=pt=$SbHxegJohlf'
    b'615MV~sRJ8~UX(`*aN%aZKC(|0+0Nt_ksm+0}#{`FX~KWAk_4mQ!jXA$CS*td+EYvXZ_s9vmT~OL7uIAPAPFPZ=6Au;O{^o#02P='
    b'35&SJXR`^$QK>96^ycFU|E`vQsCx~{(+iD+~mY%Fd6t*dTQmn%tgPVIF$Lg2YeWEi{woS$w#<EO^0@n<BiWm(F7cbkF;jd#22dB7'
    b'q);V%z5u5IPz)|XHXGlh4$2ncsT1^EM0z=C~ONEdS2LRZY_+AZ-'
    b'(O$Eko696JlEGqroHHdMRuI3{?w<J)^#I&MUn=4UKmWMu`~u?p*Lv6t5X_r@b1^=JBAG;hI5FKC1r?==mZeVj9adD{lu+l;UJC?s'
    b'K;DPITu5Ta3g#R52Ubb@Mp(*+;vHAv!~QOK*I64n_`UX(t$Q5J!c^sNZked8bv6SfawSTF#oC9-'
    b'qBGHtD?*?|`i?K4w$?<S}%I)?GhK724KHC;JLoNG;gIGZ(bJCYu%^I)EB91mRYQIfnNEU8W^R+|7*_G8#}TzjhXFxIHl&+*J*hne'
    b'+s4bOg5VU^-eYpjN3ZflQI~gH|-hHpbJR={$e)Q=S3ht1oJg)?)-'
    b'tKTTUIXhtI_!kjRVp75*|;SSy3CH@tz_RiYAjdH4u6Z$!IvGMbw(6%Yz755A+BCU?Ca5aU=m(T>na15yHVg<x+O;QDxPv7|)gn3%'
    b'&w36Ec84J$;#7Lzr9t6g^Gwzn!P*N>&t;{OgCz!F-'
    b'>CZqjGRTOzH1R%A7HE+>0xf%KKTYmw1p;kyE@_FM+gc5~HPQ*Y&9C<JT6FVi6l4_J*b77)XJ$SMW@Nw(@K3w#sjbTy%_R$Cl9r(Y'
    b'm%>1l*ZM04KC(-#-z7#%JbUzL1w0sx2?0Ank@Ju=)$mEMbh}V7JuwTU^v!TD108f+)R1!*>fh-'
    b'OEl2OFW0YEM>I7_E=RH`^0&EaqPc7cRgP;x064I$r`+)DDK+*QE-JZs|LRc$@gh<;A^UMKdvB~$<H~e(-'
    b'oLal8IoUsFS+$)ADLWAQmv}=zpD_*+B*oOn?tR=zinTW<{L{lcQA_y?*yah&Q>#8vj2$=(W*hWCLnP664<Rt*W5~YO;7&vVW87|}'
    b'!2?Iy8O%asGs@~Gc?xMB8<7-eI22)dP-u%<GEG_Mpb&A97M(f}wR@C06LM$VUWHN9w>BFUpJKBa_99$1o)>erbsa!OYv1-'
    b't{cPf>31QhzingwLGwPs2OTL!%w{ptKPdQC4{MKv|E*Ni;MoL)={UOz+Qym9@M!#d5k(gWSlLZ@c4YdwW<gV>@aBVT?8CoaS^eM('
    b'G8GLFp_X1Ifw9kocJm4on?P{F_opUlVr+utR>oW2L1xFg<>Fp%~eEEi7C8q{NGCH+H&RVY-'
    b'4}S;w$dCrU*(JxyUFemfqmgNe&Zy_fXaD3bGA9Y?G~izI#XgF{3DUvhbO!x}lI_}vbWxnv5wZ{ACdu|*IwjABh1ESXC{`<49t4r-'
    b'f8UY%twp!~>M_)I((Nfw43@oCI=XKyGBZ$>sBSN6quVV#J+#G(MwLI)d+)pDV7!LV!0Yz}LLd^}DHc{;nwy>d=sZ?#lkwU4(dI<E'
    b'Xc!-`5#mqcO-3>8*{Mvlb58Cc@(8!wYLS!)SB7k~d3$M>pdc{kF5wa1E7$0}l;hMlPR0Dz9$F_s>x6zzJoQ^!RV;-'
    b'9s3hcTJQTyPZG)Qg)ns&PrKXrI&FJUB5MoHmSai$HsFoRhfr6fhL+3#zvhi9&5-'
    b'|u_>qG$kE%=O}>7m<Ngk;V=dzN=goB0r3)q6WexVM!K2iL9h!kS(aJ4AQ{IB0uPM~x0mcm&McMn%d@WAyah-'
    b'd<kQX_K_)DR7nPd`Qy?qfS`2UTK&%O3}bZy@-edne9qc_MY=J-}xJ_obnO-ULfjYpq*0FiC~<BiMG4aA$UmApC`@|TgC{}m59Y#q'
    b'LrenfhwuqZzqj$w2esXd7f~b@y4rB#8e*y;b&Vt&$RwI<#=BWz!d`~A*?CzjSR&^r~Zfq#PU{^zo#q67h-'
    b'MpGCu2+$Bum}L;ezahgNN^0#7^{=|m{!K6^O3N6kKcO`_Iv7*V_&*hP@*!84XL>F#7!bJ7{W&+KkYf<$|AgAwdgkofLtbDE=Y>f&'
    b'Kp+p}vOT_-tegon>Y;$}I8)XzRUPW%JZtZQSI&IMnf<~^hTgKwiqubY>a`2hEF(8fz2v1AN%I~LO+MK{4sB+m4?xnPl`yWDtZ`ff'
    b'KR|LKTBQD8kx#eiY#GX@N`t|nfwXxOAwrK5l(is%-sO`>7_=G1Du709+yQ+zE}n5{>HS8C|FrSN9ib!1czT-'
    b'B*dS1{8(gl76@mDOvcbf!6O%Ao8CnBSds2pYv;g#FYOYg?`9L@5lo=y^c*wb!tlx&MJ^mGyiNA_r@>X4$HATGC2AR!aw!7^+1F))'
    b'GnaBnk7{hRC4$cYMj$$v``aeW#rZFsdY87>hI*pd!}uO}Z+d_q2luS=3vy2LwbdRMK3&6JQ>~%A6+`bSfH<0)sC?ji^8~DoCt_B_'
    b'(#&UC8**ukOd|V;(u-vQe}EZT+rKA;D<C%=Bx;M6Y?Sj^q@bS2O-'
    b'o70>{1O8dfD<k7f1_2!ou@4poxlt2dT$^4B|P~Sde6`!ZpCF>R-'
    b'l;P(lt%r=IaFTe!b=sR%YOUW(QU}owAVM*^2@Nr}M<>gn&y**4Gan>NtKcD0QHetJNN=5E-'
    b'_Lo?*J;(m$+Dsp)7IJ^&}#>FLDbQU2+6>3G%)OC#KhI6bA}*IWDUa-kb-EK_>;SVw9Nt^afL~dn)RX6mOv5>OxoF0Vl>o4TEv!4M'
    b'lR&FRy6=H9`HTqYXqlGQCIEO*SfRzY@nrAutIr9GBgkRsXSymwgqpDA_}-'
    b'+glKoJ4G9^h>8_s+S`)OW9C=OtRSfGmAS2net0y4D_;*6lNsO`Q7esY1?*q4p=(2;dJQ6JpirJ|kLRYt|jfKSF>PnfS(>qm*)UlU'
    b';wwoFNk`Ix=Z&HA0=pL=X+a3|t)^>x>WhA;NhEZ>q3Lh{awH=cA8lkPj^KgvrKyF(yZ=|4gO+<F+ax9Q`I68K;v`rC3oo8tHb0R&'
    b'B=Dg0}v|8q4%ba$+I8CkUKyYPf_gzm%U{6J!TzpPGj8xTeFk(d$KLC#|4Ir(?(5bC}wSUg@#ZJQHw>H~X(56GjaW2y?&NcRsT|#j'
    b'VBs;DYN!PT85xW4*>i}w-_*M{9OVWRRBe^Rr@Gho~1`>E!5iMpvI2j!P=HP1bCa^$$+zC-po3;|55zKe~Mu(M?PQ7<J4L>*r=Gyj'
    b'yOmVsMZk?d+5i^Gc*|qnmALx2I+pT_0Vu`pE9fUSryPV(C;qj`Ip+FXmhyjCkG>lo>jhkR?EUk&mV{`O>qL{3iL@EfKA0p!F?u>D'
    b'$KH-mG((%}VJ4d5YS?U9SX7b@^7qoNSc!8*o5pr_AUNf{lTjQLV!D%jC*ZT(~^jvUVKtRJXv%m|wO`<<)v2_7b)qKb$2#Z*H;v)&'
    b'n{l3R(;14uNr4MiBqrq<ZOu<7~#B;Mln}jX6x;R$RHT+PxHuct>^F2Sg<)G;5fgO;Sm;&vZ8>CG|H)Dr--zKiwLJH*CMd4yVEb3l'
    b'qM6ceo@YlttYMeC~3!7&&CRCVtG6|J*U8&)Ez)gL(>6Ax6GRZ-I&d}HI-'
    b'G@$%x>!LSAScWgl++1F?drZm_m$t&2xS5jxp7xK;}MhK^VRemWIIy!ZIosjK^(N`i05=hd+;|1s|I|`M2G7#NxbI`7usmLC<^}wK'
    b'uTry<!j5Fgo)Eq4t570mwRY6@G&DzjeO};i0%Yln$|jWNcTb&vPeZ-'
    b'51vbio#bnTe#^3gNJgNxdnON_r320o!<HIEA<zPuQ($eTM`G55=Ar7UC5EXr=M$13<BG)IEjTko%b{Te=;M><lVOH;>HGp(l@A`o'
    b';ekKr!+4$fd|&fmqfkA7`#d<Fph%4rMPOu||5hqsFe93M;SeUF8<6Ib&O^=o&X^RU6~}c-'
    b'h`{mEMKiGj<2W&0(|Ho~ugmdcgkPgB3(D}Nph-'
    b'6d{c~W>rx>RjuAFM)1Qc#JT%idgJyJh!<Y`)G0%LWxfi|B|N8<5BX+zO3Y>IM}glmnmzIY>d{T_{<s2bZmrD?V2g{f0Nhp5&09Ks'
    b'DSGm=*dyX%M^?hY(=zHw$CeT{GIb&^?BIAc+G=4n~C4NeOU;ihxFjFjdg0lxqaRis_|=Y}gMy7Ot&`tZ*%(2oy~hCQ&#gG?52=>p'
    b'~&X-iHi<e@7mHfA-WF!I)G7OrnHI9*)hwHwIkaF5e@O~hY9b7-b}BT7QV=>^?^hSQ^(LUkaS-&}edx4AC-aHw?CdSmmIkX~mJeKP'
    b'!<a!$R}RJ)*~rdM!MvM@o5P4Db#1sc;e;<t$b;qG-R=tCrh^plqsdL6W!vUO`4DXclejiA9C!#H{yUG8)f9)I-txeOadk=GmK*F-'
    b'|_?_V<LX0(P+?KRDIc?@BmkyZ3x+k+ZRY%1#Kq?hL@A3vTE6rsTKY5I1t*Og{XQd~M+`|PLgD3lwlS9e(T5)+!O>!KuFMAMwuTo;'
    b'LlnW1%kUtbP?dO1pax{6#|hSIn#l%;EvQDLQA?JZb={8*oB*pl8@Kt?jUbOr$FJK%I%qzCkU)4dIm52ZbIH}5TR_BZfE@cc=o)?H'
    b'u6!Dt-@{2n2t_mffVL@-'
    b'X<F`WA5QhFT?7jaJ}{C018<pG>M23qCeZ?Fcl@^~$*c7U_!$|kv;2xxw9IiS@QfTVQ@GRcni>OBnbXWPn}A7vjHZFC$eUe|p0GUm'
    b'|+;dp$Pa-3w6Q=^hqq6s;t`L(vUC`ii{u+aWYe(cX=Sl7LG5Ir=FndZlE_#iR9TjK`yW<Om6j@P%TWB3RKyHBf;jgq#-'
    b')Qk$5UNO?;*p_CM`a0!?-@FRXNs0Q5l$U7pxk$nZwwzegsTic<1mSl-'
    b'J(r$rJnX=j)`=K+>#n*qv({~foTpxvqj#K@OBmqhPye@kk;HE?gBPU#6l;$9u6<_4s@cp`q@%To$25^143MRMv@u(k2J2E9y$N8A'
    b'Q{tw6-q(^ky;z~8eVQ6QNSgD}RB4b-5b5l63K1FS=Mv+PbRh>JndhB7?~-~NUkN!4ifo@-'
    b'BR?;wMycb}7x7!s07!zW8*<mtD~|yAwa^IXvv00JVCKsVPK|Pcty8rm3KX@Yqsr@GjFYapoPi+Gs~Qpw))m$(Rw6rOOlL(S^-'
    b'#2r#CL(<w<cb^W=wo`W_EHLgw=YQ_E#U%MPQW*>2)j&%8m<Xweb8DqE~=v)tjVSTYCb(E6~3+U+jc_$8@VFNrMWRgbZVTv`~zUzR'
    b'1U^E7TLRN3S7S%~lRt^hqyVhO*V*tSFvktvjsPPKzbn7qr>&FxCme=~0^*1keQ&eXI7~O^l>wLv((|+d%)6*K}eAC$;6Ii=Cp_X('
    b'jRBq@Z<DqCYkZ>GVbfA0_%@i*7!6<8=+P&m4u*je2w@gYc%_89nowU@BrrZ;u`=_NT)IOPb@gs#`d<sqE+q(7ooSkH$|DjMEg^%V'
    b'idH5Rantfo2~06H2;yubimkwxL)fTy_jPjr4S8$1q3$|CzoV?gXMv6E9AClYWaeotD+T7EgROzd8w8rvd-'
    b'1yE>d?k`ptWr%u^fuRF=$KuoKhj8et9>$(H=92WZN?TVX9<f}W4`{qHqSo&LxG|aqZ>-`U;mFd-'
    b'^xym&c?a(5b>gM;Shlv@7>xy2a`FPwZJzn2poZ`l*i*-'
    b'ri$a*2Aj^F6bSM$~)#G85thPHy$rZ<t1^crp5k`O~LdV?_uF`Svf=avJf^(m)Kj7|jOl;KX{=XE!b(?wZ6+cC%j%@wY!efEp=t;n'
    b'~&uLbD1Xu^^lC*vRXNSk<9BjrweDcMA?bYCCtbnMg1K$jNx3f6m(cGIDkrMx)W$nZJfvFh1ro;3=5I>-y6I-'
    b'PJvq|cM@T)Nlk3LiT^CJ5VjY}YLocT}Lb=-'
    b'`l6aig}06FG+te5LJ?bF2&OYV}dW^t|s}pwkcrq|yWS0dItnoero1iecY1h!1t2HtAyF&t6Fr<u~<kbT9kgeDPtBj$X^4OFB-oV5'
    b'd#gl{SxWok$<I16MELX?DZ@tg*rhRHl#fy`I3SQBK7;Evq9OckJ4yO~mvGzhkG-'
    b'=sWkMZO|_QKUNlKLdnubBh;*`NeM0cM~V8}ROH1|K2iKz+fCi9htHJ!Pu<|@wX4Gi(!J!h4^TKsNT;b)r?;7VEfC1=g}LUK?eIq<'
    b'd}n&QT<zhdmCbaEPC&~pU9Um~dqvs9L?^F5VKULSMEKo3w${r|6>&v==w0c=h~8R7Z3C%Bp6T_Mb;&nq89AW|lke4=PUz=_#ZK<d'
    b'XNt^ghSta3ZS5gn`_O&3{0IwYaO-'
    b'L^^JzkU!pMhb7ZqPJJ_62%#PJt&!LGg|<+Q905b=l#IuvbSsKCP^U7pTm^XUulp(rk$ZI)UC!}h>_XT2rL$ZB7_@j7?svm5BQ))|'
    b'sv6!w!qr1xi+S0q+0f%0<K{XMbQtrzc!3LyH0N1`+739z?r-'
    b'@b9WV#sMqzUn<ZbrQ+}f{`{R4YFRTwqZspf;@)I$rgUuL^FsaG&4e=)&6}2hSM&2uWK!Q6onJ|{Z^yAc9Hos%1J^x%?hA+$T009q'
    b'B#=vR7-'
    b'Q!N%{&EzKv{&S4XOF>N@F%qIjsxHV;Z|_@<`ULCZC99>C3Lb&<=85NNCE9nv?+zV!O+4WUq&;82)dMkrgy<JxoH8uwG~&glg}P8S'
    b'~i*4`wq{eC`&!hQ=xoen-'
    b'Z&HFi_pAq=<&BzCa(Anj5kxE_D54FX`{{`v_J)*_y9CVF#*jOp5*LJe`lT)isBjv?YuqwIGbx9c>2o;W=ZFDZuRJU5rjtj4=YTpN'
    b'C#d5XOmciF{5P;72v~`>dGA!tZ)!M+ML8)i!E-'
    b'M^4q=f;yvw|E8!EKEw2(2Ux768l0`PRnCmN{*Ja3YuyMmPljIJ772&&yQL0lP4dy7R@bihBhe)vQy^0P#v9^G&Y;2*-'
    b'ERwAW5>ALr|2S)HcjHxB1^e3xci0-XXJY5vgAggHv=SED1cYW)y!0GcSjFIgsn()Ze~0~4dSx~@#ot&Kg?lt_RStzkSwIxY-hj!4'
    b'=0uAo~wVTy|*!;{ACt3-'
    b'*urxhj2*;>OKgPzISZnw2`L{_xeVFT1+h^qR5gd2HG2zUIeuYvxp{WnOs6cBpQ^+X|>?)V5pyDpOTVFG|qXb!-'
    b'xYrtdGD+c=tt?SfB|K?PK>?~j;x~?02cQUa2CFxCsj6W)LJlzfnH_=}57tAW)u2P>t@zs7#D?)i4JCeKyaMdk+2jJ;L9B?9rfdR;'
    b')*6}c2PrKs8#b}^*rsg!AVaw^NUnfQ3HAfLbv)*%`q+#FMZTAVRk=8(H4Rm8A2D^+2?q&tBV-)yA*X@#m-'
    b'nG%im?)cY7|jd?k4`)w2kD4#1Ja(K8csThyLLHc7&Qc(`Hpqp2|K4od95TmnM9xCdrr>RX<^Ch#+k|>r@mjI$w&xI);!%gc95TYS'
    b'MBo86LqD<+5|RBq=M-<mR?)-HqbsJ<s=1u>)s?MVUj6y;Eyc@bea}Owjq8EftK~^-'
    b'p3P~=vGHDK@~zwW))BeBtvz+`%vZy`mR>BJpkv|lHD6m2wIcKw^%;sBgyNe;zmHgY)XAHsMX~sOzwaFf2SDSOa'
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
    candidate = histogram  # noqa: F405
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
