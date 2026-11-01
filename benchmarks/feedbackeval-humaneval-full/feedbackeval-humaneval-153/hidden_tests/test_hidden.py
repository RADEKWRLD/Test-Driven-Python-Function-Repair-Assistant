import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [['Watashi', ['tEN', 'niNE', 'eIGHt8OKe']],
 ['Boku123', ['nani', 'NazeDa', 'YEs.WeCaNe', '32145tggg']],
 ['__YESIMHERE', ['t', 'eMptY', 'nothing', 'zeR00', 'NuLl__', '123NoooneB321']],
 ['K', ['Ta', 'TAR', 't234An', 'cosSo']],
 ['__HAHA', ['Tab', '123', '781345', '-_-']],
 ['YameRore', ['HhAas', 'okIWILL123', 'WorkOut', 'Fails', '-_-']],
 ['finNNalLLly', ['Die', 'NowW', 'Wow', 'WoW']],
 ['_', ['Bb', '91245']],
 ['Sp', ['671235', 'Bb']],
 ['Test1', ['UPPERCASE', 'uppercase', '1111']],
 ['Test2', ['capitalLETTERS', 'lowercaseletters', 'mIxEdcAsE']],
 ['Test3',
  ['oneUPPERcaseletter', 'TWoUPPERcaseletTErs', 'threeUppercaseletters', 'fourlowercaseletters']],
 ['Test4', ['ALLUPPERcaseletters', 'ALLlowercaseletters', 'Nolettersatall123', '12345']],
 ['Test5', ['ZERO', 'one', 'Two', 'THREE', 'four', 'FIVE', 'six', 'seven', 'eight', 'nine', '10']],
 ['Person', ['TEst', 'Name', 'naMe', 'AGE']],
 ['Animal', ['CAMel', 'hOrSE', 'DoG']],
 ['Vehicle', ['Automobile', 'CAR', 'SuPerbIkE', 'Z']],
 ['Computer', ['Laptop', 'DEsktop', 'TABLET', 'MONITOR', 'MOUSE', 'KEYboard']],
 ['Book', ['NOVEL', 'picturebook', 'COOkbook', 'Dictionary', 'Encyclopedia']],
 ['Computer', ['Laptop', 'DEsktop', 'TABLET', 'MONITOR', 'MOUSE', 'KEYboard', 'KEYeightboard']],
 ['Compter', ['Laptop', 'DEsktop', 'TABLET', 'MONITOR', 'MOUSE', 'KEYboard', 'KEYeightboard']],
 ['Computer', ['Laptop', 'DEsktop', 'TABLET', 'MONITOR', 'MOUSE', 'KEYeightboard']],
 ['Vehcice', ['Automobile', 'CAR', 'Vehicle', 'SuPerbIkE', '']],
 ['VehciceBook', ['Automobile', 'CAR', 'Vehicle', 'SuPerbIkE', '']],
 ['Animaal', ['CAMel', 'hOrSE', 'DoG']],
 ['Animal', ['capitalLETTERS', 'lowercaseletters', 'mIxEdcAsE']],
 ['Test1', ['UPPERCASE', 'uppercase', 'uppercasse', '1111']],
 ['Test1', ['UPPERCASE', 'uppercase', 'Animal']],
 ['Vehcice', ['Automobile', 'CAR', 'Vehicele', 'SuPerbIkE', '']],
 ['T1e1st1', ['UPPERCASE', 'uppercase', '1111']],
 ['Test3',
  ['oneUPPERcaseletter', 'threeUppercaseletters', 'fourlowercaseletters', 'threeUppercaseletters']],
 ['Vehcice', ['bIkE', 'Automobile', 'CAR', 'Vehicle', 'SuPerbIkE', '']],
 ['eightTeste3', ['UPPERCASE', 'uppercase', 'Animal']],
 ['AniVehcicemal', ['CAMel', 'hOrSE', 'DoG']],
 ['Test5',
  ['ZERO', 'one', 'Two', 'THREE', 'four', 'FIVE', 'six', 'FVIVE', 'seven', 'eight', 'nine', '10']],
 ['VehciceBo', ['Automobile', 'CAR', 'Vehicle', 'SuPerbIkE', '']],
 ['Test1', ['UPPERSCASE', 'uppercase', 'Animal']],
 ['Test1', ['UPPERCASE', 'uppercase', 'uppercasse', '1Test5111']],
 ['Animal', ['Do', 'CAMel', 'hOrSE', 'ZERO']],
 ['eightTeste3', ['aAnimal', 'UPPERCASE', 'uppercase', 'Animal']],
 ['TeTst3CTest3omputer',
  ['oneUPPERcaseletter',
   'TWoUPPERcaseletTErs',
   'fourlowercaseletteNamers',
   'threeUppercaseletters',
   'fourlowercaseletters']],
 ['Vehcpicturebccookoobk', ['Automobile', 'CAR', 'Vehicle', 'SuPerbIkE', '']],
 ['Test5',
  ['ZERO',
   'one',
   'Two',
   'THREE',
   'fur',
   'four',
   'FIVE',
   'six',
   'FVIVE',
   'seven',
   'eight',
   'nine',
   '10']],
 ['AnimAnimaonelal', ['CAMel', 'hOrSE', 'DoG']],
 ['_', ['yolo', '900000000', 's3cr3tK3y', 'GIMMETH3L00TZ!']],
 ['ClassName', ['XXXXXXx', 'AAA', 'ffffff', 'Bbcde', 'GHIJKLMN']],
 ['My_class', ['Aaa', 'ZZZZ', 'ddd', 'E', 'HHHHHH']],
 ['Another_class', ['AbCdEfG', 'Hijklmno', '12345', 'pqrstuvwxy', 'Z']],
 ['MYCLASS', ['qwerty', 'asdfgh', 'zxcvbn', 'QWERTY', 'ASDFGHJKL', 'ZXCVBNM']],
 ['testing1', ['TESTING2', 'TEST', 'test', 'tEstin3g']],
 ['AnotherClass', ['hello', 'WORLD', 'Python321', 'TEST', 'Extend']],
 ['MyClass', ['AbcDEFg', 'hIjKlmn', 'OPqrst', 'UVWxYZ']],
 ['YetAnotherClass', ['1', 'BBB', 'ccc', 'DDDDDD', 'EEEeeeE', 'ffffff']],
 ['OneMoreClass', ['AAAaA', 'bbBbB', 'CcCcC', 'ddddDDD', 'EEE', 'FgHiJ', 'kLMNop']],
 ['s3cr3tK3y', ['AbCdEfG', 'Hijklmno', '12345', 'pqrstuvwxy', 'Z']],
 ['MyCslass', ['hIjKlmn', 'OPqrst', 'UVWxYZ']],
 ['AnotherClass_', ['hello', 'WORLD', 'Python321', 'TEST', 'Python3yolo21', 'Extend']],
 ['MExtendy_class', ['Aaa', 'ZZZZ', 'ddd', 'E', 'HHHHHH']],
 ['MYCLASS', ['qwerty', 'asdfgh', 'zxcvbn', 'QWERTY', 'ASDFGHJKL', 'qweqrty', 'ZXCVBNM']],
 ['My_classMYCLASS', ['Aaa', 'ZZZZ', 'ddd', 'E', 'HHHHHH', 'ZZZZ']],
 ['ClassaName', ['XXXXXXx', 'AAA', 'ffffff', 'Bbcde', 'GHIJKLMN']],
 ['ClassaName', ['XXXXXXx', 'AAA', 'ffffff', 'Bbcde', 'GHIJKLN']],
 ['otherClahellorss', ['hello', 'WORLD', 'Python321', 'TEST', 'Extend']],
 ['s3cr3tK3y', ['Hijklmno', 'pqrstuvwxy', 'Z']],
 ['s3cr3tK3y', ['Hijklmno', '12345', 'pqrstuvwxy', 'Z', 'Hijklmno']],
 ['ClassaName', ['GHIHJKLN', 'XXXXXXx', 'AAA', 'ffffff', 'Bbcde', 'GHIJKLN']],
 ['otherClahellorss', ['hello', 'WORLD', 'ExtAbCdEfGend', 'TEST', 'Extend']],
 ['My_classMYCLASS', ['Aaa', 'ZZZZ', 'dddd', 'E', 'HHHHHH', 'ZZZZ']],
 ['Python321_', ['yolo', '900000000', 's3cr3tK3y', 'GIMMETH3L00TZ!']],
 ['My_classLMYCLASS', ['Aaa', 'ZZZZ', 'ddd', 'E', 'HHHHHH', 'ZZZZ']],
 ['s3cr3tK3y', ['AbCdEfG', 'Hijklmno', '12345', 'pqrstuvwxy']],
 ['YetAnotherClass', ['1', 'BBB', 'GIMMETH3L00TZ!', 'ccc', 'DDDDDD', 'EEEeeeE', 'ffffff']],
 ['Another_class', ['AbCdEfG', 'Hijklmno', '12345', 'pqrstuvwxy', 'Z', '12345']],
 ['MExtendy_class', ['Aaa', 'ddd', 'E', 'HHHHHH']],
 ['My_class', ['qwerty', 'asdfgh', 'zxcvbn', 'ASDFGHJKL', 'qwewrty', 'ZXCVBNM']],
 ['Another_class',
  ['AbCdEfG', 'Hijklmno', '12345', 'AbCdEfASDFGHJKLG', 'pqrstuvwxy', 'Z', '12345']],
 ['dddd', ['Hijklmno', 'pqrstuvwxy', 'Hijklmno']],
 ['ClassaNamse', ['XXXXXXx', 'AAA', 'ffffff', 'Bbcde', 'GHIJKLMN', 'XXXXXXx']],
 ['MyClass', ['AbcDEFg', 'hIjKlmn', 'OPqrst', 'UVotherClahellorssWxYZ']],
 ['_', ['yolo', '900000000', 's3cr3tKK3y', 'GIMMETH3L00TZ!']],
 ['My_classLMYCLASS_', ['yolo', '900000000', 's3cr3tK3y', 'GIMMETH3L00TZ!']],
 ['s3cr3tK3y', ['AbCdEfG', 'Hijklmno', 'My__classMYCLASS', 'pqrstuvwxy', 'Hijklmno']],
 ['_', ['yolo', '900000000', 's3cr3tK3y']],
 ['s3cr3tK3y', ['Hijklmno', 'pqrstuvwxy', 'Z', 'pqrstuvwxy']],
 ['ClassaName', ['XXXXXX', 'AAA', 'ffffff', 'Bbcde', 'GHIJKLN']],
 ['MYCLASS', ['qwerty', 'zxcvbn', 'QWERTY', 'ASDFGHJKL', 'ZXCVBNM']],
 ['MyClasss', ['AbcDEFg', 'hIjKlmn', 'OPqrst', 'UVWxYZ']],
 ['s3cr3tK3y', ['AbCdEfG', 'My__classMYCLASS', 'pqrstuvwxy', 'Hijklmno']],
 ['otherClahellorss', ['ClassaNamse', 'WORLD', 'ExtAbCdEfGend', 'TEST', 'Extend']],
 ['My_classMYCLASS', ['Aaa', 'ZZZZ', 'dddd', 'E', 'HHHHHH', 'ZZZZ', 'ZZZZ']],
 ['MYCLASMyClasssS', ['qwerty', 'asdfgh', 'zxcvbn', 'QWERTY', 'ASDFGHJKL', 'qweqrty', 'ZXCVBNM']],
 ['Another_class', ['AbCdEfG', 'Hijklmno', '12345', 'pqrstuvwxy', 'Z', '12345', 'AbCdEfG']],
 ['AnotherClas_',
  ['hello', 'WORLD', 'Python321', 'TEST', 'Python3nyolo21', 'Extend', 'Python3yolo21']],
 ['ClassaNamse', ['XXXXXXx', 'AAA', 'bbBbB', 'Bbcde', 'MyClasss', 'XXXXXXx']],
 ['ddGHIHJKLNdd', ['Hijklmno', 'pqrstuvwxy', 'Hijklmno']],
 ['qwewrty', ['ylo', 'yolo', '900000000', 's3cr3tK3y']],
 ['OPqrst', ['AbCdEfG', 'Hijklmno', '12345', 'pqrstuvwxy']],
 ['MExtendy_class', ['Aaa', 'ZZZZ', 'ddd', 'E', 'HHHHHH', 'ZZZZ']],
 ['AnotAbCdEfASDFGHJKLGher_class',
  ['AbCdEfG', 'Hijklmno', '12345', 'AbCdEfASDFGHJKLG', 'pqrstuvwxy', 'Z', '12345']],
 ['My_class', ['Aaa', 'ZZZzxcvbnZ', 'ddd', 'E', 'HHHHHH']],
 ['otherClahellorss', ['ClassaNamsse', 'WORLD', 'ExtAbCdEfGend', 'TEST', 'Extend']],
 ['ys3cr3tK3y', ['Hijklmno', 'pqrstuvwxy', 'Z']],
 ['YetAnotherClasUVWxYZs', ['1', 'BBB', 'ccc', 'DDDDDD', 'EEEeeeE', 'ffffff', 'EEEeeeE']],
 ['MnYetAnSlaassYCLASS', ['qwerty', 'zxcvbn', 'QWERTY', 'ASDFGHJKL', 'ZXCVBNM']],
 ['My_class', ['ddddDDD', 'asdfgh', 'zxcvbn', 'ASDFGHJKL', 'qwewrty', 'ZXCVBNM', 'asdfgh']],
 ['nYetAnotherCMYCLASSlassnothGIM!METYoetAnoEEErClassH3L00TZ!yoloerClass',
  ['qwerty', 'zxcvbn', 'QWERTY', 'ASDFGHJKL', 'ZXCVBNM']],
 ['ClassaName', ['XXXXXX', 'AAA', 'ffffff', 'Bbcde', 'GHIJKLN', 'GHIJKLN']],
 ['Python321_', ['yolo', 'nYetAnotherCMYCLASSlaass', 's3cr3tK3y', 'GIMMETH3L00TZ!']],
 ['test', ['AbCdEfG', 'Hijklmno', '12345', 'pqrstuvwxy', 'Z', '12345', 'AbCdEfG']],
 ['MMy_classMYCLASS', ['Aaa', 'ZZZZ', 'ddd', 'E', 'HHHHHH', 'ZZZZ']],
 ['x1UXXXXXXxVWxYZ', ['1', 'BBB', 'ccc', 'DDDDDD', 'EEEeeeE', 'ffffff', 'EEEeeeE']],
 ['Another_css', ['AbCdEfG', 'Hijklmno', '12345', 'pqrstuvwxy', 'Z', '12345']],
 ['test', ['Hijklmno', '12345', 'pqrstuvwxy', 'Z', '12345', 'AbCdEfG']],
 ['My_class', ['Aaa', 'ZZZZ', 'ddd', 'E', 'HHHHHH', 'E']],
 ['MMy_classMYCLASS', ['Aaa', 'ZZZZ', 'ddd', 'HHHHHH', 'ZZZZ']],
 ['My_class', ['ddddDDD', 'asdfgh', 'Aaa', 'zxcvbn', 'ASDFGHJKL', 'qwewrty', 'ZXCVBNM', 'asdfgh']],
 ['MYCLASS', ['Aaa', 'ZZZZ', 'ddd', 'E', 'HHHHHH', 'ZZZZ']],
 ['My_classMYCLASS', ['Aa', 'ZZZZ', 'HHHHHH', 'ZZZZ']],
 ['Another_class', ['AbCdEfG', 'Hijklmno', '12345', 'pqrstuvwxy', 'Z', 'AbCdEfG']],
 ['ClassNaMqwertyy_classLMYCLA_e', ['XXXXXXx', 'AAA', 'ffffff', 'Bbcde', 'GHIJKLMN']],
 ['My__classMYCLASS', ['ZZZZ', 'dddd', 'E', 'HHHHHH', 'ZZZZ', 'ZZZZ', 'ZZZZ']],
 ['My_class', ['Aaa', 'ZZZZ', 'HHHMeyOneMoreClassClass', 'ddd', 'E', 'HHHHHH', 'E', 'ZZZZ']],
 ['My_class', ['Aaa', 'ZZZZ', 'ddd', 'E', 'HHHHH', 'HHHHHH']],
 ['ddGHIHJKLNdd', ['hello', 'WORLD', 'Python321', 'TEST', 'Python3yolo21', 'Extend']],
 ['OPqrst', ['AbCdEfG', 'Hijklmno', '12345', 'pqrstuvwxy', '12345']],
 ['ClassaNamse', ['XXXXXX', 'AAA', 'ffffff', 'Bbcde', 'GHIJKLN', 'GHIJKLN']],
 ['otherClahellorss', ['ClassaNamsse', 'WORLD', 'ExtAbCdEfGend', 'Extend']],
 ['ClassaNamse', ['Aaa', 'ZZZZ', 'ddd', 'E', 'HHHHHH', 'ZZZZ']],
 ['MExty_class', ['Aaa', 'ddd', 'E', 'HHYetAnotherClassHHHH']],
 ['MMExtendy_classy_classMYCLASS', ['Aaa', 'ZZZZ', 'dddd', 'AAaa', 'HHHHHH', 'ZZZZ']],
 ['s3cr3tKK3y', ['AbCdEfG', 'Hijklmno', '12345', 'pqrstuvwxy', 'Z', '12345']],
 ['MExtendy_clasAnotherClasss', ['Aaa', 'ZZZZ', 'ddd', 'E', 'HHHHHH', 'ZZZZ']],
 ['My_class',
  ['qwerty', 'asdfgh', 'zxcvbHHHMeyOneMoreClassClassn', 'ASDFGHJKL', 'qwewrty', 'ZXCVBNM']],
 ['JDLRFD', ['AbcDEFg', 'hIjKlmn', 'OPqrst', 'UVotherClahellorssWxYZ', 'hIjKlmn']],
 ['test', ['AbCdEfG', 'Hijklmno', '12345', 'pqrstuvwxy', 'Z', '12345', 'AbCdEfG', 'pqrstuvwxy']],
 ['My_classLMYCLASS_nnYetAnotherCMYsCLASSUVWxYZlass',
  ['yolo', '900000000', 's3cr3tK3y', 'GIMMETH3L00TZ!']],
 ['YoetAnoEEErClasslassaName', ['XXXXXXx', 'AAA', 'ffffff', 'Bbcde', 'GHIJKLMN']],
 ['MExtendyc_class', ['Aaa', 'ZZZZ', 'E', 'HHHHHH']],
 ['MyClasssnYetAnotherCMYsCLASMqwertyy_classLMYCLASS_',
  ['AbcDEFg', 'hIjKlmn', 'OPqrst', 'UVWxYZ', 'OPqrst']],
 ['My_class',
  ['qwerty', 'asdfgCcCcC', 'zxcvbHHHMeyOneMoreClassClassn', 'ASDFGHJKL', 'qwewrty', 'ZXCVBNM']],
 ['MMy_clasMEAAAaAxtendy_classsMYCLASS', ['Aaa', 'ZZZZ', 'HHHHHH', 'ZZZZ']],
 ['', ['HhAas', 'okIWILL123']],
 ['$pecial_&_Cl@ss_name', ['YoUReXt']],
 ['123ThisIsTheClassName456', ['Ex1', 'ex2', 'ex3', 'EX4']],
 ['ThisIsTheClassName', ['ThisIsTheExtension']],
 ['NoExtensionHasUpperCaseOrLowerCase', ['1234', '5678', '9987', 'hello']],
 ['', ['abc', 'DEF', 'gHi']],
 ['SampleClass', ['Abc', 'ddD', 'eFG']],
 ['SampleClass', ['AAA', 'BBB', 'CCC']],
 ['SampleClass', ['aBc', 'dEf', 'Ghi']],
 ['SampleClass', ['AbC', 'DeF', 'gHI']],
 ['UVWxYZ', ['hello', 'WORLD', 'Python321', 'Exteasdfghnd', 'TEST', 'Extend']],
 ['AAA', ['AbcDEFg', 'hIjKlmn', 'OPqrst', 'UVWxYZ']],
 ['testing1', ['TESTING2', 'TOPqrstEST', 'test', 'tEstin3g']],
 ['MyClass', ['AbcDEFg', 'hIjKlmn', 'OPqrst']],
 ['AbCdEfG', ['AAAaA', 'bbBbB', 'CcCcC', 'ddddDDD', 'EEE', 'FgHiJ', 'kLMNop']],
 ['UVWxYZ', ['WORLD', 'Python321', 'Exteasdfghnd', 'TEST', 'Extend']],
 ['YetAnotherClass', ['1', 'BBB', 'ccc', 'DDDDDD', 'ffffff']],
 ['MyClass', ['AbcDEFg', 'hIjKlmn', 'Bbcde', 'UVWxYZ']],
 ['My_class', ['Aaa', 'ZZZZ', 'ddd', 'E']],
 ['AbCdETESTING2fG', ['AAAaA', 'bbBbB', 'CcCcC', 'ddddDDD', 'EEE', 'FgHiJ', 'kLMNop']],
 ['AbCdEfG', ['AAAaA', 'bbBbB', 'CcCcC', 'ddddDDD', 'EEE', 'FgHiJ', 'kLMNop', 'ddddDDD']],
 ['MYCLASS', ['hello', 'WORLD', 'Python321', 'TEST', 'Extend']],
 ['Tg1', ['TESTING2', 'TOPqrstEST', 'TOPqrsttEST', 'test', 'tEstin3g']],
 ['fffffBbcdeAaaff', ['AAAaA', 'bbBbB', 'CcCcC', 'ass', 'EEE', 'FgHiJ', 'kLMNop', 'ddddDDD']],
 ['Another_class', ['AbCdEfG', '1235', 'Hijklmno', '12345', 'vpqrstuvwxy', 'Z']],
 ['Tg', ['TESTING2', 'TOPqrstEST', 'TOPqrsttEST', 'test', 'tEstin3g']],
 ['TESTING2', ['AAAaA', 'bbBbB', 'CcCcC', 'ddddDDD', 'EEE', 'FgHiJ', 'kLMNop']],
 ['M1235yClass', ['AbcDEFg', 'hIjKlmn', 'Bbcde', 'UVWxYZ']],
 ['T1', ['TESTING2', 'TOPqrstESST', 'TOPqrsttEST', 'test', 'tEstin3g']],
 ['MYCLASS', ['qwerty', 'asdfgh', 'zxcvbn', 'QWERTY', 'MYCLASS', 'ASDFGHJKL', 'ZXCVBNM']],
 ['1', ['TESTING2', 'TOPqrstEST', 'TOPqrsttEST', 'test', 'tEstin3g']],
 ['TESTING2', ['AAAaA', 'bbBbB', 'CcCcC', 'ddddDDD', 'EEE', 'hello', 'kLMNop']],
 ['T1', ['hello', 'WORLD', 'Python321', 'Exteasdfghnd', 'TEST', 'Extend']],
 ['TESTING2', ['AAAaA', 'bbBbB', 'CcCcC', 'ddddDDD', 'EEE', 'kLMNop']],
 ['OneMorCassNaame', ['AAAaA', 'bbBbB', 'CcCcC', 'ddddDDD', 'EEE', 'FgHiJ', 'kLMNop']],
 ['testing1', ['yolo', '900000000', 's3cr3tK3y', 'GIMMETH3L00TZ!']],
 ['M1235yClas', ['AbcDEFg', 'hIjKlmn', 'Bbcde', 'UVWxYZ']],
 ['T1', ['TESTING2', 'TOPqrstEST', 'TOPqrsttEST', 'test', 'tEstin3g']],
 ['T1', ['hello', 'WORLD', 'Python321', 'Exteasdfghnd', 'TEST', 'Extend', 'WORLD']],
 ['MCyClass', ['AbcDEFg', 'hIjKlmn', 'OPqrst', 'UVWxYZ']],
 ['_', ['yolo', '900000000', 's3cr3tK3y', 'GIMMETH3L00TZ!', 'GIMMETH3L00TZ!']],
 ['1234GHIJKLMN5', ['TESTING2', 'TOPqrstEST', 'TOPqrsttEST', 'test', 'tEstin3g']],
 ['YetAtEstin3gnotherClass', ['1', 'BBB', 'ccc', 'DDDDDD', 'EEEeeeE', 'ffffff']],
 ['Ye1234GHIJKLMN5tAnotherClass', ['1', 'BBB', 'ccc', 'DDDDDD', 'ffffff']],
 ['M1235yClass', ['AbcDEFg', 'hIjKlmn', 'Bbcde', 'UVWxYZ', 'AbcDEFg']],
 ['Tg', ['AbcDEFg', 'hIjKlmn', 'OPqrst', 'UVWxYZ', 'UVWxYZ']],
 ['Ye1234GHIJKLMN5tAnotherClass', ['HHHHHM1235yClassHExteand1', 'BBB', 'ccc', 'DDDDDD', 'ffffff']],
 ['TESTINT2G2', ['AAAaA', 'bbBbB', 'CcCcC', 'testiffffffngg1', 'EEE', 'kLMNop', 'bbBbB']],
 ['_Exteasdfghnd', ['yolo', '900000000', 's3cr3tK3y', 'GIMMETH3L00TZ!']],
 ['T11', ['hello', 'WORLD', 'Python321', 'Exteasdfghnd', 'TEST', 'Extend']],
 ['AbCEdEfG', ['AAAaA', 'bbBbB', 'CcCcC', 'ddddDDD', 'EEE', 'FgHiJ', 'kLMNop']],
 ['YetAtEstin3gnotherClass', ['1', 'BBB', 'ccc', 'DDDDDD', 'bbBbBeeE', 'ffffff']],
 ['AbCdEfG',
  ['AAAaA', 'bbBbB', 'CcCcC', 'ddddDDD', 'xcvbnAAAaA', 'EEE', 'FgHiJ', 'kLMNop', 'ddddDDD']],
 ['MyClMasss', ['1', 'BBB', 'ccc', 'DDDDDD', 'bbBbBeeE', 'ffffff']],
 ['TgTg1', ['AbcDEFg', 'hIjKlmn', 'OPqrst', 'UVWxYZ', 'UVWxYZ']],
 ['Another_class', ['AbCdEfG', '1235', 'Hijklmno', '12345', 'vpqrstuvwxy', 'Z', 'Hijklmno']],
 ['YCBBBLASS', ['1', 'BBB', 'ccc', 'DDDDDD', 'ffffff']],
 ['T1', ['hello', 'Python321', 'Exteasdfghnd', 'TEST', 'Extend']],
 ['M12ss', ['AbcDEFg', 'hIjKlmn', 'Bbcde', 'UVWxYZ', 'AbcDEFg']],
 ['BBBB', ['AAAaA', 'bbBbB', 'CcCcC', 'testiffffffngg1', 'EEE', 'kLMNop', 'bbBbB']],
 ['_Exteasdfghnd', ['yMCyClassolo', 'yolo', '900000000', 's3cr3tK3y', 'GIMMETH3L00TZ!']],
 ['T1',
  ['hello',
   'WORLD',
   'Python321',
   'Exteasdfghnd',
   'helHHHHHHEHxteasdkLMNopfBBBghndo',
   'TEST',
   'Extend']]]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-qaIJF+b~Zbc<S8jCCi0e<22G-Svi2{PK(1Z2r-'
    b'vov2VoUY8CKpN`kcvW@pIhjmgV}F=@|NSrj`yb<<e*gQ=KmP4+|N38lom$%;fBTD+KJsy&_4*xh>gs9db<*A?&C(=aom2QsKeePK'
    b'Bkj_BuWCj5Nq_v$AAkMlzx`$9WGnZ5`K~3?ex<IO^hn9A*z%R{E;93!H2SqOy{cNx`=oN``13ONnvA7$m0e1&Q_s5ATD^7VUe2jA'
    b'@y&L;+3D`yD*v{xAHB0Ikv}hE!<V#?CO>Lr^9XyeG;x``NwaxRpXIjPwx-mtC-Yj%$i3Z@+x_!08f#ot{j}5XN$Cu3nE3MXTx-'
    b'`<l<U@UTd(JMFQz<pIezZQ`MHdD+g^ma*^*t{`j*qRPi@+FD!xx;scmQJgGKhkLTw~fmF)UFR5^oIrS3dw=IKsfX`em2(J^T~%A)'
    b'1=rpLGy3*w%=8U^GQ<0<j3RHJkiZBqN9AeNnLFEDUg;jVLb&)2;s6CGAlyE(Tiau03)^D<3VoigXCy+;|fq_%6ev9)>0+q~;agT`'
    b'5EV|ZG>GM6D45LN&4GKs$Vy=AOCPcH4WJ8O5nX^v$sy{_Hz=1<8P`1AoL#-'
    b'Q+Sw`lwGGE+7s>@1?plEGEVN%mIyHLnP5IZbGO&SQ#Jp50o$RE`f(f&M&{<)z+Ocn0R0!R@xY*J4Ryw_)B=@AUmpV!x?ru6w4wif'
    b'S$XtcH7ZPnA!ll&U4=3Gd2{2K6@RMfRLBSLre)E1hn0`psjz=hEk&m+7@s?R00Arg~bVg!xd6o=zKUSjm_9V*PuMy6JxmNLQMbmy'
    b'h${ri|A300rcSyRqs5Q18<6TNsbf^SO;*Sdy8z<<ODE_)$-9iLd?op?x^`olK=p-_sz11(zHi`L<bRzir%-'
    b'nUz|$1A$?^t@^;vQ%iR1l~cTQt8xuGsLJ}Fnl6-0E)<e-'
    b'=l5<v6PQ}zzendu{=5u$&w1`T&!j4~QXo4v?bp$q%A&YHs{(y!z^?<)-'
    b'pwy8wno=?rrhYuY^k=I>Bco*lld+#jAZIiRw`qR=9%&1Cf%%U<0EoR_1o2qdRiBL0S%O3LQ!KC1Ag11?+R`&Fg*8G{@9n5j>hj<t'
    b'kmS^+tswaC<E+TPlbp;2zcH}H+L&HTZPY~HDXAH^#$%yLn;>CE3(R?3<hoWIZH2mEcm`o<mE7*D{BdQfp=lCI_rQCZ{C!^x9-'
    b'N!H+vo`8GHs0&%-3ln|XkdSE-B)H_jb`Hm0-'
    b'`RL3`!%T~1W8A@93GvRv*!1cS%U1>EHIl8O)Nn^Fdn%YK76h@k5Hywz^f(RY`D?lTCOIsgZ=A%xXbBiEgkfSbFWCNW$S?e4#bO-'
    b'$TQZa6&Jq@vRAh(3#!C&oN%}Fp(<_92dx68CQ8za*)mbcIrc$eNQkKTL191JLqJ3D5f)wDl`pR;zWMvL1}RFx~00pZoUYr#CIZMq'
    b'Cs<*F!@?i|*ncX0<%4{h~{1M%9Dm;lwXqd|Hq-XpC$&Ts^m?_B^ydBEn?juk@E@lo}BOX-wtv|ZqBT!kSXvlg@jg#*(`O36zAcjJ'
    b'K?MZB5cWJrX809_+LHmM`~0{#aC8=5IRmDZejvYGaP05KpLUj#n6R68sz@d-51RvF)-'
    b'_}ZQguN2Btk~D9HiQESRnOyKlJJnoHxf|Bld`J-bi|kM}W3}Hl{5Z@xa1E+^jn;?ity-'
    b'(&iDY&><%Y)WT%Lgy54m%*Y&dSQ%=QXQyA`Xk`phZ=2Vr4GYt4>RVM6X?DR%0KXQ4gIesEE^uhB677B^A`w_GJ%!6qG=VtnXl^!j'
    b'Gl8LEle0GL9*H4nibVhHek0z*EA7QZ7rxa^DLCpeVL;GUv6;Z2j$tvs@Js<i_|TEa_~)LHjnMxW8d1dTbdP{$gzAq)@;1TE$lSd_'
    b'E5!Q5K;g9lq>&fVLrQkg3jwjLDkjbG)~35hr;G|TCOMy+=0sA<%E@LI)$TH)>Bb;@<nkLkFOXElry08Y$Q?}!v8y-'
    b'Hf^V*aQiaVFJ{TbTjm1q024y(tXfw3(Vbm+7}-9R{e+n_>`|Hs%4t&i}=sr;F$<KC!Q!-'
    b'qN|DQE*7|!VEnP$BF9zjcfNx9GZja0?W`3#X!gb2$P1ct_5gt?4uY?pQ~Z)R;#bSIXAj^5#Pf<7~oz=JQG*2T3KPzkp9g)Elk?a6'
    b'hu?+pjyD-'
    b'8O_FmZzPtEDx7r)Qj^BES|~BihefzElOoEzGSh?%l@uyK_13El^Y1i5J$sEOtOgEegFpo>#|5l`q%TH<;GhK2623(n&y;U@tpKzu'
    b'K#Bk-IYP%RSROI@+=zLHl3=`Zxo2!k3u}k>p$Zy)V!sInw@tbuj)G-I4#3UjSSP;hI6?3yp-'
    b'(ss)*KYFrswb<M5wOMOr0GL9_;PI?2L}|FhCyGrt}<j{%K_7sd-'
    b'32;F1yzh}Z>$J*xo@6$|2t#3~2*Wf&^4@<wFYp_FG5Tz{$u#hH-5v%p>Zcslkb-'
    b'}bZcgq>h@$cJR4b2C0paKzYCx`Jg#IB`bl<eFy%Sg<SjANnnd0o+<-'
    b'zk3s26>CO3fRri}944PffD^b*zln)7@l6vFs3(W+^TzpsobucSK$N8?6BsuCN`@XlfegJiCSemeCAKFpiu_44F&LsW<B9XQjuJGM'
    b'n{^)BwYCgsNM;@5zYhPs$#+!~K@T2|tHGamP1a<O6GhdC@caNwOvivDagvxCE=*I2#2`dQa2fz4c`=uk3nqz~U;^IJ%-'
    b'jw<A=!3x2);IOjSizJ@H!;C#Nm08B}U81(R_y>M21rz-(IF=$W2H)%mVz7#}y*TASYm^FxF-AErU2F5x(P&!z-'
    b'ZH<R+p;KHt{nBivwbxHxlH_=N<`B+}0{u14|!t_8LLK}T-'
    b'i<CJhOpgjnG^Amjq25uo1>Kfr=asUofv?Nm1=!wLEC+SyXN8qknt}m_#v$n_(_ATF#TYR8+vk4<7ExQ?hW}xy#tDp$uq|#u!0sG8'
    b'OliGqie%VQK`&RBg;v1g?goMWc#Tf~pYveS%86G0^hV*fqJ~g~1HU&lmkgK5+iPZS&6cEP;RnVSpU)*d|coy_bv<a9k{LY;kyD;n'
    b'g;D9i~w>f)@T=<k&=pCKAIJ?_;qzoFQzzV5(DGkpQX%S<RX~IddjM!qq%bY=UdP;1!cMyRqG!p>ZF&r$1T4j7RIeeE<6(;3jH-'
    b';yNY&H{O>6zzI&Fxn+`PtCrJ&}p*G#Aa`0;?B5jDQ0gCS-ykG@K~yL=b{oOvAUPjdDXWxZDnJ_JL0r&iGZ5T`RPaUS(Uva9AWP3r'
    b'~tU;Z|I2A<_?S(ohWi0mDav0`TbY?50k#_iYI)z(RJ%m}ZMj+ytM1C_)yB_Y4DhAOFiYcXnTJ0P-'
    b'u0DP{r3dbx;*wQJ5aP5d+9BKx!Cq@fP?TN3?9U_KJxbR!@q26A~*7@MXs*nC2NqIrq)=ae+HG$Jex#jxPS2)s$`%Y56Z|6j^LCbK'
    b'*SlfZozDGZSIi+$ssHjgP|Yza^p#+yiS$PJw*rpkQybz2{isEo>xk+cRuQ)z(1b1Wa!CPp3pVUi(3V(y?$gv_wG?T0i-'
    b'qrDT(`jb)|M?Ll+;g%}#dO^_)FFQ6}#8@U7^~O^|A9fba6Q^eH4y}PbLLzyobaaJ6tc{@-R1V*{QP9}MBNQkW9;JhxMWF%y-'
    b'RHA^g9wZ?sV`y)VpFCKMs2tZ$p%JAF!hcMN~Smim39b<h1#X5`dr4y#YPlC*U$@#eJCgwv85wOFn)f8O_m*TBnNrY5><!WfWS=O>'
    b'XeeEa}1Lb>RCu?Q2-rd3e(;<%omPa!&Kaua>Obo$H>)w#J`QKAI(&Si^hiY5Jw<>QLD-PfLgEE6Z}$a6~`Wb?64B&E<+B*u2e2Hd'
    b'LwJnvxsq|Nx0y)8E**A&I}{IF?Pm`e2?tr7CU6jY$xW;j1$w0X@5$*M)FKxf?g3zGN8vx85=FK6-l$#(+-'
    b'f;ZEemmNShfECQgm**}ruZNCt43TphEg6}6?ZNE=CW4uUB_C1x7QWH9zrE;P==Z788n=f}$MjiJ4Y>7n8bQEUicOgemXFd7xauM#'
    b'uOGaCUbMfhy+ehQagRpzem>xyLvyg-tSb3R=P=@!N^2odI@n!8X=gV-'
    b'=#b&>WN0j829!M~69ZCQ!mF~WGQ<k|ociGTiHH3fSX9IX)eM@xi_9<QTwUtk~f=l6|JQUnNoO1;KTA=8BEB{7qn0iCjhq`hKSHW-'
    b'cH4ipqqaDj5{LO-2iF|oyR>cM3r4lNi6OR*a68hpX9c6XSId=>P=jYUNW1Y~_{-'
    b'%j{PCH`m_a89rr0!6IA+}?@}o<p~wZhh8*Sw7a*WG*0L#WzxVt_5+RH0k4Afv?0jL;VN-'
    b'?1$=7yM?dO(hb90YQKIn#c5##YXv`qVq^oN#P<(|`Q4J=B{m`e4T%sVZ!-'
    b'oJHCYEYj3QM`6h=6aLG%Vh!7sc`q#!YVyqWpYWoEqeicY~s#|T$|t&urT7-'
    b'(#NQ2lPLRa!%nGF`kg#x(ZZ)A4ULe2}eC*f<LU$l}G_#b4U*4F>jKX7D1tUa%;3hnZiy(Xlw)LROM*RWq-'
    b'64Y}jRm7qHXw$GEN`0dL1xixpz+mzx8%K^doERs4lBRu;vniVhCCly^KHc!*!R|;UdA&T?BSTN!wEp9Z9lsT}ZsS`X-o-vKjW%wb'
    b'|6q|+AcIn!Z66L!~0VxoOO$wE3(RSytm9aAEf}-'
    b'P1p4X#@YaSTgYaO+wFi0J#H{(1jaiqe@D>5o&3!O)`ymM!`nMPttU)oAc<I2`*-'
    b'pYjGC}6Qlv#F(F96%)brZrhxnJscSL3tLIh6O&~(iS;enY@7p+;MPp8d<PwyloMJ90^Do{U#KV$bIk`+&Jl(YF_y4Th%NPnU$8$7'
    b'B)SKlj%D>Zxi3c!ovXJnenSQe%J>Jae5~hom<`m5X!InFCh+xPsnbQYX<M|6Rap`SVUUl_?bOBRmHT7)9C~&eriK*Y<d`DJ||n+3'
    b'f6|VT}c3Z;Y@mial!SK9GmuyFu-+xJI}W~xba3iZmKE&HvDrhaa3ZFOQ9GPn~~qCkYXu+=OIYZG^_&+>`6-'
    b'>n>M_{ZE(sK2I$85wT!A@^9`y!V7yzQ63o;P64HgVgKOx=Ew$cfSD;4kVj}~y$8vD8go1eO0;6NDPRWo8-'
    b'_JgSHVFabii1IpEeY=N_+n)(KnB~Z9%pKZXH4N@ss=Ngj6xI1i3kAe7#$pO$PKOmZ27H?5a%N0PX;iKD!`~2X-'
    b'y8fbb<|bT%b@L`KCt0YbYA?O8W3PYV*_vaLm}Zz_t`+4e?rZhLh;=@=$i{*u<-'
    b'Jav32FNsDwRzq1?s_@S+t2&&K&2@yeQ@rnuX83fOO<DDS78elqs3_}|E@hpNh-iGA7XH2k9SY0BY&*gO9=e@YDDXkW&Kxvv%n9*d'
    b'~MOfgJP!g5Gkh~!gKRuB*k}>Krscj|_#CA~I7?J^l!QFAbN~Xl#H2@>p?6UI2r<eD@71ZBjS2mfR;)&1q%4F6)BQuh{N#y3-'
    b'49f!>?08w;$&27NLC25WogL>3;e>bqg5jh?)C$v2m*L_)V=porwTgbm%g;0p3Y;qT;MsUd1y{0)hF}EZu4ugRq97<>?6$;#7>fgr'
    b'*9k#4D{%oXVO)Lo`j2;aG(_l0VbS>3LQFg4Zp*Q`A1|57x`-'
    b'(vy3}&@nis%AvwB#rSMCI(#R`W=Oc%f+)7kENQBRyH4ml*ot4GV+Tlwvj4J-'
    b'l3uIbzNnjh_nE@W)ovG;{$NCtdkOuF4!ey_yeYd92AXO1(B@_YYwErRBPd){4vk4pT}>(P&1);elGFVj!Fgk}l2H*^s@-'
    b'a__A9P1zl<1C5e<+j`699d(~gb4D^lrVa0#nGu7TbK-8x%g;}^9EdFdF-gJ2-rKekQ!=18E-'
    b';L!Nw`yb_%J(!UbpJR0$_=>EFq@77FIE6*|LadRrIMSi-@;Uo0Fb=XBoVrqfwb_WXN&fOX-'
    b'^teLgL>=ye>rT`X!=33;UdWa^wv_u}F9nWgI7L6rDs=eD6R^Sj}Pzb%T?<+lFheQzVx*Rr+vo$d5;?w^)DfLkhnnYrF7EEC#(jgJ'
    b'lL<nPwF%t3KfQT-v#(t-G5h3z`DeZJ(xu+L?ajt-243w-m3+0qD_EGB%gA#{aiRwY1JZ^JOIL-twqB7uE-'
    b'?tudO7vX3^1=xV*a5gHUO2`!l%fPF4lWR0LYVj9pCnR*s9b(&?~wy2<;sN-'
    b'4JgB2$9tw8zY{W8(_hpBcdK$a@@*VkC1TUdjnjC~n0)m<9AZ$?*PReO)g?Dv^d-'
    b'ecA_7=`r<P9~i;Oq_C}9*Irns$S;IY0faR<Q>vsf+qMdK+f3NFl^)(z^VgFO=YY7_~U-'
    b'AA!m!KD^EQy(`x>vkxJJ~D)`!i>!{;s>@fBQ<0#8WzX?f7{QQj+4#`YpP*fAAf^n#1_cbEnzb0z}x{NK1#C1q-'
    b'8?+Qj$jVFe%tu(&Gw8Is)VGMsLUW)k|bAvEkzwK>jQnpM#lBk?xX_T}TMz8t@_HUtIAR_$y5x!|$6;X|Nvu$uA=<lFe3p2PiX8Gm'
    b'1u)5}B=S#*D<b9Sun*Tk5#}^zoZS<36rv3a$mz6dIBvRO0`LA8|yDjuf)=tgJ0rjdR(^PtS2$?&V?}RgeIaMd&9=DL3jo7=3_Q3v'
    b')Tp9ws$5k}u}2;?Cm)2|1v>Cl}VFk8xf-jC^dJ1kvz>VALoTy36uBI6O{6IGlS}AY2*S{UrO3Y3trpNaq=AML_6RMh95&rBL-jO-'
    b'QielaGOhy|Db|I8@vPX?A`4P$~BHwPNmw>x0p(4ih4~ah6dSP+&=0Oyck6R6O`ONY_vvb70J#%P3}t$TuNB5+H5@MoS@Zmp;e)L#'
    b'AEhkiTMrDxMJeu{g!P!<M`W=3w*}bF)zK2pmB^;$TfFHsgBYJmVGX++oB^d05x^!Gsntuup(4hI<C8R3MIi_J|D~q~iD|_JW9oU1'
    b'GL!Y&PMR@CDgW)DuMH?@PC@;P;KcA(vu@aS#p1HlQpVRA2EIQR1&{)Wu{?BW{#|ADx7Wc;|y;tuYdade6`f<-'
    b'>j?4q+0lVGEj#l}}7#$_jpZyxbv!q)S-0Munn;cH-'
    b'r+e``#5*c01;pvL0B?TXX+@gi=HI5UojQu>Y!+tUZhVlsDbH5VLB#+JUZY~Vh3SYkm5ZtSbYOcWJb77u~|of>Br6fVxujrcoe#)B'
    b'=h{7(2#^Y}|)fHnRif`+;r!dVP(yOd~a&#@`NM^g}9s@OKiMUM1pI6g7n$;S~)jgx-'
    b'E!+5fq#rGF&%m9c?<ncNV5%btd<LT<qI1p{$&eR72bN>DR0M!pJRs'
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
    candidate = Strongest_Extension  # noqa: F405
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
