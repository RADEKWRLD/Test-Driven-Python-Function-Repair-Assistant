import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [['This is a test'],
 ['lets go for swimming'],
 ['there is no place available here'],
 ['Hi I am Hussein'],
 ['go for it'],
 ['here'],
 ['here is'],
 ['cats and dogs'],
 ['I am a developer'],
 ['elephants are huge'],
 ['the quick brown fox jumps over the lazy dog'],
 ['this code challenge is tricky'],
 ['Python programming is fun'],
 ['mathematics can be easy'],
 ['writing clean code is important'],
 ['I love eating pizza'],
 ['quick sort algorithm is efficient'],
 ['I am a dquick sort algorithm is efficienteveloper'],
 ['mathematics can be eacsy'],
 ['eleephants are huge'],
 ['Python programmingg is fun'],
 ['this code schallenge is tricky'],
 ['this code mathematics can be eacsychalleI love eating pizzangge is tricky'],
 ['I athe quick brown fox jumps over the lazy dogm a developer'],
 ['Io love eaI love eating pizzaquick sort algorithm is efficientting pizza'],
 ['this acode mathematics can be eacsychalleI love eating pizzangge is tricky'],
 ['Io love eaI love eating pizort algorithm is efficientting pizza'],
 ['I athe qurown fox jumps over the lazy dogm a developer'],
 ['quick sort algoritI love eating pizzahm is efficient'],
 ['this code challenge is triycky'],
 ['I am a dquick sort algorithm isp efficientevelope r'],
 ['eleepnhantselephanpts are huge are huge'],
 ['I am a deper'],
 ['Pyththe quick brown fox jumps over the lazy dogon programming is fun'],
 ['this code schayllenge is tricky'],
 ['thse quick brown fox jumps over the lazy dog'],
 ['I am a dquick sort algorithm is efficientthis code challenge is triyqckyeveloper'],
 ['quick soithm is efficient'],
 ['eleepnhantselepmathematics can be easyhanpts are huge are huge'],
 ['quick sort algoritI love eaating pizzahm is efficient'],
 ['elephants are hugeIo love eaI love eating pizort algorithm is efficientting pizza'],
 ['this code schayllI am a dquick sort algorithm is efficienteveloperenge is tricky'],
 ['quick sort algorithm iselephants are hugeIo love eaI love eating pizort icient'],
 ['thse q the lazy dog'],
 ['I am a deveoper'],
 ['I athe qurown fox jumps over the lazy dogm a developethse q the lazy dog'],
 ['this code e is tricky'],
 ['mahthematics can be easy'],
 ['I athe quick brown fox jumpthis code e is trickys over the lazy dogm a ddeveloper'],
 ['Io love eaI love eting pizort algorithm is efficientting pizza'],
 ['I am a deveopthis code mathematics can be eacsychalleI love eating pizzangge is trickyer'],
 ['I am ad deveoper'],
 ['mahthematics can be e asy'],
 ['Pythothis code mathematics can be eacsychalleI love eating pizzangge is trickyprogrammingg is '
  'fun'],
 ['quick soithmc ihs efficient'],
 ['I Io love eaI love eating pizort aligorithm is effIicientting pizzaeloper'],
 ['I am a dquick sort algorithm is efficienteveloperr'],
 ['I am a dquick sort algorithm is efficienttehis code challenge is triyqckyeveloper'],
 ['quick sort algoritI love eating pizzahm ist'],
 ['mahthematics can bI athe qurown fox jumps over the lazy dogm a developethse q the lazy dog asy'],
 ['Pyththe quick brown fox jumps over the lazy dogon proeleephants are hugegramming is fun'],
 ['I am a develthis code schayllI am a dquick sort algorithm is efficienteveloperenge is '
  'trickyoper'],
 ['quick sort algoritI love this code schallenge is trickyeating pizzahm is efficient'],
 ['writing clean code iis rimportant'],
 ['qu ick sort algoritI love eaating pizzahm is efficzient'],
 ['qu ick sort algoritI love eaating pizzvahm is efficzient'],
 ['thisI am a dquick sort algorithm is efficienteveloperchayllenge is tricky'],
 ['quick sort algoritefficient'],
 ['I Io love eaI love eating pizort aligorithm is efpfIicientting pizzaeloper'],
 ['eleepnhantselephanpts are hthis code e is trickyuge are huge'],
 ['Pyththe quick brown fox jumps over the lazy dogon programmi ng is fun'],
 ['my'],
 ['quick soithmc ihs efficientt'],
 ['eleeeuge'],
 ['Python ogramming is fun'],
 ['I am a deveopI Io love eaI love eating pizort aligorithm is efpfIicientting pizzaeloperer'],
 ['mahthematics can bI athe qurown fox jumps over the lazy dogm a developeog asy'],
 ['Io love eaI love eatingr pizort palgorithm is efficientting pizza'],
 ['PythothisI am a dquick sort algorithm is efficienteveloperchayllenge is trickyng is fun'],
 ['Pyththe quick brown fox jumps over the lazy dogonleephants are hugegramming ins fun'],
 ['this code schayllI am a dqk sort algorithm is efficienteveloperenge is tricky'],
 ['quick sort algoritI love eating phm is efficient'],
 ['Pyththe quick brown fox jumps over the lazy dogonleephants I am a developerare hugegramming ins '
  'fun'],
 ['mahthematics can be easty'],
 ['qu ick sort algoritI love eaating pizzvahm is efficzeient'],
 ['I am a dedveopthis code mathematics can be eacsychalleI love eating pizzangge is trickyer'],
 ['eleepnhantsethis code challenge is triyckyhuge are huge'],
 ['mathematI love eating pizzaics can be eacsy'],
 ['thse quick brown fox jumps oover the lazy dog'],
 ['writing tclean code is importamathematI love eating pizzaics can be eacsynt'],
 ['quick soithmc ihs efI am a developerficient'],
 ['I am a depethisI am a dquick sort algorithm is efficienteveloperchayllenge is trickyr'],
 ['quick sI am ad deveopercient'],
 ['cquick sort algorithm is efficient'],
 ['quick soitc ihs uefficient'],
 ['quick sort alsgoritI love this code sct'],
 ['I enge is trickyr'],
 ['I am ad deveo per'],
 ['quick sort algorithm is efficI am a dquick sort algorithm isp efficientevelope rient'],
 ['thse quick brown fox jumps oover the ladog'],
 ['quick soithmc ihs effkicientt'],
 ['mat hematics can be eacsy'],
 ['tPython programming is fun'],
 ['I Io love eaI love eating pizort taligorithm is efpfIicientting pizzaeloper'],
 ['I'],
 ['Io love eaI love eatingr pizort palgor ithm is efficientting pizza'],
 ['tPython programm ing is fun'],
 ['science some has branches of'],
 ['one two three four five six seven eight nine'],
 ['abcdefghijklmnopqrstuvwxyz abc defghijklmnopqrstuvwxyz'],
 ['aa aaaa aaaaaa aaaaaaaa aaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaa'],
 ['this is a test for prime numbers in words within a sentence'],
 ['The quick brown fox jumps over the lazy dog'],
 ['The cat in the hat sat on the mat'],
 ['Peter Piper picked a peck of pickled peppers'],
 ['An apple a day keeps the doctor away'],
 ['The cat in tofhe ahat sat on the mat'],
 ['doctor'],
 ['test'],
 ['picaaaaaad'],
 ['eight'],
 ['aa aaa aaaaaaaa aaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaa'],
 ['abcdefghijklmnopqrstuvwxyz'],
 ['doctaaaaor'],
 ['Peter Piper picked a peck of pipers'],
 ['The quicdoctorown fox jumps over the lazy dog'],
 ['abcpipers'],
 ['six'],
 ['aabcaaaaa'],
 ['zudeUmy'],
 ['fox'],
 ['clwFZYzs'],
 ['aaaaaa'],
 ['pcicaaaaaad'],
 ['Peter Piper psomeicked a peck of pickled peppers'],
 ['The cat in tofhe ahat asat on thte mat'],
 ['P eter Piper picked a peck of pickled peppers'],
 ['clwZFZYzs'],
 ['aabcaaaaaa'],
 ['tesst'],
 ['ELBDOeWCp'],
 ['fodoctorx'],
 ['eighpeck'],
 ['dooctaaaaor'],
 ['Peter Piper picked a peck of picklled peppers'],
 ['wFZYzs'],
 ['The cat in tofhe aha t asat on thte mat'],
 ['aa aaaa aaaaaa aaaaaaaa aaaathteaaaaaaaa aaaaaaaaaaaaaaaaaaaa'],
 ['doaa aaaa aaaaaa aaaaaaaa aaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaactor'],
 ['wFZYs'],
 ['doctaaaaorfoforr'],
 ['brown'],
 ['doctaaaaorfoftorr'],
 ['ffox'],
 ['nine'],
 ['Pk of pickled peppers'],
 ['a'],
 ['seven'],
 ['psomeicked'],
 ['aa aaa aaaaaaaa aaaaaaa'],
 ['this is a test for prime numbers in words wit hin a sentence'],
 ['doctthreefooftorr'],
 ['abcyz'],
 ['doaa aaaa aaaaaa aaaaaaaa aaaaaaaaaaaa aaaAnaaaaaaaaaaaaaaaaactor'],
 ['browrn'],
 ['Peter Piper pipcked a peck of pickled peppers'],
 ['picked'],
 ['tofhe'],
 ['wit'],
 ['aaa aaa aaaaaaaa aaaaaaa'],
 ['aaaaaaa'],
 ['aabcnsatumbersaaaaa'],
 ['twnumboneers'],
 ['doctthrePeter Piper picked a peck of picklled peppersefooftorr'],
 ['hat'],
 ['sciencedoctaaaaor'],
 ['tbwnumboneers'],
 ['aa'],
 ['aa aaa aaaaaaaa aaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaa'],
 ['three'],
 ['lazy'],
 ['docctor'],
 ['lazynumbers'],
 ['jumps'],
 ['siis'],
 ['The quicdoctorown fox jumps over thed lazy dog'],
 ['aha'],
 ['doaa aaaa aaaaaa aaaaaaaa aaaaaaaaaaaa aaaaaaaaaaaaasixaaaaaaactor'],
 ['pipcked'],
 ['peppersefoofrtorr'],
 ['aaaaa'],
 ['The cat in tofhe ahat sat onaabcnsatumbersaaaaa the mat'],
 ['P'],
 ['Peter Piper pickepd a peck of picklled peppers'],
 ['browrnsix'],
 ['pickedwit'],
 ['science sofhas branches oaf'],
 ['aaaaaaaaaaaaaaaaaaaa'],
 ['aahin'],
 ['one'],
 ['aaaaaaaaaaaaaaaaaaaactor'],
 ['awordsbc'],
 ['browrisnsix'],
 ['science sofhas branches otwoaf'],
 ['doaa aaatbwnumboneersa aaaaaa aaaaaaaa aaaaaaaaaaaa aaaaaaaaaaaaasixaaaaaaactor'],
 ['Peter Piper psomeicked a peck of piP eter Piper picked a peck of pickled peppersckled peppers'],
 ['abcppipeThears'],
 ['defghijklmnopqrstuvwxyzbrowrn'],
 ['ahat'],
 ['fffopipersx'],
 ['asatdooctaaaaor'],
 ['cat'],
 ['thed'],
 ['abc'],
 ['si'],
 ['ssi'],
 ['piP'],
 ['doctaaaaoraahin'],
 ['has'],
 ['Piper'],
 ['psoed'],
 ['jmumps'],
 ['caaaaaaaaaaaaaasixaaaaaaactor'],
 ['aaaathteaaaaaaaaa'],
 ['aa aahina aaaaaaaa aaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaa'],
 ['aa aaa aaaaaaaa aaaaabrowrnaa'],
 ['aa aaaa aaaaaa aaaapiPaaaa aaaathteaaaaaaaa aaaaaaaaaaaaaaaaaaaa'],
 ['doctaaaaorrfoforor'],
 ['s'],
 ['fffox'],
 ['oaf'],
 ['doaa aaaa aaaaaa aaaaaaaa aaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaactoar'],
 ['The quicdoctorown fox jumps over thed layzy dog'],
 ['browrnjumps'],
 ['eter'],
 ['aaaAnaaaaaaaaaaaaaaaaactor'],
 ['iss'],
 ['doaa aaaa aaaaaaa aaaaaaaa aaaaaaaaaaaa aaaAnaaaaaaaaaaaaaaaaactor'],
 ['bropickledn'],
 ['PP'],
 ['oabcpipersttwoaf'],
 ['prime'],
 ['aa aaaa aaaaaajmumps aaaaaaaa aaaathteaaaaaaaa aaaaaaaaaaaaaaaaaaaa'],
 ['doctthrek of picklled peppersefooftorr'],
 ['docttThehrek'],
 ['over'],
 ['ipicked'],
 ['brosiispickledn'],
 ['ccat'],
 ['quick'],
 ['Peter Piper psomeicked a epeck of piP eter Piper picked a peck of pickleld peppersckled '
  'peppers'],
 ['fodoccto'],
 ['abcy'],
 ['pThe cat in the hat sat on the matrime'],
 ['aassibcnsatumbersaaaaa'],
 ['uicdoctorown fox jumps over the lazy dog'],
 ['aa aaa aaaaaaaa aaaaaaaaaaaa aaaaaaaaaaaaaaaaapicklledaaa'],
 ['pickedquick'],
 ['aahina'],
 ['abcppiapeTheaars'],
 ['pickeddquick'],
 ['aahinP eter Piper picked a peck of pickled peppersa'],
 ['wiit'],
 ['doctthreefoolazynumbersftorr'],
 ['ahhat'],
 ['brosiispsickledn'],
 ['sentence'],
 ['P eter Piperkeepsrs'],
 ['pidckedwit'],
 ['doctoaaaaorfoforr'],
 ['atwohhat'],
 ['aahinP etpTheer Piper picked a peck of pickled peppersas'],
 ['haas'],
 ['on'],
 ['aaa aaa aaaaaaaa aaaaabrowrnaaaaaaaaaaaaaasixaaaaaaactora'],
 ['scxdLYL'],
 ['aahinP'],
 ['aaaaabrowrnaa'],
 ['The cat min tofhe aha t asat on thte mat'],
 ['witscience sofhas branchess oawf'],
 ['wsFZYzs'],
 ['quuick'],
 ['aaaapiPaaaa'],
 ['abcyaabcaaaaaaz'],
 ['The quicdoctorown fox jumps over the ldog'],
 ['aaa aaa aaaaaaasixaaaaaaactora'],
 ['aaa aaaa aaaaaa aaaaaaaa aaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaapiPaaaa'],
 ['aaaaaaaaaaaaaaaaaaaactoar'],
 ['forx'],
 ['one two three four five six seven eight peppersnine'],
 ['defghiabcpipersjklmnopqrstuvwxyzbrowrn'],
 ['eeter'],
 ['aathedaaaaaaaaaaaaaaaaaactor'],
 ['aaaaaaaaaaapipersaaaaaaaaactoar'],
 ['doaa aaaa aaaaaa aaaaaaaa aaaaar'],
 ['one two three four five siThe quicdoctorown fox jumps over thed lazy dogx seven eight '
  'peppersnine'],
 ['fffokeepsx'],
 ['ELBDkeepsOaa aaa aaaaaaaa aaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaeWCp'],
 ['t'],
 ['fffopiprersx'],
 ['defghijklmnopqrstu'],
 ['eiPeter Piper picked a peck of picklled peppersghpeck'],
 ['quicdoctorown'],
 ['acaaaaaaaaaaaaaasixaaaaaaactora'],
 ['abcppiapeaTheaars'],
 ['ewitscienaa aahina aaaaaaaa aaappleaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaceeter'],
 ['aaaaaaaaaaaaaaabrowrnaaaactor'],
 ['Peter Piper pickAn apple a day keeps the doctor awayepd a peck of picklled peppers'],
 ['bropickpleldn'],
 ['pickediwit'],
 ['defghijkaaaalmnopqrstu'],
 ['doaa aaatbwnumboneersa aaaaaa aaaaaaaa aaaaaaaatwnumboneersaaaaasixaaaaaaactor'],
 ['quicka'],
 ['aawfoura'],
 ['qpThek'],
 ['doctthrePeter Piper picked a peck of pickllfed peppersefooftorr'],
 ['aaaaaaaaaaaaaaaaaaaaaceeter'],
 ['pctwoicaaaaaad'],
 ['ffaaaaaaox'],
 ['spiP'],
 ['aaaapiThe cat in tofhe aha t asat on thte matPaaaa'],
 ['dtoctaaaaorrfoforor'],
 ['aaaaaaaaaaaaaaaaapicklledaaa'],
 ['ipipcked'],
 ['ly'],
 ['The quick broELBDOeWCp'],
 ['Yzs'],
 ['apple'],
 ['aahihhna'],
 ['aa aaaa aaaaaaaa aaaaaaa'],
 ['Tat on tmat'],
 ['aa aaa aaaaaabrowrnsixa aaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaa'],
 ['ewitscienaa aahina aaaaaaaa aaappleaaaaaaaaaa aaaaapaaaaaaaaaaaaaaaaceeter'],
 ['aaa aaaa aaaaaa aaaaaaaa aaaaahatapiPaaaa'],
 ['quicdoctn'],
 ['aahinP etpTheer Pipaer picked a peck of picklersas'],
 ['asatdooctor'],
 ['fthteffokeepsx'],
 ['twnumboeers'],
 ['ipickeed'],
 ['aa aahina aaaaaaaa aaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaa'],
 ['aaa aapeppersefooftorra aaaaaaasixaaaaaaactora'],
 ['ahhateight'],
 ['brosiispicklledn'],
 ['aa aaa aaaaaaaa aaaaa aa'],
 ['ss'],
 ['docotthrek of picklled peppersefooftorr'],
 ['aabcyaabcaaaaaaz'],
 ['The quicdoct fox jumps over the lazy dsog'],
 ['ffaaaaahatapiPaaaaaaaaaaox'],
 ['quicdoct'],
 ['peck'],
 ['docotthrek'],
 ['aahinP eter Piper picked a peck of pickled peppersaeighpeck'],
 ['one two three four five six seforxven eight nine'],
 ['bropickplpidckedwiteldn'],
 ['tbwnumboneoers'],
 ['aahinP eter Piper piceppersa'],
 ['doaa aaaa aaaaaa aaaaaaaa aaaaaaaaaaaa aaaAnaaaaaaaaaaaaaaaaaactor'],
 ['sss'],
 ['etetpTheerest'],
 ['aaatbwnumboneersadoctor'],
 ['ewitscienaa aahina aaaaaaaa aaappleaaaaaaaaaa aaaaapaaaaaaaaaaaaaaaaceePeterter'],
 ['quickaaahinP'],
 ['aaa aaa aaaaaaaa aixaaaaaaactora'],
 ['aworddsbc'],
 ['eTtetpTheerest'],
 ['wordswsFZYdoctaaaaorrfofororzsaa aaaa aaaaaaaa aaaaaaa'],
 ['matrime'],
 ['faa aaaa aaaaaajmumps aaaaaaaa aaaathteaaaaaaaa aaaaaaaaaaaaaaaaaaaathteffokeepsx'],
 ['abcppipeTheminars'],
 ['atwohsomehat'],
 ['wordds'],
 ['matsix'],
 ['lzazy'],
 ['caaaaaaaaaaaaaasixaor'],
 ['quuuick'],
 ['abcdefghaahinP eter Piper piceppersawxyz'],
 ['hhin'],
 ['apbcppieminars'],
 ['aa aaa a'],
 ['ipipckedapbcppieminars'],
 ['aaa aaa aaaaaaa a aaaaaaa'],
 ['broELBDOeWCp'],
 ['ququicdoctorownn'],
 ['faa'],
 ['aaaaaaaaaaaaaaaaaaaaaeWCp'],
 ['scxdLYtwnumboeers'],
 ['fffopipersxeeter'],
 ['aThe ciat in tofhe aha t asat on thte mattwohhat'],
 ['pekck'],
 ['doctthrek of picklrled peppersefooftorr'],
 ['Anlazynumbers'],
 ['aabcyaabcaaaaaazjumps'],
 ['doctthrek of picklled peppersefooftorrccat'],
 ['aathis is a test for prime numbers in words within a sentencebcaaaa'],
 ['aaa aaa aaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaa'],
 ['aabcaaa'],
 ['The ocat in tofhe ahat sat on the mat'],
 ['spiwiit'],
 ['peppersghpecrk'],
 ['oone'],
 ['witscience sofhas branchessc oawf'],
 ['lazynumbrs'],
 ['abcdefghaahinP eter Pir piceppersawxyz'],
 ['iPiper'],
 ['twnumaaawapdoaa aaaa aaaaaa aaaaaaaa aaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaactorhers'],
 ['doaa aaatbwnumboneersa aaaaaa aaaaaaaa aaaaaaaaaaaa aaaaaaaaaaaaasixaaaaaaacator'],
 ['aaatbwnumboneersa'],
 ['browbn'],
 ['hin'],
 ['abcdefghijklmnopqrstuvwxabcppipeThearsyz'],
 ['dooctaaaaorbrowrnjumps'],
 ['aaa aaa aaaaaaa aa aaaaaaa'],
 ['aaaAnaaaaaaaaaaaaaaaaaactor'],
 ['dooctaaaor'],
 ['sefofrxven'],
 ['The onaabcnsatumbersaaaaaocat in tofhe ahat sat on the mat'],
 ['The cat in tofhe ahat saat onaabcnsatumbersaaaaa the mat'],
 ['doctoaapsoedaaorfoforr'],
 ['Peter Piper pk of pipers'],
 ['quicdoctorownaaa aaa aaaaaaaa aaaaaaa'],
 ['az'],
 ['ELquickaaahinPBDOeWCp'],
 ['one two three four five sieven eight peppersnine'],
 ['The quicdoct brosiispsickledn jumps over the lazy dsog'],
 ['pickeduquick'],
 ['bfffopipersxeeterrown'],
 ['science sofhas branches oaffodoctorx'],
 ['zudeU'],
 ['ff'],
 ['picklled'],
 ['picdoctaaaaorked'],
 ['twnumaaawapdoaa aaaa aaaaaa aaaaaaaa aaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaatorhers'],
 ['sstofhe'],
 ['bropipekckckpleldn'],
 ['aa aahina aaaaaaaa aaaaaaaaaaaa aaaaaaaainaaaaaaaaaaaaaaa'],
 ['sciencedoctaaaeaor'],
 ['Peter Piper pickAn apple a day keeps the doctor awayepd a peck of paicklled peppers'],
 ['fodoceiPeter Piper picked a peck of picklled peppersghpeckcto'],
 ['aahidooctaaaaorbrowrnjumpsna'],
 ['aa aaa'],
 ['Pk'],
 ['peppersghpeck'],
 ['cccat'],
 ['iPithe quick brown fox jumps over the lazy dogper'],
 ['Paabcnsatumbersaaaaak'],
 ['aaaaaascience sofhas branches otwoaf'],
 ['tthed'],
 ['aaaAnaaaaaaaaaaaaaaaaaaactor'],
 ['docttaaa aaa aaaaaaa a aaaaaaahrek of picklled peppersefooftorrccat'],
 ['lazyndooctaaaaorumbers'],
 ['aaaaaaaaaaaaa'],
 ['aahidooctetpTheeraaaaorbrowrnjfodoceiPeter Piper picked a peck of picklled '
  'peppersghpeckctoumpsna'],
 ['aaaaaaaa'],
 ['seveen'],
 ['tbwnumrs'],
 ['pipP'],
 ['ascience some has branches ofaaapiPaaaa'],
 ['docttaaa'],
 ['doctthrePetooftorr'],
 ['doctaaaaaor'],
 ['jmjps'],
 ['The cat in tofhe ahat saat onaabcnsatumberaaaaa the mat'],
 ['science some has branchesone two three four five six seven eight peppersnine of'],
 ['pepperseffoofrtorr'],
 ['picaaaad'],
 ['docotthrek of picklled peppersefThe quicdoctorown fox jumps over the ldogorr'],
 ['the quick brown forx jumps over the lazy dog'],
 ['peppersckled'],
 ['dooctor'],
 ['peppersas'],
 ['aaaaaaaaaaaaaaaaaaaeaaceeter'],
 ['peppersckleed'],
 ['within'],
 ['witscience sofhas branchess owawf'],
 ['oaaf'],
 ['fffokeepshinx'],
 ['ahthat'],
 ['aaaaaaaaaaaaasixaaaaaaactor'],
 ['abcdefghijklmnopqrsqtuvwxyz abc defghijklmnopqrstuvwxyz'],
 ['pekkck'],
 ['awordsbcawf'],
 ['apickeduquickaaAnaaaaaaaaaaaaaaaaactor'],
 ['PkPeter Piper pickAn apple a day keeps the doctor awayepd a peck of picklled peppersmattwohhat'],
 ['pepperseffoofrtoorr'],
 ['aaa aaaa aapaicklleda aaaaaaaa aaaaahatapiPaaaa'],
 ['quicdone two three four five six seforxven eight nineoctn'],
 ['doaa aaaa aaaaaaa aaaaaaaa aaaaabcaaaaaaaaaaaa aaaAnaaaaaaaaaaaaaaaaactor'],
 ['twnusioeers'],
 ['doaa aaaa aaaaaaa aaaaaaaa aaaaa aaaAnaaaaaaaator'],
 ['The q brown fox jumps over the lazy dog'],
 ['Peter Piper pipcked a peck of pickled ppeppersghpecrkeppers'],
 ['ayz'],
 ['aaa'],
 ['doumbersftorr'],
 ['defghijkaaaalmnabcdefghaahinP eter Piper piceppersawxyzpqrstu'],
 ['fodtoctaaaaorrfofoaa aahina aaaaaaaa aaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaarorx'],
 ['tofhhe'],
 ['abcppiaepeaTheaars'],
 ['jmjpps'],
 ['laozyndooctaaaaorumbers'],
 ['aa aaa aaaaaaseforxven aa aaaaaaa'],
 ['ELOeWCp'],
 ['the quick breown forx jumps over the lazy dog'],
 ['aa aaa aaaaaaaa aaaaabrdoaa aaaa aaaaaa aaaaaaaa aaaaaaaaaaaa aaaAnaaaaaaaaaaaawrnaa'],
 ['science seome has branches of'],
 ['aaa aaa aaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'],
 ['pickeduquickaaAnaaaaaaaaaator'],
 ['science sofhas bran ches otwoaf'],
 ['twnipipckedumboneers'],
 ['piiP'],
 ['aasciencedoctaaaeaoraaaaaaaaaaa'],
 ['jmjpp'],
 ['one two three four five six seven eight nineasatdooctaaaaor'],
 ['brownn'],
 ['quicdoneaaaAnaaaaaaaaaaaawrnaa'],
 ['aaaaaaaaaaaaaaaaaaaaaaceeter'],
 ['PaaaAnaaaaaaaatoriper'],
 ['YYzs'],
 ['Pk of pickledaa aaa aaaaaaaa aaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaa peppaers'],
 ['defghiabcpipersjklmnopqrstuwn'],
 ['ipipckpeppersghpeckctoumpsnaminars'],
 ['docrek'],
 ['ahaewitscienaa aahina aaaaaaaa aaappleaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaceeter'],
 ['brownnn'],
 ['aawfooura'],
 ['otwoaf'],
 ['oceiPeter'],
 ['doctoaaaaorfdoctthrePetooftorroforr'],
 ['woaaaaaaaaaaaaaaaaaaaardds'],
 ['Pet'],
 ['quicdoctorownaaa aaa aaaaaaaaa aaaaaaa'],
 ['caaaaaaaaaaaaaaaaaaaaaaceeteraaaaaaaaaaaaaasixaaaaaaaactor'],
 ['matrimecat'],
 ['ssentennce'],
 ['mkZrwvKDr'],
 ['ayabcy'],
 ['Peter Piper psomeicked a ppicklrledeck of pickled peppers'],
 ['twnumboaaaaabrdoaaneers'],
 ['one two threne four five sieven eight peppersnine'],
 ['Yzzfodoccotos'],
 ['aaa aaa aaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabrowrnaa'],
 ['aahinP etpTheer Pipaer pickedeighpecka peck of picklersas'],
 ['q'],
 ['The ceat in tofhe ahat sat on the mat'],
 ['The quicdoct fox jumps over the'],
 ['doaa aaaa aaaaaaa aaaaaaaa aaaaaaaaaaaa aaaAnaaapeppersckleedaaaaaaaaaaaaaactor'],
 ['aaaapiatwohsomehatThe cadoctaaaaaort in tofhe aha t asat on thte matPaaaa'],
 ['pieckleld'],
 ['defghijklmnopqrstruvwxyz'],
 ['aa aaa aaaaaaseforxven aav aaaaaaa'],
 ['jjmummmps'],
 ['fodoctorox'],
 ['pThe cat in the hat saYzst on the matrime'],
 ['clwZFZYz'],
 ['ZGmkXBsVH'],
 ['defghijkaaaalmnabcdefghaahinP'],
 ['The cat in tofhe ahat sat at'],
 ['ELBDkeepsOaa aaa aaaaaaaa aaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaeWCp'],
 ['ofaaapiPaaaa'],
 ['onn'],
 ['e'],
 ['doctaaaaorlly'],
 ['aabc'],
 ['aaaaabrdoaa'],
 ['quicdoc aaaaaaaaa aaaaaaa'],
 ['aa aahina aaaaaaaa aaaaaaaaaaaa aaaainaaaaaaaaaaaaaaa'],
 ['ipipckpepperckctoumpsnaminars'],
 ['fodabcppiaepeaTheaarsoccto'],
 ['pepck'],
 ['twnusioeeighters'],
 ['aav'],
 ['aaaaaaaaaaaaaaaaaaaatorhers'],
 ['piecklpeld'],
 ['The quiaaa aaa aaaaaaa a aaaaaaacdoctorown fox jumps over the lazy dog'],
 ['breown'],
 ['doaa aaaa aaaaaa aaaahhateightaaaaa aaaaaaaaaaaa aaaAnaaaaaaaaaaaaaaaaactor'],
 ['aa aaa aThe cat in tofhe ahat sat ataaaaaaa aaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaa'],
 ['olazynumbersn'],
 ['doctthr picked a peck of picklled peppersefooftorr'],
 ['docttaaa aaa aaaaaaa a aaaaaaahreaaa aaa aaaaaaasixaaaaaaactorak of picklled '
  'peppersefooftorrccat'],
 ['twnumaaawapdoaa aaaa aaaaaa aaaaaaaa aaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaatorhers'],
 ['this is a test for prime numbers in words wit hhin a sentence'],
 ['pk'],
 ['dogper'],
 ['quicdoctorownaaa aaa aaaffoxaaaaaa aaaaaaa'],
 ['ofaaaaaaaaaaaaaaaaaaaaaaaaaapiPaaaapiPaaaa'],
 ['aaatbwnuoneersa'],
 ['aaAnaaaaa'],
 ['The q brown fox jumps over trhe lazy dog'],
 ['qpThekk'],
 ['fodaapaicklledarox'],
 ['lyazy'],
 ['pThe cat in the hat sat on the maetrime'],
 ['prbreownime'],
 ['doaa aaaa aaaaaaa aaaaaaaa aaaaa aaaaaator'],
 ['mecat'],
 ['science some has branchesone two three four five six seven eightn peppersnine of'],
 ['Peter Piper picked aa aaa aaaaaaaa aaaaa aaa peck of pickled peppers'],
 ['defghijkxlmnopqaaaarstruvwxyz'],
 ['piawordsbciwit'],
 ['doctaaaaoorrfoforor'],
 ['pseppersghpecrkree'],
 ['sieven'],
 ['aaaAnaaaaaaaaahinaaaaaaaaactor'],
 ['aasciencedocteaaaeaoraaaaaaaaaaa'],
 ['twnumaaaawapdoaa aaaa aaaaaa aaaaaaaa aaaaaaaaaaaa aars'],
 ['tpipP'],
 ['dooctaaaaorbrowrcnjumps'],
 ['dooctaaaaorbrwornjuwmps'],
 ['aaaaaascience'],
 ['aa aaaPkPeter Piper pickAn apple a day keeps the doctor awayepd a peck of picklled '
  'peppersmattwohhat'],
 ['witscience sofhas braninchess owawf'],
 ['dehrek'],
 ['doctthrePetowitscience sofhas braoftorr'],
 ['x y z'],
 ['numbers'],
 ['quicninek'],
 ['the quick brown fox jumps over the lazy twodog'],
 ['this is a test for prime numbers foxin words within a sentence'],
 ['quicniinek'],
 ['two'],
 ['aone two three fou r five six seven eight nine'],
 ['scPeterience some has branches of'],
 ['this is a test for prime numbers in wodaynce'],
 ['twPetero'],
 ['numbeonrs'],
 ['wWFWJpaA'],
 ['science some has brsentencehes of'],
 ['pceck'],
 ['tesnumbeonrs'],
 ['some'],
 ['aonePiper two three fou r five six seven eight nine'],
 ['twPro'],
 ['aonepple'],
 ['wWFWJaa aaaa aaaaaaa aaaaaaaa aaaaaaaaaaaa aaaaaaaaaaaakeepsaaaaaaaapaA'],
 ['aaaaaaaaaaaa'],
 ['The quick brown fox jumps over the lazy dogscPeterience some has branches of'],
 ['twProo'],
 ['wWFWJaa'],
 ['f'],
 ['quik'],
 ['the quick bazy dog'],
 ['nusmbers'],
 ['o'],
 ['fThe cat in the hat sat on the mat'],
 ['quaoneppleek'],
 ['priime'],
 ['quicniscience some has inbrsentencehes ofinek'],
 ['aaaaaaaaaaaakeepsaaaaaaaapaAf'],
 ['this'],
 ['wWFWJaa aaaa aaaaaaa aaaaaaaa aaaaaaapsaaaaaonePiperaaaapaA'],
 ['peppers'],
 ['tesAnnumbeonrs'],
 ['apbcopqrstuvwxyz'],
 ['words'],
 ['science some has brsentenncehes of'],
 ['in'],
 ['aaaaaaaaaaaakeepsatwPeteroapaA'],
 ['branches'],
 ['wordcats'],
 ['The q uick brown fox jumps brsentencehesterience some has branches of'],
 ['aaaaaaaaaaaaaa'],
 ['afThe cat in the hat sat on the mataa'],
 ['bazy'],
 ['r'],
 ['n'],
 ['ThAn apple a day keeps the doctor awaye cat in the hat sat on the mat'],
 ['Peter'],
 ['wordcthe quick brown fox jumps over the lazy twodogats'],
 ['Ther quick brown fox jumps over the lazy dog'],
 ['science threesome has brsentencehes of'],
 ['this is for prime numbers in wodaynce'],
 ['science threesome has bcrsentencehes of'],
 ['this is a tesninet for prime numbers in words within a sentence'],
 ['aa aaaaa aaaaaa aaaaaaaa aaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaa'],
 ['science threeshas brsentencehes of'],
 ['afThe Ther quick brown fox jumps over the lazy dogt on the mataa'],
 ['thhree'],
 ['this is for prime numbers ian wodaynce'],
 ['quicnibazynek'],
 ['mataa'],
 ['twPettero'],
 ['aonepplee'],
 ['eZnNBxOH'],
 ['quicniscie some has inbrsentencehes ofinek'],
 ['quicniscwodaynceience some has inbrsentencehes ofinek'],
 ['ofinek'],
 ['overpceck'],
 ['nusmbscience some has brsentencehes ofers'],
 ['ofers'],
 ['this is a test for prime numbers in woodaynce'],
 ['wtwo'],
 ['nusmbscience'],
 ['aaaatwodogaa'],
 ['science threesquicniscience some has inbrsentencehes ofinekome has bcrsentencehes of'],
 ['aone'],
 ['FwWFWJpaA'],
 ['thisscience threesome has bcrsentencehes of is a tesnappleime numbers in words within a '
  'sentence'],
 ['this is a atest for prime numbers in woodaynce'],
 ['Ther quick brown fox jumps over the lazy do g'],
 ['scPeterience some hacs branches of'],
 ['priisiimofineke'],
 ['rtwPetero'],
 ['Peter Pkled peppers'],
 ['quipriisiimofinekek'],
 ['ni'],
 ['defghijklmnopqrstuvwxyz'],
 ['the quk brown fox jumps over the lazy dog'],
 ['peppeers'],
 ['thisscience threesome has bcrsentencehes of is a tesnappleime numbers in words within a '
  'sentenceaoe'],
 ['priisiimofinTheke'],
 ['twodogats'],
 ['threeshas'],
 ['eZnNBxOHAn'],
 ['threesome'],
 ['keeps'],
 ['quicniscwodaynceience'],
 ['this is for prime numbers ian wodaynce o'],
 ['niaonepplee'],
 ['this is for prime numbers in wodayabcdefghijklmnopqrstuvwxyz abc defghijklmnopqrstuvwxyznce'],
 ['The'],
 ['ofinekome'],
 ['Peeter'],
 ['oveAn apple a day keeps the doctor awayr'],
 ['ninee'],
 ['wWFWJaa aaaa aaaaaaa aaaaaaaa aaaaaaapsaaaaaonePiperaaaawtwopaA'],
 ['lpZlaIbZZ'],
 ['pickled'],
 ['uick'],
 ['eZnNBxOHH'],
 ['wordscience some has brseentenncehes ofs'],
 ['this is for prime numbers in wodayabcdefghijklmnopqrstuvwxfivec defghijklmnopqrstuvwxyznce'],
 ['this is a test for prime numbers in twodogatswords within a sentence'],
 ['this is a test for prime numbers in inwordsentence'],
 ['ThAn apple a day kweeps the doctor awaye cat in the hat sat on the mat'],
 ['quicnibaczynek'],
 ['ofoveAn apple a day keeps the doctor awayrek'],
 ['ateest'],
 ['tuickesome'],
 ['An'],
 ['An apple abcdefghijklmnopqrstuvwxyza day keeps thdoctor away'],
 ['uithis is for prime numbersofers ian wodayncek'],
 ['eZnNaonepple'],
 ['apbcpoxyz'],
 ['rtwPro'],
 ['sentenceaoe'],
 ['wodayncek'],
 ['peppeatesters'],
 ['aaaaaaaaaaaakeepsaaaaaaaaapaAf'],
 ['ThAn'],
 ['kekeps'],
 ['word'],
 ['aaaaaaaaaaaakeepsaaaaaaaapaA'],
 ['science'],
 ['wWwodayabcdefghijklmnopqrstuvwxyzFWJaaaaaaaapaA'],
 ['kweeps'],
 ['bcrsentencehes'],
 ['nTThAn'],
 ['niaonepplquicniscwoodaynceienceee'],
 ['bcrsentebrseentenncehesnceheafThes'],
 ['thhreescience some has branches of'],
 ['ThAn apple a day kweeps the doctor awaye cat in the ehat sat on the mat'],
 ['scPeterienscience some has branches ofce'],
 ['owodayabcdefghijklmnopqrstuvwxyz'],
 ['quicniscie some hasthis is for prirs in wodaynce inbrsentencehes ofinek'],
 ['threesha'],
 ['ovrlazy'],
 ['quicniscience some has inbrsentencehesek'],
 ['branchers'],
 ['ovekweeps awayr'],
 ['wordrs'],
 ['tesnumbeonrrs'],
 ['tukickesome'],
 ['The quick brown fox jumps over the lazyo dog'],
 ['inwordsentence'],
 ['numbersofers'],
 ['nusmbscience some has brsentwProtencehess ofers'],
 ['doctorover'],
 ['sat'],
 ['aaaaapeppeatestersaaaaaaaakeepsatwPeteroapaquipriisiimofinekekA'],
 ['quicniscienthe quick brown fox jumps over the lazy dogce some has inbrsentencehesek'],
 ['the quicik bazy dog'],
 ['quicniscienthe quick brown fox jutmps over the lazy doegce some has inbrsentencehesek'],
 ['abcdefghijklmnopqrstuvwxyza'],
 ['ofce'],
 ['bnusmbers'],
 ['zYwjhBCYS'],
 ['dog'],
 ['oveorpceck'],
 ['woodaynce'],
 ['bazyover'],
 ['pkweeps'],
 ['this is for prime numbers in wodayabcdefghijklmnopqrstuvwxyz abdefghijklmnopqrstuvwxyznce'],
 ['quicniscience'],
 ['oveAn apple a day keeplpZlaIbZZs the doctor awayr'],
 ['aaaaaaaaaaaakeepsatwPaeteroapaA'],
 ['ttukickesomeowodog'],
 ['Ther quick brown fox jumps over the lazydog'],
 ['qnuicniscience'],
 ['the quick bazdy dog'],
 ['wWFWJaa aaaa aaaaaaa aaaaaaaa aaaaaaaaaaaa aaaaaaaTherawithinaaaakeepsaaaaaaaapaA'],
 ['aonePiper'],
 ['thia tesnappleime numbers in words within a sentenceaoe'],
 ['niaonepplquicniscwoodaynceiencawayreee'],
 ['oveAn'],
 ['eZnNaonepplThe quick brown fox jumps over the lazy dogscPeterience some has branches ofe'],
 ['scPeterience'],
 ['ofoveAn apple a day keepsrek'],
 ['numbeonwithins'],
 ['ofcfe'],
 ['wodayabcdefghijpklmnopqrstuvwxfivec'],
 ['this is a atoverest for priquikme numbers in woodaynce'],
 ['Th'],
 ['owodayabcdefghijklmnopqrstuyz'],
 ['threThe quick brown fobranchesx jumps over the lazy doge'],
 ['doge'],
 ['tesAnnumbe'],
 ['twPaaaaaaaaaaaakeepsaaaaaaaaapaAfero'],
 ['TTh'],
 ['awayr'],
 ['away'],
 ['twodogatswords'],
 ['i'],
 ['oe'],
 ['one two ht nine'],
 ['wWFWJaa aaaa aaaaaaaa aA'],
 ['quicniscienthe quick brown fox jutmps over the lazy doegcem some has inbrsentencehesek'],
 ['twPrroo'],
 ['this is for primeu numbers in wodayabcdefghijklmnopqrstuvwxyz abc defghijklmnopqrstuvwxyznce'],
 ['nusmbeaonePiperrs'],
 ['aonple'],
 ['twPPtettero'],
 ['Pkled'],
 ['quicnik'],
 ['thpriquikmee quick brown fox jumps over the lazy twodog'],
 ['wWFpeppeatestersWJpaA'],
 ['quicnibathis is a tesninet for prime numbers in words within a sentencezynwordscienceek'],
 ['abcdefghijklmnopqrstuvwxyz abc defghquicniinekijklmnopqrstuvyz'],
 ['twPPtetteroaaa'],
 ['ofe'],
 ['this is for prime numbers in wodayabcdefghijklmnopqrstuvwxyz abc defghijklmnopqrstuvzwxyznce'],
 ['day'],
 ['wodayatbcdefghijpklmnopqrstuvwxfivec'],
 ['pr'],
 ['brseentenncehesPiper'],
 ['lpZltwProaIlbbZZZ'],
 ['inwoovekwnusmbscienceeepbrsentencehesteriencerrdseintence'],
 ['foxin'],
 ['numbbeonrs'],
 ['pecck'],
 ['thdoctor'],
 ['thinuquaoneppleekin wooinbrsentencehesekdaynce'],
 ['awaye'],
 ['this is for prime rnumbers in wodayabcdefghijklmnopqrstuvwxfivec defghijklmnopqrstuvwxyznce'],
 ['The cat in the hat squicniscience some has inbrsentencehes ofinekat on the mat'],
 ['nin'],
 ['oveAn appTher quick brown fox jumps over the lazy dogle a day keeplpZlaIbZZs the tor awayr'],
 ['uithis is for prime numbersofers ian wodayncekthdoctor'],
 ['keeThekps'],
 ['overThAn apple a dator awaye cat in the ehat sat on the mat'],
 ['thhtree'],
 ['numbeonbcrsentencehess'],
 ['Ther quick brown fox jumps opriimever the lazy do g'],
 ['eZnNadefghquicniinekijklmnopqrstuvyzple'],
 ['tpeppeersuickesome'],
 ['tukicokesome'],
 ['ovrlazuicky'],
 ['Peter Piper pickernumbersd a peck of pickled peppers'],
 ['aaaaaaaaaaaakeepsaaaaainbrsentencehesekaaaapaAf'],
 ['twto'],
 ['wodaynek'],
 ['fobranchesx'],
 ['numbeonfoxbcrsentencehess'],
 ['wodayne'],
 ['quipriistestiimofinekek'],
 ['oveeorpceck'],
 ['owhatordsce'],
 ['Ther quieightx jumps over the lazydog'],
 ['oifinek'],
 ['this is aa atest for prime numbers in woodaynce'],
 ['quicinbrsentencehesekniinek'],
 ['quicniscienthe'],
 ['eiginbrsentencehesht'],
 ['tneesnumbeonrrs'],
 ['ovrlazcuicky'],
 ['ovrpceck'],
 ['quiicniscwodaynceience'],
 ['sciequipriisiimofinekeknce'],
 ['brseentenncehesPipwWFWJaa aaaa aaaaaaaa aAer'],
 ['ffaaaaaaa'],
 ['peecc'],
 ['wWFWJaa aaaa aaaaaaa aaaaaaaa aaaaaaaaaaaa aaaaaaaaaaaakeepsaaaaaaaapaaA'],
 ['ofinekat'],
 ['quicniscienthee has inbrsentencehesek'],
 ['twwo'],
 ['primme'],
 ['thia tes nappleime numbers in words within a sentenceaoe'],
 ['An apple abcdefghijklmnopqrstuvwmxyza day keeps thdoctor away'],
 ['nusmnbscience'],
 ['Peter Pkled nusmbsciencepeppers'],
 ['numbeonfoxbcrsseentencehess'],
 ['owodayabcdefghijklthe quick bazdy dogz'],
 ['ofnineece'],
 ['thi test for prime numbers in twodogatswords within a sentence'],
 ['awthpriquikqmeeayrek'],
 ['thpriquikmee quick brown fox jumhe lazy twodog'],
 ['aoneoverpplee'],
 ['aaaaapeppeatestersaaaaaaaaPeteroapaquipriisiimofinekekA'],
 ['The qence some has branches of'],
 ['wtowo'],
 ['thhreescience'],
 ['Ther quick brown fox jumps mover the lazydog'],
 ['qquik'],
 ['brseentenncwWFWJaaehesPipwWFWJaa'],
 ['wodayncekthdoctor'],
 ['owodayabcdefghiijklmnopqrstuyz'],
 ['aaaa'],
 ['nummrbbeonrs'],
 ['pcpeck'],
 ['foxina'],
 ['wordthinuquaoneppleekincats'],
 ['thpriquikmee'],
 ['this is a test for prime numbers in twodogatswocrds within athis senthreesquicnisciencetence'],
 ['owodayabcdefghijklthe'],
 ['qone two three four five six seven eight nineuicnibaczynek'],
 ['odogAn apple a day keeps the doctor away'],
 ['science threeshas brsentencniaonepplquicniscwoodaynceiencawayreeeehes of'],
 ['quiicniscwoidaynceience'],
 ['priimme'],
 ['neZnNBxOHH'],
 ['wordwodayabcdefghijpklmnopqrstuvwxfivec'],
 ['fVLkz'],
 ['qf'],
 ['quicnisciencethree some has inbrsentencehes ofinek'],
 ['Thhe'],
 ['abcdefghijklmnopqrstuvbrseenteenncwWFWJaaehesPipwWFWJaawxyza'],
 ['aaaaquicnissixcience'],
 ['ofinekpr'],
 ['aoonpple'],
 ['science some has branhacses of'],
 ['science thrseesquicniscience some has inbrsentencehes ofinekome has bcrsentencehes of'],
 ['ThAn apple a day keeps the doctor awaye cat inh the hat sat on the mat'],
 ['thhreescience sbrsentennceheses of'],
 ['bcrsethe quick bazy dogntebrseentenncehesnceheafThees'],
 ['wordors'],
 ['wWFWJaa aaaa aaaaaaa aaaaaaaa aaaaatpeppeersuickesomeaaaaaaa '
  'aaaaaaaTherawithinaaaakeepsaaaaaaaapaA'],
 ['ThAn apple a day kweeps the doctor awaye cat hasin the hat sat on the mawWFWJaat'],
 ['ovrlazuy'],
 ['kekepsrek'],
 ['ht'],
 ['woodayndce'],
 ['ovrlazuthia tesnappleime numbers in words within a sentenceaoofcfeeicky'],
 ['ovrlazuthia'],
 ['qq'],
 ['thpriquikmeeg'],
 ['oveeAn'],
 ['wsords'],
 ['science threesome has brsscience some has branhacses ofentencehes of'],
 ['athis'],
 ['wsds'],
 ['this is a atest for prisme numbers in woodaynce'],
 ['wWFW'],
 ['quicniscie some haswodaynek inbrsentencehes ofinbrseentenncehesPipwWFWJaaek'],
 ['Peetquiker'],
 ['quicniscienthe qui dogce some has inbrsentencehesek'],
 ['keepsrek'],
 ['ThAn apple a dayovrlazy kweeps the doctor awaye cat hasin the hat sat on the mawWFWJaat'],
 ['ovrlazuthian'],
 ['Pquicniscienthe quick brown fox jumps over the lazy dogce squicninekas inbrsentencehesekeeter'],
 ['ofineat'],
 ['An apple a lazyoday keeps the doctor away'],
 ['oveAn apple a day keeps the dooctor awayr'],
 ['gthhtree'],
 ['aonePiper two three fou r five six seven eight ngine'],
 ['wcordcats'],
 ['nusmbscience some has bProtencehess ofers'],
 ['owodayabcdefghiijklmnoptwodogatswordsqrstuyz'],
 ['daywodayabcdefghijklmnopqrstuvwxyz'],
 ['nusmnbscienquicniscie some hasthis is for prirs in wodaynce inbrsentencehes ofinekce'],
 ['tesAnnumbonrs'],
 ['ineZnNaoneppleo'],
 ['thia tes nappleime numbers in words within a sentedogenceaoe'],
 ['threeshowodayabcdefghijklmnopqrstuyza'],
 ['afThe Ther quick brown fox jumps over the lazy doe mataa'],
 ['jumhewPro'],
 ['aone tnwo three fou r five six seven eight nine'],
 ['priisiiomofinTheke'],
 ['fobrancheovrlazuthiansx'],
 ['wodayatbcdepfghijpklmnopqrstuvwxfivec'],
 ['cdTOCiFqP'],
 ['uithis ittukickesomeowodogs for prime numbersofers ian wodayncek'],
 ['pe'],
 ['bcrsentenncehes'],
 ['eofcfe'],
 ['aa aaaaa aaaaaa aaaaaaaa bcrsentebrseentenncehesnceheafThesaaaaaaaa'],
 ['thinuquaoneppleekin'],
 ['qnumbbeonrs'],
 ['doegcem'],
 ['aopneppnle'],
 ['aaaaaaaaaaaakeepsaaaaaaaaptwPaaaaaaaaaaaakeepsaaaaaaaaapaAferoaA'],
 ['one two three quicniscie some has inbrsentencehes ofinekfour five six seven eight nine'],
 ['mat'],
 ['thhreescience sbrsentenncethreeheses of'],
 ['aaaaapeppeatestersaaaaaaaaPeteroapaqauipriisiimofinekekA'],
 ['aoonlpple']]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-ri}JC-'
    b'g<vYiJAB!|E$Q1rLEX&3@0K*7x)3pyu2i4w$%`QqEropD+sAO!D9)T+L>tE*0B{(pqK*|xpi?eYKoFaPy_`w#!|Kj=UI*T4NA|K)'
    b'%EzyI@0wf)<F`A;*4S#ByjpSj|&c3Ueo&bdd-'
    b'c4t`4dg!N@GVf}0uG4c5*;+iQ75lgU_uu~WfBY~1sm(fkl<KLCbLR|cmOLtdn99AUWWOcX+H)+o@uz%M@EC8tc^=#0pC41VO+R6+'
    b';n8zUK2JVj>-XCoe1pw2g6&>|w_NA#r}73j@ik$D^UsgzE9`96$Iw%En`c{IXNAyHnY}Ikc&rdDjdI#tW3-'
    b'iAkCyoJnEv@Oxdk7I6&Y)tVaZ3YXR$s#d22Q2)dQcf;yE5>tvv2becHIur+NE%nzm-Ech;QFJu~f|Pg$ONuh-hT-fGx&jb+=tk7{'
    b'Lxc+0xOopt+psgHJwrC9gGyYpPLpIKU&wJlp|joN1S+^p=m?kb)(FWQIQz`w9olDq%&V|>p!bL}UMxWiesjGE85$+Cs*cT_!B@Ri'
    b'Qtg)NmaM@y~uF>SY>wPDp0TTlis+<gYU4evL3fDmhng$En;gw)F&Jv6o?+dApSxpIm1pC1!vz3EKWZjP~MW5={ytM_&SrqWaGJaN'
    b'{$<bJ2eV`WVb<IFf-^ZRIthqkeuJ$j26$YkNx3as<uRe968`O_9tzF1D+3v(HzmzulRmFmxir-DIX^L(?#yyK2@uTpOb-EN7!rBr'
    b'KJHG071_!+ay|E4tYkF<W4_y(=`w(2Zs>oZ}9F}sCW0xKQZklItOvGZW5q+KFkRocSY_{g89X$`v$XYX1)Sh{@6xH6l0(&8sE`Rh'
    b'6JFZa$kjorn+Jwqm(v6P>eI=7W$82L`A;}+rMJ!CTDdYr6mig6xZvE6{}U=?nC?UH-#WzHX<xU&tv?8@S&+r-eerR-rP_N>d4Jlx'
    b'z)4+k^mFZW_Xt(`k!+vA@fv#d|Q9oT8n=1!-3iEA}4J_ZhmBZSd+h%M%_THPR52`Qa5EmbeyT5-Yu3V2rf>bqI&Ij~=g6~Qbbc-'
    b'_7CvZI^(_SkT%<)OC3YNci$14TO{Y!=ye?#V)K^+7nG_8Lg)=h^V<w*iTv38cXm%sk_Pgo7XStL(z+81Af?@tnTA4mskzz<k)FC{'
    b'*my`-~1=RICEi0Exhfw0^7@j6TyVXxkT`Q+Lg~Vjp$kH#4T`teKyo-HR3gSTh;H;y-'
    b'`ZhP~&TcxZx2X*|#wn0!u4Uz*cnW@QJ@;e^?5vwBJ>VTC$*#JfL!n!d|o*({e-`7vS}`%=d`;cj*rD@wPriP-'
    b'j4bRdKhw+}9uuci2d#nv_t8-~?&EB}B8R13!6;aMPkV#^yo+R|OI-kSNs1x|QvA;lk{0AEr&*kG*+JD6@tAq@QV08?%CNbJlj<pr'
    b'>=7P0I+4#u&-gBaf!9xZ}y4fj}c09mmpMs%KoPb3V??5h!??H*R2=-&b#S1$;ia_c`Jy0a5QvVoS1IKOzAR!eNT6Zo+n-'
    b'l^p1u>%7a6zm1&5H7BBLAIZ#F-+;?I%bcG-aYgC_3j(u!f6P4@g5>W@8Onl8mOGMvyp^sP__N+l(Vm34zJYKUSJ?GJr?$J8^E<z4'
    b'e*?LVly^60on})fWPG8(1nnHUW%t^fa02Gjp7Sy*Zu;*VPtqrDZMFvj<oIAWySNl(e?uT@R{<i4LA|uM?1!LFA>5l@R^VXv)Tp-'
    b'5^jT&01noR5f?*-k>H6CtCvxDo=$8?_`(Wz5V>c@D`&g`58-'
    b'X<QRI(c^#~bf*u4A$tqvr$`7NYlA%vU~CQPkC?eJ6r_W`qRhfPKxuiC&r4s>I75I^4DG5J<|T={2-'
    b'K}4IZdgc8iA5^v#J;rR?2*sO6Z5x(?tr09v%Q<iCyJnHdZ9nE$mt!!*f&hxz0I_>xQCFC!3;?X9jVsQCw`08oJor?q<D82J0@6R`'
    b'Hxy`la|n=u$?)UM%F12%TVZq;Me1o^A}evm2)vE2NT=TMT5$p6iL0xE7l74Nz&lvLFvAfsNa8z|4d`U(1!mo+SXUjHJqEddUJ5(o'
    b'k;jZ@EgazTA+XppGQ6R+y+*f^!^Uthh``el6I#GetFd46Tkh90Uz>=_*b1y>APF#*c;HEL<U{~xQPxq6hr~DHJZKaQ=$kBI|2EuZ'
    b'a0-Own=4+!r$w-)r;}$hW0#BK0ARxg8Gg=td1IFf@tiLjKjALy*dMbi7-'
    b'}j21=Ogu6ruSd8JOh=u&r}qK53uLGacgSX1`&JKTm_Lv#)mM#rI*iP`lXy&Wtlphk5|z`?NTKXcs_Y&39(hO_NRj00rD4l#(Gbvp'
    b'za&Z3r@NxO_aHc`v_T#3GE>G|UWx#C<@v^T(&ILxgZTel-+W2wQui5cA*$2dD!%3d9LEV*@(qJ%U>-'
    b'GnNgmzj3PhhG(+QD7YKLB;t8t|MKZE9@#Vi6bc&2L4D$FFQX9x3B-$)f3@cI$^ze$P>W!34H-'
    b'6)6KskHEj0uj315hCIs=@n)B&Ld^dYE!V2jw2(3S|Z&8xwW2eC?_WQ(hND0yE|0s>s?Y&hGx!1b6jAL=h@J1j!2F@c~&V7z4-'
    b'_6~{Wa}k3n0)sH7=(wA)dn{7`1Bv8{U_V-urvM=O!RN43zd$5(3c(CS#sI?@k${VCTT>K$B6j&q-'
    b'VC1>RrnTf@X3zgjzrFd@#jD=pO{8YgT=PV8+Sr4xN3wxYz0_3#CbxG0j59ZXGS~&BoAT%e?r3)Vw3B+B{Bl~Yyg+Qd}cfO1fUcuM'
    b'(84F5vYG49Sw@Kj+4-78^c|E%3VnY!qSwEyv`LTLw+2#s+6)YKNuvNpZAa5T&Q+rPwqI1o46iC2xrEBoX7{~;t?-'
    b'qurTDt55dIn;tR{e;>r&bML#8&La(#*0rSsn0`F7~p6Y}sA_hu|*X@Qo1l!Oq;zL4Qq2=mpegujdMkR#F%=!IOF0w3wJ&R?+^jd3'
    b'P6YCC+WcI0w;hi{u`*~jllOc~0A)`nOfq*XH7~2sRL``Dj0OS+C0dfZP9a;}E1?Os^*4H&591oYBKC448p})wzi`>I4VOdM$Ne2O'
    b'}6T}c~WSfV14?3ziKjCgA79xphf|1wop1|%N(2mHs^Fo8dv_~)Lpn-X>NE9n@6})UB4t~(DMD0y)3#xb~fi3TDyWqoY*eD0xjtK-'
    b'J@i-CTKgF-bG&{Ch`nRsx6#3l_ei?}n6M{ROXnCZ$M!i_hK>M-wu+Rm^A&5-q>5gl_?dq$;aig0z{6+^WhHH(AvXd-'
    b'`6;%nfSjX#4ow%LyMH4{AHi$T}zn`_y$r`u@b8H#gBs$Jc#4@PU1p81-d^&-lZ-g3H$d`^2h*c=|g?RiH{XRO|`bhcqh4(-'
    b'yi|BJb%h>m&L&n5ovD^43>VQphK7dC?ejS7tq`nhTU+%}M;w3F0{_iC|!8Mk=9vFZi9Z{+%CSAk|I{ywj%XT79eD0fmoB=OI924s'
    b'dz7fNLTipo$_8bSVx-d9}`~vvGd|YnTr=O+|gJJyaR31nG0;Sas4WH0XKfEY-'
    b'4l8PS5TDFjpwJ=&;KYqoS~a1miKOZN5EB3`tb#nj6EL+~H#=&m43I--sX>w_&nrmAktFU1AiE1rDzf||Sy6nLhZYFsy2q{n{v5tV'
    b'(<gA2451I*;8Rd!ME^~Ef}`MK^QIrz0xP#^|90gC&;i&Lq2}_TD*-*BCgZaSWJ^2}36yZ%Km>s;LE?X`7<d<f-v^DoQ-c-'
    b'|TL^2w-Z7#V(7Q3@WIP3Ai<gA1psn$|wd^O{4MIX;Td*pGNq<;Z5z0(S6!0S?G-'
    b'fOnw@9<;SQ!nNV6RYLaP*}~ZLS3oyS%O!5GjwsMt4axHUoH>$PXMN<OO2_xzb)&I6aA2?-'
    b'C<WfDQfv4xuuU@GwXqJ5Qa}v3roUR87FgYX`6iw78h-'
    b';muz{Taq{)TF1dk=&wQ+2GOwSJqAt#@gr^#nDHSHtd6i3q8N=PeEQj`3~a#C6Bq;L<EKMs;T76Au$6S2mjFe*VcUy1H7=AQ&l3qF'
    b'<-R8-d~|Wi1zsdi^i)iGC?0r59flH)8zCL;x37-'
    b'IGGPnsLSLgk@W3DRgUR#k`@#>1V`WR3BpwcD8bopk0n`E|oC0#9H0>8qff|@7%ko2$SpRa0iGwdR0WZN)Yb(z-'
    b'g2{e9+G0%b2xG^1*@s*n(EajOKQDzr=8LXGQVA<uBn~=TU|;88;so4Au&h|axCq`-H)u`tfHIAqULhoU#wJ-ua|0`&?3Bc;tPXOU'
    b'-?;TI2lyJeH9<qUYxeYLw~tS+!?-'
    b'|S(UB7ZhecQj+5rgTL<y~jhiilPI14w$Wl@l(Q_Kw4+v`09Cwwg&X8==pkm<yziGagUiS;90@N6n3uchM-Xp`eQ8(1B@_|Hy3q*?'
    b'=@;Iyc}fGZQ#JftP%T8LQ}W59~B{|3bKiSPy%29pAw)6Wv~*fymj;677y;7a4I+<PPjBNYsI=E>k3AZ&+q)wpX(7op5I{@_i)%OF'
    b'WQeZVF_ei#VaB(KF2VR0-g&WuO*B@DNVhMGDg<0G;2`X0QLhCx*w2m+!=%+rqLiFzR@$-)3<-'
    b'Zb3>4aFL_j_Dz<a|$umdzwVlK2@hNSqJec2~GK_GI3fYJZ>s-'
    b'+VdrR&L)*faM6|la`ojm1WIvLWEgM<pO^qvE4lH_7zv6JSVK2DA2A}ZhiNr}$pJ`pne^gKM-'
    b'@8U85UtMQrH@HMtH#su)>TESXrmV5p+R$#vldA-VsJe+waFn(AI_m>X|?fN@2R2CEIAdMy!EaXo)jOhK~e8h!8qL7(>TN-'
    b'x8CLVmLA>d)QVC8Z)tEL~)C2FQUSpI&}lO31BGKE4{FFlar66$k@2@d$#3C+Xr1fgKzXI&q$Rw4=EWN5K!I0*e#;!EjSaj^y;7&#'
    b'rWRcZMgRhAOaZB0H}Z{FR%vG7uuz;$KsusG-SKud;@~G9MYuIV}!(y73(ZSV$RV5h)LMifg0j`K>w{eKksoXyhCtNeCCK(Z62>ca'
    b'D73v67!=0`VO4|&I!5+{e$To2<dQOIDlo)xGOGPboOEs9?uT4%Re5@pRnop!hX)v(WDjoXNB<Ds^eB19bJ`&0RTMm(Dj4!k!(bIN'
    b'gKWsZiavW-'
    b'?|M&LeDgaD~BJ1$Ph;mhOw6b@0b`|xu{%t;651|A72nn+NOoXyWPM>#1)H(q(jA4^blGMgo0HBJOmoFFf%Y!7v2!HmkJP@gM@FZ$'
    b'&sQr9K8DpTt1gIottzxE}Q}shrsCa`HUGXH_5@DkKv!14)BTHx~CX0`&e+Hk-'
    b'=U!cwE3lz@A3HX?zIumN2FJVMAT~d<>EU#RJ(Sv{y(#13vc?ErBr^AVE0s2`4_<SpE;nLhXS3Q}4H~`MW-'
    b'*xv0%uw@Z_VR1CZeJ4L}G`2e&dg>^2rq%*WF^Wxvj3ybYndVug+QBcxGAG-'
    b'}WtBwKS6q~hf6>>Q6arB%n=oV`X%LJ1gMCs#Kt_=(U=)|MIA`?bI!6)D}Hbfi-+so-'
    b'2;&z8_rk9TNpm@4m0^~sbpVOp0>wWH#Ao=(=8rU3AXhc{*3I$eJvVrY~!_Ngmf^Rrs?)T{A;M<qdnJ|$Jq$E6ds5xAkXixzEvcpU'
    b'PT8xuGT`yDxh?#8*Huz-N_WjryZbEv7rMp(xGzggpO8%TDU{R0(0$0Z_F`cEWMerR}i>%D3ZD{+C6(a`3{ZK2eD}+4?0q&89m>{g'
    b'X_wG6~6w^UyvSE$z+@!P{kN+#p&mBMu!NfF(J=4T34C^B%A%|^3ecTU36mmsCt-'
    b'2cV3#Twi!22y0i#kIek~b%$;^ZiB9t5fr=P0oZnFuczdPid-?WPk-'
    b'T*o`{*n3$E``Ck5DV~re`3^XVFEKcTOb|VQow2<+@JbL{*fzd02-'
    b'a6pH2hAW00VS&Sz)^+ivcx+gV+?S>szsiO==xxgQ<s05UtQiAY)2Tq`z{20T9txXg_E-Bmtc#VZZK#_T{bPpcSBU%1?X3Jn<$=&j'
    b'LQ9xB7CwxX}R!6SPHO?R4h^N5a-xZ3A%-A(;?9Sa=-Ltynjhiwd8RrPV)%t<@Yd1_0^80uBt<t2jf43THw@EK#Hzp25qBJ-'
    b'b+P%u>=drt&R?{0eVE(;=@;B&IE;n6$Ht!ac0$Mwn>3n|QP^YMo6qo4fA=hpLwEtM0xcCcOt%SBHbT3?>lp-'
    b'2pW}peR+6M7c~yr~0kk6bYbwCWhfUfAaVEFl_`qUI_P4E`;eqB960^?^P$_>sIzk%9XIJqmJBH=aGk>5|95%pTcP%W;}6EYv~wYW'
    b'^;BJKrYMGQR7MJI9CTe9Z@4St%L-'
    b'mEHrn2`!s{_?9X+vBeY9FNNy$5^*(UE9{FhexJ4qB4^;4q5Wf<1Vs+P_)9bHX^AeE&5X4(o(qz^JQ$qf-sj1<k5fw2|H~4DGu@bA'
    b'&fu!nAx?%dS-6UYTb^;P^r$8I)LGdi*It5-TcRL7S9biN>vywNEm`MV;V@iJnG-`yksI1LGw}d8%G0IhzXNu^w1`iHtgCUL-nPJW'
    b'P55_sH{Yj~G0tF(bAy_bPX}Mky;*~%@1`bhNcX`-4GWAAa@eGT;bqrq8FO?p_*L0SC#0jWv7MQ)*6Q>Wb=;s*x$-'
    b'{zo0FcT~z5|)OXC$DGkDn$IjuP$!cQWPA<;B<Ma;w-'
    b'4k~hNZFIczx0<Pm+C9qL|ep^bW_}OqBGM8!CiVj79k*UL|OstQ0qD@0UoD&ToWb-'
    b'IN<DfwKOkY4ze{ahwvO@_;hVU8$gNkg>ebChZieF&eu^@mkt1y=9p*O$Mdx8YNcXvGpbVWgs0A>C8JC-ZJM4(%6zoiU0t&%cBgD$'
    b'O5)Z!_I0k!x1<|asTo@qo(Eks>r&!t48fZ-t)AeBm9HIJ(WWm?XD5q{ov;0lg^yHlq~NwMZ_v!0V!HBexHN*@!-'
    b'57>o^i(c?Xmw&|LmhdW_u_U*b?B|v&2L3SgqJupgGvV%h5bmW^qq_wY5jP47HHZqd1Y6G&rS&ET*VG6oNWlo3))s_|?-'
    b'k#Lz>hU`-gQf|5aMmtP~q2UAwK-Mw0ckW>%mO+)gk_Nh|R9Mw-'
    b'7sziP7k6d(;GK1Z4`q;1NhChjo<?@F%J0BS!I&oF8bCZao6LF4XFLpdHL-'
    b'E4BtDHOvwKYX_n61y(KUnz>=v*k=4VGJr6|C01Ho;pXT%UB|_m&Z@IcfMJ(Ci^bbOVdCt(xT+-'
    b'hvD{wR>IfU+ZaG?6Z)lhDus$1YFL-PcI*am6o=ItU%3zG9ETnqtOK2;e4euy>P8~_&)cN3mQch8s;Dn2EiR!M%4iAe&095Y2x=;8'
    b'xYND@LjomSJI1=0zC@I;4E-'
    b'{s@xu1%PZ2?P`@Vrk3ER;fd^y9tAMrayNsRSP4FVC&h^aF?@j_%5k$HNj#eD~tPUhs#;zX5PNp){9|H{7}r$3qk@cqn5Z*Ny$=O?'
    b'CYvH>m?@0x4(#4@m4o8@i443yA$}xa~|JDtcZvKZAG>iJSy<O4Z<fz<Qox@gO=-u9;Bn<vO_8-'
    b'#En&q&y>PaCco3fYU@7A_ZUS3!%VoWPx%j3rCn0G@h4t#MEkkT@&&;w~73^((nlO*w(<ncz7(a&&Ahnh}a>*5S&6Z9qtpru<4aPX'
    b'6Yf}DlvdqWAZTrt<WwE3m7_K;u^8)EY@_TS_{Nl*HR|odxvfley5zTS?RV`dX2hZhm9!DEJZ%sZt7N^dKBy&Vz}}~>4Wr8a^1Dx@'
    b'$nIva$@)x=NsErf-ww`Pgu%&fkhKeE;xcsD~X(kTz!|I5|{-`t?v<8ao}X-'
    b'P`B5L5#p*!iAOC=KD!iL9Fl(c#Zd^171P3mbVnjoI`voX)Ra5BO=U=5WveD-'
    b'Qf0UlQE|gSrlj4~(f^6?u7ykiPM<rJROS!f1jIU^h5zp-MRr2?fDKSKHBfr$+5q(g2Ee_B!_If+)4}xkz}(N%v>s9<RxcOcKu@Yt'
    b'$7U*lFH@3!ebPb+sac0@o8{+QhRx?p?k(==D=wF&c42=-'
    b'UikJWwN%Mkhz(?U%T9DUeGV87K~2lK!HW9zX_Cm#3Qz4}S3<`PrrYWby;9;d-'
    b'b_4aiB*2216U=1LU1yi$HkOBzSmTB#=1Jh3<1in{A=)dLCm{u=|;|Tz>Zsk4qGWlshUfvAb6(v$M+1%)2W0;rOXB7*nu??G;ywly'
    b'*T)>iIB=3y-'
    b'&8Xkm8^!(j1|C{@5AHLiOq*VOdmh5E#q)4+t<&%$J9Jck6l1q2x2km|0V8j>JKKy*G)NS6CI6v4QHSELkGr%vp&bPDqKN5~Qp-'
    b'?D?v4qh>VChA^Bb*!;XyPsq`tY%~6pO&HTyp{@*@gl7@*@|uISS)!H|JBmslc8~{`Y5$Vm?m?#pSLs8LX6Oi7MQIu~mF$a*OjE*2'
    b'RUj6}IIwqwSy0k%{#bgXs>Iq0C$F)>XOglZF}tHXW~G7-'
    b'Ub?x%BheED2?uM2zDE^Wy+`so>|VWfg>P?4VBB!?gMb=MneEE12;jBdV_-=~KSG(IGE-TS^XH|q=<|FkxmG|Zv*j6fli=rFC;lS+'
    b'C!5L`7bbXfC3FNHjsNBp!`A{@xe>hrd}!3r(2%`JYPiaQGIADegNlS2t|#SS09dMSP6IKU<GaMeTG0s$udYg(Ih0wA)m>H}KNfd~'
    b'dtPMG7z%>7DDN#Ji<0&Etq>Xs@ncg}(J1lDJ0gpDPfyP&TWQ02l`BC2lDD8^YD_vRD*`uvGwdv!C%Kcr01cGH+Xay-'
    b'|AhIj1&u(#BbG)pTr?_o3*4Q)+b;Qc-cMoE3AKywP2EoALclt%!m<wMi;5Mz-'
    b'i0R3P+%Pc(~U)<HiR%=Cc2|avzjChQKScA_SLmMtQ%k<u3ty_dW4a=u+&{Oov8suR}A^%aEDGM@Pk1R?WaWYN!(^<&P0(a-'
    b'(2NIuEqf>C`0BwDS?3cNb_GZddoN$RE5RE7Hcc1pay(IWRUJ1_rSP?owF*3ocG#_Xe<zaa@#N6aC?+#pFN_DmEd#&Cg7&iqa==+j'
    b'?(U;YI$m|$^qI+uGN)z8s8pDrFhUY2s$(*oLp&k=sSEG--2&tym|n%JV2;;H4zA6j7Ecr^|0Om0~Cg|R8@;hD%lPq;|C1p7yJ_Wo'
    b'<IfrBPvBCql9pLN~ad4Sw2=UOOP@V6S^52%B&$~V{c^#aUIa&f@q<z^jk^dXwtDaj|%iuJnLKZgK41&>d^fy=3LW6V(y4$?J8^<s'
    b'^RDPc~l}$Oz_hwA+nJVJ+h*|^Ij8YZ2si<CY1o!&~L0nmma|}{sn;>Kkv$zBzz)O4I3a7UziCl{VQMUqskN9XQ@3ws6*L_e9BT*7'
    b'48R_Q%SjvoOHvF0H`YL2|RS?pO31B;_po3Q6e(|C`R6YTyZ43Ma@x=4Skrh{**r6StHe6L_Rve@X7&C22S(!Nm~i$2?59yG$c_Gs'
    b'eV;Hvq}?VthEynz`IOrQE995shO`46R01b&_Z7PPL-Qjc+Sxa+HKUKvhbGR<!b(s`o2#&XKMefGF9PPoL`^N{xZ8MFqk?_(WF2>T'
    b'L&}K-'
    b'm2NejX>Tpk+=i{f_lPHh%6Al4nwIP@9zYPC)5U=FSyd=RYMf!Lv4_*I}_BQ)yTQDB1W*4mkZ6}YxQZcoWJshe{~<OwgIl%89))4k'
    b'4BuT`c)^6Q5M{%mC*=8AZs1!{xFkWDCfbLZV7*7EA{|^0!FYZL_#ri>eH+QKBZhYUyT@hyH)6Zs*d2>trw6G=>WfbuSZRpso};Ld'
    b'NBzR?=bD9>Lg%XIb=vR^H~s9yznS<_j}e3ki9&9V5<VPaQYc8QVpJp3~dor%2qu$6xI43rgMs`QpP@RxVxl$@F6(Y$LObw_R&s!a'
    b'%;1a2&PU#lnQPZ)h8^Ao+8{aEvT&Wxr2(Ms?tW^q#|ok#lWfn;4geBJkpYK-EUXRrredP>ZT%vt>eV;TxUi|`c}~Un9vfHfR9y5&'
    b'2Yw=)PV=Fek1XuG&O|Dm9RXU+7;-CB4Cz;mR(dM^zqYRGu{SYuKEHfQsZaUG;FKbjZaZkYs$(s!bfh-'
    b'1?{PG<JvND+r!sd6E(R#pq5YeQNo6jpn(FW+Z-WPblZeU<_SA*-68r-rFszZQr~7!A31|W#+-'
    b'AUG&{(z^C%e5(yjJ7EXCC2crU6?4RB-JQztqnB9Lb)@pqDa^}6GAKtP+b>e}tx3@_dT#Z&n=?i<_Ve|rs6Iep2aJ@+{WX7+LJ^-'
    b'u}-b3cqe=C@oeh4?<TLs9)u0dfcdL&Z3?9e%8-'
    b'Q6RgRkMWEjM}~t*WgXLH)lMigQ78LYq)KR}LQ!1mI)oC{t<X@XjkwegDo5Dn$2&E%vM80)pza1s{WxORTc>qlu~98}_$SCJOLDjF'
    b'7^d%Sb8i);eT>C_MQ8Xd+ZoTnquR(}BTqtCuLqenoS}e~x-(118)^k%)8`>10dwkn<%pKIvKE~EN1g|Kz!n&%Hh1cPadjr-{#-'
    b'90&UaJBh<YM=ziJ$$x~{jS**@vEoRnYNh?sGe(N*9Uk+9t`X<pE3CZG<L_Qt0SG!tREt8n)xPN`@-'
    b'@5HC1omD7>BD`IfU3JL%`WQHF@n@HFHPx@d@xp;fBb(ojdQCmJW>UMfJJo}(G=I`JM&;#IO1%iVTX{hdlULJ_rPYF9*xO{|UQ9f1'
    b'l}_tQO-IVeblwA^Sj&uYjEKAL#d7IvC-'
    b'OeA<;4o9w(?K8a3)Mlv3Ka6t{`>N(~dH^bZes)I1yihXRIZCS?#$R))leWf2mflXu_alsB>(d3Qgcm)+&~OuBMbq-lORG4t%Qay?'
    b'E|+Fpn0#PC5AM>iC<>+P|cSf0SYOw@Cc|;KfskyhIVT;TShhuxqK|s{<`vt=)RpoeB7HdsWi(f)l2)1ZKY9!Y7qWqXE>5@oe=pXh'
    b'n%!C&g<Jnwgb*27MhW_NnE-HC$PzgmJ^wf2V8aY(YgLZ7lDFby4SvNOW-4Wr9{j<QBTR{cg)@+o3e;0BFWenE3e^-'
    b'3*RecUpn}g1J#CSb4RYc2)Z9;n5Vf;v{0Ng$!I+d~O+b^JZqU8H=EU#EMZz#+&$`VvVS!sqS97Sy!5t(q6AJ4$`RwEmswQ!doAXs'
    b'8uS!epEN&lJ8d5Ux0YIiib|q$z4#du}kbUCEGq-Dn<jd{o_+eL}SsL1g|r%K}6EEhuTHWByn3#XBVP!*AseiITVZ_uyqwi<b1Q8;'
    b'i_;SIMLc_8bUl$=LmMjkkrb~d9EA=ypnH>{L90mX*ZNZ)7IM^W5W^D-'
    b'C5|1BnzpwsSKQa#<0<P3^3$eg8IW$h5w{g&sW_LNBB1Q{x0tK(H+d)%9uzu#X@jaG0p8siNs^7I$F)4;?rn6Y$b7LH872(0w_Up;'
    b'A8VE2~GuU#jVRLC{%FKzqtZm%QC8eruCyvTxw5-'
    b'S54_#wM{^dtnhVG(KopQp%!)K<Q;m)g~8bfx7Zm)4p~y(wz4$U?ztd7^Hp;RgsHmk7H_|^3J}91;-'
    b'8dm&|xKzfu*Q!XP2U`9d}8YL7Dl8-2?E8E*K|-6G73_-'
    b'~Po31(5kmQWt~nRibm*1?<$`98I3onyLyt73P3*cy2qZP5{V$<%Q%?zbGsKLs4@+<SLvosv*?|A#9|lck!7q6W)2ugtlOX_@oKnj'
    b'`lZA`u94$Zk6qb>hr$3x-'
    b'!`bC+VCFLV>}>s9RB$mnPy#j_66A#?h<u6txEV0SZ%&PuT3|+IOC_G4=d3(owC)&85eERnSBLVdoQJqE3J`44-'
    b'>`oGb8A7TH&%t%H-'
    b'L^B6=%HLZ6dj2|`28A?4I0R#sdpr>x?v`%Plq8F*FlkN|p1v{5WTR}~h06%JN^lds90HcFWWcN1pZma5eZ+F0Zb#tX0^zi1GcmaQ'
    b'!`V|D|aolP#!&2ll;T~p6$ejNuQimoS9#g%BLR7Q~JzDyfQGA8P-yHP*GNAY-'
    b'8%Q%gL?esKwpANGRg{dzUxf6D14;vl(&7wD<!l(MT3(05r@t53W5YV0uDnHwy1N|kAp!%b5wy3X875pb+KNOSwa{$P{G?VqEw4Ag'
    b'grG)#n7&{~jd_MTd|<{%=&7=}%Z~@P1hAQELd`EAMGEhOZ2P)E_qQD%!aFfmRxhFy8frF$lCND>brIFixb11nThzH;moQT`E{31;'
    b'-5(#k0O8LC*abwq6H~%cFUP4$rRH8#2%$1}H7m~PsxeiAuuL_$Q{%2*iN#;lPyMQ<J}}RW+CKfc`WzO=RkDJb2shQqjqPhbeIC)w'
    b'DnUX;)Bsu-i0u1!o<e?vH=k7ysB#R*+-j`8a=oYM$Vf498T4JJzdIO|i|`h@L}Lb-'
    b'b)~;n|9FW_^FrF`RkLnT+vu<0t!T=F^g>SN*YUyJud3dGT6OU@Ju6Y%^1rm}?@+b2kZbB_bs7t;z8uG6g~8>@2dE)a+-'
    b'+}NIq18JD(lrk`djItpVcvjPP1~xm!LMfAu*o5s*Qi_LqkvyQv^IE=?yj7XK8j(-;G~+xbRUAJC^;Kh|-'
    b'Rmy8YbJLPK!JtCnpDW@L5np&oSz>D-hr4<_`hlcv-2pC+jw5K?T11s~vR;E<S6EEVBCRGA7-NEx|`c-819?-'
    b'~cgmnA{P&l1B}v#2R3{|t^&b*D>=213zR5<1agg~IaiU>ds6#r=H{xylW1^{B?q<hhGFZkgH)4-'
    b'E=A&#CXuHYTukb+)A1q5PcmPW3W|+4}B(i^TsvP}KTVVoy|@ioB865gypopaYw7UG#Lewy6@#;w(awm{nA8iM{2od_VQuuDQ_ex}'
    b'7xurL!wpoq2LTeCtu)7Q!~<f95oxhVsgx&b3m1>WB9`PfVN`m=?ke?J~?jE7fPF{*U4ZFvD7mPfxI+5dvF%4^YRMXhYZ!f9YI-'
    b'k3dun;+w`kZp~ZKAhAv8xEi}-'
    b'8o$wshG4~{@n@=AgoAdEPf9DYs@1P`ID~Tq^(bCW48Ll?qMoY!pk_BIh;M5Lp|DiK<r&mr4OA90%6rg@RLEAJX$KmU*7;C8L!+TK'
    b'5iatbssqdX!#RK#A=i+Q>8QyhvF!D5`AbF79uG&YXaKg3x|&@lFgmo=bR-'
    b'Q^3%%(8CBl#4mJxA02!S6T*ySwAqmh>CCmA($4fm}Fl2}UT1H{}yMJ%boV9eV!EN=4DHNZ9BI~d0*bQH9e8UoMDVQ9t~wBo?ZcG4'
    b')7cr@}Or_%SR^BkmPQDsv7oktxXm6>b09NTxNpheXwm3@Rl#G~w}-FQ;e+1dO+fVDlhjcPm<H`I9ixh*@^9D-'
    b'DzGgR*yPY2fyI#|=Jx2iG`wk<F7^h~1wv1U!C+fIJ>FAZD0;^9a6KWo)=m0{b|^gmrh`_mL?2G$^qwTG&w8<9#QA9@0N?04QzePz'
    b'YpBo(zhlHxt?-P84FoKBp5^~ql@wB0n-'
    b'GU;r_RF*S)s=1A=8WaGm|H`8d2oq9m$J3XlcL3FLVl|!Sz2XAyHD$=I($H2>$q{<B5%gkSY~MQoD95A}(7*$yrQ5MXsLSA*QW~B<'
    b'I+qVt8&+lIAi?Vn_o^%tlzgj4?KT~PqQx{Kb2gPPo^&*Z2N^8@0g-oaS9_FG1cgv=NrjY}-'
    b'qF9Eg!)xGlvFj;QnPjrq;cu<rZU;bXkPg8S*r#C0BTLD(fYh<_&t?;7~aT$s?_A1zEz*!HS>GoVw#WRy$<z2Q4`{zfpCjOuQOncr'
    b'rCpG&txB;(3T76MnkQz$q3qlaU6}0K+<GQ*b4mV(@!Ceu7=ET`V5)kX`gwbU*{&F@|_jCk`4hP(~k-e_()hrP<dJ`X-'
    b'dy$C2#gx<G{{w360*gU+Lk0%|yL#`ceEc<*V~MWrJX31zS@a?{519-'
    b'#~CwX3{~>f^(QjS<0%yBu4^d2QU3j?&*l!!?K*AvAa!kWZ|X|^axAFw@On_pr^D48%{-sjce)nvxj}lx6(rcMXU~oq-vm4L>{gk`'
    b'0=AcZ;gFyn!uy^J#3EVIH`G_4fRegDgDw!z4)YdEx^H4PYvcmWz~5sX@GgL4%H=m65sewK=@`T>yG?sO68pcy;Qxlwodji+v0sgs'
    b'p8fo7x2NK<HiNouWDVxM)0*&jn()Pu%&(+U~)lRXk46TVrLD4L~uRb=0_kPxcUVW*UoaCiPx^t)w)l9hA{X2OMya59Bbs6U8z-'
    b'?f3^>-'
    b'5d{UCM0;zTh7W1gNcaX))K3h2AFXfynnI$|97ls3XzH)}myI#5dS2qgHqprhS>5Mr4uxdz4C?%v@zEJ~`?`N|aLu5F44`yM{zvXs'
    b'-?||<8o!2&x@RBHDvs`I78x`IEfWw`toTcZ2YfQ*=BpE0II_+rENc)0%2w2hU*G+y`BW>fQ5L*PX9QC4Gr}0UrV%5M`^Qg{N}K9w'
    b'c{CXgW;oP&b8EDon(S^3vc%&x;e7g&-!`<EO$86t$D2p7HQ-R)_oi61B5?_e--J#s&(ExMG<2LRfr)E{IRJik;@OAsW&?ecZpy<Q'
    b'U5GgAwoxHh^MiH6HF{RF2W1|vYp#qI&7j4<`IIrA@nh(XA0`?S(Z=SM)b*-)=c+!non{C{eVF*-pnDp~A-'
    b'iXq017y6*RbFBmQ~F@bq8xU)=|-'
    b'p)gXn)vfyo5y)}A{I;N7Y2(DT2*x=B09H@Wa{(b~VwMl;XFD}@lrk(+|MHyN})h7e#q^><z152t3I!(pa2=}*H!U>H~i%#$z)G`+'
    b'X3OqaFl&IbLdD}|jsu@X}O3=*5-'
    b'qCTk*@y7TG8XI^Tm?ftPm&nVJTX~kMNUNzMF_x!CG6+C!1<9ow5vyRz~2<7;|Yri*_TH2>Hkd>18ZwK#>2GP6&&*f<+<_e{79-'
    b'drNOiH`*FP{EFKMH7be6`vy#?$e|*fOqX6E6BLO6ujfmD$FYLT6j}iE_Hs32iV6%;`gCafv7btt_%nr{3T@7D|C;*~<sVP9&)B{c'
    b'}YyOc;@k{Suep^+J+WCj8Kg5!CL+y&1O_2)^LX}>v=1IC8znWc$``Zmyv)kS|LcZ00UM<ydP+LiMt|qwZ4!V=N7EFvLclDP}2RV%'
    b'-)%-j>enHXRIf>IS;u+Xljgu`BgMRAvwJS&mwN_jAlDu7I;APd=-'
    b'g*ohy_Vj?1>~z*?U=@>^W0HAW?TvvM`*YOei;EMDg4w~A{cX4p*A#J_saV{S{+xTKupX&Kr%JlTSLmQT-'
    b'^Ygh9U+vGvzxFs>%?9cP}^xgzh~Pbz+Ssg|$62q+8wdrzVciw2G?#bT%@e>QOCI!J(v1P1{Q{=QURQHc{`WLqyTc#cVoQtVC!ZH5'
    b'7-FObw<|lUJPxsyzJ$v!pS*s>7Oq-'
    b'1_#|`Iqq<wF^)JU>cKc4YI9gR>)P(*id^)5a?ociIv4HlB`z*L=)`ZCaG%!t|K*9#eD<hQah~{SSYIi7YK1`ZnI{_MKu@=3-'
    b'OsNnr%Xz-*AVW5iHPYk|o0A$tJ15qW4&Ct{8-Pm19VN_)^XcKRMC3Il&>q-{|-'
    b'6R?m<K&u8Nu%Dq@>@HX=_&Ec&|46UkYQm<4swe1c&=`tn_K$!Kud7|?S^?6l-'
    b'qEBTX#R_lA>MW<3nqF?md~T^4GzeCw5lU9*%{pTIrQMX3noWd1!lc+w(oNyj(9k`zosHHt*gG!c&;?)^?nvlJs5aB&)b=k)MVCmD'
    b')MZO|`E~3TH8;5MvmTXB#tJQ!MQFMw?2I@BNG6~=@A|hD|GR<c#t}BiR5kmYZ6nrez>Q_ijCYXk8XVy%+Uro>qqK%JG?WeY|8l>N'
    b'F0%jLssI1eO$Qq}&^-vja7@i=JtA#2vmVl?*1C<jbxa*Fi)l_d#4cIj+gg5yv1wBEZknPDwGWNYLc;4<-'
    b'_(f+UWAaS7?cuOHDD2vI)$anP$p2tAMRJ0CX4bvAZ%U8hpV|9u*jNq7o&#ss@vTfR-KDKQ|o0#C>b>C&!Lp5m=VohbuR<tBnV}^J'
    b'h59vrz+@zEH}FHo&exyw*5t2DJw6&jfX!XZNIE%<~R8_Usbw&Q|s|nV(_o)suE)|d`+$45ywHz&@_<_$*dy+_1ax7=mlCee~|TE>'
    b'!_Tf^j{h^&tpb=>x>r_sk25LQg`fZw~nBm+bgw=Kx-I!XQJIYo>4V2>v!htLsCkQa-'
    b'gzOQ09?-X9F!wleX7Vx8pKz+Q1DWs_8JWPK0{I8Q-bYRjI%y_ojR6gej-xyfn<zH8vChtP?y9rKwxuTAvYe%F%Pd#oDi|Rv(zJW('
    b'uQOgSxw$x>!wO35s6qIB5cMdnz<a(!pTQZMU%b3|H9rdOkxeyzw55{ozY&<>%g^CY^hZXCR>`lyf3T@%iGmn)p}yQj3W3buFt|37'
    b'Y?d&Yq~h$W|u}s$jEYLf5Zj{QS*BAs7WAiQWTf5K)l*9RL(@|L4e%2X}t45}q9+s_5Pjv&4vb)jT<2dYJ{2G>!H=$KIFvD5)svw0'
    b'7st_Ku_k>?DK7X1(fcc9`0kK`D07@gQ#)ZBE@RA)ffej}!Ga{6;Ln)aZ{u4RL+)5%VHosq%BwrvtlAkDv=x?Vfbb>Pljo_ha*`VW'
    b'Rv@eA<epdt-IVk<w;jh@g6vZ^kW(<lQnt>XfV86M!T9(ro8^S9u!rLjlz!KaK`HxIm$%w?PwIb;KjTPXGs-'
    b'SX*enp9pr%R(`4SO<=X!?*ZXO2Splcsu9**1LKAU+pLh_7@BsSG?eG|o={7-B);Vb{mxk{*;KjFm=oz!z~s|&90Oj;Vrei<fY-En'
    b'7YLY(=Ds7KZ_Vv(EgrX8b&6$H)fHDFzr{m9$d2(Alvm|fjt=VEQU0;I_ccxZs?U|}4^3K=pM>2*AOH)E=!R(BMSxK5`R?$!sX10q'
    b'vDTk)x;(fB((6Ij$Js!dH`M`uSNg808ou<Y{K2*Gf#FB#(*)Cy)Z%42NQoJRszJXn*YPLg1(cZ^HF7m$AgT7hPr(+5sUGc`da9v$'
    b'KKJ6sOiUekjP9E3_HlrL$&4Xhug~#~p{SB9REG^4)D04+TdH`UF$u6y4Q%U*169M@{?b)Buy0j&VRZ|sa8#tJ6WeTj4gwT$*&poH'
    b'u<k23QOUn93L_Ej6+#HKpvFzlt%okw){NddA}oySx?a61jGGJYg%RCY#hjk8L_O5_G1(t85n$99xTBc1a{Rk(o4C^`8gRGMP+P$p'
    b'biiJZ8o#vF+JRS`{NCMdFFut8>MKX+aV5wigvKf}TNJ6>tbzLQ+~oh5nc}*nMUPfZwR)Q+c*%SdpI%iXs!n{!BBIA3{4IV5!e{8e'
    b'NrdAEj&36JOt&_SF@Ai@db4J<d(gz(9So>I1}8Owk-'
    b'$V$N6jLB?sigZx=~K<wW<>@pm|;)gg8bG)QaZhwY;o>l9X80lw=J#&X~YXa2^d8g=?ZBSoT&7f@l7x)o)dT);#PoQ9t>)x@XqJNz'
    b'GwIb)2CI!@ML?{{YvT6rMGF)j;OgZnD(`b(+pHFL)3brB=qENwBU<t0uU1o4MKyJoZAtz<7mfU+0O!^fMGuvuc%@8Z^AGs(d12UW'
    b'&wgb(<cVdLQ^;VPf0rQ32G~QvL5EvVXUM9MA~$h`D#3MC4b)W<Cl^iqlu+htDtx`OY3aUH+yfbRdVpm!96PaljnEwT4gpJcr8<ox'
    b'L>QPD80O``*jIH=^<g)d6oeC11B2r}~G#8_w6~M|xEBCHNG<&EP7A-4nK~(dE2@2HpB7sPr})fCC2f-'
    b'beg6_d00UWY!Ied=w2>khF0&9V+FGjsWjAaa`TF!S*HRhw;=Hm7n!?el6oZmpOcTLtmgk?ghx69Q(Tlau11pVWUBl#6xZB{ipBjn'
    b'zXV0()SFA{i2hW*p$m>p2Jk7TG0^Ok{X;V?VQkM*|+NZb=N)8=pbb${(hYAH|tWdbt6y`%wR}r<H$!0FNY7TLBmk^b_gU-r1M-'
    b'z0Nc0J2)MtE&U3>qb@hG%x|G<SH!NLq?<)dT`I)NBz{jHc4j<(`Xo9ZV<`*BgeqHtnhsl8c*y=B_`(^D27i#`k!RDCsyzs#4jc3r'
    b'5IyLPLwH(}h{{-LEGx{(>Sa5Ll``uk5G>P`Ao*7+3c9JqCa@Oq4qKU?MWP$>B4PXADN%(N)N73_lPMwd>#7pO`l-'
    b'jusjd|?pu$NL$3j$3?txELqMj(E3lX8Ys@h13`;&uZApshNARqy%jHJ%QkX2ZZABtG&Q4AF^7fY1G<FR}@xWh#*`U3iOTd8dBCZ<'
    b'b~2R0)XfYV8w{VWp@b>Uv2q9LSQ}n^2zAhU_Gbnz}<dHAN$^3D(EduR2+_Bh)%btz~Gn6qO{!hDIH3{LZ?&kE|E~Vj0vVkY6E)Aa'
    b'QF-Xty!;9i^}`I!#j6b%HBPKF%|h>I3EBCqFJVQZsQ0ypb{+yv88vDS3V7giCkib5?JPq{|ggLBd(7@Jr<u)z;Uuj{Pa0fg~Vm+a'
    b'UTWftKY==#bFl>E~2+P6T0V_Mo2Tcd$Yli2E_5qvNB-DWeRORStVDnp7}!i!+ow-Vq8BYONN&rpA$oUdQY;!>Z-'
    b'qdFPu<$Egwl0B3^C@KO26!r~QG)`$*(b+GJJb$A*L2%KNyYhnTN@09bWq7|BM%6ud}tBtx)f0|(5Lbys6)`9(97<qXb&c`!Mz3|-'
    b'j`JL(QOZB-I@~Pg-sx2Wh?JAu!q;~FR(=^y_A<e70_3`#Ng=unV4R4&ft8N09f#dd!<XAgvou(4QvDga9?GBHETWCB03USucvM*$'
    b'4`MR_bTayQCLhRA?si~FX$j#8>P@S%3|0?jDb(^D8lg+(UMtU{UYy8A;^-'
    b'wjXT!M<HZJZL^C>qQe1;GUWRV}0d!`G?6>;vei%Fd}8jq*D;JeSMr5OyVc0k#=7$WlzlM$kK@X8R6mXQH7-a}Lc#)^yAgA+-'
    b'Kpp12cvuWl_4us-}r=!W$^2al#Uk@u+TTSZ3U7Ttv3f}wdW%2j$(aobJBZft5GW!`kRkP8pVI;K2_PPvXIFy|CpQDP3IK|geA-'
    b'M@5cqXtZ=yrHycTQq)Vej7Gy9nDJYj%6xjY9COoZS@8J%sOxnI+OXhu-i0qz2Vm`-'
    b'qFI;&aY7$VI0R$k5|ARE`~{{jIFye)=u0NN2!156WYmdAq-CDR{+AJx$w>cC~-oaQ<IWl)cL+HwS|~cTW#KZ)Yv)R^{3w!Y-'
    b'qHO(1QCdjZ@3fn(5H{$r4KLfM*@LW2@KI@~a>+p0@jcF5SK<Gamq6)miC|v1tgOnFaMAQP&~OtSKG!2yG7)V1?d+g;}+sYCj#nCi'
    b'@@hsgGdmqdsjH#~o?Gx!EWrOV~SUT2sDkPQE%5+Vl3u027f5Fx1$xnh0W=uk+4j#V&8Rr(zVzoYb3&m)<Put#U+Om=Lbx9Z3LQ2G'
    b't6$?2nv(3s`Pzguq)9Z$VV!t6Yz+iqW&r(S4Gkxs`pYyJ1amAgHrb0g*C3t}WY9L{NFHy<B$m)H+UBd8xce$>ZuUr(`k=JXWkmc3'
    b'}q#TZ8xdS>mZgl8Ude4UhmN1wSA3i^{tS28>~FJNCKMNcDCs2BXK@V5;XWm_soRS!nHiM|O==M2BS+DcOZ0j1<RJ8M3BQCehz+2R'
    b'?8h7U($tyLSG+TRZ=kEWuZy3`mjVFz7F^bv2+N?L581tNP+iiL9EK0*Dt6sVOOMN`8VZZvzsLyd+(rz|k}kplY-'
    b'^@DQ4AX{Xjff*QnwoDUGKNprM5l*$yt--lBF1LLF-s7E&q-'
    b'2*5BoOYaimEgN$Xe($ij*1;MVJIpiD#o)roTp15{7!XOCS0*7fz)8{R(1cUDub*`-'
    b'U3tt=2#{M14Yw~R|3*h)tbAa|9f3gu%+0O#+io;CsAmORg<;*I!ZXs#lTGUm{tK~RyQ(rFT1V$Attccz;9$oNmr}FD;`gLQ3i&jB'
    b'HV$WP=ENVYy@SZKD3EdF3Q08or%F8UGlH|6ozQNd;uJ?!pgllr+n*L$jqy(i?LNGl9#W!a*Vj`oH`@4f5|aXOQj0nsL7Jf{07u+^'
    b'qukPoHP%H$X<2DiTw6Pus><e6IwwM|1eSPKv%|uGmT7AcY~{ITLsXmrbbZyg;MU~BTc=Xk{Wqe{GzY)4vrdOA))!B=dxizBFp9L@'
    b'&a{IRK7}8eozbmAEcKL)@fYE&rlFN){pr?S2c`6H!TE-4D(QBSV=*(nT_zBb);B^N;di2&9d2C=@y(AK>heIldzN2U4H65po-'
    b'C5pS%O8+EoCeAq`+htT7Iy3lRR33N!m2y7~Tjnt96@3x<aU-'
    b'%!$s>YZR&7m2EYtSoSj`{Eo&9VRp}<7$9>#VPFX(Qy9*A5$Gvw~;}lq%qDJ-'
    b'J!%$;%@6*W07~kNK!m$Uo`>?fKy5U#$oBpuOzfM^fr|v7tp*ZIm@qRe5uo5k+>@A|D-'
    b'GI!51PL_Us6Td2|Qzr{}`Jm=>U;M&3{IyJv(+5&x~cf5Kf^iNyQHsnGvW<D`a(x|#b^cb8f(z0`&l;B8nGO%3JYDnO=}ENvfGQ^Y'
    b'lEYJ5q{!-1%%<KJHzHG#t<jN58qkOTZFuq<j-st$1h(HvE6wNAR4y6Vb3S6Z9_*vQNIHcP035M@u~96HB;+#2LkW-'
    b'`Fq;#A#Bo)H;VHwt1NllCu~4BCI?<%v3>5PCMOV%=QuCtZ`?UX}tttV+R78vLMmLJ(6@vy!9lbO?R=o&7}BB1gsXE$gTTCq+V|-'
    b'b}rShfZUfnik=Tn&xaH)D<IE0Gvab=egg~>)-'
    b'V;ydFRB%!?Z{m!78%yg^je3Ecpc^0_?_*h@GYdd1HaNiy_D_VcwYGgzPcL@F~+?F28oq3TPh&Qkt-TqCPZ-ht5$e59xo4j5LSisI'
    b'kN{es2~55iI$EM`3S9{BXou^x;<b9f+N`5!~Yt;1wdDi^Ae;Y#Pc`F^2i_R_VN#E_za9!97+%PkMJ*&N<>>ALxhI(3UW&O=DDyA1'
    b')I-vc{*Rn%Pd#Q{FWm#JH=Mo-'
    b'QilbR_Om|kfX?W+0E0Q&8);`{nZe`Q9|rV0-hZa<W*E(+U}IR&Sk=}Cwr+Cpg$f83ucq8jx%;?e=R|1lO{qDE*v=_vWu-mU2V{w6'
    b'O<=}Pqytp}tz!r3*e(sVK%G)jEozkk<<|IgO2dLzSgRE67C^;#%Rz5RoNE9wE<o9zsB<f_O$3ow<fkv>&?F8KO;!~gvbUd}c(3+l'
    b'J4-|#(Eq<o~2>V78ojjK3|1Uw}XZDU%Ys+EpTl)#VI!-H~AZfr#@ZPiq5MDwmBQKc?7-'
    b'T#zyjY!v;rY<8LdR?aj{=LsPhNG4NCSD6B34W_@hou}9Z7@u1hLF-'
    b'M=!yvA<Ud!%uu#;lQ4Al`>y62GT{9<D9Ly3M+<6F{1|%}*PBHSwr)>3LgGL_Z#(K<ZdiizkwX%Bf9L-'
    b'^GIX8_c(^5Dt2)nRkZYAcU1EiIQY9Mu0bGIC-)we@A(VErEDnIpsS7uhS&KqO^d@Kw_ZPSowO=l*`-'
    b'@l^nTiK%XUs^<eWPZp%O$6B5P^Ax5UBIC}u0s9|@VOlF=_{xz68=;=*5x|oG^LJyT<cNt%&VhvBdd*me269<QgwVcJd{!`hEgj^R'
    b'5Q7bWP3w;VHf8e;&+NF9hV0EIaU&n?TJ29b-h|iUIb-Fn3)c6qxuUOd!{2OG<LAJup6c|)DCgQ5|7$@X+>0jrP1cNC!eFYi~UIiZ'
    b'>uJ6>g44z*;aq)L9Z{hN<tn2BV$2?n`W%H(GTKrx_m$H01d?2yUJiL8nH*BNxwONUCFPuKQ^+`<p_A<Bt2=Lw)sLhrWn((nhAxvy'
    b'lxKt9D%=|+tr!u>)ZJ<8e6UcC$(T~CpkZR(}5w?XmxEMTDeU)h?Fz5+Ei6&%``jy9pF5J=8nvGu+jxFKQ(6^BI%eL!_;(;95zNHG'
    b'%21iq85~hWPHP0=gVTmpc#8G>3lPP4-!VuAgV?gWivMLvt;RhN@s1vv!9-9Ipx1&`2PUgvb{EtesWOT^mb)hOBzST+{rDd(om<-'
    b'{8Z6LA);iEN-giF{<Y^o&z4&;thLRHiV6EjH~?{7UA9*aH#g)Q)TAHfh(w2y)B+AFr|0Ks#8oOL9zpJ>kHS2S=m*E0tsLvH3tK!{'
    b'UKK5>Bn$N>G2NUK?|$wXQW{x4Kb3+TSLwwkkbl-5SpDYN*u<nehN#?74LMec?oyK-zwfjNRYH0`)eUWnlbAXbt`7amI5lduguYF!'
    b'=F~p{G|163Q`B6d*z;Q!QB{J5;<n`yy%jPJNJOFt!4jf%HrmRGr1L!e&96r2Rgl1vr;kCDVBFPUMy+2b0+ZmQi5Mjr3v22?FqLw;'
    b'Kq+8HR9`6>1E`DEYWetS?pT7g7N?FP)mz3`0VFS*#3!Y}+6`qo=uyXT<H_&Sk^@fl=ZNfg9cJ$Rlz}xRp(a256a~>c_tXs%<V>U9'
    b'V23=3t2R0W9j0j%cMB@m{&<O7Qd&xNSLX0i-5ECAb%3l&Up{jv2gP-+s?Phh3^pCo-'
    b'U43oUXP}nx00tcuP7QX79geNDp^U!qRD<^4bN5Nrnsg@DYvOY5-_CnG5Rf*vDK-'
    b'L=?Ol)@h3H2jTjBSsP<2~W7K>B3|uXa8{wMxTG0c3Tl#wR?Vby+*aIv?E%FR-'
    b'fu_I|QRb`pXzJ($4Lo5UwAVCiYM>2=+VJ+Td9fGMY-WB}cjw)&=8Hv@IhH<}b&XO90FTtrMHV$Z29%^k0@@D~MaIp#Tj{gLG#ysg'
    b'*?*uC2)vDTjUd#W2h7r8c2T`xR@Xo_Uzff=>85I-dB@4R)>yTdqUHnzR>Frv$p67l(4R=Qp-'
    b'$tF=b#n^+dJ0v^Dz;;%xbb+OPffytdT{S^?GK$SisAD`2e4TD?^bVj8AhjgDH+2|I$4(?{gwBF29Th)?x013aaND)KoY3mw1KzsZ'
    b'Xe^%77#cuv`<^o#j`myWiH9RE<XYkwF;Q-'
    b'O%Cz!azvT2M$k)BTIF?W9TS+!g9KVl19glx53)%B`qkuS{83J)wT0f&0|taWUvy(uli#gL*q-'
    b'jx*auj>+En#<m}J+4WhDk&7jWh7UE3G8XlKbY^6-'
    b'Xz+><!z<s*eM^@YR!K>G$bnicxwP*w+L`dU4m8R{eY^#D?RTIJ{II^ARXi6OpPg`mN)Kq%TBCNePi7_Fe7l!s!dm)w&<{0C!I}Lr'
    b'F)FJSwe!AnTWj;kNGBI%C^tXo{>xklsW?7HAi{&j)$pl4L-'
    b'>yBZBcu>|Y6j&x4d>adJ22q(X03u|&&i}>kae|qbyK6SuDheNmHmVG&n+Xx)X>CEX>n=ELY|)=N`arp8-'
    b'lP~0Mf>O+ETBy)fmCpjNRi>+e8HHBOlcYkQj!`uKH)3wA%OE!XUcxW7HaH3=Kz^mV=U{R-'
    b'1dHMn)YMDyN&|yrbl12o~Rz1K^M^kCD&7v4MS4ldn3|KUeMRQiM;(0zT_bbu^Yb6FY*A1j|_ER}LKeC}|q{MQn?=W1dQytnmGL97'
    b'75!d?3W=jtoYwGsL1FiTx;x%rMiv@7Kw%vdOJMl45JIoOaZ7L){n$n{u)%Rl1d=T+g8?egto&xFNa9A1d%oI!4sSMx_!E10YapAF'
    b'|d>YF*;WLEvHQJVPuY_t4O8>L;M|gmUuNy$@AvD~^B)19&vGmsQAYUfs%lxa-'
    b'6n<<39=TUeByGUG7}A9;{Ij#E)zRRVm7^~_>fC{qBrhzHMNDuzAD)TY$MT@Wg)iB5-'
    b'7SvEfAerkrUGo1}p5`@O7K~6HBRI*Z_vqx3;j2e^;2tapVxu&gq{B=HdO$6O;;JCT8+gXVDv|0>p!hJQ0qO0|rBZueNFuW_QCn}('
    b'e(40AZJwsB%6gLsd!NrXNYifEOcbb!k1`Sm!)0PRH?BmkeL!AIKkFPe_Z#SN<@``=bKD+XTo}u&)aO7$HOPq0M<=sq0OdByvhF-'
    b'N92aEsop~W=gf}F0bbOYs9%EiJ)v33j@g{~oM&}L;%Xe6-QnD}wj)TY0KT(CC>YDd<3;JOIU3*SZ3YovlJAP?xbZ`6m%x^L-'
    b'9vkYqcdHm1Os%{nPGi^$D_^Mm6tOn{3m4f(I(>~ymHTJ2#O4!O=F8Kf&y))fT4k-'
    b'*s;nTnj6(S5B+TzL5qIgn)rRJM;{gON87vSuz!(IT9<L?runv`JI`>|SyB}g`9->Tgj-ySrqXO3iWCj=|v-'
    b'grYRt`11{^{|q*)Q<xV<C^zokdMI*Y)$PgkT&&4IYD*D7(g{sTMUd$S;j}h#>;!jPiSh|Y@LvIH76b_@&(1Qi{&^8t6>Dst|A4vH'
    b'%@z9tsx=yUl%Wblr;U<yk(tHm#Xa7eVA}j1w=ecy={7D9}z|uwCwWF0@X0x>A8A3odZ>UBLk$5UvEvVs?WVa75K#th%nW86{g%rS'
    b'm&CxD7kGo2ezd?ApM=Ogh8CA<#ksFg}dXy&LI4kw@N`B#~}5g;V1#Vr)e;7xOR92iGdk^Y0>*t`7~@$Q+w+mek%75k0wSz+z~z&R'
    b'87#^xfz~+jaNItl4{1kZp=5~3Q*%pC<xBi^N~jd%)<*#(w?@|IhcBNCynX>-'
    b'JGvdp$!ak{+T;Zh(YW<xQl~pevkTc&jAT7VQGvdlu-vJ(>0!H-AA19IfqC6GZ-'
    b'^!7{%g;L0{fib%Pp|iO9k3;Nt`n^dZLZbk%NKts8SAJ~UqO&lqx~)alL6(@AK^G#BWYT(?2I<5DX*810<k(nbZKCt|{)F`9q9EyL'
    b'lLUqUkRg*{UXsj8|7&~6dbhMMa|6oiUfiY`Wn%GKl6<i)q6o~tCJ>F@}xU{#~-(7H{G8<rT81|-1&h!7g56>ycOqbHGBCGu}8ya-'
    b'((s-~&}1GvRxbDFLU2w<22QM_o<OHO%T1U7^pa)By8a3BQH-'
    b'(#%){+Peeg=89<MB6W}e%4l#xD4~q%_I>aud0#cTbZ<|!wOf`6@DoyrUs+zzBwjpbR1#d>l9aJveFPyx4OTZ2wt_Y!0~VE)s@k^H'
    b'29&2J=_Woeyx0YGV`EXuN?`$R-4W@5iLk9kE%1$@%ma-'
    b'{fnTYNYgYNsS^RYUpk1l_hCg%)ByEpyx{4sd5Q;dNVsOZ&Q?R*c$CQp_ft0P9O`(vLmc0x;ufWQHT@}(MX4ze`KkfQ3GN!Mroa#?'
    b'2wS77(clhaYk-'
    b'E*pAjB!)57MVrLKAQ5Bb(Loq`==vv0LZZ7H(|4~NPSn8*jpc$S9FSu0<c8hMAHl@Mp}8GY%(p{aQKsun_t&{y{mgxhupLPo_=uvv'
    b'}D$eO_UaSp9|txMU+kZ~oy;jR)<mhCyG>egVAD_v!9N{318zzqD}S`ijsrwv8|CWgTJmzYz~G4$wr5fx#rMOW8ZHv+~!u}eDVpK2'
    b'9_E<5?{(F+1>!Y#kPn)^-'
    b'w1lZ#ii)crm;w<o}qPy8^nsnHwt04t1swS2nqaUJsg~D5TR{ftrv$1AFd9Ny8$l#p*q?%G3b&iRvX{7y9uK8O`$cHwyp@!K_fNrk'
    b'U;567z)wGKcjNMWKmt<L-Dp+W`3iYWhvp;8B&=@rWl{~yxrHFTpBYZ-MBa*vCwLmT+fC8&pyB`QJYM_YO{QyP7*}7lfO^IfQ&xDl'
    b'vhV}4wyhVZ%c?b^V@e_^~2<eEg>8@<dw-'
    b'2qBa1_^s2_1w7z`{UJ)mLihB9DkevOf{_mjHvSykT`CfbY)qb>F1+H2P7gn1;92s&tI8P?u5TEUP-'
    b'0AhUEoF~bb%JgNN1w8DVlrN61b|3n}2U;oel{Xaba`SP(6Af2`?WNjB@$;-}YwzA567gT@FaaSHom9Ofgdv<V%o2}-'
    b'CADi<?6Y2%1kFFzk1xOVOYqk=SL+!=mm_xO^oxrTpNgMnf`tiAKdVTZ`<<ei^>Nd@=YDlg43>;PlPDuG=&9LcD_n4-'
    b'xNV@ulOVo1SUW%@Q;oO1_sXEWl`z}=}8Zp=ARl}l34M9V(LTa(;(uQxAqn`p%c=cIUkINJ^A*|F+$cRySHb`L96w0sZ<RRVSx*<_'
    b'kn+2X6O1OdCKXEU>8C+HVvukpT*Qkl&VGT8&X``?nx?H%LK7o8rYEpQ&E<NMtO%Ok8*1J2Qj-'
    b'7zuRDRK$hO=R1g!VAh#GH+t17$6Cib!u7vv!oYo&FFVWbU0B|59~_I?8HgZ)LYtO`9<Fn<h-?2**;^eko-P);lZ_hTi-'
    b'2zhpy`zvemOH(jA}2z8ySQ?l7LdauKubz6J9YM$O5x|5TSJ~ci;15xC}YM!5X>>s`a>pfRpp4GNN_e0OcjA65#udhpY<3%Z4jp*E'
    b'<eW}}o^yf1-'
    b'dhop|KzTH5_w2Eui7o1aqa~$<>v975CLwwjJVg_#XB=ZDI0YKc<6FfnwThv$(pfp?4Kca9?NZuSezYd~!HHoltjUQ`9B7`|RtA&$'
    b'M!wDf@zWfwb4u3uO4vfx4D{V<j~cfUcC(6d)My10=Q_|<jT2Hu%zOF!QU0J>xp?1$MO$j>z0``-'
    b'2Y3uGjhBVjT}e@Q>8RY)e$>J&U$Jw|Uj3C;e6eD2;u9=*L1MQN^VDFbzPHMMfJHt68Hny&j!p~>4vr99{r(Z1UtMsjwr8yQ5P`0I'
    b'Y@P(y(Yc|AQ%gZwVK-T&J^84&h1I+?Ur^EZodg6z4@qrECNUGnkf-'
    b'W0)Pd}(SBBcj>dNO5<N0)*p~|5OGBW(>U_<;=ds5}~W~l7c(Ywk#MtH>hoICogJ6+9&TS)$`9IK}h7^K~QHr$fhed{Vn^MLRvLcM'
    b'Ocs%i@gtG2f~3uB6VNYC;aSY=9!pXUF5=b6Vxuw|M?j3u4Wqj-'
    b'#RW1_|nX_?WjuF^DuEPBuDGuw(dtotnZOI=^L<1Q0&lRXAQR)KmEVs~2|rVE-'
    b'ITTt^}k+lmk9p&mEhyUhjx|Fexp9T@wmseMa86y_8{7d8BYFF2zpfhx%?sgJfY#eu-rXH(!^w9{Yk6p8FwZ_Q-'
    b'<j*nck`zlN26&psRYr(Ig2U=5iLxUUR>F<yy^Chwe7#c<k=)b-'
    b'W0s}Mb!8STO=V&8^yg@Zqc%Y^fonTJ!&o3yFTmRN*I2A;{i)GDx;9j+wdBgf*3jO7BzC0<I${^k&^UyVRfned3L@n{CAM>HuWHS@'
    b'K&kZ<WbRO6(Qs$LVm(P^tM#Yy2@Rlh3u4PvnjC=iv&5?F1sh9L5uxtn*(-'
    b'vqdJ7gvVp7`$=!&v3YVm@|V#7jB>I<N#{(@*E`YXpn!%-'
    b'&@ZPxzG=&AU9(1da|bjUSdqH+p1SDnD1n<A)?=huyJi0f)`|5W86iF#DQ<l30xva(e$h345?gF2T^ga{B_LnzE|9$(k0&7(0aS@k'
    b'el!TyX})5X@t1eJJ*7GekUgrf5YaQvyh8JfK-gZ!NxY(6TnWlc2U+TcVW<<&W<sqd>!!j8s^5d+|$Tb;o}QocB`;Sl4MgP!i!{g9'
    b'DH8XTSA2R#28nhZiH@uTV?rQayo<&K-<L0ma-d+U0xDucZf>u}bkHc5VnO-;$@3FeF={I}-L<ycl2hJxw5)hqwO;n-'
    b'm3AHwZsK?E#jPt}0ONatWly?68Z2{coz*wchMuiyYyOMuTYQ=IPr>@g~$W876DTO2+&ni2c%La%{VWVdAGRTEN}<Vp=2A)Q^4%hx'
    b'@QB;;C)-0|BMrsx2uFnYl0-kszdNV;cX@$$n>+14JNaq$~5-'
    b'm!oDPstwV!YN$U11Yym9@*xl%Ra|zA7{z7JhU6#w;Q4_FLql;F!c2LaN^cFkl<T_5`lLQ?wK3L21#wmwm~5P9gvrsM+S$x-'
    b'svTl6@R?MS(xkC1vR%;_VZ3aBuyJ=QWU~5OUemPBrD81X0E;na4U#@d-'
    b'ctoJtsS55pU`6iKLqSico_^xF_=UVxxHSGcQCe>SeN2yNZ-5>o-'
    b'5Vd^E`TqryLQWy7{VVd&}|!H@A2DtI~ptqFd^bn+bToUwZnJ~_~{+gi9chgW&MB}E)0hB=W8NuiyWr(UVBmu+c6sS$$6WmwQAasY'
    b'o2kEcFJ(YF5m;0zo4gs_JxJgxXcp@PUekRPcK?<4EMyL7iHn!`~C{d$^#SmYJ!n_^HeEhnRnvr7^&@D`y~Ne0yeO3MO+pGSJQ93m'
    b'Z1R3h~fslV2@Xo@7YqDOqsWNCcE12j9vVZpQ{-y1(SWz<_uU-XWBuY4d)@vpy!pkM$00F{z=3I'
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
    candidate = words_in_sentence  # noqa: F405
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
