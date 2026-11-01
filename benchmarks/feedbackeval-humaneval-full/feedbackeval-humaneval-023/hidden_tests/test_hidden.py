import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[''],
 ['x'],
 ['asdasnakj'],
 ['Hello, World!'],
 ['12345'],
 [' '],
 ['This is a long string that has many characters in it'],
 ['abcdefghijklmnopqrstuvwxyz'],
 ['Testing testing 123'],
 ['The quick brown fox jumps over the lazy dog'],
 ['one\ntwo\nthree\nfour\nfive'],
 ['1234567890'],
 ['This string has a \n newline character'],
 ['one\ntwo\nthree\nf\nfoive'],
 ['The quick brown fox jumps overq the lazy dog'],
 ['abcdefgjklmnopqrstuvwxyz'],
 ['three\nfour\nfive'],
 [' This striThis is a long string that has many characters in itng has a \n newline character'],
 [''],
 ['The quick brown fox jumps over the lazy This striThis is a long string that has many characters '
  'in itng has a \n'
  ' newline character dog'],
 ['1234 This striThis is a long string that has many characters in itng has a \n'
  ' newline character5'],
 ['The quick brown fox jumps over the lazy This striThis is aaracter dog'],
 ['one\ntwot\nthree\nfour\nfive'],
 ['11234567890'],
 ['one\ntwot\nthrThis is a long string that has many characters in itee\nfour\nfive'],
 ['The quick brown f ox jumps over the lazy dog'],
 ['122345'],
 ['Testing testingone\n'
  'twot\n'
  'thrThis is a long string that has many characters in itee\n'
  'four\n'
  'five 123'],
 ['one\ntwot\nthrThis is a long string thtat has many characters in itee\nfour\nfive'],
 ['123345'],
 ['The quick brown fox jumps over the lazy Thisthree\nfour\nfiveracter dog'],
 ['GNDKQyadEb'],
 ['Hello, Woorld!'],
 ['of\nfoive'],
 ['The quick brown fox jumps overq theHello, World! lazy dog'],
 ['M'],
 ['NEvG'],
 ['Hello, Woorlod!'],
 ['thrieeThe quick brown fox jumps overq the lazy dog\nfour\nfive'],
 ['one\ntwot\nthree\nfour\nfiv'],
 ['abcdefghijklmnopq1234 This striThis is a long string that has many characters in itng has a \n'
  ' newline character5rstuvwxyz'],
 ['Hello, Woo12345rld!'],
 ['one\n'
  'twot This striThis is a long streing that has many characters in itng has a \n'
  ' newline character\n'
  'three\n'
  'four\n'
  'five'],
 [' This striThis is a long string that has many characters in itng has a \n neawline character'],
 ['1223545'],
 ['one\ntwota\nthrThis is a long string that has many characters in itee\nfour\nfive'],
 ['The quick brzown fox jumps over the leazy Thisis is aaracter dog'],
 ['1234 This sitriThis is a long string that has many characters in itng has a \n'
  ' newline character5'],
 ['TestiTng testing 123'],
 ['GNDThis string has a \n newline characterdEb'],
 ['The quick brzown fox sjumps over the leazy Thisis is aaracter dog'],
 ['G1234 This sitriThis is a long string that has many characters in itng has a \n'
  ' newline character5NDKQyadEb'],
 ['The quick brown fox jumps over theThe quick brown fox jumps overq the lazy dog lazy Thisthree\n'
  'four\n'
  'fiveracter dog'],
 ['G1234 This sitriThis is a long string that has many characters in itng has a \n'
  ' newline character5NDKThe quick brown fox jumps over theThe quick brown fox jumps overq the '
  'lazy dog lazy Thisthree\n'
  'four\n'
  'fiveracter dogQyadEb'],
 ['oef\nffoive'],
 ['one\ntwot\nthrThis is a long string that has many characters in itee\nfoour\nfive'],
 ['of\nfoivfe'],
 ['Testing te stingone\n'
  'twot\n'
  'thrThis is a long string that has many characters in itee\n'
  'four\n'
  'five 123'],
 ['Hello, WoG1234 This sitriThis is a long string that has many characters in itng has a \n'
  ' newline character5NDKThe quick brown fox jumps over theThe quick brown fox jumps overq the '
  'lazy dog lazby Thisthree\n'
  'four\n'
  'fiveracter dogQyadEborlod!'],
 ['Hello,The quick brown fox jumps over the lazy Thisthree\nfour\nfiveracter dog Woo12345rld!'],
 ['Hello, WoG1234 This sitriThis is a long string that has many characters in itng has a \n'
  ' newline character5NDKThe quick brown fox jumps over theThe quick by Thisthree\n'
  'four\n'
  'fiveracter dogQyadEborlod!'],
 ['off\nfoiivfe'],
 ['912345667890'],
 ['abcdefgjklmnopqrstuvwxyzive'],
 ['The quick brown fox jumps over the lazy This striThis is aaracter dogM'],
 ['Hello, WoG1234 This sitriThis is a long string that has many characters in itng h as a \n'
  ' newline character5NDKThe quick brown fox jumps over theThe quick brown fox jumps overq the '
  'lazy dog lazby Thisthree\n'
  'four\n'
  'fiveracter dogQyadEborlod!'],
 ['The quick brown f ox jumps over the lazyg'],
 ['one\ntwot\nthrThis is a long string that has  many characters in itee\nfour\nfive'],
 ['one\n\ntwot\nthrThis is a long string that has many characters in itee\nfoour\nfive'],
 ['thrieeThe quick brown f ox jumps over the lazy dogThe quick brown fox jumps overq the lazy dog\n'
  'four\n'
  'five'],
 ['G1The quick brown f ox jumps over the lazy dog234  has a \n newline character5NDKQyadEb'],
 ['TheHello,The quick brown fox jumps over the lazy Thisthree\n'
  'four\n'
  'fiveracter dog Woo12345rld! quick broThis string Thas a \n'
  ' newline characterwn fox jumps over the lazy Thisthree\n'
  'four\n'
  'fiveracter dog'],
 ['off\nfoivife'],
 ['three\nefour\noff\nfoiivfe'],
 ['Test1iTng testing 123'],
 ['one\n'
  'twota\n'
  'thrThis is a long string that has many chone\n'
  'twot\n'
  'thrThis is a long string that has  many characters in itee\n'
  'four\n'
  'fivearacters in itee\n'
  'four\n'
  'five'],
 ['TheHello,The quick brown fox jumps over the lazy Thisthree\n'
  'four\n'
  'fiveracter dog Woo12345rld! quick broThis string Thas a \n'
  ' newline characterwn fox jumps over theone\n'
  'twota\n'
  'thrThis is a long string that has many characters in itee\n'
  'four\n'
  'five dog'],
 ['thrieeThe quick brown f ox jumps over the lazy dogThe quick brown fox jumps overq the lazy dog\n'
  'four\n'
  'five '],
 ['oene'],
 ['off\nabcdefgjklmnopqrstuvwxyzfoivife'],
 ['The quick brown f ox jumps over the lazy'],
 ['abcdefghijklTest1iTng testing 123mnopq1234 This striThis is a long string that has many '
  'characters in itnghas a \n'
  ' newline character5rstuvwxyz'],
 ['abcdeflghijklmnopqrstuvwxyz'],
 ['1o, Woorld!890'],
 ['12333345'],
 ['1122345'],
 ['one\ntwota\nthrThis is a long string that has many characters ien itee\nfour\nfive'],
 ['Hello, W123345orld!'],
 ['one\ntwo\nthrfoive'],
 ['one\ntwot\nthrThis is a long string that has  many characterns in itee\nfour\nfive'],
 ['one\n'
  'twotaa\n'
  'thrThis is a long string that has many characters ien itee\n'
  '1234 This sitriThis is a long string that has many characters in itng has a \n'
  ' newline character5four\n'
  'five'],
 ['The quick brzown fox sjumps over the leazy Thisis is aaThe quick brown fox jumps overq '
  'theHello, World! lazy dogracter dog'],
 ['MThe quick brown fox jumps over the lazy This striThis is aaracter dogM'],
 ['The quick brzown fox jumps over the leazy Thisis is aaracter Hello, Woorld!dog'],
 ['1234 This sitriThis is a long string that has many character12345s in itng has a \n'
  ' newline character5'],
 ['1234 This sitriThis is a long string that has many characters in itng has a \n'
  ' neThe quick brown f ox jumps over the lazygwline character5'],
 ['912345667890The quick brown fox jumps over the lazy This striThis is aaracter dogM'],
 ['Hellone\n'
  'twot\n'
  'three\n'
  'four\n'
  'fivo, WoG1234 This sitriThis is a long string that has many characters in itng has a \n'
  ' newline character5NDKThe quirck brown fox jumps over theThe quick by Thisthree\n'
  'four\n'
  'fiveracter dogQyadEborlod!'],
 ['The quick brown fox11234567890 jumps over the lazy This striThis is aaracter dog'],
 ['one\n'
  'twota\n'
  'thrThis is a long string that has many characters iThe quick bis striThis is aaracter dogMen '
  'itee\n'
  'four\n'
  'five'],
 ['The quick brown fox jumps over theThe quick brown fox jxumps overq the lazy dog lazy Thisthree\n'
  'four\n'
  'fiveracter dog'],
 ['one\n'
  'twot\n'
  'thrThis is a long string that has many characters in itee\n'
  'four\n'
  'fiveabcdefghijklmnopqrstuvwxyz'],
 ['Testing te stingone\n'
  'twot\n'
  'thrThis is a long strinThe quick brown fox jumps over theThe quick brown fox jumps overq the '
  'lazy dog lazy Thisthree\n'
  'four\n'
  'fiveracter dogg that has many characters in itee\n'
  'four\n'
  'five 123'],
 ['  '],
 ['\t'],
 ['\n'],
 ['\r'],
 ['àèìòùáéíóúýâêîôûãñõäëïöüÿç'],
 ['This is a sample string to test the function'],
 ['The Quick Brown Fox Jumps Over The Lazy Dog'],
 ['Th!s 1s 4 str1ng w1th 5ymb0ls !n 1t'],
 ['          '],
 ['   \n\n   '],
 ['Quick'],
 ['   '],
 ['           '],
 ['           àèìòùáéíóúýâêîôûãñõäëïöüÿç'],
 ['      '],
 ['w1th'],
 ['Th!'],
 ['   \n\n 1s  '],
 ['Jumps'],
 ['Fox'],
 ['1t'],
 ['    This is a sample string to test the function          '],
 ['Th!s 1s 4 str1ng wtest5ymb0ls !n 1t'],
 ['    This is a sampleto string to test the function          '],
 ['Qukick'],
 ['    \t '],
 ['            '],
 ['   \n\n  string'],
 ['Tish!'],
 ['Th!s 1s 4 str1ng wtest5ymb0ls !n 1t\n'],
 ['ps'],
 ['a'],
 ['Dog'],
 ['Tish!           '],
 ['4'],
 ['is'],
 ['Jummtops'],
 ['!n'],
 ['Tish!           4'],
 ['yLazy'],
 [' ã          àèìòùáéíóúýâêîôûãñõäëïöüÿç'],
 ['LqNCZA'],
 ['Over'],
 ['hyNcJH'],
 ['QFoxukick'],
 ['Fo    This is a sampleto string to test the function  n        x'],
 ['!nn'],
 ['\t\t'],
 ['whyNcJH1th'],
 ['TheTe'],
 ['    This is a sampl           eto string to test the func tion          '],
 ['     ã          àèìòùáéíóúýâêîôûãñõäëïöüÿç  '],
 ['QFoQxukick'],
 ['tn'],
 ['Th!s 1s 4 str1ng wtest5ymb0ls !nsampleto 1t\n'],
 ['iw1th'],
 ['x      '],
 ['Dàèìòù4áéíóúýâêîôûãñõäëïöüÿçgog'],
 ['    This is a sample    \n\n 1s  string to test the functoion          '],
 ['isJumps'],
 ['function'],
 ['func'],
 ['Dëàèìòù4áéíóúýâêîôûãñõäëïÿçgog'],
 ['sampl'],
 ['funcc'],
 ['Lazy'],
 ['Th!s 1s 4 str1ng wtest5ymb40ls !n 1t\n'],
 ['n'],
 ['Doo'],
 ['aOver'],
 ['Th!s 1s 4 str1ng wtest5ymb0lse !n 1t\n'],
 ['Dëàèìòùõäëïÿçgog'],
 ['str1ng'],
 ['    This is a sampl            eto string to test the func Theon          '],
 ['Tish!           4!n'],
 ['Th!s40ls !n 1t\n'],
 ['cQukick'],
 ['   \n\n     '],
 ['QuaOverick'],
 ['Te'],
 ['QFoxuk'],
 ['Jum5ymb0lsmtops'],
 ['Th!s40ls'],
 ['   \n\n  1s  '],
 ['funnc'],
 ['eto'],
 ['    This is a sample string to test the function  i        '],
 ['sample'],
 ['        functoion   '],
 ['     ã         ô àèìòùáéíóúýâêîôûãñõäëïöüÿç  '],
 ['Tetn'],
 ['mThfGqorZJum5ymb0lsmtops'],
 ['   \n\nwtest5ymb40ls    '],
 ['    This is a sample strinisg to test the function          '],
 ['   \nhyNcJH\n  string'],
 ['str1ngsampl'],
 ['       '],
 ['   \n\nwwtest5ymb40ls    '],
 ['iwTish!1th'],
 ['test'],
 ['TTetn'],
 ['    '],
 ['   \n\nwwtes            ls    '],
 ['LaàèìòùáéíóúýâêîôûãñõäëïöüÿçQFoQxukyicky'],
 ['ver'],
 ['    4\n\n  1s  '],
 ['    This is a sample TTetnstrinisg to test the function           '],
 ['This is a sample string    This is a sampl            eto string to test the func '
  'Theon           to test the function'],
 ['tn ã          àèìòùáéíóúýâêîôûãñõäëïöüÿç'],
 ['Tish!          4'],
 ['strin'],
 ['àèìòùáéíóúýâêîèôûãñõäëïöüÿç'],
 ['   \nhy    This is a sample strinisg to test the fuunction          NcJH\n  string'],
 ['funthec'],
 ['  Tish!           4!n \n\n  1s  '],
 ['funtThis is a sample string    This is a sampl            eto string to test the func '
  'Theon           to test the functionhec'],
 ['        '],
 ['Th!s1s 1s 4 str1ng w1th 5ymb0ls !n 1t'],
 ['   \n\nBrown'],
 ['   \n\n wwtest5ymb40ls    '],
 ['iis'],
 ['                ã           àèìòùáöüÿç   '],
 ['astr1ngsampl'],
 ['QQFoxuk'],
 ['functoion'],
 ['   \nTetn\nBrown'],
 ['Th!s40ls !n 1t   \n\n wwtest5ymb40ls    \n'],
 ['nFo'],
 ['The QuiisJumpsck Brown Fox Jg'],
 ['Th!s 1s 4 stTheTer1ng wtest5ymb0lse !n 1t\n'],
 ['Jum5ymb0lsmfunction'],
 ['iiis'],
 ['        funthec    '],
 ['hyNcJ'],
 ['TTh!s40lsh!s 1s 4 str1ng wtest5ymb0lse !n 1t\n'],
 ['    This is a sample string to tea  '],
 ['fufncc'],
 ['p1ss'],
 ['wiw1th'],
 ['44'],
 ['eeTe'],
 ['           àèìòùáéíóúýâêîôiwTish!1thûãñõäëïöüÿç'],
 ['Lazyy'],
 ['This is a sample string    This is a sampl            eto string to test the func Theon       '
  'to test the function'],
 ['RLkion'],
 ['stricQukickn'],
 ['funtht'],
 ['TheyLazyTe'],
 ['   \nhy    This is a sample strinisg to test the fuunction          NcJH\n  string4'],
 ['i        s'],
 ['etoo'],
 ['Th!s 1s 4 str1ng wtest5ymb40ls s!n 1t\n'],
 ['FoFxuk'],
 ['The Quick Brown Fox Jumpe Lazy Dog'],
 ['4!n'],
 ['QuiisJumpsck'],
 ['This is a sample string    This is a sampl            eto string to LqNCZAtest the func '
  'Theon           to test the function'],
 ['         '],
 ['!'],
 ['TT'],
 ['mThftGqorZJum5ymb0lsmtops'],
 ['wwtes'],
 ['Tis          '],
 ['wtest5ymb40ls'],
 ['    This is a sample strintg to test the function          '],
 [' àèìòùáéíóúýâêîôiwTish!1thûãñõäëïöüÿç  \n\nwtest5ymb40ls    '],
 ['QFoxukcick'],
 ['Tis'],
 ['fux      ncc'],
 ['fux'],
 ['YJvcL'],
 ['Qck'],
 ['TTh!s40lsh!s 1s 4 str1nb0lse !n 1t\n'],
 [' Th!s  \n\n 1s  '],
 ['    This is a sampl          tothe func tion          '],
 ['nn'],
 ['sTh!s4strinisg05ymb0lsls'],
 ['  Th!s 1s 4 str1ng wtest5ymb0ls !nsampleto 1t\n'],
 ['whyNcJH1thfunnc'],
 ['why1NcJH1th'],
 ['iisTe'],
 ['Th!s40ls !n 1This is a sample string    This is a sampl            eto string to LqNCZAtest the '
  'func Theon           to test the functi           àèìòùáéíóúýâêîôûãñõäëïöüÿçnt\n'],
 ['stcricQukDogickn'],
 ['why1N    This is a sampleto string to test the function          cJH1th'],
 ['ssps'],
 ['Th    This is a sample TTetnstrinisg to test the function           !s40ls !n 1t\n'],
 ['    This irs a sample string to tea  '],
 ['fuwhy1N    This is a sampleto string to test the function          cJH1th'],
 ['   \n\nwwtes            ls   Th!s 1s 4 str1ng wtest5ymb0ls !n 1t\n '],
 ['hy'],
 ['strinisg'],
 ['           fux'],
 ['iiàèìòùáéíóúýâêîèôûãñõäëïöüÿç'],
 ['   \nhy    This is a sample strinisg to test the fuunction          NcJH\n  strin'],
 ['why1N'],
 ['Laàèìòùáéíóúùýâê   \n\n  1s  îôûãñõäëïöüÿçQFoQxukyicky'],
 ['   \nhy    This is a sample strinisg to test othe fuunction          NcJH\n  string4'],
 ['!s40ls'],
 ['This is a sample string    This is a sampl            eto string to test thLaàèìòùáéíóúùýâê   \n'
  '\n'
  '  1s  îôûãñõäëïöüÿçQFoQxukyickythe function'],
 ['Theon'],
 ['t1t'],
 [' cJH1th1s 4         funthec    ls !nsampleto 1t\n'],
 ['Th!s 1s 4 stsr1ng wtest5ymb0ls !n 1t\n'],
 ['Laàèìòùáéíóúùýâê'],
 ['       This is a sample string to test the function          1s  '],
 ['whyLaàèìòùáéíóúùýâê   \n\n  1s  îôûãñõäëïöüÿçQFoQxukyickytothe  \t H1th'],
 ['wwwtes'],
 ['îôûãñõäëïöüÿçQFoQxukyickythe'],
 ['   \n\nBro   \n\n 1s  n'],
 ['    This is a sample TTetnstrinisg tiiiso test the function           '],
 ['\n\n'],
 ['Tishstrintg4'],
 ['why1N    This is a sampleto string to test e function          cJH1th'],
 ['sThe Quick Brown Fox Jumps Over The Lazy DogtcricQukDogickn'],
 ['    This is a sample sttotherintg to test the function          '],
 ['to'],
 ['tt1t'],
 ['RL   \n\n  1s  kion'],
 ['LqNCZAtest'],
 ['ps1ss'],
 ['nF'],
 ['wwhyNcJH1thfunnchy1N'],
 ['àèìòùáöüÿç'],
 ['sJummtops'],
 ['   \n\nwwtens            ls   Th!s 1s 4 str1ng wtest5ymb0ls !n 1t\n '],
 ['   ã \t '],
 ['fuunction'],
 ['\n\nfunc'],
 ['wtest5ymb0lse'],
 ['QQFoTTxuk'],
 ['sQuiisJsumpsck'],
 ['Brown'],
 ['FMc'],
 ['p1sBrown'],
 ['TlTh!s40lsh!s'],
 ['This is a sample string    This is a sampl            eto string to test thLaàèìòùáéíóúùýâê   \n'
  '\n'
  '  Bro1s  îôûãñõäëïöüÿçQFoQxukyickythe function'],
 ['i        s   '],
 ['    This is a sample sttotherintg to test the funcstricQukickntion          '],
 ['  LqNCZAtest'],
 ['hyisJumpsJ'],
 ['   \nhyN cJH\n  string'],
 ['OvhyNcJer'],
 ['othe'],
 ['LaàèìòùáéQFoxukcky'],
 ['LaàèìòùáéíiisTeóúùýâê'],
 ['fuuni        sction'],
 ['fuon'],
 ['stgrsr1ng'],
 ['Ove    This is a sample    \n\n 1s  string to test the functoion          r'],
 [' Tsh!s   \n\n 1s  '],
 ['Jum5ymbops'],
 ['The'],
 ['whyLaàèìòùáéíóúùýâê   \n\n  1s  îôãñõäëïöüÿçQFoQxukyickytothe  \t H1th'],
 ['tiiiiso'],
 ['pFomThfGqorZJum5ymb0lsmtopss'],
 ['LqqNCZA'],
 ['ncc'],
 ['Tishstrintgi        s4'],
 ['!ncnncc'],
 ['string'],
 ['   \n   \n\nBrownrown'],
 ['4n'],
 ['B        functoion   rown'],
 ['vemThfGqorZJum5ymb0lsmtopsr'],
 ['Th!s40ls !n 1This is a sample string    This is a samplt1t            eto string to LqNCZAtest '
  'the func Theon           to test the functi           àèìòùáéíóúýâêîôûãñõäëïöüÿçnt\n'],
 ['àèìòùáéíóúýâêîôiwTish!1thûãñõäëïöüÿç'],
 ['Th    This is a sample TTetnstrinisg Jumpeto test the function           !s40ls !n 1t\n'],
 ['Ove'],
 ['FoF1Thisxuk'],
 ['   \n\nwwtes            ls    Th!s 1s 4 str1ng wtest5ymb0ls !n 1t\n '],
 ['B'],
 ['\n\nfnunc'],
 ['sns'],
 ['wiw1thstricQukickn'],
 ['  ring to tea  '],
 ['DogtcricQukDogickn'],
 ['Dàèìòù4áéíóúýp1ssâêîôcJH1thûãñõäëïöüÿçgog'],
 [' Th!s   \n\n 1s  '],
 ['  Th!s 1s 4 str1ng wtest5nymb0ls !nsampleto 1t\n'],
 ['Do'],
 ['   \n\n  striing'],
 ['Th!s 1s 4 stsr1ng wtest5ymb0TTh!s40lsh!sls !n 1t\n'],
 ['striing'],
 ['wteb40ls'],
 ['fJumpeuon'],
 ['hyNycJ'],
 ['mThfGeeTeqorZJum5ymb0lsmtops'],
 ['cJH1th'],
 ['TTh!s40lsh!s'],
 ['nfuntThis is a sample string    This is a sampl            eto string to test the func '
  'Theon           to test the functionheccc'],
 ['fnunnc'],
 ['                ã           '],
 ['whyLaàèìòùáéíóúùýâê'],
 ['ô'],
 ['LaazLyy'],
 ['psx       '],
 ['stgrsr1ngLqNCZAtest'],
 ['This is a sample string    This is a sampl            eto string to test '
  'thLaàèìòùáhéíóúùýâê   \n'
  '\n'
  '  Bro1s  îôûãñõäëïöüÿçQFoQxwtest5ymb0lseukyickythe function'],
 ['This is a sample string    This is a sampl            eto string to '
  'LqNCZAtmThfGeeTeqorZJum5ymb0lsmtopsest the func Theon           to test the function'],
 ['Foxx'],
 ['îôûãñõäëïöüÿçQFoQxukyicky'],
 ['The Quick Br owsttotherintgn Fox Jumpe Lazy og'],
 ['og'],
 ['str1ngsampaOverl'],
 ['Fo stgrsr1ng   This is aTh!s 1s 4 str1ng wtest5ymb0lse !n 1t\n'
  ' sampleto string to test the function  n        x'],
 [' ã          àèìòùáéíóúýâêîôûãñõäëïöàèìòùáéíóúýâêîôûãñõäëïöüÿçüÿç'],
 ['This'],
 ['    This is a sampl           eto string to test thes func tion          '],
 ['funthstr1ng'],
 ['tet'],
 ['whyNcJH1c'],
 ['    This is a sample strinisg to test the functiostgrsr1ngLqNCZAtestn          '],
 ['    This is a sample    \n\n 1s  string to te   '],
 ['x  cJH1th1s 4         funthec    ls !nsampleto 1t\n     '],
 ['hTheTe'],
 ['funaTh!s'],
 ['   \nhy    This is a sample strinisg to test the fuunction          NcJH\n  string4cJH1Jth'],
 ['BB'],
 ['why1N  p  This is a sampleto string to test the function          cJH1th'],
 ['mThftGqorZJum5ymb0lsmtstricQukicknops'],
 [' àèìòùáéíóúýâêîôiwTish!!1thûãñõäëïöüÿç  \n\nwtest5ymb40ls    '],
 ['   \n\nRL 1s  '],
 ['Th!s 1s RL4 str1ng wtest5ymb0l !n 1t\n'],
 ['str1nb0lse'],
 ['   \nhy    This  is a sample strinisg to test the fuunction          NcJH\n  string4cJH1Jth'],
 ['nfuntThis'],
 ['samplt1t'],
 ['wiw1s1th'],
 ['  Th!s 1s 4 st1r1ng wtest5nymb0ls !nsampleto 1t\n'],
 ['nfuntThis        '],
 ['Tish!  TTh!s40lsh!s 1s 4 str1ng wtest5ymb0lse !n 1t\n         '],
 ['Tish!          This is a sample string    This is a sampl   unction4'],
 ['p'],
 ['Th!s 1s str1ng wtest5ymb0ls !n 1t\n'],
 ['FMcc'],
 ['BBo'],
 ['f\n\nfnunc'],
 ['îôûãñõäëïöüÿçQFoyQxukyickythe'],
 ['functionheccc'],
 ['Th!s40ls !n 1This is a sample string    This is a samplt1t            etto string to LqNCZAtest '
  'the func Theon           to test the functi           àèìòùáéíóúýâêîôûãñõäëïöüÿçnt\n'],
 ['Bro'],
 ['JTh!s 1s 4 str1ng wtest5ymb0ls !nsampleto 1t\num5ymb0lsmfunction'],
 ['sThe Quick Brown Fox Jumps Over The Lazy DogttcricQukDogickn'],
 ['sTh!s4strinisg05ymb0lslTs'],
 ['puobAuk'],
 ['Juom5ymbops'],
 ['LaàèìòùáéQFoxxukcky'],
 ['whyNcJH1funnc'],
 ['Th'],
 ['Jg'],
 ['thLaàèìòùáéíóúùýâê'],
 ['fuwhy1N'],
 ['fuuni'],
 ['Bro1s'],
 ['\r\r'],
 ['why1N  p  This is a samplefunction          cJH1th'],
 ['QQFoTfuuniTxuk'],
 ['     o test the function1s  '],
 ['QFoxucick'],
 ['àèìòùáéíóúýâêîôiwTish!1thûãñõäëïñöüÿç'],
 ['fnuncc'],
 ['Th!s 1s 4 sTtTheTer1ng wtest5ymb0lse !n 1t\nJum5ymb0lsmfunction'],
 ['Ths !nîôûãñõäëïöüÿçQFoyQxukyickythe 1t\n'],
 ['p1s4Bnrown'],
 ['   \n\n  '],
 ['k'],
 ['etfuntThisoo'],
 ['àèìòùáéíóúýâêîôûãñõäëïöàèìòùáéíóúýâêîôûãñõäëïöüÿçüÿç'],
 ['LaàèìòùáéíúýâêîôûãñõäëïöüÿçQFoQxukyickThs !nîôûãñõäëïöüÿçQFoyQxukyickythe 1t\ny'],
 ['hyàèìòùáéíóúýâêîôûãñõäëïöàèìòùáéíóúýâêîôûãñõäëïöüÿçüÿç'],
 ['Tish!whyNcJH1th          4'],
 ['Th    This iTh!s 1s RL4 str1ng wtest5ymb0l !n 1t\n'
  's a sample TTetnstrinisg Jumpet   \n'
  '\n'
  'wtest5ymb40ls    t\n'],
 ['Tish!whyNcJH1whyLaàèìòùáéíóúùýâê   \n\n  1s  îôãñõäëïöüÿçQFoQxukyickytothe  \t H1th  4'],
 ['wDohycJHt'],
 ['TtTetn'],
 ['isJuis'],
 ['Th!s1s'],
 ['   s is a sample    \n\n 1s  string to te   '],
 ['wiiw1th'],
 ['OvOe'],
 ['sJTh!s 1s 4 str1ng wtest5ymb0ls !nsampleto 1t\n'
  'um5ymb0lsmfunctionJummtop    This is a sample sttotherintg to test the function      '
  'QuaOverick     s'],
 ['Laàaèìòù!nnáéíóúùýâê'],
 ['  Tish!     sThe Quick Brown Fox Jumps Over The Lazy DogttcricQukDogickn      4!n \n\n  1s  '],
 ['!nirs'],
 ['sJTh!s 1s 4 str1ng wtest5ymb0ls !nsampleto 1t\n'
  'um5ymb0lsmfunctionJummtop    This is a sample sttotherintg to test           '
  'àèìòùáéíóúýâêîôûãñõäëïöüÿçQuaOverick     s'],
 ['           àèìòùáéíóúýâêîôiwTstgrsr1ngïöüÿç'],
 ['Tsh!s'],
 ['àèìòùáéíóúýâêîôûãñõäëïöàèìòùáiséíóúýâêîôûãñõäëïöüÿçüÿç'],
 ['i       s   '],
 ['  Tish!     sThe Quick Brown Fox Jumps Over The Lazy DogttcricQukickn      4!n \n\n  1s  '],
 ['RL4'],
 ['st1r1ng'],
 ['sTtTheTer1stgrsr1ngLqNCZAtestng'],
 ['zPyWTI'],
 ['aTh!s'],
 ['Fow1thF1Thisxuk'],
 ['saTh!s40lsmplt1t'],
 ['     nFo   '],
 ['t1'],
 ['    This is a sample sttotherintg tàèìòùáöüÿço test the funcstricQukickntion          '],
 ['   \n\nwwtes        t    ls    Th!s 1s 4 str1ng wtest5ymb0ls !n 1t\n '],
 ['string4cJH1Jth'],
 ['     This is a sampl          tothe func tion          '],
 ['BBro'],
 ['nnnp1ss'],
 ['BBBo'],
 ['The QuiisJumpsck Brown Fox JgLaàaèìòù!nnáéíóúùýâê'],
 ['wtest5ymb0lscQukiwhyLaàèìòùáéíóúùýâê   \n\n  1s  îôûãñõäëïöüÿçQFoQxukyickytothe  \t H1thkn'],
 ['TBrownrown'],
 ['vemThfGqorZJum5ymb0lsmtstgrsr1ngLqNCZAtestpsr'],
 ['   \nhy    This is a sample strinisg to ttest the fuunction          NcJH\n  string'],
 ['wtest5nymb0ls'],
 ['whyNcJH1thFox'],
 ['1This'],
 ['x  cJH1th1s 4         funtthec    ls !nsampleto 1t\n     '],
 ['eo'],
 ['  Th!s 1s 4 st1   \n\nwwtest5ymb40ls    r1ng wtest5nymb0ls !nsampleto 1t\n'],
 ['     ã          àèìòùáéíóúìýâêîôstgrsr1ngûãñõäëïöüÿç  '],
 ['wtest5ymb0TîôãñõäëïöüÿçQFoQxukyickytothesh!sls'],
 ['This is a sample string    This is a sampl            eto string to test '
  'thLaàèìòùáhéíóúùýâê   \n'
  '\n'
  '  Bro1s  îôûãñõäëïöüÿçQFoQxwtest5ymb0lseukyickythe ction'],
 ['striing     This is a sampl          tothe func tion          '],
 ['QQFoTkTxu'],
 ['thes'],
 ['Th!s40ls !n 1This is a sample string    This Dàèìòù4áéíóúýâêîôûãñõäëïöüÿçgogis a '
  'samplt1t            etto string to LqNCZAtest the func Theon           to test the '
  'functi           àèìòùáéíóúýâêîQckôûãñõäëïöüÿçnt\n'],
 [' ã          àèòìòùáéíóúýâêîôûãñõäëïöàèìòùáéíóúýâêîôûãñõäëïöüÿçüÿç'],
 ['rBrown'],
 ['hy         functoio'],
 ['nnshthes'],
 ['wtest5ymb0l'],
 [' àèìòùáéíóúýâêîôiwTish!!1th1ûãñõäëïöüÿç  \n\nwtest5ymb40ls    '],
 ['This is a sample string Theonto test the function'],
 ['     ã          àèìòùáDogttcricQukDogicknéíóúìýâêîôstwhy1Ngrsr1ngûãñõäëïöüÿç  '],
 ['sQuiisJsmpsck'],
 ['àèìòùáéíóúýâêîôiwTish!!1thûãñõäëïöüÿçtnwtest5ymb0lscQukiwhyLLaàèìòùáéíóúùýâê   \n'
  '\n'
  '  1s  îôûãñõäëïöüÿçQFoQxukyickytothe  \t H1thkn\n'
  'Brown'],
 ['   Jum5ymbops ã iëïöüÿç  '],
 ['o'],
 ['why1N  p  This is a sampleto string to test the function          cJH1t1sh'],
 ['ywwtensLazy    This is a samQuaOverickple TTetnstrinisg to test the function           '],
 ['OZn'],
 ['cJH1t1s'],
 ['stgrsr1ngLqNtCZAtest'],
 ['    This  is a sample TTetnstrinisg to test the function           '],
 ['yyy'],
 ['Th!s 1s 4 str1n0g wtest5ymb0lse !n 1t\n'],
 ['kRLkion'],
 ['Juom5This is a sample string    This is a sampl            eto string to test the func '
  'Theon       to test the functionymbops'],
 ['   \n\nRL 1Ls  '],
 ['Th!s 1s 4 sTtTheTer1ng wtest5ymb0lse !n 1t\nJum5ymb0lsmfunct ion'],
 ['        funthec  tothet '],
 ['  Tish!     sThe Quick Brown Fox Jumps Over The Lazy DogttTcricQukickn      4!n \n\n  1s  '],
 ['    This is a sample strinitsg to test  the functiostgrsr1ngLqNCZAtestn          '],
 ['hyNJcJ'],
 ['    This is a sample TTetnstrinisg tiiiso test the function       n    '],
 ['iwTish!1Fo'],
 ['Tish!          This is a sample string    This is a sampl   unction!n4'],
 ['whyNcJH11thîôûãñõäëïöüÿçQFoQxwtest5ymb0lseukyickythefunnc'],
 ['strinifunctitsg'],
 ['44n'],
 [' cJH1th1s 4         funthec    lwiiw1ths !nsampleto 1t\n'],
 ['    This is a           '],
 ['    \n\nwwtes            ls   Th!s 1s 4 str1ng wtest5ymb0ls !n 1t\n '],
 ['st1r1n'],
 ['fuwiw1thstricQukicknnc'],
 ['cJH1t1sh'],
 ['mThfGeeTebqorZJum5ymb0lsmtops'],
 ['wtestm5nTheymb0ls'],
 ['iTh!s'],
 ['This is a sample string    Thits is a sampl            eto string to test the func Theon       '
  'to test the function'],
 ['tion'],
 ['funtThis is a sample string    This is a sampl            eto string to test the func '
  'Theon               àèìòùáéíóúýâêîôûãñõäëïöüÿç       to test the functionhec'],
 ['Th!stàèìòùáöüÿço40ls !n 1t\n'],
 ['DëàèìòùhyNJcJõäëïÿçg'],
 [' zPyWTI        functoion   '],
 ['aOwtest5nymb0lsver'],
 ['QQFoTfuuniTxusample'],
 ['rstn1r1n'],
 [' àèìòh  '],
 ['     '],
 ['123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789'],
 ['MNhqmCdV'],
 ['      The    '],
 ['    1t  The    '],
 ['MNhqmCV'],
 ['MNhqThe Quick Brown Fox Jumps Over The BrownLazy DogmCV'],
 ['1s'],
 ['sampLazyle'],
 ['ttest'],
 ['Lazy  '],
 ['ThTis'],
 ['MN!nhqmCCdV'],
 ['MNhqThe'],
 ['  \r \n   '],
 ['MNhqThe CQuick Brown Fox Jumps Over The BrownLazy DogmCV'],
 ['  \r \n  '],
 ['BrownLazy'],
 ['samplse'],
 ['Lazy z '],
 ['  \r \n\r  '],
 ['TTBrownis'],
 ['àèìòõùáéíóúýâêîôûãñõäëïöüÿç'],
 ['MNhqThe CQuick Brown Fox Jumpes Over The BrownLazy DogmCV'],
 ['ThTi'],
 ['MNhqThe CQuick Brown Fox oJumps Over The BrownLazy DogmCV'],
 ['MNhqThe CQuick Brown Fox Jumpes Over The BrownLazy DogmCV\n'],
 ['MNhqThe CQuick Brown Fwox Jumpes Over The BrownLazey DogmCV'],
 ['BBrownLazyLazy  '],
 ['BrownsampBrownleLazy'],
 ['MNMNhqThe CQuick Brown Fox Jumpes Over The BrownLazy DogmCV\nhqmCV'],
 ['This is a sample strOvering to test the function'],
 ['MNhqThe CQuicJumpsk Brown Fox Jumps Over The BrownLazy DogmCV'],
 ['MNhqThe CQuicJumpsk Brown Fox Jumps OverThis is a sample string to test the function The '
  'BrownLazy DogmCV'],
 ['   \n\n   z'],
 ['  \r \n    '],
 ['CQuick'],
 ['This is a sample strintog to test the function'],
 ['TTBrownis   '],
 ['    1t 1 The    '],
 ['testt'],
 ['    \n\n   '],
 ['aa'],
 ['   This is a sample string to test the function\n\n   z'],
 ['BrownLazys'],
 ['ThT    1t 1 The    i'],
 ['BBrownLazyLazy'],
 ['GThT    1t 1 The    ic'],
 ['Th!s 1s 4 str1str1ngng w1th 5ymb0ls !n 1t'],
 ['RGTk'],
 ['MNhqTMNMNhqThehe'],
 ['CQuicJumpsk\r'],
 ['DogmVCVBBrownLazyLazy  '],
 ['MNhqThe Quick Brown FoxJumps Over The BrownLazy DogmCV'],
 ['àèìòõùáéíóúýâêîôûãñõäëïöüÿçç'],
 ['BBrownLaazyLazy  '],
 ['This is a sample strintog ton test the function'],
 ['BrowMNhqThe CQuick Brown Fwox Jumpes Over The BrownLazey DogmCVnsampBrownleLazy'],
 ['Lazy zThTi '],
 ['MNhqThe CQuick Brown Fox oJutesttmps Over The BrownLazy DogmCV'],
 ['w1This is a sample sstrintog ton test the functiont'],
 ['    \n\n function  '],
 ['   \r\n \n   '],
 ['MNhqThe CQuicJumpsk Brown Fox Jumps OverThis is a sample string to test thCV'],
 ['Th!s 1s 4 sstr1str1ngng w1th 5ymb0ls !n 1t'],
 ['OverThisBBrownLaazyLazy  '],
 ['  \r  \n   '],
 ['BrowMNhqThe CQuick Brown Fstrintogwox Jumpes Over The BrownLazey DogmCVnsampBrownleLazy'],
 ['CQuicJstrOveringumpsk'],
 ['thCV'],
 ['Jumpes'],
 ['      1t  The    '],
 [' MNhqm CdV '],
 ['MNhqThe CQuicJumpsk Brown Fox Jumps  OverThis is a sample string to test thCV'],
 ['ThhT    1t 1 The    i'],
 ['ThTTi'],
 ['Foxa'],
 ['Th!s 1s 4 str1ng w1th 5ymb0ls !n 1t Over The TTBrownisgmCV'],
 ['     str1ng 1t  The    This is a sampleOvering to test the function'],
 ['Th!s 1s 4 str1str1ngng w1th 5ymb0ls !n 1tBrownLazys'],
 ['BrownL  \r  \n   azys'],
 ['àèìòõ\nç'],
 ['BBrownLaazyLazy'],
 ['MNhqmCdCQuicJumpsk\r'],
 ['      The      '],
 ['BBrownLMNhqThe CQuick BrMNhqThe Quick Brown Fox Jumps Over The BrownLazy DogmCVown Fox Jumpes '
  'Over The BrownLazy DogmCVaazyLazy  '],
 ['BrLownL  \r  \n   azys'],
 ['OverThis'],
 ['     str1ng 1t  The    This is a samp leOvering to test the function'],
 ['   This is a sample string to test th e function\n\n   z'],
 ['This nction'],
 ['zThTi '],
 ['BBrownLMNhqThehTTi'],
 ['Th!s 1s 4 str1str1ngng w1th 5ymb0ls !n 1tBrow'],
 ['MNhqThe CQuick Brown hFox Jumps Over The BrownLazy DogmCV'],
 ['oJutesttmps'],
 ['functont'],
 ['MNMNhqThe CQuick Brown Fox Jumpes OvewnLazy DogmCV\nhqmCV'],
 ['Fstrintogwox'],
 ['MNhqThe CQuicJumpsk BrowMNhqmn Fox Jumps OverThis  to test t'],
 ['ic'],
 ['MNhqThe CQuick Brown Fox oJutesttmps Oqver The BrownLazy DogmCV'],
 ['This sample string to      The     test the function'],
 ['DogmCVown  GThT '],
 ['Th!s 1s 4 str1str1ngnsg w1th 5ymb0ls !n 1t'],
 ['Do      The    g'],
 ['\t\t\t'],
 ['    \n\n func!ntion  '],
 ['te      1t  The    stt'],
 ['ThT     testt1t 1 The    i'],
 ['bUmvrK'],
 ['Tihis sample string to      The     test the function'],
 ['Th!s 1s 4 str1ng w1thTTBrownis    5ymb0ls !n 1t'],
 ['ThT'],
 ['r1ng'],
 ['leOvering'],
 ['te      1t  sThe    s tt'],
 ['ttV'],
 ['   This is a sample stringunction\n\n   z'],
 ['The The Lazy Dog'],
 ['MNhqThe CQuick Brown hFox Jumps Over The BrownLazy DoMNhqmCdCQuicJumpsk\rgmCV'],
 ['TThTi'],
 ['MNhq1TMNMNhqThehe'],
 ['      T he    '],
 ['MNhqmC      The      '],
 ['aaa'],
 ['BrowMNhqThe CQuick Brown Fwox Jumpes Over The BrownLazey DogmCVnsampBrownleLazyhTiTh!s 1s 4 '
  'str1ng w1th 5ymb0ls !n 1ts'],
 ['TTBrownisgmCV'],
 ['MNhqThe CQuicJumpsk Brown Foxstr1str1ngng Jumps OverThis is a sample string to test thCV'],
 ['leOvMNhqThe CQuick Brown Fox oJumps Over The BrownLazy DogmCVering'],
 ['ThT OverThisBBrownLaazyLazy   t1t 1 The    i'],
 ['MNhqThe CQuDogmCVnsampBrownleLazyick Brown Fox oJutesttmps Oqver The BrownLazy DogmCV'],
 ['BzyLazy'],
 ['MNhqThe CQuicJumpsk Brown Fox Jumpsw1This is a sample sstrintog ton test the functiont OverThis '
  'is a sample string to test the function The BrownLazy DogmCV'],
 ['ThT     testt1t 1 The    iMNhq1TMNMNhqThehe'],
 ['ThT    1sampLazylet 1 The    i'],
 ['s'],
 ['ThT     i'],
 ['  CdV  '],
 ['\t\t\t\t'],
 ['àèìòùáéíBrMNhqTheóúýâêîôûãñõäëïöüÿç'],
 ['    \n\n !func!ntion  '],
 ['    1t 1   '],
 ['    1tBrownsampBrownleLazy 1   '],
 ['tVhCV'],
 ['BBrownLaayLazy  '],
 ['MNhqThe CQuick Brown Fox Jumpes OveJr The BrownLazy DogmCV'],
 ['BrownL'],
 ['BwBrownLazyLazy  '],
 ['BwownLazyLazy  '],
 ['TTBris   '],
 ['      1t   The    '],
 ['MNhqThe CQuick Brown Fox Jumps Over The BrownLaz   \n\n   zy DomgmCV'],
 ['Th!s 1sr 4 str1str1ngnsg w1th 5ymb0ls !n 1t'],
 ['ttVàèìòùáéíóúýâêîôûãñõäëïöüÿç'],
 ['MNhqThe CQuticJumpsk Brown Fox Jumps OverThis is a sample string to test thCV'],
 ['MNhqmCdCQuicJumpsk\rhqmCV'],
 ['DogmCVering'],
 ['OverThisBBrownLaazyLazy  \t\t\t'],
 ['MNhqThe CQuicJumpsk BBrownLazyLazyBrown Fox Jumps  OverThis is a sample string to test thCV'],
 ['   This is a sample strg to test t function\n\n   z'],
 ['MNe CQuick Brown Fox oJumps Over The BrownLazy DogmCV'],
 ['DogmCVerinDog'],
 ['JumbUmvrKpes'],
 ['BrowMNhqThe CQuick Brown Fwox Jumpes Over The BrownLazey DogmCLazy'],
 ['    1t 1 Thestring    '],
 ['rstr1ng'],
 ['to   This is a sample string to test the function\n\n   z'],
 ['MNhqThe CQuicJumpsk Brown Fox Jumps OverThis is a sample string to test th e functionCdV The '
  'BrownLazy DogmCV'],
 ['BwownisLazyLazy  '],
 ['ThT Th!s 1s 4 sstr1str1ngng w1th 5ymb0ls !n 1t   1t 1 The    i'],
 ['CQuicJumpskg\r'],
 ['s    \n\n !func!ntion  e'],
 ['aLLa zy z aa'],
 ['ThTMNei'],
 ['g'],
 ['MNhqThe CQuicJumpsk Browno Fox Jumps Over The BrownLazy DogmCV'],
 ['BrownsampBrownlMNhqThe CQuicJumpsk BBrownLazyLazyBrown Fox Jumps  OverThis is a sample string '
  'to test thCVeLazy'],
 ['thCVeLBrownLazazy'],
 ['JuTTBrownismbUmvrKpes'],
 ['CQuDogmCVnsampBrownleLazyick'],
 ['Th1tBrownsampBrownleLazy!s 1s 4 str1str1ngng w1th 5ymb0ls !n 1tBrownLazys'],
 ['samp'],
 ['rrstr1ng'],
 ['Th!s 1s 4 str1ng w1th 5ymb0ls !n 1t Over The TrownisgmCV'],
 ['Th!s 1s 4 str1ng w1th 5ymb0ls !n 1testt1tt Over The TBrowMNhqmnrownisgmCV'],
 ['Brow'],
 ['àèìòõùáéíóúýâêîôûãñõäëïöüÿ'],
 ['MNhqThe CQuick Brown hFox Jumps OveMNhqThe CQuicJumpsk Brown Fox Jumps  OverThis is a sample '
  'string to test thCVr The BrownLazy DoMNhqmCdCQuicJumpsk\r'
  'gmCV'],
 ['bUmv'],
 ['  \rLazy \n\r  '],
 ['stri     ntog'],
 ['Th!s 1s 4 str1ng w1thTTBrownis    55ymb0ls !n 1t'],
 ['teestt'],
 ['MNhqThBrowMNhqThe CQuick Brown Fwox Jumpes Over The BrownLazey DogmCLazyk BrowMNhqmn Fox Jumps '
  'OverThis  to test t'],
 ['tetest'],
 ['  t     '],
 ['OverThisBBrownLaazLazy  '],
 ['DogmCLazyk'],
 ['Thi'],
 ['MNhqThe CQuDogmCVnsampBrownleLazyick Brown Fox oJutesttmps OqveThT     testt1t 1 The    '
  'iMNhq1TMNMNhqTheher The BrownLazy DogmCV'],
 ['aaaaa'],
 [' Th!s 1s 4 str1ng w1th 5ymb0ls !n 1t Over The TTBrownisgmCV'],
 ['Th!s 1s 4 str1ng w1th 5ymb0ls !n 1testt1tt Over The TBrowMNhqmnrownisgmCVstrC1ng'],
 ['    1tBrownsampBrownleLazy 1   \t'],
 ['Tntoghis'],
 ['functontMNhqThe CQuDogmCVnsampBrownleLazyick Brown Fox oJutesttmps OqveThT     testt1t 1 The    '
  'iMNhq1TMNMNhqTheher The BrownLazy DogmCV'],
 ['1CQuicJstrOveringumpskt'],
 ['JumJp'],
 ['  \r'
  'Lazy \n'
  '\r'
  ' Th!s 1s 4 str1ng w1th 5ymb0ls !n 1testt1tt Over The TBrowMNhqmnrownisgmCVstrC1ng 1s'],
 ['BBroownLazyLazy'],
 ['s    \n\n !fu55ymb0lsnc!ntion  e'],
 ['tVtV'],
 ['MNhqmCdCV'],
 ['oMNhqThe CQuicJumpsk Brown Fox Jumps OverThis is a sample string to test thCV'],
 ['MNhqThe CuQuicJumpsk Brown Foxstr1str1ngng Jumps OverThis is a sample string to test thCV'],
 ['RDogmCLazyGGTk'],
 ['Th!s 1s 4 str1ng w1th 5ymb0ls !n 1testMNhqThe CQuick Brown Fox Jumpes Over The BrownLazy '
  'DogmCVt1tt Over The TBrowMNhqmnrownisgmCV'],
 ['MNhqThe CQu\t\t\tick Brown func!ntionFox oJutesttmps Over The BrownLazy DogmCV'],
 ['This is ao sample starintog ton test the function'],
 ['MNhqThe\t\t'],
 ['to   Thihs is a sa\nmple string to test the function\n\n   z'],
 ['FstrintoBrLownLgwox'],
 ['ttVàèìòùáéíóúýâêîôûãñõäëïìöüÿç'],
 ['BwownLazyLazy'],
 ['BrowwnL'],
 ['Th!s'],
 ['MNhqThe CQuick Brown hFox Jumps Over The BrownLazy DoMNhThis is a sample strintog to test the '
  'function\r'
  'gmCV'],
 ['MNMNhqThe CQuick Brown Fox Jumpes Over The BrownLazy DogmCV\nhCV'],
 ['MNhqThBrowMNhqThe CQuick Brown Fwox Jumpes Over The BrownLazey DogmCLazyk BrowMNhqmn Fox Jumps '
  'OverThis  to tehst t'],
 ['MNMNhqThe CQuick Brown Fox JumpBrownL  \r  \n   azyses Over The BrownLazy DogmCV\nhCV'],
 ['MNhqThe CQuick Brown Fox Jumpes OveJr The BrownLazy DogmBrownCV'],
 ['r1g'],
 ['UcBwownisLazyLazy  '],
 ['UcBwDomgmCVownisLazyLazy  '],
 ['MNhqThe C Quick Brown Fox Jumps Over The BrownLazy DogmCV'],
 ['BrownL  tt\r  \n   azys'],
 ['stCQuicJstrOveringumpskt'],
 ['LaOverThisBBrownLaazyLazy  \t\t\tzy  '],
 ['TTBr ownis   '],
 ['aLLa zy z a'],
 ['This is ao sample starintog ton test the n'],
 ['      1t  T'],
 ['     str1ng 1t  The    This is a samThT    1sampLazylet 1 The    ipleOvering to test the '
  'function'],
 ['TTBrownnnis   '],
 ['    1tBrownsampBrownleLazy B1   \t'],
 ['functBwownisLazyLazy  ion'],
 ['MNhqThe C Quick Brown Fox zy DogmCV'],
 ['ickk'],
 ['BrozwnLazys'],
 ['This i s a sample strintog to test the hfuncti on'],
 ['1tBrownLazys'],
 ['z'],
 ['Lazyy z '],
 ['BBrownLLazyLazy  '],
 ['stCQuicMNhqThe CQuick Brown Fox Jumpes Over The BrownLazy DogmCVstrOveringumpskt'],
 ['i'],
 ['CQuDogmCVnsampBrownfunctBwownisLazyLazy'],
 ['aLLaa zz aa'],
 ['UcBwDomgmCVownisLazyLazy'],
 ['DogmCLazy'],
 ['BrownLazMNhqThe CQuicJumpsk Brown Fox Jumps OverThis is a sample string to test th e '
  'functionCdV The BrownLazy DogmCVys'],
 ['1testt1tt'],
 ['sThe'],
 ['MNhqThe C Quic   k Brown FTh!s 1s 4 str1ng w1th 5ymb0ls !n 1testMNhqThe CQuick Brown Fox Jumpes '
  'Over The BrownLazy DogmCVt1tt Over The TBrowMNhqmnrownisgmCVox Jumps Over TheC BrownLazy '
  'DogmCV'],
 ['Jumpsw1This'],
 ['QGLWea'],
 ['1testt1t'],
 ['CCQuicJumpsk'],
 ['MNhqmThTis  '],
 ['This is a sample strintog to tesMNhqThe CQuicJumpsk Brown Fox Jumps OverThis is a sample string '
  'to test the function The BrownLazy DogmCVt the function'],
 ['   This is a sampleT stringunction\n\n   z'],
 ['aLLa zyz z a'],
 ['nction'],
 ['TBrowMNhqmnrownisgmCV'],
 ['DogmC    \n\n func!ntion  Lazyk'],
 ['BryownLazys'],
 ['ThTiTi'],
 ['TMNhqmCVhis is ao sample starintog ton test the n'],
 ['     str1ng 1t  The    This is a samThT    1sampLazylet 1 The  MNhqThe CuQuicJumpsk Brown '
  'Fo    \n'
  '\n'
  '   xstr1str1ngng Jumps OverThis is a sample string to test thCVt the function'],
 ['ntog'],
 ['hCV'],
 ['Th!s 1s 4Cr1ngng w1th 5ymb0ls !n 1t'],
 ['ThT OverThisBBrownLaazyLazy   t1DomgmCV  i'],
 ['  \r  \n   àèì t   1t  The    òõùáéíóúýâêîôûãñõäëïöüÿ'],
 ['samplsme'],
 ['on'],
 ['ThT     ttestt1t 1 TBrownLazyhe    i'],
 ['sasmplsme'],
 ['\n\n\n'],
 ['CQuticJumpsk'],
 ['OqvveThT'],
 ['functontMNhqThLe CQuDogmCVnsampBrownleLazyick Brown Fox oJutesttmps OqveThT     testt1t 1 '
  'The    iMNhq1TMNMNhqTheher The BrownLazy DàèìòùáéíBrMNhqTheóúýâêîôûãñõäëïöüÿçogmCV'],
 ['C'],
 ['sTe'],
 ['w1thTTBrownis'],
 ['    samThT '],
 ['CQuicJumpskg'],
 ['CQuicJumpskg\r\r'],
 ['!func!ontion'],
 ['MNhqThe CQuicJumpsk Brown Fox Jumps OverThis is a sample string to test thhe function The '
  'BrownLazy DogmCV'],
 ['Jumpsw1Tntoghiss'],
 ['BBrownLaayLazy'],
 ['saasmplsme'],
 ['MNhqThe Quick Brown Fox Jumps Over The BrownLazy DogmCrV'],
 ['1seampLazyleat'],
 ['ThhT'],
 ['    1t 1 The    aaaaa'],
 ['BrownLazMNhqThe CQuicJumpsk Brown Fox Jumps OverThis is a sastr1str1ngnsgmple string to test th '
  'e functionCdV The BrownLazy DogmCVys'],
 ['MNhqThe CQuick Brown hFox Jumps Over The BrownLazy DoMNhThis is a sample strintoTh!s 1s 4 '
  'str1ng w1th 5ymb0ls !n 1testMNhqThe CQuick Brown Fox Jumpes Over The BrownLazy DogmCVt1tt Over '
  'The TBrowMNhqmnrownisgmCVg to test the function\r'
  'gmCV'],
 ['GThT    1t 1 The CuQuicJumpsk   ic'],
 ['      The     '],
 ['BBrownLaayLazystringunction'],
 ['UcBwDnomgmCVownisLazyLazy'],
 ['BBrownLaayLazystrizngunction'],
 ['BrowMNhqThe CQuick Brown Fwox Jumpes Over The BrownLazey DogmCVnsampBrownleLaLazy z zyhTiTh!s '
  '1s 4 str1ng w1th 5ymb0ls !n 1ts'],
 ['zz'],
 ['w  CdV  1This is a sample sstrintogt ton test the functiont'],
 ['qygh'],
 ['BrowMNhqThe CQuick Brown Fstrintogwox Jumpes Over The BrownLazuey DogmCVnsampBrownleLazy'],
 ['TheC'],
 ['    1t 1  The    '],
 ['  te      1t  sThe    s tt\r \n\r Foxstr1str1ngng'],
 ['DogmCV'],
 ['OverTh'],
 ['   ThiBrowMNhqThe CQuick Brown Fwox Jumpes Over The BrownLazey DogmCLazys is a sample string to '
  'test th e function\n'
  '\n'
  '   z'],
 ['     str1ng 1t  The    This is a samThT    1sampLazylet i1 The  MNhqThe CuQuicJumpBsk Brown '
  'Fo    \n'
  '\n'
  '   xstr1str1ngng Jumps OverThis is a sample string to test thCVt the function'],
 ['Th!s 1s 4 str1str1 1t'],
 ['nctoion'],
 ['TTBrown'],
 ['BBroownLaaLLa zy z aazyLazy'],
 ['str1g'],
 ['MNhqThBrowMNhqThe CQuick Brown Fwox Jumpes Over The BrownLazey DogmCLazyk BrowMNhqmn Fox Jumps '
  'OverThis  to ytehst t'],
 ['BrowMNhqThe CQuick Brown Fstrintogwox Jumpes Over zy'],
 ['    1t  Theion    '],
 ['TTBrownis    '],
 ['MNhqm'],
 ['   ThiBrowMNhqThe CQuick FoxJumpsBrown Fwox Jumpes Over The BrownLazey DogmCLazys is a sample '
  'string to test th e function\n'
  '\n'
  '   z'],
 ['Th!s 1s 4 str1ng w1th 5ymb0ls !nw 1testt1tt Over The TBrowMNhqmnrownisgmCV'],
 ['JumbstringunctionUmvrKpes'],
 ['Lazy '],
 ['BwownLazyaLa zy  '],
 ['CCQuicJumt1DomgmCVpsk'],
 ['Jumpsw1TntoghiTTBrisss'],
 ['BrownL  tt\r  \n   aCQuDogmCVnsampBrownleLazyickzys'],
 ['UrK'],
 ['BBrownLaayLazystringunctionn'],
 ['VhCV'],
 ['CQuicJstrOveJringumpsk'],
 ['MNhqThe CQuick Brown hFox Jumps OcveMNhqThe CQuicJumpsk Brown Fox Jumps  OverThis is a sample '
  'string to test thCVr The BrownLazy DoMNhqmCdCQuicJumpsk\r'
  'gmCV'],
 ['BrowMNhqThe CQuick Brown Fwox Jumpes Over The BrownLazey DogmCVnsampBrownleLaLazy z zyhTiTh!s '
  '1s 4 str1ng w1th 5ymb0ls !n 1tsrrstr1ng'],
 ['OverThisBBrownLaazyLazy'],
 ['aCQuDogmCVnsampBrownleLazyickzys'],
 ['UcBwownisLazzyz '],
 ['iii'],
 ['s    \n\n !func!ntio    \n\n func!ntion  n  e'],
 ['Th!s 1s 4 str1sMNhqmtr1 1t'],
 ['testVhCVtt'],
 ['DogmCVBrownsampBrownlMNhqThensampBrownleLazy'],
 ['  te      1t  sThe    s tt\r \n1\r Foxstr1str1ngng'],
 ['MNhqThe Quick BrowTBrowMNhqmnrownisgmCVgn FoxJumpws Over The BrownLazy DogmCV'],
 ['Th!s 1s 4 str1str1ngng w1th 5ymb0lDogmVCVBBrownLazyLazy  s !n 1tBrow'],
 ['Ju   This is a sampleT stringunction\n\n   zTTBrownismbUmvrKpes'],
 ['ç'],
 ['TBrowMNhqmnrownisgmCVstrC1ng'],
 ['   This is a sample strinazysgunction\n\n   z'],
 ['aLLa'],
 ['Th!s 1s 4s str1str1ngng w1th 5ymb0ls !n 1tBrow'],
 ['BrownLazuey'],
 ['MNhqThe CQugicJumpsk Brown Foxstr1str1ngng Jumps OverThis is a sample string to test thCV'],
 ['\n'
  'zTTBrownismbUmvrKpesBrMNhqThe\n'
  'Th!s 1s 4 str1str1ngng w1th 5ymb0lDogmVCVBBrownLazyLazy  s !n 1tBrow\n'],
 ['LaOverThissBBrownLaazyLazy  \t\t\tzy  '],
 ['stCQuicJstrOveringumpsktoJutesttmps'],
 ['tstr1g'],
 ['Th!s 1s !4 str1str1ngnsg w1th 5ymb0ls !n 1t'],
 ['leOvMNhqThe CQuick Brown Fox oJumps Ovepr The BrownLazy DogmCVering'],
 ['CQuck'],
 ['aLaLBrowTBrowMNhqmnrownisgmCVgna'],
 ['thThT OaverThisBBrownLaazyLazye   t1t 1 The    iCVeLBrownLazazy'],
 ['BBrownLLazyLazy'],
 ['Th!s 1s w1This is a sample sstrintog ton test the functiont4 str1str1ngng w1th 5ymb0ls !n 1t'],
 [' Th!s 1s 4 str1ng w1thn 5ymb0ls !n 1t Over The TTBrownisgmCV'],
 ['testtt'],
 ['aLLaa zz aaick'],
 ['DogmCrV'],
 ['hThT     testt1t 1 The    iMNhq1TMNMNhqThehe'],
 ['         The     ']]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-q~aJJM}Cj-'
    b'0y<Nsb00OTqWU>xsw!U(voMAWK%6)$`Sd)A#>N14v^<RYcvYd(Pf#bAdo2lLW#4^I!hszx~U<{)_+TfBpS`{O!N~?|-'
    b'*c+u#58Z?TM0&x*O6FvlvT?rt}}kmkxEq?B`vmiN7DhZa^G$8J8Mjup}l@9+Qj@BjX<fBUym?mBV3YW;;X!nOHw88fVKZrP{Q8cN'
    b'K2tTjXHA;w+T4WlQ1x`+Dvn3%TB5*|PGYAa{uw^y|}&w4zQZ^e1r3B_(nyQKWa;7PN+b6)uCF*(JyuZ3yb8UwBKU54J%;Xz}ju=;'
    b'+t+RE|WUSAt|mNQdcz4uqwUyqsAW6Atc-6i-'
    b'}d&w)^9!{E>v9+D^w3c6qC(f2j?0fcF?3~iDuhupp$B^3XlUF%DPxYO;W=gH^{LTz!w&Q4FEatJMy7EppB^%kQ-'
    b'Jh8{yIQ_|^)f@uBdsys<{8E~j=g=x9_1K+kt<ez=Z=VhYQK45xB1s&8ehtp$%yH`mcwqRwP^3A;g5}>o_bd-XB1w{hldq+tD|TB&'
    b'x?OO=J9^@GSoJEPnhA<+*V4J=QRF-'
    b'!N<h>ky*1_Q{F9DtdG|(c<K3h%(2$&q+Z*ecDIdp_j_|^8*8_Icf{s1hlKG<yDhgI`z^imqR-NgiBGTRVadu<2#7IPWRh?dULjw+'
    b'^3JsyQyDG3waW{6oqqQ2j41xtCe(b^y*ctxoTEM_;P~tu1~qm|i=W=cA65&!hunARZQ|!S&eZc?j~TrC!Q1K`?jVf)jad2A<xz81'
    b'58G~ecH28{jEI@nP74o6v%KGz>bbRHYm`;XYp=9i7tY(mj(x8B(po*b=cN&QX`yZWthF@z^Z@$t;#DV(Tk_4peJ$5OKvj!`-'
    b'^0|*&gHv#u5sh&E%)^LS<HS;*5=PlmDHIgJT~0731mX$4y=MlM=W(gmW;j68?T-*?6lM)afow-'
    b'@@D%9O{OlzZM|UVu}h0F4(nsK=x-Nt=vIOiYXqDn9*SSy$v@A%&B|Yo5uqQ`Fnh-'
    b'9Z#wTKUJdAZ&mRz4yRi|=)52ZM!^9vZHC_;N?Gc*o``2TZm00UK>%7&lQEjP(enTOa!`?N#c`ES>j4%Lv=j5`+Ucv6{K+I1tBs<-'
    b'4DJI;T_$-YekDVv;Tg-aNrJXgO<vwG%&&IUz=P&AuwzU&}PENqk1$L~h3mRdAVayt)_h1}<V65V@HRqFwsyWk*foTb+{6Kn3k$^g'
    b'LpBYEY?SMMG6ES~cUTs$_;#hxT41@3lJTJcR4#qKDP8<vyXT-aB3uXbwn<wFg88~CuyT>|j9<!hJ@Y32>j2-'
    b'vlr~76wQ9R*w*1}}Pdq5Qo)5wzGZ7zKhB{=d8VPIU|_N-'
    b'2Fm^;mf+u!IZN&8YF_Y+}pu8ihE0kWr*htX=7;7!W&;2)sD?UwA#;t<0h#79Dii)h9z%Fl%FJ7FX9nj^7ec{!Ko06PP8k0&hRJ*R'
    b'pauAfMmd_Ir~F*bI)KX{XY5VB%~gfK;sbPA;3ac_*oLg16+QBp20$gpt^sL+6{)ZK`eFtm&U$JjU3Q6EW&zyWjTT`Tq5uq@CTJ=!'
    b'p7izAhR(bg;Fl><uvmb(_x*NkB$;(CT1^62p#d~9u8`Q`UuHfQpOkuQ=NZS!AvOm#?lqm`tk0u~eSbTL;+AQca~n3AbKcpJ8=5W|'
    b'v>;rj6m9B7Z-$@aPN!{D5jCIP1z$3HW#oI-'
    b'~Sgbe)z{^|{VW;h!Y1xJEFki9m4d4Wnh0VIj#htRfK8yt7=!Q!xsmD0<5WndWu491&={X*nzto6L#;T=hNVcWq<Kaif{+IL|1*2<'
    b'o%K@A^-qcT&K_o}=`W6u5W@-'
    b'E=Y0itX{=rGYQg%rWoHPR3Xh}b3kP6bL1G!f;HX3Vpl(nkU=@QbnwOli56sO0p73G&ZO;g@L=J`m%~G?umb@=0y-'
    b'N)Pm}xbq@lGPJn9T1t8hV-'
    b'{oqH0=I_W@q9sKw1+VdM%Zf?mgqcYKi*h_}U2O!_1Fusig$Y59lJHpP>y}UThCyh{tsT4KNF&kcxi<{J4!~b#`*w>_{PKW85JC?P'
    b'jEX@^MM=hu?HUagp)Mt{5MOEvG=X%#j{juG5HAJbMFq%#_)}-'
    b'SeA|knbb@K>A8h0TKwNh7f={`M%Qv1UHlNY$u|iA=`E$(~ykF?3chK*%STq{n#c>_bBK_W5(ho=@ZfoAqRc{UAQwCwSiV901QuSK'
    b'LQG01Vx$Mp-nKV<f~D>A}^lfk-SmEM%rj#aEle(Nj4kSdMg#!?Rw;<?Z3b)MzEp}z>bgHU+(wt)*B484$uJ7nA7OnuqY<a=`no+='
    b'Q6N4ZwyeJDdb|wbKv{Q41Lvx{)UQ@0n(lq-Gso+cas8$6I+l+-'
    b'VulKOl5df`vXb{r&&kRGEs1_+QzRN!S%>v49@=rjWCGx(tT2Tc=2plMdslbsm;tkh9Bn7Xb>UbE-'
    b'+BZ5s(Msf%%?uK)4DS%?5!8Z*h*mdp)Ked~Kf9$oJ!im|T)QR?P+6-xVK6(j-'
    b'Xi>NW0NjKMvqE4ikIJ7yU$+XF4YFDs<}XTqTYJHcH@2sfqyijm;5C!|X9Lv1~1K3Q+0PaB#PreaR}Ho(7a{X}?*j=Klt&_Uzi65;'
    b'SMr%fZk3arJRadI+pY?kurka##ldLzIovNomyGaAiMCAf^+8<<QD@<~7dl2F170Q(mJL|6}00gr;x)sS9{zdF309Po?-'
    b'ohkTWo2yJWs=Fu*-'
    b'W`*C!u0V3QXGjTId{*~x%~X`8#pCm6jvSOcl>q(=nnvm(5Z?a;lFh?!oSSMh(`lfF@Pa%kpTC{#AFW$OJn%1795q~XW$X}?AGj&G'
    b'vOJnV6SyMfjl8r;}r)AcXw?th}f2BsRM!@`No)sgxYy#g)c%Lk#7gcgNwlRJF~*$Dr2n)2n_Rv>w4=K{f=9a42(VmpF-'
    b'csO+!Qwm+pmQ;Z?y&8Up`-Kd79;OvP-B>L1D%nHt<Vtpb1}cajsiIGs-TVH6?(-'
    b'Vag097Hdium?<yKZXU44=qb)ntaU@F|n{I62~$c4tCa8!1As*fNE6d+^!d3^A%ht=_P1(?!SZ<a*)G=#^r`1gZ7TwOcBoSi>@`tu'
    b'`&M`0~e@y8UzPo1Duc?=C5Yh5H)1xj>sD_F%dCa0h0=7fu1jsm)r1T%u-'
    b'H%2|?fiSL1*&)U5^4Z;3<^y%wRLNWpZ_1Zo*ZEJP>ZQhXupU=}=vaX5UAO8{jUETPSiV?2HC*-'
    b'uPwX<rJ23Jss#v7`W<e9pUiEau4$1aH?l=>&WKa4ttRd=yu<K8eou3tK2BMu@{2d8wyd;Rg6BQr7;{_sIqeWRD}yiL-'
    b'+R038rT`rAJ<bwQxOw;~3DB^VhXK)_%VHUfd1eD?t{JVWM7vCh=;TLzWIFrci~HbjrD+S`Wc^82IUbf@#CEtXE)!bcZw%UGdwh4C'
    b'gvzaF16+`s-zczI{sb=D-mqzi-'
    b'F<_KIN5wTsk2B~G;MD(w;PfyU&j%yizyFtXC1Vi#EPSG1k6hMIR1~5jthhqdp%CHD?t}Q~9L3bRABnn-PKyKaV*Ke4>aqYSMZ3B;'
    b'D7|hm<3)%!u5{7jZrjfTTkL=ZuB5||~1^{EfyB_65VwONB0(t=(kuOMSxW~n5c+zG{KxyBCfzFTqQes#kH&prh-Gj-'
    b'_!d#>K&Jvggg<tWwhAGD;4syVl>^Re$QFdbva>Q%UEI|CPNGu=<nq=Zu0MBtyJ!DOsgINNpUSA8JY#E(50EiPk8#Q07MqU1h#FH2'
    b';T!Gg&v?eK)j{##hmxM2nKN-L0kJ@bTJIK-uVZm8j-lP6<zg-y0LUC{CkZ(ctb88{!v#&v%=i5q$@#71}<uMcmIsy4-'
    b'T1)$76bUWB_eS!aw?I%jzC%Ddz;Cc0@@DmLz~nbsCp5?wrS;Ka=1ILF`K8B*_U=TB;G#7O5it?Tc~K4*Z5_8Zr?1q3a7a1SM<Q3H'
    b';_Ji#jl>_K6G%Y`TEt5tiBVg;4pGl^j;tm7qJ2%#K7))GOH3?szi;`C2#W!bdqP?T^4EOX)h1zs-'
    b'0`JCZ1G6L08Sb3!qE`hHahOaH#|)&F;Iy18AM*J3I@%h)VB&}?n*v6XQAy*0FXzSaJxZbLZ7|SOYH$s4zq-a^x+h&XWt)1Je-'
    b'(6$tXmjDbiD-mlBy+lzc^_xdRF0i+GhBa-ce>247m|gL`{<!5kSzoyRlsT_L|_=erYS1)VQP8w^Bdb~Sq8-'
    b'pv<x=Xej)?AN#1OKJlWjb@oB7%YO}$kCOA^A0K|>`x|N6^Lp!PeeP3-%7sUA|?^rrbOo5Ydl{~*hX9-'
    b'S#EvkLNsn^zTCUp?tSIO&pcE+Gwy{xzf?e^U{qUxqM6dXlxU_ztB^6BR?zt)yq(K?h>t~j@}e!*8qhSDRa)i(mQ+;<(UNOJu8i5n'
    b'uG*p^(M!pyfg~V$M+x{6Mg?vv9x*_sICDCE`yM^t>$qCYNWk`>aBW$f5g5B~{e%07{6_Q`k!@6x^;6tWWMYwRR7_Mu1roM+<61uZ'
    b'MuPBM_i}zR__iZ1A8RBKs+Dk|an|pj#VHWpD<O8#?s|wy<5W9BqVo1nWla@@)XbD>3sAFQ_pQ|=0`7+TCWH^$uId{S`QjK8VzA%D'
    b'TG#i!dgSkB$k_<3GjOEsD-'
    b'7ZZ7ZvIi*au<%nCu;VbtN;MOozR&&%n7!5$k%{CeYWP+06Zfyys0jLu$l&N>j5xS0_~Ywb0v5$#=sRY>F%}OD7dPGF|Mjw-gMNgm'
    b'LZWfv_QWE4HXzX%k_wD5g}!ub(=xByzuRalahiOa-g-)BA<g;K-m9j_8|V`1GC_YPx5-'
    b'Utn@Sfe{%_c>T?yt#}cEsAz@uVM~zlcvXT`J^?T{i}5mZ`69f-3m35tu=-n}y1c@v9j~-qB<UaN0gl-QaM19j)yM-'
    b'FSuJU<^q!II2mvDA5F^8tnePm~Z6y25%pI+XMNCwcH8r(Ks*(c@Y>BicnFLBVM-FX{#B}2HnSWyCbG(WJXl|q?Cg6G5>hu2}Uc3z'
    b'1&M!+Bu`Q7h5@E3@hl}t=RM9KipAvbo>X^BxY%pNZ&CFebD%uKsf2VoMtG+slTluk8F9AD*Hk28FECtR(gkcUbOV6{p+=1}nm(~A'
    b'4I>6d_jzdUoU$SHVJkd-jlMntSFX~UnE5v_mlSrXR@KIj-qu@ZnPHZz%%jsW3`-'
    b'K2)jDBV+px9RiSvE2~2a?Fraz9nAfMztRz5*KQA=+jAr`%W)tx<?x3SG)L^8zWzyx!NLFu?_2>8TvANjJc66Q^F4?t%d^cKBI*FM'
    b'wrQ_Y+kgeyadNG#b^WTY$BO20<Eljpx0~%nWe95zf$c;I}3(|AX!E{|?%kXF`|wp*HN3BJo=r+08?E@ucR*%h2Cg1#(MbwY*v&-'
    b'!-z6pIB=Zf3N&Y34b!#!{?WYlds5&-%88dUt9yAF`Q2spRKsTf=6dxVyiWH)%A|GcGp@RLFIdLw#D1(->NaexDIt>F`@#M{D;Ev-'
    b'RGwdYxWcQ!_SFgZ{+a{u{m++ULuZDBym-TNY0BMBU+&q)%%HH>sz7utt~*&XhfBnB0a?~G@`X8NGjtl>41JtkRH)K{di3Z0W9QaP'
    b'Kf>kn8uH}5c|&X#rsnlIZwKLel!RR15&p>QhrJZfM|X^h|!RjAzPblo4POBSz8bWZyS?huHp^JPwh{MPIHNt4@IZBR7>(A3Mp!77'
    b'T{K(A~smtR?qnI@a|Z{H`@@ZoxFmtgdB;i7|ZU(X$w=ZNWxiLsQ0a^RT27$)^9-'
    b'Ov#K9zG?1Un4H@pI5MzG2u5VDj#Idt2CI~0MF(3tiRGQ6SSzM~3>3t|VOsJ9`%)%<(3gvp&j-AUUhFWsh_nkk3Jf-'
    b'_!cEi$}fA$F`DGEa*Ujg_e6}S*gf)!`=3dRjHTrLIh|C31jJrn}aSyUjwFdKf9u!6zvU7i&`S(_wkqjPW;f6F-eu2;CCD7-'
    b'^Jy`4<X+*nFy_-WAVUE$K~xV;^_ZsPk(lVmGxn(a}|ny9FciE6=4L-'
    b'tjz@HDdQTUk?9{3<!5@vSO(k%>hmPO5!P&1#Ygi$ArKsDgCOGSIiSN592yRAgUN#zWTG5g^FLP`Cskxx&xk6RhZQvp=OW%updEqc'
    b'n*YTq~a!XYf-Q+R=!5^oo+N2)0ypqN11*mBx|PxADUP{!t#7heHI$V({(=gR2PdM38v|IU2&e-'
    b'Xyzti>mgTwr$t9Hu+VZ7&S{Bs=i5|T1#Jk%FR2lF~@g8iuVpg&>gv~3wSO_8zL_w0*G*=I==)y;4v7g1@RFzkq{D%MzukpDdASpB'
    b'oV*Sz}B~R5=C{QtL_9<awgzSSSNF89h4xKN2kCKhH}Cyw-0a23o!tVuT!!Z_$_hI1y!@lPxZeMNe@*ss88XIC^SX;Q=-'
    b'v`ieE)9B`W_?t>0+W9Vj#qQp`kXzNSZRg(<Cj_#@!+jI;+*&Pc&<sm@!s5O0AbINGK6$%EY=TNTjon~!xW%A}WT$rpgZ?htO84=f'
    b'|@_+7qZxa-6#^5)G?-'
    b'wm!=3jol`SHG=(|0&nfzm;HA(nDh#l6CMKm}>MLhXxHR+xO((eO4ECxqm)C$ay(EChB>!LT>@yOXkb}=(7*5dVAssx)bbi!D&#Hc'
    b'b^c)^|q@x)5vIGxL5&``y1XH7Ej40mh&PeDylJ2tzL`z3ZztVeD7L&aMV9rZo7sQeNXW+p0}MQ<0>!kuNmj+C{D<2fy-IbZk~uHT'
    b'(r2Lx|>TwAw^kJRJkAu2EfFpk|-'
    b'<CAP6YH?+8gE0a8|k?mhgGEQJrieO4F=(LN(+g5|_*0#)q^H1~RlfI`(%N^}ZPvstTJ1pn62Mpq)<HW-'
    b'vjb#CIf0nHuY^L2AS?%R6<Kg?Ti6R^ZdAeEuIS4l%$mo5qh(PKn~Got<Q@?MGLyAtt-Reg7j_#1v%g?Hxy3QKYKYj9k9&S;GcWOZ'
    b'!6kux-'
    b'L#fz%_lH{z%w;B(tHY7D=gQA^8Kb<lIuI87j4m=z}X8aJ05QPEj=3699=Dot(8S9wj%FGu6)b5Cj?IU5gQVPX$GNG4d^;>1Is}n6'
    b'S&0yaU3IfwB-'
    b'^nfU;6DTY2mu@7b|@mUFH(0Z3MtwG6m6@EHV9NJZIZ=I(S(1iO`yocxJ~W+fFHB3em#`g@GCdYf%1UzKwkwSz{K|aW&;S$Jbi<r('
    b'6{;zvM(y(7A@FmXwtX3{s(gUggwF=-_3ljfV|6%eDUApOUMD(2TJbYf9#OW-XRZPxc>OZH4mDe3nE@DD@M~?3oMcznwovltwy3lV'
    b'WJyYL{|zrzWD;#@i3}=C&Kr7zoplC1T>?xoWt}<+E^DfgSbRrN%PZpwS98C;#-'
    b'dq^)Zo^sz{`VO?U%Af(onda_5!d>!BA+N}fogUzdxmHbHGT3-'
    b'1HDLxc{bk#%ip+$=<5B*mf}k*@{m5}7XtU~hmOa_HuV*{y+TmdHo2oIClalVDS~wQ$h1<$L=hV#2Z>`8EB?D`y4YWc8-'
    b'oO!ctT`2m>Ooe3wh8OA^SMsqomtnIo4{Y06e`rm^7UiX0+yiC=(R^4gsO=d1GZCZu=@WF8rv}mLnA$qml`+L?yRUGoEM&}~fQneV'
    b';R4$0Na%6YbYL=ZfB~GGFj4J7&*{%@fsgGq%O{t0q{ZvcxnkHhRW9Hv#hoU;X{D2mqYL7GVEAYZMYD++@LH+UZoBYakGJmecrRJD'
    b'tuKvg1wRiE+Mp1hL5u*_8vd&CgdI9F0ycOJh`1&E~q$Z}i9xP2bp{<sW%@=q`GqdnJ%+1V8ySVVJvmOmpN~GrU)`fnMQi~IPg7TV'
    b'Q7GK8M@avK%($O!Q?E%$Zados~`Q2Dj6~Btk&TH0-ztyf^v_T-sQ=)|z5f;a8-'
    b'ZzjL0BK%=kMhKa|0NH}8@>2tqEr{jWO{*DYOvDV!XBa7zS_+b(Mp@>vXXyFJtbOP5FItrbyHUKJ`|Z))P-'
    b'9W;hJ4mQNJxwiIa#Ii?XJO`-!B7sO3k-*Ib|CYS60a$E3&-'
    b'<06{Ly}?7Y`9i#Rp*x+BCCrDjLeOK3Ftke@s^c`GvO!HSe2e>ujy8U)aOPW=%`)|wXg<@0f9Nr!fO~Fms$R@Y#vCXQusy@TaYV1y'
    b'nj7p0WYk!eR>4%?V!4o7g2=}Lq}JMplV0B%AQO;NCLYW08=-_>u0MziX-'
    b'3Lz?LkWsF%gYMR2=dxJtcaKC>RJ~hguTK^M2+VS0rUcf^?O5>x_T)vLogr4}x*N5V6kk8=IahjZbzC`PR*ZqICC9d1dmqc7(oli<'
    b';^JAk7Nxw|Yvc3OxTAPu8lEuSR;v?z@wWM%BGta}Gwdbu1!nA|WI?>!CWN5woAk@Vi+MF@qd&o&BZL(b_Lhawab1Pc3LEg2kz0KA'
    b'rboehyZBTf~=&(Nw1ZHH9<Zy5LYWQzFtfJN8DjGA(_?0fhs;5JqV?ues@vM`jrCo{w1BXjmTwa>mPZ(r*>nx4OouS}1B(OjLIPYS'
    b'Nu37*wr(HTU_d3iUK62t<ogqQ*6%gWVzpBdQfRIq%@R9BKLmxWU$R1O-'
    b'rM%+TOg!N66#=8ONrzG_GN2mTFU!__|723gbyR8)H{+w+yAJJDvXsP*Qzu3Hp&v8qnAPSpN10(c`<UTaKn@D6+Z57_{SLl``uG=R'
    b'wov>zdQi@1$m7NDJ}Z{4jf5{artpc)VrErP3-fkYdUqMlNs^<sEEF=S|E+^a5ZkRud07k6R?<CF@n&m4n@eK2N6c%s4YKl#0xP(-'
    b'g)<zJdE2dX1#8ua^C%T`gDvS^7+Wa4kFUW<f~s>^}skcOtHNOYD}Bw0ngSTq{d9g?EE)kS@;HRpU)dv}_(Es+jal{kH>UB9SOO4Z'
    b'ay)1E*T;TkzFQZOQsC|X)oU4bFGeGkIJ&%Sa=W39#r+{3g=nk&6$@CgJ5$=EW4)bAYg!^m$N=`|B$M_Xf}Y7?kAAsKoGSJ9h<dhv'
    b'a?=BLZCUI0ANi!cHdtC#C1oVyV0JNQX&==yX+{7g8?bg$R_(~uEpKDZ8E_YK5@4E2;w)?#E4HkSiz$#`!VQn#6!cz0gZ&Q^3<9ZC'
    b'Yz>WxuYtr%}ac;Cd?+&TmkWDaj7Cpl2zMc#y9l4JbX!~b`Ez2<bqx9TWlUE?HIZHol7NC=6}&WjR^Dr;(%$iB6-Dq04T-'
    b'7u%Q4@Q$<L?9|EC>O0>tB%uXfI`)0AH@t;8N)laKVNNR)OoMWz@P&}B8d#m6A5%{J@5BtCB-f>@#H9O2q02-'
    b's<ZQ={cuf8ed`)4QJFG`>&Lw2>7mVMcacoIbb?5)Ou0pf<;s2*FC6gD4~5?Dr}D-aFaF-zsM_<@Y-'
    b'Fo?E@&oP<i+1=%%>_j7|kL0KtAD+#(O0Em>doC!#0V<W%wKa2Jf+lbjiLqekw6Kk!f1@lWk;6GK1)11rgc*)&{}1Y$IBs6?G0#m2'
    b'itLN77)is!Unbi4iNJn-'
    b'E&nJSxsUC{lppF*UFy*jo4VS<XTEE*N~G*EBcp8v!r><V_kPdi|~IT}5|usoF1T4k9%4B~!?}N5d5Z<_`hYfMoJJF!w$i?N99c4j'
    b'|grRT(tVTxbSj=ckA<wfm<$e8C94)@2`$<i<xsh|VZ`n614>jNR6J35_UQ!~Hyx9>teVls{WQ2+ruWHk}L!VllC+`P-'
    b'w{7`pG*HZY@Lpy-YF868B2KbzX(SJe?USabLCxwjD7?M<Be;QXZnOyvP!xF%2a#mGHdA>3V>!0AxYM3#1`L$oIPt=%%!;)3Qr7|~'
    b'YFMz<G!9*^&E_l0`n1KA3p4`oixn<pn;sQK#O#jbw}Mqts~Ht+lMQUQ4MvdxLF_(EbNk$b-'
    b'O`RN4wz^yR<f$PK9y$hE&btd)fmx*8P;)1LfndWSnW|LnPQ=)CIPi+tsFe>(mcni#?HyF=;yUmM8>9?cdxfg8-'
    b'*xkOp8k*1>XtsIDhT+$5M1?b=MiMnM1jr4M7{Z(o8s3r*Cg@YBSi{JTsd~M?74KYRb@`!yxC|FO;ub^Ss(29zAyI^j<h-'
    b'mLLv!Pk2q;8#>7thOs-'
    b'}hHlk=zLg)`|fi0g_`imiZIOT)W;J(L8)FI2*=jN0xC16+tlT#iAmgjmN~4c3M}o^g_IyVui_y1}7oV`94E6n8vtZ-'
    b'`Tl$eV9Swzy58XtP$eVxpOF5it=hb%>T$ReDOZCMwdJD%)s^(NuNmn#`cOY?fHNOb|(A62@h^pz+%Lg+cF~JR=1!lw&-'
    b'kpD>Xv(0zn5@ynlnvSToKS3UmF?HAT^eW!8z_LEunI;PRdqM?=xTFr<*C1M}&jQ@FHBY*NBf~x(JXoXhu7^XA%K6YG%(GzzhmPRV'
    b'YRs6^Z7zE^W=pHe#I_`l$j|5M9FBGQdm!<PzKRMNNBd^(PUX4d$g!DM`sgPgPG0f8UYHOaBwwD3blA*9uym~E~aMi|=rX1s2!63@'
    b'vz-?%F$&MufZD<?-tjA(}d0t;htd7#Q%OCLaWx>-M&f_=|R{P|Isv^>+V(FTrjUx0@-'
    b'9fOD9}6P2ZInJk8f7Ba2RReg|9mU5hf+{mx#bPZ#*@0=VHVH=CyKMCYS%*q>6)2>H*Q-'
    b'kzE}$G=}m}HvE_AMy@Xvr1#G(AqrIfb7m5<NF@Tg5>lo^rmo+B-lnz%>0nyDpsun}MIxM>E3cl2fDDmw&27tU>-'
    b'khG;Zl{swFh@6A===QU1GM{yTil#Qv?`$49#tK*RNWFQ$(kaXgkNDeC<J`;!3P%jlK@~QycVK=WAXaNAyE*kexD`6wGiRhD4P9bO'
    b'{NBZW7R`+R&NRb)2jZ>ok=g{^x$|iFOc2?Tn91b2i9&UT>r5LqgwaV%#^6xplDG_R4FC8JV4d5RkO*jT4~c9d=iaDv?wKNh4-'
    b';rVwd5Yph=u?=#6b+fbs8x(?JA$#SK5If9@#Y)q?Mb07iDAZ(IGAW1s{dGTTeykXD&s*_KXskr-'
    b'=7T@xIMG+_h^41cZ@X0rz+^T++tBoP*WtMjV}{Z!4o8Rspd|5=@zfDA#0(5Qc|!GbCwv`AH8c!OJ#9k97?74WJVP^??q5I}T*<y-'
    b'gNiORo3mm`U?=C=+n3xMK3+JFC-'
    b'KmQR{-HVo$WDN!+L`Rf`MJ6uuMkX27d=}BNMvdMe=(RLqwHX|Sk@CEY2UNaW)2jud9B=~OV~DR)(-i)RiXy+&&_vWNRaD-glE9in'
    b'^rB8AqB2BL|1MEGZqbsP2>n!tT18Suqd`=gF`Dw#ks!OI1_(9*Jno-B@e`5c{OlP69LyQ%v4H*oB?;A+#{Kko;dPUC-'
    b'$L{l*`W`K`-%EYib$X+-'
    b'Kj22)YQ2{WlFpdI<N~0+XESM9xnvrVVgNmYj;0GRXi^e+vJ^qgY1h&zFB++uB>~ZWC2js>_wA&1sdf3&;JJoJ60t'
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
    candidate = strlen  # noqa: F405
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
