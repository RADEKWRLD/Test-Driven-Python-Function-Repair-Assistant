import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[''],
 ['abcdef\nghijklm'],
 ['fedcba'],
 ['eeeee'],
 ['acBAA'],
 ['EcBOO'],
 ['ybcd'],
 ['hello'],
 ['This is a Test!'],
 ['i am using python'],
 ['The quick brown fox jumps over the lazy dog.'],
 ['This sentence has vowels: aeiou'],
 ['strawberries and cream'],
 ['Programming is fun'],
 ['1234567890'],
 ['Python is awesome!'],
 ['How are you today?'],
 ['This is ai am using python Test!'],
 ['1234561207890'],
 ['1234561207890This is ai am using python Test!'],
 ['Thise sentence haaei:ou'],
 ['The quick over the This sentence has vowels: aeioulazy dog.'],
 ['1234567890This sentence has vowels: aeiou'],
 ['st1234567890m'],
 ['123456789The quick over the This sentence has vowels: aeioulazy dog.0'],
 ['Pyt hon is awesome!'],
 ['1234567890This sesntence has vowels: aeiou'],
 ['hel'],
 ['hellhelloo'],
 ['hel12344567890This sesntence has vowels: aeiou'],
 ['strawberries and creaPyt hon is awesome!m'],
 ['This is ahellhellooi am using python Test!'],
 ['This is a T1234561207890This is ai am using python Test!est!'],
 ['This sentence has vowels: a'],
 ['How are youy today?'],
 ['12345687890'],
 ['123456789The quick over the This sentence has vowels: aeioulazy dogThis is ai am using python '
  'Test!.0'],
 ['hel1234567890l'],
 ['12345629890'],
 ['This sentt!: a'],
 ['123465687890'],
 ['123456789The quicThis sentence has vowels: areiouk over t he This sentence has vowels: '
  'aeioulazy dog.0'],
 ['Pyt hon is awmesome!'],
 ['hel12344567890This sesntehellhelloonce has vowels: aeiou'],
 ['helloThis is ai am using python Test!'],
 ['i am using pyt12345687890hon'],
 ['1234Python is awesome!5629890'],
 ['Thhel12344567890This sesntehellhelloonce has vowels: aeioue quick brown fox jumps over azy '
  'dog.'],
 ['How are youyHow are you today? today?'],
 ['hel12344567890This sesntehellhelloonce has vowels: aei123465687890ou'],
 ['123445691207890'],
 ['This sent t!: a'],
 ['Thise ence haaei:ou'],
 ['This sentence has vowels: aeHow are you today?iou'],
 ['Progmming is fun'],
 ['i am usinng python'],
 ['12314561207890'],
 ['This senheltence has vowels: aeiou'],
 ['hel12344567890This sesntehellhelloonce has vowels: iou'],
 ['This is a T1234561207890This is ai am using pythomn Test!est!'],
 ['123456789The quick  the This sentence has vowels: aeioulazy dog.0'],
 ['172345678890'],
 ['The quick over the This senntence has vowels: aeioulazy dog.'],
 ['1234456912807890'],
 ['123456789The quick  sthe This sentence has vowels: aeioulazThis is a T1234561207890This is ai '
  'am using python Test!est!y dog.0'],
 ['This is a Testi!'],
 ['ProgThise ence haaei:oumming is fun1234567890This sentence has vowels: aeiou'],
 ['The quick over the This sentence has vowels: aeiouy dog.'],
 ['1234Python This is a Test!is awesome!5629890'],
 ['strawberries an12345687890d cream'],
 ['Ths sent t!: a'],
 ['Thstrawberriehs an12345687890d c a'],
 ['Thisa is a Testi!'],
 ['This is ahellhellooi am This sentence has vowels: ausing python Test!'],
 ['123140'],
 ['This is ahellst1234567890mg python Test!'],
 ['12734567890'],
 ['How are you t oday?'],
 ['123445691280789This sentence has vowels: aeHow are you today?iou0'],
 ['CX'],
 ['This senheltence has v1234568789s: aeiou'],
 ['1234656helloThis is ai am using python Test!0'],
 ['CCX'],
 ['Progmminig is fun'],
 ['121234Python This is a Test!is awesome!56298903445691207890'],
 ['123456121234Python This is a Test!is awesome!562989034456912078901207890'],
 ['Thisa This is a T1234561207890This is ai am using pythomn Test!est!is a Testi!'],
 ['1234This sentence has vowels: a561207890This is ai am using python Test!'],
 ['hel12344567890This sesntehThise sentence haaei:ouellhelloonce has vowels: waei123465687890ou'],
 ['This is ahhellhellooellhellooi am using python Test!'],
 ['This sentence has vowels: aeiouC'],
 ['1232140'],
 ['1234Python is awesome!123456789The quicThis sentence has vowels: areiouk over t he This '
  'sentence has vowels: aeioulazy dog.0'],
 ['1234562989012344569Programming is fun1207890'],
 ['123456789The quick e the This sentence has 3vowels: aeioulazy dog.0'],
 ['1236912807890'],
 ['This is ahhellhellooelThis sentt!: alhellooi am using python Test!'],
 ['This sentence has vowelss: aeHow are you today?iou'],
 ['This senThis is a Test!t t!: a'],
 ['This is ahhellhellooelThis sentt!helloThis is ai am using python Test!: alhellooi am using '
  'python Test!'],
 ['This 123445691280789This sentence has vowels: aeHow are you today?iou0ssentence has vowels: a'],
 ['i am 123140using python'],
 ['Thais sentence has vowels: aeHow are you today?iou'],
 ['This sentence has vowels: aeHowThais sentence has vowels: aeHow are you today?iou are you '
  'today?iou'],
 ['This sentence hsas vowelss: aeHow are you today?iou'],
 ['Thisa iProgThise ence haaei:oumming is fun1234567890This sentence has vowels: aeious a Testi!'],
 ['How ahelloThis is ai am using python Test!re you today?'],
 ['AEIOUaeiouq'],
 ['abcd\n\n\n\nefghijklmnopqrstuvwxyz'],
 ['Hello, how are you today?'],
 ['aaaaAAAABBBCCCdddDEEEE!'],
 ['xXyYzZ'],
 ['Hello world!'],
 ['1a2b3c4d5e6f7g8h9i10jklmnopqrstuvwxyzzzzzzz'],
 ['example@example.com'],
 ['Th!s 1s @ str!ng w!th numb3rs, punctuat!on, and var!ous caps.'],
 ['Th!s'],
 ['Th!s 1s @ str!ng w!th numb3rs, punctuat!on, and vvar!ousar!ous caps.'],
 ['1a2b3c4d5e6f7g8h9i10jklmnopqrstuvwxyzzzzzzzaaaaAAAABBBCCCdddDEEEE!'],
 ['Hello worlld!'],
 ['w!th'],
 ['AE'],
 ['AxXyYzZE'],
 ['abcd'],
 ['Acaps.xXyYzZE'],
 ['AxZXyYzZE'],
 ['the'],
 ['CaaaaAAAABBBCCCdddDEEEE!'],
 ['are'],
 ['ATh!s 1s @ str!ng w!th numb3rs, punctuat!on, and var!ous caps.xXyYzZE'],
 ['caps.'],
 ['worlld!'],
 ['Hello'],
 ['puuat!on,'],
 ['abquickcd'],
 ['The'],
 ['The quitoday?ck brown fo x jumps over the l azy dog.'],
 ['xXyYZzZ'],
 ['you'],
 ['w!twh'],
 ['aaaaAAAABBBCCCdddDaEEEE!'],
 ['AEIOUaeioiuq'],
 ['var!ous'],
 ['x'],
 ['AxZX'],
 ['vvar!ousar!ous'],
 ['1a2b3c4d5e6fz7g8h9i10jklmnopqrstuvwxyzzzzzzzaaaaAAAABBBCCCdddDEEEE!'],
 ['dog.Hello'],
 ['w!wtwh'],
 ['1a2b3c4d5e6fzAxXyYzZE7gcaps.8h9i10jklmnopqrstuvwxyzzzzzzzaaaaAAAABBBCCCdddDEEEE!'],
 ['over'],
 ['fo'],
 ['Hello worldThe!'],
 ['aaaaAAAABBBCCCfoxdddDaEEEE!'],
 ['world!'],
 ['Th!s 1s @ str!ng w!th numb3rs, punctuat!on, and vvar!ousar!ous caps.AYxXyYzZE'],
 ['doelloo'],
 ['ww!wtwh'],
 ['Hello worlAcaps.xXyYzZEhe!!'],
 ['vvar!world!ousar!ous'],
 ['vvar!ousar!aaaaAAAABBBCCCdddDaEEEE!'],
 ['oveHello worlAcaps.xXyYzZEhe!!'],
 ['numb3rs,'],
 ['1a2b3c4d5e6f7g8h9i10jklmnopqrstworldThe!zzzzzzz'],
 ['Hello worllquitoday?ck!'],
 ['how'],
 ['aAEIOUaeiouqndd'],
 ['example@example.colm'],
 ['efghijklmnopqrstuvwxyz'],
 ['Helww!wtwhlo'],
 ['doelo'],
 ['1a2b3c4d5e6fzAxXyYzZE7gcaps.8h9i10jklmnopqrstuvwxyzzzzzzzaaaquickaAAAABBBCCCdddDEEEE!'],
 ['1a2b3c4d5e6f7g8h9i10jklmnopHelww!wtwhloqrstuvwxyzzzzzzz'],
 ['anopqrstuvwxyxXyYZzZz'],
 ['Th!s 1s @ str!ng w!th numb3rs, punctuat!on, and vvar!ouusarxXyYZzZ!ous caps.AYxXyYzZE'],
 ['anazyl'],
 ['thhe'],
 ['l'],
 ['abcd\n\n\n\nefghlijklmnopqrstuvwxyz'],
 ['worllquitoday?ck!'],
 ['lAxZX'],
 ['tworlAcaps.xXyYzZEhe!!hhhe'],
 ['caps.AYxXyYzZE'],
 ['brownAEIOUaeioiuq'],
 ['anorstuvwxyxXyYZzZz'],
 ['ATh!s 1s @ strHello,!ng w!th numb3rs, punctuat!on, and var!ous caps.xXyYzZE'],
 ['caps.AEAYxXyYzZE'],
 ['exampletworlAcaps.xXyYzZEhe!!hhhe@example.colm'],
 ['Hello worhe!'],
 ['lftoSCkoD'],
 ['vvar!worcaps.AYxXyYzZEld!ousar!ous'],
 ['and'],
 ['ll'],
 ['Hello wor'],
 ['str!ng'],
 ['Hello,'],
 ['oveHello wstrHello,!ngorlAcaps.xXyYzZEhe!!'],
 ['Hello worllquy?ck!'],
 ['quick'],
 ['strHello,!ng'],
 ['@'],
 ['punctuat!on,'],
 ['sSsS'],
 ['pp'],
 ['AxXyYwzZEworllquitoday?ck!'],
 ['dog.'],
 ['aaaaAAAABBBCCCfovvar!world!ousar!ousxdddDaEEEE!'],
 ['punctuat!oHello worlld!n,'],
 ['Th!s 1s @ str!ng w!th numb3rs, punctuat!on, AxZXand vvar!ouusarxXyYZzZ!ous caps.AYxXyYzZE'],
 ['Th!s 1s @ str!ng w!th numb3rs, punctuat!on, and vvar!ousar!ous caps.AzZE'],
 ['Th!s 1s @ str!ng wt!th numb3rs, punctuat!on, and vvar!ousar!ous caps.AzZE'],
 ['CaaaaAAAABBBCCCdddDEEEEE!'],
 ['vvar!ousar!ABBBCCCdddDaEEEE!'],
 ['HTh!s 1s @ str!ng w!th numb3rs, punctuat!on, and vvar!ousar!ous caps.AYxXyYzZEello world!'],
 ['over1a2b3c4d5e6f7g8h9i10jklmnopqrstuvwxyzzzzzzz'],
 ['Th!s 1s @ stsr!ng w!th numb3rs, punctuat!on, and vvar!ousar!ous caps.AYxXyYzZEAxZXyYzZE'],
 ['doeloIZdDL'],
 ['AxZXyYzZbrownE'],
 ['Hello wd!'],
 ['1a2b3c4d5e6fz7g8h9i10jklmnopqrstuvwxyzzzzzzzaaaHello wd!aAAAABBBCCCdddDEEEE!'],
 ['lazy'],
 ['xXyYzdoeloIZdDLZ'],
 ['lftoSCkotD'],
 ['quitoday?ck'],
 ['Hello theworllquitoday?ck!'],
 ['wor'],
 ['brown'],
 ['caps.xXyYzZE'],
 ['abqabcd\n\n\n\nefghijklmnopqrstuvwxyzuickvcd'],
 ['1s'],
 ['thvvayYZzZ!ouse'],
 ['1a2b3c4d5e6fzAxXyYzZE7gcaps.8kh9i10jklmnopqrstuvwxyzzzzzzzaaaquickaAAAABBBCCCdddDEEEE!'],
 ['ATh!s 1s @ straHello,!ng w!th numb3rs, punctuat!on, and var!ous caps.xXyYzZE'],
 ['1a2b3c4d5e6fzAxXyYzZE7gcaps.8h9i'],
 ['Hlo wor'],
 ['wd!'],
 ['The quick brown fox jumps over the lazdog.'],
 ['AxZXyYzZbraaaaAAAABBBCCCdddDaEEEE!ownE'],
 ['Hello  worlld!'],
 ['AxZXyYzEZE'],
 ['1a2b3c4d5e6fz7g8h9i10jkldoeloIZdDLmnopqrstuvwxyzzzzzzzaaaHello wd!aAAAABBBCCCdddDEEEE!'],
 ['vvar!ouusarxXyYZzZ!ous'],
 ['aaaaAAAABBBCCCfEoxdddDaEEEE!'],
 ['ATh!s 1s @ stsr!ng w!th numb3rs, punctuat!on, and vvar!ousar!ous '
  'caps.AYxXyYzZEAxZXyYzZEcaps.xXyYzZE'],
 ['w!h'],
 ['howoveHello worlAcaps.xXyYzZEhe!!'],
 ['worlAcaps.xXyYzZEhe!!'],
 ['AEIOHlo woroiuq'],
 ['ww!wtwth'],
 ['aaaaACCCdddDaEEEE!'],
 ['w!thHello wd!'],
 ['oveello worlAcaps.xXyYzZEhe!!'],
 ['Th!s 1s @ str!ng w!th numb3rs, punctuat!on, and vvnar!ousar!ous caps.'],
 ['wdoeloIZdDL'],
 ['over1a2b3c4d5anopqrstuvwxyxXyYZzZzvwxyzzzzzzz'],
 ['mFjXdJWPBt'],
 ['The quick brown fox jumps ovelftoSCkoDr the lazdog.'],
 ['HTh!s 1s @ str!ng w!th numb3rs, punctuat!on,brown and vvar!ousar!ous caps.AYxXyYzZEello world!'],
 ['bHTh!s 1s @ str!ng w!th numb3rs, punctuat!on,brown and vvar!ousar!ous caps.AYxXyYzZEello '
  'world!rownw!thHello wd!'],
 ['anazylyou'],
 ['anopqrstuvwTh!sxyxXyYZzZz'],
 ['Hello1a2b3c4d5e6fz7g8h9i10jkldoeloIZdDLmnopqrstuvwxyzzzzzzzaaaHello wd!aAAAABBBCCCdddDEEEE! '
  'worldThe!'],
 ['bHTh!s 1s @ str!ng w!world!, punctuat!on,brown and vvar!ousar!ous caps.AYxXyYzZEello '
  'world!rownw!thHello wd!'],
 ['tworlAcaps.xXyyYzZEhe!!hhhe'],
 ['Helww!wtwhloAxZXyYzZbraaaaAAAABBBCCCdddDaEEEE!ownE'],
 ['worlld!n,'],
 ['braaaaAAAABBBCCCfEoxdddDaEEEEn'],
 ['ATh!s 1s @ stsr!ng w!th numb3rs, punctuat!on, and vvar!ousarr!ous '
  'caps.AYxXyYzZEAxZXyYzZEcaps.xXyYzZE'],
 ['anazaaaaAAAABBBCCCdddDEEEE!yl'],
 ['caps.AYxXyYzZEAxZXyYzZEcaps.xXyYzZE'],
 ['wd!aAAAAAxZXyYzEZEBBBCCCdddDEEEE!'],
 ['1a2b3c4d5e6fz7g8h9i10jklmnopqrstuvwxyzzzzzzzaaaHello'],
 ['AEIOlHlo woroiuq'],
 ['eHello worllquy?ck!wdoeloIZdDL'],
 ['worllquy?ck!wdoeloIZdDL'],
 ['mFjoveHello wstrHello,!ngorlAcaps.xXyYzYZEhe!!JWPBt'],
 ['ATh!s 1s @ stsr!ng w!th numb3rs, punctuat!on, and vvar!ousabqabcd\n'
  '\n'
  '\n'
  '\n'
  'efghijklmnopqrstuvwxyzuickvcdarr!ous caps.AYxXyYzZEAxZXyYzZEcaps.xXyYzZE'],
 ['1a2b3c4d5e6fz7g8h9i10jkldoeloIZdDLxyzzzzzzzaaaHello wd!aAAAABBBCCCdddDEEEE!'],
 ['AEE'],
 ['doeCaaaaAAAABBBCCCdddDEEEE!lloo'],
 ['caps.AYxXyYzZEAxZXyYzZE'],
 ['lAxZXyYzZbraaaaAAAABBBCCCdddDaEEEE!ownEftoSCkoD'],
 ['worll1a2b3c4d5e6f7g8h9i10jklmnopHelww!wtwhloqrstuvwxyzzzzzzzquitoday?ck!'],
 ['AEIOlHlo'],
 ['AAxZX'],
 ['vousar!ous'],
 ['vvar!ousar!ABBBCCCdddDaEEBEE!'],
 ['1a2b3c4d5e6fz7g8h9i10jkldoeloIZdDLxyzzzzzzzaaaHello'],
 ['AEIOlareHlo'],
 ['doworoiuqelo'],
 ['Hello theworllquitodacaps.AzZEy?ck!'],
 ['anorstuvwxyxXyYZzZzdoeloIZdDL'],
 ['worlAcaps.xsXyYzZEheAxZXyYzZE!!'],
 ['lazyy'],
 ['oveHello worlAcHello worllquy?ck!aps.xXyYzZEhe!!'],
 ['over1awt!th2b3c4d5anopqrstuvwxyxXyYZzZzvwxyzzzzzzz'],
 ['HelAxZXyYzZbrownElo worldThe!'],
 ['over1a2b3c4d5e6f7g8h9i10jklmnopqrstuvCaaaaAAAABBBCCCdddDEEEEE!wxyzzzzzzz'],
 ['tIZdDLhvvayYZzZ!ouse'],
 ['oveHello worlAcHello worllquy?ck!aps.xXyYzZEhe!caps.xXyYzZE!'],
 ['1a2b3c4dmnopqrstuvwxyzzzzzzzaaaHello wd!aAAAABBBCCCdddDEEEE!'],
 ['Hlo wolAxZXyYzZbraaaaAAAABBBCCCdddDaEEEE!ownEftoSCkoDr'],
 ['Hello1a2b3c4d5e6fz7g8h9i10jkldoeloIZdDLmnopqrstuvwxyzzzzzzzaaaHello'],
 ['vvar!ous!ar!ous'],
 ['yYzZbraaaaAAAABBBCCCdddDaEEEE!ownE'],
 [''],
 ['ww!wtwefghijklmnopqrstuvwxyzuickvcdarr!oush'],
 ['wwor'],
 ['1a2b3c4d5e6fzAxXyYzZE7gcaps.8h9i10jklmnopqrstuvwxyzzzazzzzaaaquickaAAAABBBCCCdddDEEEE!'],
 ['punctuat!on,brown'],
 ['Helww!wtwhloAxZXyYworllquitoday?ck!zZbraaaaAAAABBBCCCdddDaEEEE!ownE'],
 ['AxXyworlAxcaps.xXyYzZEhe!!YzZE'],
 ['mFjXdJWPBmt'],
 ['1a2b3c4d5e6f7g8h9i10jklmnopstworldThe!zzzzzzz'],
 ['1a2b3c4dmnopqrstuvwxyzzzzzzzaaaHello'],
 ['ww!wtwtwh'],
 ['1a2b3c4dmnopqrstuvwxyzzzzzzzaabrownaHello'],
 ['Hestsr!ngllo  worlld!'],
 ['eT'],
 ['ov'],
 ['ofo'],
 ['thanopqrstuvwTh!sxyxXyYZzZz'],
 ['AEIOHlo woroiuql'],
 ['efghijklmnopqrstuvwxyzuickvcdarr!ous'],
 ['oveHeleHellolo worlAcaps.xXyYzZEhe!!'],
 ['oveHeleHellolo'],
 ['var!xXyYZzZous'],
 ['vvar!ouosar!ous'],
 ['1a2b3c4d5e6fz7g8h9i10jklmnopqrstuvwxyzzzzzzzaaaaAA1AABBBCCCdddDEEEE!'],
 ['oveello'],
 ['Th!s 1s @ str!ng w!th numb3rs, punctuat!on, and vvar!ouusarxXZE'],
 ['oveHello wstrHello,!ngorlAcaps.xXyYzZEhe!!lazy'],
 ['ATh!s 1s @ stsr!ng w!th numb3rs, punctuat!on, and vvar!ousabqabcd\n'
  '\n'
  '\n'
  '\n'
  'efghijklmnopqrsaaaaAAAABBBCCCfEoxdddDaEEEE!tuvwxyzuickvcdarr!ous '
  'caps.AYxXyYzZEAxZXyYEzZEcaps.xXyYzZE'],
 ['Hellcaps.o,'],
 ['over1a2b3c4dt5anopqrstuvwxyxXyYZzZzvwxyzzzzzzz'],
 ['lftoSCkoDl'],
 ['HellHello1a2b3c4d5e6fz7g8h9i10jkldoeloIZdDLmnopqrstuvwxyzzzzzzzaaaHello wd!aAAAABBBCCCdddDEEEE! '
  'wdoeloIZdDLworldThe!yYzZEhe!!'],
 ['over1a2b3c4d5e6f7rstuvwxyzzzzzzz'],
 ['anzazylyou'],
 ['caps.AYxXyYzZEworllquy?ck!AxZXyYzZE'],
 ['AEIOlHlEo'],
 ['AxXyYwzZEworllquitoday?ck!AxXyworlAxcaps.xXyYzZEhe!!YzZE'],
 ['@anazyl'],
 ['c1a2b3c4d5e6fzAxXyYzZE7gcaps.8h9i10jklmnopqrstuvwxyzzzzzzzaaaaAAAABBBCCCdddDEEEE!apZE'],
 ['quitoday?cworll1a2b3c4d5e6f7g8h9i10jklmnopHelww!wtwhloqrstuvwxyzzzzzzzquitoday?ck!'],
 ['AxZXyYzZbrotIZdDLhvvayYZzZ!ousewnE'],
 ['aHello,nazylyou'],
 ['Helww!wtwhloAxZXyYy?ck!zZbraaaaAAAABBBCCCdddDaEEEE!ownE'],
 ['ATh!s 1s @ stsr!ng w!th numb3rs, punworllquy?ck!wdoeloIZdDLctuat!on, and vvar!ousar!ous '
  'caps.AYxXyYzZEAxZXyYzZEcaps.xXyYzZE'],
 ['vvar!ouusarxXZE'],
 ['Hello worl!'],
 ['efghistuvwxyz'],
 ['hthe'],
 ['1a2b3cvvar!ouusarxXyYZuzZ!ous4d5e6fz7g8h9i10jkldoeloIZdDLmnopqrstuvwxyzzzzzzzaaaHello'],
 ['1a2b3c4d5e6fz7g8h9i10jklmnopqrstuvBCCCdddDEEEtE!'],
 ['IZdDL'],
 ['tworlAcaps.xyyYzZEhe!!hhhe'],
 ['dog.HelllftoSCkoDlo'],
 ['efghijklmnopqrsttuvwxyz'],
 ['Hello theworllquritoday?ck!'],
 ['Hlo'],
 ['worlld!ln,'],
 ['andbrown'],
 ['Hl'],
 ['anorstuvwxyxXyYZzZzzdoeloIZdDL'],
 ['abquicckcd'],
 ['Helww!wtwhloAxZXyYzZbraaaaAAAABBBCCCdpuuat!on,ddDaEEEE!ownE'],
 ['Helww!wtwhloAxZXyYzZbraaaaworll1a2b3c4d5e6f7g8h9i10jklmnopHelww!wtwhloqrstuvwxyzzzzzzzquitoday?ck!AAAABBBCCCdddDaEEEE!ownE'],
 ['howoveHello worl!!'],
 ['mFjoveHello'],
 ['AAxcaps.AYxXyYzZEAxZXyYzZEZX'],
 ['abqabcd\n\n\n\nefghijnklmnopqrstuvwxyzuickvcd'],
 ['ae'],
 ['HelllAxZXo worlAcaps.xXyYzZEhe!!'],
 ['AxZXand'],
 ['Th!s 1s @ str!ng w!th numb3rs, punctuat!on, a nd vvar!ousar!ous caps.AYxXyYzZE'],
 ['1a2b3cz4d5e6f7g8h9i10jklmnopqrstuvwxyzzzzzzz'],
 ['ATh!s 1s @ str!ng w!th anazylyounumb3rs, punctuat!on, and var!ous caps.xXyYzZE'],
 ['exaemple@exaHelAxZXyYzZbrownElomple.com'],
 ['ATh!s 1s @ straHello,!ng w!tATh!s 1s @ stsr!ng w!th numb3rs, punctuat!on, and vvar!ousabqabcd\n'
  '\n'
  '\n'
  '\n'
  'efghijklmnopqrstuvwxyzuickvcdarr!ous caps.AYxXyYzZEAxZXyYzZEcaps.xXyYzZE caps.xXyYzZE'],
 ['abcd\n\nww!wtwh\n\nefghlijklmnopqrstuvwxyz'],
 ['vousarr!sous'],
 ['oHelww!wtwhloAxZXyYzZbraaaaAAAABBBCCCdpuuat!on,ddDaEEEE!ownEveelvlo'],
 ['ppAcaps.xXyYzZE'],
 ['oveello worlAcaps.xXyYzZEhhe!!'],
 ['strHo,!ng'],
 ['stsr!ng'],
 ['efghijklmnopqrstuvwxyzhow'],
 ['Th!s 1s @ str!ng w1!th numb3rs, punctuat!on, and vvar!ousar!ous caps.AzZE'],
 ['numb3randsAxZXyYzZbraaaaAAAABBBCCCdddDaEEEE!ownE,'],
 ['ofoo'],
 ['1a2b3c4d5e6f7g8h9i10jklmnopHelww!wtwhloqrstuv8wxyzzzzzzz'],
 ['tworlAcaps.xXyyYzZEhe!h!hhhe'],
 ['AxZXyYzAcaps.xXyYzZEZE'],
 ['efghistvuvwxyz'],
 ['Th!s 1s @ str!ng w1!th nuHello1a2b3c4d5e6fz7g8h9i10jkldoeloIZdDLmnopqrstuvwxyzzzzzzzaaaHello '
  'wd!aAAAABBBCCCdddDEEEE! worldThe!mb3rs, punctuat!on, and vvar!ousar!ous caps.AzZE'],
 ['The quick brown fox jumps overppAcaps.xXyYzZE lthe lazdog.'],
 ['lAxazyZX'],
 ['Th!s 1s @ str!ng w!th numb3rs, punctuat!on, and vvnar!ousar!ous ca.'],
 ['Th!s 1s @ str!ng w!th nuoveello worlAcaps.xXyYzZEhe!!mb3rs, punctuat!on, and '
  'vvar!ouusarxXyYZzZ!ousand caps.AYxXyYzZE'],
 ['worll1a2b3c4d5e6f7g8h9iworlld!ln,10jklmnopHelww!wtwhloqrstuvwxyzzzzzzzquitoday?ck!'],
 ['twhabcd\n\n\n\nefghijklmnopqrstuvwxyz'],
 ['wdd!'],
 ['aefghistvuvwxyzbcd'],
 ['1a2b3c4d5e6fzAxXyYzZE7gcaps.8kh9i10jklmnopqrstuvwxyzzzzzaaaquickaAAAABBBCCCdddDEEEE!'],
 ['HbHTh!s 1s @ str!ng w!th numb3rs, punctuat!on,brown and vv'],
 ['Th!s 1s @ str!ng w!th numb3rs, punctuat!on, and vvar!ouusavrxXZE'],
 ['UVzMKnT'],
 ['w!thh'],
 ['Th!s 1s @ stsr!ngworlld! w!th numb3rs, punctuat!on, and vvar!ousar!ous caps.AYxXyYzZEAxZXyYzZE'],
 ['dodeloIZdDL'],
 ['1a2b3c4d5e6fzAxXyYzZE7gcap5s.8h9i'],
 ['ATh!s 1s @ stsr!ng w!th numb3rs, punctuat!on, '],
 ['vanorstuvwxyxXyYZzZzzdoeloIZdDLousarr!sous'],
 ['capaov.'],
 ['AEIOlHlo uq'],
 ['Thn!s 1s @ str!ng w!th numb3rs, punctuat!on, and vvar!ouusavrxXZE'],
 ['efgijklmnopqrstuvwxyzhow'],
 ['quitodayd?ck'],
 ['YFx'],
 ['dodeloIZd'],
 ['wwworlld!or'],
 ['anoorstuvwxyxXyYZzZz'],
 ['apuncabqabcd\n\n\n\nefghijklmnopqrstuvwxyzuickvcdtuat!on,brown'],
 ['Thn!s 1s @ ouusavrxXZE'],
 ['AEIOlHlo wo'],
 ['w!thHello'],
 ['wt!th'],
 ['tworlAcaps.xXyyYzZEhe!!hdog.Hellohhe'],
 ['efghijnklmnopqrstuvwxyzuickvcd'],
 ['HepllHello1a2b3c4d5e6fz7g8h9i10jkldoeloIZdDLmnopqrstuvwxyzzzzzzzaaaHello '
  'wd!aAAAABBBCCCdddDEEEE! wdoeloIZdDLworldThe!yYzZEhe!!'],
 ['vvar!ouusavrxXZE'],
 ['Thn!s 1ss @ ouunsavrxXZE'],
 ['theworllquitodacapwdd!s.AzZEy?ck!'],
 ['eww!wtwhT'],
 ['efghijklmnopqtIZdDLhvvayYZzZ!ouserstuvwxyz'],
 ['braaaaAAAABBBCCCHello worldThe!fEoxdddDaEEEEn'],
 ['1a2b3c4dmwnopqrstuvwxyzzzzzzzaabrownaHello'],
 ['1a2b3c4d5e6fworldThe!pstworldThe!zzzzzzz'],
 ['AxHello1a2b3c4d5e6fz7g8h9i10jkldoeloIZdDLmnopqrstuvwxyzzzzzzzaaaHello '
  'wd!aAAAABthheBBCCCdddDEEEE! worldThe!ZXyYzZDE'],
 ['bHTh!s 1s @ str!ng w!th numb3vvar!ouusarxXZErs, punctuat!on,brown and vvar!ousar!ous '
  'caps.AYxXyYzZEello world!rownw!thHello wd!'],
 ['Thn!s 1s @ ouussavrxXZE'],
 ['ATh!s 1s @ straHello,!ng w!th numb3rs, punctuat!.on, and var!ous caps.xXyYzZE'],
 ['vousar!o'],
 ['eHello worllquy?ck!wdouunsavrxXZEloIZdDL'],
 ['Th!s 1s @ str!ng w1!th numb3rs, puzZE'],
 ['AxXyYwzZEworllquitoday?ck!xcaps.xXyYzZEhe!!YzZE'],
 ['vv'],
 ['twporlAcaps.xXyyYzefgijklmnopqrstuvwxyzhowhe'],
 ['dog.Hellworhe!o'],
 ['twhawbcd'],
 ['ouunsavrxXZE'],
 ['f1a2b3c4d5e6fz7g8h9i10jklmnopqrTh!s 1s @ str!ng w!th numb3rs, punctuat!on, and '
  'vvar!ouusarxXZEstuvBCCCdddDEEEtE!'],
 ['ndoveHello worlAcaps.xXyYzZEhe!!d'],
 ['Hello1a2b3c4d5e6fz7g8h9i10jklHelww!wtwhloAxZXyYworllquitoday?ck!zZbraaaaAAAABBBCCCdddDaEEEE!ownEdoeloIZdDLmnopqrstuvwxyzzzzzzzaaaHello'],
 ['exampletworlAycaps.xXyYzZEhe!!hhhe@example.colm'],
 ['anorstuvwxyxXHello theworllquitodacaps.AzZEy?ck!L'],
 ['ooveello'],
 ['HbHTh!s 1s @ str!ng w!th numb3rs, punctuat!on,brown and vvl'],
 ['mpYworld!rownw!thHelloSq'],
 ['wwwstrHello,!ngorlAcaps.xXyYzZEhe!!lazy!wtwth'],
 ['efghijklmnopqtIZdDLhvvayYZzZ!ouserstuvwxyzAE'],
 ['anorstuvwxyxXHello theexample@example.comworllquitodacaps.AzZEy?ck!L'],
 ['mFjoeHello'],
 ['oworlAcaps.xsXyYzZEheAxZXyYzZE!!fo'],
 ['ww!wtwefghijklmnopqrstuvwxyzuickanzazylyouvcdarr!oush'],
 ['Th!s 1s @ str!ng w!th num.b3rs, punctuat!on, and vvnar!ousar!ous caps.'],
 ['vvnar!ousar!ous'],
 ['vstsr!ngar!xXyYZzZous'],
 ['oveHelworlAcaps.xXyYzZEhe!!'],
 ['ppAcquitoday?cworll1a2b3c4d5e6f7g8h9i10jklmnopHelww!wtwhloqrstuvwxyzzzzzzzquitoday?ck!aps.xXyYzZE'],
 ['dw!thHello wd!'],
 ['evvar!ouusarxXyYZzZ!ousandfghijnklmnopqrstuvwxyzuickvd'],
 ['efghijklmnwopqrstuvwxyz'],
 ['1amnopqrstuvwxyzzzzzaaaquickaAAAABBBCCCdddDEEEE!'],
 ['efghijklmnopqtaaaaACCCdddDaEEEE!ouserstuvwxyz'],
 ['AAx1a2b3c4d5e6f7g8h9i10jklmnopstworldThe!zzzzzzzZX'],
 ['Th!s 1s @ str!ng w!th numb3rs, punctuat!on, and vvar!ousar!ous caps.AYxXyY zZE'],
 ['Ththeworllquritoday?ck!n!s 1ssThn!s 1s @ str!ng w!th numb3rs, punctuat!onHello worldThe!, and '
  'vvar!ouusavrxXZE @ ouunsavrxXZE'],
 ['AxZXyYzZbraaaaAAAABBBCCCdAEIOHlo woroiuqddDaEEEE!ownE'],
 ['mFjX1a2b3c4d5e6fz7g8h9i10jklmnopqrstuvwxyzzzzzzzaaaHello wd!aAAAABBBCCCdddDEEEE!dJWPBmmt'],
 ['Hellwo world!'],
 ['w!wwtwh'],
 ['AxZXyYzZbraaaaAAAABBBCCCdAEIoOHlo woroiuqddDaEEEE!ownE'],
 ['The quick brown fox juumpos ovelftoSCkoDr the lazdog.'],
 ['xXCaaaaAEEEE!yYzdoeloIZdDLZ'],
 ['Hellcaabcdps.o,'],
 ['oHlabquickcdo'],
 ['Th!s 1s @ stsr!ngworlld! w!and vvar!ousar!ous caps.AYxXyYzZEAxZXyYzZE'],
 ['worl!'],
 ['He!llwo world!'],
 ['punctuat!oHello'],
 ['1a2b3c4d5e6f7g8h9i130jklmnopqrstuvwxyzzzzzzzaaaaAAAABBBCCCdddDEEEE!'],
 ['1a2b3c4d5e6fz7g8hC9i10jklmnopqrstuvBCCCdddDEEEtE!'],
 ['a'],
 ['Th!s 1s @ str!ng w!th numb3rs, punctuat!on, and vvnar!owusar!ous ca.'],
 ['oo'],
 ['aaaaACCCquitoday?cworll1a2b3c4d5e6f7g8h9i10jklmnopHelww!wtwhloqrstuvwxyzzzzzzzquitoday?ck!dddDaEEEEC!'],
 ['world!rownw!thHello'],
 ['anoorstuvwxyxXYZzZz'],
 ['anopqrstvvar!ZouusavrxXZEXyYZzZz'],
 ['The quick brown fox jumpos overppAcaps.xXyYzZE lthe lazdog.'],
 ['anazzylyou'],
 ['JmFjXdJWPBt'],
 ['yYzATh!s 1s @ stsr!ng AxZXyYzZbraaaaAAAABBBCCCdddDaEEEE!ownEw!th numb3rs, punctuat!on, '
  'ZbraaaaAAAABBBCCCdddDaEEEE!ownE'],
 ['worll1a2b3c4d5e6f7g8h9i10jklmnopHelww!wtwhloqr!stuvwxyzzzzzzuitoday?ck!'],
 ['The quick brown fox jumpos overptworlAcaps.xXyyYzZEhe!!hhheaps.xXyYzZE lthe lazdog.'],
 ['aapuncabqabcd'],
 ['wdorld!'],
 ['eeT'],
 ['punctuwat!oHello worlld!n,'],
 ['exww!wtwthampletwortlAycaps.xXyYzZEhee!!hhhe@example.colm'],
 ['HbHTh!s 1s @ stur!ng w!th numb3rs, punctuat!on,brown and vvl'],
 ['aaaaAAAABBBCCCfoxdddDaEEEEoveHello wstrHello,!ngorlAcaps.xXyYzZEhe!!'],
 ['caps.AYxXTRzFAAxyYzZEAxZXyYzZEcaps.xXyYzZE'],
 ['anorstuvwxyxXyYZzZzdoelTh!s 1s @ str!ng w!th numb3rs, punctuat!on, and vvar!ouusavrxXZEoIZdDL'],
 ['vxXyYZzZvar!ousar!ABBBCCCdddDaEEBEE!'],
 ['AxXyYwzZEworllquitoday?ck!AxXyworlAxcaps.xXyYzZEohe!!YzZE'],
 ['1a2b3c4d5e6f7g8h9i110jklmnopqrstworldThe!zzzzzzz'],
 ['andbrow1a2b3c4d5e6f7g8h9i110jklmnotworlAcaps.xXyyYzZEhe!h!hhhepqrstworldThe!zzzzzzz'],
 ['worll!quy?ck!wdoeloIZdDL'],
 ['He!llwo'],
 ['over1awt!th2b3c4d5anopqrstuvwxyxXyYyZzZzvwxyzzzzzzz'],
 ['f1a2b3c4d5e6fz7g8h9i10jklm6nopqrTh!s'],
 ['doeloIIIZdDL'],
 ['ATh!s 1s @ stsr!ng w!th numb3rs, punctuat!on, and vvar!ousarr!ous caps.AxZXyYzZEcaps.xXyYzZE'],
 ['HHelww!wtwhloAxZXyYzZbraaaaAAAABBBCCCdddDaEEEE!ownEellwo world!'],
 ['AEIq'],
 ['1a2b3c4d5e6fzAxXyYzZE7gcaps.8h9i10jklmnopqrstuvwx0yzzzazzzzaaaquickaAAAABBBCCCdddDEEEE!'],
 ['mFjX1wd!aAAAABBBCCCdddDEEEE!dJWPBmmta2b3cd4d5e6fz7g8h9i10jklmnopqrstuvwxyzzzzzzzaaaHello '
  'wd!aAAAABBBCCCdddDEEEE!dJWPBmmt'],
 ['ATh!s 1s @ straHello,!ng w!th nwumb3rs, punctuat!.on, and var!ous caps.xXyYzZE'],
 ['wdooelo'],
 ['worldThe!fEoxdddDaEEEEn'],
 ['Th!s 1s @ str!ng w!th numb3rs, punctuat!on, anhd vvar!ouusarxXyYZzZ!ous caps.AYxXyYzZE'],
 ['efghijklmnopqrsaaaaAAAABBBCCCfEoxdddDaEEEE!tuvwxyzuickvcdarr!ous'],
 ['AxZXyYzZbraaaaAAAABBBCCCdAEIoOHlompYworld!rownw!thHelloSq'],
 ['oHelww!wtwhloAxZXover1a2b3c4dt5anopqrstuvwxyxXyYZzZzvwxyzzzzzzzyYzZbraaaaAAAABBBCCCdpuuat!on,ddDaEEEE!ownEveelvlo'],
 ['Hell'],
 ['abqabcd\n\n\n\nefghvijnklmnopqrstuvwxyzuickvcd'],
 ['AEIOHlo'],
 ['wolAxZXyYzZbraaaaAAAABBBCCCdddDaEEEE!ownEftoSCkoDr'],
 ['AxZXyYzZbraaaaAAAABBBCCCdAEIoOHlo'],
 ['theworllquitoday?ck!'],
 ['wAxZXyYzAcaps.xXyYzZEZE!thHello wd!'],
 ['azy'],
 ['dFymXw'],
 ['ATh!s 1s @ stsr!ng w!th numbcaps.AYxXTRzFAAxyYzZEAxZXyYzZEcaps.xXyYzZE, '],
 ['Hello1a2b3c4d5e6fz7g8h9i10jkldoeloIZdDLmnopqr1a2b3c4d5e6f7g8h9i130jklmnopqrstuvwxyzzzzzzzaaaaAAAABBBCCCdddDEEEE!stuvwxyzzzzzzzaaaHello'],
 ['He!llxXyYZzZwo'],
 ['1a2b3c4d5zz'],
 ['braaaaAAAABBBCCCHello'],
 ['ww!wtwefghijklmnopqrstuvwxyzuickanzazylyouvcdsarr!oush'],
 ['mFjX1a2b31a2b3c4d5e6f7g8h9i10jklmnopHelww!wtwhloqrstuv8wxyzzzzzzzc4d5e6fz7g8h9i10jklmnopqrstuvwxyzzzzzzzaaaHello '
  'wdw!aAAAABBBCCCdddDEEEE!dJWPBmmt'],
 ['ATh!s'],
 ['w!aaaaAAAABBBCCCdddDaEEEE!hHello'],
 ['AxZXyYzZbraaaaHe!llwoAAAABBBCCCdAEIoOHlo woroiuqddDaEEEE!ownE'],
 ['abquiccUVzMKnTvvar!ousar!ouscd'],
 ['HelllAxZXo wHellwooexampletworlAcaps.xXyYzZEhe!!hhhe@example.colms.xXyYzZEhe!!'],
 ['cpaps.'],
 ['theworllqouitoday!'],
 ['quitoday?cworll1a2btheworllqouitoday!3c4d5e6f7g8h9i10jklmnopHelww!wtwhloqrstuvwxyzzzzzzzquitoday?ck!'],
 ['Th!s 1s @ str!ng w!th nuoveello worlAcaps.xXyYzZEhrxXyYZzZ!ousand caps.AYxXyYzZE'],
 ['AEIOUaeoHlabquickcdoioiuq'],
 ['AAxcaps.AYxXyYzZEAxZZEZX'],
 ['1a2b3cz4d5e6f7g8h910jklmnopqrstuvwxyzzzzzzz'],
 ['oveHelleHellolo worlAcaps.worlAcaps.xXyYzZEhXyYzZEhe!!'],
 ['doHello1a2b3c4d5e6fz7g8h9i10jkldoeloIZdDLmnopqr1a2b3c4d5e6f7g8h9i130jklmnopqrstuvwxyzzzzzzzaaaaAAAABBBCCCdddDEEEE!stuvwxyzzzzzzzaaaHelloeCaaaaAAAABBBCCCdddDEEEE!lloo'],
 ['vvar!ouar!ous'],
 ['1seuvwxyz'],
 ['bHTh!s'],
 ['Th!s 1s @ stsr!ng w!th numb3rs, punctuatThe!on, and vvar!ousar!ous caps.AYxXyYzZEAxZXyYzZE'],
 ['Helww!wtwhloAxZXyYworllquitoday?ck!zZbraaaaAAAABBBCIZdDLCCdddDaEEEE!ownE'],
 ['aHlnd'],
 ['HelAxZXyYzZbrownElo wrorldThe!'],
 ['vopunctuwat!!oHellousar!ous'],
 ['w!wvar!xXyYZzZouswtwh'],
 ['worllquy?ck!'],
 ['numbcaps.AYxXTRzFAAxyYzZEAxZXyYzZEcaps.xXyYzZE,'],
 ['theworllquitodacaps.AzZEy?ck!L'],
 ['vvar!ouarr!ous'],
 ['f1a2b3c4d5e6fzrTh!s'],
 ['vvar!oAxHello1a2b3c4d5e6fz7g8h9i10jkldoeloIZdDLmnopqrstuvwxyzzzzzzzaaaHello '
  'wd!aAAAABthheBBCCCdddDEEEE! worldThe!ZXyYzZDEuusarxXyYZzZ!ous'],
 ['aHlbHTh!s 1s @ str!ng w!world!, punctuat!on,brown and vvar!ousar!ous caps.AYxXyYzZEello '
  'world!rownw!thHello wd!nd'],
 ['dogg.'],
 ['@@'],
 ['varos'],
 ['abqabcd'],
 ['qquick'],
 ['wworhow'],
 ['punctluwat!oHello worlld!jumposp,'],
 ['aefghistvuvwxyz'],
 ['1a2b3c4d5e6fzAxXyYzZE7gcaps.8h9i10jklmnopqBBBCCCddidDEEEE!'],
 ['ATh!s 1s @ straHello,!ng w!th numb3ros, punctuatThe!on,punctuat!.on, and var!ous caps.xXyYzZE'],
 ['AlftoSCkoDEIOlHlo wo'],
 ['xx'],
 ['mFjoemHello'],
 ['Hlo wolAxZXyYzZbraaaaAAAABBBCCCdddDaEEoveHelworlAcaps.xXyYzZEhe!!EE!ownEftoSCkoDr'],
 ['Thn!s 1worlAcaps.xXyYzZEhrxXyYZzZ!ousands @ ouusavrxXZE'],
 ['dog.Hellwor'],
 ['xXCaaaaAEEEE!yYzdoeloIZdDLZvar!ous'],
 ['theworllquitodacaps.AzZEy?ack!L'],
 ['puzZE'],
 ['fLDZzeBh'],
 ['fox'],
 ['apuncabqabcd'],
 ['efghijklmnopqtIZdDLoveHello worlAcHello worllquy?ck!aps.xXyYzZEhe!!hvvayYZzZ!ouserstuvwxyz'],
 ['worllquy?ck!aps.xXyYzZEhe!!hvvayYZzZ!ouserstuvwxyz'],
 ['wt!thvvar!ousar!ABBBCCCdddDaEEEE!'],
 ['wdw!aAAAABBBCCCddDEEEE!dJWPBmmt'],
 ['AAxXyzZE'],
 ['EjGkZwKvO'],
 ['anazylyounumb3rs,'],
 ['oveello worlAcaps.xXyYzZEhhe!!lftoSCkoDl'],
 ['AEIOUaeiou'],
 ['.'],
 ['0123456789'],
 ['AbCdeFGHiJklmnOPqRsTuVwXYz'],
 ['AAaaBBbbCCccDDddEEeeFFff'],
 ['akdj nsoirewqabfj nal kjaks kdas'],
 ['\n'],
 ['    '],
 ['\t'],
 ['\r'],
 ['Hello worldd!'],
 ['AEIOUaeHello worldd!iouq'],
 ['The quick brown fox jaaaaAAAABBBCCCdddDEEEE!oveHello,dog.'],
 ['AEIOUeiouq'],
 ['Th!s 1s @ str!ng w!th numb3rs, punctuat!oHellon, and var!ous caps.'],
 ['examplle@example.com'],
 ['Hello, how tare you today?'],
 ['example@example.comThe quick brown fox jumps over the lazy dog.'],
 ['aaaaAAdDEEEE!'],
 ['Hello, h tare you today?'],
 ['str!ngand'],
 ['The quick brown fox jumps over the lazy  dog.'],
 ['punctuat!oHellolazyn,'],
 ['Th!s 1s @ str!ngl w!th numb3rs, punctuat!oHellon, and var!ous caps.'],
 ['aaaaaAAdDEEEE!'],
 ['aaaaAAdDEEaaaaAAdDEEEE!EEE!'],
 ['The quick brown foxy  dog.'],
 ['examplle@example.copm'],
 ['The quick brown foxy g.'],
 ['AEIOUeoiouq'],
 ['1a2b3c4d5e6f7g8h9i10Hello, h tare you today?jklmnoprstuvwxyzzzzzzz'],
 ['worl'],
 ['str!!ng'],
 ['aaexample@example.comTheaaAAAABBBCCCdddDEEEE!'],
 ['The quick brown fox jumps over the lazyog.'],
 ['str!ngandlazy'],
 ['punctuat!oHellon,'],
 ['tokday?jklmnoprstuvwxyzzzzzzzz'],
 ['Hello, how efghijklmnopqrstuvwxyztare you totokday?jklmnoprstuvwxyzzzzzzzzday?'],
 ['The quick brown fox jumps over the lazy dog.h'],
 ['str!ngl'],
 ['The quiver the lazy dog.h'],
 ['today?jklmnoprstuvwxyzzzzzzz'],
 ['Hello, how efghijklmnopqrstuvwxyztare you totokday?jklmnoprstuvwxyzzzzzzzzThe quick brown fox '
  'jumps over the lazy dog.hday?'],
 ['Hello, how tare youexample@example.comThe today?'],
 ['lazyog.'],
 ['eHello,'],
 ['AEIOUaeHello worlaaaaAAdDEEEE!dd!iouq'],
 ['jyJiBLGfRP'],
 ['The quick brown fox jumps odver the lazy dog.h'],
 ['efghijklmnopqrstuvwxyztare'],
 ['The quick brown fox jumps ovner the lazy  dog.'],
 ['abcd\n\n\n\nefghijklmnopquickyz'],
 ['efghijklmnopqrstuvwxyzytaredog.hday?'],
 ['aaaaAAAABBBCCdDEEEE!'],
 ['aaaaAAdEexample@example.comTheDEEaaaaAAdDEEEE!EEE!'],
 ['The qThe quick brown fox jumps over the lazy  dog.uick brown foxy g.'],
 ['foxy'],
 ['Hello,  h tare you today?'],
 ['lazzyog.'],
 ['Th!s 1s @ str!ng w!th numb3rs, punctuat,!oHellon, and var!ous caps.'],
 ['Hellay?'],
 ['Th!s 1s @ str!ng  w!th numb3rs, punctuat!oHellon, and var!ous caps.'],
 ['Hellobrown world!'],
 ['Hello,  hh  tare you today?'],
 ['g.'],
 ['aaaAEIOUeiouqquiveraAAdDEEaaaaAAdDEEDEE!EEE!'],
 ['aaaaaAAAABBBCCdDEEEE!'],
 ['woyourl'],
 ['MBSXebBdc'],
 ['efghijklmnogpqrstuvwxyztare'],
 ['1a2b3c4d5e6f7g8h9i10Hello,'],
 ['1a2b3c4d5e6f7g8h9i10jklmnopqrstuvwxkyzzzzzzz'],
 ['Th!s 1s @ str!ngl w!th numb3rs, punctuat!oHellon, aand var!ous caps.'],
 ['ayoubcd\n\n\n\nefghijklmnopqrstuvwxyz'],
 ['HelThe qThe quick brown fox jumps over the lazy  dog.howuick brown foxy g.lay?'],
 ['abcdHello, how tare youexample@example.comThe today?'],
 ['worlefghijklmnopqrstuvwxyztare'],
 ['dog.hday?'],
 ['lazzyaoog.'],
 ['s1a2b3c4d5e6f7g8h9i10jklmnopqrstuvwxyzzzzzzztr!ngl'],
 ['1a2b34c4d5e6f7g8h9i10Hello,'],
 ['xkfHeZTld'],
 ['foy'],
 ['str!gngnandlazy'],
 ['str!n'],
 ['g.lay?'],
 ['efghredog.hday?'],
 ['jumps'],
 ['Helleo wtoday?jklmnoprstuvwxyzzzzzzzorld!'],
 ['Th!s 1s @ str!ng w!th numb3rs, punctuat,!hoHellon, and var!ous caps.'],
 ['Helleo'],
 ['andd'],
 ['anThe quick brown fox jumps over the lazyog.dd'],
 ['tare'],
 ['xkfHeZTldAEIOUaeHello worldd!iouq'],
 ['str!ngandlaTh!s 1s @ str!ng  w!th numb3rs, punctuat!oHellon, and var!ous caps.zy'],
 ['ayoubcd\n'
  '\n'
  '\n'
  '\n'
  'efghijklmnopqrstuvwxyzTh!s 1s @ str!ngl w!th numb3rs, punctuat!oHellon, aand var!ous caps.'],
 ['w!!h'],
 ['aaaaAAAABBBnumb3rs,CCCdddDEEEE!'],
 ['wayoubcdorl'],
 ['abcd\n\n\nc\nefghijklmnopquickyz'],
 ['aaaaAAAABBBnumb3rs,CCCdddDEw!!hEEE!'],
 ['AEIOUThe quick brown fox jumps over the lazy  dog.'],
 ['Hello wefghijklmnopqrstuvwxyztareorldd!'],
 ['AEIcaps.zyOUaeiouq'],
 ['lo,'],
 ['ovner'],
 ['str!caps.zyngcand'],
 ['jaaaaAAAABBBCCCdddDEEEE!oveHello,dog.'],
 ['worol'],
 ['xkfHeZTldAEIOUaeHello worpunctuat,!hoHellon,ldd!iouq'],
 ['The quick brown fox jaaaaAAAAeBBBCCCg.'],
 ['strTh!s'],
 ['example@example.comThe'],
 ['The qThe quick brown fox jumpsexample@example.comThe over the lazy  dog.uick brown foxy g.'],
 ['Th!s 1s @ str!ngl w!th numb3rs, punctuat!oHellon, aanvar!ous caps.'],
 ['wtoday?jklmnoprstuvwxyzzzzzzzorld!'],
 ['dHello,  hh  tare you today?og.h'],
 ['abcd\np\n\nc\nefghijklmnopquickyz'],
 ['ayoubcd\n'
  '\n'
  '\n'
  '\n'
  'efghijklmnopqrstuvwxyzTh!s 1s @ str!ngl w!th numb3rs, punctuat!oHellon, aand vawr!ous caps.'],
 ['MBSXebnumb3rs,Bdc'],
 ['oHello,  hh h tare you today?'],
 ['Th!s 1s @ str!ng  w!th numb3rs, punctuat!uoHellon, and var!ous caps.'],
 ['wlo,!h'],
 ['AEIOUaeiojyJiBLRGfRP'],
 ['hHello, how are you today?'],
 ['The quick brown fox jaaaaAAAAeBBBCCtoday?og.hCg.'],
 ['abcd\np\n\nc\nefghijklmnopquickytoday?jklmnoprstuvwxyzzzzzzzz'],
 ['worldd!'],
 ['aaaaAAdDEEaaaaAHello wefghijklmnopqrstuvwxyztareorldd!AdDEEEE!EEE!'],
 ['The qThe quick brown fox jumpseThe qThe quick brown fox jumpsexample@example.comThe over the '
  'lazy  dog.uick brown foxy g.xample@example.comThe over the lazy  dog.uick brown foxy g.'],
 ['AEEIOUaeHelHlo'],
 ['abcd\n\n\njc\nefghijklmnopquickyz'],
 ['The quiTh!s 1s @ str!ng w!th numb3rs, punctuat,!hoHellon, and var!ous caps.ck brown fox jumps '
  'odverlazy dog.h'],
 ['Helle'],
 ['efghijklmnTh!s 1s @ str!ng  w!th numb3rs, punctuat!uoHellon, and var!ous caps.opqrstuvwxyztare'],
 ['gh.'],
 ['c'],
 ['xkfHeZld'],
 ['jaaaaAAAAeBBBCCCg.'],
 ['1a2b3c4d5e6f7g8h9i10Hejcllocaps.ck,'],
 ['xkfHld'],
 ['worlefghijklmnopquickytoday?jklmnoprstuvwxyzzzzzzzzdd!'],
 ['abcd\np\n\nc\nefghijlazzyog.klmnopquickyz'],
 ['caps.zy'],
 ['aaexamDEEEE!'],
 ['punctuat!uoHellon,'],
 ['Hexample@example.comello, how efghijklmnopqrstuvwxyztare you '
  'totokday?jklmnoprstuvwxyzzzzzzzzday?'],
 ['lThe quick brown fox jaaaaAAAABBBCCCdddDEEEE!oveHello,dog.'],
 ['dog.hoday?'],
 ['examplle@example..copm'],
 ['Th!s 1s @ str!ng w!th numb3rs, punctuat,!oHellnumb3rs,on, and var!ous caps.'],
 ['The quick brown AEEIOUaeHelHlofox jumps over the lazyog.'],
 ['lazyog.dd'],
 ['example@example.comThe quick brown fvawr!ousox jumps over the lazy dog.'],
 ['dog.howuick'],
 ['quiefghijklmnopquickyzck'],
 ['AEIcaps.zyOUpaeiouq'],
 ['abcdHelloanThe, how tare youexample@example.comThe today?'],
 ['1a2b3c4d5e6fTh!s 1s @ str!ng  w!th numb3rs, punctuat!oHellon, and var!ous '
  'caps.7g8h9i10jklmnopqrstuvwxyzzzzzzz'],
 ['Hello, hTh!sare you today?'],
 ['Th!s 1s @ str!ngl w!th numb3rs, puncotuat!oHellon, and var!ous caps.'],
 ['Hstr!caps.zyngcandllo, how are you today?'],
 ['The quick kbrown fox jumps overt the lazyog.'],
 ['punctuat!ocn,'],
 ['efgxkfHeZTldAEIOUaeHellohijklmnopqrstuvwxyz'],
 ['aaaEaAAdDEEEEE!'],
 ['AEIOUe'],
 ['The quick brown fosx jumps over the lazyog.'],
 ['eThe quickare brown fe'],
 ['examplxHello,le@example.com'],
 ['xkfHeZTldAEIOUaeHello worpunctuat,!hoiHellon,ldd!iouq'],
 ['youexample@examcaps.ckple.comThe'],
 ['xkfHeZTldAEIOUaeH worlddd!iouq'],
 ['1a2b3c4d5e6f7g8h9i1ja0jklmnopqrstuvwxyzzzzzzz'],
 ['The qThe quick brown fox jumpsexample@example.comThe overfosx the lazy  dog.uick brown foxy g.'],
 ['MBSXaaaaAAAABBBnumb3rs,CCCdddDEEEE!ebBdc'],
 ['The quick brown fox jumps over the  lazy dog.h'],
 ['sexamplxHello,le@example.comtr!!ng'],
 ['lazzyaooog.'],
 ['examplle@examle.com'],
 ['Helllay?'],
 ['puncotuat!oHellon,'],
 ['eample.com'],
 ['worlaaaaAAdDEEEE!dd!iouq'],
 ['MBSXaaaaAAAABBdc'],
 ['laovnerzyog.'],
 ['fe'],
 ['The quick kbrown fox jumpThe quick brown fox jumqTheps over the lazyog.s overt the lazyog.'],
 ['examplle@examexamplle@example.copm.com'],
 ['xkfHeZTldAEIOUaeHello worpunctua t,!hoiHellon,ldd!iouq'],
 ['He'],
 ['yoo'],
 ['The quick brown fox jumps odver the l azy dog.h'],
 ['caps.ck'],
 ['laovnerzyog.jyJiBLGfRP'],
 ['laovnerzhyoHelTheg.jyJiBLGfRP'],
 ['punctuaTh!s 1s @ str!ng w!th numb3rs, punctuat,!oHellnumb3rs,on, and var!ous caps.t!on,'],
 ['t,!hoiHellon,ldd!iouq'],
 ['aaexample@example.comTheaaAAAABabcd\np\n\nc\nefghijklmnopquickytoday?jklmnoprstuvwxyzzzzzzzz!'],
 ['worrol'],
 ['xkfHeZTldAEIOUaeHello wdd!iouq'],
 ['Th!s 1s @ str!ngctuat,!oHellon, and var!ous caps.'],
 ['aaaaAAdEexample@example.comTheaDEEaaaaAAdDEEEaE!EEE!'],
 ['Hellodog. world!'],
 ['The quick brown fox jumps over the lazy do.'],
 ['aaexample@example.comTheaaAAAABabcd'],
 ['aaaaAAdDEEaaaaHexample@example.comello,DEEEE!EEE!'],
 ['ww!h'],
 ['Hello, how tare youexamplefghijlazzyog.klmnopquickexample@example.comTheyze@example.comThe '
  'today?'],
 ['strTh!hpunctuat!oHellon,s'],
 ['The quick brown AEEIOUaeHdo.elHlofox jumps over the lazyog.'],
 ['aaaaAAdEexample@aexample.comTheaDEEaaaaAAdDEEEaE!EEE!'],
 ['totokday?jklmnoprstuvwxyzzzzzzzzThe'],
 ['wtoday?jklmnoprstuvwxHstr!caps.zyngcandllo,yzzzzzzzorld!'],
 ['wefghijklmnogpqrstuvwxyztare'],
 ['HelThe qThe quick brown strTh!hpunctuat!oHellon,ss over the lazy  dog.howuick brown foxy g.?'],
 ['caps.t!on,'],
 ['!h'],
 ['Th!s 1s @'],
 ['XbFTQMiAwt'],
 ['MBSXaaaaBAAAABBdc'],
 ['eThe quicykare blazzyaoog.rown fe'],
 ['Hello,worldd!iouq   hh  tare you today?'],
 ['Hello, h tarAEIOUaeHello worlaaaaAAdDEEEE!dd!iouqe you today?'],
 ['today?og.h'],
 ['aaaaaAAAABBBCCdDEEEE!Th!s 1s @ str!ngl w!th numb3rs, punctuat!oHellon, and var!ous caps.'],
 ['laovnerzyog.jyJiBLGfRsngandP'],
 ['The quick brown AEEIayoubcd\n'
  '\n'
  '\n'
  '\n'
  'efghijklmnopqrstuvwxyzOUaeHdo.elHlofox jumps over the lazyog.'],
 ['tokday?jklmnoprstuvwxyzzztzzzzz'],
 ['xkfHeZTldAHexample@example.comello,EIOUaepHello wdd!iouq'],
 ['xkfHeZTldAEIOUaeH'],
 ['punt!on,'],
 ['MBSXadHello,  hh  tare you today?og.hEEEE!ebBdc'],
 ['eHellHellodog. world!o,'],
 ['The quiHellobrownck brown AEEIOUaeHelHlofox jumps over the lazyog.'],
 ['xkfHeZTldAHexample@examllo,EIOUaepHello wdd!iouq'],
 ['Hexample@example.comello, how efge you totokdayzzzzzday?'],
 ['CpCOvCPPy'],
 ['wefghijklmnopqrstuvwxyztareorldd!'],
 ['1a2b3c4d5e6f7g8h9i10jklmnopqrstuvwxyzzzczzz'],
 ['The quick brown fox juamps odver aaaaAAdDEEaaaaHexample@example.comello,DEEEE!EEE!the lazy '
  'dog.h'],
 ['tokday?jklumnoprstuvwxyzzztzzzzz'],
 ['abcdHelloanThe,'],
 ['AEEIOUaeHdo.elHlofox'],
 ['aaaaAAAABBBCCCdddDElazzyaoog.EE!'],
 ['aaaaAAdDEEaaaaAHello wefghijklmnopqrstuvwxyztareorldd!AdDEEEstr!ngandlazyE!EEE!'],
 ['str!!ngstr!!ng'],
 ['Th!s 1s @ str!ngl w!th numb3rs, puncotuat!oHellon, and var!ous caayoubcd\n'
  '\n'
  '\n'
  '\n'
  'efghijklmnopqrstuvwxyzTh!s 1s @ str!ngl w!th numb3rs, punctuat!oHellon, aand vawr!ous caps.ps.'],
 ['AThe quiver the lazy dog.heiou'],
 ['lago.'],
 ['Th!s 1s @ str!ngl w!th numb3jaaaaAAAABBBCCCdddDEEEE!oveHello,dog.Hellon, and var!ous caps.'],
 ['worlefghijklmnopqrstuvwxyztareyoo'],
 ['watoday?jklmnoprstuvwxyzzzzzzzyoubcdorl'],
 ['Hello, how e you totokday?jklmnoprstuvwxyzzzzzzzzday?'],
 ['quiver'],
 ['t,!hoiHellon,ldd!liouq'],
 ['txkfHeZTldAEIOUaeHare'],
 ['xXyjcYzZ'],
 ['taree'],
 ['caayoubd'],
 ['Hello, how tare youexamplefghijlazzyog.klmnople.comTheyze@example.comThe today?'],
 ['Th!s 1s @ str!ngl w!thg.? numb3rs, puncotuat!oHellon, and var!ous caayoubcd\n'
  '\n'
  '\n'
  '\n'
  'efghijklmnopqrstuvwxyzTh!s 1s @ str!ngl w!th numb3rs, punctuat!oHellon, aand vawr!ous caps.ps.'],
 ['Th!s 1s @ str!ngl w!th numb3jaaaaAAAABBBCCCdddDEEEE!oveHello,dog.Hellon, and '
  'vaaaaAAdDEEaaaaHexample@example.comello,DEEEE!EEE!r!ous caps.'],
 ['HelloanThe worldd!'],
 ['aa@example.comTheaDEEaaaaAAdDEEEaE!EEE!'],
 ['abcd\n\n\nc\novertfghijklmnopquickyz'],
 ['watodayhow?jklmnoprstuvwxyzzzzzzzyoubcdorl'],
 ['pun!t!on,'],
 ['Th!s 1s @ str!ngl w!th numb3jaaaaAAAABBBCCCdddDEEEE!oveHello,dog.Hellon, and '
  'vaaaaAAdDEEaaaaHexample@example.comello,DEEEE!EEE!r!ous .'],
 ['AEIxkfHeZldOUThe quick brown fox jumps over the lazy  dog.'],
 ['cpunctuaTh!s 1s @ str!ng w!th numb3rs, punctuat,!oHellnumb3rs,on, and var!ous '
  'caps.t!on,aayoubd'],
 ['The quick brown fox juamps odver a.comello,DEEEE!EEE!the lazy dog.h'],
 ['Heayoubcd\n'
  '\n'
  '\n'
  '\n'
  'efghijklmnopqrstuvwxyzTh!s 1s @ str!ngl w!th numb3rs, punctuat!oHellon, aand var!ous '
  'caps.xample@example.comello, how efge you totokdayzzzzzday?'],
 ['The quick brown AEEIOUaeHdo.elHlofoxHelloanThe jumps over the lazyog.'],
 ['abcd\np\n\nc\nefghijklmnopquickytoworld!day?jklmnoprstuvwxyzzzzzzzz'],
 ['efghijklmnopquickytoday?jklmnoprstuvwxyzzzzzzzz'],
 ['tkokday?jklmnoprstuvwxyzzztzzzzz'],
 ['worlefghijklmnopquickytoday?jklmnoprstuvwxzzzzdd!'],
 ['jumqTheps'],
 ['worlaaaaAAd!dd!iouqe'],
 ['Th!s 1s @ str!ngl w!.th numb3rs, punctuat!oHellon, aand var!ous caps.'],
 ['punt!Hello wefghijklmnopqrstuvwxyztareorldd!,'],
 ['aand'],
 ['The quick brocaayoubcdwn foxr jumps ovner the lazy  dog.'],
 ['xkfHeZTldAHexample@XbFTQMiAwtexample.comello,EIOUaepHello'],
 ['lazzy'],
 ['odverlazy'],
 ['wMdE'],
 ['Hellobrowntare'],
 ['Th!s 1s @ str!ngl w!.th numb3rs, punctuat!oHellon, aand var!ous caexample@example.comTheps.'],
 ['trstuvwxyzzztzzzzz'],
 ['examplle@Th!s 1s @ str!ngl w!th numb3rs, punctuat!oHellon, aand var!ous '
  'caps.exameamplle@example.copm.com'],
 ['The quiHellobrownck brown AEEIOUaeHelHlofox jumps over the lazyAEIOUe'],
 ['strTh!hpunctuat!oHel'],
 ['eTheaaaaAAAABBBnumb3rs,CCCdddDEw!!hEEE! quicykare blazzyaoog.rown fe'],
 ['Heayoubcd\n'
  '\n'
  '\n'
  '\n'
  'efghijklmnopqrstuvwxyzTh!s 1s @ str!ngl w!th numb3rs, punctuat!oHellon, aand quivervar!ous '
  'caps.xample@example.comello, how efge you totokdayzzzzzday?'],
 ['jyJJiBLGfRP'],
 ['The quick br ocaayoubcdwn foxr jumps ovner the lazy  dog.'],
 ['aa@example.comTheaaDEEaaaaAThe quick brown fox juamps odver a.comello,DEEEE!EEE!the lazy '
  'dog.hAdDEEEaE!EEE!'],
 ['Hellodog. worstr!nld!'],
 ['Th!s 1s @ str!ngl w!th numb3rs, puncotuat!oHellon, and var!ous caayoubcd\n'
  '\n'
  '\n'
  '\n'
  'efghijklmnopqrstuvwxyzTh!s 1s @Th!s 1s @ str!ng w!th numb3rs, punctuat!oHellon, and var!ous '
  'caps. str!ngl w!th numb3rs, punctuat!oHellon, aand vawr!ous caps.ps.'],
 ['dHello,'],
 ['aa@exampwlo,!hle.comTheaDEEaaaaAAdDEEEaE!EEE!'],
 ['jumpsexamplecaps.xample@example.comello,@example.comThe'],
 ['p,unc,'],
 ['AEIOUThefghijklmnopquickytoday?jklmnoprstuvwxyzzzzzzzz!e quick brown hfox  jumps over the lazy  '
  'dog.'],
 ['lagoTh!s 1s @ str!ngl w!th numb3rs, punctuat!oHellon, aanvar!ous caps.'],
 ['br'],
 ['Hellodog. worstr!nltoday?og.hd!'],
 ['AEEIayoubc'],
 ['caaydoubd'],
 ['dog.howuoverfosxick'],
 ['aaaaAAdDEEaaaaAHello wefghijklmnopqrstuvwxyztareorldd!AdDEEEstr!ngstr!ngandlaTh!s 1s @ str!ng  '
  'w!th numb3rs, punctuat!oHellon, and var!ous caps.zyandlazyE!EEE!'],
 ['AEIOUaThe quick brown fox juamps odver aaaaAAdDEEaaaaHexample@example.comello,DEEEE!EEE!the '
  'lazy dog.heiou'],
 ['!!anThehwayoubcdorl'],
 ['Th!s 1s @ str!ngl w!th numb3rs, puncotuat!oHellon, and var!ous caayoubcd\n'
  '\n'
  '\n'
  '\n'
  'efghijklmnopqrstuvwxy!zTh!s 1s @ str!ngl w!th numb3rs, punctuat!oHellon, aand vawr!ous '
  'caps.ps.'],
 ['lazHellod1a2b3c4d5e6f7g8h9i10Hello,og.zcaexample@example.comTheps.'],
 ['Th!s 1s @ str!ng w!th numb3rs, punctuat,!oHellon, an d var!ous caps.'],
 ['wdThe quick brown fox jumps over the  lazy dog.hd!iouq'],
 ['thHello, how efghijklmnopqrstuvwxyztare you totokday?jklmnoprstuvwxyzzzzzzzzThe quick brown fox '
  'jumps over the lazy dog.hday?wefghijklmnopqrstuvwxyztareorldd!AdDEEEstr!ngstr!ngandlaTh!se'],
 ['hHellodog.ow'],
 ['caps.exameamplle@example.copm.com'],
 ['AEIxkfHeZldOUThe quick bzy  dog.'],
 ['wlazzyayoubcdorl'],
 ['The quick brown foHello, how tare you today?x jumps over txXyYzZhe lazy dog.h'],
 ['caps.zyandlazyE!EEE!'],
 ['efgxkfHeZTldAEIOUaeHellohijklmnopqrustuvwxyz'],
 ['jyJHellobrown world!iBLGfRP'],
 ['Tver the  lazy dog.h'],
 ['AEIOUThefghijklmnopquickytoday?jklmnoprstuvwxyzzzzzzzz!e'],
 ['foxx'],
 ['The quick br ocaayoubcdwn foxr jukmps ovner the lazy  dog.'],
 ['AThe'],
 ['AEIOUae'],
 ['quiefghijklmnopquick'],
 ['caps.exameamplAEIOUaele@example.copm.com'],
 ['jumpseThe'],
 ['lagoTh!s 1s @ str!ngl w!th numb3rs,wdd!iouq'],
 ['xkflazyog.ddHld'],
 ['quiefghijkulmnopquick'],
 ['dHello,  hh  taare you today?og.h'],
 ['examplle@examexamplle@exampaa@exampwlo,!hle.comTheaDEEaaaaAAdDEEEaE!EEE!le.copm.com'],
 ['dog.hAdDEEEaE!EEE!'],
 ['Th!s 1s @ str!ngl w!th numb3jaaaaAAAABBBCCCdddDEEEE!oveHello,dog.Hellon, and var!ojyJHellobrown '
  'world!iBLGfRPus caps.'],
 ['aaaaAAAxkfHeZTldAHexample@example.comello,EIOUaepHelloABBBCCdDEEEE!'],
 ['HellTh!s 1s @ str!ngl w!th numb3rs, punctuat!oHellon, aanvar!ous.o,'],
 ['worlefghijklmnopqrstuvwxyzt'],
 ['jummps'],
 ['quiefghijkulmnAEIOUaeiojyJiBLRGfRPopqpuick'],
 ['Th!s 1s @ str!ngl w!th numb3rs, puncotuat!oHellon, and var!ous caayoubcd\n'
  '\n'
  '\n'
  '\n'
  'efghijklmnopqrstuvwxy!zTh!s 1s @ str!ngl w!th numb3rs, punctuat!oHellon, aar!ous caps.ps.'],
 ['pun!t!onworld!iBLGfRPus,'],
 ['youexamplefghijlazzyog.klmnopquickexample@example.comTheyze@example.comThe'],
 ['HHe'],
 ['caps.ps.'],
 ['aaexamDEEE!'],
 ['aaaaAAAABBBnumb3t,!hoiHellon,ldd!liouqrs,CCCdddDEEEE!'],
 ['foHello,worlaaaaAAdDEEEE!dd!iouq'],
 ['Th!s 1s @ str!ngl w!thg.? numb3rs, puncotuat!oHellon, and var!ous caayoubcd\n'
  '\n'
  '\n'
  '\n'
  'efghijklmnopqrstuvwxyzTh!s 1s @ str!ngl w!th numb3rs, punctuat!oHellon, aand vawr!ous '
  'caps.ps.1a2b34c4d5e6f7g8h9i10Hello,'],
 ['lworldd!azzyog.'],
 ['Hello, how tare youexamplefghijlazzyog.klmnopquickexamplle@example.comTheyze@example.comThe '
  'today?'],
 ['!!anThcehwayoubcdorl'],
 ['todTh!s 1s @ str!ng at,!jyJJiBLGfRPoHellon, and var!ous caps.ay?og.h'],
 ['Hello, how tare youexamplefghijlazzyog.klmnopayoubcd\n'
  '\n'
  '\n'
  '\n'
  'efghijklmnopqrstuvwxyzle.comTheyze@example.comThe today?'],
 ['1xkfHeZTldAEIOUaeHelloa2b3c4d5e6f7g8h9i10jklmnopqrstuvwxyzzz'],
 ['w'],
 ['aaaaAAdDEEaaaaHEexample@example.comello,DEEEE!EEE!'],
 ['cpunctuaTh!s'],
 ['strtokday?jklmnoprstuvwxyzzztzzzzz!ng'],
 ['Th!s 1s @ str!ngl w!th numb3rs, puncotuat!oHellon, and var!ous cappun!t!onworld!iBLGfRPus,s.'],
 ['caps.worlefghijklmnopqrstuvwxyztareyoot!on,'],
 ['The quick tbrown AEEIayoubcd\n'
  '\n'
  '\n'
  '\n'
  'efghijklmnopqrstuvwxyzOUaeHdo.elHlofox jumps over the lazyog.'],
 ['hHello,'],
 ['jaaaaAAAAeBBBCCtoday?og.hCg.'],
 ['Th!s 1s @ str!ng w!th numb3Hello, how e you totokday?jklmnoprstuvwxyzzzzzzzzday?rs, '
  'punctuat,!oHellnumb3rs,on, and var!ous caps.'],
 ['The quick brown ox jumps over the  lazy dog.h'],
 ['tokday?jkxkfHeZTldAEIOUaeHlmnoprstuvxwxyzzzzzzzz'],
 ['gefghredog.hday?'],
 ['aaaaAAAAABBBCCCdddDElazzyaoog.EE!'],
 ['Hello,  hh  tare you tod?'],
 ['dog.hoAEIOUaeHello worlaaaaAAdDEEEE!dd!iouqwuick'],
 ['str!ngctuat,!oHellon,'],
 ['xXyjcYzZwntare'],
 ['The qexamplle@example.comuick brown foxw!!hy g'],
 ['eThe'],
 ['caps.efghijklmnTh!szy'],
 ['aaexamDEE!'],
 ['trstuvwxHello world!yzzztzzzzz'],
 ['w!hthAEEIOUaeHelHlo'],
 ['qexamplle@example.comuick']]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-pM}Il3)9vTccF3e4;ZMF$*(L(7g(K>4N44p5@>#K-<}43Aj8Ujt6u8xen;v-'
    b'eu=fZ4P;0W1DL|BwIQ|M|cD@Bf?s`hWe;|L6bsKmOnUcaORJ&;Rj%)iQg@r{_EFvwK|i-'
    b'f50lYd)>aGfKWzp3iJ+jQZr3`V~%^=NaQ3XaCRt@BjS2|M&m#f3;mgE^)QdpH${mPOc-ar{}B8oa?pjnre-'
    b'0k5yMFb@!3eb=|w~b;kMc$HWnz9%k$-'
    b'q#bA4JNTXDJbYw++MUDNJBG1xyjR;h$IgfKk)FG)5dQly|LUc3sq4CSJkK+E(7E`BP)E9-'
    b'ny*;qxLb^4rz>2k_WOEr4$pO8rQCbf^KU<9KJiJFPY7W=_a15X)>FP}Ib+RwuJA-Yys~)nIc+|7ekQLJc;CD9^xuyO_ed#R<2fwC'
    b'%{o16=I*lg8m>P39#4&Dma=OIDaE|+%toygSG;@w@5f{ol}Cv8eec8HrB+s|t?lO-'
    b'&sA0|Ji&VMVNH3%)=KL+_ls``DWCP<k2!aI;>F(Fbua#pO>HgTtDjSLs_VoR_?mon$(irG?pWJ3v7K5*Sig@+r_|9-'
    b'pKfzu+fQljIpcYFiRYXguGo2@xvsH$TirL?E!=Yi9{u_4R1Ih58Cq&%w_QsMtRUaWLY8y-'
    b'E~~aYug;t15LSL%9SmsmC0CojwF%FB+QJ}nxz07$TKqjbwo9#7XuY$GuOnP}gc|entazREgceu2;(tG;?7dduFLv&C<H1ttJF}Nz'
    b')y*2E71=U2{V8YGHCvr2RGuw7cfZE?@5fyE)-W)yGRo=edY)4=n{thKaMW}6yVrQFz%sW!S-'
    b'xwtI)gvL5Pm*&pNGY*<%#LssnxhPi(GI1Io5RTbFr@Y*F4z6#4NB#tc-;iyxhwF{g_qmv2e0APit4MB?dPC!2wH4p^sUvXXg~-'
    b'b(eUzf+3`mCx&tHmHB6W<I1INJS(<qU8hCY37dQPvJy{@p*$Bm_8%<ar^@c-'
    b'DsilUmp%3OG5Zd8EH@5t;V+Y&20Q936N8!9(!c<2{NTP%XzcK*Gh(2jv!JVdu=O1LCf6A6hYuW2;;}Fh9%amP<BGke6HWwVP6U)f'
    b'&pYqUYNv@w{amx$W$}v<qdX}mJ_(#lSZum`>OF<{)ZOstJDpKW!t*P}HUi(rZ~pgV`sDTRkoeIH1WC89vDir<rlzN|t1DIvG`Zy^'
    b'oP!xWEM~piZ1Xce_Ib~z$AqWVtImq4mepf;aJF+;>s0W$KHRT%u~PUdaB#1u&Fg$G)$hWJ#w#|F_v+6bBdfQcd*Glv8_v(ltn~Cd'
    b'_8fTOa@8GE)IEN7(?P;r#@%twk~Ytgc%}d*g|JKN^NJ_NgA?c><vAG4;%BcI@!rohYo6n}Lb~qo1Ryl#UMp`_s_V6D-'
    b'VduCeayha;O#eSQwG+<u9e@%q<B~UcCY8Y(ny$kyiacI|3ygI>A|oTn}^r!v3Z{{A}`F(V*%xd#SajivGlnB15p2@xYv~)zAlt&_'
    b'5mcMM4+l}c4_MnBM73gV;}6vw^KMlx=*=S8H_eBto01OdSgaAXOK1S`oy`qjz=g?;|{o7IxF12j{#Z|z&p;(HtvYMT|LysPlgLLW'
    b'=q?;XBn(s0jj{UcI#6(1ltjQc!T-'
    b'IJ8$s569zWFv*QIyHl7J^CWaddb_6N_uub@0rHpprCzCb$xn`(1S?V!Xc9S1GonJkHV05;BbW)vDGh)L5V8YhvL_LfT>#Ozt!4`q'
    b'1;)wipKBLXjAHT9M(6!bFA0`rx1Pc(E>mp$F36>0u@ybv5w~-;%D+2)Oq;#cR4|ZQCA@BjR3D-'
    b'bYy36Lv1!oo;4=)p<wgWV(Js*fd8a8j+38^8ERVIGRV+<$~O8{8JwX{k+5+r2dA!dmm-FIIn|DxvRRdHFi3MblaROk@!&Ca&8`+W'
    b'AP1M}Wt;SR7UBk4_eD7a6Y`v(-'
    b'T7W}Vaz0blov9pIIC#>ZL^4zE8d^ZSIO9KmLQ`bG_6MEVgpOb$ZPNc5<`%aka352}do(mxKfg)Z4JY}Hf!L6@0Vi|G9z*@0<DFU%'
    b'S^V6&I=qG|j29o<8g-'
    b't2IV7P%nY<v(3JBEUB6SZ1^rtpto8+P<_hQjX0(BU#?f@ymaM#luKSPa$^l2tOHrLKPQd*B;351NN4PkVkJ^ITX9Tradqpb3%Pi0'
    b'iblptss2lo-'
    b'q+050(S7{3pn&02x<4}ty1ZvdCM_Ly5PlO}|L<p5;T#@zwwjj^sfb*SCW06U(4W5sOC{Sa1uKoLj5A>%4A&om;)2~xu?fE#d}DAQ'
    b'j+8WVm%&>nn3ScCxrM`y);OcWjgNqu@30f@~|6Sz7CJqXx%Dz3s?U`IeuATmno6G)GRW3Zq3!N+&K8pwbnUYF~*asx_<6o>=>_Q@'
    b'Adv|31O^3+;Vz997A-'
    b'}pI0IQvQaZWa97GM1I)_t4A$60S5ZSV;y`Q37~3Ht~$>xe}2Wq7r{t4EFhjP)A%G!NAsxTmWRSfUky|5D*qonGFP|(gTko)Z7&Ug'
    b'kSwW#-'
    b'IbKCIps?s0ct_=nNbKkC=DPyVYv~)tl(QP)fdV!hcf73U~W`OpA#)c(uekvB~Tz)Fro*JJJT~%V%6StR332pABET!TrPD0a?KNZ*'
    b'9(&CEhqSf6NYtd=OS`6Db?-'
    b'1K$ILLt^V$evlUY@=YOj5xcy9=m$|D1VYquXGzwrm}?Lw_DPy@2nPTIAKS4}#2QOi;3%8W368cOPykQ?(-r)HS|rXf-fnDr-'
    b'}kC=Aq=x3Kyt%VA-&+*^#nA*)$T9&_KdSu-'
    b'<r_$KwAj?E;=?}Lc9=pd7%w<24ZoF0fbJL8iZOdbN_Z~6Z}vYh@%TG$q!<tql^KZgf#%_5<s5vh%ncRkFg7nYT)kvXc8`jjVM~~J'
    b'`rU2`9ReLXdd=+UAag6<r<-'
    b'E_$4$Hh6fTH^cM*B0Yw}Qjz|P9SS_o7;swQs#f_aujfDhRgb5ComRL`4Vl9Qsvnr^uKRt!pol^J(o)Pwk*hC1ogN5iQZ2EZ_@tT+'
    b'fAD?gwYyn(t`-;!M1qx#BliHpj0r)ksOZY$z$d76WCUVz-'
    b'0EVEUjd90;FpY$h&R;%=ji32J5kT>N!3H4UD%Osx5REYsU}!whV0;7;oNi?UK3g7aZ?QOpfY1CAK`YL(_)lYtKZ}viF&DHy7M30='
    b'%D!wE%}oGBDv#drTL37`FHWt1`**@C-'
    b'e2XJkZ+)UDOm&R28=;E!FpokBhamYeBe)jt{i?=eDlsz>exIBfitaEjv5!Dcpq5*Vf*<#7CFgOiRb_Zm=Eb;oquer6^V(!IzR%r('
    b'IwuqIM9hhw3T<?L;2Wb7C=Ne(5eIZ#$ZeSw{jl!iAKYgLPG@g8>>Js-'
    b'h}^*LN7d~TnVm5a5m8S;lLTDhNsv4o!^8RU_?++h|pGx5n*eO9#Fs@M<#Fr2p0~(6Qrg#y?c%wOhj&+k6yz?+fcU|8FRyd&V$(=b'
    b'mMqhzu^<S_{zkyyP=F>BuHtZGokJLKBmAj2nPkxJz+OkC-UvaC?Q~vcyUT53ciOt4W4@;j{vyc6+V2+zXef(=rZ6%cw0qe6kHi&g'
    b'JvZ>Dd>QSO}lEZEd-'
    b'o)f;opLhL#kf+dtlL{(PWH^1@7^pP&KclSt2=rF3KTc<Dx+J>XR+kSP9s0b6YMn)wG?;9&>5dD};Bcr{5M^ld0XkeP_0eIbhY-'
    b'3y*hV8F&;IS0TYs(-`;Fo0<F3XNXp!T(<C;xizU$VZlLA+90Am#~lQgdV_KpqqtvINxa!a%)UaWQaduUlXEy6>Jb|MMHGY0-'
    b'hqtB1~V1>H}}?NRnox_<<-f6)0SwRcHm-QUC%15lpgz5y)=B1RP`bfVcGPnQS*=@*uZboay&5C!^AMQhq_o!8-'
    b'B&Mz`70gZe)Uev2H&hCLSJ8$-'
    b'Q8HLRN@YCrA=T*9WFtqcIFQCvg_kNfg_(#9*T#4As&7U`W>wtX_1noU3<{amv{z4?0BaoRY*K!8D}Vr664;VU4(5c-'
    b'k$z7d&=pUQ$LG#+(P_7BqGg;3|{Pe!N-wme}{XR*i-'
    b'8w?45z@u>j$O2Egc(jYJio9va?c>G7A9fg>6^XrafCny${O}|wYeINb%o8>vK}rW&aT7h>t>TscEfruzz&d~$;UDmHUX4&J^}mqj'
    b'4+;Sd;;(tmOhir|Xw(b)*fAh2em?a;gOhO|Dh=iB#z&%40=tOoknE|y69VtTyDmVCpU1%}bn@9hNZ*7p9HFVJud1_P<d6{=Udxf?'
    b'R>Ka&E=D|AZY14&<8Di=_wS`J`n?_x_wm67P%rc!nB3TH{0gXG+c0ow8Zd<4O;}IFjHYaQ{&tE@WmhvaZ|Ed5ly(;M;sWObN-6-'
    b'n5cOSvshh9ttwKvL&!7*s{k>EXwbim9C1G<yvcr`x1e7s)@LUL590jx<k!a|;%?kp!Vej7s0X)bPPuOwHC~aIEhQ?!q=K(23cnt('
    b'6wjETgUS_aW(L)HRXE+~AC!p5SD;@`nuPnm2N2q0?xB+#53hP7)+>nI|zVJ*@jfm%uu%X>Q3K=~$gbwmWt+N6MJ!l8|8&;J2vk3('
    b'}Do_Mu5Z|tj_gugd`eK&yqXHoL5*#YF{y^P24m^s7ZfF4ZZSlegwo9@EAm0z17=1ATi|207$NgAOj}Iz<1B4yu-WXLTQ($<&72FV'
    b'!7670`$iurrmG&5W+5R8i;2H_dF?pj2=-)s9ENL%;{{s`Pi74+OU^H+8`}pK4D-'
    b'+hMvhOp$fmFEGIdbSje4E+RJ5L~qZU?bI5W_R!#_Sjy26Wvx@fa7r-@X9TPIw3>4M0O$;i5ah#WgYn7>LQ*-'
    b'(bB|9tg$*Ac=74i{LXp5cTka*YMcynK*cF$g|tf9r-'
    b'i;G57aS=6FImASGQKjd>N6X88_!Z{iz*3pxma0X4?H?h`898GmdZavazmfe*6BO0k7J7tCXOh<5Hjk;smqLXX-XPv8^LPJ|e&3k}'
    b'-{)?f~Lj%ZtnFb~E(L6p7RiJxn34|ihqLXh}I)P;jo18?WyP-&^6X^E&r-'
    b'pW2*NYDpO4gs5J;XD3YSymvw9<u{A>=W$z9&jAc=7wD4e5Smb;EzQSa(bAhE#Md}KXA7CdzwAx6Y)pZ_}(FJVge@7u2mp@&+XX>u'
    b'M`CMLV$zf@5j?k0znw@6VSjLA++Q3fe!(JD_DWm5$+Of9QA^jimTTR564!n2VkE7It$=Y({HDUTAPT{7mOjpKK>(>@E7>xjk~fEg'
    b'hQ6B*F5elhV^rm8}tKEzdM+$_VMttR***HFY~mriFFSw`XyUfis$jJV8_sIlntm0DBZu{+X+1wLrfP$GAw{VuEUCAX`pgBUP`fE6'
    b'SzAm>jFh{&$tWz^AkcS^?rrgJ^xW?NghspJW#tmh#rCW0;Y4}w?UPv4!r`<MU;V1eX<Ph%FB$71MwmrOg|MmR0*BfFt5?xLkmJ{x'
    b'T6O!6D>RW4dP7v)Ln)h5}Xia0dJqU3(^5s09RKhK7b)!eezxfHv{^%XZs0Th#9i{i{UG+2Zhk*bf5Shz8>OC$Vo|~;|r2DeV6Q^I'
    b'>?A42YCM|rRLw-V5UI&zNGaY3WwTag{sSJJCL~Y#eQQZxOJBy@#&btI2V$K-'
    b'Tm1O&@Js`BRl~fbrP;?gzyjwV6hD*M<m1<A=<>xdtPtU3cMk9@!k1);RbWY-cP+ZQ4{lOPg7Z7^$nIZp}%eo(uyC10&K6I8(}1VI'
    b'^5ms0E)6yd}G&GLIMqpkjKB$<8i|Uv_i~B@bD}wuMS|?V|}s=8^$1cZ&;P2dS>`oBQj2}djTL|ivWIuW<2FQo{bMw7d)!?#y?2U2'
    b'6QZSLP_~D<UWtnwl{%Z{O5vrS>CQ($R03$KftFKg`ni!e&z=N;LimlQM@B((9lVew}`lr=m0vcjnK#I(4Hs^BI0Imd1uz)r(isV<'
    b'5$)I00cP%EqIhBKC}WPALZT$Fs_6lplucjdJZs_3lO^Izs+3uN6z3`bqL!ti3~CV6QCzn_dw<^Xi{hAP!Z~9RINf9>4=<sHlzzq`'
    b'7zN1lgXWj4ty2vZs?sNA+mt=?n783a=nLvh)too-'
    b'jFza<9vDwGoC=^b0g*t5x5YhCmat!J&_q9fX)>z+>z8z@KT%|M}r~$Is*O&>BM$X5rhh$F){2xTM-Zs1OgpGAX#kxQ_KBafG1jv|'
    b'7c><gc*L<qr61){1x7O8QvdaBP5t$qhOjS5du3QU_WpyjDqJTav*88H{d_g#s^jpl8InN$$EJ@eM5qH+shL`6(-!Be-'
    b'V}8gX~@L%!~m2Jl`=8Olq&=0R(UA6&*^(!-'
    b'qSgoB7&^%xL8T&F?lQp$|+88Zs0Qn42FHy>nzc&@|w|eS2greP!FhmFtl%;`ujlgc(#;CkII=jO=(q^QEe^+BG|5E8-'
    b'AB&(`rz1ZY@keecLJOyv}XS-k#pEO~)U(5KRWR{Rj2T#si|{t2~$fcA2n#{w&qE}#!ghv$L?8KEyPj)-'
    b'Vb^7tLRKzYy;OX?0&1wb+Zt003eV&18Q@fD#&I5yzh`vuzoX82x+DSz-'
    b'|Tf^Lp8>^LaZXT52NT>h|F<_z}5d&Yv1&D@7tm`3gz=`L>Cqj9DR!msv&_RScO9!{sWb1<z-'
    b'm{*PiT!}(dq_5kf}V(A51uNg@k*Ib2xT}K?1)_eBgzd^jMyiN3?eDpm+*NF&Ptpsf)21GOmgoEqx`TKsihUahAC^<^-'
    b'ghkl})^5k-'
    b'csr1i;ANL%lE`P@XtZZ!zt=gMqnR19N<QVnP(V9lWk1(q!N!AfrP=NNv+R2F|g~feA>MA(i~(yjLekTpnV@b4Q@yMsVQNaACG&<6'
    b'Urd6nS~iJH(0Hfw3pMC;ygF{3Esnkev2pU{SS!uxIh&=68UE0m6DkoZy+)E3ZJmj+5>ECYU7T+^6mig1z&T7t|3Uol*PX`jOj0qw'
    b'j?<CqN7&9<FiffPpLi*5SLp)1>#4AN0q7YZCbnkrB`2dvL!8H%&Qu{A|XTXX0Uc9C=cRSjbL4%`i<mLdzZKA7%l>L;`211VMHc^M'
    b'%|TU*)s|E%dGc^up&FbaAb}^BeGL^8~m8%Y+ss99+6xZQVS<)sYA$74Z>}R;-'
    b'TI^W+KG8RrLE@CI=0W~B@NR1Zo8RRR27X{JJGV96$*N5~9|Cx9yPB*m!y<S>6UX#;-'
    b'zY~p9HW)50h9>E%<8&3w^@4bP$+oXg6+ba-YFS)}}z<=35$;=`C9AN?PyOCYqfeQ?m!461eWdiXLE$$g{$M=Kq_ykwzBW<XLg=ev'
    b'rBThn$@da<fkt%DsU#<jG3dl=HJLnOKbnCrC01&?z{=@(VsF6I0#Tg2a83J*541yCHgeQLLgU6#uaHvKYLV18qIenQ@2{pAKMB7Y'
    b'|2`vWFd?@~)l<d((?eIxLmrhIg;F;=$+XE))@6MO7=~IJvbu42*M$DOwhjdSEX0gZIvk?j3F`?xrVjX}BDE{&76l-'
    b'wf&=56qs%m)ieqvO1vQ~A%H##gUgTgU+FYZ|;3^gJ`=9hAilc`#>80)&P(+J}S2=|oWHm8tywI{F@%!q6cpKWl2E7jJ%Ln$QFvpn'
    b'q14@e0g_BO_hKCJq}qS%f1m_9?YFv;LG;ED;^kExydQ+N2Zx1#Wpn+G5|fezDMxTM=i)a$xD(&Kmi_sR*pGM9kme*nXuPno5+W;#'
    b'5fcK{v3MQ~&JnZ1LAP5tS3I+Gs2kS&F4ZDj)>mVO^I`i6`qf0y_f0dMr(gN0ybP(QX~$wf=M6H2k|wdd_YafEoljlZYyK&14kVhU'
    b'ZuC+NXSq5XH{Q~P6bBM%_TLd(~ay#AOAu3*Z=&%*<xtb|(?1PzZS3@)fw0x%8cv$91S{Z!ffsgiF*Y5wY(&y_y1j|>N>*qf=B@P)'
    b'YNQl7$PZx0FEJ~IB?c@I7TIW(XI4dL+IEq-'
    b'|vEg3R5)UOfwJyPSNSQ+pN7`<;#&#GruJ9vQu2YepyjQV5p$9KukD?c~*yxYowc)v_e;(tI+JZ>B)%)E%1gmSMePrb5NKd8jfS&-'
    b'jOK~KF3E$9LW9|(z=5w75kA<2-o*H#@00Ih-MHm`iVL{613^<797ARBcP@DFI<6{ae(6t6!LF_HlMs<F$PrsYaQz9(T27KM77zo&'
    b'uh!ReFPl4!g<pdbf>j+Nac=scjs@lHH>fjj}y2fa0+U4g*Uo*$%N-'
    b'p^i_nSLlMD1Up9qXcl`76|l|#Vf6bhGHi>ezygQY&PiQE&0#<07|b<`%ZTc)ey}V978tY0xEge;88y0`YLa}7Tg*l-'
    b'|;Zs`3LDYUxk8dZ9-kmT0u^;nRRrii09Fu3>LG^+D32%JOE0VtBH8PTK%p^i)Yh7ukr)`8d@r5Ux@9E<pc)-'
    b'n7G^MBlF~DL>$5l*ni;jU%nrXX=W_sHGA<?p7*4vVXo{l1Q<nGF#;lIGG+3XkRSq}PV8U$v?i(tp;}Hl@I_t$chTm}*o3mOC}`7y'
    b's4o~DAvvjz7g(RYG5p0Tg#6_j<OmuYF9U=IWv-kDguRY$CMU7mn6p8!UJ%^qwKU=U_fqRI>A-_q9->1|wi$Y+Fiqk#%Q-'
    b'uO_O%8U16MD=Iw6ZC+~!k!=YHsZC4$<f$|Cr83@{tqr)VNX=4N7T@feexBdmw<n0*Z@eo2hz+J?-'
    b';3YH<mtc3|ILv1c#HNzc2K4hNvgW2?)`T(WU2iWh&wg%`l%xukN`3c>m3SJSc!V_y7dTv8L9L<4E2WFI9o{B&Bm$$_$UfGQAUfs*'
    b'n){aQT%j4G}>%-'
    b'!~#+KQJo!1rF?f2HVdd%`&kB&t!7}8>X!E|2l!8)qhOWr_8@O}f+eg30$!PvuI!lv01c;Ng__Tj_kG@TW1P0U2@);%S_Wcc-Ut_G'
    b'mOoIDvVh~~YEr>+N<@?B(mZB^i8^@0&X3(}3Qg(?xU3zYC7xD0TpCogp?k#xQ>V;T;L)!&U!lpesxPw?jW!3_CI?@}QwH3K6kjT?'
    b'`<OqLcq0agMXY#++;?C(O7KgOlg5w2v+U_6ElLy3f1F94^P2qq%2zRNNWkOe+vA;p(CLtN`!KhVm&j5QMnogO`oG2N=KIib?Y>VU'
    b'a{X@ERPZkET~>EEu68EgEnJTb~HT`>7H6a{IKB;wAyn$~(2K1sw+1APWcqjGBej-4T|;7Z10GO-li<5f*JKY(W<G(Beb7_-'
    b'n}NPWl@;+xNi5xEE${XPb$<5wH{-'
    b'#eZGVqz+2u!xFa<vkYwG%CAz;c)OWxdq;2DFr|9QOL6&FGfWyY?*ywBSt#<)I&JfaIDTB*2rE12hmKw8m4EQ`^)IPvE4qDh#q5tL'
    b'lA(J3@EqQIU(uD2BKUrw-;6bvPLMO<r*-'
    b'8FQGh1L~+bI_#Lp%=fBlL$kzL|zyO_SGP6l<f=xFM$3uRCX8X$(h`E{HZ^A{w2n!g<yWN;hIvr8ubqdHC2U6o4lU6ZvJ}_;7<+~9'
    b'g5EPUPMsvL>C8r1rokc;{gzT}*dJ}SCp{DDuD<sSj&H&^6@Mc4)pN^7*@?Ro?IWDQxG<P+LWy58>TK87a3Kc*snn6IstZ<Ew`&G='
    b'8S13>fj2@%%`W&`1hK#>8k9M|K*jIpj=jV9*0Vi04|48BEH#c$#8<;%Sk<NJeowjKT%jBr0Py_g(Z^U2#;H(+UBt`;+j|%XOR;v_'
    b'b4|qS%qc}k?o?@^!CVS7lQW!l+riiiGFi@W7+PR0ns~pzi>iozVI}+p}Go`;mJe!j?SvGbqK}h-8I(-'
    b'bb1zf;~zoU+leL6^529_E$fH-'
    b'3~z`aeQ;Kv7;u%Bv%beBZ;h&Civ5Z15s+bKTKTB2eeTmV(fpaf>NDbL+}qN_L0&b>|qaIANDGStg^7--'
    b'9P1I_n>;8)btpfosUint*UG-hyRYUfji<i}vk9+<p6!8gGEe2}hUU<K}jtCe^Lk;<HVC=!gz1g-{x5;5<PyjR=^T<_?&;R+)4X-'
    b'&2hE`UC^j1B8s1SZ6K-'
    b'5HQL&5M#20afB)ZLlsjh#!W}cA)3e;T!!2k3jDgkHKze|1cGAEzGW!(%7}6^enemzSAnB6Cv|kCmMhGH^uw+2C7`1*;uy&XY(rNE'
    b'v0F4W`Z#<iXK5?^N{U1s8Ja6m*Rx(f%%Q6nr8#hdRBV@Evs8O(oH6s4;o3vb09Syf_W+<y@S#J%+G8<;t~690oY@X?0^K6?s*ci9'
    b'S<TNUNF!{xv_CCGvP<uNY9XeLg+EaL=uYcpLI7F860o2%i;33YCr0;b6K8+!J7m#qR0-'
    b'4J#l=MZWqcE^`$yQ7j!R>2RiL4#Eb&DMK%LCCWdEI;41<bhb8=h()AyorT-(XDgQEZY&kaQzKOFSg(-'
    b'L51#c+TLSH`*0)0t&H!*Mr=qreOz9lYjU<d$krwB!LJ%p_ICSIU8;M|s6KqLby0RHua5Q$K0r?k%GAAjaos!FtVD}bH>7lRk$P72'
    b'a#9o}s{3|0dyPDEtXMb<;Kejdc|ck2;Qe7KX9o)`lH9d(F%h9{f8X86ko5$#>~0G2ik{jg;bWdbw&3N87~8G9sDvEg35&2inRR6L'
    b'95dd6iDPa-Jv(M+FWSCgI#KHoh3&u+RU6O$lkQs>PV=Ve|AAAAc`YurbuUZ}p9QAn&6X!)4n^Pup*;-'
    b'1t{ZX?|{FbTXG^dMT(qp@nX6+~y7$GckhwA|}y*%!<95KX@&W+RRa+Y*=+$|GvEG)F))UeKQA;Q$!=wC!Di#2T{Y-'
    b'4v?qhd1NdqKhdC7&1`{x(&)-'
    b'*#ba9*6f!1AbUC+?!6NN85SM@M11i(27;74cLGpU9@(`2j<cg1w;^dxXj6;kX@Pshuxcu6fx+<=YZ14<Bu1!AZ(bZ>#&{zyy(~Y0'
    b'*&n0w0m(cnuGu_}3~RN{OK#bK$gg5)0@I_Itz|s~X3XC`CC_H5Zuas9ai6V;=x=rQi29dxuW07|=Tj|SJ3v|D1xLS=^{niecM|Z}'
    b'j^>;~DzCC-qSIS1mhG~zIp04J%@={k(-'
    b'~G8_Exh;43ItODxUfvdGTFDB>ERE28}|7MrrXtq~eJG_Cm6nte9{9v%ukjI!L3bU)Imwl6zvW<RW=gj|(8r!T!aQ7=*tpG8p_6B2'
    b'h_%ixRh&viAn-9_`JQnK)*}&#PbcSm#S50l$#0-'
    b'w7=tq;3{5Hbm%y07j}_03`7xhY?xh=PDiZWQo~q50bH@dZWrAXtRHIgSfD0w|c1Mp{chM$iVL91gi=ov}(5##h3Nt5Mc8%P0XzIu'
    b'Pox<2%%tx?10}ZW5)zEbG06gV2Lzua8vIg`xU0u)F#xh3GBr4Sg05KcS0MHNcBV<35eXR$pr?1hpg49i)aPsh0yf_0FH<`A&%oz('
    b'V)Y>;Jd8{UC=y_^AAiAsfY#{7nJP@R|)X|cp#*u%n`IwWI>47NM!Vvn-oCeluh_(6@AM4%)GtSG8c(OdtiE&`GDh|b?nLS!lf;VA'
    b'vBgR|Hdm+0xOS!kt0Hyde>@&Vx=tF?z&|VlGSL9STOTxdRq@W8Gkj214ad%Iu;gP2|B=!1odzQ`jJ$#7?TfhR8Rzk80AS@a%sMg`'
    b'A4_&4?=<m^0*tnU1z*Csv}HqQfJeCuyV{|AsPxY>VEH+R9yG7_IIyoenWZKE7(~~t@Ho9wCAV*PBVWV^y>943Vq(kdh=`nh=*q1>'
    b'GeOluF&&Qw8wMgxUO8s7#{a3GO;Jr90&udKHdtLhiWVXEWoIQ4FBN`G{K{}X4XZPT|kiTw*vh3G`!hfgD5rHjjIBco{IAyNCDKu_'
    b'{=Y@kmYt79E$ArCKIOg<~&ZYyqM7eDr{?dVD#Sb<9+9PD-52mf&fhyAG{90!{DK7`LNP}|K`Q=zJZ<qAG<vhf7p!pmiob-'
    b'?IEx}?q`yYkMvegfg=$S&jTZ}69U#yap8oflzEE_0L76lGpR_BxV}>AD4+MnXQQ<Nqvp-pu@(y=!a}i=!(;Gj_M6AQ>>)-'
    b'3hC=)Q@+iDycKZTojOY%g=&!tqmJQGz^MtE<B6tzLk&D$jRJcXEd7SfU22<BtBG6%17P-'
    b'&27JBk8y#6|?43Fxq$3siO#fYcD)&*f$<oT&P(4I&--eRBtY$Jf@)xBzk;#af4FDw_)d6_f7L%p)tCkJ}^{H`l-'
    b'6Sx68Xv+|f7i`FIp&ZkHj`H%pJZC^YBV5qBiKlIM^qL6KJU-'
    b'0;v(Fa8^Nn4#AEI!MtsNLzh9=(|k!tp|g=L<?5>i)sOpX3T;(Tx1Av{1j%mN9)M{Em}D)trB5pVAWv}|Y{ep4q_Lj)u$7O46!GIV'
    b')#LhrnJ4kP1n6T}8RAO<VL%uKq2<c1dNd|)MLX{;lfiEx)MQLi;n0VV<6LUBbLZdp)S7F2d%VzGO_jh$qD#U-'
    b'fC)(SAZdi{t=83)GtW^{nGsF?R)0|-T-s__f|1$4+3O!DME;c~mZS1qUI?<~FB#--_L6Dbkg<-'
    b'UtqwHETju+z3li{&|+&zfxFV;y-23ZCEEU>ZcqH$ypjXwum$xD+bKbau80J_1Y!oYSy-YI<gbhFbwwdFd~4W@&&0t7+XPC6;WeJ{'
    b'~WoBieVp^-GN?fOGJd-'
    b'K`xs|F!Nfk0N?DXx$o`Ls@S<uBTZq7ws1t@Or4N8S;)%@rHC`bzm8H|Lg{^F|!1!nA@}LJTh<GyIUT1Eeo|R?x_|4mtjsYLC{Oig'
    b'$)rLe%$W{0thR?WWiw}10tIc4fBOeR4=i;_u9?VO8{0$;M!P$c@dC*af)b>AQANzz*93koXE$Rc?qERX4yHWb1#pga|?JivIIS&q'
    b'WN-@kQe4x;kV_wjYm&1*4xh}-jEtp7TOX-9af3VV@0LMp8FQWK3+W6D#<G_Gdq!mE8S59v;;9C<>x6LQ-'
    b'C;EBqm~=8IB(;JZW=Xf81|^Ku{CB$vb15z`Gx?kU)unK_iI7{h+Fv6~hSeZB7NsN>TJ3E-a~5g_#I}8hH-gf?|ANdSy^H1oI)5+;'
    b'2d~$|U3-vGP=-eZg0L*{=bZCtFB0L|gBbt-;-hDgQY)&Qei?gLP=OZ~^Hb;Qc!W3h-'
    b'|j%vrcZD)kl~AsnwrzyY8?_$|2SwG*txU<{YSH1Ee8(l0L^N{#Nrym>Rc9DGz|x3?w0AfzK+r|qwn$>Bqx5+QE_Y*IY@SUT}^6D)'
    b'AMYHCyPRQ}!=M)C6c1{YDDgeo2-vL-93V6MA2E2j3ReC-GnEbnem4>M7rDumxeI05>0d_;$OsW~mZxnZT%OQT@j(O+{G4;7(|_Ei'
    b'|TGvpr>=96yL^({(b(O9faAihkj4Hjg1x>>z~|9uQb+PbA#Z+YW>ycH<V@el!m=6MVe5|`BcA%V!p$MmhRq~2(spA}#739xktIS8'
    b'eg?;BNfyP>Apn{Et8muPK14J5S732^*WRL18FELPc)q>2Rej$0wcmIM_3$p{WJR@%J8u@KGrFjpTAp5Ue*zxhY0xI8m!*lg?qQL+'
    b'NUS|QKch|mJ}ZPzsKN*m$)YD7R5v+mk1e&z3_u<f_uQY_MQ-siGl!K1eJ9>Ws*qEWI&dqjZv$oXV0?ql`$$F^W5=C4fo;(dDsA0C'
    b'VcLT+yGFnzc4;ZForpNo)+nBcErX>3>hE|$hLffL522Dt2wae0Vkru6cn_?XK5S{oa9@#<i5XXk)<%bY*+YuL$S97H1%&CQn|Qc-'
    b'*-mN)Y+J^h&%Qj@42F+*I;1fRF`^WWyQrD_csVc@P8&oXbXg@N$~r!M?Aws}hx<};erd<1-'
    b'A)lP2{t{n4c#VIJtP|0>+yI9V!IyBBKBq;vD^l=O1`whn?5`#L@Gg#;3qrZ~a!uw`uF!Z$LyIEasUm<DmK%U`f#4Pyw={DXt-'
    b'm6{aNfJh}(64?9a#3D10c!I&R*$jB0Z`rpTUZC5zpZ0pX~vsqd?#-'
    b'ch##=D>&rfT)8?lKa|>Ds;Fl6z3OI<#Oyg}%H3^6FzRU=OC%aw)W8YuhU4T-'
    b'jY+B7dao|f2Dhq)EFtGTh?l$c2EOZv^Jz0TdS~UFUO7+Y43x>DLZgd`%M`SPV**0;`T5gCdg3G#=WlG?_&^f~vIS3B~?)cDeAhfa'
    b'L292#(<$KmqYtFZQ01J!uY|@sFut8Ff2V%VJ?M58S{Y(AFeF@KdDhw`!#)8MfC6fnRgbL#I;e&{z#8sQlC6g(3xvXou>X%0WGQ{Z'
    b'(T1m^}Zel023kp5A*&dnrWB-Q^)v&UnTDU3kw<Uwcyx$U|0;?SbJy%`k;oIp8BJ>tUPt5t+z8G2;+~Nrk25-'
    b'XB0P6c!_>`_OA>7APwxm<v)7~Ahn%oIga0zAJ<pn3Uw=K3hPk4x~;r^=;nx+TXqY3o%=EE!Z>#ZM*0zx=5VXi<3vDkC2BtwQLRxc'
    b'LjU&hPR*X^|w%)wh@MJDJ)3^h_`=#yRbk~PN@CHi<qUf$&&@ha`F+u&s$bz|}GTGjf{qKqWi9ZU$kh05ACdktuW71+H3dQyXZ6XI'
    b'8S(tOH$d%TDGvAt4w!n8^aFVyj^9&PWTmznDi3-'
    b'0v;9|^ho8cAGU%>?W0OS)N)&R=WJXCbi~oXBm$i$FklyOq?uV;HJdNYvMFt0TnwCg`G6F{jRZp#)(L;qCJBp7~u?NiP-Ddo5CN;p'
    b'<@8H^lrG?((s7+5-!C>{-'
    b'@c_DTrni?>}W;5krIxNUliWS?X*ZHi`r#lOBusoH?US21nyR9io7&*nPf+2nXl*?tGH$6*7LIL5|nuW?s^e*D|uYXQZ@X4M8;hDY'
    b'K~_VD7tv7=_AIP<NF2PfAu#n-!CGtbT-'
    b'!hJr)O0c=Xj+yq8Lm1jla$<MggD3A^Lq&*0RZOuy)T{<GZKf@x&c99nLWP;v4O4%t31NS3I}O+(k$5{n2>!W3Ej{<D4=NTz0Ho@x'
    b'@V@E_z!$cFH)LDHRn;_hY+;BQ2c9t`3+2tG+IE#Z#TF(&^G1ctzlH!eiw++_OqzO2oPzC_3ryWN;bD1^e4hlCnLoxB&$klfv1t|d'
    b'@X0c@;oB^Vw;(#0L2M@ugvba;P~0cKNz#{X>5#6Tp90MMAwK&ZAI?Mwz&t$(c&>G@Lmmfp&{>&k$|FI!d0w0Lbr%c%A*Bz`3k$4$'
    b'{Gs255`#uqVJ?@F4ci?sGvbcOouEhaVdc*apG82zSCNNVYWhd^k+$pd`qtcCN&QVAhG~K{cI`4UCH~q2dT@<sY-K*-58?IHFZJK-'
    b'b)n9_XGFwm_5w@*QcI-S_R94h>|i3+mcp5y-R(sgp1dvsz|V>$z}<Rxo5Ao{yL)?|md7i%mVsxnNcMT-f51IYfzm^+iKW-KHtg%$'
    b'X?3blK+CtID&pelIJkX<fY&z*L3F64z9+_Q4>NxLm*y<!rUFgENMM_UR45YE)|NEU^4WprEMCo5i4WglyU8bB9^(T@U!mncN^i$>'
    b'?HM|3WaNDjFMzVDLLSCjHgU#-pQ0j!60n01?n@=*amruyXu=`~e{>Fbd#%;2p|za-'
    b'!cq(fCgt3tdx`#dnFDo6)od5ryXLR|4Il3{S3s}cZw(sc8|`!u^A=RtM>L`Pu4%6{FPexxJYv)i%SYNaYCFAwq}hBazh|vr;MzD*'
    b'+!mbknm1tlhGABjN5buu*a)lN62Fq#?0RuG*`wH^o`PC<Y{+A`G$5MwM`W>U^|oi<x(=+;tm-'
    b'eom<DR671j^-iGT(VZM1@|BksNF^4QXTtk7l<yItNRjF1BH=KR~rld{))XRrYt^YjH<J6#4|9yZ-BdrPH207q42*8hH^9^tD=K)!'
    b'HS)*78<MSP&g{*wuBPVU&zCxAN+^b<H?7t!>fW1c&EN)Cu$9~N5&Z*dn(3H9+pWIQ%w^ZLe)&M5aFIzrX5eTvZA=RJk9K@wp7owQ'
    b'k%2J87x&TD(DdWrA-'
    b'ar6EVAore~UqBM|+WAMXnOnA`rOdAlGV;CIzpv=f*xzh#Uo9kxAJOtul$fJ#m*04!FiSNFr`-eQb$@*!M?rgc77sb*Mf1)AQ-xLV'
    b'a!8=Zo1bV}2O-rGdtiGJ24PUB#;=@aUnuka-b8!R1F;D90pasnw2F@?12f3PzbqOM0zC~i1-'
    b'tLBP2knNG9)gpX>yFs$Lw%`!nHwj5s6?lXgAZnaA~P#>1KyNxb(;Uun`aWlD!Q0`e&O4&q7pdtn-'
    b'5EhBZ8hv7ajlegCJVEl(?}({}?6|Lk_Lw2|vl&BIP^umv};KO|zsQ+Zw^zI`H+0%(|-'
    b'Z}+zR^%V$p7`#ny*vhpy?_~9T25v2vy6ltMFVCHCWyEC$C*(01KCVysh6M|$K=EY*#-'
    b'xiPF`)xWce`oW3o}`U(9vS3>cD!V9_M@h`FZ%ilJgm0;OVf9w@|9t_{NOGmnEH(RfqQP@?r)Kw5IVnjex+I&-'
    b'E3|RY+UKe{4Mg9e*TcZ#vjYXlJDrk0A{+kv!eV2CK@RslJ-u)1duqeF~$7J=%8MrW9jz?;{(*sT~+Bu_-'
    b'`;(84y*MKmCph+>6!^<8tN;TmF9wpHPWF)|#~E=U;{vg`+m2zGfJZU5il4Zbzp_NZ820SoVVdEHivJ#L~0Sh-mlxQKqc`}bBr5mp'
    b'dI+Kb|M#Q~~8AigCAj56lUi=K(Sv<qhP9_3DZfmOSYuwq2$W{+aD=YpFN5!u@IH4)>3ue0N0gQ{(QCt9nYH-$6c<T(RY+v3-'
    b'7`N3>v)@6v}Y}Nj*07EyA;j)6r4B2WMKVB@{u>tkX%OL`U9bM2ZtdK>H_ie{KJZ06t7>*7^-+-'
    b'Ogv3ds0?@aA9LGlmWmA&0Q?19~a=k-95Vy;-'
    b'l^%Xv)X!cw}YTH%&KV4qCP0}!qYR#584~UTmMTmhTx9l_939<HA{t{>QHEplueO`#T!8|W$nT*4}t9GGosppWrXM?dqVU|6C(N~b'
    b'X@9qw-M_{b?EO&2gIrMFI!!ex@9J8mP^#@-3<~w8?-'
    b'lHS$Zest}TD&1}1{#RKG$J?(CxG~E6#$%JcpG<{4}I?ED$pKt#;0B2lMS{04j0@M_=efT9t>OExXi5XJQT#+qBO;f35Zx88``0P)'
    b'<k5}$i4~!AbbD?)%;7?_;v9?8QfiWtS0RevH=*&pViJ|6CH+y&QL{`d3_!Z|BOzPD4GIv$Bsbv+Yyy$(`*E6DeMC+=0{e2=|$k@6'
    b'DaywaXdsrGvDU2rWB>Z*PwQgJ^^G{n2-(MEqk!b#kehIwt-B%dH3&r>OvL_Xc=^(6{CL-TZdA7m0Zn|<|#a3K;D?AR^IR!uuB#FR'
    b'|f+~<ouq&w_T6Lhdi7uJtutNzA=x;3tR#!^aae7)dSnAV$Ak?sV59z&$b|5(?YOqL=UBXEV%}@kv~LKaAQHd*J=`C7*#SMa9n={x'
    b'~Wu;n07;V)_!9{m;_;5+HSEkJD*@XyIVPBvp|d0r`ct@{^iihrd|aAMgEUW9FM8MtaS|b$h54qqq42a@%T~l3PHJS$?^Q#mqG#xe'
    b'!+`kBA(Z2%NBRjGs$P#O7c|C?W4{z8{!X6RtcZC3h7G@0X5D$+kog5c%~HAn;7(F2EDR!<J@)^**4%e{}?nF#FFG$<CioI48cj>%'
    b'r(?h@XE+8$FS*U$uSNNZbEfW@<A5NSXyw<+$`w+iwxOR(xO{FMV}<D*mtBtnfY1638-mRAWR7s0L?nZO1ja@_-'
    b'nl>haVoLLzOxt{UHQTua)ZY90xV9w`u72Dev@<8!$?5cRD!7cPOP{N)-'
    b'q*Aa$Q5SV1xg#Q`~i=|npNqy@e_kBw;v$n#BnS@s9`$|AZ+RmDm>kC}!|xUcDrjwMUuJj9nHS(+@hy`-'
    b'RD&p|@C{9l6SWtx}VDA~E*qgwl5fZS%JdosMOJ*jWwzTIrj1P*P72|RGE{Eu&hSmKs!*k}dUGMzZR#bMzD7>Ygm^V@|91hF6m5k9'
    b'4WWq6MYars8>uxwX;&z%#R7~exlE_V8uWI|Y;u<>QLi(m=ofjyVE(nnhP-'
    b'3XaQSj=~5@HQxp^(+=<!q+{p6@G!?@m!DPo<1HxX+i-'
    b'+r(R!Mi(x*2U9@Z{=VTdTmdU$lx129t0`fHTeQYFVeUO*9Xpn8~33&ZA$^!ACV^StdY2Uj5)#-'
    b'g)b(mKUG&IO$ohWrA#IjEn`(U#mTd;q%tmy7xK~XoM9YNvIT5y4!8DV06w_bpd)vXn=F^)Zm!rLmv^wr-^K@=e^paLOLHh_R{ki-'
    b'BT*oq=kSS}NBi!s$K=)}jeh;Yg0t7V;bC&d1ORpZ{H9-??za_P%Vd*n>T++YcaOGu+LlQaW@$ck-zjX-'
    b'V6$)~<kL3$eY%(d?;KU(cvlyDqY9xHgS7gIXZVjN)hEo=MAKI0Xw%$$e4!BBa_2tApwx7x&1%UQt8T(Qz(l_Ps<ANAbK1NgF5?aA'
    b'If&4BZJVBi(pv?IxOs0?wizb&54EOFvW1f;z|Z2kxe?z7@<{XOOsBpk~WZ@s33Y=s+v&_?r~%tpKNo(2JM+LN~#Eq_O=w!0x@coz'
    b'}Y9k3LW8Bv1(9KqT`kv?r|SF?3mXI{$jH`gJZ>$|S7^B0`O8*J}{oFrpqY_@R6mX0Wrx|hIb`6dzFmNwm<VaXep_O)HdZ*0JU0D+'
    b'3~EsiPRX^42+`+P|<PqVVk0&pW#AkwT`Vq*2oR~CWoO)ERS3&G%?VNU+rZPilv1)vwgfa;O=v572B(`NM~c;BB6M`B>5H+(GGt{?'
    b'GgXjDI#u8r<tnIg}a_JQ%4-fvCa-'
    b'Z?DuVgKz(8%zOvg|V<xd>s&gqC&)=!Ulh~pJqe)Z~<9H7v!YRiOg+$bo&w@F7LVQb3CARkYpv~^;p9QH!0TRIz*zrBF2W`!>j6@C'
    b'2>%v>#G9vE(}&pFyrrn&Gno8AF?NTZv|hQ=3T+l<^JcfMW<cEuT|}e^rgnxINF+`K3?m1k~zwQ@NAi(7&E*pHT@BOZoboPW6dxYZ'
    b'ky7VaCMxgg!uuyz(WAbZNM2)xr9JCAu-'
    b'3Uvryy53UDv*>=a9Ics?N%>@E`>j$*@1yS!t8>%6CjwVPXoy={xU!5v#?^U1;KQ_v!Q>B}O61B0|p?6B`ZLBypMAM3`BiBtR!-'
    b'WFqwc03w$nQ4B`+ZcI%{U{uukl78KRp$bminH2G3~jbkF7|h}&l)^TI+$*&v2WWbzDeCbpQ?tyv#vI$u?85ixp#flS@LGqYWPPiP'
    b'w!4-^Y<3U4PzPcD<-`2c~i9kT~Ak^QkID-'
    b'(_B^a@*%SgM)MX840{AS;Kg)8e(`^i^H3u%HO8A?KeuPJX;o}HM~s`#v<`8|YVBV)F`sGw5j!C8oZk$B+#qT=(MtTovNJTow^?nJ'
    b'aU}>n;0ywILjTq>Vsz4&F6RF)-'
    b'3Iq?b_|RrU&kqF#4+1|XS><Nw^f#1BW(42FkCZ?kpAKF2(|yE#&yY#Gs~ulU3lC5_Jr_E*SJm`4BI+XFLbk6T(?Ekz{x!C8R73^9'
    b's{@&0+K_gh7C6z%~Rf<CvuQdBm1M4;QuX^bb6A*0Fq6;zJ>sg4MML6>*67!+2zL#9uR5!lG@eiK)$SABiieoR{MKqhGBk(;5Gz*8'
    b'<*XDpyw{iOr*%e5<(F@^eOhfY%h1)op@-'
    b'MTdRlgknax0jviff<3HnAUKiS4Rk`DY7h7yJ1tUg?n~ckj08nOJmnB}`ZCNh2jpxmyi$>RCwuwR&83aKawiF9i?!&yZJ#7hWrte_'
    b'`!1tG?%;U*c%LHSQ`W}YAolN@eeT^r-'
    b';4J=*tJ%a8W~Z^*tok9~f7R;EUbDDBs<${ApKbf7tHp&<88%H!c9!9{A&{n{L6l;$%5pm+@S~8?YPReNq<Sbu|M#jqgZ*9m1};id'
    b'l1;PUyZOTw=7&%ZPy6Nj*>jsna!p71@e}5Q@Kttc%LesoqvHCX<nM*vM3k6Z5W!Sj_G6-'
    b'E2e7W5<sY+{?`eU^G8Yn#*6pU_tQ10+-KygemJt!lT)_M_k~qg&LHo<7L9D#y6T71}0ED-'
    b'D2>}?6<&?La%%2(XKZ||Gg9Uz_7_l?QGX~r31$%}hv(s#JZ1Zc#m>q{vC3&3$j614;<+L9DF@$|-'
    b'%Kf@+*oyv%?~o<n2goI4$~U3I<}5n0s+aw;RhY49)%IifyF5v^xBSzS=4xkc6OuNu6LixKLwLM44#A{Q42ID6cAsfrb-'
    b'LzPqQ;kb?+{SWU^ar_9ZSd$!X2kw{v8%}na&ryV}boS#&6i4%ii~25+g5-M9*FoVIS7;CDQ_7%H^51P?hasallVCZ-rnFmyOm!w|'
    b'IYcGgMKiIxOWxy9{4<9`BJhetgT<K=9eRWhQx8#fH99A0ln)9sX?x2m&0tbE~Rt4pOTlpl-'
    b'*rIoqz8MGbugL)d+f^&FVO_Jt%(9^YwFKu|(e0jk?sKu#fm#}F8|BU9PIXjjJVEW5r_9^Jy4G^*!U=7Rlzg5VWZvxE-ohla;;FOu'
    b'Id^AMd10ph_W?DzZTELE$yio+M$_fq@HquNJ#5+F^g5p7q2&7U~nZP7z)8>WEMU@Qay_Rhmi&yv$8S%XJyFibn~*{A(!cD(J@rJ^'
    b'q!ItQFteM*!`aII=rNedaQD}h#i=Qq>z(PDA3*Qdi$kYjc7)r(g+9yBlOeDH?b3nzX!5JlcHwGYyV{rv9!Tv$GG$m?bEb?hi(w}O'
    b'?jGNgLp1fqLjE0w@4%Kh^A?^FOk@tdMGMK)D|90<H=#Ek5R)<3WSED8I|;g+HR05_Z~m%lV+Ph3K=VZyQn<&9?jZ+Xdb2u$WdhvU'
    b'XPO}f~@`F58`#|#Yu;5V7DIBp<X^t_;<!&_yOt5F|(j-'
    b'4q$X;#G4MtE5=j~>{9KjK>Z8}IsN5<9^vb<0d^x%>^Z^c7}mW_WfOrztZIHpIr0B`^QUqy^5t25YyH(7|TfYO$^r#?2e8^Um4<Fr'
    b'HxV>+J!7J-'
    b'nPH<WvR3c=@_iHU|l?T$}K8oCqTY(7yaw0}QwVxwjEXEksE>o}=`ki;$=1yPtX+i9@Z7gU%s9_cjZBx_!~1a(+v(^cG3daj4~RiR'
    b'2I;hY@_?&O81cY^H*9Lyu8cplmL-'
    b'7r(4>@_w<u=OM@9160v}ngqpYhlOuCjl+we)7cb#D3)>oZBn7@HQOjIvW_6>;x()?K2Wl@t)t$i=IyV=5MK=kvPWIq(wcIdiEw)?'
    b'21)1+*eE7FXYVIbhDr%fyvM6+zY2mb!SP7VV&8WzS+KQpF+l(!U%VR}PU^DfJ$PaB=w!v&BfNe5X20UuQ8}r*1&^~~pfGllg5_`R'
    b'y4|Mt@r!Sf6l-'
    b'jGOI?3<1G$LK$LY5%%!tG(S@&(17Id7wL_u}LgJ<=ie6a$Ue^>z$Y=@t(U=Gx`V+yY9qz*K_x65`u89BZU$pfI^F4+XT=hp(QOT^'
    b'ZB^^abA%S6zD3~e*o%tt*?r|`Vvi9wiJq`<jb_n5G_V9#2NAD8*&Pi4Da@VigJo%6BE71HSdSTtf2xE}QMc9?}ZxX?=C&zo)0O$l'
    b'gUKT&{u+H}D-P7YNp$rjnk6VRF-'
    b'%Wsqb?=^b07pT9STYSAU|8|Q12~r))S+Do1;#5dY2Tx2EvoA*u(<?zsn67uwpJP(Y_X7;~hc|>L%T#UiWcM^^l?eez@`3^Y^oUQ9'
    b'^<qDxYlOW!TINpGTZ{88aet2+?1W4RS=KC>-'
    b'K1(YL**!xoEFs_xp{~^y1i3?h)lKx{wizv?H<LmZF7h;?K+_h>rb~sH#oKO+t98&1o?gVwD8t{n6CJpLiWo8Ol#sDLG7ikUCykQ0'
    b'hnuirv?-d+1~x(GJOvGN-'
    b'(PWJb!n0HcfWsS2Uf1i0epK(<kIjsIFyqHsBR*hpl^jAl*V^@Vybr^eJBn^Noj?hQ;qV@?=<P3S$RxE<2b`Og|_4Aw?j0I^XNqgT'
    b'WK5pKC&_RN)@N0U5iQk9yTiEI@Rb&j1Ew0r|XxYOnGJa+CVH8F!!ESdQxj$G#9a_glWho=(p^?8O*?pWKg0a=5QeATIkgJx|w6ej'
    b'npNF0b2jwyHeao5{J#X51nX%szR0BTvW}tn7GkFsvuHj1NZtkMnOHb#b?1$!1$tqI%MG?qL7fbD8JDzpMp)C#mU3mH~SJ>L9P{6G'
    b'B)K6rsDQw{yw}B@-'
    b'rD3(>z$_Wc6!>N}>U*q^Gtqj<o!$tt&R)Hb}~Ms4xBCMH86VA#o=^Wzw*_IQio+{s}BIdk{ex^xnYzv8#V|0rsvovhXCj=FJxSu$'
    b'}aIQPd}=a%-'
    b'kJu<|6Ehhv1V9CzO0q>oPJii;Ep{OA+5FqaVOh6zcmf~n8dkH0W5_`Bj?DPsgu|sB$W82o2{|(|TrVyWazq5VpZD|>K3Ya@??`U{'
    b'<l@rsBBXydi4sK<?mHgk)s#CQ0^CA{99BuDxu@;@JcJ4Pna#;{dj6P=`8^+zkan$xjw29PLf?rIgvWrF#y_%;~Fe)I=>5liCB4nc'
    b'vo2R7%5w#w6ctij<D1R9*ssfAe9l~Z6sdd(JD%J(_+Iztnvut4QwH^2i)6ehMJmq7e&9o%%FbM(4`#C(zQ)Rd-'
    b'+66&2J0e&$i#mpT+Rwr&sK<-'
    b'!=bNAlO|eSb0&>R;ZEM~@%41dQ^8SAyd|?o%#>5^2t2S4ICfPNrf7heOs&w>jW}^m?*XicAjazogT!B#ej%W&EjtQ>q4DV#eJ2_?'
    b'jjm-<@PQcFJ3)q9hz}Wv&*`9(~)=q<#*OqF#1Jo}-SS_qU%9OuMa5Go7L&Mq2?S1sJ%Ge?%#p<$Cx`lWM-=P4%EceZIU|ama-'
    b'<hZ*xwi)xBYFaLEMMtp+e7?DBOL=WLEG+&*1=E5>VZ!6?X~#Hd2P~b?|$>0>xP0q(>w;g$$m>_;^K~0Ef&b<TmNAuWpn_@eSc>Zc'
    b'7K5iYAMMZxeP#g8u1vY+IfPh8Q9K!#~YA*<<2GOcwV+YylGD53Z7Wr+ZnjS?r@&NLp)63^={VF^$g=^@BHk3kfy;=pXDzZ4HB9o#'
    b'Cku)miw`ocppR$Ht%WBEr2gu%1tc3l%d(#2L(9YuKRCo;7L5LUEXrYnT;*ZqwUU6w#Ve%ZL5JyJ8&@PBqw{4cBIjpp!?S`xR{Ya&'
    b'>Qx@a5Og?<1nYkVdHp>=?D_P^q4to+tPPf27k<N{&{$Hg1N^IR*X51(Rmlq!?$KjkqR-'
    b'&#j#i(bMbB4VPqMu!?J(fznt!5y)4l~zHn`iO`H&h<vO5lO+w`IbmrKv=p8I-'
    b'MS(37VadOjB38ohS!etEFGrL*S<Go7IB0Ze_Ii_Z3t}N|Sj~Inwtxe$gb?v>*XCc<&L>+aJ3HK3$iW_(^bIF%4rZU8h7vjM=5-'
    b'N2Q?di1cd*nD!1x;thojy2ox?RPtwTGf3AKT)TEe}P<Ga!Lto-KjZaZ%gPE+wJWPVs&?C=F!wqJ;s&(F3O&#BF7Y3D{`<Z!Xkc(%'
    b'mKZf}X8b=9=c@TognsO0GdeGUV!wk7aok>6E340HBzbc}~RtsB3MVj`j=+CcyK*JPvHw;S)Y_0L=Dk-'
    b'X$<KoG(m3$owlc4Qpv1^6YfO#4)Tte$v(oza|9W&hKO#Xc#iDxLqcqn)5G)6$8f5`NstrudaTd)_gfYUA%Bd&}#xoz=0ZY;3jG?)'
    b'DP>e%|)S-fyorXT|(Qme%~-8-_xt{b&*#UlxRT3)Vt62YQ)qvEK$})gyvpC-'
    b'rD)!njIwvKJ0MQu08lebU1zH}=qG5r^<3xh{_h`Z$Rb5KMYK&YWhS9B0*>e*uxY+Wc#l@Q+6B9NRqwXpdT^AcF{x3i^q#$BVp-'
    b'llvcDnW#?0-Q#g2-m&e_H)Z4>Jq-fO>8Z#bekz+)%HHg^wGjqrLciItDT&wjtE8ZjkF)hwH4W}-'
    b'AnRNVE8+WuAK4%99v;?N?RGgb^6}hlz8h};dOq|a%pabqoo|Yo`GFHQUF|RI<wls<Qb!vUEy-DiMucNCD}oQcg_Vcx304FtzvgrK'
    b'6h(%8WV<8M9_P%%PMj!~oHa7dxe~zOon`~r4Ld+kGgjUHrtkfm>(PIddu=zCvFyfkU&D?G{Ek8UHojseP<7&M433}J(jQZx<(w!-'
    b'TW<dXjJ-ll(R2E13l4|RmWDO&FRe=A@7tRulZqp!><K$M+#x8AK9+9I+f0x3Cc8$b)|u(WqB!fyqVMIAs^^iFEd{I{S9~x?pc}eV'
    b'zDZ%IMC&*SVRjNeV8v|6cDpZa^Due*;<3<puWIU=y7ui1AVk>Ld@k7JJT7l%(Ps`xvY>SFLE1`-'
    b'UK*NI1{gYfl7DcBd41Cg|H^4@q^*7I&B(vTZCh~@`=?VVyS>M%-'
    b'F*lQ`5j7Vx_*YuvF3xASpRY1)9~hDImQz<z1v;U(zDy*%@bCysz4}*x=$;@2<vZaBf!$mZ~Kc34&yS_ZzdZh-Zr--'
    b'%#1hl)?UL=p7th_fv4}RPQ<Ijp<6SDGyYrUyN=B>94%l?-Afb@+CZGuwOCyCl<*p60l#_2s1!+o-'
    b'rTL$`Pwf*Z*ueYKC$_r1DeAo1oq>A%vUs&$!p$HTD!LFjufXIPfYaxj>u3G2uX`IhXY<6#N>6US2rLFZ)nWLNxMl@%WRJhGr;j~N'
    b'1A=Tot@#XaXof^zCAXz`K5Z{VY?xP4uZB}Bz&9AELP(KiUVm}ufMhy|E8XS2XpFyX=2!J%tQ!>jPC(@nA!bUbizhE&g<#jyGWisc'
    b'#hZ`u=`<gGzDsTx8zJ{b5@ge@o$o7gB>KNs<Q01&3tU8Wnx=kg^@X5`d79w@p%s?roFALb2-'
    b'8bDk$KXG1=wEAzH9^Te5p7&eu3wm+<jTrvYzvw3Pe;T<&tu(@YZXHQNvcdDU&z<CK!)42fvhDH~Tg`uF;}aC@V*N^$JV%Rph`&2F'
    b'mBtFXI3b4ZSxV!MZP%iH**sCV$FpZS?be}{L9IPC5U@_lGAwtq5^;8i+dFj;|SgAqFzO$8YGiw*tePyM4_s~dA!j&tkgc)_s<zK('
    b'0i{hd5pEyW350Y0{<a8Pc8gP4|gBewoB7c$G&y)ATzo$QRgvxVN(9BczKy;8C?L2bW4ce{b5@i;buDEN=3VF8iHDPa8D-'
    b'k1n>;QEq}7aRPdFwuorzwsHL0+H`g5mYvESl3tS7G!*Ql>Hl$GJ$}AWMA7s*5Hs)eamf2a5$zg(cAWRF`1M1t&M%hy{X=^*X=+!o'
    b'AfS^&P;l>%^4u_SjGYV9-bB_LugvsS-$>$kS6b6P<G11jF5{sj8|XJ#+}!U;jt2h=vt=T;(!E4!J7t-'
    b'A%9iJ&0%}I0^1NBK=+hnUKAq5B8#`{KrX>zk!%9e^ez#?c+YrUf5$+kqT9U@<p<HT7dblI1_^bs<!>rNu!kssUl;GjDqC<49_51_'
    b'eI4~ACeRVjPx=3RJeqmibX9BB9V%&`@spgiQ%!_?Coey@nKI!UI^iMyvU$EKo68Onx3>hvdm$ZRO_`#P$mjD~-'
    b'gtKTg2}M$>j{qgWI}QEK<QlITd<?kHbK)g^|6Z+<e%-FrwwX6$6+EM?Q*i%=bHa&q~L8gg~7ioI0tRp_BjG4+3jZl=-'
    b'd2g_Om(8)#2AR_$)+xY_EOUK>w(o!Copoy+eDFL+nLEp>z|fv3x?|-'
    b'JHV^%mg`a8*VLiwOXaZUz5~24#CjoD|TqTJ$}!2JNE?4C~_|&JVe|6<2FTx0PwRioG`w^r)uv%J4;?pIL+odV55>I`{CFk`N$1zF'
    b'45jg1F)w#z5|`|q+UMhF?`z8Ku4?iZJ8JB>{@_5b7&^ehbdM2vzvHGEPs=bkoutZmqqs4aKFv&H%-'
    b'=TxRhCCA|}6J>Cii2!|GDl<z>5atA+3So^*X@6rL<?UETphW=J_p#w#Gls1{_3r#QXZOM)%pGp=I_&9SS_{4OMy&CIK}Gkqy+`4A'
    b'_iIprNDZS(Um?2)<=`N!FZ3odCVf(kvW->e)24O}rB#gXf8k~IN$fSxAl!`g2mpktv-#xZB!M$wmNY5-'
    b'~c8p!&cZ#6X<s_feX>7KH=V++GK0o=6jiV;|}S?!JXwlABa$McP%<T2j{5-'
    b'=^Ng~{@~*MY91<m&ch*drb54_m*3lef%My0VvY<8Mmrt<dPE!#INJEy4CEf`5RB=7C7|F0#G@NA4Im6oC+;D1rTdw;m|TWQX>*bB'
    b'Rf9(|-'
    b'8d9*7gpW&Z$h!8DY|ZtC0i^$;eAy6OF2Y8<+2IdL$cf6NrkB5mETr4Jq}c$DM8qeySE5LR!OI=vGa)Bf$q<X}5#*v~svxLiv~uxu'
    b'vom|uI>@n)v^t!F--A&&G|#S1w_DE}3OA+A(ZmoF6MZ+GR3JzPfZ*dV&ZT;Pz8MP=jg`s<y`vaDVk-xM_{WN(h2lO@Cs4K(4VqI<'
    b'kJoNx2b@Eot@a4ILec4D;sJ$v;s^Y<}0KgeJCLsP(Pt;)hIeH<$ab`upeh%M*wIxxKRp{#zz4#JnWHKJLNZeua5q_@BW>Of3PCiP'
    b'e*m2E|{Hk$>7iy<Q0_)aHt{`G~#-'
    b'=kyKieBs3__uFVtKi(gesG~`zP+`g!A3H+1hWp`;GDn0r%Cv;DH~s6z#!ln{IFlskU*w2()3yZRbhuQ*t@49SR%ZTnD-rZI5=I*V'
    b'u^VtR0;ao3nG)o?ZZ5tWa_BJOL!)5f^F{G!7t{p-'
    b'+vwT9OB`$yvxz4UVI|Xj`$Ba*xA|h?F;0Lh|On2le4!SZmi$^y_8WOEXXEw+Memy`GJL5IMPNPKDABTaNz}4HIvm|3%2uZHkqvZ-'
    b'_{6K-vHJLnZlL{KA5aS%#-!PM1gD*r0if=qPpYCrdrmrTT??nnuO@V!kZKF0;&Z)>%9`|1b!dO_e^QV51XkscIosE-iensaeBhve'
    b'1=@^6T@`)ZM}$9*KxM(a+0j6XXR<{6oS(OK=x*fJ&uw9xB6c@TcQ!$g3VNKW|lRy4yL|s`7(e?G>Dbsx6N16-Mn7Nt-wFtc3b7E<'
    b'QFH|;%NWT8SI5ni3zIHX>I%Q8vNY$@t4w~;mu2P9)<a+-'
    b'`Q4HPNnRLUm%>|?Vg@MYl$lu0vx;F9^ExO(N@}6fqAR|nUVA>n8TuMb$N*THYirwVkfs}*XG*VoDsy2X?6=!$}`#TrQ4yvSik<=`'
    b'4SPZ$O*?XndQ6<5^b8IrtD@dBYxO)vvIsPTN{=IYrz#wy#GcD_DlF%VvBTWc>dhygS_fcpWt*$PY|Oy)z)ib6*vTHIo^NGyr1Be$'
    b'JzE;i4NVE#RDbmny-'
    b'h^H~aSGXjN2?p1dAIaI(88Z0dYX#O#U`JZ@217xjfHnod1%Y*}*TiuJ!%De$|=ta1C<0jOT4eTSLikbUdmm^OwmTh`JtK-'
    b'U4x4oJYJY;)+CpyZXuv;ZyajX8cZBoz{TdvMO&SZ~kR+j9-'
    b'u1|Iza(5v1K!ZG!DbFt4s<9Hgw(|%MSB%+jQhmu~Fk@&_#Ehk<L2kK%W_H6T-'
    b'8!h_0boshrf9d&~+PDdTo;TSKwi^jeyo{bcZR@4_wjcIzQYRtO2)fN2==XRhJAQXC&Kx}N93v+rRga=B8`W%Ek_<Dpo8!!ppL_>?'
    b'5%{><p}QE|6F#3>Ud7ui3sDHQmPW=dZ5;7Hrq+3L>zj2AnHNLt@o7+;N1+tHBQi&(WNXZ2LN%C-'
    b'H$7ZHqc&TUwZ^a6{NSo4Oi2R}u6VJvto2K{TC7*Mb0ASHn8WCpG`6hRSjvmaGug<;%Z6mvavb+PII#fFs`BsL??sM;5H0puzOD#A'
    b'!TLtSM?3IhYd$>fGR<$<YphR5&@>U{PqLaS<^}Hn2VPbaF5+c|AHDOyi#?$&sxh^8*miY7!P`!j6_@^(nF-hvG7#r)JB;>nYXI01'
    b'Lt+SiCOMrD`2^0`frB4Jfttc%kDj0TMf3wU+A;JzoP^McLC~&Y7oA~W<dP5|h%nahz)6Uk(Zl$1Ikx0W44!X_O(neAlj0u4=_w(w'
    b'$>rK_M?=hsH5CGaQ*In6gNVBjjo+9D3;*yMFR?+|%UXte*`(frxa+p%q0QO?W(<SLroAPTEXuTD{{FYMWkXq{+T^K;o*t1NqDsjo'
    b'#hX%6J(R80(+W>85m`1m!On>wSj3OC8BP0J(wKvHA_!pgP{p9bTbhdu-;RL5Oe`EvIOQ$p-umdrww4_V4NLWL=-'
    b'QnPu+_<Up*y~b*R%}Q`MKfE$u|r6E!{~rivPM}bPsW(sAf|?mX#nft62u9F94)CrrtZMApP_ZyTHJZ3)6Oue}xE`#q7`J$(3x~_5'
    b'j4d%j@NXb`B1Lemdm1Z-B@~iOZurr>M=3Uf0xyDM^>p9cBdp<9QpWTp$Y@=CEu#3RoWIY-'
    b'THF(T{Lu_;LP@<h@a7Z!4K)8%k_9yj`o!oaM#9-1QE3vY~)N(AJ(C(aPh)VZNr!(X-jx-uH;pWKovQ%weCm^X_CSkBxcFmgFl;7$'
    b'C-'
    b'>PNPH4pKl^UMZ2IT041xiZsJ0L20L;0c6KRY()%nh$|gF|lz*FrPQ#E1U)R5l48;<VVb4ZOXB!Xv495?$Z7>_Y^VknQy~NT!6Wb~'
    b'^So|hlm<RFK8BKO(SMiFGT<^?sP%6|*J#*t>W3}e2`Qt1-'
    b'OJjI`C(+|V;S0WVn1t2dR3G5vex75$CPztDYv|S*9^!heZ9*JOx!9W%&tWM;{I}O!ri$Qd$Aa{JSv9iTvb&jWhS>|7+??qom;QF-'
    b's`h+?QxW??;%^w+b-'
    b'#`5y{=?a%poF>4aaaCGZvEV7v34@5PUTga^si?wO(=h<qCMK39+oafDWC*?Hk)H$dX6YQMI+e<E!8A7!;6m_JpW?atz;rohKpLBJ'
    b'rzQG8(*9PTs|!PY95ub@K~4{M4Ghsc><&35$T}inV{K|4t*c$$~9$2^ulmCDZ9|PKEK7$7K9yTlYG>ezr`?!vXI{{+Q@;z-'
    b'=9>RezR<Zyw2Y&+%SVhdX&<2BEmBc|r~e&)sqsFQ`8&CggjRqVRR}3d>-tC0qFPH%#>x&TmhMteW4=(@L-'
    b'KOw)nPed?}R&IMn7*s<kIRYz=^ua>6$%~>ZC&x%?JirXGPu+(FY{`y}ESpG@ML341XgQm=bv{&exIa#g(^uGVKPIMv{jKkr5(?bN'
    b'm$7wv0xbI@A4sVgXP`d1u?Ue*n4FEF9wc%y}hI5@U=Il7`0dhPcT?m=;^)K!=rE?aPRWl}HqgWo>n9OP>iG^pm+h@wE`h4t-'
    b'o9tF%E6y~&Qfgy%bn;(vculoT=7F7cV8aH*M5*!K7}z^EK&`iJK+UpFjw2~wI}~;>nf3*Jgi<39z!PUfv!nJZb#~b!JGaB&W&2On'
    b'AIgKTiGQ;IB_%dD75qmyqG$#Y@7r-'
    b'MHZOi0hhVxP8mZ)6%sw~%2|(rRs`4HdfY94Mm6wyHj#Fo&L+CU762)$#N)s|}$YF9WgN2C}NSIyuO|&$qZ+<YHg8AQ%Ep2TQj>A}'
    b';7+}SA?Xo2N^!|>ya7XyL^*7vl0TCf}e$oE%3+03C4FG2Ket2HCv@K2;VWqr%PXM!BKti~+<==**b*`rcyNAAl+|a3+d#zzthhw_'
    b'3m%NFfUhLqJoTg;Sju}Cp5CUsf^yJnF-7e%R>-'
    b'kT6fD1)565sLI44plOdV3drTM2Jp#hw2qz1x%xE{8Tz(hv0(tG#goqE@<LxGnPv$KEbBAG9_i=kykUul#Q>-'
    b'Rkadm+;4iXP1pa9pA#fCmWX#+4wisY%ebJ5mC?ZtYxWBP|AKs^6%usVRp1O?pO(S#Uv4*-'
    b'0l>iue=ik(P1r~yfjBm8yNDR5X#O_Og2HTjx(}4&Atjw@3heZ%VlQ?3zQIUZ}USN36A7Vu-'
    b'5@Uycu|4e^ZhX$R5<;(pGp8?kpE*_`3scE+YR80jzLN!@BEj4%SEZbAH>>4-'
    b'fj@j5pg94BgJY#dyV=hTFv1rax83(nq2g*8NR<;%RLwaN~~ltl5DWjxcl}H%i6r-'
    b'@H~<QEmRnHg@Z6LbjmY<!kk8lk@xRx9>aX%M*K_3lqg*a3Egq9sA0vUpQEMuj&)3%t9uc1AloGW(@&*gq@P>vCk!|=&dCL(#*K%R'
    b'BPL+J#ehP-'
    b'U=H+O@EI?;{TGUXC}CZ+XW_+hg2N7iU++}P7Zh|*0*>D1rSHmY%a^_Qtf{SFRi=>gf`5`1sPmoam4H+JHhAg==I$jObx~<-'
    b'op$ir@TSlz8u<rv{PPjL2bO7y<W=SUI0ejF3a<LWvd>K^P?A3ty}lFowG!2|C`Mf^4o}_uj|gvUVs)4J_JA{vVv*PZOgt;%ut_p$'
    b'N)#L;?+D<<+Q)H>-JQ)Z(>9@bhSOyaToX&;>Y&DJz&)+lskCV;Ta-vXX96Coo|d)1OsM7J|F0W<jzAf$q^53@z4XQgbI5L0c!~M>'
    b'_S|4rf+AMue9+W;SF#nHMyrPI*3_!bdKE6W3ka@W0i}|T(-<~*f7i;vV*GOc_H^-'
    b'@Ld*a+b+mU7c)AJ2iVEkM3&hnL^<xvs@O;(C@ehKM+A6k`ut5MB)(r3d)&?mDh~Y<|8Mh3Hl(0s`~<`sA$TX~OpkOwunq^=e*EUP'
    b'1v5lf!GJ)R_M?I55c2>3t-'
    b'afk?7Wh6IZ})a^Yj}o1VM@e5P%XR$LKq2VcUm10#uuI+v)DwRhc9Z;T{)v;O67Bv2~Gu_(WyX0u@?1sXEo)j-Kcu0E3F3x%F`#Z-'
    b'952$6=N9pXtqR&}KtORqd>7-zR0S=1<$XJho3dXEh8S=X9N6Ye76}S-'
    b'%xZuQ&9yXMBRxSK}#daRBXO9AH9l0%VTIYaOcQZ}H`h>d5JwJJjnUBh9Es2cR~@dK2CAOA!0sGw-L9=iFZC4q1e$jg!j)oyV-Kjw'
    b'`KWD=E0T21&1TIb@=dVLj@m7yn}D$p@+itq0dY2sO@6bbine_1!{hS3e);Ycv%DdD(EikH*WlmCD>r?R(X&I*`GEU7_=)Mt40;!&'
    b'bG7KI^m#9!)m03gDji?=sjTN_v3Gy<XeI*%>mGIsv-'
    b'`9^z<lm{jSH>;SkMOuR1;Sv!xosY2kMskRAL=+vPm;U>4zBGgjfwRm05?>x@$Ez@9ef2STJmoTl*HtmX3P`UvYq}$IvBnZh8rlX='
    b'E@~NDnP*eFOG<~2BzUUD=YSwdYTqgzP>^}2LhKk$C(!EMc@Xl{u)9mH?3dd|)#Q_!C8JtP?a1ey_RZP6M1H3$w&4`xKj<Y(Sqyky'
    b'gw*7NOC<wr<vYzgIw@6)_XXAYHAoy>nfdl1=!8qM!hD?K(13BbmMa|+ag(`@GX8-'
    b'~$SDywFH@#Qu9GyHMydcY{AL_JS&Ua0)=i3eKmox7`Z&$eGzd+H+6>fIAtF8Cjc&h^-P_FJ4RSfN(8k20}`mV5pYi`d-'
    b'S+T=YFTNZrbq*NxVeeSI$BR!8H3>{l)KvA208PRN3}pg%Z%|ixiZUgqJKy(&o*KWpIb=s}F8A@t`!0f&%#Vfz*n&%fH~{#n6%yXm'
    b'G%H7BW2w~h!4L}}xm&LLF6D{9t-y5=hzhK2ZxbYOY0#sX2l{EBvd&z3(H4R;%u`h-'
    b'EO|D07u(b=M~H#@Roq9rOsPh`BOj8Zw>W#h%fNAMwhXnL*Fg4t+ye%6?4Z&Ezb_VR$STE<VpQ+B^=zrRjNdxV?R1z&{?1$HUFWrB'
    b'^GIP@i>iZ^_YNoKActJ~SD#3gd`X<&A<%6Xk4Jix>H)Npx>c@M8i<SeDFX@=zI3p4($8VfuzR2n+#;Vhm4_uCJ>M*X77>K|I0RNu'
    b'++DXGgF>PTT;+@Rqs+t54>|A$528pa)?N~^xLtI=9a>(}tPqf&x6h!80`!!JG$WVa?K{Wf+d6X;+Hu}(ZufAIanq)-<zX1Jq>-'
    b'M>B0smNauT@blc3(6BZ&mkJN=YHNEuM6p&McYFK1v1&*XvJT{ZLj#adGgsa_fhipWSPD<u3H({I=wxDcOzPRB&>uEd^_PleE`z$6'
    b'?YTX6aGRN(d!uVB(s4LY4Vj^h(ZW9(69;xswr^6)uJ%h%<ysrK=&LZ^H#2|^DWl7tKL&i)-eQ59&&vr{#=cRQVT3oi+-'
    b'M_7i00NYZifk<;V;<>6j$vN*Qms57uB4a8Zo1BW}<dfu*Lvh}ti(JzjQTW_Xcb8IG_&eyj!;c9Sj*k$pq-'
    b'=}5n}?KiOCwZRu>g5MHXSc<?br4rZ{qTQSD%(cOi(+caaD1B2NGJ_`AL0D0vBi2fkq3=PNqrFq5>Gsb-kLPMHftey}Nbm=$*L$ng'
    b'6VG9_Q!VYc2g1=<HvV8(Ed)<2sE)v49=ra!wCMhdypd;MH<ECfWDWhdyy6Eg|y-'
    b'+ip<v8UjJf4GNCKbNd?RI3ALJbTxI6=$}TN*XRxWu{5DjAjrw0x`;SX+U*#l2mM3bDz<F)uzWgIfyn7zrdyEVW9Kot{7R@%XfP^J'
    b'0YbR4Ya*9L=^M_GEz1WU)jCRy|9aniOa=T%MmyP7a{T9{E79E{jXQuzfG{LHQI)D9F58ZIq92DZNNscCM+l&UdknVKWR$-'
    b'N2o+e?0zYsMDsW#2M4bCw-sjJr$%VvwdA6g><p!J%#99cyDqq4Kl)6yoB|rR2vdvc^gq@Th#u|ru{1Ll@9sxlXx1R4_q59LTrHi}'
    b'%6*IL5n)?CetwAYnVX4(^dnH`P5la}aO>*~LMN*{sltv`_zH`gu!^*l%t?<BSU;VH;H!9mnRD$(rN(Fshls8f23yQ;&U3Yhz!A(>'
    b'!Uj3eHW9j#@7pNTb?P~7pcI^?@6_kXaLi;;*2Xw|o2DiZey8Oy-'
    b'*O~(o8IrQapBufwP8HyAoSFT?8BiMIb+tzYdeEJhT;ejd@UU0gR^6JAa63mcw2FSLb>zQ}#Y%BNqFUe9)=j1SrbA&ITDTcmb=K%s'
    b'Ivq-'
    b'd&_1dn<y#S)^4sRR1l*r0t+upbLG9LJom`^}>Km7JdcIBK74jS4@?QzptDOe0p#0b!3ATYXCCu`+p!>LztQUL+;$ah#2dr$@H{3}'
    b'ki#}c9EB%X)4y`_9$<5`<r4gR$J|fcb=roY^4sQO`GP&`4Ux$>l<yki`e)b^R3>Fw3@3GgN^tY1N4S`W!)uR8c!8VW^ss{g23*pv'
    b'_w~o_T614`RusibK7It*zf^%=>n}6)ai#<ilj?i64@f@UfvFFoM?3f3r`f@wEo*sv2HFIdqOXKtr4@NlZH09N-'
    b'xR>SPR_LTo#e>hC(vyZz;j&C7HJNx_Hdp7O=ML#B?=n3QLts#Fi$2tgQRkY|e3l6tPo%^AiadZ10Bf<Nqalb}h?>sl?JxN#WJ^+f'
    b'd4Nfmd%a}CS;3zw?FEgT>vE9RQ3B{d@!Z3RKT`FRpDkg?ksz-'
    b'I^`w^<^MAB~pw@C?oqLIqa+SH9Y7YiPKBDq)Bz{<nGe*fx|H}ti-S9r3?T-'
    b'e^i?uo4K#(WvQBa!2<)%v>=@!D0?@ME;9(8O^dn;$En_{W<4C;NZ`gfQUFYlVUE$drkS)Nq}Dg{tf<eKZvmL4Gi<W%<f+K<R*aHe'
    b'zN;dDH7?Fv7|;cg`bqc^b-'
    b'r9d}YMMRzOUd7W0JY)dZFY0fOLLsckzkG+53=eS8sTWRj`c$VZ*OoU2c9tzH=NpVVvpC|R9nQH75@bjP0kDab^wn{_nFr;p-jm(-'
    b'<U@gKc==1&WVgqZtI&z~zb~Z)Vjxf!J#;VW7<nyQOl*)Ig|_)1j}HdU=hE6k40wWWsx_R3BvIu8`8uLMAuxMFRXe1h{{7NL>z0fX'
    b'GsN&P`OkT_s(UEN`G0m<RgDF&d>#$QvSpWx!>kYtN83H&ke%rmRc*FgMQR=+^u|%mqZq8x6lqZHAa&LB%y=&k_w%^f$KB3qAm0wa'
    b'I!0l%zX2tVZk#^D-'
    b'c2b%7e>*BmDEzy8hS(0K$4{0h(~JY@;5lRd?mi{6;x;VZF2#n`)6l>oX9Cx3CsaM4vKZD;Na@D`P}Pj8kikc-!1!31#MRQ+v>H-'
    b'(#vUPt`9-9!<hII)lQfOkot4$an8?Jb>IFx-HgfqA7b^hGEjLoDrlXj+iP_?d(FA8c{@e$M0o4($HRKn7qQqx<bO6}dXBMz!J2rp'
    b'4NtzRqVOeL3xqbi)whzWuDT_KM0tn~{1Tc|fQc)Vb|gQ@gGx3f>y_J}<Z{KmJAj~c;VoB7LgVe40}axE)RnP46?Ty5=Yo@)ai6v7'
    b'Fo&)u96bV^7CHPj>%_0yD^JgPHxVJ$obmLn<Mf_Y(*{awRY|B?E&9M!RM$x`xkj~g&usJC-PqiWC#36UwP*fup|@MgkNR<hxV^Qi'
    b'HU@TVs}8TWGVF$0*5=l$H@{uSoUVyaJvp3&@0{&alhu_XNBfrJ%8oGjdiBv&Z=3tC&3SQwo6ow-'
    b'wdd1tI_)=+yY*k*8!V*|*@Jq;(baR{_?D$JoaponHv1G+<`lQ*SB127n3M^yn8!B+hVpn_wsgf71pn-L8E%ob-TX$UPl=G6a4_$Q'
    b'#g7ZmH@BY$;Ua}If74M_V8c??-OvDHvdF_TgoASbRa$w+Jfr{Nw&|@~I5|Tzaw|LnIQ`;D<J`-'
    b'%xIlnTC!ffSzE!tWi!wO<NK+A0;mU4L7m_2<0sPI6Jgf5$x65aD$RN*02Y7PametX{{P}*R4v32zK)?zm(MXBzV8!>}g!q&Xb#oV'
    b'2UC7PXDGKE()!)@}{qNl9>N!M1r7wPxkVy`AvFCg3sp~JDchrme7`$43O0&!27(eG~CdJk|StkKpR0(u<^tSd=tmS-'
    b'(|2vmV?^wAvc;M2;q{Lw5?<}x5M8V6=%3x(jis4Ot?5;xYR<fpJ54wMfgGMu>T9!;#bphx!mZshiONS?Dwd~A|cK&|psy(?wQZz#'
    b'&U>hb?X;-S}gGLgK&s_Rnl{#*FK-s-'
    b'<vJnq(8H+u6JhhUn25MDXR5W{BLJ3Q8f!9+W^Wjs3#1Bg8Nb`8RmWD5hTwR3}_=QHTdu!S)C!P7cU00C4f@%F%=q18AV>CQt90gT'
    b'oL-'
    b'{ms0@QMr?ENbdr6R8LXB>)GC5AbN@<~4)KD4>{bmY4&dbs)`!{sh;qQFb8Pjg!ymsV_}Hcc7`LF8G!*KdXvngVD@N+EOK;Rht=vg'
    b'e>aE9bh)zg)8~O{bkecGa_P{)lHk9LnVtl##j`bR`|&RM7!1DyU5o?v6^T7|oHf_Nc_3EXDnq(>&3hduDC|_m}_Lj>23EeU149`t'
    b'>RH!6VArCg)qf^2%TMh$r_EbiCbiy6d&KFeCUI=;OI-D&%TV7u4=;UxF+}{d)I_{#-'
    b'_?%JiM_cHY|pExPN>>*^d?9bfoe<=$)4Q8{8xR4U5gfiW)Ct@wbt(;uZG(uPpgn%+H)+uG!4e>^@-'
    b'>qxUpRq^U*^01F<>2IXu#`|@w47f(*-'
    b'l|=Oq<8L~vr7nrD3Qk_h%#1lWb|3pR6WRGm4Ghs2m<^OXHZJ6I8rU3S0vj~#UP$vl7Ceb0PSB=(?LlZ4L?5Tpt^tTw`#;gu>7Qov'
    b'pav>huGZ-zu|S+>Pyz(#<6LaS=D6VGC^xU#oPO-'
    b'7wadwOz+AtzWoKhMz<hf%Tb~04}kI2+Aa;$)S8Y?;pyzlwS!Ci*UH)c8}|o}ih#%W<@*#7cHfN-9y`1c6bMYU0GX^csolDC-'
    b'YRFj-O&`=O<gU^z-xCAFKs<~g_ImydDV=r)op3O2=BrLQk`iy9pyCn-BN!^c8YepkKy1$Q}H!9n(v~WLoXG`>O7DbA-'
    b'RJ|hKc!1X5NpBTxtaBTsR(1>~t-mx<(6De-%6=^71_SQy;8U5kme3oEqFyj}C2e$iU)N*6RX-tdM{buDpnlxd2PU5H9))oO$%K4Q'
    b'klvPTtP5;rgjwRy<8=<q-'
    b'CZbpN%ddvQ*}6<praPO1<997^Crx*NiOKAM@X@73E0fS_j(|F18p7DfuT#c^$&TUF#CCeL1eD*uKFdAU-qLp@wA*(PlIqN%3mtQX'
    b'gl!;<W->COg?Bs;55569!bOWI=Y>*(M7Q6qa8_*Jyv2s)@{vCoQ-'
    b'5L`h^ZbYn)YcEPM|1;ea8@G}a85qClr?&t^Y?NkGiv0P)%}SO$z7V8a|5@p8;}(2*FR_Z+qDB7uZ|i<b+j%ZW0CKgkl}BHtEpAf%'
    b'>o7;?K?hQmpGXVbDu;dHtb_3Up5EPZ?g)gzb#mcxl0^w5+Gpr!7@cC9KxxhmPu{sb*NjL;oJ#=kZ!O{_b(9S107hh<vQ<IAC}&ZJ'
    b'nAds$|H4+qqkh5T(7>yCNl-TPfPMZFP>v)-'
    b'2%Q>o$hXEOWF)m$&mjV>^Am2Z6|lIzTh0Ku;dS`b%}?qosqXezU$E@ves_cVW^b7Dv_Kja(3cudY8oq6$9Ep5@Io-'
    b'EYSRwC6KG#uCBk)g4_|F3U|)Gn-'
    b'Rg~WPBeIL*tfZfO;0&q$8aC5Z`$=}x3sYguM!%m1N?9&qHfIvH(Fe5g#7Bhr?4AA@$5j8t6g7rK|H=r$!-4{PO-bG5=3?UG&Tb{4'
    b'(LeR0?o2A{X4$1_PJ$A$5zX2TkYFzz34nMAA>M{Z#`o$W~$DGx$s6hQ-^l0Gh-5`e&#x#aIc}Z-7X<<Nn1kWhDxi1y>4-'
    b'~YuQmWDNWpDR}#+9bXBzntO5H}&q?RPN-P*I$XPrg_`hO8U=L@|56PESWVY+la0102wJWOFiB}wpiqq<rD&J_eL??`~2NhO-'
    b'c*W74-'
    b'gc5Vo)3X2Vdp=z1&s&)0OVCR`ZO#C@j1c6QBqXUam{e45mVIr@{)s7=d}~_uj|3%NE|9x(KqHL*S4?=meD=)e(&883$j(C)aPo+)'
    b'*X0FZK_kSvo<%B9rvi{Vj8yU(!W`KrP>1ww+^#>cT+g!<>+~CgNU5M-'
    b'wx{i(Ofz~V&19{y?V0kcJ<b682q*_SSHEwjIFG{1QPOg4xj8WDlq)>^R+ptPHfw&<l98#aa+CtN!%IYLI+MQf$O=qv+i=+D7|~W{'
    b'R9f-EgyA?vm2TKRx9^oFMx&+RLeBz0LsCc@cI0ff9{zwd!pF;x229-'
    b'xqJm3`>y0|Jz1W>t5bDK2Jrn@Cx>#iJ8}XWH!fPb>F;}Nf%)Z4fX}&aK|!*Xx3qZNRPO$^0Y_UrLTkC)B;AsEryK!J;#uszx70hF'
    b'-q+$B!EI-lyx1iuYM*xxCFjWvB_%S7ZBV6Op7NZIkfm=`WnG1A+|lvsI`o+nIBRN?xG8o!F60(5uL!zE&bzgH31`AC>bE{(+19sQ'
    b'4A+XAIvOqALC*_-Kj9;(E^ia$*8A(9eKE0U99+!J(D7N_g>4kwiR3`Dnj9i@{j`|7r}lC$nc@=jsJt$8yU*x<(-'
    b'cfAnr~}XyJ=O_S(OtO{zkMAQMYCv2-hj-zHK8C1gDQ@{%s2o_@Jx9?RNLAL+945c=}QRs1369-'
    b'QA_$Hc5|Oea?<th2Rlg(fh6Mfl=S4C6+my`=`A7;AW{xpbJoFLlqf7F2t{Fr5jHArH)2ze~bNQUh968BPUpwi%>JJp<|lLe!Rm7R'
    b'CQa^Nq(T5lb`v~9%YeT#__Hg+e~^CNBkAR&1nm4!Mwgi=Ba>quL3NoJ1Xcj0q>Obx7`-'
    b'booa+xs4pi=+t$!Eu_9+F7z?zDd}Eg(qqS{CC9*3so%0KYNbY2ux}W-X%e%=5Q#9b8`woGQV-'
    b'2z9!Rf%EwIz_xB}LcZZr&Mu^GE0Z#{4lvG2G<d&8CF0iz|^+%qs%3JnArn{t#z%Bj?iJI&7(;YJp{pp8!dTWsB|e1)L4zXlQey8F'
    b'}}u@LrZWTB^m{)Oq=sgdBdCJ(>1fU|A{`!0>b(P-+b@k)3c#F5)&xm{%4G5bvdDM~yC#-'
    b'*@}s*&f}kYjC;Suc@@p89BngN@tI{$k!J5^U|vBW<XVG<^smNPRNCyY}ekIwx@9^Jec*2DC(Nd;y2TF{N2iFVAigRggO%uAm|3vQ'
    b'N>kvAV*-'
    b'4lMqTNsMq6~Sf~$yNu@M33dqLV$hc*}87NBY0iDjIl<UUV0J8w|Z6HAd#RIBY+0Sp975A)F1>g8B${qF!k=I3r*m2tGfy28M2moZ'
    b'oZud%xeqVWO06k5KDNP~@Kjf0ZqdZpD$As|yobn-HMhxJ5Gbwq@R}!Hy>jN`uZb7$5?uGX{)XwjEgeFfJ77$LQZP`j|0J<rhU7+6'
    b'($pE|8ZFP;vu9=BGWUd_R7u|HHemG>~hqi2AWKJtVsI_Hi)D?JxtfCq&H}QfcCiUd`yvtbu)qdgk&i5SQ;l`05ya1Jn3)-'
    b'v|r8Sy0x1jztX}j(vU_zN_C2hqL(uhBQ2ChiapYm4A`e%E#=7;!(qd2q+BDeEh9MR`TI2xQ!xk<@7E0p&)C(8Th9s@`%mp|H1asP'
    b'l2me!TgF3+pr?y#hO0sX#h8n9A<NVL-'
    b'e1mu&q6E9mW9{nbYBac<3=c$KGwqd`E17^Ko3;vaqDF1gR!T)HaaykMCNVhqwC`#PIR`a`3Erz}Be1XfcFK8^=5vlG7aJ6n_|Bhh'
    b'wN{;$-'
    b'eP_J_h<Z0wmqpxQWz9Un8`PHK`yA#0@zgT)Lg9oS9&WvaH)($k5T@UOi#tk}wwmuHMR*hycM<?>)2qdHV!u}45be|T;08#C2OPtZ'
    b'-UsORImDD8BhFD+nYq=FAQD|)Y(QT4OW*a@c7%u3^LwJ&%Wzhg)f6v$h6{F{5vv=psJ+e@n&KL|-'
    b'B;_Qd`vFuf6vB_=pGo)S|by@0P#`OmZGw?TquQ*^%p9&Y6k7ZRWX%h|M<C@&VH#135x<^E$xH;d1S*2p4QXu^r<mcELlH;gBE#JP'
    b'=PC)=m+ckG+wKq01GEW0XE`Nv&VG<r{LQTarLQ49W>tIF_mO2aB<cD_V_*J3f|=9Qnxm;yl*h@P>IpW<)rbV)^^T9h0729Ld;3-'
    b'3bkK9b{9#`r0v)8G!OQ+7VOSB@Z)PxATmpCOKmz=RK^OfHY%gYTRctvp}w?(rQ6u2xR4pbSn9;SRddjr+ppCy=@W``H(tdavve0J'
    b'oUuU{D)$b*v!?G{koPx862Mk`BF}XspC}5y#+S{p<Z8`ooM$<z|IuUyuE|?K{&9ld@u;CgBpiZ&K{yKgVOe759S4gQ3IyAH{aIjW'
    b'9>?#sh{+4Tbc+}^+Ln81Ait*ZUUF*1!_$<6`m9KUSKcF#Kh&RcHFPP?C-*PYl&xhE;e(UxMV{Og?jaN@z>=1l*N;{e&sn8TpW-'
    b's>Ri+}5d3nQqDL%5`n}DL-RleQZdlX$wJCY|W`8LeXWhg;wFFUO7P)P#p8~B+^r;M%?B5%F%;&eOW{A(urHBPDa9^Y}$4Q_xF#<m'
    b'3!q)8VlyAH5pN601zqyx{KdvgbhzjZ(E^L;*~bVlPi6CuM+FBeu8Zzd|PH7s#Ym)MgofTKA75}s;XC_9~CAuIVR&YfD?I`tJDZ^='
    b')9%!~<kAyopBRESaSx)XUxyBz3zYjwpb0;zC||3h2c;vmt5p>o$Y+$<0cZb2ruYw$@Ni?DIMN0n!Wit?Z$yqM2)tZ%v84hTYWqp0'
    b'4br|fb9$S&S&wyrsb5<^a|IF67ze+GEN=R9*1E$A&To>gsiFLq9=aUp}7EI6uPp%+4~YOCCV+)Kz8F90r&s)~|)uDd*X5zeZc7r9'
    b'%)0f~1-C4CM(sYd-MA+Z(RNNMD>p{Ut!E60`TE8Si7lZ&UM#sB~*?8)gblgFE`7SIy)hg}y`|Fsw8u72(`Gbs2)i~-'
    b'7yqS{a(#|1rSFDGNQgd<zRR-h5^hGN5#ysER$cf@tG8b;1rLE{qFXxAEeJGWYhKtH$~=g9t{1vv|x>-'
    b'wkk>v=xz!eC52B@=A$c4^6i5bvU>i3;l_r}AE_)=h+FJ|l#8?Gx7QM*ok79o!4>%Eh_jvt7x;7XH%ogm~vr88NIYs}^lCRjzH?w%'
    b'<LSF`ksO-g9d~7N_-q>sh<%2Ja<ms6nmCP1KI-'
    b';Sae&s$<zLs+&InS;dR$!+QtX*AAk+bOQk}`JK471gPfdW~=<?sUxHQTcdwbw}o;XpSJ7OvblHd^rIr-'
    b'&=N`a`0yxGAFgfFW7jNbwUHCILc@(S!d;XHd;yY6-'
    b'JV_ltg^4JvpnxtwHtK?vyax60}z2ED}cT^hevo=H(JPV2(ADsnP4Z>eP|Fv5&zD|-'
    b'5foG9%+BKYH=wTvwYGghnHYY)j5RNwuLUQjbCa}WLWl`L6L~T9SScG0}jHcZyVdKBa}t_%p6c?_pO!0(&Dc+4x^bMc87DXu23+)`'
    b'cs(Rp_{3`?F%qGZ_1x1TNCukKAZPlU1)tt3NVD_c(Ws2@zy%QE*vR!7t-OkE_(j$)$9aEo?;}&kzL2t{4K!SqT-u-Jy#(>fjwaXy'
    b'O<AQbVaK=9kWi^nGfSsilUDCv}M&@H5Mj*FFn(`GTKT9y>Uz9m#@2*uW7ZTVLvF4EtY&1H66842P^0c@j7eCbGl@~IjMFAB?z$I&'
    b'k4S#1o-ohYkIbp{5!Y_p}C_&oq}HXMqL_Fa8z{<n>?hCX=o%MII&w#EOsM6r<-'
    b'>qyVf9z4yA@5tM$T3BFd{lymy$$SXCt&5LfH5kl{~XlYryk9ic5K#P~Q{2>&NE0E?bsS6<0_jb|MCgO+K>+L}h0>43IBTKjD7TtG'
    b'N2DouHkVDjC;;NmVey%N0sE}?tMxn5uVp2>%~?qB^T?dg#%;|6K13P2QK6Z}<6r4~Lwz9L$waeK2?TUF^u{-;7E&#x-'
    b'LBL~NQt~F~1{3+TDBrW>vIW_z(splgi0DMg)+yXqhscUqq*U<fFLCMM)p|o&);U(&lTK(ftf0qijy@50|Yyy$-'
    b'Ei3HIiQ?b**K3C+XZ!dcUs!qbTPG3FJ1`WKJCq^i>=WsCR}TIH26LVXl95g)krxf1Qk%n~x`S0s$sywJ-FGj+>e^+Sh(FmMTY-'
    b'R&^#bAAJfel)F0^NvlA@mw7sa-0zP($8)bT;Rs@;jN_VHWWhX&-'
    b'DeqvC?*7p1~)&u@3+NjEFQ1X9%aHb3t4=##r8AgJim#+T<a*os-'
    b'p{$@tv158(5;vEJ(3sOyA;s}l@4czTtRS2_V?f!U#Ttk|{od5yOoDUgNDDJ>OEJx<l@cwgq!J?Dy`b0ufuVfX64cAeE|NxfsIFh1'
    b'LD4Yo$}3o(99CzGvWvhf*UhYXGr_Mpf<Sm9R=aklcd0eKn1AL0#J2@FgB{%$d>!1ZfK7k(oKUycb2hB-'
    b'3<3xd2m($Z>h98#4vsA8wknnC#77&Ose6wTT#oHT9xQCbT*&hjC&wglBtxo2aG&F+nR|XXe2&h}&e<|RX2875f%#5+*r3r}_xj&g'
    b'jvC-D8?n`m-'
    b'!svh)cFF8aKyHWVo`c4x?%QBYjQzZMPp$j+>LEbsavn>l=1%Q&~7J0Vg!+i|8G@io9L#<>YcU_o+FFN;(>j{Trb;YAGeTWT#ww_D'
    b'~#8rvyE*o?h>=8H<F0c0zksk9k(GzeM0@Fm6~)fX@mQdG<%+hiy0J$n6F;&j)cR7mD*Q;zqeg%1&=&@4Bg9yE-AA5lFlT!ArX87;'
    b'(<#w8EtfyR*M<e9&cBfKsvtVTU1?BCBG_!UR@*oiHO~o@~GrA7w7g?LdjVrwP2_71x6)nKh=S+OHb!!;SQ1-'
    b'%PGlo=db*YOB%yBhdK`hTwCFx4r5MnuE#CzOTWyf<%D_(j+T>p;!*u4`49WaT@g~f1)U{=m+N1;6&JRj^yic*0oFD9Y13)=@{Zpf'
    b'fqdv_x~y1o-Qe>Yoai4xu#u}8k(-'
    b'5~!vDqQW&2)Bh|5{bQ`<6oS794x|5Iz)L_Z)=y~2*l)@n=6Vv)HO*AF(|fTlV*mUtM9bLM+6|8r$&$ev!pQgV1J==%(ZQu7*u!t1'
    b'ZZN{8FP{G{uAnzhkkaaaSSFKRZJN)4LFmEaDFeiME0qQB*0JeeH0`|4xC{R8wK(}_z%Rt<MU{jy3=bE-'
    b'A5rC@jnUI(JN_NtbTqob*g9el6#w{><|_hh2BX|HGAIm)`83R8DG6N1G5ks!=n;U?5>rMon^o)d_G(lhZgi9@dgXj-'
    b'R|D;;JY+q*Yv=c*E&mI#i$DrjNR*HVYe_Meh3$F-3wL*P{i1@Jeu&Q#1S-'
    b'@9XRgH0iO{2_;9AAsKq3K;k36v}%l`}$t$%1%1TI|JQI4Pk!P?SK7^^*fy}=%6@kka*N>=As3dJLx~W#W<bAuokHZ-'
    b'y~vMRB}JUq-lI28^6-)-'
    b'WT`wRmPJWG9AzO?=mQbD)WEs4C)h4;<(&$&%O}YbLT3ox&dhw!gM{IDvbYuX`EJ0c*~wG@$G6J33+mA5Q+^za7&|K#$Hlw)xYowN'
    b'@fg2#25GTXxPQz^02D*`~erRRAqCjdVO1v_9Cq+3kx#gDZ-LC!=LtF${rjGQ@P|*`FHN}mcU1~>DT!Rwt80qv8S;|HhFeIi^Ils9'
    b's1>#{+lmu>*jfk(f8Eco2qK)4t!d;%?_vzg7sVX`LwO#JSta%TWqcG*bzzSLV2c!2BG^{xdz#V{QNml{Cz-'
    b'v=lLy~7BAX#UW^E<b>OkU@H$=l%sDclEogf$aW&NCajk)r0^@d7=vFEfo|xwguqW}ABNKS@sk2>hJLz$C*EO5g40fh{!2l!`XnCF'
    b'GS^{}{8=#vd?L0bd{o-&~bm^0%r{1=^Tcl488Yum9A3*~gKH>(FZX0RcR4><X4om_`Ph9}Pqu^@wlWa(?sjal4pbC<-'
    b'q4~*FhH@^YajHs|#b)EN_=3MD4dA+s&^-8d>t98e3=ME>-42X`u!K&Iv<}Gn(LX_Ti^DZPKIF^Ej7q-'
    b'hegN#}nY$~cF}6#U?c2hP5R1>zrKEGC8o(VKejF`(QHKi70(ggptGc?B9#=^i))JkiUFwEh&+8Cs)lOM2q|AeCzj0Fz1Q<UL867{'
    b'ypHXon5y92l2R!<+ULZeN+J^U5cX3*1J`m=ksuJvxw5195n<K1wuOmSg34Iy}`wms1egR!P8yL^qXRu6fW#>q?>VP#SFL0>d>|X#'
    b'^`)u`g;9o<1x#ONsJ{)Hu=*q><CnM%5^lFDf?7V%vwUTS|3x<2#wcJzc!dz%h)m_DT;FlQuDavfC_yF2UjCT6szJ&ADlE_e=KtJ5'
    b'e`6LyDI|(DGDLGcRv~_tXKgC54Wd-AM8lCiZ3s%>xm4bqfPU|@)6r62?Qt-wA0=igo<z$JPVjWMnYbubc9-'
    b'w8dnxnq3bq_0o+#KL=sYQ(^E!a2aB5C!T)W_>RW+jv8q(2ORI=)0BewvV~_vp5Wdfb(tgm2v<qSKuhv;nNI-'
    b'CX*)Qp+8=4ow#YD7H3rYLJkK!ZzQo4MOjWRQ?3+Pq2_kbsdKC&%}>YZ^0%kC^iJ-tx)W5rpiC>KK`Iqrd~Z{6(x(5NqmZ=|C4Y1_'
    b'oiMRW2+M=UvKh%`vAX$4M>jGoztnsYRS(j`>rv7J2QlQ;{ee8^usyyshN>3z#eFeU-'
    b'c;b8D0AAqb+T<qBRrvR=C}IB&Iom^TJsEyP8(y!l!aOk3wO2Xa1Zdnxuqkht2t1*Y377WiWdrLzo*08&Uj!|L_0(f9?O;>9bz1M?'
    b'xWvROWg};M^hy_gsTjNI{Nt^Xgwy=%*+nEa#2RTb!#t>r{C;eO4)6GUFB<xtyVxitafbbUSlTdROyRxvHr>Q%M%Ot|Mm0XC;y-'
    b'vD-D#u7-'
    b'G(kX5RI=cVoF+hC%w`7oVy47`<35!5<<>&Ko5Vur>tBf2gHe7`{}{4ZLlas`wW*fYKUUfrK&fUXVB+<9fookTaUR9LD&7@LR-'
    b'B2u#hro^Gkk&mdD*#oS5E)MzE>>qr#jQ+Nc$eo?w?Dld*2^(%7bKldv>~*;nL%0EFJDag<OtHBx*v5A|)O6gnu4PS(ho~I6ma|Gc'
    b'YM<chllxQI;m>@>+vBBfP_)2qQR}<M88rTQ{<-cM^_HAoRoyl&n9b!V-'
    b'9ymQH}Ns=g`p4ElwIXj<Ktxg5yI&ZE?53RgEdIVmLh%SRZ`xHK))SwpDviRueu|_t5DG9dBX2a5!Tjr;3~IvwPCkc<Iql(Cjm@Jx'
    b'><ci!=&!7>e~CdC@zRUVKC`o-'
    b't`G9O7vt2^d9dd$n1gqI@Cl@(FRrF06QWkE3tuoCWIx573dcE0q7h#iwx>cq~;?Pi2qDZ4cC3v2+CPmGi+T{v~}W_{RH><dENuTy'
    b'66&m#h@l2X-NU}we<`;w9Fv}xx6|eo$U7by?&+I64f4E{3{-'
    b'd5~F$W^=)G+*em3*R~t1PdI;w3c*Wgh=SBX+UZgorSCiWU6c*fhDJE}!c<$XNjfbDBLrGLiR$OKhMJ#+Z;$#0Q5O;@olV&;Gq{o!'
    b'eZ)@MxwlkDP%^9*f$uww@D&8VYLb)JTKfi}z-`8=#&_8?m%Ng8Aa@bK6@=|u8K%+DePEg6%F-'
    b'E?z^L2ka_Wbh1b_ekddC$_oYFdNENB2mZnpIIu4JRTmI^*FwbW;;lnTE3v<ABf97m~|cUxEqf4a)He#cc6FTuD*sg(0~T{}8zw*{'
    b'kZ+2GTvV2hB=6D4q<?Cj*_sG5N#s0{(NHh#}uz2+Ye<>+OebC=2Dj=&7-'
    b'$q`Vz`hvy4$<Pih82Z(6|D8_W1idPFUBp^=!@7DTt3a;e;b!CGWH`0?!VrEOib<hgSG8Un-'
    b'>#(8P@(`t3Uh!BLRqJ73*C}IXm#By0vZPff@Qqc^NN#F6vF{-VX-'
    b'`X~Dj~T4k*`kyxm*8`znv_v@F#e(4SmqgcC%Y<dRn$2`RhkXlI9UTGV;4>*90`RCZbf`^|v=1w8cS5IoWd5%ol>H>OM3cTu;DFp{'
    b'lPLy7mBlH>2if`9xEP6a6knwIAyfrnIbDOmKgU&-'
    b'HRIs<W6x^p}`$^L$@jK^0zb)<boL6N{f&92DU3R<km^j1=#PDtY4G&RTmssl5WN?v|w!M!rv;%^yGFKUx&GKE!9P3N2iO_7I!aXZ'
    b')IL@=KuLbt-8D%BbXEy#frL<Zv!~I3<1$@uhz+r+Y8>@yB(sbnPFq`vwUMDH-~#p$u<o5Sq3e+7i#5sr#s#<!7&o{H@=xqm54`D-'
    b'$~umk&UI!f7C0<$s?I#sSiJ=a@eamBHKSw?j$rFYa{<aNd}T{=22U+GP<3lNxf#Y1XfDp?Lo)V!lT;q3vl5jz`rmW822+DRe*Z_U'
    b'6|D41w1!3pZ*P@w)7R@N?Z=@zcb6xQ2Xo;+t#g?p%_%Dp419_C7kl?hpLFD)b1D*FU3~d8ylZe5HAB_HqbZSJhmd=d5K7K}tDyt1'
    b'tYgOX;({)o|(mRowTfZnB+*!`w^5;2<cDD~J~vMuTdF9h^fWuh}cN<Jlc2(CVD8wr8|{(t1~O+0M0u%V7ZB(=GxrNXfBlV0z4YB;'
    b'GbWZqxq@INOTafxL5Cin+diV8>JWMLggtM0Q;bqS)I%H<W4qaIP3E@dcnxyvX|;#uNRL_0*byLo->j<|%OJ=cABN<bgiRp-'
    b's|&O+eSDwhFXbDxI)>e2K2+x?fbt%vz8FDqGnfoOWwA67Iz#Q&NVg$(al9r9B)3j!1tV@!0Cdd&DfL3!jJfX5X8Xt0cCoTw<A4Z2'
    b'f3hkcb1CmhkUJKRNu5)<}spT!KemSaXfjmo20{eGOi{3@I821y0bbG!X1}Yl$mNrUS`;(QmnF;wmSk?6xSbG@yFBJVQsUyo2vtmw'
    b'f)UQI#!|+>p#Ve`b=Z6GVjvf<m0Ctr89GWOGJg4p*Ln^lbWltD7VmFmuPJ<9hu^gf0Mt?k&W5zTM=}6mEz9FEV;K>nNbK{5XYRK}'
    b'Z=Y_dvT4<u^=gO{wvZ03G46!^)F0SSsTYA92NVYd1+~%i7?E^z?hk`MW9+|GlYucV#yssuq)6f>roc9w(#MO?14&;m<ujxjhGO`w'
    b'}`?pBvt~(QU*0==h&&oJou2<zOw`^V6ui-CG}#=k@3j&uNW26`k42YJbI91;+vG6n^!(6G%>n9#wUn({-'
    b'YjII5~KscK#>1YFJOzvCXt`*7zuDwN-%1m%97$1O%J6f=>qMTO+!-'
    b'VS_JW#Hf!jjhU2gMWxsnoESLjIEOv<#SD)@S&g~)L==AJ6B_Y;bH-Usf0`dRluVD?S$}j9@5Ag!Q}wS6anNg<aegc&dDc@MC0evO'
    b'~fU0!am2!Uf=zDHvF^#?2lr{p}=*)-'
    b'}<nG477CH{jo)n#agQv_npQrmnAU%?QwDjx9ek<L+7{vL?GJT$%kpt3y@y`KYX?15`Am;MIr|Hf{yu`>8!ljfT*s1sz>d{@8nZy('
    b'x^J9(qv0nq^kXqV=I^DCO4#@@eMU`IP!51$Uhf1h~RKnTG|J6b;b#T#No7@o2@R{s&<zxpe-le@(slOH5@{GZXYgjHpd$X_&JUB*'
    b'6|UG)@p6J)W3b+dC8h%-Y`+#Qky0HR4=u|B>2M!xU_kamV!#`ifJm>a&h`eW?XO}+o;!ezp=&;&0l9#GW=tA`uY-'
    b'!oYYIMF%v%?Em76yT;26*MN?FAy|WV{OFh^-'
    b'{rVQ1vZwZ$9n9c0sM*e?X$i*HtiO?z0G7lkvY$vijGOH2M2qXW{~=MEU~mC|h2|>Fb|4`&7eGT+TXIZwl^T#=TY>^yb6S#n7Q_2L'
    b'-pP)t#LoM<(^}+}&j49(&;iM$f6!izW(qn_yTv;#Am6T5@}v0-'
    b'sQ=ZhQ`DY!IcwcMbvr<K_XKAqVY#BX%DV4ede@kf5{vFAls!UlrWqZ<A^e)+AaT*L;%s+_7vyS7j~?6#>QcmmIHj!9s}?8m=*q`o'
    b'fv^m$g5}PwS*v_K!CXz{i^uZ08A~eG;k^*H7ugD!4YBJkxW%)$Nno~Ynu4`C0*gxw951M)l1GG5#s0oMLh;X}GP+)vqYoV>b{y;6'
    b'2NgR_-Bc!6Lm}gjldA*a%5uu)G%Oc?+fkG)=oZSDVC0`-*58oCytX6*h}G5Xk%H!MOF;ZM>A-)HS9-'
    b'LA!MSKU*Us))fA)Z|=Vtyte+W$gpkGi8BqT5<@NErUKS>j{$y2YaYbC%DAP8xVdbL-upnEH@nV(7F&=Z1Ju$1?H8)pn4JDmV*Hy5'
    b'*LEu!@JjFV_V#1=TemKLFj<ILT^*PHFZ4=7c*cr$_P$+aH($yo?hR@<pd{^P4`w5x(dTP>2S$awyr{~xuqE_('
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
    candidate = remove_vowels  # noqa: F405
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
