import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [['Hi, my name is John'],
 ['One, two, three, four, five, six'],
 ['Hi, my name'],
 ['One,, two, three, four, five, six,'],
 [''],
 ['ahmed     , gamal'],
 [',,,,'],
 [' '],
 ['Elephant,giraffe,,lion,zebra'],
 ['Hi,there is,a lot,of,space   ,     ,'],
 ['        '],
 ['apple,'],
 ['cat dog, fish'],
 ['hello,  world'],
 ['One,two ,  three , four'],
 ['The quick brown fox jumps over the lazy dog'],
 ['hello,  oworld'],
 ['         '],
 ['The quick brown f the lazy dog'],
 ['          '],
 ['The quickbrown f the lazy dog'],
 ['   '],
 [''],
 ['The quickbrowny f the lazy dog'],
 ['The quTick brown f the lazy dog'],
 ['The quick brown fox jumps over tohe lazy dog'],
 ['The quickbrown y dog'],
 ['One,two ,  three , fouOne,two ,  three , fourr'],
 ['cagt dog, fish'],
 ['Elephant,gieraffe,,lion,zebra'],
 [',,'],
 ['The quickbrown  dog'],
 [',The quTick brown f the lazy dog,'],
 ['cat dofish'],
 ['hehello,  oworldllo,  oworld'],
 [' cat dofish       '],
 [',         ,The quickbrown  dog'],
 ['The quTick brown f One,two ,  three , fourthe lazy dog'],
 [',The quTick bThe quick brown fox jumps over tohe lazy dogrown f the lazy dog,'],
 ['The quTickf the lazy dog'],
 ['app cat dofish       e,'],
 ['The quTicat dog, fishckf the lazy dog'],
 ['The quTicat dog, fishckf the lazy doyg'],
 [',,,,,'],
 ['         appl e,'],
 ['The qucfTickf the lazy dog'],
 ['XUI'],
 ['hllo,  wold'],
 ['One,two ,  three , fouOne,thello,  oworldwo ,  three , fourr'],
 ['app,The quTick brown f the lazy dog, cat dofish       e,'],
 [' The quTickf the lazy dog  '],
 ['cat dofis'],
 ['Theh quTicat dog, fishckf the lazy doyg'],
 ['The quTickTheh quTicat dog, fishckf the lazy doyg brown f the lazy dog'],
 ['Tx jumps over tohe lazy dog'],
 ['The quick brown f,The quTick br own f the lazy dog,ox jumps over tohe lazy dog'],
 ['cat dhofishOne,two ,  three , four'],
 ['The quick brown fox jumps over tohe lazy dog      '],
 ['cT he quTick brown f One,two ,  three , fourthe lazy dogt dofis'],
 [',,,'],
 ['The quTick brownThe quickbrown y dog f One,two ,  three , fourthe lazy dog'],
 ['The quTicat dog, fishckf the l         appl e,azy dog'],
 ['The quTick brown f the lazy The quicThe quick brown f,The quTick br own f the lazy dog,ox jumps '
  'over tohe lazy dogk brown f,The quTick brgdog'],
 ['The hquickbg'],
 ['Tx xjumps over tohe lazy dog'],
 ['The quTick brownThe quickbrown y dog f One,two ,  three , fourthe flazy dog'],
 ['Elephant,         appl e,giraffe,,lion,zebra'],
 ['The quTicat dog, fishckf the l         appl e,azy dogI'],
 ['   Theh quTicat dog, fishckf the lazy doyg      '],
 [' he quTickf the lazy dog  '],
 ['Theh quTicat dog, fishckf the lazy The qucfTickf the lazy dogdoyg'],
 ['cat dfofish'],
 ['XI'],
 ['Hi,there is,a lot,of,space  cT he quTick brown f One,two ,  three , fourthe lazy dogt dofis '
  ',     ,'],
 ['eesrvDWbLL'],
 ['The quick bThe quick brown f the lazy dogrown fox jumps over tohe lazy dog'],
 ['cagt dogfish'],
 [' hOne,two ,  three , foure quTickf the lazy dog  '],
 ['The qkuickbrown y dog'],
 [',The quTick bT,,,,he quick brown fox jumps over tohe lazy dogrown f the lazy dog,'],
 ['  '],
 ['app cat dofish       e,Elephant,gieraffe,,lion,zebra'],
 ['The quTick brown f the lazy The quThe quickbrown f the lazy dogicThe quick brown f,The quTick '
  'br own f the lazy dog,ox jumps over tohe lazy dogk brown f,The quTick brgdog'],
 ['   Theh quTicat dog, fishckf the lazy doyg     '],
 [',         ,The quickbrown  dobg'],
 ['The quTiThe queri tohe lazy dogk brown f,The quTick brgdogckf the lazy dog'],
 [' The quTickf the lazy dog The quick brown f the lazy dog '],
 ['The qu  dog'],
 ['hello, l oworld'],
 [',The quTick bT,,,,he quick bro,wn fox jumps over tohe lazy dogrown f the lazy dog,'],
 ['Elephant,         appl e,girTx xjumps over tohe lazy dogaffe,,lion,zebra'],
 ['       '],
 ['The quick ybrown f the lazy dog'],
 ['One,two ,  three , fouOne,two ,  thre fourr'],
 ['cat dhofishne,two ,  three , four'],
 ['cat dofiElephant,         a,ppl e,girTx xjumps over tohe lazy dogaffe,,lion,zebras'],
 ['TThe quTick brown f One,two ,  three , fourthe lazy doghe qck brown f the he quTickf the lazy '
  'dog   lazy dog'],
 ['hello,  woXUIrld'],
 [' hOne,two ,  three , foure quTickf thef lazy dog  '],
 ['Hi,there is,a lot,of,space  cT he quTick brown f One,two ,  three , fourthe lazy dogyt dofis '
  ',     ,'],
 ['Theh quTicat diog, fishckf the lhazy The qucfTickf the lazy dogdoyg'],
 ['cat dog,  fish'],
 ['         apple,'],
 ['hHi,there is,a lot,of,space  cT he quTick brown f One,two ,  three , fourthe lazy dogt dofis '
  ',     ,llo,  wold'],
 ['hwoXUhIrld'],
 ['Hi, my    name   is John. How     are    you?   '],
 ['The,quick,brown,fox,jumps,over,the,lazy,dog.'],
 ['Two spaces after,  one space before  , and no spaces in between'],
 [',,,,,,No words, here,,,,,,'],
 ['   A  random    string    with     no    commas     or   spaces'],
 ['Amazing, how a sentence can change, meaning just by, adding or removing, commas!'],
 ['Multi\nline\nstring\nHello,\nworld!\n'],
 ['President, John, F, Kennedy'],
 ['The quick brown fox jumps over the lazy dog.'],
 ['ThisStringHasNoSpaces'],
 ['Muluti'],
 ['   A  random    string    wiorth     no    commas     or   spaces'],
 ['eB'],
 ['   A  random    string    with      no    commas     or   spaces'],
 ['Multi\nline\n\nstring\nHello,\nworld!\n'],
 ['Amazing, how a sentence can changee, meaning just by, adding or removing, commas!'],
 ['The quick brown fox jumps over the lazydog.'],
 ['The quick brown fox jumps over th e lazy dog.'],
 ['The quick browner th e lazy dochangee,g.'],
 ['B'],
 ['change,'],
 ['is'],
 ['Multi\nline!\nstring\nHello,i\nworld!\n'],
 ['th'],
 ['line'],
 ['you?'],
 ['The quick brown fox jumps over change,the lazydog.'],
 ['Mullti'],
 ['   A  random    string    with      no    commas     or    spaces'],
 ['yMulti\nline!\nstring\nHello,i\nworld!\n?'],
 ['line!'],
 ['Hi, my    name   is   A  random    string    wiorth     no    commas     or   spaces John. '
  'How     are    you?   '],
 ['space'],
 ['The quick brown fox jumps over tarelazy dog.'],
 ['The quick browner th e lazy do changee,g.'],
 ['BeB'],
 ['jumps'],
 ['   A  random    string    with      no    commas    r or   spaces'],
 ['Hello,i'],
 ['The quick brown fox jumpwiorths over tarelazy dog.'],
 ['onwords,e'],
 ['The quick brown fox jumps ovMultier tarelazy dog.'],
 ['Amazing, how a sentence can change, meaning ovMultierjust by, adding or removing, commas!'],
 ['just'],
 ['   A  random    string    wiorth     no    commases'],
 ['Hi, my    name   is JohThe,quick,brown,fox,jumps,over,the,lazy,dog. you?   '],
 ['Helllol,'],
 ['Hicommases, my    name   is John. How     are    you?   '],
 ['The quick b rown fox jumps over the lazy dog.'],
 ['   A  random    string    wiorth     no    commas     or   spacesth'],
 ['The qmpwiorths over tarelazy dog.'],
 ['NWUyMDWJAr'],
 ['   A  random    string    with      no    commas     or   spacesNWUyMDWJAr'],
 ['HellloThe quick brown fox jumps over tarelazy dog.'],
 ['spacesNWUyMDDWJAr'],
 ['ladzydog.'],
 ['Amazing, how a sentence can change, meaning just by, adding or removing, commasAmazing, how a '
  'sentence can change, meaning just by, addingThe quick browner th e lazy dochangee,g. or '
  'removing, commas!!'],
 ['The quick b rown fox jumps over the lazy dog.commases'],
 ['iis'],
 ['dog.commases'],
 ['justt'],
 ['spaces'],
 ['   A  rand om    string    with      no    commas     or with'],
 ['Multi\nline\nstring\nHi,rld!\n'],
 ['John.'],
 ['The quick browneer th e lazy dochangee,g.'],
 ['The quick browner th e lazy randdocPresident, John, F, Kennedyhangee,.'],
 ['HellloThe quickx brown fox jumps over tarelazy tarelazydog.'],
 ['Hi, my    name   is J you?   '],
 ['after,'],
 ['TwoB'],
 ['quickx'],
 ['   A  random    string    wiorth     no    commas'],
 ['TheHi, my    name   is John. How     are    you?    quick brown fox jumpwiorths over tarelazy '
  'dog.'],
 ['the'],
 ['yldadzydoJohn,'],
 ['in'],
 ['cmyTwwoe,'],
 ['The qmpwiorths over tarelazy dog.changee,g.'],
 ['Multi\nline\nstring\nHwords,\n'],
 ['The quick browner th e lazqy dochangee,g.'],
 ['H   A  rand om    string    with      no    commas     or withicommases, my    name   is John. '
  'How     are    you?   '],
 ['Hicommases, my    name   is are    you?   '],
 ['The quick b rown fox jumps oveor the lazy dog.'],
 ['    A  random    string    with      no    comtmas     or    spaces'],
 ['cThe quick browner th e lazy dochangee,g.ommas'],
 ['jumpwiorths'],
 ['Two spaces after,  one space before  , and no speaces in between'],
 ['Hi,rld!'],
 ['spacesThe quick browneer Uth e lazy dochangee,g.NWUyMDDWJAr'],
 ['The'],
 ['MAmazing, how a sentencse can change, meaning just by, adding or removing, commas!uluti'],
 ['dog.commaTheHi, my    name   is John. How     are    yo   A  random    string    with      '
  'no    commas    r or   spacesu?    quick brown fox jumpwiorths over tsarelazy dog.ses'],
 [',ThisStringHasNNoSpaces,,,,,No words, here,,,,,,'],
 ['TheHi, my    name   is John. How     are    you?    quick brown fox jumpwiorths over '
  'tareadding'],
 ['MAmazing, how a sentencse cant by, adding or removing, commas!uluti'],
 ['ThTHello,e'],
 ['The qmpwiorths ovchange,theer tarelazy dogwords,ngee,g.'],
 ['ujumps'],
 ['do'],
 ['Hi, my    nam e   is J you?   '],
 ['on'],
 ['Multi\nl\nstring\nHello,\nworld!\n'],
 ['Multi\n'
  'line\n'
  'strin   A  random    string    wiorth     no    commas     or   spacesthg\n'
  'Hi,rld!\n'],
 ['yldadzydoJowithhn,'],
 ['lninie!'],
 ['Hi, my    name   is John. How     oare    you?   '],
 ['lniniie!'],
 ['or'],
 ['The quick browner th e lazy randdocPresident, John, F,n Kennedyhangee,.'],
 ['are'],
 ['H'],
 ['   A  random    string    wiorth     no    c ommas     or   spaces'],
 ['by,'],
 ['Hi, my    name   is J you   '],
 ['The quick brown fox jumpzs over th e lazy dog.'],
 ['HellloThe quiUthx jumps over tarelazy dog.'],
 ['uThe quick brown fox jumpzs over th e lazy dog.jumps'],
 ['chhownge,'],
 ['linee'],
 ['   A  random    string    with      no    commwords,as     or   spaces'],
 ['nlniniie!'],
 [' A  '],
 ['you??'],
 ['jumpwiordog.ths'],
 ['Two spaces after,  one space before s , and no speaces in between'],
 ['ThTH   A  random    string    with      no    commas     or   spacesello,e'],
 ['BB'],
 ['The quick b rown fox jumps oazy dog.'],
 ['om'],
 ['ThTHrownello,e'],
 ['dog.commaTheHi, my    name   is John. How     are    yo   A  random    string    with      '
  'no    comma  quick brown fdog.ses'],
 ['spacesu?'],
 ['yldadzydcommas!uluti,'],
 ['Multi\n'
  'line\n'
  'strin   A  random    string    wiorth     no    commas     or   spacesthg\n'
  'Hi,rtld!\n'
  'H'],
 ['The quick brown fox jumg.'],
 ['chhowngec,'],
 ['rdandom'],
 ['wiorth'],
 ['meaning'],
 [',,,,,,No words, her,e,,,,,,'],
 ['Amazing, how a sentence can change, meaning just by, addinhg or removing, comma!'],
 ['rdmandom'],
 ['John,'],
 ['rown'],
 ['Multi\nline\nstrHwords,\n'],
 ['TheHi, my    name   is John. How     are    you?    quick brown fox jumpwiorths over tareaddHi, '
  'my    nam e   is J you?   ing'],
 ['ynldadzydoJohn,'],
 ['and'],
 ['dog.H'],
 ['s'],
 ['jusAmazing, how a sentence can cnamehange, meaning ovMultierjust by, adding or removing, '
  'commas!tt'],
 ['dog.commaTheHi, my    name   is John. How     are    yo   A  random    string    with      '
  'no    comma  quick brown cThefdog.ses'],
 ['sentence'],
 ['n.'],
 ['cheange,'],
 ['no'],
 ['Homicommases, my    name   is are    you?   '],
 ['brown'],
 ['TThTH'],
 ['changee,g.'],
 [',,,,,,No'],
 ['spacesNDWUyMDDWJAr'],
 ['Multid\nline\nstring\nHello,\nworld!\n'],
 ['you?o?'],
 ['   A  random    string    wiorth  ThTHello,e   no    c ommas     or   spaces'],
 ['eBThTHello,e'],
 ['cheangeg,'],
 ['yo'],
 ['showu?'],
 ['spsaces'],
 ['H    A  rand om    string    with      no    commas     or withicommases, my    name   is John. '
  'How     are    you?   '],
 ['dog.comyldadzydcommas!uluti,mases'],
 ['The quick brown fox jAmazing, how a sentence can change, meaning just by, adding or removing, '
  'commasAmazing, how a sentence can change, meaning just by, addingThe quick browner th e lazy '
  'dochangee,g. or removing, commas!!umg.cheangeg,'],
 ['BrandomeB'],
 ['   A  random    string    with       no    commas     or   spaces'],
 ['The qu ick b rown fox jumps over the lazy dog.commases'],
 ['Bra'],
 ['iiis'],
 ['rdmandoom'],
 ['words,'],
 ['spacesNDWUyMDDWJAspacesNDWUyMDDWJArr'],
 ['Multi\nlinjumpzs\nworld!\n'],
 ['i'],
 ['browns'],
 ['how'],
 ['cThe quchange,theick browner th e lazy dochangee,g.ommas'],
 ['change.e,g.'],
 ['rThe quick brown fox jumps over change,the lazydog.dmandoom'],
 ['lninile!'],
 ['Multi\n'
  'line\n'
  'strin   A jumpwiordog.ths random    string    wiorth     no    commas     or   spacesthg\n'
  'Hi,rtld!\n'
  'H'],
 ['sshowu?'],
 ['   A  random    string    wiorth  ThTHello,e comma!  no    c ommas     or   spaces'],
 ['jumpzs'],
 ['quiUthx'],
 ['o'],
 ['commas!!'],
 ['commas!'],
 ['   A  random    string    with     no    commas     or   spacesNWUyMDWJAr'],
 ['cThe quick browniiiser th angee,g.ommas'],
 ['l   A  random    string    wiorth     no    commas     or   spacesth'],
 ['sentesnce'],
 ['brn'],
 ['cThe theick browner th e lazy dochangee,gn.ommasThTH'],
 ['cnamehange,'],
 ['oveor'],
 ['taMultireaddHi,'],
 ['rdmandoHello,'],
 ['Multi\nline\nstring\nHi,rd!\n'],
 ['commasAmazing,'],
 ['BBThe qmpwiorths over tarelazy dog.changee,g.'],
 ['spacesNDWUThe qmpwiorths over tarelazy dog.changee,g.yMDDWJAr'],
 ['FLoaost'],
 ['before'],
 ['namouu?'],
 ['   A  random    string    with      no    c'],
 ['The qmpwiorlazy dog.'],
 ['sadding'],
 ['uThe quick brown fox jumpzs oveth e lazy dog.jumps'],
 ['Hi, my    name   is John. How   i  oare    you?   '],
 ['cThe quick browner th e lazy dochangee,g.omm,as'],
 ['tarelazy'],
 ['inor'],
 ['wBBTheith'],
 ['spaace'],
 ['Multi\nline\nstTherHwords,r\n'],
 ['orHi,'],
 ['yo   A  random    string    wiorth     no    commas???'],
 ['quick'],
 ['H    A  rand om    string    with      no    commas     or withicommases, my    name   is John. '
  'How  spaace   are    you?u   '],
 ['adding'],
 ['jumThe qu ick b rown fox jumps over the lazy dog.commasespzzs'],
 ['The quick b rown fox quickjumps over the lazy dog.'],
 ['spFLoaostacesNDWUyMDDWJAr'],
 ['oazy'],
 ['dochangee,g.ommas'],
 ['sho?wu?'],
 ['tTwo spaces after,  one space before  , and no spaces in betweenh'],
 ['yMulti\nline!\nstrin!g\nHello,i\nworld!\n?'],
 ['Two spaces aaf,ter,  one space before  , and no speaces in between'],
 ['o   A  random    string    wiorth     no    commases'],
 ['brlineen'],
 ['The quick brown fox jumps over tqhe lazydog.'],
 ['JohThe,quick,brown,fox,jumps,over,the,lazy,dog.'],
 ['dochangee,g.'],
 ['The,quick,brown,foxdogwords,ngee,g.er,the,lazy,dog.'],
 ['juust'],
 ['   A  random    string    with     n o    commas     or   spaces'],
 ['   A  random    string    wiorth  ThTHelo,e comma!  no    c ommas browner    or   spaces'],
 ['spacesu?,,,No'],
 ['ii'],
 ['Homicommases, my    name   is are    you'],
 ['brlJohn.bineen'],
 ['youlniniie!?o?'],
 ['sadspacesNWUyMDWHellloThe quickx brown fox jumps over tarelazy tarelazydog.JArding'],
 ['s!!'],
 ['beore'],
 ['spa   A  random    string    wiorth     no    c ommas     or   spacesace'],
 ['iThe quick brown fox jumps ovMultier tarelazy dog.'],
 ['n'],
 ['l   A  random    string    wiorth     no    commas     or   spaesth'],
 ['The quick brown fox jAmazing, how a sentence can change, meaning just by, adding or removing, '
  'commasAmazing, how a sentence can change, meaning just by, addingThe quick browner th e ulazy '
  'dochangee,g. or removing, commas!!umg.cheangeg,'],
 ['change,jumpwiths'],
 ['   A  random    string    with      no    commas     or   spaceTheHi, mry    name   is John. '
  'How     are    you?    quick brown fox jumpwiorths over tareaddHi, my    nam e   is J you?   '
  'ingsNWUyMDWJAr'],
 ['cochange,themmas!!'],
 ['tTwo spaces after,and no spaces in betweenh'],
 ['MAmazing,'],
 ['The quick browspacesNWUyMDDWJArn fox jumps over th e lazy dog.'],
 ['?'],
 ['   A  rand om   i string    with      no    commas     or with'],
 ['dog.commaTheHi, my    name   is John. How     are    yo   A  random    string    withrown      '
  'fno    comma  quick brown fdog.ses'],
 ['ulazy'],
 ['tTwo'],
 ['rdmaoom'],
 ['HelloH,i'],
 ['arBBThe qmpwiorths over tarelazy dog.changee,g.e'],
 ['Mulluti'],
 ['Two spaces after,  one space before  , and no speaces in sbetween'],
 ['e'],
 ['onon'],
 ['seHellloThe quiUthx jumps over tarelazy dog.ntesnce'],
 ['ooazy'],
 ['   A  random    string    with      no    commwords,as     The qmpwiorths over tarelazy '
  'dog.changee,g.or   spaces'],
 ['oare'],
 ['Hhe'],
 ['Multi\n'
  'line\n'
  'strin   A jumpwiordog.ths random    string    wiorth     no    commas     or   spacesthg\n'
  'Hig,rtld!\n'
  'H'],
 ['yo   A  random    string c   wiorth     no    commas???'],
 ['   A  random    string    with  ddHi, my    nam e   is J you?   ingsNWUyMDWJAr'],
 ['random'],
 ['H   A  rand om    string    with      no     commas     or Hwithicommases, my    name   is '
  'John. How     are    you?   '],
 ['dog.commaTheHi, my    name   is John. How     are    yo   A  random    string    with      no '
  'h   comma  quick brown cThefdog.ses'],
 ['nrandon'],
 ['sbetween'],
 ['dog.commaTheHi, my    name   is John. How     are    yo  s A  random    string    with      '
  'no    commas    r or   spacesu?    quick brown fox jumpwiorths over tsarelazy dog.ses'],
 ['jumThe'],
 ['FLspacesTheoaost'],
 [' e  A  rand ocommas     or with'],
 ['President,'],
 ['Hello,'],
 ['jumg.'],
 ['ocommams'],
 ['commas???lniniie!'],
 ['angee,g.ommas'],
 ['broowns'],
 ['FWR'],
 ['quicckx'],
 ['The quick browsl   A  random    string    wiorth     no    commas     or   '
  'spacesthpacesNWUyMDDWJArn fox jumps over th e lazy dog.'],
 [',,,,,,,No words, here,,,,,,'],
 ['   A  random    string    with      no    commwords,as     odr   spaces'],
 ['President,yldadzydoJowithhn, John, F, her,e,,,,,,Kennedy'],
 ['yldadzydog.jumpslydoJowithhn,'],
 ['Hellloll,'],
 ['Two spaces after,  one spaces beforfe  , and no spaces in beMulti\n'
  'line\n'
  'string\n'
  'Hwords,\n'
  'tween'],
 ['   A  random    string    wiorth  ThTHelo,e comma!  no   c ommas browner    or   spaces'],
 ['br   A  random    string    with      no    dcoowns'],
 [','],
 ['nn'],
 ['H    A  rand om    string    with      no   her,e,,,,,, commas     or withicommases, my    '
  'name   is John. How  spaace   are    you?u   '],
 ['commasMullti!!'],
 ['The quick brown fox jAmazing, how a sentence can change, meaning just by, adding or removing, '
  'commasAmazing, how a sentence can change, meaning just by, addingThe quick browner th e ulazy '
  'dochangmas!!umg.cheangeg,'],
 ['cThe theick browner th e lazy l   A  random    string    wiorth     no    commas     or   '
  'spaesthdochanngee,gn.ommasThTH'],
 ['The qfuick brown fox jumg.'],
 ['commas!!umg.cheangeg,'],
 ['taHelloH,iMultireaddHi,'],
 ['youlniniie!?o?   A  random    string    with      no    commwords,as     or   spaces'],
 ['John.inor'],
 ['oyo'],
 ['The quick brown fox jumps over the lazyy dog.'],
 ['TheHi, my    name   is John. How     are    y ou?    quick brown fox jumpwiorths over '
  'tareaddHi, my    nam e   is J you?   ing'],
 ['ThTHelo,e'],
 ['The quick brown fox jAmazing, how a sentence can change, meaning just by, adding or removing, '
  'commasAmazing, how a sThe,quick,brown,foxdogwords,ngee,g.er,the,lazy,dog.entence can change, '
  'meaning just by, addingThe quick browner th e ulazy dochangmas!!umg .cheangeg,'],
 ['The qmpwiorths ovchange,withs,ngee,g.'],
 ['oyoo'],
 ['Hi,rd!'],
 ['Two spaces after,  one space before  , andspFLoaostacesNDWUyMDDWJArspeaces in between'],
 ['The quick b rown fox jumps over the lazy dmases'],
 ['yldadzydog.jumpslydoJowthhnu,'],
 ['spaesth'],
 ['The qmpwiorths ovchange,withs,ngee,g.Hi,rd!'],
 ['cThe quick browner th e lazy dochangee,g.omjumThe qu ick b rown fox jumps over the lazy '
  'dog.commasespzzsmas'],
 ['HigarBBThe qmpwiorths over tarelazy dog.changee,g.e,rtld!'],
 ['adnd'],
 ['jarBBTheuust'],
 ['jummps'],
 ['F,n'],
 ['dog.commaTheHi, my    name   is John. How     are    yo  s A  random    string    with      '
  'no    commas    r or   spacesu?    quick brown fox jumpwiorths over tsases'],
 ['dog.cogmmases'],
 ['   A  random    string    wiorth  ThTHespacesNDWUyMDDWJAspacesNDWUyMDDWJArrlo,e comma!  no   c '
  'ommas browner    or   spaces'],
 ['linee!'],
 ['Hicommases,'],
 ['nTLxTIkG'],
 ['cTehe quick browner th e lazy dochangee,g.ommas'],
 ['dog.commaTheHi, my    name   is John. How     are    yo  s A  random    string  ThTHuick brown '
  'fox jumpwiorths over tsases'],
 ['TheHi, my    name   is John. How     are    you?    quick brown fox jumpwiortyhs over tarelazy '
  'dog.'],
 ['cnamehangrandome,'],
 ['cThe quick browner th e lazy docahangee,g.omjumThe qu ick b rown fox jumps over the lazy '
  'dog.commasespzzsmas'],
 ['ce'],
 ['sa'],
 ['oo'],
 ['MAmazing, how a sentencse can change, meaningb just by, addin!ulunti'],
 ['TheHi, my    name   is John. How     are    aryou?    quick brown fox jumpwiortyhs over '
  'tarelazy dog.'],
 ['ddHi,'],
 ['   A  random    string    with      no    commwords,as The quick browneer th e lazy '
  'dochangee,g.    The qmpwiorths over tarelazy dog.changee,g.or   spaces'],
 ['dog.commaTheHi, my    name   is John. xHow     are    yo  s A  random    string    with      '
  'no    commas    r or   spacesu?    quick brown fox jumpwiorths over tsases'],
 ['spacesNDWUWyMDDWJAspacesNDWUyMDDWJArr'],
 ['rddandom'],
 ['lin'],
 ['chspacesNDWUThe qmpwiorths over tarelazy dog.changee,g.yMDDWJArwngec,'],
 ['lazydog.'],
 ['ovchange,theer'],
 ['theick'],
 ['The quick brown fox jumps over th e l dog.'],
 ['b'],
 ['cheangMulti\nline!\nstring\nHello,i\nworld!\ne,'],
 ['Hello,rds,ngee,g.'],
 ['saspa   A  random    string    wiorth     no    c ommas     or   spacesacedding'],
 ['JohThe,quick,brown,fox,jumps,over,the,tlazy,dog.'],
 ['uThe quick brown fox jumpzs over th e lHi, my    name   is   A  random    string    wiorth     '
  'no    commas     or   spaces John. How     are    you?   azy dog.jumps'],
 ['The qmpwiorths over tarickelazy dog.changee,g.'],
 [' AMulti\nline\nstTherHwords,r\n  '],
 ['uThe quick brown fox jumpzs over th e lHi, my    name   is   A  random    string   Multi\n'
  'line\n'
  '\n'
  'string\n'
  'Hello,\n'
  'world!\n'
  ' wiorth     no    commas     or   spaces John. How     are    you?   azy dog.jumps'],
 ['iiiis'],
 ['   A  randomstrHwords,    string    with      no    commas    r or   spaces'],
 ['yo   A  randomas???'],
 ['spsacesTheHi, my    name   is John.The quick b rown fox quickjumps over the lazy dog.readding'],
 ['commas???lnine!'],
 ['dog.'],
 ['The quick brown fox jueBThTHello,emps over change,the lazydog.'],
 ['spa'],
 ['dog.commaTheHi, my    name   is John. How  Two spaces after,  one space before  , and no spaces '
  'in between   are    yo   A  random    string    with      no    commas    r or   spacesu?    '
  'quick brown fox jumpwiorths over tsarelazy dog.ses'],
 ['yMulti'],
 ['ingsNWUyMDWJAr'],
 ['The quick brown fox jumps over tarelazy doTwo spaces aaf,ter,  one space before  , and no '
  'speaces in betweeng.'],
 ['omas'],
 ['uHjumThe'],
 ['aaf,ter,'],
 ['jusAmazing, how a sentence can cnamehange, meaning ovMultierjust by, adding or removing, '
  'commas!tquickxtUth'],
 [',T'],
 ['rom'],
 ['dog.changee,g.yMDDWJAr'],
 ['ldog.changee,g.yMDDWJArwngec,zydog.'],
 ['The quick brown fox jAmazing, how a sentence can change, meaning just by, adding or removing, '
  'commatTwosAmazing, how a sThe,quick,brown,foxdogwords,ngee,g.er,the,lazy,dog.entence can '
  'change, meaning just by, addingThe quick browner th e ulazy dochangm!!umg .cheangeg,'],
 ['yMulti\n'
  'line!\n'
  'string\n'
  'HecThe quick browner th e lazy docahangee,g.omjumThe qu ick b rown fox jumps over the lazy '
  'dog.commasespzzsmasloyolo,i\n'
  'world!\n'
  '?'],
 ['lazy'],
 ['Multi\nline\nstTheerHwords,r\n'],
 ['Amazing, how a sentence can change, meaning ovMultspeacesierjust by, adding or removing, '
  'commas!'],
 ['yMulti\nline!\nstring\nHello,i\nworl!\n?'],
 ['F,'],
 ['dog.commaTheHi, my    name   is John. How     are    yo   A  random    string    withrown      '
  'fno    comma  quick brs'],
 ['TheHi, my    name   is John. How     are    you?    quick brown fox jumpwiorths ov er '
  'tareaddHi, my  jusAmazing,  nam e   is J you?   ing'],
 ['The quick  b rown fox jumps over the lazy dog.'],
 ['eBThTHelleo,e'],
 ['cTehe'],
 ['Ammazing, how a sentence can changee, meaning just by, adding or removing, commas!'],
 ['h'],
 ['chspacesNDWUThe qmpwiorths over tarelazy dog.changee,g.yMtDDWJArwngec,'],
 ['jumpwiortyhs'],
 ['Hi, my    nameonon   is J you?   '],
 ['Two spaces after,  one spaces beforfe  , and no saces in beMulti\nline\nstring\nHwords,\ntween'],
 ['ohvchange,tMulti\nlinjumpzs\nworld!\nheer'],
 ['eBtarickelazy'],
 ['yldadzydog.jumpslydoJowithhnn,'],
 ['hth'],
 ['The qmpwiortths ovchange,withs,TwoBngee,g.Hi,rd!'],
 ['Hicommases, my    namem   is are    you?   '],
 ['uThe quick brown fox jumpzs over th e lHi, my    namer   is   A  random    string    witTwo '
  'spaces ohn. How     are    you?   azy dog.jumps'],
 ['cThe q,uick browner th e lazy dochangee,g.omm,as'],
 ['comminors???'],
 ['dog.changee,youlniniie!?o?g.yMDDWJAr'],
 ['Multi\n'
  'line\n'
  'strin   A  random    string    th     no    commas     or   spacesthg\n'
  'Hi,rtld!\n'
  'H'],
 ['Multi\nline\nstring\nHello,qmpwiorths\nworld!\n'],
 ['browsl'],
 ['   A  random    string    wiorth  ThTHelo,e comma!  no   c oarBBThe qmpwiorths over tarelazy '
  'dog.changee,g.emmas browner    or   spaces'],
 ['comminmors???'],
 ['F,,n'],
 ['yyQwaoYdS'],
 ['you?y?'],
 ['browner'],
 ['kquickcommas???lniniie!'],
 ['   A  rand om   i string    with      no   commas     or with'],
 ['shbeMulti?wu?'],
 ['brli A  neen'],
 ['spacesNDWUThe'],
 ['HelllroThe quickx brown fox jumps over tarelazy tarelazydog.'],
 ['ThTH   A  random     string    with      no    commas     or   spacesello,e'],
 ['spacesThe quick browneeWr Uth e lazy dochangee,g.NWUyMDDWJArdog.H'],
 ['ntesn'],
 ['saddiang'],
 ['BBThe'],
 ['HecThe'],
 ['nam'],
 ['cMulti\nline\nstTherHwords,r\nommas!'],
 ['noiin'],
 ['eBThTHelloh,e'],
 ['The quick brown fox jumpsThe quick browspacesNWUyMDDWJArn fox jumps over th e lazy dog. over '
  'the lazy dog.'],
 ['randomas???'],
 ['thebrliick'],
 ['cnamehangeThe quick brown fox jumps over change,the lazydog.,'],
 ['Homicommase s, my    name   is are    youbetween?   '],
 ['The,ThisStringHasNNoSpaces,,,,,No words, here,,,,,, quick .cheangeg,brown fox jumps over th e l '
  'dog.'],
 ['eHi, my   i namck,brown,fox,jumps,over,the,lazy,dog. you?   zy'],
 ['removing,'],
 ['Raav'],
 ['ThTTHelo,e'],
 ['namem'],
 ['sbetwecTeheen'],
 ['heer'],
 ['ujummThe qfuick brown fox jumg.ps'],
 ['ck browner th e lazy dochangee,g.ommas'],
 ['zy'],
 ['The quick bsrowspacesNWUyMDDWJArn fox jumps over th e lazy dog.'],
 ['cnaranddocPresident,mehange,'],
 ['upjumps'],
 ['cThe quick browniiiser th you?uangee,g.ommas'],
 ['ing'],
 ['bbrlJohn.binee'],
 ['hnoiin'],
 ['   A  random    string    with      no    commwords,asver tarelazy dog.changee,g.or   spaces'],
 ['cnamcehange,'],
 [',,,,,,N,o'],
 ['The quick browne fox jumps over tarelazy doTwo spaces aaf,ter,  one space before  , and no '
  'speaces in betweeng.'],
 ['!s!s!'],
 ['ss'],
 ['Multi\n'
  'line\n'
  'strbrowslin   A jumpwiordog.ths random    string    wiorth     no    commas     or   spacesthg\n'
  'Hig,rtld!\n'
  'H'],
 ['betweeng.'],
 ['brThe quick b rown fox jumps over the lazy dog.n'],
 ['seHelllThe quick browner th e lazy do changee,g.oThe'],
 ['sbbetwecTeheen'],
 ['randomstrHwords,'],
 ['Hi, my    name  you?   '],
 ['ladzydoga.'],
 ['ovchange,withs,ngee,g.Hi,rd!'],
 ['jumpwiorF,ntyhs'],
 ['iiicommas!ulutiis'],
 ['BrH    A  rand om    string    with      no   her,e,,,,,, commas     or withicommases, my    '
  'name   is John. How  spaace   are    you?u   spaacea'],
 ['sshoHhew?'],
 ['oom'],
 ['dstTherHwords,r'],
 ['cheangge,'],
 ['The quick brown fox jAmazing, how a sentence can change, meaning just by, adding or removing, '
  'commasAmazing, how a sThe,quick,brown,foxdogwords,ngee,g.er,the,lazy,dog.entecThe quick browner '
  'th e lazy dochangee,g.omm,asaning just by, addingThe quick browner th e ulazy dochangmas!!umg '
  '.cheangeg,'],
 ['The qmpwioBBrths over tarelazy dog.changee,g.'],
 ['d   A  random    string    wiorth     no    c ommas     or   spacesV'],
 ['cant'],
 ['jommas!umg.'],
 ['Hi,my,name,is,John'],
 ['Hi,my,name,is,John,'],
 [',    , , , ,    ,'],
 ['1,2,3,4,5,6'],
 ['Hi!My,Name     is John'],
 ['Two spaces after,  one space before  , and no spaces in betwstringeen'],
 ['   A  srandom    string    with     no    commaAs     or   spaces'],
 ['The,quick,rbrown,fox,jumps,over,the,lazy,dog.'],
 ['President, John, F, KennedyThe,quick,brown,fox,jumps,over,the,lazy,dog.'],
 ['Hi, my    naF,me   is John. How     are    you?   '],
 ['President, John, F, KennedyThe,quick,brown,fox,jumps,over,Hi, my    name   is John. How     ar '
  'e    you?   the,lazy,dog.'],
 ['my'],
 ['Hi, my    name   is John. How     are    ychange,ou?   '],
 ['President, John, F, KennedyThe,orquick,brown,fox,jumps,over,the,lazy,dog.'],
 ['Ama zing, how a sentence can change, meaning just by, adding or removing, commas!'],
 ['srandom'],
 ['Thbetweene,quick,brown,fox,jumps,over,the,lazy,dog.'],
 ['Kennedy'],
 ['beThe,quick,rbrown,fox,jumps,over,the,lazy,dog.fore'],
 ['icommaAs'],
 ['beThe,quick,rbrown,fox,jumps,over,the,lazy,do,g.fore'],
 ['Two spaces atfter,  one space before  , and no spaces in betwstringeen'],
 ['jHello,ust'],
 ['Hi, my    naF,me   is Johow     areover    you?   '],
 ['zing,'],
 ['beThe'],
 ['dsrandom'],
 ['comMubeThe,quick,rbrown,fox,jumps,over,the,lazy,do,g.foreltimaAs'],
 ['sMulti\nline\nstring\nHello,\nworld!\npaceno'],
 ['Twrandomo spaces after,  one space before  , aTwond no spaces in between'],
 ['Hi,  my    name   is John. How     are    ychange,ou? aTwond'],
 ['EeJKnUSVXF'],
 ['qk'],
 ['world!'],
 ['President, John, F, K,ennedyThe,quicjumpsk,brown,fox,jumps,over,Hi, my    name   is John. '
  'How     ar e    you?   the,lazy,dog.'],
 ['y'],
 ['   A  srandom    string    with     no    commaAs     ort   spaces'],
 ['world!!'],
 ['ychange,ou?'],
 ['Amazing, how a sentence ianing just jHello,ustby, adding or removing, commas!'],
 ['moving,'],
 ['   A  srandom     string    with     no    commaAs     ort   spaces'],
 ['ychange,Hi, my    name   is John. How     are    ychange,ou?   ou?'],
 ['BCKkvp'],
 ['azing,re'],
 ['eKenney'],
 ['Hi,  my    name   is oJohn. How     are    ychange,ou? aTwond'],
 ['Hi,  my    name   is John. How     are    ychaKennedyThe,quick,brown,fox,jumps,over,Hi,nge,ou? '
  'aTwond'],
 ['cosmmasychancge,ou?!'],
 ['lazyThe,quick,rbrown,fox,jumps,over,the,lazy,dog.'],
 ['beforsMultiethe,lazy,dog.'],
 ['Two spTwrandomoaces atfter,  one space before  , and no spaces in betwstringeen'],
 ['sMulti\nline\nsaddingtring\nHello,\nworld!\npaceno'],
 ['lazAmazing, how a sentence can change, meaning just by, adding or removing, commas!y'],
 ['beTh'],
 ['ychange,Hi, my    name   is John. How     are    ychang e,ou?   ou?'],
 ['How'],
 ['HoJohn,w'],
 ['comm'],
 ['leine'],
 ['Tjumps,over,the,lazy,dog.'],
 ['spTwrandomoaces'],
 ['lei'],
 ['commma!'],
 ['ychaKennedyThe,quick,brown,fox,jumps,over,Hi,nge,ou?'],
 ['boeThe,quick,rbrown,fox,jumps,over,the,lazy,dog.fore'],
 ['aftThe,quick,brown,fox,jumps,over,the,lazy,dog.er,'],
 ['   A  srandom     string    with     no    comJohn.maAs     ort   spaces'],
 ['Hi, my    naF,me   is Johow     areover    you?   ello,ust'],
 ['HoJohn'],
 ['   A  sranadom    string    with     no    dcommaAs     or   spaces'],
 ['lazAmazing,'],
 ['ychaKennedyThe,quick,brown,fox,jumps,ovesMulti\n'
  'line\n'
  'saddingtring\n'
  'Hello,\n'
  'world!\n'
  'pacenor,Hi,nge,ou?'],
 ['atfter,'],
 ['President, John, F, KennedyThnamee,quick,brown,fox,jumps,over,the,lazy,dog.'],
 ['yXdEXoUU'],
 ['EeJKnUSVF'],
 ['Hi,  my    name   is John. How     are    ycPresident, John, F, Kennedyhange,ou? aTwond'],
 ['BCKkvqkp'],
 ['BC   A  srandom     string    with     no    commaAs     ort   spaceskvp'],
 ['yu?'],
 ['The,quick,rbrown,fox,jumps,over,tog.'],
 ['cosmmasychamnce,ou?!'],
 ['Pre, F, K,ennedyThe,quicjumpsk,brown,fox,jumps,over,Hi, my    name   is John. How     ar e    '
  'you?   the,lazy,dog.'],
 ['Two spTwrandomoaces atfter,  one space before  , and no spaces in betwstri ngeen'],
 ['ychange,Hi, my     name   is John. How     are    ychange,ou?   ou?'],
 ['Hi, my    naF,me   is Jomhow     areover    you?   ello,ust'],
 ['KennedyThe,orquick,brown,fox,jumps,over,the,lazy,dog.'],
 ['adJohowding'],
 ['Twrandomo spaces after,  one space before  , aTwond no spaceHi,  my    name   is John. How     '
  'are    ychange,ou? aTwonds in between'],
 ['hinow'],
 ['The quick brown fox jukmps over the lazy dog.'],
 ['spTwradomoaces'],
 ['Hi,srandom my    name   is John. How  spaces   are    ychange,ou?   '],
 ['aftThe,quickThbetweene,quick,brown,fox,jumps,over,the,lazer,tthe,lazy,dog.er,'],
 ['quicck'],
 ['Pr, F, KennedyThe,orquick,brown,fox,jumps,over,the,lazy,dog.'],
 ['aftThe,quickThbetweene,quick,brown,fox,jAma zing, how a sentence can change, meaning just by, '
  'adding or removing, commas!umps,over,the,lazer,tthe,lazy,dog.er,'],
 ['lazAmazjing, how a sentence can change, meaning just by, adding or removing, commas!y'],
 ['atfterHi, my    name   is John. How     are    ychange,ou?   ,'],
 ['dcommaAs'],
 ['between'],
 ['jumpychange,Hi, my    name   is John. How     are    ychange,ou?   ou?s'],
 ['Pre,'],
 ['Tjumps,over,thThe,quick,rbrown,fox,jumps,over,tog.e,lazy,dog.'],
 ['EeJPre, F, K,ennedyThe,quicjumpsk,brown,fox,jumps,over,Hi, my    name   is John. How     ar '
  'e    you?   the,lazy,dog.KnUSVF'],
 ['ycick,brown,fox,jcommas!umps,over,the,lazer,tthe,lazy,dog.er,umps,over,the,lazy,dog.world!\n'
  'pacenor,Hi,nge,ou?'],
 ['over'],
 ['beThe,quick,rbrown,feox,jumps,over,the,lazy,dog.fomre'],
 ['spa,,e,,,,No word,s, here,,,,,,ces'],
 ['ychange,Hi, my space   name   is John. How     are    ychang e,ou?   ou?'],
 ['after,BCKkvqkp'],
 ['Multi'],
 ['jHello,usst'],
 ['OPvfQ'],
 ['a'],
 ['OPQvfQ'],
 ['   A  srandom      string    with     no    commaAs     ort   spaces'],
 ['ThisSaTwondstringHasNoSpaces'],
 ['Tjumps,over,thThe,quick,rbrown,fox,jumps,over,tog.e,laz.'],
 ['qPresident, John, F, Kennedyuicck'],
 ['ort'],
 ['onejHello,ust'],
 ['sPresident, John, F, Kennedyrandom'],
 ['ThisStringHasNocosmmasychancge,ou?!Spaces'],
 ['icommaAMultis'],
 ['Pe,'],
 ['The,quick,brown,fox,j,umps,over,the,lazy,dog.'],
 ['HoJohnyu?'],
 ['spTwradomoaEeJPre,s'],
 ['Keneello,ustdy'],
 ['   A  random    string    with     no    commas     o r   spaces'],
 ['dcommaA'],
 ['adJohownding'],
 ['Hi,  my    name   is John. How     are    ychaKennedyThe,quick,brown,fox,jumps,over,Hi,nge,ou? '
  'aTwoHnd'],
 ['qquick'],
 ['Hi,  my    name   is John. HoHw     are  dsrandom  ychange,ou? aTwond'],
 ['lazrandomy'],
 ['jumpychange,Hi,'],
 ['KBCKkvqkp'],
 ['aTwoycick,brown,fox,jcommas!umps,over,the,lazer,tthe,lazy,dog.er,umps,over,the,lazy,dog.world!\n'
  'pacenor,Hi,nge,ou?nds'],
 ['K,ennedyThe,quicjumpsk,brown,fox,jumps,over,Hi,'],
 ['yort?'],
 ['HoJomoving,hnyu?'],
 ['adJohowdMulti\nline\nstring\nHello,\nworld!\ning'],
 ['sPresident,'],
 ['Two spTwrandomoaces atfter,  one space before  , and no spaces in betwstri ngeen   A  random    '
  'string    with     no    commas     or   spaces'],
 ['areover'],
 ['movingover,'],
 ['ychaKennedyThe,quick,brown,fAmazing, how a sentence ianing just jHello,ustby, adding or '
  'removing, commas!ou?'],
 ['ychange,Hi, my space   name   issMulti\n'
  'line\n'
  'string\n'
  'Hello,\n'
  'world!\n'
  'paceno John. How     are    ychang e,ou?   ou?'],
 ['beThe,quick,rbrown,feeox,jumps,over,the,lazy,dog.fomre'],
 ['ou?'],
 ['The quick brown fox jukmps over the  lazy dog.'],
 ['Amazing, how a senteence can change, meaning just by, adding or removing, commas!'],
 ['here,,,,,,'],
 ['m'],
 ['   A  random    string  n  with     no    commas     o r   spaces'],
 ['The,quick,rbrown,fox,jumpsu,over,jumpychange,Hi, my    name   is John. How     are    '
  'ychange,ou?   ou?sg.'],
 ['ycPresident,'],
 ['ychang'],
 ['adJohoweding'],
 ['spa,,e,,,,NolazrTwrandomoandomy'],
 ['lazAmazing, how a sentence can change, meaning just by, addinge or removing, cogmmas!y'],
 ['spTwradomoaEeJP,s'],
 ['oPe,?'],
 ['yuu?'],
 ['ychaKennedyThJohn.e,quick,brown,fox,jumps,over,Hi,nge,ou?'],
 ['saddingtring'],
 ['Hi,  my    name   is John. How     are   d'],
 ['The,quick,rbrown,fox,jumps,over,the,lazy,dogou?.'],
 ['Hi, my    naF,me   is Jomhow      areover    you?   ello,ust'],
 ['betwstringeen'],
 ['qqck'],
 ['movingovrandomer,'],
 ['dsrand'],
 ['d'],
 ['ju'],
 ['Multi\nline\nstring\nHcosmmasychancge,ou?!ello,\nworld!\n'],
 ['zin'],
 ['spTwradomoBCKkvpaEeJPre,s'],
 ['K,ennedyThe,quicjumpsk,brown,fox,jump,s,over,Hi,'],
 ['sMulti\nline\nsaddingtring\nHel'],
 ['ychange,Hi, my    name  ThisSaTwondstringHasNoSpaces is John. How     are    ychang e,ou?   '
  'ou?'],
 ['Kennedyucck'],
 ['aftThe,quick,brown,fox,jumps,over,the,lazy,do,'],
 ['ThisStringHasNocosmmasychjumpychange,Hi, my    name   is John. How     are    ySchange,ou?   '
  'ou?sancge,ou?!Spaces'],
 ['Ama zing, how a sentence can meaningemoving, commas!'],
 ['The quick brownTwrandomo f the lazy dog.'],
 ['HoJohyu?'],
 ['Hi, my    naF,me   is Jomhow     areover    yremoving,ou?   ello,ust'],
 ['areoveyuu?r'],
 ['Pretsident, John, F, Kennedy'],
 ['spaceskvp'],
 ['President, Joychange,Hi, my space   name   issMulti\n'
  'line\n'
  'string\n'
  'Hello,\n'
  'world!\n'
  'paceno John. How     are    ychang e,ou?   ou?hn, F, '
  'KennedyThe,quick,brown,fox,jumps,over,the,lazy,dog.'],
 ['sPresident, John, F,n Kennedyrandom'],
 ['Pretsident,'],
 ['lazAmazing, how a sentence can change, meaning just by, adding or removing, coHi, my    '
  'naF,me   is Johow     areover    you?   ello,ustmmas!y'],
 ['dcdommaA'],
 ['yy'],
 ['KtowRydY'],
 ['Presidenpacenor,Hi,nge,ou?ndst, John, F, '
  'KennedyThnamee,quick,brown,fox,jumps,over,the,lazy,dog.'],
 ['jukumps'],
 ['yXdEonejHello,ustXoUU'],
 ['sMulti\nline\nstring\nHello,\nmeaningemoving,world!\npaceno'],
 ['Presidenpacenor,Hi,nge,ou?ndst, Johdn, F, '
  'KennedyThnamee,quick,brown,fox,jumps,over,the,lazy,dog.'],
 ['hiKennedyuccknow'],
 ['qPresident,'],
 ['dsrandello,ustmmas!y'],
 ['JHoJohnyu?'],
 ['belazAmazing,tweenn'],
 ['lenine'],
 ['JkohThe quick brownTwrandomo f the lazy dog.n.'],
 ['S'],
 ['atfterHi, my    name   is John. How     are    ychange ,ou?   ,'],
 ['aychaKennedyThe,quick,brown,fAmazing, how a sentence ianing just jHello,ustby, adding or '
  'removing, commas!ou?ding'],
 ['aftThe,quick,brown,fumps,over,the,lazy,do,'],
 ['aTwond'],
 ['ou?s'],
 ['ello,ustmmas!y'],
 ['araeover'],
 ['   A  random    string  n  with     no    scommas o    o r   spaces'],
 ['pDWegu'],
 ['pacenor,Hi,nge,ou?nds'],
 ['Tjumps.,over,thThe,quick,rbrown,fox,jumps,over,tog.e,lazy,dog.'],
 ['EeJPre,'],
 ['slMulti\nline\nsaddingtring\nHel'],
 ['betwstringee'],
 ['hjumpychange,Hi,'],
 ['a,tfter,'],
 ['qPresident, Jiohn, F, Kennedyuicck'],
 ['brownTwrandomo'],
 ['Tjumps,over,uick,rbrown,fox,jumps,over,tog.e,laz.'],
 ['dog.a.Twonds'],
 ['VqVNGKV'],
 ['Twrandomo spaces after,  one space before  , aTwond no spaceHi,  my    name   isworld! John. '
  'How     are    ychange,ou? aTwonds in between'],
 ['HoJohye,ou?u?'],
 ['Hi, myJoychange,Hi,   t'],
 ['paceno'],
 ['beTbh'],
 ['chan,ge,'],
 ['spa,,e,,,,No'],
 ['behTbh'],
 ['aychaKennedyThe,quick,brown,fAmazing, how a sentence ianing just jHello,ustby, adding odog.r '
  'removing, commas!ou?ding'],
 ['thlazAmazing,'],
 ['KeKnnedynucck'],
 ['aTwoycick,brown,fox,jcommas!umps,over,the,lazer,tthe,lazy,dog.er,umps,over,the,lazy,dog.world!\n'
  'pacenor?nds'],
 ['HoJohye,ou?uKennedyThe,orquick,brown,fox,jumps,over,the,lazy,dog.'],
 ['lAeSbnrM'],
 ['The quick brown fox juTwrandomo spaces after,  one space before  , aTwond no spaces in '
  'betweenkmps over the lazy dog.'],
 ['adJohowdMulti'],
 ['Twrandomo spaces after,  one space before  , aTwond no spaceHi,  my    name   iswostringrld! '
  'John. How     are    ychange,ou? aTwonds in between'],
 ['dsrand,ello,ustmmas!y'],
 ['naF,me'],
 ['.Hi,  my    name   is John. HoHw     are  dsrandom  ychange,ou? aTwond'],
 ['e  lazy doge,ou?.'],
 ['   A  sranadom    string    with     no    dcomma     or   spaces'],
 ['The quick brow n fox jumps over the lazy dog.'],
 ['Amazing, how aa sentence ianing just jHello,ustby, adding or removing, commas!'],
 ['qPresident, Jiohn, F, Kedog.a.TwondsnnedyuicckHoohnyu?'],
 ['dsrandelmlo,ustmmas!y'],
 ['comJohn.maAsjukmps'],
 ['eTjumps,over,the,lazy,dog.'],
 ['BCKkvq.Hi,  my    name   is John. HoHw     are  dsrandom  ychange,ou? aTwondkp'],
 ['Tjumps,over,thThe,quick,rbrown,fox,jumyremoving,ou?ps,over,tog.e,lazy,dog.'],
 ['oThisStringHasNocosmmasychamncge,ou?!Spaceser'],
 ['here,,,,,,cesne'],
 ['qPresident, Jiohn, F, Kennedy,uicck'],
 ['lazAmazing, ehow a sentence can change, meaning just by, addinge or removing, cogmmas!y'],
 ['lazAmazing, how a sentence can change, meaning justodog.r by, addinge or removing, cogmmas!y'],
 ['izin'],
 ['dsrandello,ustmbehTbhmas!'],
 ['mmy'],
 ['KBCCKkvqkp'],
 ['aftThe,quickThbetweene,quick,brown,fox,jAma'],
 ['sMulti\nline\nstring\nHello,\nworld!\ndom'],
 ['pnaceno'],
 ['here,,,,,,addinge'],
 ['Pe,aTwoHnd'],
 ['Two spaces after,  one space nbefore  , and no spaces in betwstringeenHel'],
 ['brownbeThe,quick,rbrown,feox,jumps,over,the,lazy,dog.fomre'],
 ['spTwradomoa,s'],
 ['na,F,me'],
 ['Ama'],
 ['ng'],
 ['meaningemoving,'],
 ['The quick brown mfox juTwrandomo spaces after,  one space before  , aTwond no spaces in '
  'betweenkmps over the lazy dog.'],
 ['lazAmazing, how a sentence can change, meaning just by, adding or removing, commas!yeKnney'],
 ['President, John, F, KennedyThnamee,quick,brown,fox,jumps,over,the,ychange,Hi, my    name   is '
  'John. How     are    ychange,ou?   ou?lazy,dog.'],
 ['HoJohHi, myJoychange,Hi,   tu?u?'],
 ['quicc'],
 ['comHoJohyu?m'],
 ['c!ommas!!'],
 ['Joychange,Hi,'],
 ['aTwoycick,brown,fox,jcommas!umps,over,the,lazer,tthe,lazy,dog.er,uThe quick brown mfox '
  'juTwrandomo spaces after,  one space before  , aTwond no spaces in betweenkmps over the lazy '
  'dog.mps,over,the,lazy,dog.world!\n'
  'pacenor?nds'],
 ['onaftThe,quickThbetweene,quick,brown,fox,jAma zing, how a sentence can change, meaning just by, '
  'adding or removing, commas!umps,over,the,lazer,tthe,lazy,dog.er,'],
 ['Mychange,Hi, my space   name   issMulti\n'
  'line\n'
  'string\n'
  'Hello,\n'
  'world!\n'
  'paceno John. How     are    ychang e,ou?   ou?'],
 ['brownbeThe,quick,rbrown,feox,jumps,over,the,lazy,edog.fomre'],
 ['ychaKennedyThe,quick,brown,fAmazing,'],
 ['Hi,  my    name   is John. HowbeforsMultiethe,lazy,dog.     are    '
  'Tjumps,over,uick,rbrown,fox,jumps,over,tog.e,laz.ychaKennedyThe,quick,brown,fox,jumps,over,Hi,nge,ou? '
  'aTwoHnd'],
 ['Tjumps,over,thThe,quick,rbrown,fox,jumyrefmoving,ou?ps,over,tog.e,lazy,dog.'],
 ['The quick brown fox jukmps over the  lazy dog.chan,ge,'],
 ['A'],
 ['cosmmasychancgeu?!'],
 ['President, John, F, KennedyThe,quick,brown,fox,jumps,over,Hi, mye    name   is John. How     ar '
  'e    you?   the,lazy,dog.'],
 ['BCKdog.a.Twondskvp'],
 ['dsrandd'],
 ['ello,ust'],
 ['meaningemovning,'],
 ['Tjumps,over,tdsrand,ello,ustmmas!yhThe,quick,rbrown,fox,jumyremoving,ou?ps,over,tog.e,lazy,dogspaceHi,'],
 ['nae,F,me'],
 ['Jiohn,'],
 ['adJohoychaKennedyThe,quick,brown,fAmazing,dMulti'],
 ['HoJohyei,ou?uKennedyThe,orquick,brown,fox,jumps,over,the,lazy,dog.'],
 ['The,quick,rbrown,fox,jumpsu,over,jumpychange,Hi, my    name   is Johdsrandn. How     are    '
  'ychange,ou?   ou?sg.'],
 ['Twoyort?'],
 ['KennedyThe,orquick,brown,fox,jumps,over,the,lazy,doTjumps.,over,thThze,quick,rbrown,fox,jumps,over,tog.e,lazy,dog.g.'],
 ['srapacenor,Hi,nge,ou?ndoehowm'],
 ['cosmmasychsPresident, John, F,n Kennedyrandomansrandomcge,ou?!'],
 ['Kennedyrandom'],
 ['brownTwranhere,,,,,,cesnedomwo'],
 ['bfA'],
 ['OPvleifQbelazAmazing,tweenn'],
 ['Twoyor?'],
 ['spa,,e,,,,eNo'],
 ['lazAmazing, how a sentence can change, meaning justodog.r'],
 ['pnacHello,eno'],
 ['adoJohowdingi'],
 ['HoJohye,ou?uKennedyThe,orquick,brown,fox,spacesjumps,over,the,lazy,dog.'],
 ['Mychange,Tjumps,over,uick,rbrown,fox,jumps,over,tog.e,laz.ychaKennedyThe,quick,brown,fox,jumps,over,Hi,nge,ou?Hi,'],
 ['   A  srandom      string    with   paces'],
 ['Hi, my    naF,me   is Jomhowlo,ust'],
 ['HoJohye,ouo?u?'],
 ['after,BCKkvkp'],
 ['HoJohye,ou?uKenneodyThe,orquick,brown,fox,jumps,over,the,lazy,dog.'],
 ['wHow'],
 ['KtowRydYThe quick brow n fox jumps over the lazy dog.'],
 ['annd'],
 ['e  lazy dge,ou?.'],
 ['ychaKennedyThe,quick,brown,ifox,jumps,ovesMulti'],
 ['wychange,Hi, my    name  ThisSaTwondstringHasNoSpaces is John. How     are    ychang e,ou?   '
  'ou?orld!!'],
 ['areoveyuur'],
 ['meaningemosMulti\nline\nstring\nHello,\nmeaningemoving,world!\npacenoving,'],
 ['lazAmazing, homeaningemoving,w a sentence can change, meaning jusfoxt by, aaddinge or removing, '
  'cogmmas!y'],
 ['VqVVNGVKV'],
 ['spTwradoa,s'],
 ['ou?snaeme'],
 ['lazAmazing, how a sentence can changewojrd,s,g just by, adding or removiyng, commas!y'],
 ['usst'],
 ['betwstringbeen'],
 ['hereHi,srandom my    name   is John. How  spaces   are    ychange,ou?   '],
 ['Pre, F, K,ennedyThe,rquicjumpsk,brown,fox,jumps,over,Hi, my    n   A  srandom      string    '
  'with   pacesohn. How     ar e    you?   the,lazy,dog.'],
 ['   A  sranadom    string    with     no    dcommaAs     adJohowdMulti\n'
  'line\n'
  'string\n'
  'Hello,\n'
  'world!\n'
  'ingor   spaces'],
 ['Hi, myJoychangVqVVNGVKVe,Hi,   t'],
 ['cthlasentencezAmazing,osmmaKennedyThnamee,quick,brown,fox,jumps,over,the,ychange,Hi,sychancgeu?!'],
 ['President, John, F, KennedyThe,quick,brown,fox,jumps,over,Hi, mye    name   is John. How     ar '
  'e    lazy,dog.'],
 ['qqquick'],
 ['lazy,dog.'],
 ['r'],
 ['HoJohye,ou?uKennedyThe,orquick,brown,fox,spacesjumps,onver,the,lazy,dog.'],
 ['coychange,ou?ammma!'],
 ['comJohn.mthbetweenkmpseaAsjukmps'],
 ['YNe'],
 ['brow'],
 ['yremoving,ou?'],
 ['lazAmazjing, how a sentence can change, meaninglAeSbnrM just by, adding or removing, commas!y'],
 ['aTwoycick,brown,fox,jcommas!umps,onkmps over the lazy dog.mps,over,the,lazy,dog.world!\n'
  'pacenor?nds'],
 ['ycPresidenadJohowdingt,'],
 ['.Hi,  my    name   is John. HoHw     are  d  ychange,ou? aTwond'],
 ['beThe,quick,rbrown,fox,jumups,over,the,lazy,do,g.fore'],
 ['jHelloo,usst'],
 ['dd'],
 ['he,,,,,'],
 ['voTB'],
 ['President, John, F, KennedyThe,quick,brown,fox,jumps,over,Hi, my    name   is John. How     ar '
  'he    you?   the,lazy,dog.'],
 ['dsrandelmlo,ustmmHi,srandom my    name   Pre, F, '
  'K,ennedyThe,quicjumpsk,brown,fox,jumps,over,Hi, my    name   is John. How     ar e    you?   '
  'the,lazy,dog.is John. How  spaces   are    ychange,ou?   as!y'],
 ['HoJohye,ou?uKenneodyThe,orq,uick,brown,fox,jumps,over,the,lazy,dog.'],
 ['lazAmazjing, how a sentence can change, meaninglAeSbnrM just by, addcing or removing, commas!y'],
 ['dcoTjumps,over,uick,rbrown.e,laz.mmaA'],
 ['ychange,Hi, my    name   is John. How     ychange,Hi,are    ychang e,ou?   ou?'],
 ['yeKenney'],
 ['ou?sg.'],
 ['beThe,quick,rbrown,feox,jumps,over,the,lazy,dog.focommas!ou?mre'],
 ['areobrownTwrandomover'],
 ['qPresidenJiohn, F, Kennedy,uicck'],
 ['issMulti'],
 ['the,lazy,dog.BCKkvp'],
 ['agdJohownding'],
 ['Pre, F, K,ennedyThe,rquicjumpsk,brown,feox,jumps,over,Hi, my    n   A  srandom      string    '
  'with   pacesohn. How     ar e    you?   the,lazy,dog.'],
 ['qqk'],
 ['noThe quick brown fox juTwrandomo spaces aPresident, John, F, '
  'K,ennedyThe,quicjumpsk,brown,fox,jumps,over,Hi, my    name   is John. How     ar e    you?   '
  'the,lazy,dog.fter,  one space before  , aTwond no spaces in betweenkmps over the lazy dog.'],
 ['lazAmazjing, how a sentence can change, meaninglAeSbnrM just by, adding or removing, commams!y'],
 ['mye'],
 ['spaceskpvp'],
 ['BCKkvq.Hi,  my    name   is John. HJohowoHw     are  dsr andom  ychange,ou? aTwondkp'],
 ['sMulti'],
 ['dsrawithndd']]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-qYUJGw17vULZNLb19+5ssHTG<Jjno*(t<KuMH-@vr`J49~lK-'
    b'v%6^^4^SyJhAs$?ts~}ISpop|L_0n|M&m?U;fws#sB=D|MP$UAOG9`=l|-'
    b'l)c^TE{*RT%HTt=Cf5u5|J}ceN=`ozq#~ngRJ*IHaYd@iuCyyQXyjEP-PWNi*fBxV9^Z)u^|HuE4Ps?LoDW}ozGB%%6_oyT6okLj'
    b'bo_W{a(v^3+atWngql~MRJB>Tn_WPJ{^U2Q~`^;HqIcKlEW`6D(L*;ARolhPo$ET-Rt~63R&rIWqyYZ|4_G$X;^QklJ8rtkF)KgR'
    b'BL*nXl&Jo9bugD+Nc%2wF-?OitpHxOmr=IX%9}`*${o-'
    b'5Cc|zg`d&)fA=zH>+VTGsMVT5x+E+@^@?o;O7X3Ocm>dgQ4Y5vj2>~lY(hkSO)V}$29`@Yg1_j>Y)XY)bVbDvtSc%`SuewA^Tl=J'
    b'Rb&J+LZW73XkKF>Zp4O`ux`mA=Xy=S_{U3)55yZKOlr(U5K3^LRe&&}%9Jpb`ajc}(}dhhpr=XS*t?w$hv5mMsyVm()EyWAs}T6Z'
    b'72@WanDCRSGZ{@Kmlu7S7UDbK~8r+)Qk@s)GuxYC+ohNs5O$DDhy?RV;PkLy|(b<1)5*T+0p8|4}I&M9EB`|J~Y>v@)tdoC%ajQ2'
    b'jhj5Wq!0m2j7NUmM#Px(1R$yd7qZ+&a<r=2=lTd}ev>1KPvY9r1V+f2`y@xse@;1gqAYv*(Qo@N!^q6fYyw|+l4)SRmrao5p-'
    b'i4anm<HF0XePtFdwp!Z`IrBW%?`irfyF9#Q%6MU(Jn(ftPu-'
    b'{2HP=q~cie+FAC1lHIDJVeoRw3lPrm={hO_wVU{}CNjpvj#5AU&Njn7FKW*qhE6QpTR#)LD=HAha@vm&+{{_)cQrx%~SpS#_C<5='
    b'uG?ooIka4&W?d(Q|s^G$$VFFT9EW7fULc*g&K0!65!Onw;~jdyBKOKbIb9}E?kKTj=%?*Zts!CW#%#;VV2TsMw(en5fc^Er1}t;G'
    b'B8pe655Sm-C<q;aP?p9^o{v2e+Ihl>R(X*O-Cub*p%bFCB&WqUk4QmQjmTy$>#1k+tH;r-'
    b')ct=o0dwT(pWG#)<VCZ97j{tZ97uDWx*<Iq!P1M>K_=SdY;zMqtGiM#Ar*|wU}ld-'
    b'gfwg1=0TqUo$?}edV2cJ13#(9?-N?$!yR)M!-Z8D*WAGm9od}4kGZ*j-+bIlb_-vvjht3)E(^URB-'
    b'!&TD>;PM)=ta7ssxLCYf45K~s5Q4xDAoaK5;4285({8+Yef9=KN;>6vmcPm>5-'
    b'{r`_=Y}!G9LC}xkkKLzWn@SyQzfY#`D&P7yw9|`)*+D={fQ-Bep*9&;fGP2vMo^ny0`})~bmg{<n5h*wT7GVb)qRFVxn^17HJtr4'
    b'V32?Hgv2EBHNDh_I=%D=VB%BHsVPojcLy-'
    b'3jaWS*$=Ba4wLaZF;V!k5Y*~g|!PMUOWR72z(5J!gXK&_G$jn5<^oO(VN#f6MC~cUXU?aTpssYH9{22x%diP1Wzc$G4Kr91IpglX'
    b'E%+XZ3KTdsIOCEI^b?`e|Y*<o=aQ4FLsD^N^BE<0z-'
    b'Hjv2}gn?!x4r{OnbQ^tmH=1DwwsN{jscKr4yOrM7hiC`<57aHwm+GTQwkv<0pbdFae$<TkNlmTuuyJFyi6`^0<kQBbrfWsU9XonS'
    b'{?Pdk^N-'
    b'CSp9Y@45e0L74uim8NAmNY2tl|sn`$+IW$4t;_g&J%fjZDi~pY!Pe00&EsEseC_Hv2ufkq{**8ti8AbE4stn9lKZ;0epAhK=Sl&U'
    b'6Tb&EA@&*C~*al8WxdTUEpAu{4;>gv-U8{y+Xt2Y6e1i-'
    b'&x0O{Rdm92+Ti+#JhDK73&3ncm$SsKzMSIYhaOm=dQt2$QA}L2A*;Kb}C?8As|o!tdKS9><>uYGOGir&)VEtY&E<Z-'
    b'U6D9Q*T%jy5`|qe$FuPgBIpsg<^+F^@0$I6HbHOV}bzvP8ichMa+BEi@4my__+Ao^J5g@4*Udw^4uw{6B?}Q41Vkpi8_3rCki~_+'
    b'819yTtDT`dtt!<z=t<;-'
    b'un`}(|YcJQ4c`kY8(Eso;GVCEUi*XYpg5+qAg({!%z6&RR66rXuf=DNrab<!OnAIJI}rLgYDD=n#$J(%a5(ZRN88H0Nbi@DgBl>B'
    b'JVapj3fg{0JRAptvov#Za};sVyL0hBC&V#jFok)(0?RF*s1?KJdX4bh#+oY97xij#sPZ-'
    b'H|{~WB!IJ%Y;9`#Rpk@gI5&PZTe|CSr|!tY#da1_a3nAaF@vwNI|<HGfWL>w!C+Co6Ie}P(^X*tyn0^YXT<;~Vr@;ZYNr6!5u1@J'
    b'5LP(x$;}YY(yEi9!Wr|e0}FMH$_hV7KXI-'
    b'(*bxA+K_C#}3oV!foIhhG7aN(d&#NLe8vhtV9swE^<RE4LTYi&!I>36(h>L>ez_uU)A)(CqWw<^}bkv4hhwDL)0gOAHm@zS!^#0e'
    b'pcm#}ueZlz6OLU?$)*pE+;CHQt1#ZX)vgV*62%2Sw8F{A``NtoHoS{9yO;gu^Rf1MJ1jnn^Frhj#Ly|TshRwY3le|t{EZf2aShL^'
    b'90RGPicv=~RBc$N9+J=p(<SPq<;NkIM8@L6Lo$uI}PZuYCcGsV427=n%Gl3LM43%t^S84vv>{ogL2<h1ptDmB(2_#Gfh-'
    b'(BAV&d;(c5iaah4zDmwp9qcTbEy9uHF}KNu-'
    b'&5MZtL12Snq0R_=SS&A+w5v~a=Gfvi<{y^L#Dbk~NbsLjzMd2WRW3?Lu?C5EsiOy^1;O{x=eP{HlN!nEBY?uMi%em2apUn8-'
    b'?`;7aEH?}dZGx62F(0SPXM<GvmkU9J;#y}*vz>R)toB6q}j`JV|4FM0d1TwI%3D_J2^oU{RTEf4@8=et|yKWOkSI7JT?NB!083I0'
    b'0q4oG|IuPM@B2f`@$JbajI7|8De1W!O7~v*V^HX^uY4NeC%ksH%#wQcSz$tmo1#q%wEn-^-'
    b'yZ&@Ix)T~p07(}Rf?hgt6A@3C5IbNB8y*Rr#m-a^WU?DqDo^aaG?xA6;cZ?m-'
    b'_PPjvB}Px1vqHM#T#_Kf`8dK4&MWE0`89uRlo<|3Aum4cLFc>okBJdvO{@biFg!?6+8Qe_a|HpvmAun3;$lQ1>W(%Tq5%6w>DQlz'
    b'}PJ6Kz<6u08Q97wr{~jk6|PdDp~2Z2vR-'
    b'wI@(<WiUtq*Vev+SVLaH~@)0%^I4}MRy+GC@=L4L!HM5t4MGb?;RB9UV%6}tmF|zms!UY2$0>rzQ%B#g2Q$us-Fk1)-'
    b'zIwx5;B5qN1UcMhOM8A~pH&Uen#AX)c;o844x$!fU!z%s4V!5dX34eyO~5cz=IJ+RYli5jHDM}Gk=?-'
    b'fYJr<yr$N*SNb|lYK}yI#AwW;()A%Ree6`FcttW-wOCdUl3Tza}+JPh}HE5J$!5E<>r%XHx_7sVG@RE)u7?JhFL4=lnop{*|b<0n'
    b'U3QffY2zRw$?9fAA7N3pqk0%jR@l`D6ltt_UjsWcQ*^O4yuWrh2<^pIx(2<FG$VJ*+o?Qr1gs>+dp^G{s!{Z}_lDGVV?>_<xy#q9'
    b'8y=*m-cGd|;bu|Dyb|S(~M4YFout2N{z@q3u(+UUMKcI*y;Ru-QhH)TEp{xK!$I)JPk%_wz842>^ROs2$c=`mKKhWg#5fg+t%p3W'
    b'F?G~IUnm0w??}I*wY$2Y3L4p%J#VMdcDFgWIO>%pFJ{2$c7D%#zS?x-ThIfG+%al7?-pho$V&w!JJb-'
    b'n9nPL{uocX;}zADxp&devdvOG;DI%6sGLMGh&G0X~!9kcRI52jd(78Else*H*Wf`3B9@nJowuTh9p_pZ<*oVbAvs6k>c3V+?{iik'
    b';|0*vSj=vlu2Gj237)CD1V%0+bVsEtYJP9A-'
    b'fc~7%~kVl{$2@MN>@Op^gHss&^A7|QDMn<)mc!7zC#KhAuBlJv{JlwUkj#Vg&@8^NQm_o=zmyMI;@fS63EpUc(5l_!mJvo8l%(x5'
    b'o!s-H*nBb)j!UT9`tTXqg=M7Q$VKM6)5V&j!%gc`~l#-'
    b'<5#wrSbgMl5>bTCkM6YJgnBuh!?2Ry!0j{$;4LL^v*df|hByk1I%pM<!NVHF4s1aXW8nX(`&n7nKu+`l-'
    b'rVup3|bj5{kc|*%&UnfBgVg%mVuvmGYSv!6N_cz5jkVH68`F#vhj9-'
    b'S<oCcCWz5^@N&EDPRBK8p*uWRAuuveB;)4a|N%*K18BhvRY{Bt27g0?s#f~iFV0q?n38?+NqV5}vFhcBDauMfU-'
    b'^Ng_i{XNa`N1%rw0)ZKA3CNheVN<X`92=CA!V~x0RuJUQeV`~Cf%^-0p;dwx2-'
    b'2ZM><o;cZd~y(t&aI&F$g8r;u<&yK?VkWU!&iXjT_IuJ+AmihbORnK$H#0!R!++%o^f}h_d(RN(VFsTbFjNFhG2`puo{@YpUyi<`'
    b'=MybfE+1^W;i|&A_w2cP-+{nF;yGvLO4-_(2Q^MIO)<f-7P6_cS;?!4ME0=|I@ije3hO3C<6ZD-'
    b'j<qTobx79}E+Uz>Z=%Kn|MpXMQ&!oL`&ppEC%)Jv6NXw+d`OM5)4(&Cemnk?<X8#$F%LM#sE<!52Mq_PN=MT-'
    b'd=)L|_Bh&UjvW0Uc=a)B)rJQ>T@Fh=sU0j+Z{=o59WwtI28$P%E=YD?c8%q=7G@@6mbK0QRsq)Upk*>nfo@qKF?~GLsDi<%mt4jW'
    b'81P`Wf{<^L0a*9u|~+!-I0a395)g&;w>WSext1Q7jhgKekt)L98$!LBvtRH|QW9I|iT4uAud%tBzFxUdmjk&~J%*<_RHD3u-'
    b'O%DZ7Ll8-#oDlau{@Mjto>;fA*dY^Omu3Hs0YVmOby@K2(^Sm(M>&Hy-'
    b'z8HptjrH1dYu7v;%oiK&d3+xY*hIHdy|9Ha>=o%v!ith}G0{>W8bpDbca6Ph`5V$)K5TG5zlxLz%fE7&r{w*;qzJvS3$=Z+uaCU;'
    b'3EFNdWT6q$<@JZ-Xa5<I-EF5V=&rrT-(=QFA|KVxTR2-'
    b'ZZI+`bht$5U137Z#`o6r+HVFU>S?8r<}Z+>F=6214$J`qMxc{eO`f!)!g-GuCz@EH^E5lIV0SO7<Zsqp5#<Ygi?{#*0=M|M-'
    b'jy&t46ak3xcFotnDEb+AT+}g<UG#5+1_&f9`-mn`(Rd|aKo=-'
    b'qy5&SH#3gJIQG%TQM8qa3uYfJ~TL|xB<WlmHxPnJ*vFb90+_c2h$#n)g8iwK)|7L)-'
    b'(<DP4|i_w)t(;?Z2^+>J9bKnQN1}w(;ZFswCA;{dG&jZF+dy}ejGzerI#um&R4hZX#VZxG;9<5>Pgif6LCt0P@I06Pw{P38dd)g2'
    b'6Vxu5*8@dCLySGFD)}A55Ana8~1zE$N5UMZ+lU{fcLH68(cn$kvFZ%God80=BX<_7B*1vDbHl_^u&HK~gwXxxl2cCzRA90u3(Du;'
    b'#1HAID>cis`-2fyc2>NKiEpRMrHoj~U5Riy&8198^;+cbGCktwyp7Y=e9%Mp>%`4B#-'
    b'A?9TvBy5*cLoEcdyw?7=glU@T1+k@+7Xz%jEDK~u~Ck02a}!H*&=qYD}*;`{#zS-'
    b'r?!`H=ON)cOYYi+soM?XGWVF<?hR#w*v@{1DZVt|&Z&JVd3Z?zmR1M05(3(CA3`s01bM7uw+Ykpz!^t>6TPD+ONSo3wtiNepftDn'
    b'@kUS~bP!)Bbm+<XL8stYL`^AK#9-'
    b'PsXNHS;HuVG^_^SrWfXa^OSoZzE9p>hX@f_^3^&1VjYsaU92Q>?*F}M@;;g_IjtN#`#FxLVe^Fx>l8z4TObRo;GTSLhke$5JngJ<'
    b'ay2tOoiFAw1~Uq8)29933go^=#h$2O%51Y*y#Re9xgKbJ`Y&?0F>5Df4&@<k}E{+S;S2m9f*bGvJMGyN>%*bng=8oY>+yxKNePCo'
    b'AtI)dqw3xLXB@C~3U?lJ(9%i<l7twS16!Pu)ZJY0J}03Rv}{RY8;+D&+n=Wy-w@PZ2`bim+W)<sBJk9AjAOGuW25KS-GE%2k>#dO'
    b'#_4_b0spvzB(4+0xs&_R<MNP>!=l9D@x3C%&6sG+Cb4`y!u0KbJjn9RQL)vo{|o8BA=N?$!C9K6gjk>t@MQ3jthKfIcP3e02&Fqa'
    b'9pdJ+t1{XV7{bx>HBF33AUmQsD@WdgZg;a0DW>_Nx8zy}C5QW_=13#G|g{bU)i^pws+p|*fX9FXvK3)^!La$uM@zXd~|9&51Dh)+'
    b'wT&`d1y4~w5MaGG8)c*M(Yp4sl4)c#<z<pvR7eIY0U|AcM4<ieVu%?}Is^KhgOR)<X#0uxFGEWYrDwQvpaBx2#H-{tC-'
    b'1EYiyhjJMxGK=?7$kWY2v%XIq$>f&>b<vef9%4Y%`12<qda;9t&nL3Cja<9y!+ZaL!YErHu$}GO))dV8Rx$CdMA;T#H&<9<B-'
    b'nv+9UiL?t&aj?{pfXFK$fZkC*PPRD4jwnf#=7s$KgZ44d_?z9(oWW9u(6UP^yyolHb~xmy9xf&y_LLirC~8re%pIJ<su|6X`=d7p'
    b'yPHH%@h$HBI4TqRk9miDolZCpQ@Im}diSP)2wt28iG#JXh2hV)JF*RsU_S@y{6uQ<0q_9xb4}vg95c@_*BK6o>^8utL(OIj<Qoh='
    b'U7*6yO3e`#YV7r_J{`^adT-'
    b'9X=QPg^IE&;5IVliV@m^f_6tQp45aBCO`!E#VP*0oBfaY0ycBt0<g0JCW6^W1{h(Dre0SCQO<xMz}A6|6?a?TamBL0G<%8*T<}a#'
    b'qT!)HT155xNUO}HqsIeJjVd<LWUhnQK|J{~w8VE9j0YZ}nAkLbpmc`{p&ZJ=2`2P>njg*JBJhEb6Vbq=GrlvJ8BiV*MoVz+7i<@b'
    b'1#c6#rga7YpZuE;0*q&vywy3UXeN7n=TiiRM~g(l4DDw%oHHjRuFGC7&&vpg$Z+B@3lC2mG9rS0tzQhc1SR2gu;vX9gn5Nrur{bY'
    b'e+J=>(^3io;6dmiJ-}_aw+Zf>p!)d~)Cuiwp#iWUl3*?b9m3*Kp%BB+GUEY4Hn?wA66bml*Uy`X_{(iocmtv`-'
    b'v$Zr3ydX1#Opt~K#=sxZ{pb8wduvjpu?x)UHjw3>`1bnFt6)CCr!Vym%Ik=5qNMyb7gffatKh*aK5_d!#|r0+55{E7qp802h2k2h'
    b'z{&1Fq5&L_Pn4AVi7j>E7MUC>siudlUKX`v8^yO4D~sOS0;q>5^zoRF`VDZW{9YTjF8;GCWCC|p27W+5DMR+8?=(GyIg7W!^Yfuv'
    b's%JgeY2`FTcqsiLN~!!XP&Mz2>+djqZuo<j?+wJ*9HqmJJ<_U9X}$h!5z-'
    b'(<Cd;Y#jlkfPee$L4qyK%7$Qa^OcBJOQ5D^RY%P14{|EW=<q<D7VhS9FU<L_xF+9n-'
    b'XZg+<zykDb=$J>nV&=b?39!U^fJz3W=MW0Cn}ui$&>Lbp8Wvj4<MqF4XY@r0gu6Z;bVaHr*p3HL(=0zW7wRUIAx79$%ZYNT5ps7U'
    b'hsu{PhL2cg0?eu(5|0a*V@fc)`+g4?(U!#3FgB~levd8BKv|^xm)o+2BpH$lv>7^979{wd7fUkoW1({H=YGt_vY#L!@W5-'
    b'gjMBw#KA(bU9`kiqCz3A%YKDP7kO2%CTZK!U>i{oB6$CTB*~%FnHm`hycE>*RzEwP(&6pl#cd2l1o)ZP>Q5ftxjBwy@IC&zPsEx<'
    b'OLVq9gOoS<66iEQq6MaGgN)ez4A*dxF3v@tP9@Hm1bc4W94@@60ygzkkd~6xsVR2xTULbO-'
    b'9@f}&1PJ5_HcsH~t0XuLxOZPhPcX2?{%K9Nw81Gl5pEDjq=L{)_Ppl<tZTOimjb?Wi1Pq4MEHp~<*7e@ljl>4;ckPSVO*9`@>|2w'
    b'+h8S01}V|o5rBsaz_FVNe}3s&{7(K3B!|qJ5R|dh1nS&j*T@pUsuN+I7%b0$eHA|T;X`-'
    b'DzF2Qx`G>`MU)C+N!CG=ciZ6m48fBqdq-ZyM(PN=`EJH7rnhYMhc@%)f{~|+$d$STd7nCSS<Pi<;ejOP%%V@ziPFd0E9m|_YERY9'
    b'C7o+~#B8YHACH9x^-'
    b'7ltK_hxOw!`>aw#J80%u!>;n3{KT9R(HZK&iLy6Hl%mplq?X7dm>sKa4y?&l4i|7)XTvQ;sw+Xx%(e8HY%M@va+;h6{3ffw>mSd$'
    b'm*bc)`9^71+9({%s4DxD@I=F;Ne5={0E}Ya`+bE08|0FH-'
    b'R3e)dgg>Pk<(rS~v)U<vo&xCKDhg2*Lz@PlF8;z%dLSxDRuLCWwy<3==9KarS7C=#4o<GhGWYVl`9FD$<{aH{PKgv>5cUhld|661'
    b'djnAhQtEcmzlu5{2hO?V$~qnGR3zJ_<Pk{zLQ*tK^DU!K4hKpcb~zD{L%#AS+;=H*p7f-'
    b'Czntz)b`j^*aItDRqw9&;}((m!o=lyB2W=%YPB$5hi^pqA=TSnVnJJBlhn^XwDpuNt6DbZ*Jukn#J0HW>-'
    b'%ztwG#?hNNsk1tOy0E3mN)6Zq|vrCb=_2Fn3EXvE@G;)M-'
    b'Bvn)`LrLb@oEwlfSlgq=rn?NA(9zT{It)Pd<ZqMfvf#b=E#X^|I4ZGTKh|AMfzW%_$FJ!qb0vA#QNcak8V3+|j;!DsGa2*hmn71v'
    b'M0St*f$vSd`k~Po}-'
    b'y52Nv2Ks`@X}w@gs8FO7(OBhMwQRP26+_qe0&SGVSpYr!#mI22sX#C5wiUN=W8{3AnhoQ8~l$dDD*~$&F>pBfg=H35+<{8&x|(;F'
    b'%yms5ee!!>UYe=^Db~LB%=ty9TstPjv+r^5n+jI5$d4s&0-'
    b'AjiBLrRgjper{sc6*3#Z?Sbp#>;4~j;C<92X!ra>Hm)L`K#t&Nz$%mB#;T&hsR??5uL*Q^W_T6k!?3=A52{S@Gf5Q2XcLrNZ~Od@'
    b'e4WbJxcPzZrK-$~+=Fi_uWM&t}8t{Pbo5kUO9Sp9-'
    b'Lhz6=d+{Oe}H~9|N0quSPrkn>`I>6|i(RVfz5Yv$3`~FYQ7GDbX;NmTY2E!nlcEST{=&_vkJ04XTVwh|KkqGHJvGH7a@ND92j$~C'
    b'48-53vuvroOgC%DH2S)i-'
    b'1072)ich$}hRc)st9cx_CIs44&V+kERs(o!)Zi6wMFs5pkL+9Tc^)eT;h?xyy+fBlzDF<PwZfXMzsL1YQAH5tTV|KoK}f@wcp+36'
    b'5%}{P4$-a-NxSWlEAX5P<@pfiAz3jth|UR632+Eyz)SV-'
    b'K(Y?4q@sLTIkUPKn^qo_*L^pu3^Fc&dtgQzy~(f3d5A)Dppbvg5H7qM_r8=0u=Cp^-'
    b'K#}DC1cjwO12d#n5>%7Dkm1<0BgKN{1i;f*7L2lSQrpEH0*SvohD2GX4M}AF+qMNNHFTz1A;s)lH!SwiQf?*WFdud(CM%uafS^W;'
    b'3~!%D&duw&}PTn+Q1`tq#g+s&2t_k+m{4y$klzrJ&bE3wAM_hJt0bD_O%PaeZZ9Q*9*p^dcjR69+kDuFGGvZb!gl(`2oHm+BvfG>'
    b'USa@RFvZZ&~vOsUCweBqR8nJN{E{IxhDTUBYSVi2$%whMw|e;UCpcE8|>n~r^Qux`-'
    b'YG7XSq0SCcWd+nhWnhfD`qxc4CCpJ_IFPjIezPKwvBpDRwr!Uom)Kbz21%aM~YBzir<Ormx^7puy%HEzTGZ<mkencu3;gL+oGSKy'
    b'!GXXMl&>VEwTz+!Xibmm9ILBpXe`Nbhz*A(CY!tK#qYOTo;IG(2j!mu)udub_O`&Xyvp*HNnIJ}d4B^KyX+t7$T%biwpPI=Ok`m3'
    b'a9*z&g<WW9dl$W~8-'
    b'I#1n4hnCBj?mXfb)lx<lMA*mq>XNTOqHR8lVWWaYkIy}_C{%S;Zpuo|P0~|g0^0sCUY+nOfbcnd=A&S|d17Qy~e*V=LLng7LmbO#'
    b'?iO%|E+o?b(bO5RYq`>K6jxE{+22<k$FM_zW0Q;*IU=`Ucm_5-'
    b'P(7N`lrp;|e@W_*x(H5ewu%NcdK*n4;{5=x1>&LdLg+CF(Up?xZkZ>dwiVO*j|6C~|<Eza}P*HQXZ%?3kPwW$u|5_WbX5SOB5i3-'
    b'z0{ehGnr;e)BM7SC<J|V3ctVJbMv8cL0J8qp2D63f7N{Lt9f=#zuVT+etgBj;XE#7G-'
    b'&S$CYFDkvzb8Dd==l_k$);sKlOH8S;hN9F9FZd)Q;uQrfenz-'
    b'D4EIjtOs4zHu~geH|<eTvl+cZh_eM{Xoe|BG%JSRnx0oKK;v(A7+{>HHK3XRNd5a5IMg7lR)V|5`Ndwu=+X1_k`ya6ry8ns3t%ms'
    b'c`5`&ZvSC%>x2(}jAsxBi41n&Apph5aCOWVnyXH`)`TcMpu>csVQX-VzlOOLW*%?nPm-_ZTjD&R&mbx>wwOD~9@58Pi6-'
    b'#h_vk<cTf&Neoo+x!4k))?-f9ly|A8X$_CTV?W0<n7pExdyjqlk_H*me75c}Z`p=A!3-'
    b'n6b0atqA?rlc1HXv?TQRf@`GG*t443l)l%h1z0EUyo4YbIgS<4@Tc&Ek3qb#*yI%{0AIDB@){(Jro*(He*T`CJZ@PU*i)ni|pg~Z'
    b'U`Mq5BytJ2e}~JgQx%v_#EmDZUJ`zb<9JWs+sHj72BH+gdO4Mo@OAKIw;c~JF)I)+U7r;E?dTionlXR17+Ur@vQ&zsh!P*0SMSIL'
    b'WD18VXOop{9=W06?>;FYADFRY8ev>x)Di`8(&pNpOEr-'
    b'10d0=yb9P{+aE*~jsZ4e^iYFzY!BO>U_mW2zLmFO@n<)YplO<PVHZI(vcB7MKzr;#Do+O3rj8%R%X94Zg!cr%#;d==8R=oO$py;w'
    b'>?wNz6Y^lg2r<*#?2Q%yFem<q-'
    b'$Se5YrJ2%uMb4QydI04ImgEOvw5J$fM0A$!~2bvW@cbfghZ&1uN?;qVBuZ(Z^!C*6VIAz4AWMF<KZeix0*c$NQSwO{6K41)MmAy2'
    b'cWQiSmEEtpfFh)>zHsJdr&NigMKs%q2X`|<HgVWvMdDjDllA}YiJdp^q2^-re4B0*lCY(VojE3u6%HX%l>L)683%BOpwf_-'
    b'4>PAl=hbucwiq&5>F0UwA-Sg+jyLbV6du0%=49FST>U=M-'
    b'#TiD`x0S8(*fau>=Vj)#n))Ffh$$VXd<in?&0!f#uz*$>xOkDRI>(pTTQ?K7|nkV=l2DR4Q*ClidWc`V9cGw3}apem*uRzy+b-'
    b'=A<#LX3F|Yk=Zv6!^G=jv;g;d+mPei5R#_a|9U|C{&peqyq-ICiF&t<@fYs+9u<}0I$B_8{cK_H5&^4sM7WtBRJvyrpy`AULvJu{'
    b'A>eDnszyu#lSMhh$^;B1TyPw$4qPXu+w5)OCcod_v#$Z?#XT`uu=bPlH);x*Llla`icx+wz8MtEF2nLI-'
    b'!YGvW<@HdEG_lG@p%K&Z;5l-brp*!DvH_O;?4iUZEi4lTK&~-_!A1D_KYw<M6PF>J~`5$A5ajwZfHB=u!WMtdlJ-'
    b'Rw_RiuGZ)=L|6$UYy=>95QC8u$zN~zQwLBV&nY+b{@W1I1J%Z2BZS4h7Nks*SpnU-'
    b'Ba+`aHa8!_+HT-n=jdBbT)4Ar&9*VxiIPBiClxP`6z<64DAg~Z-!k>+Dm+@=W^OxCQZ;keWJ))dm&_d-|FKd-Fw8SY1OXz~E<Pvc'
    b'FZMes|kP=^|RI4bcmEHow-r;;3?FT>}3!M6GPJvKUcr!Hq&J%IV+9l{e(rbOBjhJv%A{s^r1-6Uh1ds8Q3q)<?jWrSxBj95ff-'
    b'_0hF%#lp{Z3h*ZHEJF8Hcd05@rH4K|IHkojY;}EQ&j*bFt6M!r{sGcC2&$^)nC**#PrTh+W_cd|TP0!h4w6@7aEx8@d9Bs33X4jt'
    b'GCxy{}S#Yh&j_2yxh|g0dT6abaa49V~bfH~8PuE8N|5y}2@k#cfrNHO4=Fvpo*m;0oq7_99NA6f6eC=)q^hxw%YxFwx@>%?yD@@u'
    b'b-'
    b';_xjR6F#(aw9$gq60u1OZ&Dkt695V~s4om#Wb5H*MWQ~ap<YB(Lbm9?kYcs3;601~e^PH8zAEG<3++#xp+qbW>;Fpa^#Q!eY!piS'
    b'N2r_nM_7UT~tYr3RG#`1}Y10*c>`9mqO<w0|Z>u;l?BUsKxyB#csvy!y7TC*AZjW{S5MYmIf;emksvxY*5wswl0-'
    b'+A{aPhv@Mk_rIR-Hf$4{6f&0RG8N-ob;|c`O9|{}`DaS1{UrTi_k6HTwEs9=-'
    b'#EQf4oqbh58(wFQ>_a*Rv6<FM$YB;XgM#$75py+cC!H~(fsgox@Gjz)&E)Cf^3$u2-'
    b'51MB_fmsE_$f(($K51BW63!~_Ny&gp(_HKBo*7Cv`5Ut2;#jR&$ywHV&M9hQH#0zvI%<_(Q^L{7L*<v;eB6l(n&xssZ9<9MuBF{G'
    b'=Ue#0qz>LY^{zSWp>Lh|*-yjJ-2LgbjSPy5FuGKv7)gafuSe{eo0=(@E3zZ+imM{#<=<8ph-a{l@b{Rg#OAHxzH$_4eU-'
    b'3S+IJNf7jd>Dto-x*VtVTQUu!xT)!R-hf)mal*PMhk<D4DtJ_AaGb;K!!bhzT6z-'
    b'UWprB1Qb!o|fMd!ze9B7(8ILbTS|c><EU`4^|o(kEpW(AB^Oa07+H`RTUfhBE~QALg>awYGMhGQHuX7knZ`P6iNrLKzj=vdG%oW?'
    b'pRS<_4fYNrEg&ooxc{Sa#_QL?XX(ehg8-aIfqqQAcY)uNxIDo-'
    b'E8saQ~dCPh~MCKO^({JKo}v0G6Ri0Ie+tOPEG)_twb<M9+q~zu*NU7`UuTXYT#{DR9;72-5aQy(ZL%=!-6DM&hNLAk`FA--8l;Q-'
    b'_tx!%F1?enF(Tp2+eX%zHQrP0)p4KBhh~I7EDuETgb`~0q^_oAls8J7=m4^3DJt;fQ;B48fLJ<sX$nq(zI=%ChAxTQ#Q!ZSmz)5Z'
    b'9D{;ifF}n$6Ge3B)4bEBZJx3cAgl3-0g0?Q?&w`z#HGwkAHjWfdG5!TjE)u<z>mL=XD)^tR}Q3W9(Wj4%*KR*{`-yPMw!!`-'
    b'W^BUU@(|GHUbMMmjrJH{#4(!keVeHDlI^P<A5|`I1ptqypWa*MG|wvqLxN1bAHU`GD1DRlsr9SGW+5uwqu(lX>_U=yxit5=sHo{@'
    b'WtPiJpa+VkyCcmdNURb}<T0<=HW@hHX*aBa0(?mN>MYw?G}8k<ZsI3>1U3Ec=ZK52OI>ugn|96cm0Yq78$loe~yIsAgNyGUdej)u'
    b'rzQ>j7-bN(81J!r48agLPS~GZMd`EklX{3nH?^qEHaHE5v*Mjf&xW?Mde4EJwRmXGJcH;1TnvqjZ7o)y&&{-'
    b'Xt6Za668pKem_sk_&6|a~(4P9#0f7fFl-KDhMZ-p|QSJsPh7tQ-'
    b'P)T*L#W5Hpc%x2DLojAvuUw+iUG1C+JuR<PmVTMKBPn=KDt$RRH_8N~=jfM)9NvT0{&;ZR^#+#!;vn^kO^%Rxzp*YP!`8z(}nume'
    b'sbb?{oF<=(xPWNFS-qFccgo1gp9%X-'
    b'Wr;%Ui0H@_T#&a3D5;*W!VB{(z#G*d|OrBGqs(7(wK|G5g!`SdJ%h^a5)Ho$eq$AzA*6UBSe@V=g!+I*OQzHwsA2GXZOUrPmR8aR'
    b'{OTvzq1Bw1JD26s*Ju=+f6+f$mlnw+88(5%ed3paA!<Uv5iERs`9f1-r0q$m0mMvRqc0e+St%Z-'
    b'&Q8Vjxl7We#%@i)|IML7I=e9GAeB0f=ScdhuHJnr}0SU&bWfJmTE!0Dgf&xoan2J(f8Sz<g-'
    b'f5UaI<3I59>b*Hvv$G?0>$2cKO<iVk?W8ev9c|EKEDbmHtRmo3PO6U9(v~kukS*nJzIQ#Q(+ehJ776}yr4_Zs0g*DtLZzNA}-'
    b'Uy$9Y=cB$TyHCp6ML@kSAPR}=bJlLS6Lu5A<qDNS+Or?{27^Nu(y0$o(LKlIo@5`_xPkownLdX5BHmieeX^jIsx*Ern`;pqoQEg9'
    b'J`dvT7|}=Hp^+xtl!9w)-eHFxV!SPqKXKZ0T%b%rX}JXyA^ei2)l{yji-TK5VG!R?(e0bNAK|^ut0RPtL}m+JT`Anuy7&NE;D|SA'
    b'O<PN{7&#eqb1Sx8>6GenD9ytIz)Z|DBV#tP!i%9_O%0iVq<NfArJQ!;9y!HSPk>D8!R-KD)AT-'
    b'64aF$7Z#(xLk%1j>EKOh0uX%qwh*-'
    b'd<u)@zE%vAG+B8Y4!t4O(%?mzG^sBvE(sTgtY&6N%WAf`f%eWmdWR2DHkE;)%pONLS9>Z+lMu&t=T8iV)oocw@)5C*LTA%UGs{*j'
    b'ClHvQxf1dyWi$}|EGlGs10z0RN6S)d<v8Q5H8hkyndhmbXa^kR%r?2a{Ib_3Hs|z!MJE99SZ0p7f2$c$}X72?G{>IpNyBzU&kPFf'
    b'XlkOkCSxDn>+2~q;9!Ha|4AT^`k6nLY4ZFxEG+QUF1BepjW#h&D9gl`&$J6!pKv;JG$LdX0Xz@qKpLzZQooMh(;J6UY)zJHSr?19'
    b'uP?lX0wGtbYoUG5rl`lu69HJdT#~NGn7N`Offe^~;2(Hy~!uB1WuqZZa)ntExm3ahF=PzX2S!L@Ud4kV`7B(3R?)7p4(?))Tuf7<'
    b'G(15juM=huYymvc8=(KL_)crXA25K_u6!uPe>*np9x)Zqbd<i><uX#V<gCBS+N9qFvLOa>0|3riE_CZYL=ON-Rv<YGT&LMvJo5Yg'
    b'x;ZCodSt~S!aHoh$#%=fIS$aYs#O#^7-Cpx;!}FYee8nLaTflFVQIc=PG}-'
    b'*OWRHLDwkbHw>X>O(&s^)euVvXIsI+*MuSuh7AC6T4i~eJbkhW~^pv9j@KAt>^!Ovj3kDWcBpB?fceAB-'
    b'a;nT!EPt(AHO%!zyNo{8E-@1&B?e)i@El$KumPkyAE5h(gb(8_Sw2LiTDt0>*V_(U-'
    b'fa`@K&q^!H(`?GAp~4Hgt>$ol)cfCX7SD}g;}eY{FF|QIF31vcMTY$rFa!^=t_Gllv;!oi<5M`|`Igwhcd4Jb=JOnNoMN27$5Tls'
    b'f+Us48s&Bd$z-'
    b'K%Te*PdV=3;}_PHy%IGX)xVbnJRS<K+<%gK5|AGV4~m)pj|YuaFekrQ$*TQ<MB0?lE(3wi>JKrTfr1@uY@O(VTxeVm<RFSbofc-b'
    b'z`u$296>G+wSfH>bVJN!U(DjA9e4`{F;<VPD|kmFG>7-E!F7DW3|ZH+-'
    b'f{q={>j>Cp%hRs<W!}Dr<!(<GE`GrN)u{k7r=h+RS(DuOM?%}K3x;AoqJz!iylj5D%S$5^ae}Uh6V`R(8x+htKZOIAj)Jc28Au{K'
    b'iRP-'
    b'p1ots>2p~(cjU_)ZMh8+wx>;X|7sfZG{?Lk_+0sT2GApELUA?Opl!CWr~SqW`e4SR3%2Wkrd97Y&e1P;KCwG{Y^sioGwv%7`mJy2'
    b'kF1;RSz!tcqW<AZsl`L<@kyw-9oC-L-_1VXN?l^9<W>WK}sMwPKR{5>Skbj*k%koiPu7he6?Nd1Dy@dOK7%Yk)T-'
    b';{%w5bBGqqDUb(ND=;|IivvKd|-'
    b'Ya<`kvlan7j)DfW%jA$R%h)U@pxG6iqnDxnGey39RCk0jYL;yY+OfT89md!QJ779bSZ{n^d!sK*7sOe}s`iR?_laNh)*D-'
    b'r0<5e2U!oq?mGqa9_|pf3r5^RcZASI)>C;<4qMz%jqt7aHb9YdjLS6oV5!6bzRW9n&k<w^^F@%`xf3MZoDTMmjwLFGI$Zzy#u}32'
    b'j!VcN={8WVATM1lsqG*lS<<aPpYxd9u^`9y6y9Y<#!Z;pkN#;#s-'
    b'~nhPc7!p*~DR>0`G|4N+RR(Gi!E?l~&3HYB~twUQ*W~it0IQwu&n55J*J$twK)Aj9CT^`}G1AS%3h2iEmpVH9{#hKJLG2qS?9;6-'
    b'1OePp?8TW|!Z|?PC9c`0asD39$go`yr6c#JvM_INMVId}5t^P+3qZEt~0qs<O#DqYA<Y-'
    b'TN4<d<?$%$y!eyi7tvocnVSKX|Yqr*J+bbcEsyS0FCiCGm;%R;fN`pQHtxN=#w@)8^Nf8fP1LE;5agR2rMiI4J&)xWF&>r`9-'
    b'kMIJt2X7t?>;@|D12Y!z9b)HjInM#j7?jBJ^<j+untOuf1li84!RL&(xH-=mA`%e}rsm!7b}SN-'
    b'(h__YdJ5%@R`#vm5?`kBv)zbh`Ot4Rj3H^wboGoiI;yIlJD?(YAls@Tc_q}x@|UlbI?kGp1GuxZVP#w$CV&goZ8jQ!0xt*KAoV!7'
    b'%S5CckCX^g>pNKD8SV=O*<Kqj<qdQmWARR&z}q!bR8n%W>#E2|V=GSw7hysEmKd0_Zh_@Fpv|!b(c|K(gQZ}h437b$SYZBfwk<$-'
    b'6mCY0Z`AKnHb7)SDF<tz0k^XQB5KhVA#==xrGq$0co7@`-q8+}_ZF(Y!`f$D8&(@EjJMR-dXp~ELCeX{A%M={3_<})5~I1S-'
    b'e?f#>q|<lXW3v3L$U|NQ?qE@K7uHA+cY64w}tb?DcH^12^I)tjcVi3&fif^m(W9O;CIE2R-'
    b'2Bn!fU=`et3QR`Q+#?)Dk|HlO^ozyZ+V&Z#$0%_|6%v$eH{$fnz9UQIC*S92Xd0DOIx@R}kmcW##c#f8*?|3KNH>K_uAC$I)TVdn'
    b'3+>V3+<=oHv@G8?svq`6sY~apylKI+|4!kMhtNRko?4be^|J*8xd3ZQ`Zu%`z#2hC|jhn}+8%cAclZmLpE#;?*I+@)!IsnU`hB+S'
    b'^U6)O42KOm+@Ctx#e{MEvXKTKKqyOYK6-6Ytn0cs9sSz?JjWgBrZcS@%hRq@)34Y8W5z_?6-'
    b'|_|y$Uf2?|5gl^D*AW&_t$%xMGT>#iw0hJdd9CzJ><)AvQe~I2VUycWfe~-'
    b'2Kc>L=Tv5H@gE#ZlS12_N@N24l)fY>Fi%3sv16N%#_4r{M$gLWbz5y83e>&<DggZr3AL#s{?L+TqForUn-'
    b'7J;mGJS#c^xyTA`Vl4tIWvBdr!B4R|2gXK#dz@tpiv!XK(U|Hti_CTz$Jjc}4MjYpHN!!qkT`xFrWNq>ZX73ATza1R7FzW{)4u}G'
    b'ksQ(rAB~}};hZu%D2s(QP@4xjYdHo{6l<}w{jHPOc<!+F=MO0IOfXC{;~r=_a~X8&_HR1$_+rnku!DJmSFG0@_zsVihY6~`8xih7'
    b'%(Sy(Kg5(s$a22l_Iw1oR=_{a-'
    b'1`LH>3+3{u1nHt>i%<0;uL|6uus5sNE08+K1$i1i=8w1&5}Tz^Gn^We}!wB=0H32Z$@t%wK|m&oIr-'
    b'1>4_BZb>Zc<;44|7v2bdjzewRO)Z;=5NBpyV#}&<#=|a{fFwR+M;Ny8u+Rz5UP9)aIvuwb4q_o%V`MC`N*)h34MllY~c%hj+$!v%'
    b'^2R_)rlZe+28m#F5ijg+=(VB;b@)++VIvnIXyGzL<hA8orBEy`$aU@zGTb=bVZEds*jsVn%YR~*nj`<P;z6O>J(Bf{xW99Z1;K2V'
    b'!!zHcm8jh#F;hYz13<Kzn*>hApUyi4rza|aV>R^9Y@Zh;T+tC&7`9oCV*B?M8za>f!>m{h61aD&L8Q%W#+bJUAPLALuaOay}h6kI'
    b'Af!_@Y9VkEJJFSiQ9?{pi+r<Pm8UJkpL~wk>{Yq=cTw45~Qy|2gRyjOc$G_{Fz8&^#;3CDWr--'
    b'`0?6rxG2P<(_Iwszrif<r=TvT@aE(nEn?`_zFdpZ+6O7fCpv&NUO+c?!a7*}y<Gp75dM6F$qwgeN@u3}-5<;`$8&-@E9<e&ud{g-'
    b'LG-uWOF91fGCo>i=TSK#r$VkJfwD2Bf}M{ap=w>_E*{>Js!U4i(&%xOEt|K*wNj~#&69UIq>4pQu9xpe^Oi+t(UQ5!x{)8B0o6N?'
    b'Xk+<jKDW#>B19COec5NvT=HKj33&u0hYzAbF*0q=jF{-'
    b'<D?rpf{YGc!+wFQsk~*s%o2);K5$yWIMA5*hZ@09a%oLGX`lA&GBi(TwetJFD7+o%vjdqk|#LzeRA4uw^rkW9}r1j@7i=<uCD~qR'
    b'N(KXXn#SVo{Wi*lPPY1Rp|a1M|U?5dG5&1qiL>wgWMhug}*Z9#)|=tKqHLYmQj(<_ky~A!;^^auISoxL!9h(}qDU?K<D_=$+zi>n'
    b'zeFKNxPXtP(pc-'
    b'M$s*E`M@KZMPLkp8d0yj<9nA`SmH7F{a~Yaffk1U>&$(|K@Y2^A6Vxurvrtv<%!i#sK4Ryr_q6@%n400X@v3O|M_NRF7-'
    b'S4%Krs@Yo75YbuYqDNs0XSGk)@Dsc6$+Iguipc$3|5(7Y!Zmo%P@hxTG<CbIF@Ci7B!}Zhi4i?NFt%R>77FL?=7(iT)Zh!esM-DO'
    b'-6WtN33y$L`zinDH_le5Fs6n;NR$Sj$i-EM`RoT9V1wO|6$L@KI(hg*cw;i~;HY_}PND^NFbQn_nQmfmpz$+pM@<O-'
    b'~U5N)b3@bRe(i#4aseC85;IKB+q=*4H%ip}lmrb%d!|Rc(iZxW)EN*W3nJ0On62TExZp+SPm1Hp#UzR~P{o<oZUKHSHVx=Ku++*4'
    b'4C|j)Nn2N%f?&S2&Zr$Q^CP}T>euPNHuLl|o9bvvzo!P4yoOtg1b)wQ+;bpB!@X(Av1sGed(6{A!IQmNG`7&+G{spkb))Pk-'
    b'w`jSc<%Gy7qNp>_L{L;GC>Hpp@I3MMrib~Z$l7HinEkUDGJ4bEX=@^b6hom2L7PsM0L~pBZLhzoalK+G{k56z%X8SRWp?LEm*p96'
    b'C5+m0ZcmKD+)GjNaRfL10Q@+kF#R>XvvY*8nmh1oiGws2+v_&2!V$EbqFH*_iT1J1HUe8Qz5~nuI+jAR2Az=YWR?sAWb?b7Sg#P8'
    b'XoG1WCWtqSiZ>gEF-J|`+LbQ}ZccVMsfd@aP72mko$g`2ZeYsWx>aJhS2-Y-s$p{-'
    b'OKP9zZzMf0m@uhiT@dnQ!UCMLpBx&s#H|FOfjFaWAq=KBa!F5i@Zx&D;Vd{nMhd{9q$Y%4hmE|WpE@8)JOG?9;OjUQpxV!|EDqZ-'
    b'J3ap!O=YJjdlVL&9&O6ISlS6rn2xBmrFtXyV1c=KCXv$ZKrBor+bvbTC0=G^<vjOvW)Wcp?lGPJ?BE*Qba@VppbAc|Y^WBbX`GIF'
    b'd7kf(-'
    b'(%qoeFOp><6%NK`n$b)A;IHZQSX?@!BHFeyaQE&rJxRX`wD~2Y}oPA*=EZNtsV!?@yd%26C*C00UbJr2eaaKjhg>gn#V6P<V<9T='
    b'7tf?`~$`YN=zi%4|B1Pu=K_=cDrayuA#p@wRF5@`|hrQmq73X_LMJ2QS1I4mIZX%nB<8AVb4yS@%pxGU1}N$V!8a4#yPZjIyA2nG'
    b'%dCYo@F}*FAzf$e<4`eZRq4dV8n~$z${06K|a3e7#1M(+Zx*Ya!g?|QPR9|!uF2d*c}AlQ;V0ILF4KU>CFejSm#$b<A7jC2S7C5g'
    b'VnNn!By8Of|3p1<|w@9<Kzcm$bvO2Y~{Cg`;VnZ$b!>s>}miWib+E2v|vXaI5aP96(&LSd2bG|_BZ<PVRZGo0z<^h+NV`aP|N`Pc'
    b't?QTDAanhnEX!4=56leHAU<tt7SQ}_bdFKhW9sq5!$=AR6KU97Uu|^V|kL*6JpG^Y(@aHDddENw8iv49lm+vcS;Ndq6TMPdT3od_'
    b'64n?!(NHto>bWfXkrT_0{GtIh4wA+znUisAtcf{;KeZl*$&cP-$_oG_AEzUUEi6PUU*<Zq0I!x`M36o{@tX3z~G~-'
    b'lRaJqlWyXNU8$v*9>FN>?CQn#ti<-fI&6D-'
    b'r_Sz=><?>amo<FP1%q<lkmnwgfDNd!8JTxFZ_dD=g~q#<9or^8>vsm@`G`|h9IC5zW6;4$hv@Y`1ombHx()EBI(B}W6SAEMMZ|J_'
    b'Z4vMum~8GyA8#k&eHFlt=_h_xiw{{<^Gddm-1Q9_+ldTFc^o|c+cZ$HSoU(r;4T&=ZDqVMYl)cKp#tWjZMq^BvB=G-'
    b'!S6U}ym$TM8!a(2P+HCtmlygFD<Kfs0p4CsX~vfKCX`7D5ZcuX!D4sNs`<h1w9Mo`k^qrYZ%~o{AFMAdl7Q1i76(On>KPm+4KK4v'
    b'py8k69f|UZMC=Pu)0zXSACFj8GjU(vBO+acZ&r1q`%p30cuN`si*zF(zC`c4Q&=#29GdrTwfF6aoJq&9Tb4Jm<_qC@<sN`+Yc!*U'
    b'FJEM+PEW374I6K_l?BcXy^|fv7TRPB4k09WmeJk>k*1z;>IEd@Ip64pX|HGW9utc+!|9GS&@|MF5t`#JqE?sPil7+`-'
    b'PsBzB>LYtl$&>f>$A6z$a?;3V7GTo9>-zCc)u4A-L+J6av;s}W)jN;+h0u^q~s3rYWp%G!W1AJ#Tx^WJ@81>5sTz}wi-PZhV0Abk'
    b'`;jaZyJw%IN+Kw5@Og0#4OU4@`Z@NgV3+h8x`;ds2*Ae7w{qo`=YF^{%gSxRw$!djP<yijm5@A(|;a;8VgWW10j2+2fr|$Jk6eDd'
    b'#k=<^<$6x4Tp4qApUsO!IG!|p+XSh@s6Obw=@0uJskG&{?+YpfLy+MKOzIX(MgTNrUUCatTcs^B(HR`f6wF2F+9w9r%}o#6L#<T>'
    b'+hJ$84(Uwo7e)PAqGpp?33zJtc1XO>v$dQyQ1A?)hQAk^<4IMKrouqgy!3Eo!<!NY#;=Ex^Hy^&fFI8S#F07d83L`6qG{Qrr2+SC'
    b'j`u??!^X#cN9eSl0}S|5C2b=-'
    b'eE}bIL^lV?mSj^0_T8;=5Hvo0}t5JU@>@sxbb^?daH>Dc9}{V|LL4^>avHd4}{06H78%D??CeQ0uu;}O`BftwH?0c5DljmdZUB4k'
    b'l21UP?pFx00DyWOdtbLzW*CB@j5BU`*188Dw$=r@WTd?Y(3FA!!p<H_`zUZ(DIxdj2-'
    b'd$^wjlU`axtE9ThXrwnTqj4xHsLJfK<9<?TTjV;Q;HKK`b7n>ziY0`GKNUSL>WJk^3ATeY9QI_txWDtSmGH;eBb1p~qV;Ji=>T<|'
    b'MX=1XiQW%ZoI(6*&<$7^J~KhjZ0e3+-u>#fJ1-'
    b'T9(U%<!V5`>O^zPxoxgyRSTKwc2aH1#T$U^<IAEL5SOMHn0!H$E+YMs0{w$t1pHeTqfA6HJ||rW&b8FSR6ct)mqWvjn9ho+nb<Yo'
    b'(Q%{jLvrih=d%O2r~hw6<*eYYH9X`Kq&AdTf}ai$_%grm3j7+JL0nJzpk9yIaBAhKoi)6z&l~iBYfxZSa?hTMP)5ZkF1@u4r*qH;'
    b'6xjC`j?|%HEt=472}Ut=^F8svtiuuDci<bI-KlsCYP`IsAVuw7<Nv7jZfzpESP;-cBBx9EJ6n!CY*hHE!^ecd-xGy6OPp0p*UD2&'
    b'@;X&GJBMx6(*@p!t}6V*PAv{vSH&{PBu^Lc&^vWJKeh4+iK2x?fdTxW_!aIpe3D~)5~8<vWx1iHFe5hMx)(MU6v-'
    b'k_rL^)z&($rdEeyMw#|rP8gO!Fm*9wA2jg59!Zz}GUS2(uae(JoTQ@FNc`xrg`lfJ)vTn1^{LPaUhx&I**_%~o=`mJYUx4g#jjjL'
    b'*b6yoR9&jmNLHQnzcEJ}tD71}VneExo<q))ZJ*Ev?GXDY{yq(tK`EH2r==#R4JDTQhsX6cVbQYF~GEFEF{uEDMpk+y9xUyx>9;4V'
    b'Fh<>QHNM3(eZEtT~M*k4ny{6O57ZPhCcyl$~W8XB3`gopVDK)T|Z3OB_-Ot09xBNjNFK-Po^V;^4l`t$OWX_AF#RW9Uh|ajkp>>Q'
    b'bz!2m94kV|825qN__VI^IWWI1#i@C$Lirw3Xs?F-'
    b'Q5My#qHa#$BIJaj>Ki8C6s{(PW>4*Zei&i__mL%P8YLigaEQ7UO6qiT$9{UI|lD~3Ome<C4Z-cOM>v8-'
    b'pblsFza7Vx@@3T2da~s0V)FN9Qc8))OhbK>W!WQ(@;vt*fz%9L+Ezh3h_c%<e!jte(uj8?8q(E81jhy&zOC0LDv*#rZ=;v#*<v(C'
    b'K1i`UE{0B0Y37jgm0T4zD&EbGyeDl(Cb0N|T|H%U=BIS(?Hmx73t)GycTGH(-'
    b'sNroRc%HWdKnUyy{SF9@w*?ljD}7VPP`VYIh+@A~jUJi8LaZ6|YOp7Qw99reCl?Z5|ElD>GYYLOw$FcfVU<l1Ye15djg^J}Ec+E%'
    b'SsC83z;ZXoX#R~BXM-=?AKM6~JXjbnM{npkN1A%`xR-'
    b'?KBDZBd*(%oCE(tFd`Vw}8uEM`DyJkZnk{L%u%@H4p+6tmEE%HzIz@m>0PzP6U^R0*fSh@%v+l<S_tllpMAO*AE@3;_aGHtipPL('
    b'DM*&{IlGWZT;^7*E!*vK)gmL^CZbH{m98^0VHFuVqX#kgb5CeQ5bvyjP2Tvjl99Q=2S+GUy!25oVXW2$WQXi!t<Xl#k;y!b_;AHQ'
    b'nda~h}E_|s9i<G)?v2j1C4Rd{2sM?BN<9rl<tTbGDzqLg<|yti_k_k!Ox7V_@PLfSYqZFp)<%NxkN+21Kt*_%eiy7IQJB968#9DN'
    b'|qA+vn`74z50?=+z|Ty|@k7IL~)t))A!?t+KIkv$5;iY=Dg?=0{q*aGT>!(X}SF=5hSypd(HAk);><@LM68=)P8?c9gGVV@rIJ1h'
    b'KRxsz>SV|??AF)?f@_~L{&D*=eZmq8INXNmul=35}ry-'
    b'?^Ki{r_f6aL~i8Lhw9%x4>J9i20eM|B=OAUfu07F7YuCU0>8)QmSl@Zh7{xmv%<1@j+hCBD%$v``1_aQZDO^URpMgLJ*~hm}ATAF'
    b'#B)L+qE6HognvWySpW=*`~1ZeIu#9Y%uez3h8pp@XNUrtQFN(A8mMUTXV%3MPA_!!6x><Q<M>M_lmOsaC>?S+!%&4`J9*+LBVQj_'
    b'^zex%AByFupfgn}wbpB|hx;GsVd(qsAR@Nr2!NyrKy3MT^|+cyyrf%ilyj2|PUgvSzJC3w`bcoxg5S>_$yC_*=A<$Mg;~i!c?OTI'
    b'7W$?R=A8y%KggS08YMTy0SAv2D|v9O2R3D^P~3=EdR5Yk|C_OEH4o{;4}jV^`KXFbM{qi<OQrE-'
    b'S!_2RX%yPmm+oYRfmR;(<dWQhqaD95zAdeJ`<l-u7V6BaKJuZ)?%-'
    b'x6*n8h2DhsHV4^VS{?TDUGYVvtT5)|I24E~0@JDh!i%hzDDH_sQL<!tB#KKeejIvWhWY~v4~o{Z0nx%GXGjVRZ~)IH&?Pf^qq9>p'
    b'upbLVwv)6ilt;6quWqY4+~9WlEROS-'
    b'A}Fk=Jrc)EK=zuu=qSfylK<LXt77wj6J$M&`8`c>)=kc+@o{j!*^2@TSs(bpa}zkPg9JffhUHM7;-'
    b'%SEU?0}t0}99?05NtY?6o&J5nyJ(pEm$GY;gDl&W5*h!#lOS6mEE9tl{Eoi+HT-C@kBhmT9n>V?8Qt9)1-'
    b'8Kh#0vN7y{e+8qee<p-Cx^O61IEm?fF7vfktJ)N#zY-EY*PdvvFhPMqN5aPEYf=`Be+o=L0{bsFZTkf1zSd)n~Vb(%+>w&!}1Udo'
    b'hcGfdepFIO_qGQ0kV-'
    b'7+0rGZd7CwPr_yRAX<g2=mjHv1ekoWp~>&^pHqb6(X_W2mVY)TjN;zv&MSoOf~9D3Zt&Owa;uP|ukYEMrH80?gS_{vIB);r3JV2K'
    b'&q3$Qbs6MzPF}=v>~Z5|c$b@30W3pGS{7z54PUazVt^92&56e>sZgyt}+rf)*D#`Eq)vqLRusugAibvCaLSK^&@gw>M#1h3D@6Vz'
    b'}3Cu_N1d*XO-'
    b'o8#tI=uMuGZ!fkP)!6c4eU|zt<dVy*YfKcq;P7&xk3eX#|h}Ft5+zX3YZzXtij+EItOX9LeWS4i*KDJG>i(ivQvW9!BN4y^x@jiF'
    b'=z&bmb!;>Etz`<h<bM>lnFFL*#;oa&RG~Sn7xV!`e-'
    b'&eN}f;g<JKeo9cQA;$<f8MgA+j|N}G(cT9D$WsB=Wj?V1PTHJ?ty;YR4P`JEoZ_f<9k<;!)pL3f<oc-ktu|!V~I@pvI5I{%squFo'
    b'&zWrv$wZ-%V4U)kF#I41BDRZ>e%A6N!0<uAdIiix98@O`f%cVd|P-+^YTEu0U(XA0~Bj%&S5k?wci_S-'
    b'|{Q=={remrl{tA&plA>M0zh6wJe?I0w>XV)_^~yn$`4HXKxx%d`0l>>!0$@0CZUJcW%qfJRY-'
    b'RcS12vw>ul~@r04Z;bm{Hi7*ZEPT)I#1)h(jZ0IWuLuL^&0ZzV-GFy%t3y$Y@L<dBx%Qeb=Cw9#1FKY6rz=!o7$D>AezMJP$$y^>'
    b'tZ40{cJG<1=*<trVcJe?aB=>KKn4_B&#R%R30uZJ*Ywd`2%h>o-'
    b'R5A8wfy8vsH^BYej)8HYUY&m<qTfW`u^@jqZ00}J6gE|d_r}oVx7sS^uv?59Job=j*lHiXB1R%LTi3yn^;8pu0d)bRS%eBZ`WG>8'
    b'EGw7nVsNwtFW-'
    b's>cke`yFJag74dUKj#ARvm;{+*LgBMEOfKc96&n<=SYF=D?d+jpe)mdR5Y*iwYw_z@r*_Qe7vz~xHXj`Zgj_zOt1ZnL@RQA4ibJW'
    b'K%lb>WYk)AAUR`|WGxgANCBpACXroCOrT-'
    b'1WGuGskD<De#+dhhgsXnZS)kR!ac1uKh4dk+WcjpEG)S*j4v;?2(XmPCS;Q@k5OFaMd}y>#hm?;wx^pE*`9O(87IZgG;+^zP|ENh'
    b'EXkq&&ZKR3}jVVezt(x#BjX+V+k@L~8{!+^}AWEkrvYA-$1JH;wIbd@7G&MR;4|-`+CPf}?At=A~F><rGQyGy$;#e-'
    b'kWys{ykpHSMDu*!S7q#9O_1@$+y@%=>WAT~?Br_<V}DdGVCNa(?{F10uVTfw&v;jP3N}J-'
    b'Y<^zd8E}_K+;H2<aVA2i<Ybv{A6}*xe5&gu(my$G0D%+oKil{Kx&QK*89F<6^s0scxrTv1!PZ;Q0nD&9OJcu6veuF6V{Z3H6yy^Y'
    b'{*ypmuMEJ@KP$V(#X5iGeI(x85Z94JI5tx$5r)%Qksc>+$9{49cS6Y}Oz-'
    b'_6%Y}kUZXxg!HgO#G_~pZhBZ|ImN@je2@8avW4*rFbfXvcsoAsc1W~<;QU0QdOcUljso)9kjKGWw(WMWu>di^gb%i+#PoXB;B{YW'
    b'<aHpI7bDMR+RlreSc+bW2gxMzaGJcs2%LuW6{9)AH?QQaAZh{xZf<O)ql8QiIaeBH;f3n9f;vKzrB{7=3*Y&QLjbpTlJXPf3|PAz'
    b'(EP=zg6~b%=m5+Pp6(cg<Pd&`Y298;f~!0q*{{|-p_Jf#)&6kj!a74a4^7g}N}~JYV7B5-'
    b'W=PV+I##Q#>vtk_JF040kKj;|Qy{9|G|v8Q$m?E&=HS#Nl&2@LUTBb_e&<Ex*LQf5$J^ZMZJInaSk$~Xu6yn<Qg>7WGN5@=$#!<O'
    b'T>{lRj)*=iSpS3&z+o2TzQVk`YY4DHd>`bz2asNEL6GrEqvk#BtZue7?u2#oN#Dg$*<QRooFjO9M-'
    b'^e0_q0{Wsq$qPLimO3vlGG2^Qr7?xvPXM=lmMx?%?fk!9pas*kxUxgYBO75P-'
    b'oa=j~Z*xv>je7@I<(9q*(fjDMtUcq#kx@(1S!u^haVbte1b$;_88%Z$9BJvzO^>Jl%|hN*57D4%QQ>ZM1w*Ki^@OuGsauzQfyqLb'
    b'_)rnPa$d7d68EIWm3*H^y&sdvN;tj4=;5I;5s2s7`sbGEnN7K|b09HrIYTe7y-'
    b'O*o_6OO^jhoJMtY(?sf6w+mEOKs0#0&{I)B#L!&>HsXnnm$)RannwA*<8nWK<A|qI-a#x74psMsdxheFye=WP73g{FV+-'
    b'CZkWkKqhbMXA^>^lLTG|E-$QU#MPt51N?U<0&E_15U*&NO39r}R7FX}@C9$xfY{@YFOPG8+-'
    b'b%&W*ZxeaUw75*(xM`Nt+hbug`%To(Y<nRw&@%IXd+MQN1zY-db}6ikK!2N}u^Dh!cB1HZK02N;J?2#KLZ2Rjm|Yj&&CB7o5~aV('
    b'W3jKJYVql6Ce}f(ka%o#+B*zvMQ_J)$V)}&hA$~)d6s@)nT%!Dd;u`<3_jRtC;7a`MN2;Cq}~)Abp)oca;(!={OUZU0dkg2pu*lA'
    b'%)V{JeBu2*A&GH&IROi*hCY6F=An=M0P{Oo`bSmre1$_E+=~l+gli4edl^=#G_bFFxc+jtS7T={SkjdCvC5!)Jwnjd8b&a=k8p94'
    b'KwaL5t{``*oZ1J*I7DMO!sa*vVmafvr1CwDcV8-U>SOI}vDV%>7O|QE-'
    b'3mKo3vAE!Rd0YnmmK?hoC#IF<U&%$q4?|%al+)1ZqMNPN_x7dq3e2wMMkfQGu`q|60LSOwCgKz`bQIk>+Ows-'
    b'Z*qR2zNQFa9UG!JZCD-$dZ>n-'
    b'tu}w{k<{DVtT$FHuj}ff%h3a6lQM_`i|TvkH=aLN&=+34Pf3@!)5P!aNO%<L+MB+2L8sq^;Mx%<#EJ_cG{j{l(1MrCGXtb+sWvrX'
    b'BOM&owup08h83D4!O`-'
    b'UeyWCgPkpSXQ|hwSvHtVXG1Y<jXCc~Kji(sEM^0f32cAYbV7;H(6@(i$E3$`8u)E~%j?lCcd)h40%$KRLX%ZUCp$H*4f>lHY?XLO'
    b'Z?8LFjZtI>atzLRMW5QfQFC}}N0w94z3COk-'
    b'3ad<WY)i%G;Rx>y&cCwt9Q;C=4WFgV1`k7K?PdHdOO&4G=Og}x}AQ`mod2rfZ&Ozl=9+e2W!GjJ(s!hf#bj#;<nePhBI+8FIqKK4'
    b'NBIpzSyx1Zk$(2JL|W5Rf&hpe47W@MB~jHIbPQDe`u+bg%zcjO@}{1D{*l=iMR936v2ac4pn5A3K1z=9u2#3WV=&k_j~Vzu=ma#|'
    b'8q?xAPW#6TzGN5y^aeqi7To}@ec3*1wiu3CUw%yS`r*DM^xTl8P6h$RY*iQXL^?7kr=AMqI@rPbGCuC5#E4B4ED(^(Q}@LuJ8?Iw'
    b'r<(#5Lqk&!*P<2mv}k&_4c+f$D1!NS|i%vZEtSVGFz6wH~9#y1pt@#uXoR79ZGy#PBy#@%LbC<+42N`&N4M+;p}_&3hEK){N^U1-'
    b'iSXIe50p8PjDbyxRsavILF(O20&?pKv=}~nrd~5;Q+_JMg*_5c@ti>Dh>hQhb8LPGC<=@$XM-'
    b'r#)Bu=veUd_z#`SK#`*59czECRa*4-#Z?UywfnKz{+<V%Z_iU%?5D3CSCXlEz^Lu>2%70zQP81<-'
    b'tSd$w!`V3RRdjgRQ6!Au{0XAF(<e~)>@$H1?fBmP`!@=2J6VlAWj7v&6i3TN0nzwa2I=if8!m_S@gW|b*k|4CFH}L?UzPl20^Z|O'
    b'NZxd$YbQj`r#j7#zfbSD!UjB8LhAsOsJ88Rp0vDy^*a%=oHV{SjlbWuT`1d~Cd$<_vp^KC9y?FW?yYWIURVYZ%<-'
    b'!g05~qM@3nKplC`%b|9&P6c&}hD*|1&FD?PyQ+p)p8C{oLLe(U2mD9oav14Py$IgRi}F&JB)b3Yz>IW-'
    b'8Nb;gyWGH`r1(D6XyE1F)QVR9h4`{6y;J5{e&?#;q)Vp{TAx)!YK@Cejftlz22p3&dm@HvY=qId2L%cJ@C0ZQ{;$6DQL@5M$SEic'
    b'<6cHNKd`d;s6<~H{)edvvr*_l61?d-'
    b'T)@Wu+~QXS=^gO9P==%rfn;(4LCtfXBYo<9AHns}+ls6i5B0Y!i`gQLNkq!`}R6t84iD70>78-'
    b'ItGk?r95&hD_wOY6K;#^FI(#D0cXiMIFnqD51vh@tmR3+I+O*Xu#~?#CX^ukX(3?2e!=Z>x>Y8Hpa*x|ZxfoJZI=nIJZuW#Ucd%S'
    b'rxTK>SxU{UG3N$h9!h(a?^X18TfR$ab3L7%uxVoH2G0jE4w(dFdR?>MNXa;PK@uKlwrZc603&;p=>L2SRlR#(BAe=b>r&J>4rlte'
    b'kc<`|qWW2gjD;@p<7rE>D&@Sv&8TP3UGqhhb<AmA#!=1TS{pWC}2~`|oyP`~ADqmw0NA#7(Gpp|fl%zxQ&fPP<aa8eBL~!dbly<Z'
    b'nXx+kN<s*2dtj;|aZEiQp)+zE>pT7tP6o_IAMiY@6L)M@+OU_eb`vtvlG7lMA3^4n(tF1H?nWpqi#>Ol)X6X)1dD`wmJ_M_TCn!4'
    b'_Xj6dMW{WlHeWofUG7N_;Fn^a9fZH+7(~Q$M^L`qA(3xo-f80Xe-'
    b'r7<|=s_?~63c0HuzU~A_@U0$2RR$bH7MYZ`1bMhYX@pm6gHc_}8c*Ekda^0>FFc0vzwaJ8HaEP}Pq-'
    b'S$ha<(B2s1Eh~%?7g8)^X{?nCVo3={QSAKeXdeJ`Vwb5u#Q0ULpX%!)^3ics=nKHN8;RTSbr4w#PgB(P9ZgoR^w(r;APdlFdgw&d'
    b'73@%w=e{hUGit2j<^vg~M*%5V}1}ew+f`$2+&RSIaX%5a-'
    b'5*H@!{_o?d!_U!1S&m~b;4UlmdB(}R(?yj;ih^K1{&<;i9^p3B?3z2L_=c`yjg{F`4q_c2{cw2s+U(c9sc@p>AX%xkHfAU92yM7%'
    b'okb>8@8u^0d5A;^7rbH8_tCNJ;wdI&(*RFKVI+3T?2lZ3+b4h9YAHcSiawNV49|J|ZSG_5m3?wonz!~|lI_~2!}@jtUAhu5dsyJ8'
    b'V-'
    b'%Vx!$xMJPhcLR$9u^j6G*E355UO`dV1MuxQ9_6|)@DnQ$r#c1V!j*4}WNvR<`0jy5@tLz_5$0h35Px>WIjA0%o>?QO%~*dp##=`l'
    b'-_lsiR(#&C*CP&xBa9u*!rROfy|u!zz9raa3@-)%pn}I-'
    b'u&o1lCc=ZCF%kCFiFTW0ZZCwwk#OzfE#2N{vAy@&b3E(;2z2NqzJRNFaSFPEZ~dz=F|QRJR#+vT1u1kao%EXQ|6Hx=UBtXtCX(A)'
    b'llA`I-otTp()TgZNo@;s&F{S%-VV=G^!FxclQ*CcaS4?ctq6ICIKpIHJ-FOAL~JJOQbEJvyxM8<{NahJ{f@&i&2~V0Es2+C{ii}6'
    b'FMZ?=9uR$1s}8M6*54ruiWeSq59W5e9qMjZ>`r!|SO?~iV5f|fg&KCwZ7YBI8)xp_XctqN2(SjeKp6J&W-'
    b't3#y?x*v<b796J0#V05HdYQ|Ls&Wr{g$CThH~lONABQTe&Y7{{~3AbK!X|c6~>0vO-'
    b'6&y&>LTW<N=&z4!5s!x2KPRaz$Xcp#4gf;@klnM7w;LGC5sJRN$AIIzD`75gBnXMbS=6$L2rlDX~0b*VX}qIvup%<DO2{EDdHv!+'
    b'uFAR!+WV6RccR)y`iH^A!zJ+H{o0{XJw!Y;Gl=5~{JIPJ}v;|Ykn?`b>;0<5OjE;V$%hd}3sL%xF;-'
    b'y1Ew{MDg)7L5f{R^6F0j>ay3!8Z@12(kSckSNcGtd#QlCSo24ljKY$cOHj8yxvE^vQaeM>uYWNM<4T#8lT=?Ca1YR?<knthGf83q'
    b'Vm{30Moc}=S|?BmgizT&eiqi>^HIU<wT*Lh;O)!<q43MfsS`98|Z2!U9jw;SvX<G>y5i+2no-@dxiXW-'
    b'<_?l_yc4)dHJ9@2~6e!YcOP%LsFPM?Fc7eaiMz2Uvye<9^dpYc!OoS&wHPP1AHCkKh2r!{}jbR1VWzgoyprSzSz7?)Ji(1b9}+q('
    b'{GIZ?Qd4RJ&+>lWcG6RRZ*?U9Fs3WWB}qJ7Is_*^b|<@H_ZD~s{wX#vRrw*?93vR9L9TvrOmy-'
    b'R0__D2YhRWOqdl#;jOQZ!ekLY0TE$ur)|vWw0BtWTcTp)-'
    b'nQDt(U%tYu%krCPVD4k=64}SwTKmp=Sa5h`61Z;jQ4t!W97B2mDh7w%X-'
    b'74pcK<8R0n)J0`*JS@f04c^QFu7=jx5U&2c#kk8+6nx!;+5Fk0fDDGQ{&^OkFKg!tb@F5VeXEqaCfU0yT8f~@Avw$9hs4k%QZVC;'
    b'B*KhfER^SxUAd__gsUc!cUDKpu4nwy($@nF7_S0;n0`)zfy3kK6-3GFXM#W_gwJCJ-'
    b'J6v$ueIpksl+*U2~a2mSvo4g~``I(?JAMflA;l{hJWBxl>x)<skpEZJbQ<*1|@Tuz5)E#Uagl0p2syX;5Q}Vv~s)#-'
    b'INq$8|=eCHkF8^B4L(W58L?xi_a^Sl~z*aXpa$3b%9?PI*s-'
    b'}Xz3FX~J!)1m~E?d2r+C$Ay`#T)ddx>1!<2*!IK7nn6dzU9t*Qa3KNspSvgR1s=FI&L>b64v9X1XwCRepj^5kCmcTDB*2_sx%eJ~'
    b'dnu8+;IBkXFpYZhrP<crJvDwrZt&dSUs*A=HC_PkG*3aQ`4(2702MD@k?eIYf2TEZ%_h*n?09+TY5xHO+-'
    b'1R^7dTiTxGMy!nb~`LI_C<e++TlH;t$3#hFr#+0|Z8K8A)ARHZ7ej+UR{)WJ}<=w{!imK%%XQ??`d3d*#)6F*=k6jdel0qFjM`iy'
    b'%t({r2<v4Og^{W+V3;L2_AO<dn0Kpw;zd8r0#H|IC%+%dgnfdZw5{Ph*!QJmbGQHvfv{grsV&5Z@UV-'
    b'&*ZEmI;1%r>uxs0XYyy<wjWU14P%>oY5QMhvNSLBvb-HvVg9uajv59Oy!v9hbe9c>Zvb}IN5&-'
    b'm@?3&ay|_#8nCMj!p`o2*o~IG+R^mT|kic0nGx6QrD6B09;<q0dmlDIackS?KplPV(^Scmz6pD9;MExm>ad7CfBwN!AR>?U!pc+G'
    b'3oZ?~-9_kM^h=`3B|RAgXV_?G2Dcp_`ExM5yf-tOKO-IIA7D=EvW3_c?W}GiTWC+`_ft@N(3E7<^ktjPExM8Tpm{AMxE%WDykg{E'
    b'7?GN+si}%9?6?JdUC8M+j(3VcD+jO($V23yq5auP4OZ7(D(K5yqA}BF)0HvYN^BQUEFO0Ll5PF1}eyMsgSY(uyP`Cg-kQ?};~6uM'
    b'YLYAmL5|lDE1hTwVWdKptFZR?_$Mbvnz>Ne&7eXk*cikI?5NF=+wz4W+zP2mT`f{*?qrBTsU{$?=~MRuc~U=H-uamQ#CwU-'
    b'%7zRAkG?&kvX+S3op>eR4ES|0}0FIZd$TJE(9!zIQiR$J>v+t3^=9EkbR&y_1FS8y;y16~L)#8XU%M%2Ejd+P^QSqn5Ih<3XT91h'
    b'2Fx;KEOOmT=gX#6xy_zo?+zYyY&g;(}j&tG+c3kSzBg&MxcYpoFT=d#niJ`UWS^`GKH%*eb_g<`|-DUv?n)3-4-W5~hBp$oR-'
    b'EZX~i#@K;q5R4Kv(?fxux5{x5<8kUL4R!UcVCJgs5{|1UZ6+LtaiSP$5@yeE-dGbbN!N8T&t6u6U*QEW5$j{ykkK;YAMy2&GMHm`'
    b'nxW0XB<U#`FJh?y(C`>x`LB;Hm6%EBNAW&17^i-'
    b'2L8WvxiC{Su*Z@}|JMz?QFz7^Q2UR$L^x7wsv<P9jrNgONx?jx>S5nn}*n_~m}C4v(lw$O*eB)Wn<ByJ78xegkvU%I_>qXSRxlsf'
    b'dS5tNbI?>{D0>*W-Z5u>?6sRig+-'
    b'}^}V{i^TchXlsE6m_H<c$zMb+gOiI`$>gVPH0x#tr6;eNJ<V6y9m%wO##fabQwIhz)7;@G}89VAPl4&E1(#N7IZ;d64^Jb>>h}Vs'
    b'u%Q`<D-C`#y6)7^ged~1}EFXL9#Q-'
    b')rdTFQ6DGY`I4p{q<OkXV&Al_8uWWSMewHV>+(O6vi`$ilUoCV?<IJ1hILm|0R~EJCH&jlZ1(^|q=Wr*Gg=n;+ECJ^sp(TxEE-'
    b';L2cAgWcbAE}Q}g)Ei0s_?6_jN<0{I+@z24_|!WV{~sj#@L{wfHV2(<dA9NCorUXt27n)L4hLOroqNmh$I!K1F4xCM%N8`{z}l=*'
    b'7fVJh!PP*sJY{E@j@`ak|X#SUkHiClmwODXr}-1-N9*5gfEXKjecI3+@Bo66-'
    b'LMHP5c|CxqPC;AMx_Sb+gWY|*Es_}6FfmceLR+ohwl?8>|0zKnEJY%Tr@yk<Rlm$ZbU0mR^s=OcSaDKjK@vv)%ZVzhIT}U>>U0#V'
    b'EH9v>Bp^-'
    b'KRRs;2^P&6bK>UrzbFu1ZwFM09!yDi<6A|lA~ubqB8XzMdAfNA;OMs#@kQqc_<2)HH;wIn488Se0@^y*GtzBEqw2tY^Q?^f=g_h&'
    b';<oq|WV=ISkQN>%Tesa;#rUb+dKKb?PXl@Wu>%}4M^dRS}?4;V7(%Ij43isoByB{$lq>?$DrzMux7<yD+Ya>nK8v=!cxBl`S7#a-'
    b'Mq$VJt_F7M{X-HvU=?T!fZ2EZs&M6__bd!2#u$JnOxNFu2z?rt-bqkcI%J+zgoDt(N-'
    b'efISLDa&qyY83tcR`50S(m$6VM}j3tUas8tAey=FOGOfE`mWD^iYzP(EXL*AeoZ-'
    b'=3p(w>LDg)yt9nb<)RjkT4)7OX@pkqM0HnhRzlmFNU(u}+3Gmsws~l4|M)GCwwUk6S`E=8sYB$@IEc%UT$L*9rRF{^Yqa4L^7Um*'
    b'<bSh~yFF==l3H3hRGy!oD4o!Gd@xR9Zw#>lW7$$wqzx!`{bi1k)bulh$7@>1*^jmwhJ+m0_P5mZJ{F;03b&vt#fDr-'
    b'}=25s3D_H$h9{zHFZm6)AYv-p%J%p0Rn%U4fm4$#fLK-yxRd?eDlK{BH%lq0Bmn%JlHeQ~4;a}cjldd53USrmh!amTFhXX^$PkgT'
    b'Hsy0+~BoqL|nw^wOC0!K&`WJXR>KA>YVmDa1m+f+Z#eJ<a9HMCv55z$8aLj=VPjrX6#_qgF<&J46<UW|9OwnQ-aadnIO)$=s{Nps'
    b'f!$Jwl1U2A{TCJFJ{OJ29kb+u*A%M^nUAo=cyWo|x%ew8i`TnW`LU=nkaw&)4i0inYq$y!sL+$eJY&%~cGUdOpK71hLJ%)M%ix0%'
    b'HvS6-'
    b'dwSyj{KL>~i6;N77e0Utmh4ha*?plpPHD??n==Y?av)Vt>uI?HFuSZF&SC_gvv?{BQGf8UxclBqh<(hD&$ei`APWZj+ak5|vwA>F'
    b'%_Q=|<Q~AWyba5K&zH@M><#GzPo>AP#7X$kukE98#dIs@8bJRru*U~CLz?&jUUMcQ8K{%MGhm!n9C@b)@CwyDUOc036`Nchjp~n('
    b'8g^a0%HtAc(CL=#&P?((gTgq|6g1qgWoOkaTPOpX<K{?3cCSYTJ082u2P<Umo?GyyNst?IC9(NjNY7F$rBCRXSYr3iR+53gDY4X9'
    b'rRi}-'
    b'cWY2T#_D<5Hg}?B(hUNS&h&bQ8CCmOR!&G=wL?GU}WBeLO@@II#v+`75#}BydVDIDWF}}<bR8})6J?b!)t3K+{LLAex#rLy@#Tyv'
    b'CoT;LRxZAED9RKI*;eN6c1%Gs-CQ;(rBY>aM%!x?X;Zhp5I(8FWIeDt9^znJmjET&}KF_tSvv&f`Be~^!tB>mZjf)Wjb|;60pMf<'
    b'Tim1<4V?AcGBW$?}_vgRmptW7PE4q*{ReS9Yoq)$R&P$phXD5H=rF!9sH=mPL<O?8<{YF<Z6###g_ux6{)++tl?s{b5cPh15-'
    b'X|(*-jBI8_v6oOS-vFQ&F<5qkT}0b`8(y44bwq?x|i_or5ymo6?Z=UcftN3QIgam{KlDVE)fqz)rBF8UAF|2zz{%RJaRpl%^m(g7'
    b'&M9RRIjx+7<%AoQzr4&Lnf#i(rwlg9<n>6#CG+1HBG1is2vo$JtGJ4vxjRoff#e}61QDh&BVp$yK7Vj{&d7;D0eLy>FN~gFRWS8-'
    b'$$&h&TubQrNoES+%;1Twz{}BPB|&DPYhE=B77F6E-'
    b'_(#Ud4QWCVrzj0jFZU7C;bJu6d}Y0PgW!!+N7d9Ivk2N4qBuIMJ75blMe!P{Ndh+O9_2iNEueM{2=ZC()j3blW8V?9te1&=cc%qf'
    b'N<n+-XWzucE6GXO|kjtm9hSqfVY)BA6xSri0XSD($w_2Z8V)99!UKO-'
    b'u&h?r+Q1h=F5kdb9{aY9GFpH`Fip&iSiEF=Lx4J1N=@zIj$ry!#PFn&z_!lJo|PsM9P*w#)Y}_}f_>Ku&I#+qNpm{6lHFyJ--'
    b'c?WTvAPExx7`|(w+^cq}2D{l$<P#mvR>o1af%li)>A^W;d;j0Q>EuVAFoU`u^rzd@z2&%o_LdT2m|5OlbSBYDrl~Z<pEJ-WB@wnV'
    b'V7%_<1{j19vMEzg^24n|q>3VV@-'
    b';Iezu(c*}`V3&PR(1L%)U4+85NUh@O2fMs<@l{l?JSNj*b>mp2NeHs&6VRnT4W?r^5bw9^@S%m3403$V|4tR532CBMrv06qFVEuV'
    b'~!=HrJYWqCZSd+!lzE<m$%L&0H|$mHgd0ZID(9&QvJ+0aoJ<>+#bF&971$*H1YC6H9n^^s!kETdv7iR<|>heKwc6QeZegF*%o04^'
    b'}x2X_L*(q)?yt!`TQ@ZIICtmut4RRZ{n!KXt!yD^ShNnTn@M#AO43dDX$5fuCEw4lK)l|xI{&=d4>tdU4o0;L8+X|bBcgAsLC^cO'
    b'Q>1voIwO|5634wsvjUKk4h{hVY`%HwVfgtfd-'
    b'|rRk_Zp8}0G+AUBh$AT|90Md&@6pH%$|E%;cq=I36nKyXxwoz<ykn^i}33V%HqE^q`p42zWyp>20BB=Y=yJTk{7lpuCAXb%N#FYp'
    b'l)Pvh_@g1$2^x^imv1a0_q*(O@l>`oy^j0fQqo3>ouGn=xX>#vs{T&HymlYqT-1>(V)R%cwfwrNwe0)C-'
    b'VuWHc2l8YT>yD9uj&gXMl$AizFh!xz;N6qG(l+gyvI)@9VejLehu#G>v3y(<|na7Q3S0he^cFAuXz6^4xrGo1B^5L&{`>70D$M;f'
    b'Z&1bK2uI(cQZ{4Ur*zY6CMP29is0Q&=buuNz<wmYuli!=Feb(X2cDxO*ngf-'
    b'H)K8a{PrJDN{4g>`uz&hk61pvML?!=tPg@+)G6D2<>Z4(OmE_#df^IJN)`@YkQmv-'
    b'^I7C}jN4|sRM32cvGNclHc60Q3oTaFDjz6y)-JhTb(b|xu$Je2tuF?r?{C#beYW$!HWp``bYTR9%kR}-1XP*J!y=M|$1-'
    b'2dK%c^$R?0bnX4u~`;Ex`J5kHGE=c+ky%C#l|gd_9EmyN+OU0!pXd^R>HFU`0aN&;XTd53htUD0BwF(gFlPJ&x@9zf=?b-'
    b'masQQo|&YENfmaG40xZ1xj~iwIQ%76#+<9q_xiv5KSta`~@bS*!Z~a-^q-CldPJ23EZ8cb|P3%uy;FZ_9-'
    b'x+A{xng?5fn+$ljY@S+QmE7kJJM4DbT6<5r6NO@Q&s)Wa*YK0U1%*klPXv{NGM*@1WhLbr+XxfXOOfAj24kUJ_%BnoV?dZ)|C<j>'
    b'n`Qbe$y(Ks8lQ<~Ab?t)(*>YV72qA8(dRZ|cE8ZX`9#m81Mm;nyw@Y64d=ALz$wKg78xZ(`jC^@d5Kh0|isd>-'
    b'*XU|w@&I1EFLtXQ@eFEu;P+S@7K~=T=K~&iQeMZNKb(XCvaRh5S-DzZZ0=B_(IPQC%Mt$p@ko8YO-PLV#xkHs<hvAw=iZK}1Y)@$'
    b'^N^&cEGW(pH%6HUp<5ODPq<KxtMxaS<Su;E(wV64DHEyFD#e6w;TZE_|(3ac{nQ1SEX%zOnt`%|VKh8-eWAdD;-d6!^-'
    b'QYre+GgNe?!}zy^%hnnWK|fOtuTl!tXy#hlIGJiRh@j9drg7z)Nm)-'
    b'B5_cu{`~Hy3ut`tpd3Fz782H!In(~3sakj`QKS@<C0@(@8lZPGEu3ha#i#lXi;G2FL!0?Z3g|HMDg~dvhhwe7xtf_|0{65CDDNiB'
    b'={R;<Qsrs`s6o15H~2H3nRItunvQ(#)ix(Hfl-'
    b';9yhH@wBVzC2?fq<XO`vY*w|A!GEzO}r!?@HP6e;mjzZZVCl%NDEa=oOjkPle;aWjvEbOk&f2eh<4C8h*nFQ;1G&rP|z%!Ze9Dc$'
    b'x(0#a7V-'
    b'5TlPnwRB+@cqB2_i_lWxYH6Jb3@pz#@B+eYg2GL<*GT(Zx|*0G+sU{V3)FUz}ZIFNUOWZ;b3tlPK~TxlkEs`$fx6*^BX*8xcO0j9'
    b'R#My^9?r9zh<4pg<mrE`%L`<!53wl3`@t#tGa0B8#{1Qe!i?L*wN)I$+k)Yti89~eZ0w?9?!1AE0GN7zzsk7OR@5V?K!V@+_0>Wq'
    b'^vMi6a?NbDK>sLNb729L%oW%)#YAvR=Qp>sc&dFqaE&%h%RsX_Uf)<A{QK4?Ybve7D{#=ngg3lj&D(to7%jfz>tr_@SMs%zn8zoi'
    b'B<>SIm1ik8NwXNMgVDThx}$vcB=0qR)nP{+u{hG8ii#xjfB7L-'
    b'vB1r_F%DTTA<AZfaWbyF2$~NKIaZTc2O?a|6wq5@wH}i5hRi%iwuPf4X%8Y6;PIGIUFl}{IvWm9<=v%y=JxZX$mnyseRQEEsAKsQ'
    b'&s4D_4wt|bZuLP6I}#S7le}4*V^E1FCXCNd16<Z3#Ea_`uH0^K$D^+Z*`^tOkcZ0Gkw=Ww2*j{y&aIod#0W9wZ#4e?l*o)b#+^!9'
    b'3ZQfyxeYR*?s|;cdl!L2U`2B)yQ$D)N%3n?EToKxGtq_AK+vsk6itJyIopfTIDN|KEhC3N+ULMeTIi0%DM-'
    b'9Vg!n51Y1Mi1Fl1ZT>Z0kI4=6;M0b9J2Ac$hG@yLo$fMB<ymOIhn%tuP9UwP?7AGE(r{;nB5lN+#E*jK8er)-'
    b'rd#dUfekup9it<eP@q-%)qJJ&1@TYYxTW*2cw;?t-Sq-UFJJhVXh1brg%A-8$?P%$&+YWCk=aKar;<=_LX=)h)-'
    b'_9JZ@hz9H^LYJuzu9YbpIv<-nGq*mT^-5e&$qqb=a!t53%RREjJN(B-9vXN?>d};P-A80Q3QQe7(4ujd-'
    b'd*RVN%wulr?~|v@BHrIystWr?oTJ_b}gosbb>1T(+{MaP?&hGBgpc$ts`7#5o@ac)wL@bSiy2$Jlpxm32C^0{Ug{U2=u+te|}y5r'
    b'V=l1(4t#dv8#}Ipp`;YV9WZj8>0MpFtR?zh-pwMdHT!Xu>_PAE-dl(k;X;u)L($#i1%vos**B2oGx`MlL9>hc9;w483uxg=%wthC'
    b'2as^L>f-'
    b'VP!mFkgwi&WcPX6qs3V*x4|m6g)|iZ*#9Wu1!pEssPoGuxQS*$ByRVBBn=1Z<k^3(CgD7AR}J(@A5tQLT1?#;MEz`w^=~^nw-'
    b'b^}rSP)HJev>c3<fL8D!{V0@4#*#DJF<W6GLdd&E0CNt^}70o1O>J`O?_$JBA!C+*W-'
    b'U^)HMH17?02msPo^sR2Fd#EElYJV>AyYuDE%Nb-xLe{;k7fby{acfn86Rwh+ioLC?{fE7;lTKs6>ekn#VKfY6kkaqf0p*fSu(@cA'
    b'ja4F5sN4WO!aYwHKtJc)ox9v%1&ire6QP1krAW-'
    b'L9fxOMpwHyi3@ypf2u=tSNw@d78<Gfy04{VS_+V;xC$qeR6t&c+1G>5dfeU0H~Wp8W--prjZEs^0v8Ylzh_llz%<LAdX@#fMqxl)'
    b'lg$Ok-*-'
    b'>We(k&(m_>b5zAOndpXkKs%Lou1)N^<S{xO6Da47^80QMTZX<J#h2YaXzVC1e3RpTonWlBpqO`zy75Atna}NiT{we_PCCa_t)=`X'
    b'AUjUyxaz7-6EA5=K)^8oU1^N04~6fQ|Q%92gdP4_YhU9+>TXWQe?Wg4gk1U;nqQ(Md}>w(xb<sQ3gaF$<~&G%2BG-UdjL{ISlRML'
    b'~mo&s<|~Rg5&EvET_hicks4bALsb}OC|a3f4(gUf(;h(65n7D{T^4*$m_+5Ie=&KN8Jbc@)jD4w>_J)m2++BZFPG;g_mLmRzW&B2'
    b'1;oUM-ek;|Ig?^-'
    b'X7#&nK}M2?$e(FE$~COdnEYRk@~e)ccy;umC)0tDq79HOkI9HRXOa^O$hMOF<BOZ!M;Un+72<$Sukp4Wq6s*c%&9xa?;Lfr1Li!S'
    b'm{JO*Yj_J;Um~<_Z3V<$1D^NjlgbL7m=tGT|%z6H(iN=t8JF)@Bk1kAI{JTYPQX5bF-'
    b'&99rzicI5BT^Vny>HfShf6{+QdyaI4@v@uiW>-*}@32N&m$LdYEndLUL+PMs#*bB)}#VmtG(ue`-OmHHw2IlplPtDS$ETC<W3r-'
    b'nV>ecLE~ot==%Wc@Hyuv9t59WrHpv!Zn6^nACDKEc1jT;|QG3R*CODK%l%HBI5hr2Gk>I(gsbI~1?}BpU~9fx{*sVAyXjBz_Rmv$'
    b'ymwVumBbkg@e?Th`Q$2qch8a_E>l=k@Q8Aqq!FNsCn=C`aClx4a=G;dR*r1@pr{eG0oPb8|Qcc&Ts)Ri0<yN-sXpUQoGIQ1*R-'
    b'+)Hg=aReASUxmlSi7v`ZILVz1B^=V@JO6CuvsY*L=XFtpliZfWTcZyPshdf~Q56PMMSse}Z*9+cA>XOrKywsOp3j!t%}vjtXp)f@'
    b'R8Zx%Kwgjg^aRLjyQCEe0mT1z!<*A3Wc$A5AplIR>n8EWq|92dhd9(hysS=!n;`4FV|l>)&cdH!CPx5*2$cZlaQs1%@G7?piSV^5'
    b';=|eOwk?73ga%N|R>T`}^)rh5JQ6{!(c-TS3eBk`nzq}OJAH}U4awm{!UJ@ih!8aulGD7Oe^8ICg#I-*-'
    b'tR#F$0HstArr^ZZUNy7WT_PvNPO|Dusny4beueTTUJaYJ%Ch@1N5WG1uUlCLA5QgqFcGairaJ`B~Aq`FK9y?ry*$+cWEs+!00Ueq'
    b'o6VOc)CGbNLad+UXae0bEr6?A{8EuwucJO4PWYuJm55-'
    b'JXj>yJ0aye&U}vt3`3aOI#u^7s*O)YJBCq~=Qd6U+I$A{xf*|vcQEVVtO9c&&D)7=II;tv?StbGz{IZud3;D66wky9lrilJFnCPm'
    b'l%ji8NlG3Nmt2ttCxgf!i1u*+?nz#z93l}v9HFeFTfCBB`XLtANwl)u^`IAW!ON*GkHgP+UffciCJAsj<aQnH!{Ty#Cr+dyy8bk&'
    b')>#!S!6Pg@OzjHGa=MhCpX4=s9iUAoPK2||`tkV7vup0Ica+zPyeZewp4L=#QLEbK63@R%j0(90gpu8RJRRs7LeEyIt$GC8cfk_)'
    b'TCbMI8vT$Xz<|{aie`hv;s0DeE^9th@+n5Si9Nsv&U8f*5^q;qG-'
    b'4?Cse06$duf_(*7g3`DRjt<Q2+N!&9No4c;)4O)f=q5s#}wr2@Xl0!<t&W!gob2+^zwP(MiPR&SQVJG){U)xqDX1isW{?ihnE8Z$'
    b'wl)#>F4^3=~>{gLVx`Z1{#BFww3RDyMG|(R4W1BAx-'
    b'3>hM8Yl051K?#k`6?Mvrd`6xtyei{V*4x1cV*b1sRrN`wrH*=cueAUfi{p=kU;E6-'
    b'dUf030c5y#jndE>yq)eB3W%u+7a?^h+7RHkGupmBtHqUfbRa}D5y0Y(z|2!-'
    b'Bp3Zl>#*z5I{+AaMxXoz~+s=$5|Gk_;h{xT%4Rcx_ySA9s8OPw*JI^#e1zAQg^n){dwy3Mysxpucv86p$seiZ*TKb68`@HY~{O6j'
    b'0xa*2TKlrI;KCp)DMZkG)6BTf+X>DQ9=1p<Li-s3{-Us`s9HC><3UdIhv^Z)2ZSI-'
    b'd5w~?Amr}u^{J)YW3XAULaht+N(9t2*Qb9oP)MbcYgs8e-'
    b'O$3*p_eN}RIMW?h(o;~#<>5eejpqOU7~<j3lJRyP+?|wb%R>eIUs84j^YSfgX#a61OH##)r>02!_<qXv+lHrs_(?BX1BC?GRw{$5'
    b'H>3MRYOtCqKLZ$Vi7WzhR2u1@i<VZ*obOhC;VQ4LyQ*Vt6)Q1Bgns0x2Zk_Ek#@cyoNMZzblwyPuR{e?4!N|eew?QOk=P~%a1y!f'
    b'XxJ{|vgjQ5L9WY39(mvVFE{yh<#aqbX7^?^YDn;0Z9;DyW}PG7O+<b|8+II{<sa?b!}#iv>wgQ3R52Oi$F+s%@3=lGvde&D-'
    b'_J`sg*}!HE=nAsr2ceItDo9d;cs(Z@P0Toyk$}~q0UeXrg+E^-'
    b'S((cYEi+3Y@tBX1Kp~C;QT8}J$re6xDW)_2Re53y2=GKBK|lTbX(>ND%;k)r4p`E{@j*)20XQ^hIQzEP`jGb96k`pApL4yWl?jxb'
    b'OBEk@qgSWY7qh%48A8%g$_r*JyH%qhR5Es4ps$DJ}$R(v;7r#EXb%hzoMarDzw*c^nZCAe4(o0CmS{ie)DjWr=yfS)vVG`)s18dE'
    b'tdWI^}_qIHHb4B#~Ix_jf9d<zid@HZ_U;;R)8>0jYw0r;c78vj#jriKp-a{&l43b@3!T=G-'
    b'SN`cCiv?sM$oEFf|3>SJ2ey0Uv!A5fDIS8qB8yy#ln7P~{71@Dx{Qo~^ZMiB;A2WOJqQgE_bm-'
    b'e$2w>#peV$4`3GaOXVk)RtQjm|a}W?p*QC`%tr?Ikp8xB<{O0PNotr|B6zv1*evh+$%f$VN+%)zXJ5+jX4$0r?_WITPTvVqyx1m+'
    b'#h&U4#Kv(kQzk&0#fp`N0Vo6!_u8`4g9Ir+IV#;gtEVooaT7tuRrA)l3Q@fuW_sSbIv^gmmSd{oC;pEnhh>cf~bQ9NK#E$2Ie!F2'
    b'?&5QxTNw~4u+D66_c|w+T`84P;&>n4oZ$>Fu(B$>csaxeNC4+ZQukA4Fc#|_p*2DbUNK|)lK2k?1YyE=F%F&#cyXFxm3R$XgJBE)'
    b'w^=A^HZ^TqzIN$7Um_R$3K&YcD!{c<Qo<pK#DebXSqi^-'
    b'|iOo3;EHVGeJ2kOmJywttMLdGr2dfMidmc+PA1y3iw0qn3cR^x1N++1QxWSGGHNH!yDiR=`vBMFX^1KqSSrM8?OX84o8QU^v%m14'
    b'-b>@M^?_Rv_66i&AN-;-NsBJzf&3uFwlwipKvs_lcyjMZ3`DX@Aj(#mRh(2FSz%20h?e5NfA6gm`^s6z4D#AR$`F-'
    b'pK#3s$k!8*koEB_J_0!@ytU1wV8yS~$?Kka%oUYdb^W*%p3SE_&u`JhZ8@H*RFnIhjf_^lsm1F@1bl%Lq)0M{HTqyX$QG)U^c+91'
    b'3%M6c3@Gyn0OON#<0;#r=k!7%x=zFHEA4%Yp<ts~&n25PC0||3(>Ta-'
    b'+|3^WZzm0$lfImwYW<|$AaRa@kW1k3i)$*V9@9_7DeGqF1cPOHzLn}~I&p{@TqJxZ43m545|$EQ@(*qk>^+=n(nAE<YF!n0xzdhl'
    b'et0uRkIJxU=E7@ssa08cQO>KZ*bS;Z%@g}x3u-x)K!lDfMG8Tk_jHR{?ICfjT|*5{-'
    b'8F;~Y0vO!cy~tQn(Is{HO1wY#*W&OOpuZbPf=#*$P70h?n#!mCVsmc{-xIQPqLLW6C3gRYJj~^-0bM;lieT-mv`(hJe=p(4#vebk'
    b'*_b6rS@9s$>G`+4dU;m3SHI5;;no`hhxOZVEQ*dPMtPwe5!+|-'
    b'TL}#4f#~BN%@a6zv^NJXcOQ8*5I(9GYH#%NK5HZbz0)`79Y4$SHn90QAX23r$O_BoAT8ysN(Ev<UUM&H=hAr05Ar!tN-j-c_olQw'
    b'3Ux6>2NzM*gySjS9Zk*W>qn)XvFYXx3Hy5_+ILlc7oBpZ<V?^M;nOG){T^UFg)7i-'
    b'9RF;tly7l;JlwQS85+Z)k%YdudEM%7NftyOR;yO;<YZDd#c%a8MkYAe_z-pC4+aC9+9l-@T3N4jX{TdbdoR8g-'
    b'mNTSdRrlLCSkvpQEgBC8YCGN*4a2XqAhE%fS%k(k<p5^MKS8)!?~mU%?xy>N+pz)MFpT(OH+h)oRn7Pen9ha=6!0aq8D)Rc>Y|SY'
    b'IWGo94w;_3l$@>02&DE2-k>%r%K-S-bLY?LP8(Q+$}p(}^<(K^3dyY$=ef(7L{aoDX7>iy-'
    b'=#kPcLp{tT^Z!5s?>1#kd*#n)7uKCIyStSm2|>eE!RY5LGpuxm0Dv`iqLqDs&a0(A<XOHZUOgJYqJYSx}{$)_|0A*~H4ULD%GIKM'
    b'uieq`m>#p*MeDgNljX7X*<s)-}C-'
    b'mQpo%XqTu;)R#B6)Vj6ad#M2wOn~R&|H<ioSu<VCBi9q#@<PWA<HfG;tYyRXZ~QxvnVoQKQ|F?I9<oPf<S+3*vESwb8Fct!s7DSY'
    b'dTS9H7PJPU#0XvK$2rqMAzP)_qSUHvLe52FS!Egu%7l3X#;<y-'
    b'VC;(Nrp*52)otaWgYngHLJpZh!9|oGpgj?O?FB<)9^6#Anu=9i#8v4Bo|2Mc2XAxqBMjmU;QlTlAsMC*4`hJ<Pw8$BaM_@a`u`4o'
    b'^8cb%FN;fZk)4>JpOQGkOA97>qlRvr1{Z&h}Syv?6a!U;oBch)Dtp@Le}o272k=2Gf%qXtSlfduss0zIl1MJ+441j>7d-jy9s-'
    b'gfPA+s=2!UnXHQnsp_4TmiI#W(R3`gEBXi*&l_mX@ySQAP2_%%M@U=bE=6E63{8AV<t)J3#<*4Zy^w?SRl5$%0GUIpOF0MW*mS2v'
    b'$&f?_fHd1q}ugo)y2DN@jmXX|RhqL;vhl5Ok-|nCgnHhvqhq#-'
    b'6r;l&3HNxMir})voA<L3`inWa8baK})_JW;rDb=h~M{gw6xRs>UH277)#2un~HkP`^aDeC6CGk2&98j~SUwg6x<_cbnS`e5u-'
    b'(i9PepjB>-i7*y<cFjE?+#168(pp4nVy7GMH5_v-;POHQ|`Ezbf?31T?@2%TpL^Fjn-(jFvh4cx(~TPtA-zuV_m{FNe$b{C5Q>k8'
    b'!iFer|Y4@-'
    b'UWvOR9hv~!EDQDR~_~UgXAq;ZrlrW)}`#$!CEC)@p^um3)cL)I@8Y4wVPDCtk+7*fknK(H)?gGWc~9wtyLY1wiX^GKYvd#XF&7!e'
    b'8ruvUG$J!UV5(C^u2jd<cPHALcrw;$`MV~t#xJMOm!@^v@CD0N%YdyH7i%<CQWvE(U8DlktZn32lj#UeFW0idixPPdcnm?e{tUVg'
    b'L=2><LO{BfL7;&t&3GO1h825*{~TJ`ze-kmcpFA(gl%Nep@HB{bUNc{Z!hF+|JQ=_48lF2qkVX0dD40TK4Gs!B{W%!p8VCT;U<PN'
    b'2!s^Fzi0JiYrUizo&S!mg;9fdbl3n_wOkNXo4k@P#zW%RY6u1#j#9xhqq0lEwv8d7*47O&a`5|NkhrMKjzJXSm2;K|3V~Q7}=LV%'
    b'XLtU&Pnr29{+vX#r5zJpI`t)+7(aTZ)uY5T>H(Pvvb1_CE%xQq)T7z+^=_Xn5)9xE(UNY`llr~cq{&F^Q<@Xr(1KJYlbZe>PiwM1'
    b'kxIB<rr3hu@EN9)ZP#bG&PQ&;f*I2cLzyy_~GL!8=zr_2Fgxz_?JEaPjKpR3@<y)OJZ$`R=QySyHngdQo1U_&DnGA1IO6|pR9RDq'
    b'hS6324vhy+;Z;6k*Qs)Ihs<Ma)s+!+AEL&Y~c$n$c<dVp~PCN>NZ`DWkMQ2Flr!8^%hz`r&uC*^CS4OoHJ5dxKq}XTyyB$wjv_Q='
    b'~I`92y6jekr$o)40u2DfCR0PPr2Xuxxq^QhQkfQxQ<x*b}Q$4yDlt;nR2`d^Ld<-'
    b'{)gFY(z%c*uPIzgkA^PU87%7s5#p#+YLc+?bsVEr;Z>PNVfwk6`Y|Y?s**((v|Z%Q(rkG+S9fV3lX#?=|IN4Vw@S#$>qS>Tf8L{4'
    b'npV`cQrDcR&u_pHh*?fl5+s@{Cfdf_QAc#m4#!8zS*p>UDf#^Dg>X*P|5sUw@tk*MF76xXm4i}l_n!XeZF4rJVtQ^B-'
    b'N$=0@gx8k`UdJveJitC$U{0v@Sl&qz(JSq#C;B~)Phf%66f97`m^}NIp-'
    b')q`wiMlpR4t$z&JJZP*Wu+tjfo$E;C!b$?)=*!{GSysZl8Hto;=@j_Xi4LHW@^A%bLh_pl+I^+M33>T+`#el{J}X|BK@n@&+ooLp'
    b'$-;0zOdly05Wt6r@sea@&4+Xh$AjnLsR?p<-<^$Znd*SEMn#c_DzY$U7~$7q0CWKiPr^1^Kq@K=6Wxv-'
    b'zQKa1;f4CBphzLHxNQng)kyQ{*~N%NQDW(a)rw($V9P>IY6mI4>=SDxb^t^#n*j*Bfz-TEc#-'
    b'Zfks?beonQ6dhaK9^GM0A2I6*ce2Z-z2!gCYvlzn~#HB&&`OF6Sg!KAz;SopfU+O0%)U~DTBkDG_pA>_%rVb-'
    b'4bEvA}_*r6g@yOisH)I2!3z4XFpMiD%CpyJOR%0Gvv^D^0A!m#6)#uA#orbWOD3`|AUbe+yDia2b>pF9n`fvyzZmztgOSkh1+=x3'
    b'T5(rips3ElWgf*?^fn2YigjZ_XRR>GT>59?kq0@uJ|hz=yrQdF}sHd{09B0mosu-xNP9*6{p><%d@X#`b@w+0}!w~chZ6rG|ABye'
    b'Oq1B&<QHrPu8w;xD(SHzR?}_QwoC1M^^c#SxK|Pa@o4N3HEANINqcvEV*R=Lgbo=Y8^XrgU2<pz*RZIe9F(e39mSv(%0K{s&nEm-'
    b'n6#akYRG2(^Mogu2kLwQ+(?s6Fyy5J%i<l-'
    b'fUtahwV+n(J7TeUN6r0ARlgyagbMDX=*PQ6`(#vDen5Xzwg#BDscF?%JX)fj=NQtj-hGU?wZvx2#4%-=F<O1X}0-mbGbjI-zA?Ph'
    b';l(U*W7DK&bU}~EAC@;yPECWW(t$^?Np=w^yh}Rv}ISmqNfJriG&1j3QE~z*}U?N_GM>yiYs#4QI%Lqq;E%Fa`m$1BeYEBFH2M7C'
    b'Kb+$Kj`I6eUC+}8`5*xIpBg;eN`Ryd7gG^TU9?A;wNym-gY-XO%cgoS~aRXc-caFH<B}z83n=(=@PM?4FYn872-'
    b'!HxYh~aOPYQYT&{hm9afFkvWYRC+Go>#w3g-'
    b'+^x8d`|NYPZ`j7p8e@1(iqXic_IKU}N?hpKdqYmK&Rc{D)Qfy1%Iw^BbFW{%$!Q+y2D<5&YRibC-'
    b'09htCDXtrg;^=~6^j%HatB<59c(Vx2<I~<@9A4itq{o>!FsX{r#N%pF$a3a%A_xxUYRu!{dE#nCUHO{r>aGLp+18k@W2t4E97O+m'
    b'DS)_3gWD%;4QA5)jN})^@SB??+*?q!+c(b{2?rpFUepMjF*_}GS=sMy18F=A&gUPxt5Ez3Axj4|N1I>gRKhXo8u3<1@+PD};yI1!'
    b'>N<32+ofXgs~aiFF@Q|Sfuy|b!wtN{aNhiF#8ZL@+Qo;q6hO%PuCSu^r7pL;`fRG6K`wqkOt-yBzU}?|X5<`%PIdsnAkOSM+-'
    b'`hPCnLcmzcAJ=P!%n$z*9@I32svr{yvwhX`r2WW?TZ$;UG`c!R>Z8_^OuPwpPz&CqNZps7=tIEUCHLj_Yi6RXae5wokX)?^DK2{B'
    b'`92OX?tM;Cm4V%d4)LV~v|2J+t)FMR6k}Jpc!u?{&LRWG}7)qV5fT!fumiXXS~4uU5iK6LuI>`R17}0;jE6Ag+8@PLKwI4i`K9T<'
    b'm*vbG^o7Y6`>h@1_7t17i^2jxvA<`ralYQBS1dpq0aJ&Ev)e+Ri-jg`ROl)x|W?ENzPc;_LJ+_*=Hg2FLBzsq+HnK44Fq4;J|D-'
    b'L+`j2|!CS7Z&0g*HxU1J;yJpOn&iH0B4`}Z5F_thSysRng@z~0I8tgM^QO4gZsSJiC-ITr~78%#^<o*m7uQH&Vwj;XwPR#o)%%66'
    b'Vb0$nu?ZzrN|KCon!r^M%%5=GfB5v!yGTnp2#ch<h+oYoy4>9{@8hVT(IAs7V-NvIBz$p+%3`RuR2{tK6Vb$wxmM_&-'
    b'2Ys!AepxF@7p@cGaoiE_dT-'
    b'{$^Lt+%V>Sf<c^A7{ldQ_tzdNlzWcbeq~i_sF3ueRC%61=dtcogneVBwcrs^h!6C0>I$r_WIce|m1w@ZY^q;6rzWL7pK#EdeM(g)'
    b'G&{caUcA1ndCC(9IN&3V?dspFuZat1a7Myxh{Pb^?^)cej)TBYBcaPuVR(e>m$p`c^9Z<7Ciu2N-'
    b'd(}dH(D_@(kx)_IP%U0ix+)5KLnVZDr%E6Ny4k^3MpFRI5}t#c_Lc=eVro^lH-(TwD-FmiE0jc1U;*wx@hm<{;Hbm084bxukGOVj'
    b'BPg@HkKjh{s=kz{85!bo~gqR!MkuY_FNm_aI3FFDy|(n4Xgl2`z?U#@3+TiP1!YJLRYhR{kRBE1XE<H7RP*F1(3BbeWy{$&Y4#8u'
    b'k$9SsICah;^f>K0yVSC_Fz^K_102i=&7MYKvjtWfMHO-yx>j{wBKm&w)FM4x*rD%=7vdpH3X^)JWzcQub#DpYyAm%Ko3!b2NREwv'
    b'BshtzDD2$YU*{XMHClQ=c`vy30p*}PFdmBp3vqcOjb*kajN0Nd1kv)q-'
    b'uM8X}Asm2_hzws!N4UF4<AnO6nn;H7mwn?EM2SA7N48Jt?ibYp`74DOR~lvzB0CLb=hUELv3s)0wizX?pJN9S14?NHUJc+6v$pFn'
    b'B>`^qfrqG^^lt_|!DzADRM7)>vJoP*gz!*|<)J$u(X<$E`6_5ie-KtB)Z+60%R0;-0?k6&}q?<GgKg1v3f9S9-'
    b'5v63M!fwM1nF^`T-'
    b'U7!BtmF^50X97)hptbcxEjg|FN=<lg&$`CHkhjs<3gSws6tQ0n0pVdX3YP*i<;)$?@4j@HJeSN=q<u$rKqmMY*J|Gc7#OOYxd&CX'
    b'Kctg?j&iMdS@B3{^r1(HmROh&B1?%dcGvs#is$(Hp|8kRE(w<1`99>FZ0Tprlb+!A}0`WTaAW;6d1I60ICZDB8M@;~u5Gl=gZj}q'
    b'Zt-JY5z#YG|HooH}{(8v3jG!g2>ohB-q5JbCZQ}4KnUlNPkb13KvR`jg?i)q`bax5mC=hFDC+l_=dTo7P1-'
    b'XZ#5OAEwP&CAAj_ZYzHH~rcV3C^Y5#AyJG!F8Rbi31Lp?kRVsf{`mYG&ImzRLvms-NS1BMnv0BKPsfK}ZBmy3mx2A>Kn}a|pum>N'
    b'2RqZXhFPIN?})o6nuN7RyI6JjzE}@5vCtmh>)KxLrY5yKC&OtniQaUxveR%6HhdbT^ssL((~Y3rJ~kT*Ku#PB$EDdva*t=K9E;U5'
    b'qDBJw@@0Z}Ff)*L<6>eimXDUy#oN@@qxAGU8%YOjiYTBQ)n$L+4$P^WjY}Rn=m8C?0Y0RG1bE_^Mrv)hdL1KBva}Pz7;vN-'
    b'9|9^6_#QZe=-Khaxhm4tRDPdB&Cr?ZYopQv9?~R7Kg^cGioT^e5LddBQfP-Z)#x5F!)KxIFPb?+PjKMT1|90J=~qo-'
    b'_83ZTiVpK5XZiMa6QnJG;d8bfi3ql0zep?p(NKw&kV}=lJbc^qKiN6;S7Hd`0OgZO*&)sl>zkJsaMJD#f*l{+y4bMK>{Pz{+lQZT'
    b'Je`)`2Chf2#I4Sg81G;oQXcEH=QTGGy-Ay0+2zmvucwLkeBB)F$Rfa$+8Jig}mh$9y$X`)K9Znk)P=9kSvNzs_{?;hGlbKpo)JRN'
    b'YRIx=%Y;7Xe_}<0U}z)yV%xgR^&kfhXK;wiMgZdhrdrS^)mNXW#_uax$c7O9k*#fg!5Vf4)@v;2X}dHU4$g=Ft_q2+JhCBujS0Wk'
    b'>iv_)pc{)M>G|J)hc-'
    b'$30X8IzYT+Gaid9w>o94I$d;#HZ}*;z!b@#=sFb9^j!oC0LNJ+5Y!R2mIZnjV@yO%bp+@rkU~>PPJicBmIj?tfTT+8HA*6*_TRYt'
    b'4Up<%^7Gag$DJauB`S*A)Jo^n7x~BKIHF!0(OnBS@f1otU6iHvP#(6g9z8T<<;x1uR&yaW5f@s4roNBc1>`!F7o#4&njM`N&ims^'
    b'5{=c7=7(zi7S&_AT#Obtu068J*)2^`x<#4*`VAXjX9`voQ&QWOIp)l|97c5De@9QfKrh%iay#2$-'
    b'lSv@&zvAS$z%7?(~0U0Pa~wZ@nF#?T-'
    b'6w(t!l+YBRzgt;{C0sEwa~c#+X}wb|Xz8EO$^e(c&noTH}hIcDThAU>7%|;}k?7;#inl>&q^+Kke)|zFCbxKKYehc6|A4DXPIP;S'
    b'0NsJzaDl^Ec(l^{RB<y%J1Mqw3b3oS*JkdU2b8*ZC@zd+V&Q>pMg#Ww*d})?-'
    b'L7Ic#TAX!IGTT{e^WUHWN(oR#8+Vn>Tm@C)AXXrI=1n&A3PrO4`mX!@(1%jxz5x29ga4x{D~??0m}PRHs|?C3!wL#(0UG)ZReiPN'
    b'Ub-*xA6r^L#&UKJ1k#fzH97N_&8D;AQ)S2sTHB)<R-'
    b'Rp_~VuR>rMesl0mSKqvGBN~?!Olk>0TRB3UHuFuVQ5$)#JHJ9<E;h_mwc_UoXq{+xJHLY)Np3s?`QPM8T6lE}R?BR1m<k5NZdtta'
    b'LG~*FfzLFff=`b_k)!+Il(~!%(8y2zo>E-N;!S<-ge5`4gup^pfxp1`aR&dcu*=OLSIB8nxUTYFyXi_kPgfAA6L%f-'
    b'1h95FWFmlRZGPonrA@Oo*f>XWIcV<?%u?-;%+#u8SQ_yW4#DJ)7Ozc95ds-'
    b'0^*)(_fBh{Rk3<`bp(G#3X37qlaHC$SvkS32DGs`3i*8eEtE7|a(QueX7rn8HR?ig@tT??xHgJ^Ws6o8l2aXPTYIk=jhF0NxT0)+'
    b'ofj_;ZS?uB{%A$)n{BZ0FfqT-'
    b'H{3@9sHD{m0rL2v5BO>EpN4pla>71aHS|*pG^;GghRx8*+$U|n}(ST3t^5iM|H+kaxU1#(~OLOHrRTEb$X<mbf^{V=ui!<oeO~7V'
    b'{0Y3d`{Ot-hH#KW}#*bP5z4={I&NOcGy=v8nqr_QX+Il#K>_vsL@e`G%x@|xytwBg7Fx2bEHuZYQHf~|I-'
    b'COD^AlT@!0e+9+lJ|tmG<RYQdn9mzg=(qc2)Qpepc>r4s=|uT;>$#LjfjEV)Ym$vd!XMtRNu%h1VJ3s<DP)~(~JhYe0*UYpGeuTr'
    b's!ZdptCQ5{_?illzsixtm*1j3Lke+BKx2}J|=ImD-'
    b'9j3hKm#5*}XhaRzm<logC%hogRc$zO@|#lwCQ^Ay);H1$ifC8eCP^QoUlnPa9h3_Ed3m>x*!9&F{QI<*r_3?0r}N^M4PaW9a'
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
    candidate = words_string  # noqa: F405
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
