import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [['Example'],
 ['Mudasir Hanif '],
 ['Yellow Yellow  Dirty  Fellow'],
 ['Exa   mple'],
 ['   Exa 1 2 2 mple'],
 ['Hello,   world!'],
 ['happy 123'],
 ['Hey    there!'],
 ['  spaces  every  where  '],
 ['NoSpacesHere'],
 ['This is  a  test'],
 ['Testing     1  2   3'],
 ['Hello World'],
 ['Hello   World'],
 ['   Hello World'],
 ['This is  a  tesst'],
 ['This is  a  tes'],
 ['This is  a This is  a  tes test'],
 ['Hello r  World'],
 ['This is  a Hello r  World tsesst'],
 ['This is  a This is  a  tes test  spaceNoSpacesHere '],
 ['Thish is  a  tesst'],
 ['HelloNoSpacesHere,   world!'],
 ['Hey   e there!'],
 ['  spaces  eveThis is  a This This is  a This is  a  tes test  spaceNoSpacesHere is  a  tes '
  'testry  where  '],
 ['happy 123  spaces  every  where  '],
 ['  spaces  eveThis is  a This  This is  a This ishappy 123  a  tes test  spaceNoSpacesHere is  '
  'a  tes testry  where  '],
 ['Hello r  Word'],
 ['This is  a sst'],
 ['  spaces  eveThis is  a This This is  a This is  a  tes test  spaceNoSpacesHello r  WorldHere '
  'is  a  tes testry  where  '],
 ['  spaces  eveery  where  '],
 ['happy1233'],
 ['  spaces  eveThis is  a This This is  a This is  a  tes test  spaceNoSpacesHeNoSpacesHerello r  '
  'WorldHere is  a  tes testry  where  '],
 ['happy 123 p spaces  every  where  '],
 ['  spaces  eveThis is  a This This is  a This is  tes testry  where  '],
 ['Thish isThis is  a Hello r  World tsTesting     1  2   3 a  This is  a ssttesst'],
 ['Helleo World'],
 ['happyw 123 p spacees  every  where  '],
 ['Thish is  a  tesHey    there!st'],
 ['happyw 123 p spacees  This is  a sstevery  wher  '],
 ['  spaces  every  w here  '],
 ['Th is is  a This is  a  tes test'],
 ['This is   a This is  a  tes test  spacoeNoSpacesHere '],
 ['  spaces  eveThis is  a This  This is  a This is happy 123  a  tes test  spaceNoSpacesHere is  '
  'a  tes testry  where  '],
 ['Thihappyw 123 p spacees  This is  a sstevery  wher  s is  a Hello r  Woreld tsesst'],
 ['  spaces  eveThis is  a This This is  a This is  a  tes test  spaceNoSpacesHtry  where  '],
 ['happThis is  a  tessty'],
 ['This is  a T  spaces  eveThisTh is is  a This is  a  tes test is  a This  This is  a This '
  'ishappy 123  a  tes test  spaceNoSpacesHere is  a  tes testry  where  his is  a  tes test'],
 ['This is Thish is  a  tesHey    there!st a This is  a  tes test  spaceNoSpacesHere '],
 ['Thish is  asst'],
 ['  spaces  everThis is  a This is  a  tes testy  where  '],
 ['This is  This is  a T  spaces  eveThisTh is is  a This is  a  tes test is  a This  This is  a '
  'This ishappy 123  a  tes test  spaceNoSpacesHere is  a  tes testry  where  his is  a  tes '
  'testa  tes'],
 ['  spaces  eveThis tis  a This This is  a This is  a  tes test  spaceNoSpacesHere is  a  tes '
  'testry  where  '],
 ['  spaces  eveThis is  a This This is  a This is  a  tes test  spaceNoSpacesHello r   WorldHere '
  'is  a  tes testry  where  '],
 [' happyw 123 p spacees  every  where  '],
 ['happyw 123 p spacees  This is  a sstevery  whser  '],
 ['  spaces  eveThis is  a This This is  a This is  a This is  a  tes test  spaceNoSpacesHere This '
  'is  tes testry  where  '],
 ['haappy1233'],
 ['Testing   Hey   e there!  1  2   3'],
 ['Hello r   spaces  eveThis is  a This This is  a This is  a  tes test  spaceNoSpacesHello r   '
  'WorldHere is  a  tes testry  where   Word'],
 ['Testing   s  1  2   3'],
 ['Th is is  a This is  a  tes teHello,   world!st'],
 [''],
 ['ThThis is  a Hello r  World tsesstis is  a sst'],
 ['This is  This is  a T  spaces  eveThisThh is is  a This is  a  tes test is  a This  This is  a '
  'This ishappy 123  a  tes test  spaceNoSpacesHere is  a  tes testry  where  his is  a  tes '
  'testa  tes'],
 ['This is  sst'],
 ['NoSere'],
 ['ThTthis is  a Hello r  World tsesstis is  a sst'],
 ['This is  a This is  a  tes test  spaceNioSpacesHere '],
 ['This iis  a sst'],
 ['Thihappyw 123 p spacees  Thi s is  a sstevery  wher  s is  a Hello r  Woreld tsesst'],
 ['This is  a This istest'],
 ['Helleo Worldhappyw 123 p spacThis iis  a sstees  every  where  '],
 ['Hello r  Worlld'],
 ['Testing This is  a sst  e there!  1  2   3'],
 ['ere!st'],
 ['This is  a This is  a  t  spaces  eveThis is  a This This is  a This is  a This is  a  tes '
  'test  spaceNoSpacesHere This is  tes testry  where  est'],
 ['Hhappy 123 p spaces  every  where  ello r  Word'],
 ['He  spaces  eveThis is  a This This is  a This is  a This is  a  tes test  spaceNoSpacesHere '
  'This is  tes testry  where  llo,   wod!'],
 ['rCMrcvK'],
 ['This sis  a  tes'],
 ['  spaces  eveThis is  a This This is  a This is  a This is  a  tes test  spaceNoSpacesHere This '
  'is  tes testr  where  '],
 ['  spaThis  This is  a This ishappy 123  a  tes test  spaceNoSpacesHere is  a  tes testry  '
  'where  '],
 ['Th is is  a This is  aHey   e there!  tes test'],
 ['Thish Helleo Worldhappyw 123 p spacThis iis  a sstees  every  where  is  a  tesHey    there!st'],
 ['Hello r   spaces  eveThis is  a This This is  a This is  a  tes test  spaceNoSpacesHellThish '
  'isThis is  a Hello r  World tsTesting     1  2   3 a  This is  a ssttessto r   WorldHere is  a  '
  'tes testry  where   Word'],
 ['Th is is  a This is  a  tes teTHello,   world!st'],
 ['ThTthis sis  a Hello r '],
 ['Thihappyw 123 p  spaces  eveThis is  a This This is  a This is  a  tes test  spaceNoSpacesHtry  '
  'where   spacees  This is  a sstevery  wher  s is  a Hello r  Woreld tsesst'],
 ['  spaces  everThis is  a This is  a  tes tThish Helleo Worldhappyw 123 p spacThis iis  a '
  'sstees  every  where  is  a  tesHey    there!stesty where  '],
 ['NoSer'],
 ['Thish Helleo Worldhappyw 123 p spacThis iis  a sstees  every  where  ishappy 123 p spaces  '
  'every  where    a  tesHey    there!st'],
 ['Hello rr  Word'],
 ['Hello r   spaces  eveThis is  a This This iThis is  Hey   e there!a This is  a  tes tests  a '
  'This is  a  tes test  spaceNoSpacesHellThish isThis is  a Hello r  World tsTesting     1  2   3 '
  'a  This is  a ssttessto r   WorldHere is  a  tes testry  where   Word'],
 ['HeThis is  a This istestlWlo World'],
 ['NoS'],
 ['Testing   Hey   e there!  1  2 This is  a This is  a  tes test  spaceNoSpacesHere   3'],
 ['  spaces  eveThis is  a This This is  a This is  a This is  a  tes test  spaceNoSpacesHere This '
  'is  tes testry  where '],
 ['NSooSerre'],
 ['Hello r   spaces  eveThis is  a This This iThis is  Hey   e there!a This is  a  tes tests  a '
  'This is  a  tes test  spaceNoSpacesHellThish isThis is  a Hello r  World happy 12Testing   s  '
  '1  2   33  spaces  every  where  tsTesting     1  2   3 a  This is  a ssttessto r   WorldHere '
  'is  a  tes testry  where   Word'],
 ['This is  This is  a T  spaces  eveThisTh is is  a This is  a  tes test is  a This  This is  a '
  'This ishappy 123  a  tes test  spaceNoSpacesHere is  a  tesHello r   spaces  eveThis is  a This '
  'This iThis is  Hey   e there!a This is  a  tes tests  a This is  a  tes test  '
  'spaceNoSpacesHellThish isThis is  a Hello r  World tsTesting     1  2   3 a  This is  a '
  'ssttessto r   WorldHere is  a  tes testry  where   Word testry  where  his is  a  tes testa  '
  'tes'],
 ['Helo r  Worlld'],
 [' happyw 123 p spacees  every  whhere  '],
 ['HTh is is  a This is  a  tehappy 123  spaces  everyHello r   spaces  eveThis is  a This This '
  'is  a This is  a  tes test  spaceNoSpacesHello r   WorldHere is  a  tes testry  where   '
  'Wordo,   world!stey   !'],
 ['Thish isThis is  a Hello r  World tsTesting 3 a  This is  a ssttesst'],
 ['   Exa 1 2 2\nmple\tExample   3'],
 ['   A-B-*_--C   '],
 ['---a-a-a---b-b-b-c-c-c---'],
 ['Big gaps    between words    in this sentence'],
 ['          '],
 ['    '],
 ['         '],
 ['Exa 1 2 2 mple'],
 ['Example  1'],
 ['    Example   2'],
 ['    Example   2    Example   2'],
 ['  E  Example   2'],
 ['this'],
 ['----a-a-a---b-b-b-c-c-c---'],
 ['     '],
 ['his'],
 ['words'],
 ['ExampleEthisxa3e  1'],
 ['Exx1'],
 ['  his   '],
 ['gaps'],
 ['ggaps'],
 ['ggga'],
 ['  his    '],
 ['   Ex     2\nmple\tExample   3'],
 ['---a-a-a---b-b-b-c-c-c---     '],
 ['Example    Example   2    Example   2  1'],
 ['A-B-*_--C'],
 ['EEx'],
 ['Exa'],
 ['   A-B-*_-E-C   Ex     2\nmple\tExample   3'],
 ['---a-ac-c---      '],
 ['ExampleEthisxa3e'],
 ['  his     '],
 ['2'],
 ['in'],
 ['  E  Egapsxample   2'],
 ['  ExampleE  Expample   2'],
 ['   Exa 1 2 Exa2\nmple\tExample   3'],
 ['  E  Ega psxample   2---sa-ac-c---'],
 ['ExampleeEthisxa3e'],
 ['zPb'],
 ['ExampleEt  E  Ega psxample   2---sa-ac-c---hisxa3e'],
 ['hsis'],
 ['  E  Example  2'],
 ['   A-B-*_-E-C   Ex     2\nmple\tExample  m 3'],
 ['EExample  1Ex'],
 ['  his    EExample'],
 ['psxample'],
 ['ExampleEthitsxa3e'],
 ['1'],
 ['----a-aa-a---b-b-b-c-c-c---'],
 ['---a--a-a---b-b-b-c-c-c---'],
 ['hsExampleEthisxa3es'],
 ['Expample'],
 ['his  ExampleE  Expample   2'],
 ['sentence'],
 ['Exa2'],
 ['   Exa 1 2 2\nmple\tExample   2---sa-ac-c---'],
 ['   Exa 1 2 Exa2\nmple\tEx3'],
 ['   '],
 ['   Exa 1 2 2\nmple\tExample 3'],
 ['ExampleEtEhisxa3e  1'],
 ['    E  Ega psxample   2---sa-ac-c--- A-B-*_-E-C   Ex     2\nmple\tExample   3'],
 ['hsE2xampleEthisxa3es'],
 ['Example    Example   2    Examle   2  1'],
 ['  hExampleEthitssxa3eis    EExample'],
 ['          EEx'],
 ['thits'],
 ['----a-a-a---b-b-b-c-c-c---ExampleEtEhisxa3e'],
 ['---a-ac-c---'],
 ['      psxample EEx'],
 ['E'],
 ['    his    A-B-*_--C   '],
 ['TnYIFZqaAz'],
 ['between'],
 ['zEx3Pbb'],
 ['gs'],
 ['      '],
 ['---a--a-a---b-b-b-c-c--c---'],
 ['   Ex     2\nmple\tExample   3i'],
 ['   Exa mpleample   3'],
 ['  hismpleample     '],
 ['thitts'],
 ['ExampleEt  E  Ega psxample   2---sa-ac-c---h-isxa3e'],
 ['  '],
 ['  his  hismpleample '],
 ['---a--a-a---b-b-b--c-c-c---'],
 ['word'],
 ['thi  E   Exa 1 2 2\nmple\tExample 3  2'],
 ['---a-ac-   A-B-*_-E-C   Ex     2\nmple\tExample   3c---'],
 ['Exampl   eEthishiExamlesxa3e  1'],
 [' Exx1   '],
 ['ggap'],
 ['  hExampleEthitssxa3eis    EExampple'],
 ['E  x3'],
 ['  his  h  hismpleample     ismpleample '],
 ['R'],
 ['   Ex     2\nmple\tExample   ExampleEi'],
 ['ExampleEtEhisxa3e  1gggaps'],
 ['hsExmampleEthisxa3es'],
 ['ExaxmpleEthitsxa3e'],
 ['   Exa 1ExampleEtEhisxe  1gggaps   3'],
 ['gss'],
 ['           '],
 ['hhis'],
 ['gggga'],
 ['Exampl'],
 ['ExampleEtExampl   eEthishiExamlesxa3e  1'],
 ['    his    A-B-*           _--C   '],
 ['ExampleEtExampl'],
 ['hhi---a-a-a---b-b-b-c-c-c---s'],
 ['---a--a-a---b-b-b-c-c--'],
 ['Big gaps    between words    i2---sa-ac-c---n this sentence'],
 ['Exam    Example   2pleEtEhisxa3e  1'],
 ['2---sa-ac-c---'],
 ['11'],
 ['dwords'],
 ['betweeExampleEthisxa3e  1n'],
 ['hhi---a-a-a---  E  Ega psxample   2---sa-ac-c---b-b-b-c-c-c---s'],
 ['E  E2---sa-ac-c---b-b-b-c-c-c---sx'],
 ['hhi-    his    A-B-*           _--C   --a-a-a---'],
 ['hsExampthitsleEthisxa3es'],
 ['ismpleample'],
 ['hhi---a-a-a---'],
 ['hsExampleEtheisxa3es'],
 ['   Exa mp  leample   3'],
 ['ExampleEt  E  Ega psxample   2---sa-ac-c---h-isx'],
 ['EleEatEhisxa3e  1'],
 ['  hs'],
 ['---a--a-a---b-      psxample EExb-b-c-c--'],
 ['s'],
 ['ExExamplampleEthisxa3e'],
 ['   his  h  hismpleample     ismpleample '],
 ['---a-ac-ca---'],
 ['  hExa  hsmpleEthitssxa3eis    EExample'],
 ['A-B-*_  hExampleEthitssxa3eis    EExampple-E-C'],
 ['ExExamplampleEt  E  Example   2hisxggggaa3e'],
 ['---a-a-a----c---     '],
 ['Exampitsxa3e'],
 ['----a-a-a---b-hsmpleEthitssxa3eisb-b-c-c-c---'],
 ['thtis'],
 ['---a-ac-c-thitts-'],
 ['hihis'],
 ['---a-a  ExampleE  Expample   2  3c---'],
 ['wo'],
 ['Exaword'],
 ['thhisis'],
 ['hhi-'],
 ['    his     A-B-*_-E-C   Ex     2\nmple\tExample  m 3thitssxa3eis    EExample-C   '],
 ['zPPb'],
 ['EExampple-E-C'],
 ['E  c-c-c---sx'],
 ['i2---sa-ac-c---n'],
 ['    his   Exx1   --C   '],
 ['ExampleEtEhisxa3e'],
 ['hhi---a-a-a---c-c---s'],
 ['Exmpl'],
 ['3'],
 ['Rhsis'],
 ['sjRboRkSy'],
 ['2---sa-ac-c---h-isx'],
 ['mples'],
 ['Exa3c---leEtEhisxa3e'],
 ['hsE    his   Exx1   --C   xmampleEthisxa3es'],
 ['i2---sa-a-c-c---n'],
 ['   Exa 1 2 Exa2\nmpl'],
 ['thi'],
 ['hsExampleExthisxa3es'],
 ['hh'],
 ['hhhis'],
 ['hsE    his   Exx1   --C   xmampleEthis   Exa mp  leample   3xa3es'],
 ['EExample-C'],
 ['2  2   '],
 ['2---sa-ac-c---h-isxa3e'],
 ['3xa3es'],
 ['his  ExampleE  E3thitssxa3eisxpample   2'],
 ['Exam'],
 ['---a-ac-   A-B-*m_-E-C   Ex     2\nmple\tExample   3c---'],
 ['2----sa-ac-c---'],
 ['thhiss'],
 ['wodhhi-s'],
 ['FoFlZTDagW'],
 ['   Exa 1 2 2\nmple\tExBig gaps    between words    i2---sa-ac-c---n this sentenceample 3'],
 ['ExampleEtExpampl'],
 ['   Exa 1 2 2\nmple\tExa---a-ac-mple 3'],
 ['   Exa mp  leample   3Example  1'],
 ['Exa---a-ac-mple'],
 ['Example'],
 ['sgs'],
 ['---a-thits-a-a---b-b-'],
 ['xmampleEthisxa3es2  ExaxmpleEthitsxa3e3c---'],
 ['his  ExampleE     2'],
 ['  ---a-ac-c---       Example   2'],
 ['3c---'],
 ['ggagp'],
 ['EFoFlZTDagWE'],
 ['hs'],
 [' p ExaxmpleE  Expample   2'],
 ['111'],
 ['ggagExampleEtEhisexa3gep'],
 ['   Exal mp  leample   3'],
 ['gapshhi---a-a-a---  E  Ega psxample   2---sa-ac-c---b-b-b-c-c-c---s'],
 ['ga Exx1   s'],
 ['---a-a-a----c---'],
 ['wwo'],
 ['   Exa 1ExampleEtEhmisxe  ggaps   3'],
 ['A-B-*'],
 ['    Example   2    Example words  2'],
 [' Ex3  Ex     2\nmple\tExample   3i'],
 ['thhi'],
 ['iin'],
 ['--a-a-a---'],
 ['his  ExapmpleE  E3thitssxa3eisxpample   2'],
 ['---a-ac-c-a---'],
 ['jgOtGgdMm'],
 ['ExampleEt  E  Ega pshhi---a-a-a---b-b-b-c-c-c---sxample   2---sa-ac-c--11-h-isx'],
 ['1gggaps'],
 ['-E  c-c-c---sxxample EExb-b-c-c--'],
 ['hhi-hhh'],
 ['   Exa 1gaps   3'],
 ['hsExampleExthi  hssxa3es'],
 ['----a--a-a---b-b-b-c-c--c---'],
 [' p Exax  Expample   2'],
 ['ExExameplampleEthisxa3e'],
 ['thi  E   Exa 1 2 2\nmple\tExampExampleEtle 3  2'],
 ['hsmpleeEthishiExamlesxa3eEthitssxa3eis'],
 ['---a-a-aExampleEt  E -c---hisxa3e--c---'],
 ['  hExampxleEtEhisxa3e  1ile'],
 ['EleEatEhisxa3e'],
 ['ExampleEi'],
 ['wo_--C'],
 ['Exampl   eEthish iExamlesxa3e  1'],
 ['c-c-c---sxxample'],
 ['   Exple   3'],
 ['  his '],
 ['   hi s  h  hismpleample     ismpleample '],
 ['gapshhi---a-a-a---  E  Ega psxample   2---sa-ac-c----b-b-b-c-c-c---s'],
 ['  E  Ega psxa   Ex     2\nmple\tExample   3mple   2---sa-ac-c---'],
 ['A-B-*_'],
 ['     his   Exx1   --C       '],
 ['sentenceample'],
 ['ggs'],
 ['    Example   2    Example   2   Exa 1ExampleEtEhisxe  1gggaps   3'],
 ['c-c-c----sx'],
 ['hsmpleEthitssxa3eis'],
 ['  his  hi2hisxggggaa3e '],
 ['----a-ac-c-thitts-'],
 ['2   2   '],
 ['Ex3ampleEtEhisxa3e  1'],
 ['his  Exam   A-B-*_-E-C   Ex     2\nmple\tExample  m 3pleE  mE3thitssxa3eisxpample   2'],
 ['   Ex     2\nmple---a-a-a----c---\tExample  eEi'],
 ['   Exa 1 2 2\nmple\tExBig gaps    between words    i2---sa-ac-c---n this sentenceeample 3'],
 ['-E'],
 ['---a--a-a---b-b-Example  1-c--c---'],
 ['  E  Ega psxample   2---sa-ac-c-  E  Example   2--'],
 [' Exx   Ex     2\nmple\tExamhhple   3i1   '],
 ['hsExampleExthi  hssxA-B-*_--Ca3es'],
 ['    his    A-B-*          3i1 _--C   '],
 ['E2---sa-ac-c---b-b-b-c-c-c---sx'],
 ['  E 2 Example   2'],
 ['A-B*--*_--C'],
 ['gapshhi---a-a-a---'],
 ['thi  E   Exa 1 2 2\nmple\tExampExamplE  c-c-c---sxeEtle 3  2'],
 ['cc-cggs-c---sxxcample'],
 ['hhi---a-a-a---b-b-b--c-c-c---s'],
 ['sggs'],
 ['  EExb-b-c-c--  Example   2'],
 ['ss'],
 ['   Eexa 1 2 2\nmple\tExample 3'],
 ['gapshhi---a-2---sa-ac-c---hisxa3e---'],
 ['mple---a-a-a----c---'],
 ['xmampleEthisxa3es'],
 ['ggss'],
 ['E E x3'],
 ['sjRboRkS'],
 ['  his   hi2hisxgEleEatEhisxa3egggaa3e '],
 ['EEE'],
 ['ExampleEtExampl   eEthishiExamlesxa3e  e1'],
 ['hhh'],
 ['   his     '],
 ['22--'],
 ['   3'],
 ['---a--a-a---b-b-b-c-bismpleample'],
 ['c-c-c---sxxamplthi  E   Exa 1 2 2\nmple\tExampExampleEtle 3  2e'],
 ['   A-B-*_-E-C   Ex     2\nmple\tExamp1gggapsle  m 3'],
 ['Examle'],
 ['    Example   2    Example words  22'],
 ['tshitts'],
 ['2---sssa-ac-c---h-isxa3e'],
 ['his  ExExampl   eEthishiExamlesxa3e  1ampleE  Expample   2'],
 ['Examhhple'],
 ['hsE'],
 ['hisExampBig gaps    between words    in this sentenceleEthisxa3es'],
 ['ExampleEtEhisx'],
 ['senteExamplnce'],
 [' p ExaxmpleE  Expample a  2'],
 ['dwoc-c-c---sxeEtlerds'],
 ['Exal'],
 ['hsmpleeEthishiExame1lesxa3eEthitssxa3eis'],
 ['E sc-c-c---sx'],
 ['worrd'],
 ['Exam    Example   2pleEA-B-*_-E-CtEhisxa3e  1'],
 ['Eexa'],
 ['betweeExasxa3e  1n'],
 ['sss'],
 ['ExampleEtEhis3xa3e'],
 ['   A-B-*_-E-C   Ex     2\nmple\tExampsenteExamplnce1gggapsle  m 3'],
 ['2---sa-ac-c-Exax--'],
 ['Eampl'],
 ['IclExampleEthisxa3e  1'],
 ['---a--a-a---b-b--Example  1-c--c---'],
 ['bet3e  1n'],
 ['---a-a--a----c---'],
 ['hsExampleExthi ExampleEi hssxA-B-*_--Ca3es'],
 ['EExx'],
 ['IclExample'],
 ['fwlMxhGm'],
 [' sentenceleEthisxa3esc-c---'],
 ['hjnY'],
 ['2   2'],
 ['2hsExampleExtEleEatEhisxa3e  1hi2--'],
 ['ga'],
 ['    Example   2    Exampxle   2'],
 ['ExamxpbetweeExasxa3e  1nl'],
 ['---a-thits-a-a- sentenceleEthisxa3esc-c-----b-b-'],
 ['ybsTcN'],
 ['dw   his     ords'],
 ['2---sa-ac--c---'],
 ['htsExampthitsleEthisxa3es'],
 ['hsihis'],
 ['ihihis'],
 ['  E  ExaExx2'],
 ['---a-thits-a-a- sentenceleEthisxa3esc-c-----bggagp-b-'],
 ['EExampple'],
 ['Exmp---a--a-a---b-b-Examplel'],
 [' sRentenceleEthisxa3esc-c--'],
 ['-   '],
 ['ExampleEmtExampl   eEthishiExamlesxa3e  e1'],
 ['  ExampleE  Expamplp2'],
 ['---a-thits-a-a- sentenceleEthisxa3esc-c-----his  ExampleE  Expample   2b-b-'],
 ['Exampthhisisa3e'],
 ['--C'],
 ['KsMcxuu'],
 ['ce-c-c---sxxample'],
 ['22  2   '],
 ['_--C'],
 ['EExpampl'],
 ['xmamspleEthisxae3es'],
 ['-ExapmpleEc-thitts-'],
 ['his  Exam   A-B-*_-E-C   Ex     2\nmple\tExample  m 3pleE  mE3thitssxa3ei   2'],
 ['ple'],
 ['3Example    Example   2    Example   2   Exa 1ExampleEtEhisxe  1gggaps   3'],
 ['ExampleEtExampl   eEthishiExamlesxa3e p e1'],
 ['1gapszzPPb'],
 ['DQaiLlVsgN'],
 ['    his     A-B-*_-E-C   Ex     2\n'
  'mple\tExample  m 3thitssxa3eis    EExample  hismpleample     -C   '],
 ['ExamplhsEteEthitsxa3e'],
 ['ExampleEt  E  Ega psxample   2---sa-abetweeExasxa3e  1n-isx'],
 ['Ku   A-B-*_-E-C    Ex     2\nmple\tExample   3Mcxuu'],
 ['ssgs'],
 ['---a-thits-a-a- sentenceleEt p ExaxmpleE  Expample a  2-b-b-'],
 ['ExaxmpleEthitsxa3e3c---'],
 ['ExampleEt   E  Ega pshhi---a-a-a---b-ggsb-b-c-c-c---sxample   2---sa-ac-c--11-h-isx'],
 ['sentenceleEthisxa3esc-c---'],
 ['thmple'],
 ['ssss'],
 ['cc-cggss-c---sxxcample'],
 ['Ku   A-B-*_-E-C    Ex     2\nmple\tExample   cc-cggs-c---sxxcample3Mcxuu'],
 ['  hExampleEthitssxa3eis Ex3ampleEtEhisxa3e  1   EExample'],
 ['sentenceleEthisxa3esc-c-----his'],
 ['3Mcxu     u'],
 ['gsss'],
 ['   A-B-*_-E-C   Ex    hismpleamplegapsle  m 3'],
 ['---a-thits-a-a  his    ---b-b-'],
 ['zExmplPb'],
 ['EExammle'],
 ['---a-a  ExampleE  Exp-ample   2  3c---'],
 ['EF2---sa-ac-c--11-h-isxoFlZTDagWE'],
 ['  his EF2---sa-ac-c--11-h-isxoFlZTDagWE'],
 ['hExampleEthitssxa3eis'],
 ['hsExampaleEtheisxa3es'],
 ['h'],
 ['T'],
 ['_wo_--C'],
 ['2hsExampleExtEleEatEh-isxa3e  1hi2--'],
 ['A-B---C'],
 ['2hsExampleExtEleEatEh-is-'],
 ['   Ex     2ple   3i'],
 ['his  ExampleE      2'],
 ['  his   ExampExampleEtle EExample'],
 ['mE3thitssxa3eisxpample'],
 ['    his     A-B-*_-E-C   Ex     2\n'
  'mple\tExample  m 3thitssx   A-B-*_-E-C   Ex     2\n'
  'mple\tExample  m 3a3eis    EExample-C   '],
 ['c-c-c---sxxamplthi  E   Exa2 2\nmple\tExampExampleEtle 3  2e'],
 ['    his   Exx1 Exa2--C   '],
 ['2pleEtEhisxa3e'],
 ['xal'],
 ['    Example   2     Example words  22'],
 ['Examxpbetw--CeeExasxa3e  1nl'],
 ['hhi---a-a-a---b-b-bKu-c-c-c---s'],
 ['2----sa-aciin-c---'],
 ['rpfY'],
 ['c-c-c---sxeEtle'],
 ['---a--a-a---b-b-Example'],
 ['----a-aa-a2-b-b-c-c-c---'],
 ['Examxpbetweel'],
 ['ExampExamplE'],
 ['wodhhi-ws'],
 ['1ileExBig'],
 [' ExampleEtEhisx  Exa mp  leample   3'],
 ['2hsExampleEis-'],
 ['zExmbplPb'],
 ['2  2---a-a--a----c---   '],
 ['----a-a-a---b-b-b-c-c-c---ExamplceEtEhisxa3e'],
 ['2---sa-abetweeExasxa3e'],
 ['Ega'],
 [' ExampleEtEhis  his   ExampExampleEtle EExamplex  Exa mp  lmeample   3'],
 ['---a--ba-a---b-b-b-c-bismpleample'],
 ['beteweeExasxa3e  1n'],
 ['Exa1ExampleEtEhmisxemple  1'],
 ['hhi----a-thits-a-a- sentenceleEthisxa3esc-c-----bggagp-b-hhh'],
 ['3pleE'],
 ['wordss'],
 ['---a-a'],
 ['Exa3c--i-leEtEhisxa3e'],
 ['EExam  E  ExaExx2ple  1Ex'],
 ['hhihh'],
 ['---a---b-b-b-c-c-c---ExampleEtEhisxa3e'],
 ['plethmple'],
 ['xalxmamspleEhhhi---a-a-a---b-b-b--c-c-c---sthisxae3es'],
 ['g    his    A-B-*_--C   gs'],
 ['hiss'],
 ['n'],
 ['gsentencele-a---'],
 ['PzPPb'],
 ['2---sa-ac---c---'],
 ['3Example'],
 ['  hjnYExample'],
 ['--CC'],
 ['---a--a-a---b-'],
 ['--CExampleEmtExamplC'],
 ['Examxpbe2   2tw--CeeExasxa3e  1nl'],
 ['22EExample-C--'],
 ['     his   Exx1   --C       d'],
 ['EExc-c-c---sxeEtlepampl'],
 ['ExampleEt  E  Ega psxample   2---sa-ac-c---hisxa3eE'],
 ['1   Exa 1 2 2\nmple\tExBig gaps    between words    i2---sa-ac-c---n this sentenceample 3aps'],
 ['hExampxleEtEhisxa3e'],
 ['sentenceleEthicsxa3esc-c---'],
 ['mplees'],
 ['   Ex     2\nmple\tExample   ExmampleEi'],
 ['         Example   2    Example   2   Exa 1ExampleEtEhisxe  1gggaps   3      '],
 ['gW'],
 ['htsExampthitsleEthisxahhi---a-a-a---b-b-bKu-c-c-c---s3es'],
 ['i2---s-a-a-c-c---n'],
 ['sentenceleEt3mplehicsxa3esc-c---'],
 ['---a--a-a---b-b-b-c-c----'],
 ['  his  h  hismplhsExampleExthi ExampleEi hssxA-B-*_--Ca3eseample     ismpleample '],
 ['wordrd'],
 ['thitExampExampleEtles'],
 ['   A-B-*_-E- C   Ex     2\n'
  'mple\t    E  Ega psxample   2---sa-ac-c--- A-B-*_-E-C   Ex     2\n'
  'mple\tExample   3ampsenteExamplnce1gggapsle  m 3'],
 ['  E  xaExx2'],
 ['xaE sentenceleEthisxa3esc-c---'],
 ['zP----a-a-a---b-b-b-c-c-c---ExamplceEtEhisxa3e'],
 ['tsthitts'],
 ['3apswd'],
 ['ExExamplampleEt  E  Example   2hisxggaa3e'],
 ['thitteEthishts'],
 ['A-B-*m_-E-C'],
 ['sentenceleEthisxaa3es'],
 ['ExampleEt  E  Ega psxample   2---sa-ac-c---hisxa3e-C'],
 ['3thitssx'],
 ['---E  c-c-c---sxxample EExb-b-c-c----a-a-a---b-b-b-c-c-c---ExamapleEtEhisxa3e'],
 ['    Examp2pleEtEhisxa3eExample   2'],
 ['s3thitssxa3eis'],
 ['    his    A-BA-B-*_  hExampleEthitssxa3eis    EExampple-E-C-*           _--C   '],
 ['  hExampleEthitssxahsE2xampleEthisxa3es3eis    EExam'],
 ['1ampleE'],
 ['mE3tshitssxa3eisxpample'],
 ['2---sa-ac-c--  Exx1   -h-isxa3e'],
 ['   shis     '],
 ['A-B-*mA_-E-C'],
 ['ExExamplampleEt  E  Example   2hisx'],
 ['ithits'],
 ['---a--a-a---b-   Ex     2\nmple\tExample   ExmampleEib-b--c-c-c---'],
 ['hismpleamplegapsle'],
 ['nn'],
 ['hsE    his   Exx1   --CE   xmampleEthisxa3es'],
 ['Exeamggapsle'],
 [' s ExampleeEthisxa3e'],
 ['ExampsenteExamplnce1gggapsle'],
 ['bExametweeExasxa3e  1n'],
 ['---a--a-a---b-   Ex     2\nmple\tExample   ExmampleEib-b--cc-c-c---'],
 ['E1ExampleEtEhisxeaEzExmplPbEEE'],
 ['   Exa 1ExampleEtEEhmisxe  ggaps   3'],
 ['gaTnYIFZqaAzpshhi---a-a-a---'],
 ['2-    his     A-B-*_-E-C   Ex     2\n'
  'mple\tExample  m 3thitssxa3eis    EExample-C   --sa-ac---c---'],
 ['    his    A-BA-B-*_  hEx  hExampleEthitssxa3eis    EExamppleampleEthitssxa3eis    '
  'EExampple-E-C-*           _--C   '],
 ['cc-cggss-c---sxxcgapshhi---a-2---sa-ac-c---hisxa3e----ample'],
 ['   A-B-*_-E-C   Ex     2\nmple\tExample  E  c-c-c---sx3'],
 ['ExpampA-B-*_le'],
 ['2hsExampleExtEleEasRentenceleEthisxa3esc-c--tE2   2h-is-'],
 ['sRentenceleEthisxa3esc-c--'],
 ['thitExmE3thitssxa3eisxpampleampExampleEtles'],
 ['hisExampBig gaps    between words    in this sentenceleEthisxa3 es'],
 ['   Ex     22\nmple\tExample   3'],
 ['Exa-E'],
 ['hhis2---sa-ac-c---h-isx'],
 ['2---sa-ac-c-i--h-isxa3e'],
 [' '],
 [' a b c '],
 [' a  b  c '],
 ['        '],
 [' a   b c  '],
 ['ABC'],
 ['1 2 3'],
 ['百度是中国最大的搜索引擎'],
 ['Big gaps    between words    in thce'],
 ['Big gaps    between words    in this sen3tence'],
 ['  Big gaps    between words    in thce      '],
 ['        mple'],
 ['  Big        '],
 ['mple'],
 ['  Big gaps    between words    Big gaps    between words    in this sen3tencein thce          '],
 ['  Big            Example   2'],
 ['Exa 1 2 2 mplle'],
 ['   gaps'],
 ['wor  Big gaps    between words    Big gaps    between words    in this sen3tencein '
  'thce          ds'],
 ['thce'],
 ['mmple'],
 ['   Example  1 '],
 ['    Example 2'],
 ['sen3tence'],
 ['mmpleExample  1'],
 ['  Big            ExamExaple   2'],
 ['Big'],
 ['     Example   2   '],
 ['Exa 1 2 2 mpsen3tencee'],
 ['ExamExaple'],
 ['Exxa'],
 ['   A-BExample   '],
 [' Big gaps    between words    in thce  '],
 ['Big gap        mples    between words    in thce'],
 ['     gaps A-B-*_--C   '],
 ['sen3tencein'],
 ['se3n3tence'],
 ['Big gaps    between words     in this sen3tence'],
 ['mmpleExample'],
 ['mplExa 1 2 2 mpsen3tenceees'],
 ['Exa 1 2 2 mpl  Big            ExamExaple   2e'],
 ['mmpleE1'],
 ['   A-B-*_--C  Big gaps    between words    in this sen3tence- '],
 ['   A-gapsB-*_--C   '],
 ['t Big gaps    between words    in thce  his'],
 ['Exa 1 2 2 mpExample  1sen3tencee'],
 ['  Big gaps    between words    in thce      fKqrpAGA'],
 ['EExample  1'],
 ['  Big gaps    between words   o in thce      '],
 ['th   Exa 1 2 2\nmple\tExample   3s'],
 ['BiBg'],
 ['mfKqrpAGApleE1'],
 ['EExampEle  1'],
 ['BWnXAhX'],
 ['                    '],
 ['sen3tenncein'],
 ['EExa'],
 ['Ex     mmpleE1   ample  1'],
 ['mpsen3tenceees'],
 [' Big gap        mples    between words    in thce'],
 ['   A-gaps-B-*_*--C   '],
 ['  Big gaps    between words   o in thce          '],
 ['Ex    Example 2xa'],
 ['EExample'],
 ['   A-gaps-B-*_*s--C   '],
 ['         sen3tenncein'],
 ['   le   '],
 ['Exa 1 2 2 m'],
 ['tthhce'],
 ['Exa 1 2 2 mpsent3tencee'],
 ['Exa 1 2  2 m'],
 ['   A-B-*_--C   mplExa'],
 ['A-gapsB-*_--C'],
 ['BWnXAh'],
 ['fKqrpAGA'],
 ['Exa 1 2 2 mp'],
 ['Big gaps    bet ween words    in this sentence'],
 ['se3n3ntence'],
 ['EExa 1 2 2 mpsent3tencee2xa'],
 ['    ExampleEx    Example 2xa 2'],
 ['   A-B--*_--C   mplExa'],
 ['se3n           3tence'],
 ['Exa 1 2 2 mpl  Big            ExamExa 1 2 2 me'],
 ['ample'],
 ['th   Exae 1 2 2\nmple\tExample   3s'],
 ['BBig'],
 ['   A-x   '],
 ['   A-gapsB- '],
 ['ExxEa'],
 ['     gEExampleaps A-B-*_--C   '],
 ['sen3tence-'],
 ['Bg'],
 ['    2'],
 ['ExxA-xEa'],
 ['                   '],
 ['mplExa'],
 [' Big gaps    between words   Big         in thce  '],
 ['ttse3n           3tencehhce'],
 ['EEpxample'],
 ['A-gapsB-**_--C'],
 ['pBig gap        mples    between wo rds    in thce'],
 ['  Big            Exaple   2'],
 ['m'],
 ['sce'],
 ['EEpxampl'],
 ['xExxEA-xEa'],
 ['2xa'],
 ['ExamExaplae'],
 ['mmpleEmexample  Big gaps    between words   o in thce          1'],
 ['Big 3tenceds    in thce'],
 ['gap'],
 ['   A-B-*---a-a-a---b-b-b-c-c-c---_--C   '],
 ['ExamEA-gapsB-*_---Caple'],
 ['isenn3tenncein '],
 ['   le    '],
 ['me'],
 ['ggasen3tenceinp'],
 ['Ex    Examplxe 2xa'],
 ['BWnnX'],
 ['EEpxampl     '],
 ['tthhcewords'],
 ['A-_B--*_--C'],
 ['    le    '],
 ['EEx  a'],
 ['     gA-B-*---a-a-a---b-b-b-c-c-c---_--CEExampleaps A-B-*_--C   '],
 ['bet'],
 ['  Big   Exa 1 2 2\nmple\tExample   3        '],
 ['mpl   A-x   '],
 ['thh'],
 ['   x Example   2'],
 ['mplExa 1 2 2 mpsen3tenEExceees'],
 ['A-gapsB--**_--C'],
 ['  Big gaps    between words    A-xin thce      fKqrpAGA'],
 ['   x Example   2gap'],
 ['A-gapsB-'],
 ['mm'],
 ['Big gaps    bet ween words    in this senbtence'],
 ['3tenceds'],
 ['2e'],
 ['     gaps A-B-*_--C  msen3tenceinp thce'],
 ['     gaps A-B-*_--C  msen3tenceinp thcae'],
 ['mpscelle'],
 ['se3n'],
 ['Exaa'],
 ['    A-gapsB- '],
 ['EEExa 1 2 2 mpl  Big            ExamExaple   2e'],
 ['ExamExbetweenlae'],
 ['   Exa 1 2 2\nmple\tE  Big gaps    between words   o in thce          xample   3'],
 ['isenn3tenncein'],
 ['     ExampleEx    Example 2xa 2'],
 ['BWn  Big        XAh'],
 ['ExampleEx'],
 ['ggasen3tenceinpsce'],
 ['Big gaps    bet ween words    in this senbtenc   A-gapsB- e'],
 ['   x ExamEEpxample 2'],
 ['  in thce          '],
 ['2Big gaps    between words    in thcee'],
 ['tbet'],
 ['sen3tencte'],
 ['A-gapsB--**_--C Big gap        mples    between words    in thce'],
 ['Big gaps    between wocrds     in this sen3tence'],
 ['  Big   1 2 2\nmple\tExample   3 '],
 ['sen3tenecein'],
 ['2xExa 1 2 2 mpsen3tenceea'],
 ['A-gaps-B-*_*--C'],
 ['isennmpsen3tencee3tenncein '],
 ['mpsen3tenceeees'],
 ['mpsent3tencee2xa'],
 ['A-gapsB--**_--C Big gap        mples    between words    in thceEExample'],
 ['betmples'],
 ['  Big ga ps    between words    Big gaps    between words    in this sen3tencein '
  'thce          '],
 ['Exa 1 2 2 mpsen32tencee'],
 ['Big gaps    between words   '],
 ['pBiggap'],
 ['mpsen3tenEExceees'],
 ['rds'],
 ['BiBgg'],
 ['mmpleExample  ExampleEx1'],
 ['mmpl  Big gaps    between words   o in thce          eExample  1'],
 ['   ExampExaplele  1 '],
 ['Big gaps  A-gapsB--**_--C Big gap        mples    between words    in thce  between words   '],
 ['Exa 1 2 2  ampsen3tencee'],
 ['mplle'],
 ['se3n   A-gapsB- -C   '],
 ['Big gaps    between words    in this sen3tenwce'],
 ['tthhwords'],
 ['pBig gap        mples in thce'],
 ['am    A-gapsB- ExamExaple'],
 ['BWnXsenbtenceAhX'],
 ['CWSrjljyFR'],
 ['Big gaps    bet weens    in this senbtenc   A-gapsBmplExa 1 2 2 mpsen3tenEExceees- e'],
 ['amplmmpleExample  ExampleEx1'],
 ['ttse3n           3tencehhce    Example   2'],
 ['gaa'],
 ['    Ethcele  1 '],
 ['    Example  2'],
 ['th   Exa 1 2 2\nm3s'],
 ['   Exa 1 2 2\n'
  'mple\tE  Big gaps    betwe2Big gaps    between words    in thceeen words   o in thce          '
  'xample   3'],
 ['e'],
 ['   ExampExaplelea  1 '],
 ['A-gapsB--**_--C Big gap        mples    between words n   in thce'],
 ['sen3tenc  Big gaps    between words   o in thce          te'],
 ['weens'],
 ['   A-B--*_--C   mExampleplExa'],
 ['mExampleplExa'],
 ['th   Exa 1 2 2\nmple\tExample   3smp'],
 ['wse3n3ntenceor'],
 ['eExample'],
 ['Exa    ExampExaplele  1 1 2 2  ampsen3tencee'],
 ['isennmpsen3tencee3tennceinbet'],
 ['se3n   A-gap -C 3  '],
 ['mmpleExample gA-B-*---a-a-a---b-b-b-c-c-c---_--CEExampleaps ExampleEx1'],
 ['bets'],
 ['mp'],
 ['   A-Bb-c-c-c---_--C   '],
 ['EEpx'],
 ['   A-B-- *_--C    mplExa'],
 ['ExamEA-gapsB-*_a--m-Cap'],
 ['  Bi           Exaple   2'],
 ['pBig gap   *_--C     mples    between wo rds    in thce'],
 ['BWnX         Ah'],
 ['xExxEA-xEaExae'],
 ['sen3tenc'],
 ['mmpleExample p 1'],
 ['tthh'],
 ['isennmpsen3teEExampEle    Example  2ncee3tennceinbet'],
 ['  a                 '],
 ['  Big gaps    between wordae      fKqrpAGA'],
 ['BWnX         mmpleExample p 1Ah'],
 ['     Ethcele  1 '],
 ['ebS'],
 ['A-gaps-B-*_*s--C'],
 ['eaxa'],
 ['rrds'],
 ['sece-'],
 ['pBig gap   *_--C     mples    bet   A-gaps-B-*_*--C   ween wo rds    in thce'],
 ['A**_--C Big g ap        mples    bempl   A-x   hce'],
 ['t Biig gaps    between wordshis    in thce  his'],
 ['ExamExaEple'],
 ['     Example   2mpsen3tenceea   '],
 ['BWnXAxExxEA-xEaExaeX     Ethcele  1 '],
 ['ps'],
 ['a'],
 ['isennmpsen3tencee3tennceintbet'],
 ['ExampExaplelea'],
 ['   Exa 1 2 2\n'
  'mple\tE  Big gaps    betwe2Big gaps    between words xExxEA-xEaExae   in thceeen words   o in '
  'thce          xample   3'],
 ['pmp'],
 ['n           3tencehhce'],
 ['rNfUBspa'],
 ['     Epxample   2   '],
 ['wocrds'],
 [' Ex    Examplxe 2xaA-B-*_--C   mplExa'],
 ['rNfteUBspa'],
 ['Bigmpsent3tencee    in this sentence'],
 ['esen3tencempsen3tenEExceee3s-'],
 ['        mpl  Big            ExamExaple   2e'],
 ['EEEpx'],
 ['t Biig gaps    between wordshis    in thce t his'],
 ['   x xample 2'],
 ['betmeples'],
 ['th   Exa 1 2 2\nm3sBig gaps    between words    in thce'],
 ['te'],
 ['  Big            ExamExaple   2ExamExbetweenlae'],
 ['XRSIx'],
 ['BWnXAXhX'],
 ['     A-gapsB-    ExamEEpxamplemplExa'],
 ['  Big   1 2 2\nmple\tEx2ample   3 '],
 ['A-gapsB-B*_--C'],
 ['th   Big     gaps    bet ween words    in this senbtenc   A-gapsB- eExa 1 2 2\nmple\tEx  3smp'],
 ['mpsece-lExa'],
 ['tth'],
 ['  mpsent3tencee                 '],
 ['ExagmEA-gapsB-*_---Caple'],
 ['ggasen3tenp'],
 ['mmpleEsen3tenc  Big gaps    between words   o in thce          temexample  Big gaps    between '
  'words   o in thce          1'],
 ['m3sBig'],
 ['Exa 1 2 '],
 ['BWnXhceAh'],
 ['smpl   A---a-a-a---b-b-b-c-c-c----x   ece-'],
 ['XBWX'],
 ['A-B-*_-C'],
 ['  Big gaps    betwneen words   o in thce      '],
 ['  a                  '],
 ['sp'],
 ['mpsen3tenEExceees-'],
 ['EExampEle'],
 ['BWnXAXhEEpxamplX'],
 ['3tencehhce'],
 ['   A-B--*mm_--C   mExampleplExa'],
 ['     gaps-- C  msen3tenceinp thcae'],
 ['Exa 1 2 2 m psen3tencee'],
 ['lmmple'],
 ['secn3tExa 1 2 2 mpsent3tenceeencte'],
 ['Exaisennmpsen3tencee3tennceinbet1 2 '],
 ['   Exa 1 2 2\n'
  'mple\tE  Big gaps    betwe2Big gaps    between words xExxEA-xEaEhxae   in thceeen words   o in '
  'thce          xample   3'],
 ['    Examaple  2'],
 ['tben            3tencehhcebt'],
 ['betmEx    Example 2xaples'],
 ['ebBig gaps    between words     in this sen3tenceetween'],
 ['A-B-*---a-a-a---b-b-b-c-c-c---_--C'],
 ['senbtenc'],
 ['BWn i Big         XAh'],
 ['mmpleEsen3tenc'],
 ['Examplxe'],
 ['th   Exa 1 2 2\nmple\tExampale   3smp'],
 ['tthhX'],
 ['sen3tenwce'],
 ['EExEampEle'],
 ['mpsen33tenceees'],
 ['  e A-B--*mm_--C   mExampleplExa'],
 ['tthhrwords'],
 ['ebese3n   A-gap -C 3  tsExxEa'],
 ['Big gaps    between words    in this sebSentencte'],
 ['     x ExamEEpxample 2  Example 2'],
 ['Ex2ample'],
 ['betms'],
 ['  Big gaps    betweentthhcewords words   o in thce      '],
 ['smpl   A---a-a-a---b-b-b-c--c-c----x   ece-'],
 ['m    le    ple'],
 ['BWnXpAXhEEpxamplX'],
 ['mmpleEsen3tenc  Big gaps    beBWnX         Ahtween words   o in thce          temexample  Big '
  'gaps    between words   o in thce          1'],
 ['gga   A-x   sen3tencce'],
 ['pl   A-B-*_--C  Big gaps    between words    in this sen3tence- ee'],
 ['mpsen3ttenceemmpleExample  1s'],
 ['mpsecmpscellee-lExa'],
 ['plmmple'],
 ['lmmpletthhcewords'],
 ['wo  Big            EEExample  1ds'],
 ['Big gaps    between words    in s sentence'],
 ['am'],
 ['Big gaps    bet ween words    in tsentence'],
 ['epBig gap        mples in thce'],
 ['psen3tencee'],
 ['A-gapsB--**_s--C'],
 ['Big gaps    between words    iExaen this sen3tenwce'],
 ['th   Exa 1 2 2\nmmple\tExampale   3smp'],
 ['meaxaplle'],
 ['   Exa 1 2 2\n'
  'mple\tE  Big gaps    betwe2Big gapmpsen3tenEExceees-between words xExxEA-xEaExae   in thceeen '
  'words   o in thce          xample   3'],
 ['pBgig'],
 ['A-gap--**_s--C'],
 ['mmmpleExample'],
 ['mExa 1 2 2 mpl  Big            ExamExaple   2ee'],
 ['ExampleEx1'],
 ['ggasenp3tenp'],
 ['XBWXX'],
 ['betwneen'],
 ['2hcee'],
 ['BWnplX'],
 ['2xExa'],
 ['pBgiBg'],
 ['EA---a-a-a---b-b-b-c-c-c----x2 mpsent3tencee'],
 ['t Biig gaps  e  between wordshis    in thce  his'],
 ['Big  gaps    between words    in this sen3tence'],
 ['bteet'],
 ['mpsen33temmpleEmexample  Big gaps    between words   o in thce          1nceees'],
 ['BWnAXAh'],
 ['BWnXAXhEEpxampllX'],
 ['senbtence'],
 ['ampl3tencehhcele'],
 ['mfKqrpAGAlpleE1'],
 ['   A-gaps-B-*_*Bigmpsent3tencee    in this sentence--C -  '],
 ['  Bigi        '],
 ['mmpleExA-_B--*_--Cample p 1'],
 ['   Exa 1 2 2\n'
  'mple\tE  Big gaps    betwe2Big gaps    between words xEx     xEA-xEaExae   in thceeen words   o '
  'in thce          xample   3'],
 ['smpl   A---a-a-a---bisennmpsen3tencee3tenncein-b-b-c--c-c----x   ece-'],
 ['A-Bb-c-c-c---_--C'],
 ['tbsenbtencet'],
 ['Big gaps    bet weens    in this senbtenc   A-gapsBmplsExa 1 2 2 mpsen3tenEExceees- e'],
 ['Exaisennmpsen3tencee3tennceinbet1'],
 ['   xExxEA-xEaExae  Ethcele  1 '],
 ['Bmpsent3tenceetween words   '],
 ['A-Bf-*_-mfKqrpAGApleE1C'],
 ['crdsExamplxe'],
 ['betmEx    Epxample 2xaples'],
 ['A-gapsBmplsExa'],
 ['mmmp'],
 [' Big gaps    between words   Big         in '],
 ['   A-B--ExamEA-gapsB-rNfUBspa*_---Caple*_--C   mplEx'],
 ['mpsen33temmpleEe          1nceees'],
 ['senbteenc'],
 ['ExapleEx'],
 ['thisebBig'],
 ['mpl   A-C-x   '],
 ['EamExbetwe    Ethcele  1 enlae'],
 ['Exa 1 2 2 mpExample  1  Big        sen3tencee'],
 ['ebBigmp'],
 ['pBig gap   *_--C     mples    ebSbetween wo rds    in thce'],
 ['E   Ethcele  1 enlae'],
 ['mmmm'],
 ['mpsen3ttenceemmpple'],
 ['1nceees']]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-'
    b'qXpIkqi3mSvYIkn9RYzyL#`Wk)EWvXMGFK#5X_!T#o)_T$*~2Dm^U5#PVRckel7z%JI><^S`){eS<*fBWzM&Hwyg|M`FZ$N&C+|I'
    b'cyV<v;)9f7I*5^gL<w6Kl?KwlnIv`W_)&?Y^&j&63s_^W-'
    b'{K593NTte8@WW9Isw|L=eP&;R}(|0Aw>r?S#rcDzrSYn8fh{%6@C_4}!#hB;2U*6Q;a_g!OY{n;&Fr}j1f>tn*5Mw@+vD?KCR-'
    b'F7YMuIZkm&gaT^I@f$wD{H26=U#f)*NnZD`+my4eou2hIfQ40tLJ#t)cER<+gSOGtB<_%!*7)HtSdgHmvfKQPvHyr>KcC^lb^WS@'
    b'pD7I`l|H|J|Lbu<@AJdUDtX}y4yW=dScJxxnsCbeNx~k^7yZhnQ8KdtMxhdmDg;Y_gW=gcjsyLUgL@UUL056_cQl>$9$KIKdH~tz'
    b'at*)n!V*#@2AzepRw!6v&MUk61l@vIHJ3ReiBDLYl!{S6i=J2wK?1GW3E_72&?CI-IEt-yg;w{?oS(gl)|yx_ep856C1~KU1e_`Y'
    b'u6Rm^Lwe#pT*hkalfa_TXQQ<ZZY-#gi}I`9KnUul;@uNsxkMr#!UA)tHj^a@Tb*FDl5k4-m~1-'
    b'x?AE`?#j7deD0a2UHeA#t~^HUPswc~j@P>O?`$TbF&{p5gr}$05aIZ=liJBGKhIiqo_#&7RfOgAFjM4&`)Moitn>FVwZ<?IeZHuj'
    b'*kh}G?!ZT{vOAwOTa2|mHFGL=;ZUy@&t9BP<iXGLUmtVF-'
    b'2(TQ_m#$uyl*~D_1Oy{jtLbwXUy@0e$~RE@6pHD0kOT$`s5~YEbU3@8hxRFD3#)#u06v-'
    b'b_(yd=l!Ze%Fq4qbBXV$J0M{r{&Z@GFjiU59p=rQro3xhyM%OhM%PN`np)|r4IU_7xs_bI$A~rHFV|0Qa=q%ha~e1L+&k|u(drtX'
    b'@Z_%i?I*PwM=kX!wYDo?A=EsvBy-pB`<QW;@$8v5Z+g%QEJewk&wV(Gjv!%%o{eNTRAu#bcC8qIu;Vk+h`*b9T1Sr8nKLzHnXf4v'
    b'Mi1-oV&NHQBK>P)B<eY+WiJ?#TuXdnIb;9MW|wD%5>_q+F+&j194uHscJs~U-e@&Xw0V-'
    b'9Z?6fdNl)fko_v0CgZ;$ZoEgUHeY6<TJ@UO!(hy5tNGk^Ri99GDf9G?!c9eNyL9h0FPlFMtPaIr{Lfp~dbv5kcDqQoK8+(U_^Zh6'
    b'-I^Ou{)}E3Q(%5tPJq_}8?sZB-'
    b'6?e)Qw>k@^mVcm8i<`pKsYI#loI>SQ!qa#iZf|q#zo#iJ?z`03E3edAh;bJFXJ`ij(0V<`yF=32T(OpWWjzA|$k}{1g}|+Tw<~z*'
    b'oy({<zf<qP!(pcq76N@dXC?$^pV<(Lj+)jqR?VNGxHfhuwX5G}wB(cXr2JgPemv9LxEe0(Ap3Qcbzdp0wVt~2eN}|&cj4C^4pN*$'
    b'3+Q;sIH$3m&B3DAH}cw%Rm@deHzooL(XYLDb-r}O{FCCV^2g_-ssfgRz2S#)7~CLNwqu<gr?d-SpXNM0?(-'
    b'nAPe&m6%%6ine+OoB@Dz&5jkDuPR>YGa7xl_`%3K<r5{nZ%0-WY`Bbdm<)52$Oo^tQF%EfD8k<WgR*asgS+e9-'
    b'iULp;=Rll)T?GB+}v~QfC4yc`<_?>XyI34UFY7(y4k>GOHj5l5y*H!ojzL$R>%$QJq8o%DxrKP}C{k&!hWAeLLk5r#?+Vk9b>6b?'
    b'HMYz)(a1#%I%fZGx5qs=o0BS50<0pRF$g~#9@?h<Iy`!&;2if6lEgmZ09*_dw0!g@W-Z!U?2!!XlKX-R-'
    b'1a)C5M(bEYo`Z+&aUGPR0UoZ_BBr@x;W5L{URUOguN?aO^S`IzBCzmR;JmQyi@)7^l^(~FSLzo)A>cK5gN(57KDcPl=Rrxs_|7I`'
    b'7j(vG(`hZwiAd~%I^r=Z2Z>VvisZd2IyOVaOmj_<r^0i5s(Ev^<#b#ihnTg;J7z3*9|hsM6QVf7)^-)_)^qS#zywYi^AvNre;-'
    b'q>XQP@xGtS`FU3MG;kGrtF6XnE=a>Y1Ayk^@u<2LuiY^B=v{j)ds*$5}Lt=#D2ntUxH^aQ*uM~zxy1MA&(M?Rk@L|o|rG|;pX%JV'
    b'^iyYL9yHr^-#8{4^O;g&9J?l@SUvPQ)MPVCF_6aj-+p_V3UgslBEyaCke;Z`DeZ#6LE>iwVy70t&zpz0T%s{<?7-'
    b'Z)?Uf5(}p*yqZ>Bj(_7Jni8<gKoD0Y|FebkU>9<DaA^pbzS#Wu+|vmxmz8HGb}jNpHAV9aRul;;4P$vrRJ5m&K2%`fF?0>9RrBk2'
    b'j&NRRB@Wm13JKjulTb!4}LXa_4rwQ(zOw`vd#)XE(8o2AESW)c%OdtfHS<Fj{IThILy?4KAbzm{8l_TwiX+qPl~NntaYdr;8xy);'
    b'5YlIZGb%!k`*r;FYfU(=@G1Z4yd{52g)hes;S&SV4nO6YhYcErmz5y<CzFIUW|`QI-uuwQ{h4c?g_>Q(g1c*eh~JY1><@$_@37R!'
    b'=tTXKLu!V`>>qt00sRaQP9H17$qd@x+cs6j1Pdt3*Z*Hv3PTqwN6~&&F>Eo3kdZN4bP4q|CC|z&IN;eZqD?AzErGj#Q<)=F*adik'
    b'2Z1-M7vi5TMi7OE-'
    b'Y)Z^Y3i#KJ)B4w=3b501fH6DxM(CS_4wNc)5CTZ9v`%xY@WLz$5Z`r|bHi4Z3s$sPV)dz*0%~Ie4KczQ;@4c_M*x+z1ImiEYfBiQ'
    b'Z_aa32yyihx@1iUNh>OtHM)2j6@*uDJ1)9NS(u@F?Ohu5oil0W-'
    b'RJ)1NY6R`I=81Uq6K(D8&(!B}B>U>rGY{2ZPgQZ)sC@rtmZCKQ}p$){7bB2K^%P#FjofREJSa*&A;5T$W4wkTp73y=wcKMFuX&=D'
    b'^H{m*NT2@XK8F~*UrN3(EJpcMd?1P!Z*H<k??%o~zaaWWljiRIYgQwCtkdU*bXoZ@?G;F(|wcv4K0cl2C*KjNZ?PjzA-'
    b'5qadhH$L?FSwBo&&jIP1h{E)Y)eXKrob!lTlYdtmd<x$KH-VM<$8+F}o=+L@jG!_}*#ZM%cX%dH=qbI007gtu5#TNk5p#yo!F0w6'
    b'DFKoKg2Q)H;JKZ8NMJ}j;RVn_=%qQZtWdOO8McUfKLz}^I3W&YZ@;nOCO?y2Bdk#Wj}^U9B{Vx;LP|sj4{`Ecc?!Wx#68@IK+Al2'
    b'dNe{m@tYhi-Vv7p+r`mh+S1Ir2+kf>h1=T*%~C%HwoRmoM@2oKlh^1!LlLjwGd>TlwCsv|pAe&Gf&mt$DTac5!c$>;_pQ_*GD%#p'
    b'bwkewXyGTw3MP|7fFUMGDozFCr^y4O#S6$0kh?H4*b%&!&h#vx1LbFn^+Omth%bx}Y1@@6UlZd6ErMsEy7*p*P3OIlaok~uxT6QZ'
    b'pXT$ssTUT)b029b{&8WTU=G+!{s{D0bs7C+G#s;>z3s3whLU5%vwpVtsu#k*c>q^%{gXoy^R_9}MiDO#5(!2kU}RVoo^|D!fS9S5'
    b'^!pgTdf=V+yu!RVKiqbaYGRcp)=zc_TJR6ASD$djAa=Y2NHDkOyD7xx0C5nl2M+{P*jQ1nJzP(a2Ew5l=zF5RFog*K4B<vVavs39'
    b'4;KdoFQMn4#Bl>SarccokZ&B$NG{qN5F3P5@%ZR1Hh?4V+)DT%3dn5@DnsC!(v2@yTNb`l(+xD`);au%F~|NvV=+otGDzSmfW|Mj'
    b'b;P+y<$*nLnZOfBr9`8^eBq9Vrw_1<>mERs;MeFv@Y4|WxjyRAdV}O-'
    b'%y&hL7G5;?t1upg1~7(xKA2f70O0R|R75EH8$x@o@*VLb`bSQ=PY5KuJYV|p_=x>L)3^iP4?A@Lz5!IRR_DYZd?18hRN&&R<GyfQ'
    b'kg?~fljnJ`TT$Fl(1Uq{A>bm<Xj`X&l!J5dGzARa%l9$(45VV>$v`>CUgr<c#tIj~af9iw#<>{%!0=#%z~Q(T5JwDnq(8J3A2|tt'
    b'Xa_zNq=PcTS6~-7l?)gh*Tm67gaDWqKCCBTV#X$g&)vlbnh4Uz5AKY&=Ba_R;GY_vDM*9k0y;tK4=y3WjSFo5!LRcA$l{+)-'
    b'OqUv1_Nrr!}Ble>H~{&xOeUk?SzjG>;x*5aji>4ho8EP>-{bq7Y4NHh}2`iqzO9}&-'
    b'8%zs?n!^f_R255<~**yOW`<DMj61Pzp4KaH0!1VLTz~hY0VE<=}>Jo+xABAaomhLlS|*v$r!N0@Z&{gGAsIJ9oDZXawYq8HNZxm='
    b'2)CeFL2^Fbk~TAc_he|BuRNLrR~YdL;t4HTlXqd0_}8m`&=|{H@7{B7>mD1dm<#yvzw+#u9+0_x<-'
    b'YZ>R=43BNT+2W!G~wF)j?97o}}F9<~AY=MUtd<3(Mp<WQfdOqxjm#p}Fh#)`;7t<iol242t<QJ<68x0xzfwW_Yf<*8<*cU(acQzM'
    b'j6}%5s?SR^8NOeP*I0}Rgq{f#Z{fU!#ctInTNM^u9L>@EDpZIad*`TNd=Ygd@JQCJ1Vj$q{8Vm#!RF8=aEAkJFSH~)GgSeUa1GFb'
    b'YN-'
    b'&ft(Bu?0Xr7y?H{Jlwr`xEl<KHF}2Qi1+bBQAw>Q070e^2x94zK~pEU5Mh$S^E+U<(d>19XK!e&BaVBnHa^;$kDF#LwR!_FH=Z1p'
    b'-L&<~HEVQ&=shga837;KjTMCO&64Z1AwSHY8(b=zITyQfLWSdTfw)Ld<Zh|KK5v7nu4=LR&yGET|)!=pIOD8xN?Uy74pVSf_4o;&'
    b'6i*-'
    b'9&c$;hWp3u)%qQhj0D^2JsWh0rv{Q_Q0Ot5kHv3edK{X1G;a(B*zSI!9pB^5p#il(J%BHm%Yjrar#NzmLNmmq@OJog$PYH_Glk$Y'
    b'3>j?@C9aKp#>GyLb)zn8JHj`e!37KE`*|fVdp;a)R>ukT^{fSAv`Edh*FfuCj&TR+%fGd>W+<XAg6qS!J^;Oz^~`xkL%jWPXH7|u'
    b't9<Y1Fc6>uK+R!XYvfh^1vj~6-?d6#*Z(UnFb1sIf1U=$t9(4xD5e?2jWl4jHi`@2-'
    b'baM{cUUvsG(MLwtta*d{KKiLLMOA3HA*>hPfimF{O?^11Anrl&a2#kG`%9l6kz;FJb}&&b?sI@CGPtH*|1qZn)zp5O%mBG6PCENB'
    b'DO24h_gAW;WuyK9kN@z~KQvc`Qul{kkEr8-'
    b'jdmV7S@)QUi>$6a!?_0PryCQvWo30KV`?7=Q$qyfN>1)?hm30372T3RJa%L?X~{wR7NBb7#J#_p^UQNIwhbN(;6G@`XzdP_GuT8z'
    b'<%(xgdBrpWY${f1`4+HEci};+UUKrH#%!Ql`w|H5kYPFq&E}9vwhAxL;%%;{qH2=R%ILH~jZip#;B=spsw~NuJ7;q3gzSumezpVP'
    b'b6{-WPPfK_@^g0fKd&Cz{Y}{K`+K5UM0-I~C}vE~E?1#5>^F19TDtklRcR$6Wz1VEG4}Gy)z1H~m>Z(_Bb6X6pc5In@wxk-{46-'
    b'PL2}SP{50YQ2DPMi<JJFuYhlncPpO#I4X4km{@xoa!5x737+F=EuzlT*u4Hyb6dF3WI^b@&h|Q>VbPJ6|qdS11BPWpHG8c*0GDB#'
    b'T&$V9k|^!1Ob3-b6!}HlMC+P_c53kNe2|LgQ;gO1!)D+OfV!iZy7xbW>PRTsOqCa$YFS*`-Cs-jF17t4=+$ec;K~tE)#8B9}uo_@'
    b'&I%$I0Z8wI76PE=kB-0Y5trqAWax+{1s^Nz*`Z!e4^<j?!2S#LCjY5S&fgWZ?tvsKe4>|2L-'
    b'^ydXFghJ`KIau7FtQ%RFPb@qioz)R~_+>gpp3;JER$nS=iS<;UQb5gH?!C|kVMVZgjU-hyNe$zK;|jo)}~uy6yPBdyq*x>u|poi|'
    b'mT_=SZF2FQ2trIdkVe1IOiAVWI=-oe74WgYl}n@lVRKKc{C*0H{$1HaD(ZiE1LKda%@;hJlMA@M$Q3@rd?YF;;@WMI_{-'
    b'BUi4zQx|C3`S;Nz|=Bu3wS?ZH3~n*ff%BY$T1WJYRum)d|!l~02+TUg~vXyu>0n<4ek}A#ydjzfob>Bw*mg}of)VH6?$Yd*t3blz'
    b'hE>!Wxx!9<t8o!?E&g^c*9!>pc}jk5KWcr9P7CI1bSV!h7VuLPkz+HEChxMt(kl~SBdAoVT^5E@x%$D1@#y!vXmh`xC+QWo~K=0>'
    b'*@L5D>op+#{~K0hOkVaMr=QL>7YFI>3sBpn-+6QI9>D0=qXfom=Qq8KA7}?G=U6Ds0;QEu-hp$=9sX)W8GMa!sl?N8C*1Ch0X(@I'
    b'kEU9vN4fmqWmrLpxkMJmV*0mjT}rKIIalU#|~r6`U(Iu&N~<Ycv_14`EII%wZT+L*^;)j3Og%UsADcaaQaWa`kny@bB~vHm~(?%V'
    b'C=s@FDA5HAt<5X-DYBRcD(N%*@BP-GOmDSpa=|J1Ik+-'
    b'a2);~qx+?DHsB^*pgFjI0^1h8AC}Dnw2qTqJHBCXqeW`vW&8vi3PdTfpX&=do2#BOHvYCK-'
    b'w79lkvtcyGlM_)@9WKXUj@{4jLs%dGx%hcPl_YR7u-'
    b';g`;IFU@S1o40U~SXLL^VY0YVyZxX_#X3fKtv>o6j*|IKG}HM7zHjobGsIAdhF&1E6Yh?$4Q1A2G^5DM9Z9@cVW;USgC&`*kQasH'
    b'h!La0{l5pM#|ftOo917^Gmd;stS+=#%_qyYo207PIt<;yeZmXJ;mAx0E@9}-'
    b'Zn;)rtP9WD?tf37^2u?{Mcui7iu($Eg{;zyv3_81^RbpvV#GAR`?hDc1o?hOphXc_FKv?HyDe9yVTJn)b&9}Z|ndaeHm<`~Ld4A_'
    b'Y*<RDo0g-mn#kL-'
    b'<0g#N*^Lgu*<oG)9Ju^aeb3yUyv&`y55Ug8}d6JxlHHXegz&A?dWIL>Qkq2t)2^nDBv6Xvq!8&bdp;1Psp=rzm<b>=tEWkhN;plS'
    b'}B0b~VNV0iIoZ_EfBxG1WLx^0V!HirAoFjzpK2^~m!>aeIwC&mxOj0eG-'
    b'+>o!I+${W*MLAd}PQtM2Jia(QH&!4|<n6AfY{X;~m^H#BYP&2`n7r7(SBkZj_^%7#dJjZnH47m^06c+kZ%qB2Ky-'
    b'M+FrIybmJawFf@HKQf1y=tj<|+L>)kL7U?Ln^Hj`Q}Zp@TeJz)C<_njjd;{rN&jQsBFi~GUs0fi7G;Cip)O$uM;C@cvpVA%|OgM}'
    b'e&o5N|LWB*$<tiAyAKPfhk-'
    b'0_%(61GtWpkiJR#z&oPIpc<*4q$YvVxC<m{xo6oaklw<It7b8W|GlFC?BsDk`V3gHJXBloT3Uq0^A)!W!b`*69$o>eHJDBye5x<O'
    b'YD2$6gqSoky@Crdt9Z#dg3$_6$4<#WYvQk-'
    b'{8WHLLpP%$E1Li_SS^NFf!08C)$wb8_<*HeB&l^62J|Q`aDKQL*~`n)DZr7IP3rjEg8cPResy^o}mUzOF=t13S<)Fk}(@0;F?hn0'
    b'}BZ+c0MRDFCMT#3%iMrV90Qy4p&Gk!-F!ABtRYJ0S;rJH#`N>&&8%@w)%HdGp!g=<o?z!+@=^%t?*!-'
    b'o&bprC<=#!2~D%jo?<t}&|0%}<D>Ji5%}}Kyqybm21G&dF;r+Fl6s#A|LAp1{H!_Cj#zhtIgrQu`Lo5{x-'
    b'N`Shc%z%v2g~cfkVOa`+-'
    b'=Z*E1#*thEOL+%UY1CN%Iy%|9Prmhlw8)CR{S9ykIhHdqPt!JS&N7~2K0(y$*q6?hlBk=~M)QvXsph*{z-'
    b'u&~P#uM8dRFqLM_LPzy$Mh`#$qQQj1V#<m!icwk#=`Uh(xCI>5Fyv}f*xc>DFCZYliG)Nf04iz)!@_8wp^rSJLn8mhYmS-'
    b'=UkJ1@PY>hi2RG48(H3<z3BW;rh!W^=Xb|IbU+u=Fw;%RP2DDMX8>^#-'
    b'+shI*2zc59B+GSikzfdj`L^I<fe8nwE?xE1=ZgwJn#ZUXVp)eWaVEe$nAH@54ZP02fLN~r)Rr-'
    b'*CSCz6+gMKQ^Lv`h${rvXwpaJm4VVF~FZ_0x7Z%nlJ2>=#=J5xZCd2|s24Vb#os%_H5vC6P#fPuQ_)Ft(!N)kj4z$5vZy4`mg-'
    b'9(}43rnIegTm`Tx?b*7-GXuuC<MsLLWfec(aNb%9zK*s~d2#jA&qdFc1@Di%fnQXpmaFA3lLUFP1*E2<2D(kS>%U;IE-nSbmH2Oa'
    b'pPY$2z8Z-CvsPB@B4PgEC@!xmtW>0;=GJEp><->a?_D3%HQ&#dlh1R}kc!zUXy8-k~;^l|VacdF~txI~UyEZn2}W7-'
    b'$?ncgFje6f~lVI015=@4~@Fcn@^uF%ZBl@vl<jeqeDrBom<vgt|uqx{vtOII+dSSkqT4a3T259e9o;g*w(eL_Ay=;QWHgG3?eYiy'
    b'b%};EqvN1ml7dtdHIOyO=Ld*E*DZ1AsB%1v%jY8b390!R8o&w^m?73~wYMqLnzhj&Sb0@4t)?cnr!MAfO0K>Bc#D8S``ecaKMyiV'
    b'p&X<9EjZsn;5dbrAK-!Hf$63hW$~8S-'
    b'+)q*giw{lRhVZR`Y)xoR`f&&^}aEj1}{o7Cf1)p0>YtlqH985?z(bSOrzwkd9_Rd6goBJk5=rWdI+HFd3A()z-'
    b'Or~oh?c!1}`Ktf<~vW2^9^Xk^cYj=T8Ggq+p#1B<a$6UPItmzB9V9Of9s1L!EUq~pbh!X(5=8R8{7QGg{hq-'
    b'5Cu+TGWf%;{Y@n58kOTno@b*93cAsGo7^v5{e(L7Da%e}FUX29bmMi4Jw1rYW#6px85^cXN*-'
    b'rR}B$9%wzAH~t+hDxA!)#xz7lW((Fn8#L62dh4RSr6kMs^Z2Xv<iSn&~YOjPhLD94g^lc(eb1W$O7;{pvHNL$#>!0-'
    b'(^Xsl(wS4mf7^(<FyhV`<0G?O9G^3b2sZUN5{(zjx2qZ3+>$e%Jt;KTg5p#P88mJplW~=o_pcokvj``th+k6E?|o_C{O;Y_lsZ%%'
    b'v%w?6?|FeN{U6dc-qJ0d9mKLY{>e$_-'
    b'T}egSl|~5zPJJo1A;T&)9Jx6&PQDwArBe=BV~H2Z$DHf|0}=9RO8J2{>T?#F;DqRduYvqvP6nRcjB2)n0t`xWnMj9s}=I24SJI^@'
    b'C+(>(ene590K5Fh?(dH3!sGOEGzv_?jGq51?mMzz}fa=Abelre46ZK*9xvx%Za>gda>J$*4Xy<wA#fi#CrH&7}nR^5uc<8_a?0%@'
    b'a3~-<}2QBY!#t+$ehi0Wl_M1BZVVjv61ZF;eFN+ArKUiunL2xNqJId-woA_=^2+4j;lPU|3+;-'
    b'Vl0ZecFF;0lG0bI2Q!rfZnj>T49O){a9u4tYXQ{&-q&9W|NBNGCKlN0fNm>KZC0R-'
    b'd^T{ad5)10J4BXK9CM5YhCF}b1i7uMqsRx;kQ7Bh+;$v@U*8J^T8l*SXJN6n3?4I4KQ#1@L!_Wk<$eC@}R)pX4$vi)6~*G%{cK*s'
    b'lx4(sbNqOXdRcl8wMkNQjEm(eIpQs59^?4h$+^lKv*oFT+M2(r%KqZyL+rNJ7z~V$l+&1doWndFO|qIrP{5{!XB93Hq3902O1tNB'
    b'7g|Q=Pjc~7~UfBFDiiAgg7)P8DI$i<wTcd+hR^mf`d60D2Z2iC4JP6@WF|=V-'
    b'9|3OVA5&U%`foWc&(KH!jY(nG(J9>aQuk1+vHyi1{+g3-iPw{&nTpeE{e6g3&0vLXoKf2P_|tx1B1`HZ1XZJ3)Fh@Pe(K{MMHbM-'
    b'~cKGM_nZGI`qKdNMo;1DJs^DA$H{S|S@jb%3X1ezCy!Q@i6&rvRwdlcGeAMO70rm2ZwlCnUArAifv@>A;99KX8tF#KpJf8~XVb&Y'
    b'<yzAgu+8(9jVF1|YuF2{Th|D0+;-acVeYz|Y(7P_)ORa-_ePLQDan+X_{@>lne5JidP+{CLlf11_sUx?bpxVB~DcdhK|g{53uyV+'
    b'pJgL1wm3V8Mcc2>c{0%<T0B?N+c>GSg~pLW7GRzOwR-F@DLDYgHSZGTijJOnKe#_<QYzwOeCA-z{W6Xnel#qwyJU(4s7(-'
    b'ro`Pz}$cA6)P79@(wM;X6`3ipqtA?%<*AdL%AZ7ydfCVLh$EUT>Hhgt~WbusjZRr7tK!Wj1@_{Vb7s{aJ`(db}9HW7C0IO7`*xTJ'
    b'cCvW^J0aH<k(8=xEiPlOPIt*)jwYkE@DY(!A3*M4>yjjeRUM~hSlDjf#vW3P(TEKX5B_!RceT<f_T{bu_0!BOu-'
    b'`aGsnor@4~V3`~c6hEbNZPuG=egZ2(y>6aTwaRG=g*q=gt(flbI!?CDEnb1PFbtJK#}@ryNVYb6qDd6^*%s6L`pfvlE|LqBnc20C'
    b'j8PyX!9DR+#+*vgz|pi{uK%Yq9`A-91P*sao_iDQBaQkihKV-'
    b'X8yG`?~S42@_NHfaA})0sU6QlHHq^IBHLg7U5X&KS{FS3kaPMCtxOTMEtc(KX+SfF_BKFcYigo1YHJLn9{;PJCUAH1W<d+Hjx_?R'
    b'%O_gf*Ae`(C#lIy~MyH!ydB^uQNZNJ2wO3+v7>7(<=_6Vxb$f3MfXY@h?2EC|91AR+x#$8ONtYvLc#^T!jzG}>o}xo<$A1AI5M_('
    b'e>RqKU^jG7a-w6Gr!BI~fosL<7S<I&KRgY!J4Jhgu`bI-((;FYuC}Pz&ie?U-'
    b'3<sZK5><z|rHEI;rNxrA6eSLB_8`LIh>KyB*R2g9u{&Jc(VLK$`tp3LPBlWwMe<H<OmZvOoMW!qb$`Q`-'
    b'wC1O(awsYv6tW@RJIh=_19k_=LW=e@S3pw!K(KJvq_-'
    b'G~P6S0k7sAD_`cd(KWH&_f~bgNG4uue2oLxHv>P8$?ZZ}_N?^A*4J*IkkMyT<~`4d7jPlV#2<*aLKo6s%T(c-'
    b'BG)KNEH>S_guazl~MRuS%Y$hW^jDWwF0iY#HjY^|wG7<OC~=_1qXza1oCS(!s>-'
    b'VOi5h%i6Bi#6ql3wK^qSw{0gF9mM~dQ+&C>Sh%;14qyAdt@|xT0f>E30h@1b`%L;U7LN&Ca>{9)3ZMybLcWph<!xvhy)J<C#w)e;'
    b'RW9gx(iR`%oVT^t_``+43@BE&!vnRv??(-'
    b'=>IM+RLEP|+(LN2wg2~x**|=dSS};EZmLCZnsF!WW{Qg*m5H0@|MDb7!sW)=;IbRMP0%iTf&b)N7G+0v$Rz!VpNC+beU7@rUr<TU'
    b'BRN|5mm#-9ejtg%Fal^$vh4TQeV^#r_$x0xJX++7b^x_bwWej+}=~>`j?=J-'
    b'i;tq4BwG$8tPTvYI2k<x9d!G*Kgm@RL?!X6Du9`ZF_UZvQzX<K*$Q~<IP)Hsi-AG^`$vh&k!}ge*&>pmcug*Lx(%OsyFFU5cNE>F'
    b'=!rTX%jwJ_;pxS}YfmTlb2otLL#^b#$yOGDis}*}%msKvmBj$y~RJi#I6a6|`KFk)FnE==V4lriEfR%tQ%qN5h&UVgwS><=c>rBH'
    b'`Z_|6RtqE|0I^#RnK4#mZ6o8kxx~&{R`(WkZXc4hb_XqZIVdB=z?@v3)!!&uAmhEjN-'
    b'd3e&LwFCI6jl$^o>wa4BwGr<j1cGn3xQbS<_xF6Nk>5@Pv9It??>^xgWeKoY%agNU9S!NbmjXCk>Nl%<vz0g`Ux-'
    b'1y;=<b&Y9WX5g_BX?<`^f8t5h2>WC@rocY(0UDh@{$=6{XZ%`194ATn>METlDI&OFZ4+)5c9z$Jm<d@Bu8CLX_I2FLI^$Qk09yn6'
    b'SU|vWLn3I3c9iqYc889esom&LurUJRpxcpv<hlK}#!1*U83Z@jFBqud|V~LWY#s~A)AU4oS2di7u!)J-'
    b'qzBVifNrS2EH+nxz%Hs|Sya9i&SDyjl=js487K-+stw8{Z+nxTIbY6hhzg{58O|B;uPAJ%u3)SC-t>caWNn-=3%)Wr28k33J-'
    b'rv*M$Q^dFt~lv~poy4(V1p!zQo>tj#O<O(Z34m#K4)}?3vArpPp77s9W%iRANyk44RXj<-GeoGpxoY=1Mmw!h3o3iz$Ksyw#R-'
    b'QOXHc`twI1~gm#&VGH!<tx7U1}QLXef7LDw8yQ9uB&jmp}^)u=A+vGR3g=NBMat3zbms9a9NM8vsAFh4K2I9QT_zr6Vv8y=4uNG2'
    b'6pK$cJlx+*r>PxPIj^d%80^I^kR!Ag-DWN&xMpLYRnD&CFud{YEZLlpI2#*aNQ>@Z4C=fIJH!2BIz^`5&YE9K@033c;Xwdnh0%C*'
    b'tG<#U_bvV>>SqEZO3m5~a3%};<I*iW{O$Hw&YlTLGXMFwP4p6`an4=n8^$q+OC>AbOn2dooWn~THwoxmA4`KJ=UgA^?<QIiRbNA+'
    b'#E)2!7_bPcX0KH|IVLL|pp9s==Oe$9Mq-LSw;?>VbJ%)og^p4i%HJBzA6n9&3l74zlrP*$R+GCdUNM4<h3fRFjziJ??*+I~z*%RF'
    b'X)}Eu}XadY3+xmn(ga*hr!E&N!Fj$)r*(uK#g<Rm6C!&l0G^nnakhN*qllOcF?eBRfQ}EXZ=sCdn91S05J3{|Tac^@b+mEt@uVQ$'
    b'yDXG~>4GKUKQ3E`fCA2nWqV-o#HoR<SP<%%WX^-'
    b'}%8mb0cVPJWAiyipkM<CHmO<5cdcij`Ji1~>o%rRacOahmOwza~TX)MV!K5KPG16F2G3m^t$UPCiYcG>G(FI>+$$ttU_UD!bt0Z)'
    b'QjZBOTMhJ-m^I~FQBIY0}5W8gK$-8R-^vyPDAkIu_@upKCmIUitg7+Bux)_3E<Dohb@wR-'
    b'`kSB)vG1we)*p{DWc562xIGy6lhWv!I`jl~#1^-mgJ&^D$OEh-'
    b'0JTp~ygsp5moy8WK!ExvW~O5*3O)VX_%?_>*DceNANkTq%qVMY$YDk_=rE7-^vl-g@!(E(ihc1i-'
    b'cIoN_4?eQ}$hCjf+VfKsF%LVsoqIJy_9{}$BsV1fhw+lN)MDW|&>Y&HOZ3EW4MU?N8HDtdiEy6NT<^wfHo4*)E0fWFA>eK^Fd;&x'
    b'st6<{@>=Qq0KVP*XeB;q=Z`qOatvHPb>hs+cG658M47)q4=copD_CqWYXWJ;=H2eZ&^YXVdF`!s^<4yNpz29xON_>z0m`2qM)-'
    b'a6pR?Dd`dr;zmrd_x=5E*XT3O6(e7XFoR!}O5_$en!mHl+wsdrX32_7fJuntmfM_+iZ{O0jJfw~_R|J`Kk>@aqpo7($*vw&H>U|G'
    b'D<n8x|E^;IFY{GudqPm|C)0(_ZPnr~ruKpsmT`^|zhXNiXoEWBn`awL|eXp0wK(8LYI#1tFy%zy*H!%D;Gj>_WjmSmmAG=>ypcC7'
    b'coF{#g#B!5W$jxAqnvYEz6Odid`TrGqu5NyrC>P}(qXh2L7&1#iDLZ*#wCUO9F^LZ7-oZc$YFm@ocXVmXUzZc}3DZE5fD7Q-'
    b'c`nDKq4UJbeA#(@kK`(;MB5_IgV6}axp+V8hb^H@lUtZ;F|)=#j7B`jT7!?&*l6)?UJIIb~5C)Wq|@fI`UkR~T{)_sB&;I>1>&TJ'
    b'4;Nn_neO<(!KU0w#>EfP@t=KAss7LBD~1y!<K;BuslU9$nMTWeZ;ClJs1AH6>gSh73_R0X7iVEjdBXI}w=_#EyzSmy=$T6?@%9Am'
    b'$H^Ncmx+G>>aL1m*XHx%RN->4Yy0f=~+NW7dzg9*jV9-'
    b'9_S=YbPsye4}TE+{8v*i;S2$HV<T29AssJD4quK8(u<Bo8!9YY)Wu=J2r$wn13gYR^1;dQ6K+x%96%1YeKFnFK00HY6=ft5LE5b%'
    b'7TrdJpcwS)^Mxe1qd7U-eWI{a-KZHXhJHpzH0nvAkp&qiXgk0phuy`>pr7G5FDP2y^_x&NRND)XTG?`7MK^+fJgi_p-yN+D}^{Xy'
    b'yb8Rug!MQ>Y!w94+Bdq5tUojemt2S|*veRqi@rZHAO)>1jdE&Lueoa)v(iBHj*;6e?ez?*o;;-ryjD3H-'
    b'zq;iWk9`Szr|$Elog<>|lxU*H?JLwB4>7Cr)PZ!0f(8JYxU4>e&GTlur``hdOC7J)_=VC4elShnBAobCDG^>U2PTLTnsJjl~4LS+'
    b'pTZ*&`!#2!iZ(6NC7+pTYFH~PA*s`z4}_uG-'
    b'Y(enpxvJwvJzL$j=9Efhkg26msu#PBb7A~~M0`YFp`|I=NCmQY@2MFP^$e=ckr#oL{TiWs1qfqw(06qH+VgqsvKyje)V|OMmfV1Y'
    b')HB_Jp6dGl>^o7r9c2Y%7rpV6i)y8We9|-sj=K1<Hi+y*;VF7U8k_~lW;G8GnBp-{FC;VaT+p2OQSM(=1X*dCx<r@Z-'
    b'?a=0Br{y=cQ$N+pJ!1>284iz9PK>5W)LPC1g+XDE0Bpz?X+wp%M#1GB`y3Hdol>uGsABze8P#zS>)^{RA$_Do)v;WB5>)zw*9{;Y'
    b'jKRl%yG>&Z^Fyg~eCJsMHvnwH4u|egs>}Hl;H}GvdMMi0q~W}h@L)|~3j#7O{Xx<e`umP(;P}BN;OUY#UukXZ>C=u#YoNb5ZOuOE'
    b'=!h97S8)V-%<~vXu+R{SZcD>-p2rz!6qI}_9v=Gs3TJR6GK~VDHsG(A1#~7h00cHF+s1V}wIn*j=#9MS@4=N$b_-vc>z%4GWeN+?'
    b'vv1geXm<KK>;UyJ>e!bP7Z7Viv_W9-'
    b'$o<JHd`47gSJ1VFna<5p$v2H}?=}~TAa3l)K44_$(IpGF_)F*PU5?88XxW(+h22)f*&KdZHqp18<`&K#pb>t@82+^k7zg-'
    b'&y`=@qGWoCm=HD|y@vZW?L5|LOdiWd1T*1Ur@d>dQ(*XTt6oVgwI^K^par_|ukz4(q2GK=1U@TGLMw9w>#NK$vrHzU+zGbJ$E{_M'
    b'S-xn%4S2FznJq_{<1me0UCJ#_ttU0wzJ1eyf4hB6q#!5h|2n-'
    b'Gs`w<@8BA()l7hjmOx0O5M5GykGyd^=mgDC=Pb)9NR0S6WwRtP{1NDYQIG%oaf?ZRPAjOrM{Zunzw=dj+dyb==)DDu+D{?cRsC~('
    b'L&(u+7Ocl@2rezALh9!uaMrQ0rLE?snQ8WdO$YU^N#e@F~y3%qLSxU=WxXK%Ptur)6oG0|q6^V@obOyYUEqf)j-'
    b'b3M((Bi$k4RM%VX7oKk*zytNx-s8ri-9HsuZn1kSwy?Yn;c!|01Q1~-'
    b'PI;&HEjucw<=;OC)9v0KPPc6Nu64gtLvUQh@=((_W;(0GPzDG68k2?|UKQwfeRW&>G9JfBVL=Xgax6_X%z(jhq!P$)8N6t>NraG>'
    b'6_|E{nnGCL*>H2Y-'
    b'E&#@GH2@uEPiO&m>zZdJvt^pOOdfS5TXYpXKLqdov(jmyQ=Mwmo&58kKyLBs=NT$1h>IhIj0Qn?jzuSEwwKlG`=|1uj1v3-'
    b'SY4JR<dP~5zfO5P;rFNWgub6FuWkMCCC99b0?=gWdPt8u<Onb0uPA#_J*05gUJ@6q;05TAmNydyxzjv^vEG`n%huX{K|MNLRa>xj'
    b'SELzFrJB57%(`~`3|v*nq{~(=q>=cEkl!M=JJ94rQxW<2&;|0wwa(f)vi+~*j#Y%2;gq{avH#a3WJmEYK8<l(ev{R#k%YVCk>pnQ'
    b'k++OGGs@ijSJ4Ev&?%*?ol&<%N3VJ8@3gdzqC4+z!hQ9Lu>c7ZBoY+-_<PCJN5LzirMqbV`p%8nHHd2`l)aH5-'
    b'`{?O%|x_i1OQ%l)-4gfWepZdOQu%Yps=e%p-'
    b'LL%4}$rRhYjJ8Ac9L#`)X10<uSijBdjGU*k0l@TK}(r$5MF)#Mt}>AhKIlm6&D0tU0jdiSQ&H?s<WIlUT!DjZh2Q*#7ZZTRJ6(gK'
    b't}MBLBsY@C2*E)fL$L^IkibPW3fY8#NRM?U5lDJNcD1_Fmows=!6@e6fizURHF#mSnfv2U;#tivW*#22bn-DuOXu-'
    b'NQp)bVgi4!Zd%1Lrycjke2hA`ap;VNzoOxJCehZW}(342!o3X%-yeW4d4U7qGi-OB`aYmaf+YqOm9BEvr_r--'
    b'$<;2{UUZF{1D(GeHgIbQEFuBD9bsUg(+zr7RVMqM?560hTsr4!sJ8(^w9&88BKnr=@ssfc1@varS`I4x@#!_3nsGGJ&|U@Zb}t<e'
    b'{M^k+l-'
    b'p=_v=dV=pJ?^VJvQqj(zJW5ahO)9>(~VdMzv3=zjo0W13{{}cxCZOx|rnGM_H>A$D|l4O11eGCs=n9eIX`2!QQuoBqKX~V7Fso3;'
    b'93z8O`<-!ksMU1b^TtMlLJ(02Fj}TN4qq72q%37n@-'
    b'{~T}IL;s^xYuwZ)?cAsHY);cYUr&&Sx8U^jdDmhEDvVnWc^LDR~aK@Cw_+7-'
    b'yAdC>l@1KJXxNzlwgde@|Cq^M~q?wkwpxqHJX^Z+xc`+gzWe;5UPCf7wUM2&tmDE4g^}lI4s9bEGXx^Z;tYvZ-<G-*-'
    b'flbA5Nz2yIJfpTKq=+b|_zeGco8f6u3Ar1&964wpzNH4Ck|qwVGVkK3v!*CkgM*-'
    b'BnKNdHq};*MK)CYb}t#%>zLSFH{f!;xkxs&L5W7k78O^`0F5$KtU2O$k|(khF^f*h>@!uW{=_6z^h!jp6H|*a7zJvIoJ_jUH|22_'
    b'yu6_0(i%_knC|Zt2sM<#leewHv(L3a_M&5;a{!%JT^vsA^EG=U^-'
    b'E^f4b!JKRq+(w1(Y!lH$0uQRnTzU+m82I)F=P;8#%o3}=L*a5!tnUgP1629+z>I&4MJ{k*NVGDX{rnhojCY(?&uzBz5d#%b_)x=n'
    b'In+h;Lxne)^xzT<59dT?a2eFiWJN_2XnM6P`mc5kc829q}w8g$XC!`QIz;XrkH?hWfSO%JF=LAY!?`k-'
    b'A73anpVGa>bkd%JEtrnTs)B$3G57Y5cUjs+EbJ3r>K4p#IOuYd$0{NMcI(wx(Efn5P~SB|!NR1gohhUtFEYdtprh4Zy@z!8Ct<Nz'
    b'3PdSB_khi8q6Q*esY3NKaZL~E$?`<-'
    b'ZWa_|uh;SLa2=SKs?`a6H^YcqG~6Q15qX{a{N5{nM5afB!u#ZiE$fj{W0j@3G>RvcDY@iia2!&GA<I;uZSI$2(T6Ntf?AKbKHcbW'
    b'*SGbGMw+iHcGXgCXtkiLZEZFLyb<K_@8LrqS71><dJGF1mf3ShC$ePv6cIid#SwKlQzPp2R%13NO_z^5rc3#I148$595QLQ}(ZQy'
    b'l}iKU|eugH^4Bk$o$5J)fY;6Rm$h01uc^jOlIDsTxvK1^vNExBE`;RE<iw3`D)f|vjJ6o-<t6KX=fF4V`VH$_rr&=u4-'
    b'olFV^uK;D7dzi-c({owJ7`|-'
    b'T#cSY(%;KH~2tYPaYbP%h{~sWGsR_e|&o_zNox|anB+EO$r};NU_6tt=76JFH2LsAmbTYv}py!rWajqiT@|yn6t7eNVj2N^hl)ny'
    b'1j00{81L<VK&g(2t4DWM^)>lNwEM3DpECZ3j%nqD7n;M4yUw=b=+PU&2=!|yH!i%;O-'
    b'rk}d5OXpEdl_Sh8Ix{N7rYPmhQ9W1s!9Wv-'
    b'M0m3*gzX3O{PJsENg<p2NUtdfD`aD#c%^e%f8MXsudDne>g}tm~_f$%UMrPzDczB`c`Ns5*V*H#>tQ1a_lJ4wE$Mi^DogPv$O{B&'
    b'89uww*R+1B^fi+A7LIWKegf=wTswVklcp6zB3)aiF(~pmR%(t=BDzx-'
    b'Z4iI_Fy9`{=j;CtF*Sm=Nv|JoO+nECglrtRQq5w+on)BqMF3x*2)$D3bJULCjeb7o+_4z)r{?~PSma^eQgowBshS-'
    b'x6R4U$KoCYSSJV}a?18<CkKOC{5HEx9PbIPDh{Xq64{Ywy>K5eN2f*kdtrH@-G-'
    b'jWHo!80OwOlD#!$?p@TLn{D(%Zpi3}fr(bcCp0?6)wkQyEv7<t$WKtYA%a+;9Y`U>nI)*krrHCo;lNU!3AFkB_Z50EsR_!yjVabd'
    b'eqMEOb4@J9z{+zW!W7KrC#zVkt5V>F;v0lU?3=5757?+(>QW0QCznuD&vC>kCJ8vtVJknV5xVNO=d*vcER2^=n-'
    b')?A=ki4B8wUXml*s~y<~e!J4!rfQYrSGSc{G5uvU+Dg-Fz0-'
    b'g>0;iT4RpW~%)E7l;$VIgN0X%ivka+VQpSw#K%6#KZE%t`7t&Zp+emL?W@dW?aa@5>JVWZ}p*&++n3Lo?}c8@obiJ5}HS@;b=cIu'
    b'7!5{NH0S7U=JIO-'
    b'4X;4=XoOr8ua<X^k+!Ufm^Suk+s^szGzLBogFm>zQk29m7H07rFu`>ONEAB^{h{U#sLajr<RgD|a~$;Or|tN?j0*(C%M*tLhrFpP'
    b'xF>drL8M2+XC;ZD`CetTJNWD%wHCLmsX)nx>B9s8_1*dE9f-sXhW9W@l~ioL@(qZg+&@JztfSkrOvjHB$Wb!-'
    b'met{{wVMT8}bJhyo)w`wGu-uULUrD!3WQxwMbYsVeYL!n}`cokA;kzBI`5|4=-J<}?h-'
    b'po4oFFopX?d*gn;5UqRY<@QySiYinvTeJ3sv#*DTS68x)`^?w9_L>vF2dA|Mn$O3lW$?oErj9tY<s~cTOZ_L@R>r$Hu^#0Az6<@w'
    b'LT&QE9q}q79{PgnS__UowM--p=`xA!T+q*Se1i+I;uJ!EE;w-'
    b'{*5K=pqa<;k}k6}90lYRd<X{y6R+Y<8h~N8>%|={oD}~*+IdGUeaRCePOV`fP3r?p+#`Ukb^@`9f4s3JG#K6B{A3<ax$M;x-'
    b'3nLzn?vgg58F;I-ph)jYBM25fK$MKC&&{95rmF&n$|z!X|RW9{WB^2t4-'
    b'oG%CNl8;3#?^D1t;7`Mhzd@1R6v9VmqofiT8pasZ8srG7#1VAc8!6!sK6oMsEGu@A=p+OoDhxw>n|5;n`T7M2(nf7$r|=~Q)?H)g'
    b'jj$n^#uJ%X+x?KT74Y~KuTpoKrmm^i-kHUjzpO}^5&ZYtdXP|r@PGcZ~lTO886ga_|Fnna&Z9gl9+S;Ft^)!A-{;a94H-%QSC1-'
    b'l*0QAV-`>TNNHRVGz^=fJ9i)`R7Yeb_4LPM`3Zt(;mii2(q|hdTmU(p+(G$1!bcKr?~bWo7}q)g6NEO!e6zf7h4D#-'
    b'up_(~3Y_Rj^3!EM!+%m|a9y8;YN?Hxa~_xrp1jV9jdU`zwA`RHgWi0CiBF72y4{N#k~45I)PglWq;v6%FGA^NiSme@4guUJ8vp@c'
    b'SoQ+jBd%hV$XU$2eR`fQsFROW;hQ)`p|rQXuRtcI5id7F<^Q0TD8)$Yt1#bU|HOc<VE9xXv7W+b|#dG5K^G@n?73eEZ}^0)vFD=#'
    b'HmlXRafo!h2I(S;8zNE(#W$s{;%lN0mEHB0J3C>mEg;f?H0E8rVICfq5dp<A&r{d#+#X*wyKSp%>8}ki~?)rRSTufCZ0c(t)qWbF'
    b'DDOQa|v`>hwpfaj~PMz{DE<zVThv@#)+Ww&|;*02X5zXXnsX16}}?u(8J_AGWJG#xIEAV%2V0>H{)>wI}O@;y0!89F8=a!7syMWX'
    b'}aRL+u?QaN#ow&-'
    b'oUtJAJ@m7RgdEPHj3Q;G1w2ZR>%WURE)I&*WoqWhCynj>IuIHpOhG=^f|02WRnK&#@}&e3hB=pF;9s;|}y)2{$zWuzS$e3VNK$iJ'
    b'#>iz3WUG5!i*Bde<EFue-t!nNzE?4%Md9=IvM)h0WRdO=BE!qjTaN8eOeEn!pvq$Y1UbW)!SPv;o-'
    b'c+BS4w+FRKhjUS;<4vMc@xZC1|X08ZO%O8Hrk+wrtYnK?JUuN8H6BJs>n!HmiK-flIs#E1nwSy3f12(X!=c}XOKa1CN%9=9O5VD1'
    b'<Tyhl@KAMTKYlvT+R-++-'
    b'@t?S&6$;;Sq+yq9v>zA%u#6X?q0S4n%&h}TT%!V!cZ$=oHHwpS>Olrue(ihp9glby?0?7X1I@vCt|>4k!6z;om}XWDPF=~;h$PwH'
    b'POm9neet`_Yb6&Tz{lLn0fr4+*7Z)ApEjc5K-b$4@1)P^cBE|luGmiYdzyeXzFmL?b+M_!jzwp~3<m=(@aD6gcHw)R_RRBu`<-'
    b'MIt!VyBo<QKV3aKt0-gfZi@(o*G9NAg2xsSbVjC!!4*q-'
    b'Dx+;<lHHWBxkbQBgMmd93F<8q3FRLJT6c<j9PvUngFuXnCubhdD^8zovS`Az?VZ({;5qsvB?WqulfA23f&HgVFtBDCMZNG1y{cf='
    b'7vv2ys*T(>5OhrS0MZrIEP{6VtZzyL<W9Bu(F*Z?HU9nA1fA?Ezzn|k}}XMkNVU?;+VLFuten1II`IYh;X762o2u8#k8XBZUSMm@'
    b'><_{Q}|T<g`5Qn<w%?63_S^~OQHP{+WQ)77x-75-'
    b'vXu??vEnU>;y(IouIx!rqXfvp2OaRAYFs!)yBto5!8<0PyUod_PHy8E(>36SyCiB>cj?3XdzR(@tnAfRDWoMmGJ4jXp(2J5Xy+7<'
    b'&G*z9mFa`-0dK}J*!6Sc|Nh-THD{A70+A5>myGh7e!x}j?SJZ8&I^Ybs^LwBa31Gh#Jwo{E;*160;*=JZ?BA_p6c01yHN-'
    b'>%v617hL{sw`XnZ4h@53FJV8Y&Vux2e2pe`T%BsoS=RgZ-Ygp6=v=t5{(*zmKUFK!eYgNBzj49pN6iO|jA=x`-'
    b'OX3FMJQWw^?y8>TLJ|1ycO@XpSANA|FzZ*bJX13~crF7j~XI>)kILN@?O5LrhyWtYQzqhfXg5aoB3pCeT)>wCbq2X1bh)P}_F__Z'
    b'TMu_)WX?cj?8ZsYy~Ca}9yHuq=;`n%}qt?rt`y)?JwVehiLxE@0b#Y)mV;L9`4`i--'
    b'#E(1bPbH3hDtq<nCa1`ZsE*u9Q?UsDscACY7sqhuN7ouaC_m^}V!c0ZgR&=XPa7x4BH26<s!QrtFvb37}r20Se&x7M+hJ}ycEV7;'
    b'q7U5X19-<ly3wnC6QIJ*V-t7+0!?hjPGudVqny~`T=lUj;n@_{1zunCO@|YlU&g8kIU5+Bd3-'
    b'dF@S%+`w({KlmwW&bE^+g4=hB%XrSRyLM^Np5(_J-'
    b'X49|ZVRXK<MXhEMfqe#43L+}{_W%{JEG$+qoV<0%uZ0gl?7Ih_7U<`_A`q}#K_MPpN;wWdJ6G9EiICg|l#ruq^O3~t~~4u<16q0Q'
    b'zFK=P6t+l`sB&Ny1nhTebSLyfs9HwU>`S~vlN_J*7emR?RCdTh0P_dR8tvcu3(Q>Rn$IA0kL3>Dv&0gKfHsS7WhPnuzX&FObIZh$'
    b'a2hY!MLTq{QCq={o7;y2Rl8qv<EW6kq6;aQ#XV{i}lp0|rME;pMF{xvw=&*m{lEjc6v7x-0mps+yvgRQ^dgw7o1t3qp-'
    b'c~^O~YJa~;tWc2O;_y>w+i>Jy`sQr`8by7=2?xu)8!SRH&xIR(7hai{Uw|KkO+81_c`SH)b)aDQ>Th(haQ;h-'
    b'4zienCRb@V32bree8e=v@bHq(WpxVrcD%e4|Et@=G}vQY2FL6ewUO`3zUvNjaF|zhc-'
    b'`WJcn3K6<0Lyr!`{w?{VFqIMHmOSa4xjP5tF;LG!yz;Lw{Eo4M&75XDv7Tb1m<|@dM}_68dw#?pQ&nwo|H|d~9)hvBpqvI=sDDZ#'
    b'2^KiW_RdRY++a>Mf@K`g{?a)<i6Tz=yxOTkYKq09SEY-'
    b'+I>|Aw7uG00P|2k%8GJ4Akz+Pf7k>X6)cFEZsKS8=Sx30+@|<O&r{E{nP?t2OPfWUw&%1;cq)l4hI9YUz6q*zsu@_g!;k??Pq;6*'
    b'ai)S2yHkU(Ot3blK5)c{u!#_gzV!cKnJ_8W_{f4#s!B@TyACw#i<1k;3;=ul*NV!#5X9*#e9G;XZZHl)vR|HNsbB3KCHB^&I`A94'
    b'ibugdS@#`aGhKezx8LBVlnKEmb~i+h9MDj($Y{E0KOTjX7kf+gTJG?fEU2h<X*9MeKTH+sJM{CF}*;h9t`2U6HtmR9Xw=y{$T?^?'
    b'(SOK;hYlZWr9$?q0GRU<dk@4+B}by+IG!=Qn=n^ei&}nuOx?XGa$a#p;g`SU4XRjrrb$@TL6G3j0~#fK)i%AD%b>PEVy)byoG8Dq'
    b'm5EY%VcW~$o%5P*huc&fqC1`f$6k&uDKwTu6}X=hYf!3vR<QX;2X<6k{!_T58s#pDwuy9sgo?5ZRKljrzTFfWf(9WPVdW|M{!stY'
    b'UPT6HLNN5hB8kV=OrNUHJU*_H$B+-'
    b'nuc3tAqcKu1?9P?XuZRMhW($|y7QL;g!o#Ihv}>d?r7UKKIk%D(z?*%c8?6Us~Ri;2;*IkopN#Eg#T6wqS@PBJmyX6#_b^`LurIL'
    b'hHM;yYbtJyxZy{bV22kN=eh*j-'
    b'(pOx9RTw}Ypn%x)i5A%RB$fN*yUdBh9pIQr@C(x<H;dIoixv9eqi5G62Zl!eYioUmY^eb=IxUD1<u<V{peB!ch9<YaTwPLPx(eSJ'
    b'nsN;Y4kmci4=+GEWBJWAcMRfJ4tvYXD3)mect9TOs=cizPXUXyl29HZU;nQe54Rvb-'
    b'<)Lk%U7YuDTvw+GeK09fu%&D_Hjz=(YGBnhO}t$ArhU0Pmei-koybUZvY~Jn$;J)mj_?W;XYJeYhCxY<>|<I;QxFb4=G;rM29;14'
    b'_!y^t6f*6^5+|k6bkl2nppYDgsCaEEeY0l_UoQHw}(Xs|h)1%bS)%x&RS?v1Y9%jsb;+AkVS?mX%ZoA6UQ(1}r8=hEqMuys##~$c'
    b'i4GfC7Wlw&@Qz|DCLE?C#zCmu0i@tsz^^L*|N-'
    b'yQ@HQ#rf5|?>l?TSy%EUr%!7{9bv*Bhw^REbw_x*`!>li9ikj9RD4V@xO^GE1*71!-'
    b'#j}mw!F*Oirl1rnZ)jB2(cr_*qzV^!gI8Xr6F($M9;p|8!Z4;4jaGc+jz@EUyl6!osAP+O5sW_eNS|MWOEKmcgff7riEq{2=9=J3'
    b'+D{iTik9tNcal%-'
    b'W?;V3<nzB=vrK_03vYu9LUpv5Jb^n$dz?CFbaHmcgMW5KR&Jrz<^33G2AB(WE+*42>%0LR=ZZvB4YVgX&NG(#5@CmcWTR5QW;Szy'
    b'ZVxKK|4*}9iLs@g=_hw-'
    b'9i?goy*Y!R`fevq40nAiJ#YW5W0g{<0;4aB3$#ivXT2N*m4`TgKAtuDg4=%W;qNjJJ+y(e9BcgwwK`VCRh)T^oAr&PCa<I-'
    b'Kqmcq9eE6-F*Mk6KtKvcsql?ZJ(HYlZ&r~-B)raHU<pMxS`G#Xkn6Fl4hF`2G<E8#~Fl=lR|$-+|W{3T69&m-7c#dpOdv-ZtsTbI'
    b'yuv=J#bR&jN{X6Y<AzPjhvtLtH;H+w_}}0s{hpSx@s(1S9J5u9jhB$+Le`KbDXeQK6@DX|1R7;)>xhWqPl~F9dFONzUtC^Pq+Z^t'
    b'G@&2&`-y--'
    b'!A!h!rzb$yA}YP0RW3oa&V7*5%m=VgY%Ca2e|HgZ?_+Fj>Yv#j?0aBmH9Uv<K59*EqDYZn)d*bSnt}3<>7B;Z(P7j`^2rj0TLM~b'
    b'bI2LNgQ@X_4SUcnwXsB<UD+tpnE$&A=dhCci~&$Y8`L09Hy|$5A&g4_|WlMdmCha96mALz3}ba2V?IB+>#u4jzp^cx3QA~b_p)^O'
    b'8u{Y>J5So<Yv0P*%tlGvpI6w+2^j-'
    b'ownLK%P=~q1FWjwG|v^kAsZG<RE#mF8=cYvvcr8_jCh8;%n8CKwBANwnW&|^UR8SDmgsL(j9p-'
    b'mm24vqz_2a*1)bOqOPm4YciWBP6oGMMz~%<uZDZD;e?A;s53{*-kI5Mp&QmYk4<-'
    b'*<t?z0){CaA6^CJjXbhYn<i@WsehbXq2d#B~v+4+yt2fG~3V{0(z&E;Y5lx{%tTf(@Cy9P1c&UXHK=biV&omd3{oHbkyutC!?&K+'
    b'E`-HgW5^;K@+w6!Y|s{?`JO}|(=;KstP+$Js{I$zIylE-y3Q1Ho{c0lj3D1N)#*}VAUu$;Wq^p7M$Z-XYFzBBHRscZM9CV)Ej!X-'
    b'cWaM#?zZm_a=TuUG9SV5To1_IoWh%pRYViqRA|7bJb{I;XMus^uN#En89-'
    b'eL{RVV;guwBYfpc)7Sg&EJ*lTeM+Fq2Rkxg<UwGF`FU+E&+e$Fyd*WZL?|>@bxpI{85+XgRR_ETAg5TmmRbdIH=2X(!X&MKRCPDI'
    b'bk<2mTuerjOaBT*1+S~ndbuV5rYdUt$%PVi;2zhxE3nA!ThbRHMR%E+1L3d&Nw#Lb->#$I~BMn%c7Kqqie3rvyT-'
    b'XumafsakG;s7v0Beov)z0xUhY_l?LG83q|aPG#$u>28GuuYGN?N*x~5Tb}%xkH!U#zMhsbu?$8BO`e)Q>x1lLp%loUd-'
    b'oQo~gMGa)*2(gZ6H72h12y~#APk7P*vnbVkMkznmIDlb9v934;SpS!T!obziP$?ei<aX_f6aten!6t3n7GH~zf-c71_DPv-BbkD!'
    b'dv0m9_I{MJORxb-'
    b'4Wlwvv0+hWAkPycDR7k`oe&jf^xN0ciHQkS$wRTna*Z*=J+v^eTstejWo0T4ASm|%!#LUA~+!Jv7G{?c)Jm!eOeDF(Pa)69pg*vk'
    b'Ov2S&4ec6+~LHPIno5o(VdY$rufVa6Nq%XMJX=1vy*ANqPWeB_xLi24yttlNpu_C?JP%k|6;#7<`WGXc6p!V`VqaN^W!fpwJ}qa@'
    b'XLo++*_Z3fV=2-'
    b'O_Chzi$ZoyF1J=6xUx;jTw#O<9|QI!J+3(Xj`%I9mWNuwon4txWGQyNw|5RpC~liFjk0qxJ+m&GhB0&2h<qROHfISAR|i;Hn)fa!'
    b'Irc<aGCQM-<6Zw{kiR!uQ1%3X9SF*IHV5n&-Q)7s=5g5FxSiW-oT_Xm-'
    b'@U!WC>`iM+TD&1cf$hscaMK>iyAaExFZ!JSKU4HHp)9K#;PW#5?52*1N{LoZKxyed{u{*poR0RT(G<_xLI*RNg&dWK@8noA)jJSI'
    b'$}ia)oacfvX)Jdd%sj3bNF?hVEyWHLy(CTD_x-jOIK{y>Fwqc)Uw&!zpP?_KO%#6^P3(2=KI+t8y_KVbgSI9+VcX!IMWQE7OF)^4'
    b'm-1k5zz3C$*bA@>6pfE)%LQV=HAsl4^vFX9Vx~!jbipzo1<c^X@C2~Hs9s4H7KcFSa<y!PY|%Td*y#-'
    b's2Ec^2G@&Ka)2v)K5iK>J`cCWvk9tk<k4WkH^CDDgMG~9zFpkhRgxp_{#j*Zr@Mpo!?wok7O$uyz<_*%Ok6hm{ChLd*EQ|CKo#y%'
    b'oC|i6Hp5NF+YqW<5^g;*1TVR5V;Fo9WMISoWt^>Pt%)`USVEQIzRiif<ldK2B}Z8RRrA4}RU2osbq)Q^UVR(pd`;Y6b9@Jg+U3YS'
    b'TXBIUb4<2_0JeJru%TR&Alp&ur;6#zw-'
    b'_@yAlCM66SmIhh}~Ku$4Ogw<~*qEji6#l+S}cngzb3RZL<6uT=Tee2syyzg0jG(cjs!{a{>#MoGnzvrrhdW0wC&Rrw>kqD{cE<$}'
    b't-J)Kx+6%AU;EBPC8t&Q3A3u6{Wo>0OX%b%aCQMjGcvga6!}Tk-'
    b'<T%{C)B)NKtA>S`miLpuWs=j7UnyFe#%v@wn^yqyv7McS@wpoV4`9gGR(+(13=bR<JdWdg$B%hx{cW4ZAcE(#y8@(4Qlh8DV;-'
    b'4?lMwI7&jhRCM^B(citt&e_e!IK`89pBlLqaLF&Zkztn6_)52HJWY@uG`*vhlSaRVo(wJcMAWsNdmvxEx!V?y6)h%xB9OZ5?uIp%'
    b'<l9?m3WF=Vh?V|J2oGd(V!aE8iD|y3US~g+|UbU`i$uPyc0s>bjj4QUj^7Qjfl*Fj$=!qBoFR$VC!$I2b^y8mK{JIzj1GF8+cyyQ'
    b'zuZ^!Ken`v(*j>Zy;#e!#QHeUvV4+Qa-'
    b'`Bx1A9EYf&>p4%rWHojd%C&q~pWe$csO@$<4%$Y~=RgouxIc>=Jz9jD}fqwu0JBqyTSvtEX)Xua_~+|~pz1Sz5W2y{wsK;iIn9sA'
    b'^B?)>p^oMega6>-'
    b'jofO<On8rtDE2g}Y7pJEWY8!1KlqKz{ye4AR5&xa?6y4x(_rlopN9^86=jqw4%$2U*kE@x0<AkF7)7_UvLHg|sGmpFY_WJex6S%h'
    b'JE(KJkN1xQ$C%L-'
    b'm5#bkoMg*OV}@Xay*mZHP#CvfF*n9n<B+pQ3|L*q+1S;87z7=K)h4IH+m1lj3ebTpxTstF~uTcX(#51zJ4aK3}Bt<7C~%*QxGhm~'
    b'*e9XIXx5Y)3dmE```%0vf3yE@NB50=VT(~Y4x-sIf}2iwRm4FUQ}1Dyj1-'
    b'@&$H70cII%QIu@o5OpNcBkXof_j^&i%!Y4J@&2G;lLaU{=AJ)9g?z~<oQFQ^Ef*Sz!32)E(LeIg5k{s>c&P?SDo3Ju-'
    b'|+w_vpmJjQdLlvOb*xc)#0Pj?0(r`wqy88B*Zh)!S_m7E+IQfx&UFd}wh5>3$2|zC^ag92GlN9BFg~d;4HwQNUs!Z4Z_yUH99#e&'
    b'4`f{M8g3ga5upgt7kF3Valg;hd2ux5VP^=2W=LaKy1Vh(DNkRy?~j(Rd8P{|ENXaXW$)Nq*1;u#0^xR&^dbx-'
    b'D&Rf}N>T%ZsuD`w_707KQv(kr~=XVz9Y<0tVKxwIazTC$X)-aVC%bwYSZ%@I<Z--fp>D`ywVAdF^h$0U$l&v8@s77_7r_29OJSFN'
    b'~}y{Im=(w(h+DcgP6d;oD}uZLvDg4ggEGoGLkcb~q`&Vf+n<pY3jIH(0o*073*$!YT4o`CB?sov0C<mk=(eOjw%@Leq|OD`p^F4a'
    b'hqhYy~aJRNp0%TJ10A>sFdK)Hf_S<hq+MA55`dEN$_=1Kg{5YHM&U1ae2G<95)(uQ&u~<W~3LJjAL!MX2|g*1VQxXRkk89d>>2V!'
    b'8|7?l|DY6?tEl6?DLJ!~JlN#=7m{x?JX*pfs1m#dCATE{Dc#4y4yn53Wda<M7u#s++nE7@DtaFWY>u61VlD1|M+*I4zYWz#W65n8'
    b'7T-'
    b'+2~rlFX^_9(bOfNH#`zceVyZ)@5n_bFWC17xDMUjb=gs=%SlxUj@Z8GUoJ7UP|$$J^MLY~!`uXIoRou8jmu;HoEmKge4CmJAQz*T'
    b'Uz*DTdUw-UuwZS$;y6$q`1mx81DHF<^@1=^{~X~<hQycsmSufY4raA*!aVi_$?;6MDih7lQi6zY7kOV&Xj_1~V+Zx!@OEpi%2%jY'
    b'yCZ3WaSOXAt(bxkwkJ4D4A$Wi)M+dDo7#jb`L4EXiaW~Zd@Tq$pmTF=PF}-'
    b'{a}q8ka+Ee~62S}Bl0Bx@r#p|Wg~XP1qdA|Sg6Jmu&USlisQ|nl&bi-'
    b')!tGWzXUW@DFx}q>(ZO_~g7^m{>aUZ30FsWe`)!*PS{xi!nCxc(sdRVHcGK!Z4uQY-'
    b'p?P5R^bTLmJ{N%+aXkSFjz=5LV%gc@*q5nYO9^ei;do*B)^IsR;%;v{R5|}Lv=EgtmIpuW8ke0wZ_7;s5W?HRz~wkZ&#|cjmDiY?'
    b'm9|0tYf&2*5+_ySS7paxwYNJ0tKTi@<9A(EX)AMe$r_r(^I7+i-z6d6hPnM_tQ_g;b^s{Sb{lPQwcl7EEKb|@&)Z25ATQ_IR)-'
    b'owh|k|lDeS3hQEU{sYO_Sbp%iF?P2O;`1|a6|-J)k?95$e-'
    b'$yWd89sic1M<?Hfx5j_J{d+cZTnp5WzV@Z*>IZs{RcOyU8m9pmxraH{N1#op5A2lN)i88cRsyAfXTezwTU<U3$jl9dy~=V<{{uth'
    b'xj35q1v7D|*V}LH;-'
    b'ctJgG0Mb3?)rBki8=|Ffbvz%2tQT4I<Q#+54N9ZYdB#fD&NQr|InLC1}o$#kh0zE~7V&`xcj3EPm3v%))A&uYGUW4uvBzzMCA}*S'
    b'G7akL#vxbB5dz=n(z2V8lrkDHve~I@wtHO`O5Pxuhwf`R<hkAa&<o@NUgYL2&)s)n~<Ebxkoutz!LfkZ8^qcoBO>^E+VjaNYzzpL'
    b'<()j>ChX71t@<PTB~-uIA#TWaaxA4ov-0Ic_?)#z6ZYpl~i4c%0n`HGgi0J)-'
    b'YeW9xm26SQ$Q(Ot&ediv%UTLiKlbF!D+XPEUnt?s<r+wGn(N_Soq9;k8?*_r<Kzd7o>A9&3VZMhq90}Tyiy#aM><+Ah7(Al<1Wq{'
    b'Hh4Tj*FFRYddTQ0i{UVI@k=NT_&Ep>;zW3gSxg6(PV)}#@DDahb;Tu{VgS$!Ux74_}>(X!{h&EkMt+Jd+g?c*@G-'
    b'W?upGx15>Zg4`i(+nRFmfiFmg|jd7UjYQ5oR6Q@;tRcd41j3dlgr32D7>p19o=fk6vyD4MO(En)AgIGVh!B8y4kU3{C0Dm@iF~Vi'
    b'}gv%g=}sYN2#+%<ER|I;;jPy>z#klUSlJ{38b#<ful#Whjv;yt!|$laEH#IcN*j|;A=DS;2r+vCOMcXXU7j?Nsq5+6O9X_#UG#}+'
    b'!U&rp4-'
    b'J7j;BoPSUGe7y!v0AsJRxG7ggI)j(Ze_i(Vig+UB)=Gz$phKkLnN&2DIcys2zGe%7zm<}AeH&K|H7@E12a9aiaF84Kbz{&0abF=C'
    b'Dqb)}2o0a5vuqN98~Ca3Qjw+3mt{dE@!ExSZHX-pSjAAjsd6L-'
    b'DiF<?{}ALQ?gQB+9g0A4vh9w>&na7giZdoAA>trH!11k>n7*o)iSjWfOD%|6axxxb6jED%HvT%>WuH}8Y`;7=Yjrw!NO0-'
    b'Nh)?F0&v`JMq0`w~l5Qs!v`2LAVcEV=|)RM&*MDZ|R=g>7&k>b+eKg3rz1{^LySuVaa0kN=o5r#5k0&arq-'
    b'&zECXIcZCKmvdNvH0I+Fq&Haw2U-6z^*`FeS?|e9fNWZqiQbN*kLW#@>UebI8E}3%YP|J-'
    b'<{w<rn*6Pmad!G`d2@%C6ws#Mz1|gHZ_m8b%>fAoB95EFo;p{@nwkVI1*3dR{6NI%#V*{ntx`@%;xyBn?{$1U$iBv7C-'
    b'!!6VT>pb)NLGx5d2<hyKcfNzh@PDC9Mp^?t%xGQyV3P&gEV1Mz_u+1rG*UfT{d#df(2(1aLY#*NH4R2y1AA?N}9S>y!Z0(jG}WPP'
    b'Vks)iueok@?jZyOIzr<W!dAX3Wd9Ge=V$acDz*;2jXTXoJoy*i)yhgtFs!2Xy_!4`(n<m1m3kkDE%8lUA1NBwwwE)g^)QbW($3KH'
    b'flQ!JYymzC<=w)>d^Kn1grJ_VPFabeP6_c5)^sPYPD;rhUAi>TJxowa#CJmM`O4Jqm-'
    b'v*fZd7dzWeli&GqD@z|;v$~&i{yU)UifJ;&D4;N1dZ#cpT@dpz;+hx`{l+Hs~l7T?HZRf|^He4AkeQ`xma-GOGi7`69?}8y(Qp05'
    b'ySL!;4L*EO<<oU6f!1^q<cPI|}g`&Z~>iP1Ty*Sw1UUNLcau{E+|6w=+-'
    b'yuH`ET@CRP}Y2sMd$B4t!)z94c6bVgsVL!HjU6&Y`U|l`C~}gst9aB#ZiEpku0PBYaqVYu~>ko-hVmYww+)p971!jNk&Y<+j;^9w'
    b'qW20Jm0FZE;B#djZM$}c8q?#9+Tgl;;VkdTKU}NhGo0h-'
    b'AGK&=0DneW^t^6+iWeD2Q)Ym^sfNol}&g))b=XqufyvO98vuP@t_Rd{KK)|X+-'
    b'=E^al&=XtMi5qBhY+r@DaSgWY)mAzN>7tigGB2HR}l%MO!u@H9lfG?~47Mq2&$mJM{-'
    b'ExMR#i2krODBq4`X%4dDES<OMw8#hbbV@4l*#cEdF8&H2EOUT?4Lk}mbhT>5xgy6q9S8Uq=j3jgC8uTc#RGPk)yQq{e>>guDQN64'
    b'l(LPYUvJ}z>uxbu7DV25X+6s|=1^IP>SLlWy^UmF@#{MjySW9m0hF@tL4*O-'
    b'EvA#k9UT=1wH4a}E!^$JjYRZ&eR~r5SA1x2K?xkiJykY|;nM2uqDLo3_v-Q$Cn>lBQj(?-uo~_8K-=qfU6Au=!4ZVx0t7W-'
    b'JMdu)Q<~0XL-55{Hl|+2@}{LHU!|0Fvi5-'
    b'EApm~{qMT^*PG>w0Ews`j_iNz|ArUKAi1LjhHm6uWUvF7?oCT0wd}O+D_2nFj8*Fnob4`~4Ivl4ZL=oJ+9T17q*d9OrRtiF%7huF'
    b'GHT*2f@L1~#BXoCba)*p#cYt6*5?<nRGSp+E4Dbr>^c8rzCMdWu9^7(VBe;S0hK@G>iI>SK4C#0xaF6GHhrqcPbIyMm6=PMrs64t'
    b'64~JrntDAYs+v?NaJmpMp9f*_!Bl<Se1-z%#0Ds#)0jfLMavWV1gYI@{t+Chy-'
    b'7#r45xm>E^5)eYD&VHX<O(s^z|Z=Ds71wbj@!i*&L6P($Tq?QQtDtv5Sb1035UM$9q&Rtz88rN-'
    b';9^$h}sM4^=Ktf8n*~xHc%q?#_d*4s04tm@^82wA2;}5Th9C`!?sG-'
    b'N#Xa~Co*7U9fTQd7qN`U!n*7}cozuqUGMa{#KUGczkJ=J#kIF<Ied7z;eLfjW|6v+T~OxbKp$SRBx^v;R~7hpkN>N+cgvO>SCTAy'
    b'6g`IisztmAayZ0mMm3=tS?>)`heiE+uFQKg!XwTxBLP)WRZ$TYlk35LmsY#hs%~9?%n0i`+zf4=`(`>^Han>q>TXg_xzhkjbs?29'
    b'IARIB;1cyTet7!H!LA0l>D_@MTH2Mk3nG{KUEFN}kWAX_ah*mlWyi(YcgvZ|xpym7b++Rxfr6rs;I5n@DOGQEH8(Zc)mm}5EqcoN'
    b'>vOUGvj~`Kg6brs5Fe$b%;UWvsp}CD4M3*fYpe2^!E)gc^&HWV6|E)+at7dP1u>c@k(ioXC{hHHtX}p4s-'
    b'EXm)}Mo%)7e*U5iAbIAYd<D0DEm85QOk|%SVfHAMzsqxG$m|yxV7Tarchw&%(5B6rAmyJb@1#6omW$pQ}AmBDqm&oN+zuQH?qjxh'
    b'cu<(s{(4(*OOaOfp!q66mr$r)AH^zAZUsflfT%RoyPam`#1Mc?B$vqc}r8G5QyB+^3!<cgkJLq=4kxn-'
    b'&UcOjoB>pasgbs>7;n{r2T?RGh9$v88BtgCaM)0_rVAyKhvKxmoVX*NmU@S-'
    b'sdRXF^UGhhhF(pG38W`Fzds{R7C}I~(6zGb>p@B(8Pyc=Q6$-'
    b'2k|&n)MyyQpWA5;;P}L36UaVLqd<7$UIz}(yz?X>Fpxs*5uQF5JZ_2lg-*K9ny4p)c8-'
    b'F*vk|E)^Yr@_e?SsHy=ke`sil3#3?FHeN>3&(INfOKIA4{j}1E>^>khFYFSsSnsuODn)e9Q0c)=+NM5+P6&V3A-'
    b'#Uz!n)f;{U&+BYB}%`${iSrd7s#Igz{Z=@=lE1kb0snGJ~#;XcfM45oRw;vrDrtPqzf0C8<VSCe_Gf)PlciPj-'
    b'36SMqFCEmV1BtH<IVJkbeE_7Vy4q%|U~c+2J%ubeL?PCDjM{ivfI&mm~etk{@ox2SrQ@7)Ng<z?OPjQC%S?{k$&9Cn8^df%Dt@#3'
    b'40Fl{bH=aYMD@ozbFjUipdj?P{vDsCosFH!9FZ_)#e!x&6vhxpV+OH$0IvwcWgR-pO1=(kj1sSDsZyPgLLd;w19Pc*na;)^BN&V('
    b'<G$8+>_eTtC2u8=ZuA0?d-<q6peERln1ymX}|(TIb$xc<B<-JiIN<uv}UNG&kL3lB%X@5ae7u<m|mc2cNiO8c-'
    b'q0$10BENr2^N00cgoRxP*d@UE4q(55c|G3s)`S0{DJ#su4|+2*1W9vpymb3yJCwq9L$k{wsq_SKR8IJRJ8<?lAe;40X2rV?&jbm6'
    b'OQ69dTZXIj?mEZCe;>59t}2m|hbXSo6r54g2i_Ky2$R)9P^Zm_Q|m1DJiy$Y8SpLGb)21FCMZW~-'
    b'i`f`<as>4URYGmy<ki{3tVvqBmbNr@a4Ufj;R0&l-'
    b'nMsHrTu(REmNJrn9Yub$Gs_}U)sc7uReSZbugN8&_R_k=VbN0YN|8HVb@(ilO+gr@_XhtxGk`>4pE!p;Xs2Q4Zv2SLjT*J1bt4Y;'
    b'unFHu!$>a2q8`d%r|KF=+$v3PAaGrTsDApz?kCIc(J2ZD?XtKs)ir9fH0`{)_-0N7>4FILO#+4|nO=uQ*0-'
    b'*LDr|1llOh55W!X8Bl6;4ucZsYxsiL>&3m99noP@XK!<6Dv1SMUA-kQ|MnjMzctu3Q`{DA&L6MK!|E#y@~YI<ORF!T^TKV~Kc;Hz'
    b'v_hlb8Bvv#_Qj*}&`GP-k%+3@D$)wv0}fV>jnemZSYF$F;6>-'
    b'fbBsUn4Hd8ChbcfBWJh{&83IeWA+1}Iu}x%>JY56P4_L$Ysuj7K%f;hOv40!jADee=l)>8i&@(b}|*;T4c;zvElhT^o=)#_cY?k4'
    b'(iQtCljV18axIxD?a5DaFVy<TAJIDh9efnc?C7xuK#SjlH~!qO<Fulk8%GwJxouEz*ee!3d_>pZYE2=`)?@iD$<VqA<lMX6(J{S0'
    b'SF@0c(XB)jQxm+JOEPJ`nr`C2&rl;F<z&J_Ge@Vb{U7aoeU=#Vf-j7OlzRmFocDyxS~}k-'
    b'7NgImQZPR6vz$bdDK!EK;J=QORwC%gMq=7?pdrvfUX9U$c4e{v6RllFi*`H!<3eP{~_~CdUr(`E-'
    b'K*>^@RzWOt}ELeTLAFhKaJM+mfk8lLt|*&w$r&3TjreAJF7LPcdMIKp0rSB*7Iu&06!E(HI$*YCZ%gU#&=|2fbuA6<A9wnRd<uiA'
    b')rpW9=D|8Kmn8jA_g^_$)On;hN&5j=j)spVnHdgBX#UI2ea@)~VkUPAq<)tmAakNPXU7oyl%HF8HmGjAaJkY!H<`)-'
    b'9dUHk`_aFCv`RsQrI3+6iFic&a_BbKuRUDSp(Vp=~}S2GDId@vG2Q7i!r*Z_fF(f*brw;8EHRm<GYxI$k_R~m?DuTH%jIkE@wnzC'
    b'SNAJr~}AWWlwwAZz#BMQVn`v!-'
    b'XemndDd(TvLwQ<pI)v=8<oY_ZyxCI5sE6%MTPtczJ5I_Ghj3;2J(_DD*Ex4MJc0%NvMjk9VRe6s}+A7**zZS@j!d-'
    b'u?B%Cv4%`(KyoNC4wu!HM83eH&^nmQk~L7kbE)b%8L`M3GK5;M}T(R<yR2rq@q1+|?7s_mHyl0q&C1_b7*pN|XcRPpX=IHR9r*yG'
    b'%D6YRKkp)@JejVv|PDQeYD9$&Eu@PoRsfES$&xvwt!WUhYv55rFJW-'
    b'6iLT+Q_f^2fSIF5j4)kN!wT)5t`ZMBPCsJ0o%LwzGY7A$=kpjK#$a-'
    b'2v&;>munNzt?gyuabX5p+I0??8+Z<|Noe$zSn;|Bvo|dpHhL0X#H#jCIX~HC1NTe_~H-'
    b'Armc&$9ztlfqyeLIDgFWziS=C>K|xPb52Yxp_))XmTA6V@rZg9KpVa*do6$Rni2eT(uDPh7U5l_~we}2v1ZqE|toMDn_G7tgr)3?'
    b'5^`gSoQ}&vYhsx>SOrn1L2-'
    b'2^cn$I@kCdw<qn2F&b@W@@8%em(zgWehSmaiZn|GX=Bt5xWuAzpKJnV@QGmR~F81jxMcvG3=0*`tl-Qo7(>>WcgnuKrDtNKwJh1%'
    b'c*m&<;lJs#bIAV#xC*>R2HTJ^1o;-'
    b'Gk@CrJ+>ZPxBl<yCXUusGa)(ZPh3j0qXYbHBwFJTDM=&#T*$3Et|2LM(1ajbqbRB5!$wB1M_6kmA~_ju94k+n?eTbR}Mr^0<B9YU'
    b'E6^thu<$x(4CH{`gu-'
    b'zo^cVmqf3#2rezDaNAEsah*|m(|2FxIkDSlBX|7W$S5I}GgSHNUM~YgKUFlp$<q}?7xFlafVhR8_#oI22WAFRhXK*V-ogN-bdW^b'
    b'dACJ{loRsJqn&s;j{V$h7xerijZZ*wAw*N<0lZ&XDfk>S5kc%7KrBKMlt>PEOFx~!^ee(NO?~=HsLXy<z^JB8Cye<K;Q(Njq+`L-'
    b'L+FhxssI{82Nxi0BTH$KRZ*AaClJV(YXT@(-gjQ8o)4=6KX>OrFH=jv3u9qe&D;EH7SB*ZsdM^*+-'
    b'xp3GnTkK#_5w5UCdyl#8a!2+P5E{vodzN);AHeMb=3H7Cj~#E9?y?_kpIW@$Lr4xRApBM<Lr-'
    b'XeAB3$jV6|yd8IV^UB~#3BSJ1q3l}gxCqx6I3ACDE3(5_$jt*E{j}qH#@&`JHh_}d9ClZI#TAh@y1Ukw5yj~>))M^RUg-BAE*6eD'
    b'LbI=7D#Hw*`bHb(_^g8-CD-W`DuL@8-'
    b'<=Tw|S;X3`q@0&NUOL6wgs>+@DK@uSD2G)~gyTD3$7`QQe(B|~IfzwxD@6fnC$hRM0VIcJY=mtM_RKn3T!i0vbh?#Fm{-b(@3Wi-'
    b'O3@gXTm82AHDt+&^8B9q>J3ebHKMt~VUYnjmMxAH<%{u-Qog=@uq@8_10BkmE7A%>0-'
    b'NtGa7c2z^y7}d<z<H(3V?%h+LyzvHk=HcSMxsYUv)YJbL;HWT!jqkF~>$}oZ}&s+bNh`8XHeV%9@nR;sUAtRu1t;0)Av4fIfQLvO'
    b'9Lu)S3FyPf<@LDi=7mBM)&$lNnVJifPmg_ZbzIwAkp{ZeQMQ&ar)u)9Cdd;@|RK6?0WHxT!U{T(^}79A2toS<qT2+Hx(FSUIYy`W'
    b'Lhjc@mN3vf&cH&plTHrAs55IYB{DG%S7;;N+H2aFTOUAD8MP>xhWyv<kA1+0g=NwPo<5%ojJ!)SY#m#ND7$<OJ%KL;`=RZD_I2L8'
    b'8Ds2~3(daA_{W8jr!2CMStc^pR45YE*L*P(fxD{Wh&urljp7mJpS&DtGkK0ZP+QICk@6r3#MjwyY|{<j+4%pf7v?sCVlCAB!(#q}'
    b'|^KfcCMi`1I0hqJXuxMjkaLfzO|-'
    b'i4)Lp0}%Ng6rbxTKs;ofaqGDIP&K5U<PlNba~W@^n(hHmFY60;xoS(wm@b+VH>@mwSF<^hzV$cGU4E~9o<}eGr4aH61>7^01G9ZC'
    b'&{=#pK#$$6qr^y*FKV2;mu?6p+sNYCIuQgusvhn9F!SiBCtj^#xk_Z&{-~e+{Iog%-'
    b'UP@`*^(xK2CPo0kO)5ACS(M^lT9l{OXInF2iM{sRv)L;(~?(Z)HX7oLdl!^9p3HPG+m<vRb4M^d&}|hStxw@5P*qS+0cBP3AeM?x'
    b'RmfVqY;eS<;oqejL6(v%Hu|ZO)2&j0wJl8-'
    b'8CZrwk7%Lw5?Agq0edcHo2i#=$6sEuVS~6bepGKPAbqPjghL3=QZ}y_pe8>J^Utt@slg6=oBbcPZ2jSn=9QxJ>u^*t-'
    b'kyiIpc4UoV0!fh!!RGk;loZUM|&GDL7^yGL?qIGm4<0m4brvfe%Ugno7BGjKj|~bO@!FVw6)NIbex{tWb<N<f}_td#Y#dl;mQHET'
    b'!siwVs}%VK*!#zpeW17g8V{VB^}uZ9lz_H-jr(kdYOytD+15dE?tZ_>hV;kl^|NW;$iPy8Rqmj<Rm1O3<n@;NCBFEajw2mP#MW8S'
    b';vje~XJjz0(FUciiot$|rcVJ0)8ZyXIclQvqG<7uD`1d#0%gEw84Yr7+1$LlOXy;Il~<RTkOa8&sTR2&HL-_B_C*itFG7=xExtvT'
    b'aAO+Lgh2nGmGHJ5!I&HD5}NTQ9_sTOU)+sjB#4RxkK+R=_RphwTiW4a*Cw6N*!9FeS0OUNtBtB8nn0xF+G5?EA%1nyIz8{X33^-'
    b'Mg)uhte7(|0gOHGnRXuVK@af)yZUVuZo{>2W1<H)$Icj{T90^xHyl3zGCq~Iw2aTO34p0NxQatc4pR{2F%aL-'
    b'8``&Dd8Xr74(;y!{otE5L?Z5qqA45t|{Iojp<k06uXGk^<zGfjREk`@vb1y^%5jqQFj!zRK8X+3F^7!6^%3>5be_PQJ-zzcC{h6)'
    b'bc(}DIk)i=@5{UKGyBJp=!3Vx=l)g4C=lPMbk?JM$XTfIALx%UOA+qW@=rOBPyoIfmPV-({}AOzkI+o0-'
    b'8Hzu8Au)@yZ8qO@Ul;q#L#lWR?r~^1^MdeP2?u_PzE>OL0-'
    b'#l{$C46b$!zl%;gXwbrk>V3G3_MZw<w@k~{ZjNFK7(kCal5ev}HyY3m{AD*rb(NX2m!=s?6)aC#LNr6HZB8BLD@J!w_!M(`Rtf@}'
    b'kKc!pR!b4PGfdBA&Q(zzJ>p1GIYzT#wlp^&Tw*ENLUp~g=Xe_CTG<2Kcs#>o37S9HOl;8R4-'
    b'Rmq%=K)#V{@v<KLf^V>DIj+#y}Gk;X7X@*2So7mfu1T^2@@$@ZVqoq=B&@fT`7i7<iYQ9MacqpSzK7kvX!;gJ$rZBEG`NCu5}f+i'
    b'ft+8PnS}il!|s=8XfQwBzxvP;^*pkK@Mo6oV4krnHQMBtw>#zT!!(l?UA`tS~YfD8Z2Da!*#k$<5NC2{JXihuZEQ=*;TuWtZ!L=O'
    b'~nM2xIn4O+L1IZp*4?eeCjoSuGIgio>E`TdR~bnDG6lCSQGhMuPt3eGhzAR*aG&zaNq+8>yl2xq$EAvYjP$LHoJeh>504;Kqjx@d'
    b'3YY`1wP8I*nzYnQ>9dqCaYs0!u9L>IXqG82tdSXb2zyz31jZs5P{N{#2P08(lP6!LW4_p(isln%5I{{qtEL?8R@1evLO-'
    b'pnY#wFq6MxI-KVJaZTgsXZV8{|IK97w(CSjL-'
    b'|D@tx?Iu)i>TwnMbN%m5pcP^3#>f0!bAlsYHxZB4u|a&(o>kv^Qt?=e?00J6i2&3{YLrIV~iBt@=pAdw$#b-'
    b'(cg1qEqJniQ>FHX?g|<<rfs1hX=Ky2q$lUA+T5is&2Cv6MXvWQ|MuK0RoN3Yg8yUt<O$z!L1ig2a48a?SZ9<*z|VCraOxogY_Whj'
    b'SrdF;x3UoLlP8}Qz^53cfNC%Q!Rraq5IQj7{j+JU?dy}&9^|6_eKuLuA-'
    b'7Ik&Eq#GpwRuQ<GJ&w>RYlA$+grAHr4g`EbZEq&I2K>Oyz5EO#8DH{#-'
    b'D~87!Vd^Azo3L5aams^=u8N4|LFzvenH>2e5H+j6)SK4S<`RpC7#(bfszq*-OXm1`CDV&_r^g&?Jf`gh9t;)+qy(!{U-'
    b'`F}CkV_WsMeL)3E5vItz>)4qeL4BaUt~mENBG`C$RXMou@G6f4a0Mo+?J_BKDE*aLln@lS#KmaH@#AIO{ii8KMA!#j`ok9G0qj&|'
    b'q6axre@|YIKMe5rQu^@1i%K{;#1QGv)pRM03)w8-'
    b'G$D#awyIFJW+<*c6bh?6!~`l^^s=SYZ!WIez(=L>)u=!_FKgEr{>PHX4SU^*G)Um8RwuPD2qS`KABWc5&sWvK!@UNXm6qJnAlu2V'
    b'y{S8tVZL3M`M7f4Ai0pzGstO6TDxKtTaW*51q0f9GnsBJ;m@r(jt7*;DG8=0?#SHR(C!H>5={guy<7_y%74rS5_(htdT(1riIZfw'
    b'hX7qh?25)uQ5pr^Ol14wJUy-'
    b'4GYOD4cv`DVpUP=>N6&IVC?AiYTvf=GgE@+}f9jGGpBrUxD2hf>?lmR5kMnYJ$ybpxKSt)xX;J1%jEoC~tnC+5b!yoZ%DqYXpmEu'
    b'4>u7a=o^8sCEiay$so!>hyWWcjnlu}6z*9jg9BDOurX+4HJ^k-'
    b'Pjmx49_3`Zn5tZ$T*;2Cq+Q`gm(1N4tV|JJ3vstzdg;xG~<?Q`mwXp5Jx(}|LisDuIHMf&smuvJvMsCWQr<3axkF5a8Q?jN%c0SV'
    b'yBk`<kdVN*L^rnKFyt}29#%*$c9#y95<zkY%{r9g!3w|gO1Z_7^`_yIQg#b(~|Ec^jHb?%|*LnlDOVE|Hm~p%FXMJm7<Cqpyck{m'
    b'Ar}=QmUM{i$SpkG!y}MejUwHLgP?9vO97p9E{%tu=X~YY?)F{wG(v=MTo87dKiYtmDc`Kw`xm4+OuO+;Jp9>oJA<=06&Q?>A?UBl'
    b'71M8ECK_LVPAgYiA_(Wdx1~LYg`HrmZK1%Dup=~Og$l6ic=aIHfwf8Dr*uK}@XwDlatLle&J#HoCEe^`}?nib#ab)ZO$o^hCd4q}'
    b'ax}!3&Rc>^wy}o4^&ZFua#x-'
    b'=mKe}bO{%xnNB~BYrf)7iYmVV<m|9G%Gtf^*x08<n@n^Xuo%VmYRA1CGiA*0Q!IBJSZTN~X$>(Jw|aDTK=m9g|VI|F)kOB<P>&t{'
    b'Ewt(uPE*mLoj4R(r-%Zns--%dtA6C_C|3kqcDP)t=FwSkZsyWH^S4E+5u8br!K|6`YtT!fGr<*e4dR;m?2O>><ziNy-FqS8gY8?8'
    b'_Nww+sx&1QL2`R*o)l%@fv(!F9r;Jp%_yus-'
    b'n<(>%HNBs1l8E0XxKD>_HsJ@z;{GUw?LQB`tmoK?qeP`U{2IYs!uX^l1>x{z>$*1q9EFWi``%vt#f7|6{3m-'
    b'c=&S|^e%L{pVFw^DJPY}sl)0uW28c!s0)UMdzW3AMyD(Ggl>ei~rZwnh~Fr`eelAzNF#TCET5v+Ct#BEogul~fKU3FUT%Ddo@go{'
    b'(xlz!0!ioh3uzgJVbhmXwhJ0m~^=G;bC1(&1GeO8!w1mz_L0F)YB%^Pk9?@>wj^tj<}S38$eGk6t<-'
    b'R`Tqc+8;?yXDK(WW#RXd?x;rj1?5rQj#zi!Pa)?I%+&|5Dsc}uqSp?C{T3O)tq-ox?I|r`u500xGzQLVvHnoFx))kSIR%9hMZ2xd'
    b'i-*pba#TH0vwl0*Bt(v`jZ?=2KcnF>e??z3_KQJHj0RM<Pb2U%(u%H(%y#zzX8VFstG#9JA!ds3sh8$fOGrXyVEM-'
    b'E6E)g{_ZsS1?9TFizhU6?988wyE*~x&9gwHrtZATUW5A^{iY@+>eB+)$hC?H+BkK&V$&k?N3gJmBLwB^3C^k;22@7vG+wCZ^7{;Z'
    b'A*lX_3MP*dCa!7#sfk+pL8T&J?H*uWKsJv)8wZFMXJhH6K2JCInt!wE;?yYOqzQ)n*_BB8Ek7J2eQGHCBCzKr>;sh^a=<~NO=-'
    b'ZHsN{<>_lt;K6jZ!R2^woZD%fpTLYw@}B6Qrk7GB`I!<3T0a?5pn6<gA#{dTg;DJDeCExJP-'
    b'<X@Tfb{=QP&+)S!>_6GAsxGX2?8gVs<0MsbJ3d|BRMYNS6x%r9+;D7oUi$sMZV_v5dN#7xRu2HolN2dT?%*N=fycQfxST>)n^~gS'
    b'u7lp;Bf7!N-'
    b'`t_;WCpQ7vPpc&7IK(CQU|QLQlb1hkIXsQZGVD;*j`|ab}PA3i?`Fisd}eA8Yz;iy89HM*cq>J1DKwVM6hkz<*v&+wij$bR|Dkdh'
    b'LySfUGkbN=&u*SgNJ<kqu)F>>fhzoDq!Gpm9=t&WvY?BxM>IbX>^o*9RTb^Udyfneq2ox-PWoKHcbdzwQ7<!r6^t5ec<PQeu}|eH'
    b'3G0!=lBJ^b*UdN6@2*SJa;#O>?KZ}&W9o}4jQSgR^U<nec{wjT$Kw%JB6tPQvNZb<ZY_GS_L%mLHi%kdkV>@FQ|)m#1%VYf8z~_S'
    b'eMD*Fz(qs)S;`Pn}?T-VIugoX`eL#hCkhVwDkqre*~^G_0Wd$HioPD@o3OP&>|!(vA&}0lxVtxQw|rku}0Z8OrKIcU-<dKd}-'
    b'XSze%XpW!-5xnb+%hCki8T1lU*w{-'
    b'B+2&(#fJ>TB@xA){%k>BxJzrm!_ZUH~_dhZqBByD57V1>{`=+%!NNJN>xZNTfQP{g;9gxWOe+=N*Wh^eVZW*Z?855YqF++d!SC7R'
    b'jZlRCmVJe-'
    b'>Z7H`#TC;+^}ZFCp)XhhUXya=D$9YqH_hPpY_Tf&7l8w?{vNY?a3;RqyFC52>$BCA>(x<;gPAo;Yi7f960hudw=?C<9(6EB~?0qo'
    b'z}OCrd?=;3o-v3&2a=A5L)Ry~S+!3{6V(W%WwpDY}jwkqwGDH$~qiU%a}A0$2!x18A2-'
    b'qD|+Y=Kuk6CulC{7UE*a^SF?EIwq})@sx1`!8mrh+ar1RBUEZur(I3q%5s&Qm|2Od+?R?Anx~v^eAcw|(|WWJ(lOWxf9D^cWQr__'
    b'S?$)W{=02MJ*6pyN=(mn29jw{sioL-UeA{1CDrPHn<)2^Ht(NZ)U0V$QRl?|)1{Mi5z-yj>LNA+D>*usRz2;>x5-'
    b'*b)S|2<Xy1k8sQWx$iN8rsB9Ho%Pp#RTR;fzfCzoh7oL0;GD;MXiW;OC2NB5*SmETmO%v3RPxLfz$KU1x_a|NN)4J!k~`)-'
    b'~VsZwvmOhq3q`L5Fzx!Li3xu-'
    b'9ecpe=S?r>1_LfeX&iI{rx>8_womM~b2<}F;Ovye1{u5}%;M{ACs+TgT(a&3pZ>Qtwi9bMWWfGFvszILp(g4~H!2M$>43Y}V)$E;'
    b'*hPULY7>G6su@l=Z50A0yHffsdkQ^t65NHn72kP`s(lIwPS&R9Kh5U71L9u4~3Q2<I6rOpL|6cIWh>Y93a-'
    b'0Nu)sS3!gJMBKoXw(lBD0SJK6Kaz7=esRpz;3}#BH625#DK}QcxA(BuE$m9h294W@a`NRxpH56ma1dk<5Jqcr_2J?E6E}5P)$~id'
    b'#6tG(uR|eaKxbMo252KTR+xI{Mc|&EldDa*GxeopvnnV%ZFEi5bH=Au>B~9n46lig6d)D@R{6OAY8hx^fYVfhdOL_V3YIOlEW6_q'
    b'(pn>I@*T|NVx?19Kym2pmcgbhWT;}_u?jk*(vYkZKt?(6I=4yRTn!c%>T36NCBzCTCi++<;hD8YW<2O1Z_vj!(4dEK;Y7|O)7Hdm'
    b'|F}V;*4HvOO3!Msqq%v0jq7xo9pYOsD;Gj;wn*99n2cX*61LWoRtyR%vF=I+1!-'
    b'|GH0#|Wa8ksOSL9H$s)HoPd6C%O~$`f$U93Kl(<|xt#q`bl&?)CMXg{P(VMDsK~}_BGxS%x<;zy!d}Odc$EYsro?g|uR_`O$qOAe'
    b'QA!g;AO3_}PM-k0|!FkTo#=gr&i%zcpKAUGaywy;T5;b${R5SRpi-'
    b'i=e505)gHV)hNQFJL|lXyxJ%NqV2Hc)cNs&k@_Ynt{bJIEDD{D1rz*@o)LQdccas#R?n`jT}E$T?FF35q;sKKH#vNdXMh#$ZIZ6G'
    b'4(ZtoicP1T#Ti6;Dg;<m=%XpPFHNc}Q^Rj<U?=$u$)c$?JBGc^y1PC7`cbG6)6ox;|OYr||XBFHV+i4@ge87%l77lFnrMv^AXHuH'
    b'q43d4>3>x9|2M2l};-{QbI+eRn`E$s?1WVI!9GN!-zaTK~^w&)e-'
    b'tLCd9qI0!w&UE$6D*bybdk*?p~YuBWLi2K$OgufEx?L~CAkU&s`o=eH&lphYsG5!X>capuHUgQP^P+zU;-'
    b'PO3)HYLeMYKIUUa4v_s0Mu;P1he-3%bI&w>zvYBM?9mO+n8H!zW^(#t*H9CqD`;MdrCi-'
    b'=Z~4+F)Pt;K`|}AiYr2zY4g@?vA3@px5<_yYc6N9sBwC(6;zgWa>k>r4uKZetZ$9s$XQ;%lMS7S#6Uw;gQpyhyxdnymxQNEMWrXy'
    b'Da+jRASu4OS~iVP0RSVYNmM?46)Cvw&}#tLohfw%^1wT9RmuEt1$c<yFCf}h0F9bHsj>KJWp>4_8$Tp#-'
    b'O3Ht$D%#CCY8FPPd{xS1xp@x=6SOeodD~la{Z;$&9)BX?cO1EgL{7Syw#a@O_}JOPdP86ohVw=4mNQT8K}Ee-gJ=KWluIO$q1b>)'
    b'JwG~JqcgI?Xj<Sd5s_@OO&IZ9(TIB=8)7<Z+6Dd+4nY*hN(~^pQI%vaY{5g9ZIE&@K2ZSre_V$f@<taZj#7X9E&g<Qqg$vQQXr}x'
    b'LPAkmydGFvL@-'
    b'XadK33sY9XUq5zrlRJO3lVju64?^A?W>Vw}>ysoza#D9LiGKTjSEbuJsy>)pvP7;O+;Q*Gk8=;q;hcfsY73QaXp&K&!=aYCR5D)J'
    b'e7%szs{JMoyC0pv*IJUBP;Ai&&930QB6}{g|naR_mkkKWzK-KR2Y1(l)*Wzpte$)W&qbidjD>}ID&l}`5>U7=CPNFWjHTJ28n;h+'
    b'uDRiDX^?05D@#qe=E`n3rdpjLXzr;eJth`S8x1fz<HZ`$&mCydFeu`vkUAsAu_5ujb`Sp0;i71~H;}O8AwIqw?@10uPdt37u{+Ea'
    b'LWX{S5fYxFHSac@>pqVeZqX@Wp^{ST9FypW7Y&$J<wI=jty^1lFD>q!c`i6_gA7F6ul*cP0y4jQ)3i!(sJ?f@KCpm(U_A*)xI^cX'
    b'Yp(-'
    b'xIl$j}LJ2)LsT&zZ@TqwUl$v}iU&iWo8Q4_hDRCoK7Gtz>94Am4vCCPxW0OmmxPyPyUzJ0JG*_102(wS?Ll}U9kFN`|QN_X3<n-'
    b'YYV${4v-*{2E$edz$n(N5f23gdJ(vR?qPYqK_gxD<o|FuzpRl4by!$f)JaSbjJ+BW#6joe&+#9z-#}n>4AsGC^1~m-'
    b'nuhhE`S21B&FP1lA*gNRjP}+8$)WLG_2HGp<<bG(IZk=q039B1IV(w8Y{@0l-'
    b'EaFcdp?4CAfoRO0XUwlC*~CszwCmoHP(9Mp04exmK=sd^2E<CbVo=FmJy>u<o5J!a6wafu~%@Z~AST|JOh&hZ?}ESweO<Z<(-'
    b'gb?ZVWXZDU<77_F;#)kHf{Rx`TGH;xtV-'
    b'^DL2rwSF)KEvOq;U9N|y)ahJc7=>}`AEPF#m_P!$dNz`NhObUoHtL))hBCJhocU%h`K2=U>Fufk7@^456z*J|;%z9;veq?oE?AJ?'
    b'Yu@4M`_RFnIqcDqX5w{2x3#RQDnEg@;eL*cG}D8Bxb#-'
    b'T_ufTLiFyWtihS>m&P;h=EFb(Yr6!LC~hR6ReY6mgrN7}_3_`U8V43$7HO8vyJ=liRe9OC|E8mQ%smU%kNk*@JOBpVdxUgCwk!xy'
    b'e!Y67ZSBfT{@$pOvGoy_d^`RD@La6zzw9BQYfI=HX499DsV4Jg;y6_&tkHOP^M)<}RRTwev~r=hnMqaOP7A^KqA|ThruUC5jzuS7'
    b'nU}(bP?M&0>jb``5c8$erN5M?I3BpJy$#=dH?hPS&<FJcSU^H1*t+9fB~w>3Vi|=B+Xu{UlotGyLXLpQ`&=J)UU7<Ih!P<H-'
    b'z4fO|6sIh!xI1BjvIf<3Qs-IE7)N>)w(RL$eT5Z3Q_a~}vW<||jJ^kY_)z)e1WgFe}|l{8#+%li5`q2BfilAKn>&A1X?RkwgRH{5'
    b'C}3GPQA{j|qH_@hwtQh%6Cc5JLTQBRm3f$rJXD6Ve<{;NL4dL7>28ifYkq`qt}PVTnCJrd2+>CkpnE&6)_+H{%ke?*feFQ!O%Ohb'
    b'FMOx}<vs+N+Za3wN0pQ)a(#h2b=K3<F)e)e~hveVM6DN&UqddvH{KzVnCG4)nfj8L-'
    b'#qW<6GCk>wuGF>&%>%g{(LYd?tZ6Z`Av{k>FgW}JnmRk*EzE`ck&6DMZ6eon={6ts2>`Kj~A@wYF#T5Bd{mKIBa!{rfqkeu5=V+Y'
    b'93!%3cDZeU}bOrgr=*^AXST`Te{ziJib=ermhriXO7ZqJURTWp6iuy17bCk&bv^~{oQmP(`Sa)Q=IzuANr_VqIax1A3)Nnt?FLb{'
    b'bs78Vx<(A9%0NdAfv;}6?cqrwe*^LP<c)TPFchw}%KEtPp3E0@Zr7)y0aMadk7f<csD-!gE-'
    b'DrxZi^7BaEy2}E4|(zW4i#4#U?D$73ow$jYib|IXH9nsLF*r&;EJ1upVH7*+BFo=vZ7K))<SZj=fxeX-HjvG^6^NNuFGnB!&iBoa'
    b'b8*{D?`ESR_;cXq0>I3Xifd~gHYu0HhII;fjoAO%oYeKpL&M22=>s(xre0)&$t{%gzjQOwB*u)f$y7c7X`LqtqUUn;ak(~Pxo)<d'
    b'rqn=89TZM@g6{{=bjP4h5n_guq%MgGwr~OEY%#L^(}Sv?as-oLWYt(QY}s|T~IGH=i~#A9Q$?3j|LD?V}b-'
    b'j_{h!8H&=K0=RDX7H%4CJf3#MkuW54BNzUt4c982xz2`0ipPNdmZ?i?^>$u3|@RI*%Ounb`CH#UEyY)s+hHhdPUxNpoxIJ=`cqn^'
    b'y1l0UBev~E3tHqlvqyr&|5le_^7f~USXiMw8<=9M>%5M+aqacB-eoYAcn#7VKgY764jYYOI0;Zu2+WQf4NC?rz-Jo37ls2&Lk7W4'
    b'$vE$(y5(9l(KRaoTH#KMi<vFQc+Dj4GLX|*VG%Y7haZ$lsTue}+-cX$yEU8OzPO-}$E-'
    b'R{urPPtBLqYe(%S&2Zg>P*;!mU~e+N8!)UDUxhg}{$gbZL-W$*9?)jXHFbYKdIyb;Dm*4vE6bdL`L=z^}1oOgByDFQA?7hBkiv-o'
    b'zkQfSrjDuA4tfaPsrjE}OpkPnU4AGf_pwP-!S<u%ui3J=8L~G?pIfVpOhlrQj&`TU=QBG=T4E`+ZYKq?gF9)5`&EtLw<cLAbe8@-'
    b'l5!tljd7Nrx+?>0Yr!)W`Ex_@5wT#g>0^DBMaSI`~^TmMv~ti72{qP+&PQ8{7&`zoS=inG0u4As`T0y#Diu9|yve4qzcCHZJ9X?A'
    b'2n_dTF}9tK#oNp(!4D=BM(Aj)r`ZGgfzx1o-'
    b'=q1|*Jg>nxN34*EM#x(s2hGAx6DeXBg4pRtn(S@JM5cfst;5ZHNpk0zL;yZ0}u*uFI~i+LvD)7?*5Zo%jfYtEB=|4|)oqY>oDhfi'
    b'Ah5`MYfl%<MAkOYYq{8%3C^Udqx+eRv?rZ|mQ{wMV-'
    b')7;svdW0R!MJ@m2oAbwQ=dsL0)Fec!S}EC2y(v;faza36I+V&gx>rh_(PTPlrO+&?=S5A;Wl-MF9Vjgq)i>7~vc@^B_~afOx+#~3'
    b'<EpL9r4-'
    b'+Lzu_%WJfH?E)d;D)Nw~6OcS*Cb80QH19gqG^lEiAdCfgQb(b%3&RMb+=^buG9{>LWWwk2Lp+X5%b`GdMue?$64d*JfDW7c#Duc{'
    b'Qik84Mkz~A12S0emVB3I68?)%fq%Kg#5IH)R(C=kpWTvpg&1W9?yKByI|>q34(zFmc=S?#s8=-'
    b'l=w24DP%7!&OL=?y?6Ng#|QC6V{)8>C7AiVVB%?r(lAjG``wDvyVb(aBOyr-ybU)!_;G@V*GH#T`wm!dD#z%8f@l!`g-'
    b'<?;;myb#p>Gk;qw%L@`yE;-+Mg@#XVz#XpHxi<+mc!56NI_BRkV7iB)D)Al;TNv=<B)?%=_<D={;9c6CivOWFTJ~2-'
    b'iHe9%Al+L$b>*?!9oXHdln?%u7eK+X`UFY2#d0bWJrs!xOg_T4xT^iBrI7mM}1$3|wHPF2j6<|YdhdwHoa>#1&T)UH{4rvcoXOAv'
    b'^S0Bz9u0uIkPR?3&aa##UfUz2B@3;F~k0xJKPQLyo0h>e|m5yCChn@j?M|k)(3xRTyY>t+PN)DuI%Ck$ZHPyR*G<;n}WeDa(knKt'
    b'sb<sJWhHrX5dc+J(Oh1xk&@hr>5<m*FnUp+Q4ECD3EXCj$W0G{DgT?b~cyaO4F3)o!SuY9np1ZnpLk@LYfIrme(fZGVxZLiRM6Jl'
    b'roI&e?E?NUBdpS*?gmi6pMBIzhG$a@k*xkwKzIP>$G^_u9646CtA=UTv$&=6S5U;6FQ*{p2uW?a=udEd796GXn?#F`QRXylGcVSy'
    b'`U~8YtQ*Xr$_&aJ?DWTQmV7T;h1%>TwFTdmS*YHy7iGH%{cIVUf{-'
    b'>|>Zo<q!`Xqu$z1pMu@6stEB^M`&<~sBF>+>mulGJbBm6IavT)(}tm31!Q;p>^am7b}FG-ofxt?#U@ll9WyPeZPAx-'
    b'ZAw9^8`0ph3gBWQ^P|XZdXg(Wb^x)sE-A_u};<5#l5mJ0m2WrQB2bu6zS6i2q#53La24j+~M=*axj~XNEKSEoe?`2>%^(X)ddr>!'
    b'bWAa1%`ZXd~b{3lUGy&E2HJBE%_4Jltnfu=%tPpYPQo;!?RYt7=<}@Q*%+PuOr+cPwH<)}gZ9Hdk&AekVAolFX0!-'
    b'~Z?T{eSlV{E@hKgU>cYPIfLs56TuezI}A8_X+i^S_^Sh@+vPxjyI)`N-'
    b'6n33wyX_C3n=qUXN8H%D$l<M@!jaH;6e4*Das*mRL>wS9YiAz;)1vlIP{M5>i}4dEIOut0!Wo-'
    b'K$6?Pt>3ia$#0=_zncUik<Y+N4%5y-'
    b'koep%cMk>E6Lk%Vu77+edzAza}~;i#)$$aQ4zSReFjw=?lqNSi8B;!kt0bRz(0ZezAK)^ZQH(qB={fzK;ll;Q<!7&9!pdXkP2~j%'
    b'<kc0XK0R5R6kMu_Z}HsMrHSIXSI-QAA!C7-9eMcBWR+z*y^>)#gvu`;JFB%{0mwF)pRS0yhCTdx$AEEOzHXMQ4H)L6t2;wj-'
    b'6FFC{4kFFHv>6Q>(Vu#o?qzdGa^^)c=nKw;qk-'
    b'*H!|k`|F6;l#IzGHfhe)3H_8=5ud%NS*7NB!zfnP$H~1@BgUPp4v4yReQc349CV8Ygv%DCaJp9*lMJP<F;@mOI^R7Yon-'
    b's059ryCAQW2<xcx4Xkdr(V0v+19X!xu5u=)l?>yR9+A2hDJD|cF1rPJcKXSiE@ZTGR?rkJ-DTiR2qYp&2cF}Ao;pgi@(S5w-'
    b'pO1wFz__?)2ur-~iJly}*EbMcIIw>)bRcD&YMfaHR3P{-'
    b's_ki$LPer5#X^qQq#e7u%@qt_H7FB#*s37F{X&)+AS1&0qD;HG*5Pschx!pX!OufEdTP;LyvH}Hh68BJ9eLAB79I5#lQR3zka=Sx'
    b'O0**_!eoC_PZU<k6Crr($+E();C^PrQhf8bw=hOQwC>x_`AVuk$E+q@k>Jkv(`pQVzkx^>VVekTzG*?=zqwnDUdRItK<z3)$nbK{'
    b')`W|h1UXHG4q`9?sf<eMT3q>jt>Be?G`r~fFr#$Z9tLE(126=q(jL)L@aI-WGdklM3qA&I0Z<}wAI^$(XNGvL##Xl$L;<VPNj`%n'
    b'N16={c*WNBiQzKpVxTS=di)ZPit#|&(VrlD8Kic`ZagsG1nrBWbHHUwT>rai{b+<~O^Qc&xx)i*tM>>jTkQ}(EfQ21hK#po^M`!Y'
    b'K(vV!XrgCq4-'
    b'g@2o6lvA$p&V9P)zvID&}F$7&76_~4M)9D8&;>#aW`s7)SN4?0L6y;j@!W^%Yl_HOWCWW(*kYgy`p}W=vBIrCO}F`8lz7wmX*W?Z'
    b'@Sw?5aZ12M*VSjZ$2@1RWC>YT|e&Vl$$CTx2;$ofE5J2Z6C2zuH|Fs-`dIu04rmNyx1kybXo5{*4-'
    b'bmE!l0>fh7f=9$6&3(KxSog4_VIQ@4NSNu)eb&KH<QoPN)IoiMB7Ca7+2%KKlo_d_L;7gx`z^ms{{K`M;-'
    b't|kF~ymEVNikx0qx`&#N(#A(sw=BEkE=S6)@6?~S>Y!2eGg9b1*q475+xyO<xEe)7Dp$>P8B`X?Q|(<HAdQ<e%Y_dbl<;akQu1X+'
    b's)ZP$h|=GR2nhOVbgxrRmhnoh-L9`WnjA{O=wJ1@Y`jG#)L}`WRBD?jE%E#q-'
    b'GMH>TezEiHNul()h>IHriMz3VH<~+mk3cMHg{S3`kaQJEDz~g6&F|H2X%viC(HZ^90F1*H(C`C^&eDlimq34thZvWbjH7J?DB35Q'
    b'0}cVt=HM3@%A8rljVwnq?#1HAt?U>sGD!skHGz-'
    b'c)ARv$?eQAyISQ0_WsJYdL*F@8EC3#1jj(S5V?w`K9_X0uni^7=3Ll5K^^S7l_)i7)|FUlc-'
    b'1Ig0d_|#x2*R~GrW13)YeV8vcJb~Ni|=D(BOE!fxz{ddQCc-!H+gFch;Fvde>}9{E-'
    b'lp+K#%#pF72^x_uI^_kcF8Zz>6E6H*ONPB{n71$gReN-l8kt@s77-'
    b'A2oGq&!D`Qgq|4kq4e)bxyqHhJ$l%*J~8aAdy`r#;wuwO8!YIdj06~)zUplX9>wTD%ZbS@=WtbR-'
    b'2LJTiy25M#}XQs;3q&M?L3DIUoR%1+kHFh07n?AE9P7BlK6Yqhv=Q*-'
    b'*3JM1@sViU4Y!=vPQOx5|7?yZ75Rw+#FCL@^3)#f0~9GPR~Br!7~<39M1)#c)X2-'
    b'N9JPWDi~s#k2hpjwAO`NNC~lS^Q1&WVTfwA2&iZxuS|X!{4nC3k>7KyDFzLAb+Y_P&Pm-9(fy2b>icN-JqN#&1AUVa<o6HR7x-'
    b'v#Z;oOpt?*3Qwq^nw+1<3kFp+ZDu~+jOA^p^<%5WJhk12_*^_ON&XIRhi66kNnw^A9*5>v+V0%qoc;?N%!BC;rO|b9x!lgBUnmJH'
    b'5da|<epl2SUORPh6&XU!?8uLo?3vv?3b!li+Lx_z(LE1};atgaj%@IRYaeEPJZZ*R|4&PR)Clq~2Tf*(M6qMZP)O<&FuoL2xbRO4'
    b's(WDdy-D&OoC|FIQM_sH-Y_N-dEg!#rxvzAFpWO)AwN*Q4cFWu%y%f$To$+}D#KA_Z8aLE3^1ew@OHt1Dy2*982T?Z<<;PzhyXIG'
    b'qf~QgrnvNN&v1?2pZv8Gb2qzs(tx^<>&u2CJmG|=)4qN%`Hxp8qj*wJ*L%%b9#v65X94f1Il|U&hc-LHs=eQNGozkULfImmLw>*&'
    b'=)s^e#s@A)PVq{vNs)4BH<fXFeAforfymIW!yOitT%9@LnQ<EhEB5@87Nz!VBKSvs>aleYr3@VsQ64bFo9SW*UjuQ#(aV`yV&RXV'
    b'O8m%|Ji8_mX01cg`(((uXLsX`VM1LANDorN=|FY)X%|<ImjWhujZW)2{xkZm_OQhpy#cKJU%k`6-c87g$Qn{%h_ag-'
    b'j>sJc4e%B4swvp&E&bs$=4^7FQwe&|gJyy3aI>)_kB{7jpi_&fQze%<M*;CMs9<_oX{65hKttbvjx#d%`x+5g5*UrB7N>tp6RjC3'
    b'cX{5{Va}90kegstDbCJNZlL@EGrvsxHKrG5bUK8jDx?1DyysfT}NAs+8&8cO0Q|bnJoP-Q@hNx>#Sr(=;c7ZDB-F-'
    b'$?s;YyvL?K%!WFLocMO!18K^GviTcUm1*c}qKf-+ia4A&fetj|>ZK=JmW?)#H~Y=p<Xd+|}P>rG<MeJf?B-'
    b'$+s9Pt6g6GVzJ?u5IqU@}-'
    b'%R;P>s?$6HxEnho)>zbp+$S*v4Don{8V1f{d>vT$sB+?H%=)>u@#tE>A|QqzNSYw~Ms6Y7OD&gPu{7GxoXlt~y=g*s0=JmvN@wF>'
    b'qo6y=>`#I0b+b-2E$0#ZD-<_ko8TUdiZs4f1e&ed>#?^_8I(qn<1mGH?EBh~AU8=a%5nRp+v$-1-'
    b'onDb~lpsFoo>8K8!J`mv7i_6_7D9kO;MdnUK#u%=v>6Ls~u>AERYCc!pWMwsHR9TsJXl?ZJr{wpjI%U=-6LikKEsl11>-{%H`9m-'
    b'pB9^OA<b|O@<<j_wOTR@Kx!#Y*|5D2tXzb#)+V#H*rf8t+PNNzd1tg)6F?ao&AX|R8i@ob1uxc07_0rs`!M2-'
    b'0G{=47HPn&jE~WUSm<E8F%L}A8x!W_3Pq_<~_M2o^<s2v)H=Fs?nm2*J=#jS(dQ^k=ks7CjF}R@EjtuX0E5fhVv8t8PQd5Fg%Rgs'
    b'T{;lX>iHLhkE(TeEVuq3kaypi`L`y(#uT;kp{%llvx_{ID@!2QVK<Z0U^EE)G_6Umcfb%|8HF{Z!k!kdyL!6pf&H>wVlt{o>y*I('
    b'*?e1IB%Z;1K+2*zi<3=}by!tE-'
    b'H;MVnV3Rq>u0IvbAe1@gxru4Osr&YN#hzRc4(=R(%KA^Y=5#}C+r!otH(#*7M}PgH@V1$u3*3^wL-'
    b'^DFee!X92t?yX;t;jnHoPLQVQR<f0!*#Hv6-'
    b'Uj!&09s379CWZrjlI7<tu&*rq%{zMx+y7mNx!bXC<{{^rNb|L@Oi5^T^KKkgy_0|WTu>e301B&r(nbS+F4H-'
    b'D4(w(D@*mSXjuhhNlWk|`7NYU`&DUH0lmg&g_aqY8`EgiytMmF*^7q6|Z~JkR1f0g3qf$tCht$H_}?DuEQ$$^dnwt8&#ZYq$^<*L'
    b'EqLIFXfsDZeqEkU=ujZr>}?F1Ft$6_+Q-mGPz)SXLiE-'
    b'!)xL`I`$=bs+66dr=SHCNs6W)keiD?==%L2oq!<dxp<dv}#E<9|7JYUbauR{mJ}a|35H%Pht'
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
    candidate = fix_spaces  # noqa: F405
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
