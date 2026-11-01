import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[''],
 ['abcde'],
 ['abcdecadeCADE'],
 ['aaaaAAAAaaaa'],
 ['Jerry jERRY JeRRRY'],
 ['AbCdEfG'],
 ['banana'],
 ['1234567890'],
 ['hello123'],
 ['The quick brown fox jumps over the lazy dog'],
 ['THISISALONGSTRINGWITHNOSPACES'],
 ['aaaabbbbccccddddeeeeffffgggghhhhiiii'],
 ['AaBbCcDdEeFfGgHhIi'],
 ['hello world'],
 ['1,2,3... go!'],
 ['The quick brown fox jumps over the lazy doAbCdEfGg'],
 ['hellold'],
 ['1,2,3... gog!'],
 ['lhello wworld'],
 ['1,2,3... go123hello12345The quick brown fox jumps ovTHISISALONGSTRINGWITHNOSPACESer the lazy '
  'doAbCdEfGg67890g!'],
 ['AaBbCcThe quick brown fox jumps over the lazy doAbCdEfGgDdEeFfhello worldGgHhIi'],
 ['AaBbCcThe quichelloldk brown fox jumps over the lazy doAbCdEfGgDdEeFfhello worldGgHhIi'],
 ['1,2,3.hellold.. gog!'],
 ['hello wThe quick brown fox jumps over the lazy doAbCdEfGgorld'],
 ['hell1,2,3... go!o world'],
 ['AbCdE'],
 ['hellAbCdE world'],
 ['1,2,3.AaBbCcThe quick brown fox jumps over the lazy doAbCdEfGgDdEeFfhello worldGgHhIi.. go!'],
 ['hello wThe quick brown fox jumps over e lazy doAbCdEfGgorld'],
 ['1,2,3... go123hello12345The quick bbrown fox jumps ovTHISISALONGSTRINGWITHNOSPACESer the lazy '
  'doAbCdEfSGg67890g!'],
 ['THISISALONGSTSRINGWITHNOSPPACES'],
 ['1,2,3hellold.hel,lold.. 2gog!'],
 ['AEbCdE'],
 ['The quick brcown fox jumps over the lazy doAbCdEfGg'],
 ['CdE'],
 ['1,2,3hellhelhelloldloldold.hel,lold.. 2gog!'],
 ['1,2,3... go123hello12345The quick bbrown foxhellAbCdE world jumps '
  'ovTHISISALONGSTRINGWITHNOSPACESer the lazy doAbCdEfSGg67890g!'],
 ['The oquick brown fox jumps overg'],
 ['AaBbCcThe qldGgHhIi'],
 ['The quick brown fox jumps over t1,2,3... go123hello12345The quick bbrown foxhellAbCdE world '
  'jumps ovTHISISALONGSTRINGWITHNOSPACESer the lazy doAbCdEfSGg67890g!he lazy doAbCdEfGg'],
 ['hello wThe quick brrown fox jumps over e lazy doAbCdEfGgorld'],
 ['Cd1,2,3hellhelhellol.dloldold.hel,lold.. 2gog!E'],
 ['helllold'],
 ['hellr1,2,3... go!o world'],
 ['THISISALONNGSTRINGWITHNOSPACES'],
 ['AahelloldBbCcThe quick brown fox jumps over the lazy doAbCdEfGgDdEeFfhello worldGgHhIi'],
 ['bananCd1,2,3ellhelhellol.dloldold.hel,lold.. 2gog!E'],
 ['1,2,3..Cd1,2,3hellhelhellol.dloldold.hel,lold.. 2gog!E. go!'],
 ['lhello wTHISISALONGSTRINGWITHNOSPACES'],
 ['hello wo1,2,3... gog!rld'],
 ['The quick brrown fox jumps over tehe lazy dog'],
 ['hello wo1,2,3 gog!rld'],
 ['The quick brcown cfox jumps over the lazy doAbCdEfGg'],
 ['AaBbCcThe quichelloldk brown fox jumhelloldps over the lazy doAbCdEfGgDdEeFfhello worldGgHhIi'],
 ['hellAbCdE worhld'],
 ['AaBbCcThe quichelloldk brown fox jumhelloldps over thello wThe quick brown fox jumps over e '
  'lazy doAbCdEfGgorldhe lazy doAbCdEfGgDdEeFfhello worldGgHhIi'],
 ['THISISALONGSTRINGWITHNOSPACESThe quick brown fox jumps over the lazy doAbCdEfGg'],
 ['1,2,3hellhelhelloldloldol1234567890d.hel,lold.. 2gog!'],
 ['AaBbCcThe quichelloldk brown fox jumpsAaBbCcDdEeFfGgHhIiver the lazy doAbCdEfGgDdEeFfhello '
  'worldGgHhIi'],
 ['123456789aaaabbbbccccddddeeeeffffgggghhhhiiii0'],
 ['1,2,3.AaBbCcThe quick brown fox jumps over thhello worlde lazy doAbCdEfGgDdEeFfhello '
  'worldGgHhIi.. go!'],
 ['The quick brcowen fox jumps over the lazy doAbCdEfGg'],
 ['123456078980'],
 ['12The quick brown fox jumps over t1,2,3... go123hello12345The quick bbrown foxhellAbCdE world '
  'jumps ovTHISISALONGSTRINGWITHNOSPACESer the lazy doAbCdEfSGg67890g!he lazy '
  'doAbCdEfGg3456789aaaabbbbccccddddeeeeffffgggghhhhiiii0'],
 ['THISISALONGSTSRIGWITHNOSPPACES'],
 ['1,2,3.hellohello wo1,2,3 gog!rldld.. gog!'],
 ['1,2,3hellhelhelloldloldol12345671,2,3... go123hello12345The quick bbrown foxhellAbCdE world '
  'jumps ovTHISISALONGSTRINGWITHNOSPACESer the lazy doAbCdEfSGg67890g!890d.hel,lold.. 2gog!'],
 ['1,2,3hellhelhelloldloldTHISISALONNGSTRINGWITHNOSPACESol1234567890d.hel,lold.. 2gog!'],
 ['ACbCdEfG'],
 ['The quick brown fox bCdEfGg'],
 ['aaaabbbbccccddddeeeeffffggggAbCdEfGhhhhiiii'],
 ['AahelloldBbCcThe quick brown fox jumps over the lazy doAbCdEfGgDdEeFfhello worldAGgHhIi'],
 ['aaaabbbbccccddddeeeeffffggCdEgghhhhiiii'],
 ['1,2,3.AaBbCcThe quick brown  fox jumps over thhello worlde lazy dofAbCdEfGgDdEeFfhello '
  'worldGgHhIi.. go!'],
 ['AbCdEAahelloldBbCcThe quick brown fox jumps over the lazy doAbCdEfGgDdEeFfhello worldGgHhIifG'],
 ['AbCdEAahelloldBbCcThe quick browAaBbCcThe quichelloldk brown fox jumps over the lazy '
  'doAbCdEfGgDdEeFfhello worldGgHhIin fox jumps over the lazy doAbCdEfGgDdEeFfhello worldGgHhIifG'],
 ['1,2,3hellhelhelloldloldol12345671,2,3... go123hello12345The quick bbrown foxhellAbCdE world '
  'jumpsl ovTHISISALONGSTRINGWITHNOSPACESer the liazy doAbCdEfSGg67890g!890d.hel,lold.. 2gog!'],
 ['THISISALONGSTAaBbCcThe qldGgHhIiSRINGWITHNOSPPACES'],
 ['THISISALONNGSTRINIGWITHNOSPACES'],
 ['helAahelloldBbCcThe quick brown fox jumps over the lazy doAbCdEfGgDdEeFfhello '
  'worldAGgHhIilo123'],
 ['AbCAaBbCcThe quichelloldk brown fox jumhelloldps over thello wThe quick brown fox jumps over e '
  'lazy doAbCdEfGgorldhe lazy doAbCdEfGgDdEeFfhello worldGgHhIidEfG'],
 ['BKktjaBaaaabbbbccccddddeeeeffffgggghhhhiiiiKkh'],
 ['The quick broTHISISALONGSTAaBbCcThe qldGgHhIiSRINGWITHNOSPPACESwn fox jumps over the lazy dog'],
 ['1,2,3.hellold.. ghello wo1,2,3 gog!rldog!'],
 ['The oquick brown fox jumps ove rg'],
 ['The quick brown fox jumps over t1,2,3... go123hello12345The quick bbrown foxhellAbCdE world '
  'jumps ovTHISSISALONGSTRINGWITHNOSPACESer the lazy doAbCdEfSGg67890g!he lazy doAbCdEfGg'],
 ['CTHISISALONGSTSRIGWITHNOSPPACESdE'],
 ['AbCdEAahelloldBbCcThe qCTHISISALONGSTSRIGWITHNOSPPACESdEuick brown fox jumps over the lazy '
  'doAbCdEfGgDdEeFfhello worldGgHhIifG'],
 ['1,2,3hellhelhelloldloldol12345671,2,3... go123hello12345The quick bbrown foxhellAbCdE world '
  'jumpsl ovTHISISALONGSTRINGWITHNOSPACESer the liazy doAbCdEfSGg67890g!890d.hel,lold.. 2gWog!'],
 ['hellAbCdE wor1,2,3.hellohello wo1,2,l3 gog!rldld.. gog!hld'],
 ['AbCdEAahelloldBbCcThe quick brown fox jumps over the lazy doAbCdEfGgDdEe Ffhello worldGgHhIifG'],
 ['CTHISISALONGSTSRIGWITHNOSPPAdE'],
 ['AbCdEAahelloldBbCcThe qCTHISISALONGSTSRIGWITHNOSPPACESdEuick brown fox jumps over tThe oquick '
  'brown fox jumps overghe lazy doAbCdEfGgDdEeFfhello worldGgHhIifG'],
 ['AbCdEAahelloldBbCcThe quick browAaBbCcThe quichelloldk brown fox jumps over othe lazy '
  'doAbCdEfGgDdEeFfhello worldGgHhIin fox jumps over the lazy doAbCdEfGgDdEeFfhello worldGgHhIifG'],
 ['BKktjaBaaaabbbbccccddddeeeeffffAaBbCcDdEeFfGgHhIigggghhhhiiiiKkh'],
 ['The quick brown fox jumpsg over tThe quick brown foxl jumps over the lazy doAbCdEfGgazy '
  'doAbCdEfGg'],
 ['The quick brown fox jumpsg over tThe quick brown foxl jumps over the lazy doAbCdEfGdEfGg'],
 ['hello wThe quick brown fox jump1,2,3... go123hello12345The quick brown fox jumps '
  'ovTHISISALONGSTRINGWITHNOSPACESer the lazy doAbCdEfGg67890g!s over the lazy doAbCdEfGgorld'],
 ['The quick brown fox jumpsg over tThe quick brown foxl jumps oCver the lazy doAbCdEfGdEfGg'],
 ['1,2,3.hellold.. The quick broTHISISALONGSTAaBbCcThe qldGgHhIiSRINGWITHNOSPPACESwn fox jumps '
  'over the lazy doggog!'],
 ['1,2,3.hellohello wo1,2,3 go g!rldld.. gog!'],
 ['AaBbCcThe quichelloldk brown fox jumps over the lazy doAbCdEfGgDdEeFfhello HworldGgHhIi'],
 ['1,2,3... go123hello12345The quick bbrPown fox jumps oTRINGWITHNOSPACESer the lazy '
  'doAbCdEfSGg67890g!'],
 ['1,2,3... g,o123hello12345The quick brown fox jumps ovTHISISALONGSTRINGWITHNOSPACESer the lazy '
  'doAbCdEfGg67890g!'],
 ['THISISALONNGSTRINGITHNOSPACES'],
 ['pneumonoultramicroscopicsilicovolcanoconiosis'],
 ['"I am a complex sentence, with lots of punctuation!" said the fox.'],
 ['1234$%?!@'],
 ['The quick brown fox jumps over the lazy dog. 1234567890'],
 ['!"£$%^&*()_+-={}[]|\\:;"<>,.?/~`'],
 ['This is a sentence with repeating characters, such as "s", "e", and "n".'],
 ['This is another sentence with repeating characters, such as "t", "h", and "i". The two '
  'sentences combined should return 26 distinct characters.'],
 ['This sentence contains a mix of uppercase and lowercase letters, but all characters should be '
  'treated as distinct.'],
 ['This sentence has repeating characters such as "t", "h", and "s". The quick brown fox jumps '
  'over the lazy dog.'],
 ['22'],
 ['distinct.'],
 ['"I am a complThe quick brown fox jumps over the lazy dogex sentence, with lots of punctuation!" '
  'said the fox.'],
 ['Then quick bro1234$%?!@wn fox jumps over the lazy dog'],
 ['"h",'],
 ['am'],
 ['222'],
 ['complex'],
 ['The quick brown fox jumptreateds ovebro1234$%?!@wn the lazy dog. 1234567890'],
 ['such'],
 ['return'],
 ['"n".'],
 ['This is another sentenlazycters.'],
 ['repeating'],
 ['fox.lowercase'],
 ['repcombinedeating'],
 ['This is anoth"i".'],
 ['vD22ZtLSjt'],
 ['fox'],
 ['repeaing'],
 ['ureturn'],
 ['repcombinedeaticontainsng'],
 ['"i".'],
 ['repting'],
 ['of'],
 ['aam'],
 ['26of'],
 ['fsox.Thenlowercase'],
 ['distinThe quick brown fox jumps over the lazy dog. 1234567890ct.'],
 ['ovebro1234$%?!@wn'],
 ['treated'],
 ['"i"i.'],
 ['This sentence has repeating characters such as "t", "h", and "s". The quick brown foxasg.'],
 ['vD22ZtLsenatencedistinTheSjt'],
 ['quick'],
 ['lazy'],
 ['This sentence has repeating chasentenceracters such as "t", "h", and "s". The quick brown '
  'foxasg.'],
 ['a'],
 ['"e",'],
 ['commplex'],
 ['This is a sentence with repeating characters, such arepeatings "s", "e", and "n".'],
 ['"s",'],
 ['comcomplexplex'],
 ['reepeating'],
 ['"e"e,'],
 ['This sentence has repea ting characters such as "t", "h", and "s". The quick brown fox jumps '
  'over the lazy dog.'],
 ['The quick brown fox jumps ovy dog'],
 ['dogex222'],
 ['comcomplanoth"i".explex'],
 ['The quick brown fox jumptreateds ovebro1anotherg. 1234567890'],
 ['lletters,'],
 ['bro1234$%?!@wn'],
 ['laazy'],
 ['lots'],
 ['distinct'],
 ['repting222'],
 ['as'],
 ['characters,'],
 ['ofis'],
 ['characterrs,'],
 ['commpplex'],
 ['re"h",pting222'],
 ['fox.'],
 ['The quick brown fox jumps orepcombinedeaticontainsngazy dog. 1234567890'],
 ['comcomplanotx'],
 ['bro123$4$%?@!@wn'],
 ['123?4$"e",%?!@'],
 ['quic'],
 ['uch'],
 ['This is  a sentence with repeating characters, such as "s", "e", and "n".'],
 ['commbrownpplex'],
 ['uuch'],
 ['This sentence has repea ting characters such as "t", "h", and "s". The quick bruown fox jumps '
  'over the lazy dog.fox.lowercase'],
 ['ovebro1234$%?!@@wn'],
 ['comtwombrownpplex'],
 ['222distinct'],
 ['bro1234$%?!123?4$"e",%?!@@wn'],
 ['dWesgo'],
 ['uppercase'],
 ['dogex'],
 ['x'],
 ['pting'],
 ['colex'],
 ['combined'],
 ['edog.fox.lowerdogcase26of'],
 ['all'],
 ['dogegx'],
 ['comcomplcommplexanotx'],
 ['uchh'],
 ['comtworownpplex'],
 ['This is  a sentence with repeating cdWesgosuch as "s", "e", and "n".'],
 ['comcomplanoth"i"explex'],
 ['chasentenceracters'],
 ['"t",'],
 ['comtwo1234$%?!@mbrownpplex'],
 ['ofpneumonoultramicroscopicsilicovolcanoconiosis'],
 ['chsalowercaseracters,'],
 ['uThis is  a sentence with repeating cdWesgosuch as "s", "e", and "n".ch'],
 ['This is another senthenlazycters.'],
 ['sentence'],
 ['",'],
 ['llettuppercaseers,'],
 ['comcomplcommpl"I am a complex sentence, with lots of punctuation!" said the fox.exanotx'],
 ['re"h",pting2"22'],
 ['fo"e"e,x'],
 ['rQXXxau'],
 ['bruown'],
 ['comcompmlcommplexanotx'],
 ['bro1n234$%?!!@wn'],
 ['This is another sentence with repeating characters, such as "t", "h", combinedand "i". The two '
  'sentences combined should return 26 distinct characters.'],
 ['charas,'],
 ['26oof'],
 ['comcomplexplexting'],
 ['"I am a complex sentence, with lots of punctuation!" said  the fox.'],
 ['characterrcs,'],
 ['comtwo1234$%?!@mbrownre"h",pting222pplex'],
 ['characters.'],
 ['ovcomtwo1234$%?!@mbrownre"h",pting222pplexebro1234$%?!@@@wn'],
 ['uquic'],
 ['disitinct'],
 ['This is a sentence with repeating characters, such as "s", foxasg."e", and "n".'],
 ['"I'],
 ['22re"h",pting2222'],
 ['combinedand'],
 ['comcomplcexplexting'],
 ['"i"i1234567890.'],
 ['bro1234$%?This sentence contains a mix of uppercase and lowercase letters, but all characters '
  'should be treated as distinct.!@wn'],
 ['combineThedand'],
 ['This is  a sentence with repeating cdWesgosuch as "s", "ee", and "n".'],
 ['dogo.'],
 ['Thith repeabro1234$%?This sentence contains a mix of uppercase and lowercase letters, but all '
  'characters should be treated as distinct.!@wnting charactarepea, such as "s", "e", and "n".'],
 ['lowercase'],
 ['ubro1234$%?!123?4$"e",%?!@@wnuch'],
 ['Then quick bro1234$%?z?!@wn fox jumps over the lazy dog'],
 ['quiqc'],
 ['repeainbeg'],
 ['and'],
 ['This sentence has repea ting characters such as "t", "h", and "s". The quick bruozy '
  'dog.fox.lowercase'],
 ['fox.lowercasThith repeabro1234$%?This sentence contains a mix of uppercase and lowercase '
  'letters, but all characters should be treated as distinct.!@wnting charactarepea, such as "s", '
  '"e", and "n".e'],
 ['This sentence has repea ting characters such as "t", "h", and "s". The quick brown fox jumps '
  'over the ldazy dog.'],
 ['uppercasee'],
 ['Thisall'],
 ['aall'],
 ['do2gex222'],
 ['ofpunctuation!"'],
 ['!"£$charas,%^&*()_+-={}[]|\\:;"<>,.?/~`'],
 ['distinct.!@wnting'],
 ['Thisallchasentenceracters'],
 ['!"£$%^&*()_+-={}[]|\\:;"<>,.?/^~`'],
 ['This sentence has repeating characters such as "t", "h", and "s". The quick brown uuchfoxasg.'],
 ['comcomplcommpl"I am a complex senh lots of punctuation!" said the fox.exanotx'],
 ['vAhhv'],
 ['"I am a complThe quick brown fox jumps over the lazy dogex sentence, with lots of pion!" said '
  'the fox.'],
 ['repeabroThis is another sentenlazycters.s'],
 ['ubro1234$%?!123commpplex?4$"e",%?!bro1234$%?!123?4$"e",%?!@@wn@@wnuch'],
 ['amm'],
 ['qCrF'],
 ['brruown'],
 ['The quick brown fox jumorepcombinedeaticontainsngazyptreateds ovebro1anotherg. 1234567890'],
 ['This'],
 ['Thith'],
 ['"I am a complThex quick brown fox jumps over the lazy dogex sentence, with lots of '
  'punctuation!" said the fox.'],
 ['"Iubro1234$%?!123commpplex?4$"e",%?!bro1234$%?!123?4$"e",%?!@@wn@@wnuch'],
 ['ubro1234$%?!123commpplex?4$"e",%?!bro123@wn@@wnuch'],
 ['brrun'],
 ['ZaojBy'],
 ['chsalowercaseracters'],
 ['dogegThis sentence has repea ting characters such as "t", "h", and "s". The quick brown fox '
  'jumps over the lazy dog.'],
 ['repeeainbeg'],
 ['characterrcsr,'],
 ['222distidnsct'],
 ['comcomplcexple"i"i.xting'],
 ['2t'],
 ['combineThecomtworownpplex'],
 ['fox.lowercasThith repeabro1234$%?This sentence contains a mix of uppercase and lowercase '
  'letters, but all characters should be treated as anoth"i".distinct.!@wnting charactarepea, such '
  'as "s", "e", and "n".e'],
 ['chaxsentenceracters'],
 ['This is a sentence wtheith repeating characters, suchcomcomplcexplexting".'],
 ['brno1234$%?!@wn'],
 ['is'],
 ['said'],
 ['jumptreateds'],
 ['pion!"'],
 ['The quick brown fox jumps over the lazy dog. 123456789'],
 ['"I am a comcharacterrs,plex sentence, with lots of punctuation!" said the fox.'],
 ['iss'],
 ['"I am a complThex quick brown fox jumps over the lazy dogex sentence, with lots nof '
  'punctuatiotn!" said the fox.'],
 ['comtworowncomcompmlcommplexanotxlex'],
 ['fox.exanotx'],
 ['"h"vD22ZtLsenatencedistinTheSjt,'],
 ['comcomplcommplexanotxofis'],
 ['26o'],
 ['pirepeainbegon!"'],
 ['"IdogegThis'],
 ['This sentences has repeating characters such as "t", "h", and "s". The quick brown uuchfoxasg.'],
 ['ddogex222'],
 ['JdmjOJcRx'],
 ['"s"",'],
 ['repeabroshould1234$%?This'],
 ['chasentenceeracters'],
 ['ofpunbrrunctuuation!"'],
 ['"I am a complThe quick brown fox jumps over the lazy dogex sentence, with lots of pion!" said '
  'the foxh.'],
 ['2tt'],
 ['combibned'],
 ['kEjzTF'],
 ['22re"hsenh",pting2222'],
 ['aallsescomcharacterrs,plexhouldntenlazycters.'],
 ['suchcomcomplcexplexting".'],
 ['uppercae'],
 ['comcompl1234567890explex'],
 ['bro1234$%?z?!@wn'],
 ['repeabroThis'],
 ['comcompmlcoThis is anoth"i".mmplexanotx'],
 ['cdWesgosuch'],
 ['This sentence has repeating characters such as "t", "h", and "s". The quick brown '
  'uuchfoxrepeainbegasg.'],
 ['jumps'],
 ['@mbrownpplex'],
 ['"Iubro1234$%?!123commpplex?w4$"e",%?!bro1234$%?!123?4$"e",%?!@@wn@@wnuch'],
 ['ammchasentenceracters'],
 ['"comcomplexplexi".'],
 ['"I am a complex sentence, with lots of punct26ofuation!" said the fox.'],
 ['characterrss,'],
 ['"I am a complThe quick brown fox jumps over the lazy dogex sentence, wdistinThe quick brown fox '
  'jumps over the lazy dog. 1234567890ct.ith 26.'],
 ['containins'],
 ['rQXXQxau'],
 ['26anoth"i".mmplexanotxf'],
 ['jumpps'],
 ['fox.lowercasThith'],
 ['fsox.Thennlowercase'],
 ['tureturn'],
 ['Thitcharacters,h'],
 ['This sentence has repeating chasentencer acters suc"s".and "s". The quick brown foxasg.'],
 ['Then quick bro1234$%?!@wn fox jumps over the dog.lazy dog'],
 ['laaazy'],
 ['"i"i.fox'],
 ['This sentence has repea ting characters such as "et", "h", and "s". The quick brown fox jumps '
  'over the ldazy dog.'],
 ['This is a a sentence with repeating characters, such as "s", "e", and "n".'],
 ['comccharacterrcs,omplcexple"i"i.xting'],
 ['cmplex'],
 ['ereepeating'],
 ['ng".'],
 ['repea'],
 ['repeabro1234$%?This'],
 ['cormtworownppubro1234$%?!123commpplex?4$"e",%?!bro123@wn@@wnuchlex'],
 ['OTAcPh'],
 ['bro1234$%?!123?4$"e"i"i1234567890.",%?!@@wn'],
 ['dog'],
 ['camharacterrcs,'],
 ['jumpsdWesgo'],
 ['This sentences has repeating charhacters such as "t", "h", and "s". The quick brown '
  'uuchfoxasg.'],
 ['1234567890ct.ith'],
 ['."i"..'],
 ['chsaloweraamcaseracters,'],
 ['"Iubro1234$%?!123commpplex?4$"e",%?!bro1234$%?!123?4$bro1234$%?Thisn@@wnuch'],
 ['comtworownpplereepeatingex'],
 ['The quick brown fox jumps orepcombinedeaticonta2insngazy dog. 1234567890'],
 ['lSJrRmZld'],
 ['characters'],
 ['aallsescomcharacter,rs,plexhouldntenlazycters.'],
 ['osuchcomcomplcexplexting".vebro1234$%?!@@wn'],
 ['characterrcstreated,'],
 ['t enlazycters.'],
 ['123456789'],
 ['foxh.'],
 ['gureptingquic'],
 ['"hThe quick brown fox jumptreateds ovebro1234$%?!@wn the lazy dog. 1234567890",'],
 ['chraracterrss,'],
 ['iissss'],
 ['aaam'],
 ['This sentence has repea ting characters such as "tam", "h", and "s". The quick bruozy '
  'dog.faamox.lowercase'],
 ['Thitchareacters,h'],
 ['iis'],
 ['1234567890ct.'],
 ['ovebro1234$%?!@@!wn'],
 ['dog.lazy'],
 ['comabineThedlowercaseand'],
 ['distinct.!@wn'],
 ['Thitcharactersh,h'],
 ['ddoge22'],
 ['anoth"i".'],
 ['JdmjOJcRdx'],
 ['comcomplanoth"i".aexplex'],
 ['sentence"h",'],
 ['er@mbrownpplexeepeating'],
 ['iidog.lazyssss'],
 ['comcomplelxplexting'],
 ['r"ee",eepeating'],
 ['comtmbrownpplex'],
 ['characcterrcs,'],
 ['This sentence has rcepeating characters such as "t", "h", and "s". The quick brown foxasg.'],
 ['"hThe quick brown fox jumptreateds ovebro1234$%?!@wn t"Ihe lazy dog. 123456780",'],
 ['!."£$%^&*()_+-={}[]|\\:;"<>,.?/^~`'],
 ['distincnt.'],
 ['comcomplanoth"i".expex'],
 ['cowmtworownpplex'],
 ['ovy'],
 ['dcharaccterrcs,o2gex222'],
 ['Then quick bro1234$%?!@wn fox jumps over the dog.lazy bro1n234$%?!!@wndog'],
 ['fsox.Thenlowercasxe'],
 ['comcompletreatedlxplelxting'],
 ['bro1234$%kEjzTF?!123?4$"e",%?!@@wn'],
 ['fsox.Thennedog.fox.lowerdogcase26ofowercase'],
 ['ddog.oglletters,o.'],
 ['dogeuchhx'],
 ['osuchcomcomplcexplexting".vebrThisallchasentenceracters%?!@@wn'],
 ['distinct.!commbrownpplex@wnting'],
 ['comtwo1234$%?!@mb?rownre"1234567890ct.h",pting222pplex'],
 ['",,h",,'],
 ['osuchcomcodogegThis sentence has repea ting characters such as "t", "h", and "s". The quick '
  'brown fox jumps over the lazy dog.mplcexplexting".vebro1234$%?!@@wn'],
 ['fox.lowerandcasThith'],
 ['ovcomtwo1234$%?!@mcomtwo1234$%?!@mbrownre"h",pting222pplexbrownre"h",pting222pplexebro1234$%?!@@@wn'],
 ['rereepeatingea'],
 ['o4veb34$%?!@wn'],
 ['This is a sentence with repeating characters, such arepeatings "s" "n".'],
 ['ovebro1comcompletreatedlxplelxting234$%?!@wn'],
 ['Then'],
 ['sbro1234$%kEjzTF?!123?4$"ew",%foxasg.?!@@wn'],
 ['comcomplexpcharacters,lextin'],
 ['comccharacterrcs,omplcexple"i"ixting'],
 ['suc'],
 ['comcomplanoth"i"'],
 ['disitinict'],
 [',",'],
 ['This sentence has rcepeating characters such acommplexs "t", "h", and "s". The quick brown '
  'foxasg.'],
 ['anoth"i".distinct.!@wnticngTsentence"h",'],
 ['ng"".'],
 ['ano"nh",'],
 ['"t",combineThedand'],
 ['comcompmlcommplexanotxcomtwo1234$%?!@mbrownre"h",pting222pplex'],
 ['aaldisitinct'],
 ['"i"i1234567890.This sentence has repea ting characters such as "et", "h", and "s". The quick '
  'brown fox jumps over the ldazy dog.'],
 ['2characcterrcs,6o'],
 ['This is another senthenlazycters.gureptingquic'],
 ['complThex'],
 ['!."£$%^rQXXQxau&*()_+-={}[1234567890",]|\\:;"<>,.?/^~`'],
 ['ofpunbrruncjuemptreatedswithtuuation!"'],
 ['rRrToH'],
 ['nX'],
 ['asbro1234$%kEjzTF?!123?4$"ew",%foxasg.?!@@w2nm'],
 ['reepeeating'],
 ['rQXXaQxau'],
 ['Thitcharacte,h'],
 ['"hThe quick brown fox jumptreateds ovebro1234$%?!@wn t"Ihe lazy dog. "123456780",'],
 ['rQXaaamXQxau'],
 ['fox.lowaercasThith'],
 ['This is  a sentence with repea ting characters, such as "s", "e", and "n".'],
 ['o222repcombinedeaticontainsngazy'],
 ['focomplThexxh.'],
 ['This is  a sentenece with repeating characters, such as "s", "e", and "n".'],
 ['JdmjOJcfoxasg.Rdx'],
 ['ovebofpunbrruncjuemptreatedswithtuuation!"ro1234$%?!@@!wn'],
 ['acomcomplanotx'],
 ['This is a sentence with repeatieng characters, such asrepeatings "s", "e", and "n".'],
 ['comcharacterrs,plex'],
 ['The quick brown fox lazy dog. 1234567890'],
 ['enlazyrs.'],
 ['"".'],
 ['pirepeainbegoncomtwo1234$%?!@mbrownre"h",pting222pplex"'],
 ['comcomplanooth"i".expex'],
 ['foxasg.'],
 ['"Iubro1234$%?!123commppchasentencerlex?4$"e",%?!bro1234$%?!123?4$bro1234$%?Thisn@@wnuch'],
 ['123456789This is anoth"i".0ct.ith'],
 ['"comcomplexplexei".'],
 ['uccommbrownpplex'],
 ['bronwn'],
 ['ani".'],
 ['nof'],
 ['renbeg'],
 ['ibruowns'],
 ['This is a sentence with repeatieng characters, such asrepThis is a sentence wtheith repeating '
  'characters, suchcomcomplcexplexting".eatings "s", "e", and "n".'],
 ['"i"i1234567890.This sentencefoxh. has repea ting characters such ast "et", "h", and "s". The '
  'quick brown fox jumps over the ldazy dog.'],
 ['reptingereepeating'],
 ['bro1234$%?4This'],
 ['22re"hsenh",pting2JdThe quick brown fox lazy dog. 1234567890mjOJcfoxasg.Rdx222'],
 ['comcomplanorepeabroThistx'],
 ['asbro11234$%kEjzTF?!123?4$"ew",%foxasg.?!@@w2nm'],
 ['ovebro1anotherg.'],
 ['fox.lower@mbrownpplexandcasThith'],
 ['anoth"i".distinct.!@wnticngT",'],
 ['re"h",pti222'],
 ['This is a sentence with repeatieng characters, such asrepThis is a sencexplexting".eatings "s", '
  '"e", and "n".'],
 ['"Iubro1234$%?!123commibruownspplex?4$"e",%?!bro1234$%?!123?4$"e",%?!@@wn@@wnuch'],
 ['@mbrolex'],
 [',222distidnsct",'],
 ['combineTcharacterrcstreated,hecomtworownpplexdogo.'],
 ['comabiaseand'],
 ['ng"".umps'],
 ['ofpunbmptreatedswithtuuation!"'],
 ['ldazy'],
 ['g"f punctuation!" said the fox.ureptingquic'],
 ['"s"",,'],
 ['JdmjOfoxasg.Rdx'],
 ['col'],
 ['"s"'],
 ['ovebofpunbrruncj$%?!@@!wn'],
 ['uThis is  a sentence withs repeating cdWesgosuch as "s", "e", and "n".chrQXXQxau'],
 ['uuchfoxrepeainbegasg.'],
 ['PZactersF'],
 ['ting'],
 ['fox.repeabro1234$%?Thisxot'],
 ['Thitchabro123$4$%?@!@wnracters,h'],
 ['fox.ureptingquic'],
 ['nfox.lowercasThith repeabro1234$%?This sentence contains a mix of uppercase and lowercase '
  'letters, but all characters should be treated as anoth"i".distinct.!@wnting charactarepea, such '
  'as "s", "e", and "n".eg"".umps'],
 ['uuchThis is another tsentence with repeating characters, such as "t", "h", combinedand "i". The '
  'two sentences combined should return 26 distinct characters.'],
 ['The quick brown fox '
  '"Iubro1234$%?!123commpplex?w4$"e",%?!bro1234$%?!123?4$"e",%?!@@wn@@wnuchjumps ovy dog'],
 ['retturn'],
 ['jcomtwo1234$%?!@mbrownpplexumptreateds'],
 ['rQXXxu'],
 ['anoth"i".distinct.!@wani".nting'],
 ['rejum"i"i.foxrepeatingpsdWesgonbeg'],
 ['commbrowcnpplex'],
 ['Thitcharactersh'],
 ['12345689'],
 ['fsox.Thbrrunenlowercase'],
 ['This is another sentenlazyctersThith.'],
 ['The quick brown fox jumptreateds ovebro1234$%zy dog. 1234567890'],
 ['combineTcharacterrcstreated,hecomtworownpplexdogo"hThe quick brown fox jumptreateds '
  'ovebro1234$%?!@wn t"Ihe lazy dog. 123456780",.'],
 ['llettupper"i"i1234567890.Thisrs,'],
 ['osuchcomcomplcexple2xting".vebro1234$%?!@@wn'],
 ['acommplexs'],
 ['nfox.lowercasThith'],
 ['ovebro1234$%@wn'],
 ['This sentence has repeating characteras such as "t",comcomplcommpl"I am a complex senh lots of '
  'punctuation!" said the fox.exanotx "h", and "s". The quick brown foxasg.'],
 ['JdmjjOJcRdx'],
 ['anoth"i".odistinct.!@wani".nting'],
 ['another'],
 ['!."£$%^rQXXovebro1234$%?!@@!wnQxau&*()_+-={}[1234567890",]|\\:;"<>,.?/^~`'],
 ['comcompletreatedlmxplelxting'],
 ['dogegThis'],
 ['comcompletreatemdlxplelxting'],
 ['2chpion!"araccterrcs,6o'],
 ['"II'],
 ['"t"bro1234$%?!123?4$"e",%?!@@wn,'],
 ['chsaloweraamcasefox.ureptingquicracters,'],
 ['anno"nh",'],
 ['"123bro1234$%?!123?4$"e",%?!@@wn",'],
 ['ovebrdisitincto1234$%?!@wn'],
 ['g"f'],
 ['acoOTAcPhmmplexs'],
 [''],
 ['22ore"hsenh",pting2JdThe quick brown fox lazy dog. 12345678902x222'],
 ['"e"'],
 ['letters,'],
 ['afBra'],
 ['The quick b9'],
 ['2ttt'],
 ['mix'],
 ['This is ancomtworownpplexothycters.'],
 ['coxmmpplex'],
 ['distinThe'],
 ['"Iubro1234$%?!123commpplex?w4$"e",%?!bro1234$%?!123?4$"e",%?!@@wn@@wnuchjumps'],
 ['cThis is ancomtworownpplexothycters.haras,'],
 ['uThis'],
 ['This is a sentence wtheith repeating chahracters, suchcomcomplcexplexting".'],
 ['mam'],
 ['txilaO'],
 ['ovebofpunebrruncjuemptreatedswithtuuation!"ro1234$%?!@@!wn'],
 ['lletters'],
 ['contains'],
 ['22re"hsing2JdThe'],
 ['fox.lowaercasThithubro1234$%?!123commpplex?4$"e",%?!bro123@wn@@wnuch'],
 ['"n".chrQXXQxau'],
 ['t enlsazycsters.'],
 ['fsox.ThbThis senreepeatingtence has repea ting characters such as "tam", "h", and "s". The '
  'quick bruozy dog.faamox.lowercaserrunenlowercase'],
 ['This sentence contains a mix of uppercase and lowercharacter s should be treated as distinct.'],
 ['uppecrcasee'],
 ['ovebro1comcompletreatedlxplelx!@wn'],
 ['"comcomplexplex"IIi".'],
 ['b,",%ro123$4$%?@!@wn'],
 ['disck brown fox jumps over the lazy dog. 1234567890ct.'],
 ['iisss'],
 ['reepepeating'],
 ['ddogex222comtwombrownpplex'],
 ['anoth"i".dist"comcomplexplex"IIi".t.!@wani".ntin'],
 ['o222repcombinedeaticontainsngazzy'],
 ['omptreateddswithtuuation!"ro1234$%?!@@!wn'],
 ['This is another sentenlazyct ersThith.'],
 ['ddocomtmbrownpplexge22'],
 ['sentenciissseex'],
 ['dog.faamox.lowercaserrunenlowercase'],
 ['ThitTcharactersh,h'],
 ['docharadcterrss,go.'],
 ['disitinuucht'],
 ['Then quick bro1234$%?!@wn fox jumps over the dog.lazydWesgo dog'],
 ['"co,",mcomplexplex"IIi".'],
 ['""i"i.'],
 ['This is  a sentenece with repeating characters, such as "srereepeatingea", "e", and "n".'],
 ['suchcomcompexplexting".'],
 ['@mx'],
 ['disictinuuchtcomcomplcommpl"I'],
 ['"Iubro1234$%?!123commpplex?4$"e",%?!bro1234$%?!123?4$"e",%?!chsaloweraamcaseracters,@@wn@@wnuch'],
 ['rQXXxuu'],
 ['accomtwombrownpplexomcomplanotx'],
 ['Then quick bro1234$%?!@wn afox jumps over the dog.lazydWesgo dog'],
 ['ovcomtwo1234$%?!@mcomtwo1234ownre"h",pting222pplexbrownre"h",pting222pplexebro1234$%?!@@@wn'],
 ['rQXxau'],
 ['ovebro1anotenlazycters.herg.'],
 ['sencexplexting".eatings'],
 ['This is anooverth"i".'],
 ['characomcomplexplextingcters,'],
 ['1111'],
 ['$%^&*aA'],
 ['AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'],
 ['абвгдеёжзийклмнопрстуфхцчшщъыэюя'],
 ['aaaaa'],
 ['abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'],
 ['नमस्ते'],
 ['こんにちは'],
 ['The quick brown fox jucomplexmps over the lazy dog. 1234567890'],
 ['ocharactersvver'],
 ['"I am a complex sentence, with lotsaid the fox.'],
 ['sentence,'],
 ['This is another sentence with repeating characteers, such as "t", "h", and "i". The two '
  'sentences combined should return 26 distinct characters.'],
 ['This sentence has repeating characters such as "t", "h", and "s". The quick brown fox jumps '
  'over the rlazy dog.'],
 ['returtn'],
 ['1This sentence has repeating characters such as "t", "h", and "s". The quick brown fox jumps '
  'over the rlazy dog.234$%?!@'],
 ['over'],
 ['1This sentence has repeating characters such as "t", "hsentence", and "s". The quick brown fox '
  'jumps over the rlazy dog.234$%?!@'],
 ['This sentence has repeating characters suchlots as "t", "h", and "s". The quick brown fox jumps '
  'over the rlazy dog.'],
 ['jucomplexmps'],
 ['ocharactersvve'],
 ['This sentence has repeating characters such as "t", "h", and "s". The quick brown fox jumps '
  'over tehe rlazy dog.'],
 ['pneocharactersvveumonoultramicroscopicsilicovolcanoconiosis'],
 ['The quick brown fs over the lazy dog. 1234567890'],
 ['This sentence has repeating characters such as "t", 26"h", and "s". The quick brown fox jumps '
  'over the lazy dog.'],
 ['uuppercase'],
 ['The quick brown fox jucomplexmps over the  lazy d0'],
 ['"I am a complex sentence, with lotsaid '],
 ['1This sentence has repeating characte ssuch as "t", "h", and "s". The quick brown fox jumps '
  'over the rlazy dog.234$%?!@'],
 ['1This sentence has repeating characte ssuch "Ias "t", "h", and "s". The quick brown fox jumps '
  'over the rlazy dog.234$%?!@'],
 ['suchlots'],
 ['This sentence has repeating characters suchuppercaselots as "t", "h", and "s". The quick brown '
  'fox jumps over the rlazy dog.'],
 ['This is another sentence with repeating characteers, suc two sentences combined should return '
  '26 distinct characters.'],
 ['ocharactersr'],
 ['The quick brown fs over tocharactersrhe lazy dog. 1234567890'],
 ['teheas'],
 ['stetnce,'],
 ['1234$%%?!@'],
 ['sttetnce,'],
 ['1This sentence has repeating characters such as "t", "h", and "s". The quick "I!@'],
 ['!"£$%^&*()_+-={suchuppercaselots}[]|\\:;"<>,.?/~`'],
 ['This sentence has repeating c"Iasharacters suchlots as "t", "h", and "s". The quick brown fox '
  'jumps over the rlazy dog.'],
 ['The qThis sentence has repeating characters such as "t", 26"h", and "s". The quick brown fox '
  'jumps over the lazy dog.uick brown fs over tocharactersrhe lazy dog. 1234567890'],
 ['pu!!"'],
 ['jucompplexmpjs'],
 ['brown'],
 ['This is another sentence with repeating charactiers, such as 1234$%?!@"t", "h", and "i". The '
  'two sentences combined should return 26 distinct characters.'],
 ['This is another se26"h",nt6ence with repeating characteers, suc two sentences combined should '
  'return 26 distinct characters.'],
 ['This is a sentence with repeating characters, such as "s.", "e", and "n".'],
 ['This sentence has repeating characters suchlots as "t", "h", asaidnd "s". The quick brown fox '
  'jumps over the rlazy dog.'],
 ['1This sentence has respeating characters such as "t", "h", and "s". The quick "I!@'],
 ['ssuch'],
 ['1234$%%?!!;"£$%^&*()_+-={}[]|\\:;"<>,.?/~`@'],
 ['1234$%%?!3@'],
 ['lase'],
 ['This sentence has repeating characters such as "t", "h", and "s". The quick brown fox jumps '
  'over the rlazy .'],
 ['This sentence has repeating characters such as "t", 26"h", and "rs". The quick brown fox jumps '
  'over the lazy dog.'],
 ['fs'],
 ['pneumonoultramiicroscopicsilicovolcanoconiosis'],
 ['octeheasharactersvver'],
 ['This sentence contains a mix of uppercThis sentence has repeating characters suchuppercaselots '
  'as "t", "h", and "s". The quick brown fox jumps over the rlazy dog.ase and lowercase letters, '
  'but all characters should be treated as distinct.'],
 ['!"£$%^&*()_+-={squickuchuppercaselots}[]|\\:;"<>,.?/~`'],
 ['This is another sentence with repeating characteers, suc two sentences combined should return '
  '26 distinct foxcharacters.'],
 ['This is twoanother sentence with repeating characteers, such as "t", "h", and "i". The two '
  'sentences bined should return 26 distinct characters.'],
 ['octeheasharvver'],
 ['1This sentstetnce,ence has respeating characters such as "t", "h", and "s". The quick "I!@'],
 ['t"h",eheas'],
 ['"I am a complex sentence, with lots of punctuatsion!" said the fox.'],
 ['This sentence has repeating c"Iasharacters suchlots as "t", "h", and "s". Th1This sentence has '
  'repeating characte ssuch as "t", "h", and "s". The quick brown fox jumps over the rlazy '
  'dog.234$%?!@e quick brown fox jumps over the rlazy dog.'],
 ['The quick brown fox jucomplexmps overThis sentence has repeating chcaracters such as "t", "h", '
  'and "s". The quick brown fox jumps over the rlazy . the  lazy d0'],
 ['sttocteheasharactersvveretnce,'],
 ['punctuation!"'],
 ['should'],
 ['lotsaid'],
 ['!"£$%^&*()_+-={squickuchuppercaselots}[]|]\\:;"<>,.?/~`'],
 ['tehheas'],
 ['The quick brown fox jucomplexmps ovocharactersvverer the  lazy d0'],
 ['"I am a complex sentence, mwith lotsaid the fox.'],
 ['This sentence has repeating c"Iasharacters suchlots as "t", "sttetnce,h", and "s". Th1This '
  'sentence has repeating characte ssuch as "t", "h", and "s". The quick brown fox jumps over the '
  'rlazy dog.234$%?!@e quick brown fox jumps over the rlazy dog.'],
 ['las"IIe'],
 [',sttetnce,'],
 ['""I'],
 ['"sttetnce,h",'],
 ['oThis sentence has repeteheasg.cteheasharvver'],
 ['This is another sentence with repeating charactiers, such as 1234$%?!@"t", "h", and "i". The '
  'two sentences combined should return 26 distinct c haracters.'],
 ['This is another sentence with repeating characters, such as "te", "h", and "i". The two '
  'sentences combined should return 26 distinct characters.'],
 ['the'],
 ['This sentence has repeating characters such as "t", "h", and "s". The quiclowercasever the '
  'rlazy dog.'],
 ['This sentence contains a mix of uppercase and lowercase letters, but all characnters should be '
  'treated as distinct.'],
 ['This sentence has repeatlowercaseumps over the lazy dog.'],
 ['1234$%%?!$!;"£$%^&*()_+-={}[]|\\:;"<>,.?/~`@'],
 ['This sentence has repeating characters such as "t", "h", and "s". The quick brown fox jumps '
  'over the "t",rlazy .'],
 ['Th1This'],
 ['lotd'],
 ['brownn'],
 ['repeatlowercaseumps'],
 ['The quick brown fox jumps over the lasttetnce,zy dog'],
 ['"I am a complex Thissentence, with lotsaid '],
 ['suchuppercaselots'],
 ['lotrneturtnd'],
 ['laocharactersvvezy'],
 ['haracters.mix'],
 ['laoc"IIharactersvvese26"h",nt6encezy'],
 ['charactThisersfs'],
 ['1234$%?!@"t",'],
 ['"""Ichcaracters'],
 ['This sentence has repeating c"Iasharacters suchlots as "t", "sttetnce,h", and "s". Th1This '
  'sentence has repeating cha!@e quick brown fox jumps over the rlazy dog.'],
 ['t"h",e"""Ichcaractersas'],
 ['This is another sentence with repeating characteers, such as "t", "h", and "i". The two '
  't"h",e"""Ichcaractersassentences combined should return 26 distinct characters.'],
 ['punbrownnon!"'],
 ['oc1This sentence has repeating characters such as "t", "h", and "s". The quick "I!@haractersr'],
 ['1234$%%?!!;"£$%^&*()_+-={}[]|\\:;"<>,.?/~`"I am a complex sentence, with lots of punctuatsion!" '
  'said the fox.'],
 ['This sentence has repeating characters such as "t", "h", and "s". The quick brown fox jumps '
  'over the lazy dog.This is twoanoither sentence with repeating characteers, such as "t", "h", '
  'and "i". The two sentences bined should return 26 distinct characters.'],
 ['This sentence has repeating ci"Iasharacters suchlots as "t", "sttetnce,h", and "s". Th1This '
  'sentence has repeating cha!@e quick brown fox jumps over the rlazy dog.'],
 ['"st"tetnce,h",'],
 ['ocharactcersr'],
 ['This sentence has repeating c"Iasharacters suchlots as "t", "h", and "s". Th1This sentence has '
  'repeating characte ssuch as "t", "h", and "s". The quick brown fox jumps over the rlazy '
  'dog.234$%?!@e quick brown fox jumps over thThis sentence has repeatlowercaseumps over the lazy '
  'dog.e rlazy dog.'],
 ['laoc"IIhmixaractersvvese26"h",nt6encezy'],
 ['"I!@'],
 ['"I am a complex senttuatsion!" said the fox.'],
 ['This is anothdistincter sentence with repeating charactiers, such as 1234$%?!@"t", "h", and '
  '"i". The two sentences combined should return 26 distinct characters.'],
 ['!"£$%^&*()_+oc1This-={squickuchuppercts}[]|\\:;"<>,.?/~`'],
 ['"I am a complex sentence, mwith lotsaid the ffox.'],
 ['suchuppercaspelots'],
 ['This sentence has repeatinrg characters such as "t", 26"h", and "s". The quick brow lazy dog.'],
 ['ssucsh'],
 ['oThis'],
 ['!"£$%^&*()_+-={squiThis sentence has repeating c"Iasharacters suchlots as "t", "h", and "s". '
  'Th1This sentence has repeating characte ssuch as "t", "h", and "s". The quick brown fox jumps '
  'over the rlazy dog.234$%?!@e quick brown fox jumps over thThis sentence has repeatlowercaseumps '
  'over the lazy dog.e rlazy dog.ckuchuppercaselots}[]|]\\:;"<>,.?/~`'],
 ['1234$%%?!!;"£$%^&*()_+-={}[]|\\:;"<>,.?/~`"I'],
 ['ci"Iasharacters'],
 [',strespeatingetnce,'],
 ['FDJcjR'],
 ['The quick brown fox jucothe lazy dog. 1234567890'],
 ['"charactiers,I am a complex sentence, with lots of punctuation!" said the fox.'],
 ['"sttetnceThis is another sentence with repeating characteers, suc two sentences combined should '
  'return 26 distinct foxcharacters.,h",'],
 ['This sentence has repeating c"Iasharacters suchlots as "t", "h", and "s". Th1This sentence has '
  'repeating characte is@e quick brown fox jumps over the rlazy dog.'],
 ['suc"!I!@hlots'],
 ['"'],
 ['doge'],
 ['"""Ichc!"£$%^&*()_+-={}[]|\\:;"<>,.?/~`aracters'],
 ['"I am a complex Thissentence,  with lotsaid '],
 ['lasesaid'],
 ['vQ'],
 ['toThis sentence has repeteheasg.cteheasharvver'],
 ['dasaidndog'],
 ['toThis sentence haThis sentence has repeating characters such as "t", "h", and "s". The quick '
  'brown fox jumps over the lazy dog.This is twoanoither sentence with repeating characteers, such '
  'as "t", "h", and "i". The two sentences bined should return 26 distinct characters.s '
  'repeteheasg.cteheasharvver'],
 ['doge,sttetnce,,'],
 ['This is another sentence with repeating characters, such as "te", "h", and "i". The two '
  'sttocteheasharactersvveretnce,sentences combined should return 26 distinct characters.'],
 ['haThis'],
 ['The quick brown fox jumps over the lasttetnce,zy dogmix'],
 ['suchuppercasspelots'],
 ['las'],
 ['uupperucase'],
 ['brownThe quick brown fox jumps over the lasttetnce,zy dogn'],
 ['d0'],
 ['This sentence contaof uppercase and lowercase letters, but all characters should be trearted as '
  'dogedistinct.'],
 ['This sentence has repeatinrg char1This sentence has repeating characte ssuch "Ias "t", "h", and '
  '"s". The quick brown fox jumps over the rlazy dog.234$%?!@quick brow lazy dog.'],
 ['haThisstetnce,'],
 ['p"u!!"'],
 ['haracters.'],
 ['This sentence contains a mix of uppercase and lowercase letters, but all characters  treated as '
  'distinct.'],
 ['characters.s'],
 ['liasesaid'],
 ['p"u"!!"'],
 ['1oThis234$%?!@"t",'],
 ['ssuch1234$%%?!$!;"£$%^&*()_+-={}[]|\\:;"<>,.?/~`@'],
 ['t"h",e"""IchcaractersassentencesThis'],
 ['jucompplexmps'],
 ['!"£$%^&*()_+-={squickuchuppercaselohts}[]|]\\:;"<>,.?/~`'],
 ['Thi"Iass sentence has repeatlowercaseumps ovier the lazy dog.'],
 ['0d0'],
 ['ocharactcersrrlazy'],
 ['This sentence has repeating characters sThis is another sentence with repeating charactiers, '
  'such as 1234$%?!@"t", "h", and "i". The two sentences combined should return 26 distinct c '
  'haracters.ch as "t", "h", and "s". The quick brown fox jumps over tehe rlazy dog.'],
 ['"s.",'],
 ['Thee og. 1234567890'],
 ['"s".This is another sentence with repeating charactiers, such as 1234$%?!@"t", "h", and "i". '
  'The two sentences combined should return 26 distinct c haracters.'],
 ['This is anothdistincter sentence with repeating charactiers, such as 1234$%?!@"t", "h", .and '
  '"i". The two sentences combined should return 26 distinct characters.'],
 ['charactThiseThis is another sentence with repeating characters, such as "te", "h", and "i". The '
  'two sentences combined should return 26 distinct characters.rsfs'],
 ['"Ias'],
 ['rlazyeturn'],
 ['"s..",'],
 ['This sentence has repeating characters such as "t", "h", "and "s". The quick brown fox jumps '
  'over the lazy dog.'],
 ['sentencesall'],
 ['"charactiers,I am a uupperucaseon!" said the fox.'],
 ['respeating'],
 ['oThiTs'],
 ['The qu 1234567890'],
 ['octeheashrarvver'],
 ['This sentence has repeating c"Iasharacters suchlots as "t", "h", and "s". Th1This sentence has '
  'repeating characte is@e quick brown fox j rlazy dog.'],
 ['oc1This'],
 ['This sentence has repcontainseating characters such as "t", "h", and "s". The quick brown fox '
  'jumps over the "t",rlazy .'],
 ['ocharactce1oThis234$%?!@"t",rsrrlazy0d0'],
 ['dog.ckuchuppercaselots}[]|]\\:;"<>,.?/~`'],
 ['anotheThis sentence has repeating characters suchlots as "t", "h", asaidnd "s". The quick brown '
  'fox jumps over the rlazy dog.r'],
 ['haracters.ch'],
 ['laocharactesvvezy'],
 ['"Iaas'],
 ['The quick brown fox jucomplexmps overThis sentence havs repeating chcaracters such as "t", "h", '
  'and "s". The quick brown fox jumps over the rlazy . the  lazy d0'],
 ['The quick brown fs over the lazy dog. 1234567890This sentence has repeating characters suchlots '
  'as "t", "h", and "s". The quick brown fox jumps over the rlazy dog.'],
 ['Thee og. 41234567890'],
 ['ocharaactersvve'],
 ['Th1Ths'],
 ['alll'],
 ['sttee,'],
 ['stnetnce,'],
 ['ffox.'],
 ['t"h",e"""Ichcaractersassentences'],
 ['This sentence has repeating characters suchlots as "t", "h", and "s". The quick brown fox jumps '
  'over the rlazyog.'],
 ['!"£$%^&*()_+-={squiThis sentence has repeating c"Iasharacters suchlots as "t", "h", and "s". '
  'Th1This sentence has repeating characte ssuch as "t", "h", and "s". The quick brown foshouldx '
  'jumps over the rlazy dog.234$%?!@e quick brown fox jumps over thThis sentence has '
  'repeatlowercaseumps over the lazy dog.e rlazy dog.ckuchuppercaselots}[]|]\\:;"<>,.?/~`'],
 ['rownn'],
 ['sttocte"heasharactersvveretncet,'],
 ['This is another se26"h",nt6ence with repeating characse26"h",nt6encetences combined should '
  'return 26 distinct characters.'],
 ['ocharacersvver'],
 ['1234$%%%?!3@'],
 ['is@e'],
 ['ocactersr'],
 ['rlazyetuurn'],
 ['pu!p!foxcharacters."'],
 ['"ee"'],
 ['ocharactcersrrlaz1This sentstetnce,ence has respeating characters such as "t", "h", and "s". '
  'The quick "I!@'],
 ['Th1Thi1s'],
 ['This is another se26"h",nt6ence with repeating characse26"h",nt6encetences combined should '
  'retusentencern 26 distinct characters.'],
 ['1Thi1s'],
 ['"I am a complex sentence, with lo tsaid '],
 ['"s..,",'],
 ['a1This sentstetnce,ence has respeating characters such as "t", "h", and "s". The quick "I!@'],
 ['"charactiers,I'],
 ['Thisci"Iasharacters sentence has repeating c"Iasharacters suchlots as "t", "h", and "s". '
  'Th1This sentence has repeating characte ssuch as "t", "h", and "s". The quick brown fox jumps '
  'over the rlazy dog.234$%?!@e quick brown fox jumps over thThis sentence has repeatlowercaseumps '
  'over the lazy dog.e rlazy dog.'],
 ['laochThis sentence has repeating characters such as "t", "h", and "s". The quick brown fox '
  'jumps over tehe rlazy dog.aractersvvezy'],
 ['1This sentence has repeating charters such as "t", "h", and "s". The quick "I!@'],
 ['octeheasharacThistersvver'],
 ['octeheasharacterchcaracterssvver'],
 ['1This'],
 ['This sentence has repeating characters such as "t", "h", and "s". The quick brown fox jumps '
  'over the rlazy.'],
 ['1234$%%?!!;"£$%^&*()_+-={}[]|\\:;"<>,?/~`"I'],
 ['1234$%%?!!;"£$%^&*()_+-={}[]|\\:;"<>,.?/This is another sentence with repeating characteers, '
  'such as "t", "h", and "i". The two t"h",e"""Ichcaractersassentences combined should return 26 '
  'distinct characters.~`@'],
 ['This ies another sentence with repeating characteers, suc two sentences combined should return '
  '26 distinct foxcharacters.'],
 ['122394567890'],
 ['This is twoanother sentence with repeating characteers, such as "t", "h", and "i". The twoThe '
  'quick brown fox jumps over the lasttetnce,zy dog sentences bined should return 26 distinct '
  'characters.'],
 ['"charactiaers,I am a uupperucaseon!" said the fox.'],
 ['laochThis senetence has repeating characters such as "t", "h", and "s". The quick brown fox '
  'jumps over tehe rlazy dog.aractersvvezy'],
 ['"This sentence has repeating characters such as "t", "h", and "s". The quick brown fox jumps '
  'over the "t",rlazy .Iaas'],
 ['This sentence has repeating characters such as "t", "h", and "s". '
  'Th!"£$%^&*()_+-={suchuppercaselots}[]|\\:;"<>,.?/~`quick brown fox jumps over the rlazy.'],
 ['This is another sentence with repeating characters, such as "te", "h", and "i". The two '
  'sttocteheasharactersvveretnce,sces combined should return 26 distinct characters.'],
 ['The quick brown fox jumps over the lasttetnce,suchzy dogmix'],
 ['1234$charactThisersfs%%?!$!;"£$%^&*()_+-={}[]|\\:;"<>,.?/~`@'],
 ['"This sentence has repeating characters such as "t", "h", and "s". The quick brown fox "jumps '
  'over the "t",rlazy .Iaas'],
 ['26"h",'],
 ['p"u!!"laocharactesvvezy'],
 ['octeThis sentence contains a mix of uppercase and lowercase letters, but all characnters should '
  'be treated as distinct.heasharactersvver'],
 ['retrtn'],
 ['This is anothdistinctercharacters.rsfs sentence with repeating charactiers, such as '
  '1234$%?!@"t", "h", .and "i". The two sentences combined should return 26 distinct characters.'],
 ['"In am a complex sentence, with lotsaid the fox.'],
 ['ci"Iasharaacters'],
 ['t"h",e"""Ichcaractersassentencesog.This'],
 ['dThis is another sentence with repeating characteers, such as "t", "h", and "i". The two '
  't"h",e"""Ichcaractersassentences combined should return 26 distinct characters.og'],
 ['!"£$%^&*()_+-c={squickuchuppercaselots}[]|]\\:;"<>,This ies another sentence with repeating '
  'characteers, suc two sentences combined should return 26 distinct foxcharacters..?/~`'],
 ['The brownnzy dog. 1234567890'],
 ['This is another sentence bined should return 26 distinct characters.'],
 ['"In am a complex sentence, waith lotsaid the fox.'],
 ['1Thi1'],
 ['This sentence has repeating characters such as "t", "h", and "s". The quiclowercever the rlazy '
  'dog.'],
 ['The'],
 ['ste'],
 ['distinct.heasharactersvver'],
 ['p"u!!"laocharThis is anothdistincter sentence with repeating charactiers, such as 1234$%?!@"t", '
  '"h", .and "i". The two sentences combined should return 26 distinct characters.actesvvezy'],
 ['is@ee'],
 ['dogtrearted'],
 ['EQJmbBXT'],
 ['tehe'],
 ['"t",rlazy'],
 [',sufoxcharacters.,h",chuppercaspelots'],
 ['foshoulThis is another sentence with repeating characters, such as "te", "h", and "i". The two '
  'sttocteheasharactersvveretnce,sces combined should return 26 distinct '
  'characters.dxocharactcersr'],
 ['retetn'],
 ['punctuatsioncharacters.!"'],
 ['dog.uick'],
 ['ssuchh'],
 ['aThee og. 1234567890llll'],
 ['characteers,'],
 ['dotehheasg.ckuchuppercaselots}[]|]\\:;"<>,.?/~`'],
 ['tocharacters.rsfss'],
 ['pneocharactersvveumonoultramicroscopicsilicovolcanocs'],
 ['lastztetnce,zy'],
 ['."s..,"",'],
 ['122394567be890'],
 ['The qu 1234567890.'],
 ['uuupperucase'],
 ['t"hracoters.og",e"""Ichcaractersas'],
 ['retetnliasesaid'],
 ['"s'],
 ['twoaThe quick brown fox jumps over the lasttetnce,suchzy dogmixnoither'],
 ['"In am  a complex sentence, waith lotsaid the fox.'],
 ['aThe1e og. 1234567890laochThis sentence has repeating characters such as "t", "h", and "s". The '
  'quick brown fox jumps over tehe rlazy dog.aractersvvezyllll'],
 ['jucomplex!"£$%^&*()_+-={squickuchuppercaselohts}This is another sentence with repeating '
  'characteers, suc two sentences combined should return 26 distinct '
  'foxcharacters.[]|]\\:;"<>,.?/~`mps'],
 ['anotheThis sentence has repeating characters suchlots as "t", "h", asaidnd "s"anotheThis '
  'sentence has repeating characters suchlots as "t", "h", asaidnd "s". The quick brown fox jumps '
  'over the rlazy dog.r. The quick brown fox jumps over the rlazy dog.r'],
 ['p"u!!"haracters.chlaochara1234$%%?!!;"£$%^&*()_+-={}[]|\\:;"<>,.?/This is another sentence with '
  'repeating characteers, such as "t", "h", and "i". The two t"hnces combined should return 26 '
  'distinct characters.~`@zy'],
 ['!"£$%^&*()_+-={}p"u!!"[]|\\:;"<>,.?/~`'],
 ['The quick brown fox juco7890'],
 ['p"u!!"haracters.chlaochara121234$%%?!$!;"£$%^&*()_+-={}[]|\\:;"<>,.?/~`@", "h", and "i". The '
  'two t"hnces combined should return 26 distinct characters.~`@zy'],
 ['senntencesa'],
 ['repeteheasg.cteheasharvver'],
 ['doge,stotetnce,,'],
 ['al1iThi1l'],
 ['octeheashrarvverdog.lastztetnce,zye'],
 ['charactThiseThis is another sentence with repeating characters, such as "te", "h", and "i". The '
  'two sentences combined should return 26 distinct characcters.rsfs'],
 ['lasttetnce,zy'],
 ['This is a sentence with repeating characters, such as "s.", "e", atnd "n".'],
 ['pneocharactersvveumonoultramicroscopicsilrepcontainseatingicovolcanocs'],
 ['122394567be8The quick brown fox juco789090'],
 ['122394trearted90'],
 ['!"£$%^&*()_+oc1This-={squ1234$charactThisersfs%%?!$!;"£$%^&*()_+-={}[]|\\:;"<>,.?/~`@ickuchuppercts}[]|\\:;"<>,.?/~`'],
 ['Thisdistinct. sentence has repeatlowercaseumps over the lazy dog.'],
 ['This sentence has repeating characters suchlots as "t", "h", anhd "s". The quick brown fox '
  'jumps over the rlazy dog.'],
 ['Thpis sentence has repeating characters such as "t", "h", and "s". The quick brown fox jumps '
  'ovechar1Thisr the rlazy .'],
 ['conjumpstaof'],
 ['Thpis sentence has repeating characters such as "t", "h", and "s". The '
  't"hracoters.og",e"""Ichcaractersasechar1Thisr anothdistinctercharacters.rsfsthe rlazy .'],
 ['suchs'],
 ['"""This is anothdistinctercharacters.rsfs sentence with repeating charactiers, such as '
  '1234$%?!@"t", "h", .and "i". The two sentences combined should return 26 distinct '
  'characters.Ichc!"£$%^&*()_+-={}[]|\\:;"<>,.?/~`aracters'],
 ['jucomplex!"£$%^&*()_+-={squickuchuppercaselohts}This is another sentence with repeating '
  'characteers, suc two sentences combined should returnm 26 distinct foxchara\\:;"<>,.?/~`mps'],
 ['chcaracters'],
 ['"s"".'],
 ['laThis sentence has repeating characters such as "t", "h", and "s". The quick brown fox jumps '
  'over the rlazy.sesaid'],
 ['punctuatsionchara"cta"'],
 ['characters..s'],
 ['ocharactervQr'],
 ['dotrearted'],
 ['twoThe'],
 [',sttetcnce,'],
 ['charactTrhiserslofs'],
 ['anotheThis sentence has repeating characters suchlots as "t", "h", asaidnd "s". The quick brown '
  'fox jumps over the rlazy do.r'],
 ['ojucomplexmpsc1This'],
 ['This setwoaThech as "t", "h", "and "s". The quick brown fox jumps overthe the lazy dog.'],
 ['This is another sentence binequickturn ."s..,"",26 distinct characters.'],
 ['This sentence has repeating characters suchlots as "t", "h", and "s". The quick brown fox jumps '
  'over the rlazy dog'],
 ['jucompp'],
 ['1234$%%?!!;"£$%^&*()_+-={}[]|\\:;"<>,.?/~`"I am a comt"h",e"""Ichcaractersassentences said the '
  'fox.'],
 ['ihaThis'],
 ['rlazy.'],
 ['1This sentenc", and "s". The quick "I!@'],
 ['repet"sttetnceThisasharvver'],
 ['!"£$%^&*()_+-={squickuchuppercaselshouldots}[]|]\\:;"<>,.?/~`'],
 ['26""h",'],
 ['punctuatscionchara"cta"'],
 ['!"£$%^&*()_+-={squickuchuppercaselshouldots}[]|]\\:;"</~`'],
 ['charactThiseThis is another sentence with repeatingpunctuatsioncharacters.!"ters, such as "te", '
  '"h", and "i". The two sentences combined should return 26 distinct characcters.rsfs'],
 ['ovioevr'],
 ['oschararctersvver'],
 ['"s".'],
 ['1This sentence has repeating characters such as "t", "h", and "s". The quick "aI!@'],
 ['se'],
 ['characteerse,'],
 ['foxcharacters.'],
 ['do.r'],
 ['"I afoshouldxm a complex sentence, with lots of punctuatsison!" said the fox.'],
 ['""s"is"".'],
 ['r"epeatingpunctuatsioncharacters.!"ters,'],
 ['doge,tsttetnce,,'],
 ['twoanoither'],
 ['This is twoanother sentence with repeating characteers, such as "t", "h", aocharactervQrnd "i". '
  'The two sentences bined should return 26 dibutstinct characters.'],
 ['"sanother"".'],
 ['1234$%%?!!;"£$%^&*()_+-={}[]|\\:;"<>,.?/~`"I am a comt"h",e"""Ichcaracterces said the x.'],
 ['Thisdistinct.'],
 ['The quick bro"hsentence",wn fox jumps over the lasttetnce,zy tdogmix'],
 ['!"£$%^&*()_+oc1This-={squ1234$charactThisersfs%%?!$!;"£{$%^&*()_+-={}[]|\\:;"<>,.?/~`@ickuchuppercts}[]|\\:;"<>,.?/~`'],
 ['sentstetnce,ence'],
 ['!"£$%^&*()_+-={squiThis sentence has repeating c"Iasharacters suchlots as "t", "h", ande "s". '
  'Th1This sentence has repeating characte ssuch as "t", "h", and "s". The quick brown fox jumps '
  'over the rlazy dog.234$%?!@e quick brown fox jumps over thThis sentence has repeatlowercaseumps '
  'over the lazy dog.e rlazy dog.ckuchuppercaselots}[]|]\\:;"<>,.?/~`'],
 ['Thisdistinct.oc1This sentence has repeating characters such as "t", "h", and "s". The quick '
  '"I!@haractersr'],
 ['binequickturn'],
 ['sttocteheasharactersvveretnce,sces'],
 ['This sentence has repeating characters such as "t", "h", aand "s". '
  'Th!"£$%^&*()_"aI!@+-={suchuppercaselots}[]|\\:;"<>,.?/~`quick brown fox jumps over the rlazy.'],
 ['This is anothdistinctercharacters.rsfs sentence with renpeating charactiers, such as '
  '1234$%?!@"t", "h", .and "i". The two sentences combined should return 26 distinct characters.'],
 ['dog.This'],
 ['charters'],
 ['This sentence has repeating c"Iashcharactearacters suchlots as "t", "h", and "s". Th1This '
  'sentence has repeating characte is@e quick brown fox jumps over the rlazy dog.'],
 ['jucomThis sentence has repeating characters such as "t", 26"h", and "s". The quick brown fox '
  'jumps over the lazy dog.pplexmps'],
 ['haracrenpeatingters.ch'],
 ['esttee,'],
 ['This sentence has"s repeating characters such as "t", "h", and "s". The quick brown fox jumps '
  'over the rlazy.'],
 ['""s'],
 ['two'],
 ['hasucracters.'],
 ['sentsteisne'],
 ['""charactiers,I am a complex sentence, with lots of punctuation!" said the fox.I'],
 ['foshoulThis is another sentence with repeating characters, such as "te", "h", and '
  '"i".doge,tsttetnce,, The two sttocteheasharactersvveretnce,sces combined should return 26 '
  'distinct characters.dxocharactcersr'],
 ['afoshouldxm'],
 ['ocharactce1oThis234$%?!@"t",rsrr"lazy0d0'],
 ['"e""'],
 ['This sThis sentence has repeatlowercaseumps over the lazy dog.entence has repeating characters '
  'suchlots as "t", "h", and "s". The quick brown fox jumps over the rlazy dog.'],
 ['st1234$%%?!$!;"£$%^&*()_+-={}[]|\\:;"<>,.?/~`@netnce,'],
 ['"In am  a compelex sente1This sentence has repeating characters such as "t", "h", and "s". The '
  'quick "I!@nce, waith lotsaid the fox.'],
 ['.and'],
 ['p"u!!"haracters.chlaochara1234$%%?!!;"£$%^&*()_+-={}[]|\\:;"<>,.?/This is another sentence with '
  'repeating characteers, such as "t", "h", and "i". The two t"hnces combined sharacters.chhould '
  'return 26 distinct characters.~`@zy']]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-q}vJ<@Hrjg*5K@4#ztG(`d=0A}9E1pF=Mvw?{wQYdf8D{~)}tXY6MKs^PL-uJ$HE)M}T8Xy4v?|=N`&p-'
    b'X?r|+Nt{^hSf|L6bweM+}qe*Rl+(fV0c+bJVfYkm8?^%WUQOA%46b?Ux%?P6usIP>Z$Jywxj-'
    b'Y@_6%isU>^WVnw+SJ|qZsp7|yy=qb<;YNL$F}O2rmxjghiR+6hxazmX@;e6AJf`hr>@thzjC77Ii9u{WtDT=KCSoCs_s~86!TK+?'
    b'(3Ft!A5u?ujWWy`-b#s*7jI-b-nha*YbLl+7A}d@f7@>?$&lWuaCK`Utj9ux5t=`(c+yd_=etEleV9<+V3uXbo_9H-'
    b'MIxKdU{1~_<pUgrN=z<x5t#@{k&0T-'
    b'(y1PF;>O4ybFoqW98W$YZ*4L&idAFujo2{_I5n14)ROQw)EE0yS+UhR`K3mV?@J8=ZhJ0j#c{dfj75z?cf`%+a8c=%-'
    b'<fPeI9@KJ?&TGLHNCl{X%pct9tIeK4rcE5lO)h>XSF?QVoc)&ENH=%ATWP6ACr}B3_E+bcp_}2PJ}<)PXgWHgA*NL|+6{XV^RE74'
    b'Bp99r*0H^HbI{C!}@pR#s~~o%NK34O8jIrVY7K@%sf^@2feqqH$M4k`&FtGi|YrIkY_JwOVYO!#0*TM&EZ<+qY|tea?yqozd}vvb'
    b'Vm{n{KG6bGMjfQ}Qi+mNEA<pnV_j0{>k;sl|}8057-CrS)C!&q7B#Lv%s9uP^Run)ng-t>wOr-'
    b'+?;ZfQ27uLhJ9sBPpJJUc7!H<}vXKU4yxo_J)xm{iw*5yZfBBuuKi0@4PqQO`(<sobGFM8Lg`x1&j{pPc87Y<+OjRU%|ctF?*kQD'
    b'~%X+>^Q!G;8iTn7&FEVK)o(Ja?a;as;Ky`y<%Uo-f*;-'
    b'gvBKFBMF?f#T*~bGEI)a2cG&G7(#KoAdKIVW?*?fniu>Xh*ov*NGVgXgi*JBX1OQ$SGD@@m#W_9ejfJfeh^!?^8EqKGwzAzA9{Ov'
    b'^=#-4tfk!sM(1EH;2J|xVll}WSYDF@qNJB1Z86>e0vrXjcH=kttpbd_%bM*i>)HtIrz-FhINN~QSYdC&FLr0OL#B|NEharCmlo&Z'
    b'HzXgP>!sWkz<Fd1glo^FnOuP9Q3D+Yn9eqB+dcTA*i%dZem%~*@IU}Ta#)5B3lP7KD)*Td*r!>Y4@v|r2|WMwyJ`cvBNl(>Gvd9i'
    b'2i~IZS5wj?QUINcZL#o%^ispV?*xs&ruFY%cd1#^5eHG(*19*o{Np(T0^cS4NwI5!N7wqeISR$<_e5A(nw|FW;W|oz6P_L036<{K'
    b'8=%BLSNlD7jQWO$ix;(LDdTX`YLZ1T$pRsY-jFODLcls4CW6SLi&@kS39CR_@qIqT5n^<OPqYWivNZwRcIL&G|3AGZF$xmd&y`%@'
    b'1VSYB%S9n`*;FpQNtX9ZWtzFvk3}IlUNe{aeJl**eVhvqQ|Bt!w=Dx!+V|`iv^j<$azfPoM7mx`p)~{ma5vy-oeUJ56d5aj!|@Cx'
    b'(uS?khTprY&%D<?;=KjExZ*P!H1L+ztPY5-'
    b'R6p1_#kZ~Zj%k$5WfUxWy+GZ^YkIXHIGg${9n`<#{oi|IBE+>~I)Gv|+|=dySqMB;CbX6-'
    b'Dbn7M4zfvsP!*_j@e<{2Z2$_qv)~o0t}jJ`psc&dnynvf|L#!3rrjVrSbqF&;de<rr$gcpd%+7t8wQ-'
    b'i3&6Nuc<YW&!f@4ed)#Z+706d$a`-ZCF8v(|1*|kk#Ib-1@B$R-+HM7o(9CrJ1-dU7yG#dwwQ3M<z+!q%Nj*HV-'
    b';SVpIJC3X)72JG7a)dTm8L6zsI3ACVHl#@%B&r`v)irj_nav7`bv-f+{-~=9dF#V#ILPo-'
    b'd5db03f#25Xd3~i*2u+w?ALw<TDtKz)4<{baYJ0LXzAaDYwNsR_6$uWK$$9X64dT?F|V;Nsl4H7D-'
    b'Yhw&j2UnX^P~;~Yr7eRX&T<^)CzFT6q8<LW%{ylri{SYtgtpo377w{l`JhqUE7WhJQ}X>UlxBp2SW(m<(RDwo$}MKB~S-'
    b'r!!deY|Kwi>D8`iro}M7er{|{m0b+)Y%g#u&-'
    b'J@R>P`&gYH$f^PL}?0;gIN|2Mw^>F$uMuL8L63Y54&fj#zTPoSC|Y!hTjCicN^%9mn!O%nQX_J(9rBw|8Z4QY#65ex_YSb-'
    b'2{Z%8=`Qo@d9;hfAqX^UC4kQ^$&ss>8sd`U3_NpDC%L8|v7Ihb6@g<OqKq{p!OU^sa{5)~lr4XYT96bO+(lv6fH%8BL*%R*Nis7b'
    b'%^t*2mzqIOV<i%4YPIoL{{I(+V3p{5J_17u%T0=xc%YYe#ro~uWQ1Qa9-C!K4O1Wt0kEU(E~4M|e0ir!p_7f#GTQa_S0umWhjje-'
    b'q2NHfq*Rs`_S9B|Oj#0JEMWGDVY5xkst@FX~^?x31q1vJ@Dk*dg2rGZFZlLYB35alEna-BevYD|(bQI0W?$_7b5L25N3W!iG(L`h'
    b'^nSGg%EDMiYdkURsc{EL)LVr3yI=TodH2OM6U>p+s#XvqNzR%IqBwaVGzT-89VAh9cy;A(}!1LHcpO8@-'
    b'KJ{K|GHd%h#p7<el7z<XIt=j;t(>la8<rxe~{T{qK-Uc2XhykAXYa9$IKX6yPKb%}(hZcV8)B_``_&WzsfTh2>gsgta^d=REl4w$'
    b'{6KGNd!-'
    b'6eN8i>_u#ECUYaX4vjayb~1h3E29@4zPK5&vS6dH0Nm&%d!1E@GSCUB}a*(1edrUPF*q@nrWI5E(h~Lh@6j^Ke!iPCDc#&6G-'
    b'YlE@n9m@1c^Yn~`65Mq_arOHC)DjQ@S<&gTrIjL0=`jPgA6+m+ivPq1BwZ*BhIM*OhR^&?>>O*3p97*Mx(VMH@FIQ6-'
    b't4ul9%uJ3=kpiJy=|h^=%rr=XHIE`y152*v9uiGrc}>zuB4;(M&e|W53a|zqkvdOO4a#DT3FMSxu$sb1sSZ*Z4`(bXt0|15ex%jp'
    b'>St*CLN9=;XYTTCfWjx@x92PSL~r;*S<odFkYax@F!fV(k1HF9b5eGX(vB<MkcL-*^YIJbC^`Xl8va$2P6S5-'
    b'`#lPN@I|&@roOvXh^jn?Cb4-'
    b'j=cPD#KT<rEt7C~}Q>lO=+0ik_`Tmf4ldFm>*V!G37Z(Q&iMayLYtLRY?Ff_1%dS3Ff3lX>uj5mqB5p0V3&L!Z;p0Qhlm(t7o66P'
    b'L&6?9jN(1Fe*pcoL;^c2~jlyFk7jj+5!LcdQ;9(N?V@*>|bskPi*pWKjSjDfYhQO1yI9dHoswNGR`mrt?OLYd5>$cBiXTG_n9FXc'
    b'LI4Lqx`4`C;a;3;fTAV9mLW(t$%|7JB3@n;N>c}RYhm)qp<vKhe?F}iMPt~MB0?}OOnyjQ0$1{-'
    b'nU~=U|b4`sS1wy%;Z>}5WSUC#P;Rz=V#JVG!0~93FB(d~dmEfe8$~Ar|*WTnxf|E!a3DQYEJlW{YRF`Uz;wh4(a-'
    b'kn7V?qK7+Sy&IrgzTiJgKCT)v=W742HzESX6)mqPeDHuwaXHZ61fEld_O3*h-'
    b'b#Vnr~dyK*>bAlB44(%fs#YKnr40PM#t3oGcm|B5dHI0h`8&*w}yE%1;Pt99vk81P8|Odve>rK~<At%d|!v}rt)(1SI-Jyo~*4;c'
    b'tmu(WUCil}#B?_iuhZ+%5z(WSswX#K`2-n(`ITw_t6eu7`XrS0;#mp|s3QkiR*H|w|}*L6g>`lmQPoKygjD}R&BG&xL^6>E|X-'
    b'8e~bQh9r>L$_Q9lDV#T%{BjqHc>CtOes=FHpesMnqN%Xn_MAlvLtw_ZZ49AC+k?^U@@z^B2^m}>yV!`oF!Fn87XEUF;P~{K1pv<b'
    b'*qyu4JAb|q}7PnXHpA0gb&;U6Z$-WN%K-'
    b'Fv}$`9X79<7YxV^L4ci$|<5xj|xvL=^y5+hykCfZWRq?{oV$#tuCuC(6F>=oCSXVW1R+B3$Kr#l_T{*0ITZl;)%*tR8*rd<5$;Tz'
    b'v)Me#twerHSGuGPz34d6=`#JK!%GcyVdaj%(iC&Y8f%F*KP45&fCXL>tT@6PuhFn+Q(s~j({DxE20e*wmIPm1Ir<c!VAAHfL0D%x'
    b'8rr{xYXDCy}mg@0OL9fXJxdFxDYB8y1Ki6d?EG9}K`=pDbSj~hS?nf$dVqG{!xtTCm4J}DhBrVQ$|5PqQODY>AP2(XE6V_lp4p6W'
    b'L<dd#w=MdUlw^HZ2DU4MMNvh~2b&qnQJJ#h$q}E0f*-'
    b'tgpC)YuCE+)#FB~Q9?hXd)X9%v2|&6S}g5n9%2Qk6KdDl=2{2$8lp*Tk70azH+*Co$QD9Jww>;<VF{d^kzqxta-'
    b'CvsP10jU%mwmA`SYU=S0v;ovQhR>wlHnO6calfV_nfMc#P1ZFC_t<2hC-MiiTPRf>8)@fNPep4K~Yg=rUcNKw8D_hr>B)b3`NDJZ'
    b'v1=m&Y!GGr24n)GjuACZmq|Awu1WudcL^&-ZIT%tI59=VCbw@U(#EE2@q@to+m-w-Igi=+4(<<yZ6q1vYr^VrvkTq8&c&-'
    b'tOB%2~NKCv>ism?WX4J~9PdQ<g4vo0JX)orCZpJE-'
    b'>a=0Js4gwOSr>X`bbytuW1uYJzFbdY7tRJ!Bg~TXWQ&m!3aG0ynGMB(vg~1#PC#{C`m|O=-B)lQj-;lf}tIa$Wq|>fWNp-'
    b'7Hs!2t(B1THunbmbnI%VY?NamWt%~C(o?88*!C0UoEr^@@WDy2wSNYW)Yq(e7O8i+NLK2`T<uD!_>2(kL7I46nf{Zn&5M}q*ymrd'
    b'v&(1L&*1q}h<y|TOR3Hty@F2tA+E7mil_g1;EMG`nEV?v6<bH!6yz@s4D5d&IZzXAoYhPby@7)1FFQS3YE{f_C6H-'
    b'Km>v7i;(Ko3i>vq_Z0lUx_Z=gOFn^2Mx1OHLITYdQw&_B~E-'
    b'8L3~B1L?WCM{`x!<?3f(4H4r+zNGT6T(Kr=$OcDJxo*<PRSU_w*MpRHCbgM!=82MCD%pr3j=))CkW*zLSr<5yDy2AM0&`spOp0Jg'
    b'{DyQQR35fLV}hE4<uq__tR7Z>*J<z&Qm<6`F8bQq+m}p=amI3ilkn~yDMQv=Spm`(vzp#nwbz;ECXvuDS8glW{9@8=Sbtpo{_)Sh'
    b'{PgQT-'
    b'}B~L0fvK3DE6Hn0&^9}eh+>GVV#g2ZNlw9=hjz<uU6`9pgsZ|kjG79lVC8{(2itjB@UVnm#TWZV4njqnD+`ZI!oY6v8~>918J~l<'
    b'N1OeYkar`()~$5W=k0@vb=Dr+4RXK^rf0!n5(>llpH0kCfAt`N#HDZmr9FCIS*Dn&%S_c5V|vW`F>XcN-'
    b'&%+m3{(2WI?zGnAcxj$^+|BKSlSrvf&v{%1I=oiJ+u5QkMF0JOj!3k|<=Z;Zm&eDya%_a`ld|_)V&AR8k0BN5E(38VAnRzG){7*x'
    b'NuIT-vFKYA4t=LV+m|z!!Hw%m<Q%TPS!_a*CgGMIp(DlbkQ9CYLn`hod*FUNs2s6j?1090F`%Mo^6_aDa2-'
    b'+uyBUwMmNukg%g=hQm7Wi8HpZlX9L;t|ofYV{$cp(8m8~x*s@KZ6yhBNLfu1Y|*AO|6#qkf6aISK&m_I{`gVV{jYxk2}f&k'
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
    candidate = count_distinct_characters  # noqa: F405
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
