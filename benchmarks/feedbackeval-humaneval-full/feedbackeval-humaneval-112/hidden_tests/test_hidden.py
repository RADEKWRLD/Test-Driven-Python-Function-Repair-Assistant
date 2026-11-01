import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [['abcde', 'ae'],
 ['abcdef', 'b'],
 ['abcdedcba', 'ab'],
 ['dwik', 'w'],
 ['a', 'a'],
 ['abcdedcba', ''],
 ['abcdedcba', 'v'],
 ['vabba', 'v'],
 ['mamma', 'mia'],
 ['racecar', 'ace'],
 ['level', 've'],
 ['noon', 'on'],
 ['abcba', 'bc'],
 ['kayak', 'ka'],
 ['deified', 'de'],
 ['radar', 'ad'],
 ['tenet', 'ne'],
 ['reviver', 'er'],
 ['refer', 'fe'],
 ['non', 'on'],
 ['abcba', 'ne'],
 ['radar', 'a'],
 ['vee', 've'],
 ['ave', 've'],
 ['level', 'ave'],
 ['ve', 've'],
 ['er', 'ervee'],
 ['bc', 'ervee'],
 ['noon', 've'],
 ['ve', 'v'],
 ['', 've'],
 ['deified', 'ne'],
 ['WqHkuRXIf', 'WqHkuRXIf'],
 ['ervee', 'vrefere'],
 ['vnonrefere', 've'],
 ['nooon', 'noon'],
 ['vrevivere', 've'],
 ['racecar', 'racecar'],
 ['ratcetenetcar', 'racetenetcar'],
 ['deified', 'deifiedracecar'],
 ['vnonrefere', 'v'],
 ['er', 'e'],
 ['noonoa', 'noona'],
 ['ve', 'WqHkuRXIf'],
 ['racetenetcar', 'racetenetcar'],
 ['', 'e'],
 ['tenet', 'tenet'],
 ['vreviveere', 'vrevivere'],
 ['tenet', 'radar'],
 ['racecar', 'deace'],
 ['refer', 'er'],
 ['racecar', 'vrevivere'],
 ['dei', 'deified'],
 ['re', 'rer'],
 ['vnonvreviveererefere', 'v'],
 ['accce', 'acce'],
 ['vnoone', 'v'],
 ['deifiedve', 'deified'],
 ['noner', 'ervee'],
 ['refer', 'vfe'],
 ['refer', 'vnonvreviveererefere'],
 ['deifeied', 'deified'],
 ['racet', 'racetenetcar'],
 ['abcba', 'abcba'],
 ['radar', ''],
 ['refer', 'refer'],
 ['', ''],
 ['vnoone', 'xUJIA'],
 ['onooon', 'nooon'],
 ['tdetenet', 'tenet'],
 ['ve', 'WqHXIf'],
 ['dveeifieacced', 'dveeified'],
 ['tenetvnonvreviveererefere', 'tenet'],
 ['dedi', 'e'],
 ['dedi', 'dedi'],
 ['r', 'reviver'],
 ['referr', 'refer'],
 ['kaonyak', 'kayak'],
 ['radarr', 'radar'],
 ['tdetenet', 've'],
 ['reviver', 'de'],
 ['radarr', 'radarr'],
 ['non', 'non'],
 ['raderveenar', 'deifiedracecara'],
 ['dei', 'ne'],
 ['racetenvfeetcar', 'racetenettcar'],
 ['ne', ''],
 ['avreviveerebcba', 'bc'],
 ['erve', 'ervee'],
 ['noxUJIAn', 'non'],
 ['racecar', 'ne'],
 ['vffe', 'vfe'],
 ['bc', 'bc'],
 ['e', 'ee'],
 ['none', 'vfe'],
 ['vnonreeferrer', 'v'],
 ['onooon', 'onooon'],
 ['raderveenar', 'raderveenar'],
 ['ve', 'eve'],
 ['nonnon', 'nonnon'],
 ['raderveenar', 've'],
 ['vee', 'vee'],
 ['lelvel', 'ave'],
 ['vededie', 'vee'],
 ['raceetenvfeetcar', ''],
 ['refer', 'fee'],
 ['acreferrcce', 'accce'],
 ['racetenvftcar', 'noxUJIAn'],
 ['dde', 'deified'],
 ['racecar', 'aei'],
 ['kayak', 'xyz'],
 ['madam', 'ab'],
 ['rotator', 'z'],
 ['tattarrattat', 'bcdfghjklmnpqvwxyz'],
 ['abcedeba', 'aceb'],
 ['level', 'ev'],
 ['racecar', 'a'],
 ['rotator', 't'],
 ['asymmetrical', 'lme'],
 ['asymmetr', 'asymmetrical'],
 ['mmadam', 'ab'],
 ['lme', 'lme'],
 ['aceb', 'lme'],
 ['kayak', 'lme'],
 ['racecaeir', 'racecaeir'],
 ['abcedeba', 'abcedeba'],
 ['t', 't'],
 ['xyz', 'xyz'],
 ['racecar', 'raccecar'],
 ['racecaeir', 't'],
 ['kkayk', 'xyz'],
 ['mmadadm', 'mmaadam'],
 ['kayakaceb', 'abcedeba'],
 ['mmadadm', 'dmmaadam'],
 ['racecaeir', 'racmadamecaeir'],
 ['lme', 'a'],
 ['mmadadm', 'bcdfghjklmnpqvwxyz'],
 ['rotator', 'asymmetr'],
 ['kayak', 'ev'],
 ['madam', 'aab'],
 ['racecaeir', 'ev'],
 ['mmadaaeim', 'dmmaadam'],
 ['aab', 'asymmetrical'],
 ['kayak', 'racmadamecaeir'],
 ['ammadadm', 'mmadadm'],
 ['asymmetrical', 'lmme'],
 ['kayakasymmetr', 'kayak'],
 ['t', 'xxyz'],
 ['aei', 'mmaadam'],
 ['bcdfghjklmnpqvqwxyz', 'mmadadm'],
 ['bcdfghraccecarjklmnpqvkkaykwxyz', 'bcdfghjklmnpqvwxyz'],
 ['adm', 'mmaadam'],
 ['madbcdfghraccecarjklmnpqvkkaykwxyzam', 'madam'],
 ['kaadmyak', 'xyz'],
 ['aceb', 'aceb'],
 ['rotrator', 'rotrator'],
 ['bcdfghjklmnpqvwxyz', 'ev'],
 ['ab', 'ab'],
 ['bcdfghjklmnpqvqwxyz', 'bcdfghjklmnpqvqwxyz'],
 ['tattarrattat', 'xxyz'],
 ['racecar', ''],
 ['elevelv', 'ev'],
 ['ev', 'ev'],
 ['racecaeir', 'rotator'],
 ['mmaadam', 'mdam'],
 ['asymmetrical', 'bcdfghraccecarjklmnpqvkkaykwxyz'],
 ['kayakaceb', ''],
 ['rotrator', 'ab'],
 ['elevzelv', 'emadbcdfghraccecarjklmnpqvkkaykwxyzamv'],
 ['racecar', 'racecear'],
 ['mmaddadm', 'mmadadm'],
 ['tattarrattat', 'mdam'],
 ['madbcdfghraccecarjklmnpqvkkaykwxyzam', 'maraceceardam'],
 ['madam', 'acebb'],
 ['bcdfghjklmnpqvqwxyz', 'eacebbv'],
 ['lme', 'xyz'],
 ['tattarrattat', 'mddmam'],
 ['ammadadme', 'ev'],
 ['t', 'xadmxzyz'],
 ['rotator', 'racecear'],
 ['kaadmyak', 'kaadmyak'],
 ['abcedeba', 'a'],
 ['bcdfqvwxyz', 'bcdfghjklmnpqvwxyz'],
 ['madam', 'elevzelv'],
 ['abceadmdeba', 'abceadmdeba'],
 ['mmadadm', 'mmadadm'],
 ['kayak', 'lmxxyz'],
 ['abctattarrattatedeba', 'abcedeba'],
 ['racecaeir', 'xadmxzyz'],
 ['kayaak', 'lmemmadam'],
 ['ammadadm', 'madam'],
 ['kayakaceb', 'mmadadm'],
 ['asymmetrical', 'l'],
 ['mmadadm', 'rotrator'],
 ['bcdfghraccecarjklmmnpqvkkaykwxyz', 'bcdfghraccecarjklmnpqvkkaykwxyz'],
 ['maraceceardam', 'racecear'],
 ['asymmetrical', 'asymmetrical'],
 ['bcdfghjklmnpqvqwxyz', 'bcdfghjklmnpqvqwxz'],
 ['tattarrattaasymmetricalt', 'xxyz'],
 ['xadmxzyz', 'lmemmadam'],
 ['dmmaaeacebbvdam', 'mmadaaeim'],
 ['raceccear', 'racecear'],
 ['raccecar', 'a'],
 ['asymmetr', 'asymmetr'],
 ['aab', 'racecarab'],
 ['kkayk', 'tattarrattat'],
 ['racecaeir', 'racmadameceaeir'],
 ['kayak', 'lmemmadam'],
 ['bcdfghraccecakrjklmnpqvkkaykwxyz', 'adm'],
 ['elevzelv', 'xxyz'],
 ['bcdfghraccecarjklmmnpqvkkaykwxyz', 'mdam'],
 ['mddmam', 'bcdfghjklmnpqasymmetricalvwxyz'],
 ['bcdfqvwxyz', 'tattarrattartbcdfghraccecarjklmmnpqvkkaykwxyz'],
 ['teacebbvattarrraattat', 'tattarraattat'],
 ['maraceceardam', 'maraceceaarda'],
 ['xylmxxyzz', 'lme'],
 ['asytr', 'tattarrattartbcdfghraccecarjklmmnpqvkkaykwxyz'],
 ['madbcdfghraccecarjklmnpqvkkkaykwxyzam', 'madam'],
 ['bcdfghraccecarjklmanpqvkkaykwxyzxyz', 'bcdfghraccecarjklmnpqvkkaykwxyzxyz'],
 ['racecaeir', ''],
 ['asymmetrical', 'teacebbvattarrraattat'],
 ['xxyz', 'abcedeba'],
 ['ammadadm', 'maraceceaarda'],
 ['racaecaeir', 'racmadameceaeir'],
 ['asytrmmadam', 'ab'],
 ['rotrator', 'kayaak'],
 ['rotrr', 'rotraatasymmetrr'],
 ['racecear', 'bcdfghraccecarjklmnpqvkkaykwxyz'],
 ['tattarrattartbcdfghraccecarjklmmnpqvkkaykwxyz', 'tattarrakayakasymmetrttat'],
 ['racmadameceaeabcedebair', 'racmadameceaeir'],
 ['a', 'a'],
 ['tattarrattat', 'bcdfghjlmnpqvwxyz'],
 ['abcedebaxxyzxadmxzyz', 'abcedebaxadmxzyz'],
 ['abcedebaxxyzxadmxzyz', 'racmadameceaeir'],
 ['eccecar', 'madbcdfghraccecarjklmnpqvkkkaykwxyzam'],
 ['asymmetr', 'mdam'],
 ['lmxxyz', 'bcdfghjklmnpqvqwxz'],
 ['t', 'tt'],
 ['tattarrammaddadmttat', 'tattarrattat'],
 ['asymmetr', 'aceb'],
 ['kayakaceb', 'abcedceba'],
 ['kaadmyak', 'madbcdfghraccecarjklmnpqvkkkaykwxyzam'],
 ['elevze', 'xxyrotator'],
 ['xxyz', 'ab'],
 ['ammadadm', 'tattarrattartbcdfghraccecarjklmmnpqvkkaykwxyz'],
 ['ledmmaadamvel', 'level'],
 ['xadmxzyz', 'bcdfghraccecarjklmnpqvkkaykwxyzxyz'],
 ['rotat', 'rotator'],
 ['eelevze', 'lmemmadam'],
 ['xadmxzy', 'xadmxzyz'],
 ['l', 'tattarrattat'],
 ['ab', 'lme'],
 ['tattarrattammadadmat', 'tattarrattat'],
 ['elevzelv', 'elevzelv'],
 ['kayakaceb', 'mmadmmadadmadm'],
 ['tattarrattat', 'abcedeba'],
 ['mdam', 't'],
 ['eteacebbvattarrraattatv', 'eteacebbvattarrradmmaadamattatv'],
 ['racmaeteacebbvattarrraattatvdebair', 'racmadameceaeabcedebair'],
 ['kmmadaaeimk', 'xyz'],
 ['mmaddadm', 'eteacebbvattarrradmmaadamattatv'],
 ['lmme', 'mamadadm'],
 ['asymttical', 'asymttical'],
 ['eelevzelv', 'eelevzelv'],
 ['racmadameceaeir', 'lmemmadam'],
 ['racecr', 'ammadaadm'],
 ['racmadameceaeabtattarrattaasymmetricaltcedebair', 'racmadameceaeir'],
 ['kaadmyak', 'kaadmak'],
 ['mmadam', 'batattarrammaddadmttatb'],
 ['mdam', 'xxyz'],
 ['mmaasymmetrdadkmmadaaeimk', 'mmmadadm'],
 ['kayamamadadmk', 'xyz'],
 ['asytrmmadam', 'adm'],
 ['ammadadm', 'tattarrattartbcdfghraccdecarjklmmnpz'],
 ['mmaadamm', 'mmaadamm'],
 ['xxydmmaaeacebbvdamz', 'xxyz'],
 ['eteacebbvattarrraattatv', 'eteacebbvattarrradmmaadamaelevzettatv'],
 ['racecea', 'racecear'],
 ['kkayk', 'xyracecarz'],
 ['lmem', 'lmemmadam'],
 ['asytrmmadam', 'tattarrammaddadmttat'],
 ['dmmmmaadamam', 'dmmaadam'],
 ['racrecaeeir', 'racrecaeir'],
 ['abcedebaxadmxzyz', 'mmaadam'],
 ['racecarab', ''],
 ['mdam', 'ledmmaadamvel'],
 ['aceracecarabbb', 'acebb'],
 ['acbcdfghjklmnpqvqwxyzeb', 'aceb'],
 ['raccecar', 'raccecar'],
 ['mdam', 'asymttical'],
 ['mmadadm', 'lmemmadam'],
 ['eteacebbvattarrradmmaadamattatv', 'abcedeba'],
 ['ace', 'asymmetr'],
 ['tattarrattartbcdfghraccecarjklmmnpqvkkaykwxyz', 'tattrotrrarrakayakasymmetrttat'],
 ['abceadmdeba', 'ev'],
 ['', 'xxyz'],
 ['kaadmak', 'raccecar'],
 ['ammadalmxxyz', 'abcedceba'],
 ['mmadadm', 'mmaadadm'],
 ['acracecare', 'asymmetr'],
 ['asymmrical', 'lme'],
 ['ammadalmxxyz', 'kayakaceb'],
 ['asymmetrical', 'lmee'],
 ['abctattrtrattatedeba', 'abcedeba'],
 ['kayamkamadadmk', 'xyz'],
 ['abcedebaxxyzxadmxzyz', 'tattarraattat'],
 ['level', 'tattarrattartbcdfghraccecarjklmmnpqvkkaykwxyz'],
 ['lmee', 'lmee'],
 ['asytrmmadam', 'lmxxyz'],
 ['asymmetriabcedebaxxyzxadmxzyzl', ''],
 ['lmee', 'xyz'],
 ['asymtr', 'mdaxadmxzyzm'],
 ['eelevlevelzelv', 'eelevzzelv'],
 ['rrotrator', 'ammmadaadmmdam'],
 ['ledmmaadamvel', 'll'],
 ['acebb', 'kayakattceb'],
 ['lmee', 'eteacebbvattarrradmmaadamattatv'],
 ['abcedaeba', 'tattarrattat'],
 ['lme', 'xxyrotator'],
 ['bcdfghjklmnpqvwxyz', 'lmeeev'],
 ['lmme', 'asymtticaldadm'],
 ['asymdaxadmxzyzmtrmmadam', 'asytrmmadam'],
 ['lmme', 'abcedeba'],
 ['mmadam', 'madam'],
 ['acracecare', 'emadbcdfghraccecarjklmnpqvkkaykwlmmexyzamv'],
 ['racmmaddadmmadameceaeir', 'racmadameceaeir'],
 ['levevl', 'ledmmaadamvel'],
 ['tattrarrattat', 'racecea'],
 ['xxx', 'xxyz'],
 ['tattarrattat', 'abcedaeba'],
 ['teacebbvattarrraattat', 'xyracecarz'],
 ['bcdfghjklmnpqvqwxyz', 'bcdfghjklmnpqvqwabxyz'],
 ['abceadmacebdeba', 'abceadmdeba'],
 ['kkaadmyak', 'madbcdfghraccecarjklmnpqvkaykwxyzam'],
 ['xxyzlmemmadam', 'abccedeba'],
 ['kayakasymmetr', 'a'],
 ['mddmam', 'tattarrattat'],
 ['emadbcdfghraccecarjklmnpqvkkaykwlmmexyzamv', 'acracecare'],
 ['eteacebbvattarrraattabatattarrammaddadmttatbtv', 'eteacebbvattarrradmmaadamattatv'],
 ['abcezadmdeba', 'rotator'],
 ['lmemmadam', 'kayaamadbcdfghraccecarjklmnpqvkkkaykwxyzamk'],
 ['t', 'lmemmadam'],
 ['lme', 'ledmmaadamvel'],
 ['emadbcdfghraccecarjklmnpqvkkaykwlmmexyzamasytrmmadam', 'acracecare'],
 ['racmadameceaeabtattarrattaasymmetricaltcedebair', 'racecea'],
 ['ammadaadm', 'rotator'],
 ['mddam', 'asymtticaxyzl'],
 ['lmme', 'lme'],
 ['asymtdticaldadm', 'asyimtticaldadm'],
 ['asyimtticaldadm', 'asyimtticaldadm'],
 ['lmee', 'ledmmaadamvel'],
 ['mamadadm', 'mmaasymmetrdadkmmadaaeimk'],
 ['asymmetriabcedebaxxyzxadmxzyzl', 'asymmetriabcedebaxxyzxadmxzyzl'],
 ['racecarab', 'racecarab'],
 ['ledmmaadamvel', 'leve'],
 ['rotator', 'rotator'],
 ['rrotrator', 'lme'],
 ['asyimtticaldadm', 'a'],
 ['xxyzlmemmadam', 'rotator'],
 ['ma', 'madam'],
 ['elevze', 'xxyraceceartor'],
 ['bcdfghjklmnpqvqwxyz', 'emamadadmacebbv'],
 ['reteacebbvattarrradmmaadamattatvotrator', 'rotrator'],
 ['amadbcdfghraccecarjklmnpqvkkaykwxyzambcedaeba', 'abcedaeba'],
 ['raceckayakaceb', 'abcedceba'],
 ['mmdam', 'mdam'],
 ['mamadaeacebbv', 'mmaasymmetrdadkmmadaaeimk'],
 ['abcdeba', 'abcedeba'],
 ['adm', 'tattarrammaddadmttat'],
 ['lmem', 'raceckayakaceb'],
 ['tattarrattartbcdfghraccecarjklmmnpqvkkaykwxyz', 'xxyraceceartor'],
 ['madbcdfghracabcdebaadmcecnarjklmnpqvkaykwxyzam',
  'madbcdfghracabcdebaadmbcdfghjklmnpqvwxyzcecarjklmnpqvkaykwxyzam'],
 ['abcdeba', 'racecaeir'],
 ['maeccecardmam', 'acebb'],
 ['kaadmyak', 'eteacebbvattarrradmmaadamattatvkaadmyaceak'],
 ['asymmetr', 'lmxxyz'],
 ['ammadalmxxyz', 'abcedcracmadameceaeabtattarrattaasymmetricaltcedebaira'],
 ['mmaadaabcedcracmadameceaeabtattarrattaasymmetricaltcedebairam', 'mmaadam'],
 ['mddmamyz', 'xyz'],
 ['tattrarrattat', 'xymxxyzz'],
 ['ammadalmxxyz', 'ammadalmxxyz'],
 ['asytrmmadam', 'asytrmmadam'],
 ['madbcdfghraccecarjklmnpqvkkkaykwxyzam', 'y'],
 ['elerotratore', 'tattarrattammadadmat'],
 ['racmadameceaeabtattarrattaasymmetricaltcedebair',
  'racmadameceaeabtattarrattaasymmetricaltcedebair'],
 ['racecar', 'asymmrical'],
 ['lme', 'xadmxzyz'],
 ['asymmmetr', 'asymmetr'],
 ['mmaadaabcedcracmadameceaeabtattarrattaasymmetricaltcedebairam',
  'mmaadaabcedcracmadameceaeabtattarrattaasymmetricaltcedebairasymmetram'],
 ['abctattrtrattatedeba', 'tt'],
 ['bcdfghjklmnpqvqwxyz', 'batattarrammaddadmttatb'],
 ['mddam', 'bcdfghjlmnpqvwxyz'],
 ['racecar', 'rtattarrattaasymmetricaltacecear'],
 ['tattrarrattat', 'racecekayakaceb'],
 ['adm', 'tattarrammaddadmtatat'],
 ['xylmxxyzz', 'lmme'],
 ['ledmmaadamvel', 'racecekayakaceb'],
 ['eelevzzelv', 'rtattarrattaasymmetricaltacecear'],
 ['bcdfghraccecarjklmnpqvkkaykwxyzxyz', 'dmmaadam'],
 ['ammadadm', 'maraceceaardra'],
 ['amadbcdfghraccecarjklmnpqvkkaykwxyzambcedaeba', 'kaadmak'],
 ['eelevlevelzelv', 'racecr'],
 ['mmadmmadadmadm', 'amadbcdfghraccecarjklmnpqvkkaykwxyzambcedaeba'],
 ['ll', 'ev'],
 ['teacebbvattarrraattat', 'elevze'],
 ['rrotrator', 'rrotrator'],
 ['ll', 'vev'],
 ['emamadadmacebbv', 'elelvze'],
 ['kkaadmyak', 'xyz'],
 ['tattarrattaasymmetricalt', 'tattarrattaasymmetricalt'],
 ['lmacebraccecarbe', 'lme'],
 ['mmlme', 'mlme'],
 ['rotrr', 'aa'],
 ['kaayakasymmetr', 'kayakasymmetr'],
 ['xylmxxyzzz', 'xylmxxyzz'],
 ['kkakyk', 'kkayk'],
 ['abcezadmdeba', 'adm'],
 ['ma', 'lmxxyz'],
 ['eteacebbvattarrraattatv', 'eteacebbvattarrmaadamattatv'],
 ['bcdfghjklmnpqvqwxz', 'bcdfghjklmnpqvqwxyz'],
 ['ical', 'asymmettrical'],
 ['kayakattceb', 'acebbb'],
 ['asymtdticaldadm', 'rotat'],
 ['arelerotratoresymmetr', 'asymmetr'],
 ['ev', 'evlmacebraccecarbe'],
 ['tattarrattartbcdfghraccecarjklmmnpqvkkaykwxyz', 'aa'],
 ['abcedeceba', 'abcedceba'],
 ['rotatr', 'rotar'],
 ['mmaddadm', 'abcezadmdeba'],
 ['lmee', 'raceecarab'],
 ['kkaykmddmam', 'eabcedcebav'],
 ['bcdfghraccecarjklmnpaqvkkaykwxyz', 'bcdfghraccecarjklmnpqvkkaykwxyz'],
 ['t', ''],
 ['asymtdticaldadm', 'asymtdtticaldadm'],
 ['lmmlmeme', 'lme'],
 ['rotraatasymmetrr', 'abcedcracmadamece'],
 ['tattkaayakasymmetrarrattat', 'abcedeba'],
 ['kayakasymmetr', 'kayaammadadmk'],
 ['kkaakdmyak', 'bcdfghraccecarjklmnpqvkkaykwxyz'],
 ['abcedebaxxyzxbcdfghraccecarjklmnpqvkkaykwxyzxyzadmxzyz', 'abcedebaxxyzxadmxzyz'],
 ['teacebbvattarrraattat', 'teacebbvattarrraattat'],
 ['eteacebbvattarrraattatv', 'eteacebbvkaadmyakattarrradmmaadamv'],
 ['abdcedeba', 'abcedeba'],
 ['lmeacebe', 'asymmetrical'],
 ['asymmetr', 'asymmetrtattarrattaasymmetricaltacecearriabcedebaxxyzxadmxzyzl'],
 ['kaadmadmyak', 'eteacebbvattarrradmmaadamattatvkaadmyaceak'],
 ['t', 'xxxyz'],
 ['mddmam', 'atattarrattat'],
 ['raacecar', 'racecar'],
 ['abcedceba', 'abcedceba'],
 ['kaadmadmyak', 'asymmetr'],
 ['dmmaaelerotratoreadam', 'dmmaaelerotratoreadam'],
 ['abcedeba', 'rrotratracecarabor'],
 ['raccecar', 'bcdfghraccecarjklmmnpqvkkaykwx'],
 ['mrrotratormaadam', 'lmxxyz'],
 ['raceckayakaceb', 'asymdaxadmxzyzmtrmmadam'],
 ['kayaamadbcdfghraccecarjklmnpqvkkkaykwxyzamk', 'kayaamadbcdfghraccecarjklmnpqvkkkaykwxyzamk'],
 ['elerotratore', 'abcedebaxadmxzyz'],
 ['mmaddadm', 'xyz'],
 ['racecaeir', 'ttemadbcdfghraccecarjklmnpqvkkaykwlmmexyzv'],
 ['tattarraattat', 'tattarraattat'],
 ['aa', 'lmmlmeme'],
 ['racracecrecaeir', 'lmeeev'],
 ['kaadkmyak', 'rotalmeetxyz'],
 ['raceckayakaceb', 'eteacebbvkaadmyakattarrradmmaadamv'],
 ['amadbcdfghraccecarjklmnpqvkkaykwxyzambcedaeba', 'kkaykmddmam'],
 ['z', 'racmadameceaeir'],
 ['madbcdfghraccecarjm', 'kaaadmyak'],
 ['mmlmtattaammadadmrrattate', 'mmlmtattarrattate'],
 ['madbcdfghraccecarjklmasymmetricalnpqvkkaykwxyzam', 'madbcdfghraccecarjklmnpqvkkaykwxyzam'],
 ['maraceceardam', 'mmlme'],
 ['ammdadadm', 'tattarrattartbcdfghraccecarjklmmnpqvkkaykwxyz'],
 ['mddraceceaam', 'asymtticaxyzl'],
 ['dmmaadam', 'mmadam'],
 ['asymdaxadmxzyzmtrmmadam', 'abcezadmdeba'],
 ['kayaameteacebbvattarrmaadamattatvmadadmk', 'kayaammadadmk'],
 ['racecear', 'racece'],
 ['racmadamecaeir', 'bcdfghraccecarjklmmnpqvkkaykwxyz'],
 ['xyz', 'yxyz'],
 ['tattarratttat', 'xymxxyzz'],
 ['maceddam', 'raacecar'],
 ['aacbebbb', 'acebbb'],
 ['mmlmtattaammadadmrrattate', 'lmxxyz'],
 ['t', 'racrecaeeir'],
 ['raacecar', 'ammadalmxxyz'],
 ['tattararattammadadmat', 'elerotratore'],
 ['tattrotrrarrakayakasymmetrttat', 'tattarrammaddadmttat'],
 ['teacebbvattarrraattat', 'taraceckayakacebttarraattat'],
 ['kayak', 'elevelv'],
 ['racmadameceaeir', 'mmaadamm'],
 ['mdm', 'mdm'],
 ['racmmaddadmmadameceaeir', 'abcedceba'],
 ['asytrmlevelmadam', 'adm'],
 ['abcattateba', 'abceadmdtattarraattateba'],
 ['eelevlevelzzeelv', 'eelevlevelzeelv'],
 ['emadbcdfdghracczecarjklmnpqvkkaykwlmmexyzamv', 'acracecare'],
 ['asymmetriabcedebaxxyzxadmxzyzl', 'ev'],
 ['bcdfghjlmnpqvwxyz', 'abcdeba'],
 ['asymmetriabcedebaxxyzxadmxzyzl', 'acracecareev'],
 ['abceadmdebbcdfghjklmnpqvwxyza', 'abceadmdeba'],
 ['emadbcdfghraccecarjklmnpqvkkaykwlmmexyzamasytrmmadam', 'bcdfghjklmnpqvwxyz'],
 ['ammadayz', 'ammadalmxxyz'],
 ['bcdfdqvwxyz', 'bcdfqvwxeccecaryz'],
 ['atattarrattat', 'mmaddadm'],
 ['racmadamecaeir', 'bcdfghraccecarjklmmnpqvkkaytattarrakayakasymmetrttatkwxyz'],
 ['tt', 'racrecaeeir'],
 ['kayakaaceb', 'kayakaaceb'],
 ['rrotrator', 'ma'],
 ['bcdfghfjklmnpqvqwabxyz', 'bcdfghjklmnpqvqwxyz'],
 ['eteacebbvattdmmaadamattatvkaadmyaceak', 'eteacebbvattarrradmmaadamattatvkaadmyaceak'],
 ['kayaracecarameteacebbvattarrmaadamattatvmadadmk', 'kayaammadadmk'],
 ['lmbcdfghraccecakrjklmnpqvkkaykwxyze', 'asymmetrical'],
 ['y', 'aab'],
 ['lmeeev', 'lmeeev'],
 ['abceadmdebaaba', 'ev'],
 ['raabcedebaxxyzxadmxzyzcecaeir', 'racecaeir'],
 ['racracecrecaeir', 'bcdfgasymtticaldadmhjklmnpqvwxyz'],
 ['asymtticaldadm', 'raceccear'],
 ['mmaadam', 'mmaadaam'],
 ['bcdfghraccecakrjklmnpqvkkaykwxyz', 'admxymxxyzz'],
 ['tattarraattat', 'lme'],
 ['abcezadmdeba', 'l'],
 ['mddam', 'mddam'],
 ['bcdfghraccecarjklmnpqvkkaykwxrotatoryz', 'xxyraceceartor'],
 ['tattarrammaddadmtatat', 'dmmaadam'],
 ['maraceceardam', 'maracecekayaracecarameteacebbvattarrmaadamattatvmadadmkaarda'],
 ['pqvkkaykwxyz', 'bcdfghraccecarjklmnpqvkkaykwxyz'],
 ['abcedebaxxyzxadmxzyz', 'tattarraatatat'],
 ['ba', 'mmadadm'],
 ['kaayakasymmetr', ''],
 ['asymmettricammadalmxxyzal', 'abcedebaxadmxzyz'],
 ['reaeir', 'lmemmadam'],
 ['asymdaxadmxzyzmtrmmadam', 'aab'],
 ['racceecar', 'bcdfghracceckwx'],
 ['mdam', 'tattarrattat'],
 ['eteacebbvattarrradmmaadamattatv', 'dabcedeba'],
 ['bcdfghjklmnpqvqwxyz', 'tattarrakayakasymmetrttat'],
 ['asymemexxydmmaaeacebbvdamzr', 'asymmetr'],
 ['raceamadbcdfghraccecarjklmnpqvkkaykwxyzambcedaebayakar', 'rtattarrattaasymmetricaltar'],
 ['', 'xadmxzyz'],
 ['kaadmak', 'kaaadmak'],
 ['xabcattatebayz', 'xyz'],
 ['aracecaraba', 'aa'],
 ['maraceceaardra', 'maraceceaardra'],
 ['mmadim', 'dmmaaeacebbvdam'],
 ['mmadadm', 'amadbcdfghraccecarjklmnpqvkkaykwxyzambcedaeba'],
 ['mmaadaam', 'bcdfghfjklmnpqvqwabxyz'],
 ['bcdfghraccecarjklmnpqvkkaykwxyzxyz', 'dmmmaadam'],
 ['kayamamadadmk', 'kayakaceb'],
 ['racmadamasymmettricaleceaeabtattarrattaasymmetricaltcedebair',
  'racmadamasymmettricaleceaeabtattarrattaasymmetricaltcedebair'],
 ['tattrarrattat', 'racecmaeccecardmam'],
 ['ledmmaadamvebcdfqvwxeccecaryzl', 'xadmxzyz'],
 ['abceadmdebbcdfghjklmnpqhvwxyza', 'abceadmdeba'],
 ['bcdfghfjklmnpqvqwabxyz', 'bcdfghjklmnpqvvqwxyz'],
 ['mmaadaam', 'bcdfghklmnpqvqwabxyz'],
 ['reacecaeir', ''],
 ['acbcdfghjklmnpqvqwxyzeb', 'dmmaadam'],
 ['racecara', 'racecarab'],
 ['lmeeev', 'eelevlevelzeelv'],
 ['lmmemmadam', 'lmemmadam'],
 ['mmle', 'mmlme'],
 ['asymmrical', 'asymmrical'],
 ['kayaameteeacebbvattarrmaadamattatvmadadmk', 'reaeir'],
 ['emamadadmacebbv', 'reaeirmmaddadm'],
 ['asyimtticasymemexxydmmaaeacebbvdamzr', 'asyimtticaldadm'],
 ['admm', 'tattarrammaddadmttat'],
 ['tattarrattartbcdfghraccekayakattcebcarjklmmnpqvkkaykwxyz',
  'tattarrattartbcdfghraccecarjklmmnpqvkkaykwxyz'],
 ['asymmrical', 'rtattarrattaasymmetricaltacemaceddamcear'],
 ['kyak', 'llme'],
 ['mdam', 'll'],
 ['lmemmamadam', 'lmemmadam'],
 ['abcedebaxxyzxadmxzyz', 'tattarraatata'],
 ['abceadmdtattarraattateba', 'asymmrical'],
 ['mrotararaceceardam', 'maraceceardam'],
 ['asytrmmadam', 'atattarrattat'],
 ['racceecar', 'racecear'],
 ['ammadamlmxz', 'ammadalmxz'],
 ['tattarraattat', 'lm'],
 ['asymtdticaldadm', 'kmmadaaeimmk'],
 ['asymdaxadmxzyzmtrmmadaeteacebbvattdmmaadamattatvkaadmyaceak', 'asymdaxadmxzyzmtrmmadam'],
 ['elevzvelv', 'elevzvelv'],
 ['racmadamecaeir', 'racmadamecaeir'],
 ['lmme', 'asymttticaldadm'],
 ['abcedebaxadmlmeacebeyzxadmxzyz', 'abcedebaxxyzxadmxzyz'],
 ['el', 'elevzelv'],
 ['xxyrotator', 'xxyrotator'],
 ['abcedeba', 'akaaadmyakceb'],
 ['racmmaddadmmadameceaeirtattarraattat', 'teacebbvattarrraattat'],
 ['asymttticaldadm', 'racrecaeir'],
 ['asymtdtticaldadm', 'asymtdtticaldadm'],
 ['lme', 'abcedcracmadamece'],
 ['abcedebaxxyzxbcdfghraccecarjklmnpqvkkaykwxyzxyzadmxzyz',
  'abcedebaxxyzxbbcdfghraccecarjklmnpqvkkaykwxyzxyzadmxzyz'],
 ['mdamyz', 'abcedeba'],
 ['axymxxyzzsymdaxadmxzyzmtrmmadam', 'asymdaxadmxzymzmtrmmadam'],
 ['tearcebbvattarrraattat', 'teacebbvattarrraattat'],
 ['abcedexbaxxyzxadmxzyz', 'tattarasymtticaldadmata'],
 ['asymmrical', 'mmlmtattaammadadmrrattate'],
 ['mdamm', 'mdam'],
 ['ammdadadm', 'tattarrattartbcdqvkkaykwxyz'],
 ['rrokaayakasymmetrtor', 'aeai'],
 ['abcezadmdeba', 'abcezadmdeba'],
 ['asymmettrical', 'mmaadam'],
 ['mledmmaadamvebcdfqvwxeccecaryzleardam', 'mledmmaadamvebcdfqvwxeccecaryzleardam'],
 ['kkaykmddmam', 'rotrator'],
 ['bcdfghjklmnpqvqwxasymmricalyz', 'eacebbv'],
 ['racceecar', 'bcdfghrakcceckwx'],
 ['mledmmaadamvebcdfqvwxeccecaryzleardam',
  'raceamadbcdfghraccecarjklmnpqvkkaykwxyzambcedaebayakar'],
 ['kayakackaayakasymmetreb', 'abcedceba'],
 ['reaeirmmaddadm', 'reaeirmmaddadm'],
 ['tattarrakayakasymmetrttat', 'tattarrakayakasymmetrttat'],
 ['elevlv', 'elevlv'],
 ['tattarraaattat', 'acracecareev'],
 ['raceecarab', 'raceecarab'],
 ['xadmxzyz', 'kaaadmyak'],
 ['abcdebea', 'madbcdfghraccecarjklmnpqvkaykwxyzam'],
 ['racceecar', 'asymmetr'],
 ['asymttticttaldadm', 'asymttticttaldadm'],
 ['abc', ''],
 ['abc', 'abc'],
 ['aaaaaaaaaa', 'b'],
 ['abcde', 'fghij'],
 ['abcb', 'b'],
 ['abcdcba', 'ac'],
 ['aasymmetrical', 'asymmetrical'],
 ['racecar', 'aa'],
 ['madaam', 'ab'],
 ['asymmetrical', 'asymmetical'],
 ['bcdfghjklmnpqvwxyz', 'bcdfghjklmnpqvwxyz'],
 ['asymmetical', 'asymmetrical'],
 ['racecar', 'eaei'],
 ['asymmeetrical', 'asymmetical'],
 ['aasymmetrical', 'lasymmetrical'],
 ['asymrical', 'asymmetical'],
 ['abcedeba', 'xyz'],
 ['ba', 'xyz'],
 ['aasymmetacebcal', 'lasymmetrical'],
 ['aei', 'aei'],
 ['level', 'level'],
 ['asymriical', 'asymrical'],
 ['aasyammetrical', 'aasyammetrical'],
 ['tattarrattat', 'asymriical'],
 ['eaei', 'aasyamcal'],
 ['aei', 'aasymmetacebcal'],
 ['a', 'bcdfghjklmnpqvwxyz'],
 ['madaamasymmetical', 'ab'],
 ['basymmetrbicala', 'ba'],
 ['abcedeba', 'aceeb'],
 ['tricaasymmeticall', 'asymmetrical'],
 ['z', 'or'],
 ['tricaatsymmeticall', 'asymmetrical'],
 ['xyyz', 'xyz'],
 ['abcedeba', 'xy'],
 ['mamdam', 'abracecar'],
 ['level', 'tattarrattatev'],
 ['aceb', 'z'],
 ['mamadam', 'abracecar'],
 ['tricaatsymmeteicall', 'tricaatsymmeticall'],
 ['aei', 'tatxyyzatev'],
 ['asymmeetricalkayak', 'xyz'],
 ['bcdfghjklwxyz', 'ab'],
 ['mamadaam', 'abracecar'],
 ['mamad', 'abracaecar'],
 ['aasymmetrical', 'mamadam'],
 ['asymmeetrtattarrattaticalkayak', 'asymmeetricalkayak'],
 ['ba', 'level'],
 ['tatxyyzatev', 'xyz'],
 ['aseaeiymrical', 'madaamasymmetical'],
 ['xlmeyz', 'xyz'],
 ['abcedebaba', 'xy'],
 ['abracaecar', 'abracaecmamadaamar'],
 ['xyz', 'xyxz'],
 ['asyormmeetricalkayak', 'level'],
 ['xbcdfghjklmnpqvwxyzz', 'xbcdfghjklmnpqvwxyzz'],
 ['ev', 'tricaatsymmeteicall'],
 ['asymriical', 'level'],
 ['ror', 'level'],
 ['bcdfghjklwxyz', 'ba'],
 ['madaamasymmetical', 'xlmeyz'],
 ['aasymmetrical', 'tricaatsymmeticall'],
 ['asymmriical', 'asymriical'],
 ['t', 'aa'],
 ['tattarrattat', 'tattarrattat'],
 ['abrmamadamacecar', 'abracecar'],
 ['abmrmamadamacecar', 'abracecar'],
 ['abcedasymmriicaleba', 'asymmeetricalkayak'],
 ['basymmetrbicala', 'basymmetrbicala'],
 ['asymriical', 'asymriical'],
 ['aeai', 'aeei'],
 ['aasymmetrical', 'aracecar'],
 ['level', 'leevel'],
 ['mamadaaam', 'abracecar'],
 ['xyxz', 'asyormmeetricalkayak'],
 ['abracecar', 'mamadam'],
 ['aasymmetrical', 'aasymmetrical'],
 ['abasymriical', 'mabmrmamadamacecaradam'],
 ['arxyzacecacr', 'arxyzacecar'],
 ['aasymmetrical', 'madaam'],
 ['asymmeetricalkayark', 'asymmeetricalkayak'],
 ['abracaecar', 'mamad'],
 ['abmrmamadamacecar', 'ab'],
 ['kayak', 'kayak'],
 ['abracecar', 'abracecar'],
 ['xyxz', 'xyz'],
 ['asymtmetrical', 'caceeb'],
 ['caceeb', 'bcdfghjklmnpqvwxyz'],
 ['aei', 'aasymmetacebcaal'],
 ['abracecar', 'abrmamadamacecar'],
 ['asymmetical', 'asytrical'],
 ['bcdfghjklmnpqvwxyfz', 'bcdfghjklmnpqvwxyz'],
 ['aeai', 'aasymmetrical'],
 ['mamadaam', 'xlmeyz'],
 ['asyormmeetricalkayak', 'aasymmetacebcal'],
 ['asymmeetrical', 'mabmrmamadamacecaradam'],
 ['aasymmetacebcaal', 'abracecar'],
 ['arxyzacecacrxy', 'arxyzacecacr'],
 ['mabmrmamadamacecaradam', 'xyz'],
 ['xy', 'xy'],
 ['level', 'ltricaasymmeticalleevel'],
 ['tattarrattat', 'level'],
 ['aei', 'aasymmaeaietacebcaal'],
 ['tatxyyzatev', 'aasyamcal'],
 ['z', 'z'],
 ['rmamadamacecar', 'abracecar'],
 ['lme', 'HM'],
 ['caceeb', 't'],
 ['abcedeba', 'xtattarrattat'],
 ['abcedeba', 'acasymriicaleeb'],
 ['madaamasymmetical', 'xllmeyz'],
 ['caceeb', 'caceeb'],
 ['arxyzacecacr', 'arxyzacecaeaiar'],
 ['eaei', ''],
 ['xtyz', 'xyxz'],
 ['tricaasymmeticalacasymriicaleebl', 'xyz'],
 ['asytrical', 'ab'],
 ['aeei', 'kayak'],
 ['ab', 'madaamasymmetical'],
 ['asymyriyical', 'asymriyical'],
 ['xyabcedebabaz', 'xyabcedebabaz'],
 ['rotbcdfghjklmnpqvwxyzator', 'rotator'],
 ['asymtmetrical', 'asymtmetrical'],
 ['rmamadamacecaraeei', 'aaei'],
 ['arxyzacecacrxy', 'arxyzaccecaacr'],
 ['mabmrmamadamacecaraadam', 'xyz'],
 ['madaamasiymmetical', 'ab'],
 ['aasymmaaasyammeatricaleaietacebcaal', 'aasymmaaasyammeatricaleaietacebcaal'],
 ['tricaasymmeticall', 'asymmetrotbcdfghjklmnpqvwxyzatorrical'],
 ['aasyamcal', 'aasyamcal'],
 ['aasymmetmrical', 'aasymmetrical'],
 ['arxyzacecacr', 'arxyzacecacr'],
 ['aseaeiymrica', 'madaamasyaseaeiymricalmmetical'],
 ['aasymmaeaietacebcaal', 'aaesymmaeaeietacebcaal'],
 ['aasymmetrical', 'madmaam'],
 ['bcdfghjklmnpqvwxypz', 'bcdfghjklmnpqvwxyz'],
 ['z', 'abracecar'],
 ['aseaeiymrical', 'aseaeiymrical'],
 ['aasymmetacebcal', 'xyz'],
 ['level', 'leel'],
 ['asymriyical', 'eaei'],
 ['tricaasymmeticalacasymriicaaleebl', 'xyz'],
 ['tattarrattat', 'aasymmetrical'],
 ['asymmeetrical', 'mabmrmamadamacecaram'],
 ['level', 'arxyzaccecaacrleevel'],
 ['aammetrical', 'aracecar'],
 ['madaamasyaseaeiymricalmmetical', 'tattarrattat'],
 ['mamad', 'xylmmeyz'],
 ['aammetrical', 'aacecar'],
 ['aa', 'z'],
 ['xtyz', 'xtyz'],
 ['madaamasymmetical', 'asytrical'],
 ['madaam', 'madaam'],
 ['bcdfghjklmnpqvwxypz', 'asytrical'],
 ['marxyzaccecaacmrmadamabmrmamadamacecaram', 'mabmrmamadamacecaram'],
 ['madaamasyasceaeiymricalmmetical', 'madaamasyaseaeiymricalmmetical'],
 ['xyz', 'asymmeetrical'],
 ['zz', 'abracecar'],
 ['asyaasymmetacebcalmmetrical', 'rotato'],
 ['xtyz', 'xtymadmaamz'],
 ['aeiaasymmetacebcaal', 'aei'],
 ['rmamadamacecaraeei', 'mabmrmamadamacecaraadam'],
 ['lelvel', 'level'],
 ['caceeb', 'aasyamcal'],
 ['aeiaasymmetacebcaal', 'madam'],
 ['asymmeetricalkayark', 'asymmeetricalkayark'],
 ['abceedeba', 'abcedeba'],
 ['abceedeba', 'abcedaeaia'],
 ['arxyzcacecacrxy', 'arxyzacecacrxy'],
 ['iaei', 'iaei'],
 ['arxyzacecacrxy', 'madam'],
 ['asymmriical', 'ev'],
 ['bcdfghjklwxyz', 'bcdfghjklwxyz'],
 ['tricaasymmeticalacasymriicaleebl', 'madmaam'],
 ['iaeiasyaasymmetacebcalmmetrical', 'asymmetrotbcdfghjklmnpqvwxyzatorrical'],
 ['xbcdfghjklmnpqvwxyzzaa', 'aa'],
 ['asymmeetrical', 'amadaamasyaseaeiymricalmmeticalbcedeba'],
 ['asymmetrotbcdfghjklmnpqvwxyzatorrical', 'madaam'],
 ['aaor', 'z'],
 ['XtMIzX', 'tMIzX'],
 ['rotator', 'ba'],
 ['asymrical', 'abcedebaasymmetical'],
 ['aasymmetaycbasytricalebcaal', 'aasymmetaycasytricalebcaal'],
 ['asymmeetrical', 'asymmeetrical'],
 ['leel', 'leel'],
 ['mabmrmamadamacm', 'xyz'],
 ['tatxyyzatev', 't'],
 ['arxyzacecar', 'xyz'],
 ['madaamasyasceaeiymricalmmetical',
  'madaamasyaseaeiymricalamadaamasyaseaeiymricalmmeticalbcedebammetical'],
 ['madaam', 'madaamasyaseaeiymricalmmetical'],
 ['bcdfcghjklwxaacecatryz', 'baba'],
 ['tatxyyzatev', 'xyabrmamadamacecarz'],
 ['asytricalasytrical', 'asytricalasytrical'],
 ['aaor', 'aaor'],
 ['asymmriical', 'abracecar'],
 ['abracaecar', 'abracaecmamadaaasymmaeaietaceabcaalamar'],
 ['ambmrmamadamcar', 'ab'],
 ['aseaeiymrical', 'aseaeriymrical'],
 ['bcdfghjkllwxyz', 'ab'],
 ['abceedeba', 'abceedeba'],
 ['asymmeetricalkayak', 'abracecar'],
 ['aasymmetacebcaal', 'aracbecar'],
 ['mamadaam', 'mamadaam'],
 ['mamadaaamabceedeba', 'abcedaeaia'],
 ['rotbcdfghjklmnplqvwxyzator', 'rotbcdfghjklmnpqvwxyzator'],
 ['tricaaasymmeetricalkayarksymmeticall', 'tricaatsymmeteicall'],
 ['ba', 'bcdfghjklwxyz'],
 ['asymmetrotbcdfghjklmnpqvwxyzatorrical', 'asymmetrotbcdfghjklmnpqvwxyzatorrical'],
 ['ambmrmamadamcarXtMIzX', 'XtMIzX'],
 ['abraccecar', 'abracecar'],
 ['bcdpfghjklmnpqvwxypz', 'bcdfghjklmnpqvwxypz'],
 ['xylmeyyz', 'xylmeyz'],
 ['level', 'leasymricalel'],
 ['asymrical', 'asymrical'],
 ['abceedeba', 'lelvel'],
 ['madaamasyaseaeiymricalmmetical', 'tatatarrattat'],
 ['ev', 'asymmetrical'],
 ['rmamadamacecaraeei', 'aei'],
 ['xtyaammetricalz', 'asymmetical'],
 ['mamada', 'abracecar'],
 ['ba', 'basymmetrbicala'],
 ['mabmrmamadamacm', 'xy'],
 ['arxyzacecarxy', 'madam'],
 ['z', 'zz'],
 ['asymmetical', 'yasymmetical'],
 ['xyz', 'xabracecartatatarrattatyz'],
 ['taaasymmetmricalrrattat', 'level'],
 ['xtyaammetrz', 'xtyaammetricalz'],
 ['zz', 'or'],
 ['ev', 'evabraccecar'],
 ['aasyammetrical', 'aseaeiymrical'],
 ['aaeeisymrical', 'Jlxtasymmecal'],
 ['xbcdfghjklmabmrmamadamacecarnpqvwxyzz', 'xbcdfghjklmnpqvwxyzz'],
 ['kaayak', 'kaayak'],
 ['tricaasymmeticaasymmaaasyammeatricmadaamasyasceaeiymricalmmeticalleaietacebcaall', 'xyz'],
 ['aei', 'arxyzacecacrxy'],
 ['aasymmetacebcaal', 'bcdfghjebaz'],
 ['maamad', 'xylmmeyz'],
 ['rotattor', 'rotator'],
 ['madaamasymmetical', 'ror'],
 ['aasymmaetrical', 'lasymmetrical'],
 ['abracaecmamadaamaer', 'abracaecmamadaamar'],
 ['asymmetical', 'madaamasiymmeticalasymmetical'],
 ['aceb', 'xy'],
 ['racecar', 'aaa'],
 ['asymmasymmetrotbcydfghjklmnpqvwxyzatorricaletrical',
  'asymmasymmetrotbcdfghjklmnpqvwxyzatorricaletrical'],
 ['maadaammadamasymmetical', 'maadaamasymmetical'],
 ['racecaar', 'eaei'],
 ['asyormmeetricalkayak', 'asyormmeetricalkayak'],
 ['mabmrmamadamacm', 'xtricaasymmeticall'],
 ['tricaasymmeeticalacasymriicaleebl', 'madmaam'],
 ['aammetirical', 'aracecar'],
 ['ba', 'bcdfghjklwxy'],
 ['asymmeetrical', 'mabmrmamadamacecaradamasymmeetrtattarrattaticalkayak'],
 ['madaammammadaambcdfghjklmnpqvwxyfzasymmetical', 'madaammammadaamasymmetical'],
 ['z', 'oor'],
 ['asyaasymmaeeietacebcalmmetrical', 'asyaasymmetacebcmalmmetrical'],
 ['amadaamatattarrattatevsyaseaeiymricalmmeticalbcedeba', 'tricaatsymmeticall'],
 ['bcdfghjklwabracaecmamadaaasymmaeaietaceabcaalamarxyz', 'bcdfghjklwxyz'],
 ['aatricaasymmeticaasymmaaasyammeatricmadaamasyasceaeiymricalmmeticalleaietacebcaallsymmetacebcal',
  'xyz'],
 ['asasymmeetricalytrical', 'asyormmeetricalkayak'],
 ['eaeei', 'aasyamcal'],
 ['bcdpfghjklmnpqvwxypz', 'madaamasyaseaeiymricalmmetical'],
 ['aasymmaetrical', 'ylasymmetrical'],
 ['asymriyical', 'abracaecar'],
 ['bcdpfghjklmnpqvwxypz', 'madaamasyaseaeiymricalammetical'],
 ['aasymmaetrical', 'aasymmaetrical'],
 ['mabmrmamadamacm', 'mabmrmamadamacm'],
 ['asykormmeetricalkayak', 'madmaam'],
 ['eaei', 'mabmrmamadamacecaJlxtadam'],
 ['xyxz', 'xyxz'],
 ['madam', 'aabracaecarb'],
 ['aseaeiymrical', 'madaamasymetical'],
 ['bba', 'ba'],
 ['basymmetrbmaadaamasymmeticalicala', 'aba'],
 ['tatxyyzatev', 'tatxyyzatev'],
 ['bcdfghjklmnpkqvwxypvz', 'bcdfghjklmnpqvwxyz'],
 ['aaei', 'aaei'],
 ['mamad', 'mamad'],
 ['madaamasyasceaeiymricalmmetical', 'asymmetrical'],
 ['yasymmetal', 'aracecar'],
 ['bba', 'aracecar'],
 ['abracaecmamadaaasymmaeaietaceabcaalam', 'abracaecmamadaaasymmaeaietaceabcaalamar'],
 ['tatxyyzzatev', 'tatxyyzatev'],
 ['rotator', 'abracecar'],
 ['aseasymmeticalaeasymmriicalmrical', 'aseaemrical'],
 ['tricasymmeticall', 'tricaatsymmeticall'],
 ['aaeeisymrical', 'bcdfghjklmnpqvwxyz'],
 ['bcdfghjklmnpqvwxyz', 'or'],
 ['tattarttat', 'aasymmetrical'],
 ['yasymmetical', 'tricaaasymmeetricalkayarksymmeticall'],
 ['asymmasymmetrotbcdfghjklmnpqvwxyzatorricaletrical', 'kayak'],
 ['mamdam', 'oylasymmetricalasykormmeetricalkayak'],
 ['aassymmetrical', 'aracecar'],
 ['asymmeetrtattarrattaticalkayak', 'aei'],
 ['aeiasymriical', 'asymriical'],
 ['asyormmeettricaaasymmeetricalkayarksymmeticallricalkayak', 'aasymmetacebcal'],
 ['asyormmalkayak', 'asyormmeetricalkayak'],
 ['lasymmetrical', 'lasymmetrical'],
 ['tricaasymmeticalacasymriicaleebl', 'tricaasymmeticalacasymriicaleebl'],
 ['level', 'ltricaasymmeticel'],
 ['xtattarrattleasymricalelt', 'xtattarrattleasymricalelt'],
 ['xtattarrattat', 'z'],
 ['abracecar', 'abrmabcdfghjebazcecar'],
 ['asymmetricalz', 'oor'],
 ['acaeb', 'xyy'],
 ['abcedasym', 'abcedasymmra'],
 ['xxymlmmeyyzy', 'xxylmeyzy'],
 ['lasymmetrical', 'aasymmetacebcal'],
 ['zz', 'asymical'],
 ['tatxyyzatev', 'aeai'],
 ['iaeiasyaasymmetacebcalmmetrical', 'iaeiasyaasymmetacebcalmmetrical'],
 ['abmrmamadamacecar', 'bcdfghjklwxyz'],
 ['alsymriyical', 'asymriyical'],
 ['xtyz', 'xty'],
 ['or', 'or'],
 ['z', 'abracecear'],
 ['asymrical', 'tricaasymmeticalacasymriicaleebl'],
 ['aasymmetrical', 'aasymmetmrical'],
 ['easymmeetricalkayark', 'asymmeetricalkayarkev'],
 ['asymmasymmetrotbcdfghjklmpqvwxyzatorricaletrical',
  'asymmasymmetrotbcydfghjklmnpqvwxyzatorricaletrical'],
 ['z', 'amadaamasyaseaeiymricalmmeticalbcedeba'],
 ['z', 'madaamasyaseaeiymricalamadaamasyaseaeiymricalmmeticalbcedebammetical'],
 ['rotator', 'asyormmeettricaaasymmeetricalkayarksymmeticallricalkayak'],
 ['xyxz', 'xlmeyz'],
 ['leracecarveracecarl', 'leasymricalel'],
 ['aasymmetacebcaal', 'ev'],
 ['abaxylmyzmeyz', 'xylmyzmeyz'],
 ['ylasymmetrical', 'ylasymmetrical'],
 ['arrxyzacecacr', 'arxyzacecaeaiar'],
 ['asymmriical', 'xxylmeyzy'],
 ['abcaceeb', 'bab'],
 ['caaceeb', 'arxyzacecaeaiar'],
 ['asasymmeetricalytrical', 'amadaamatattarrattatevsyaseaeiymricalmmeticalbcedeba'],
 ['bcdfghjkllwxyz', 'xylmeyz'],
 ['rotatorxylmmeyz', 'z'],
 ['bab', 'rmamadamacrotbcdfghjklmnpqvwxyzatorecaraeei'],
 ['racecaar', 'cracecaar'],
 ['cecaraadam', 'xyz'],
 ['lelel', 'madaamasymetical'],
 ['madaamasymmetical', 'bcdfghjklmnpqvwxyz'],
 ['ev', 'aasymmetacebcaal'],
 ['asymmetmadaamrxyxzical', 'aasymmetaycbasytricalebcaal'],
 ['lelvel', 'abceedeba'],
 ['yasymmetal', 'aracecaaaar'],
 ['aseaeiymrica', 'aseaeiymrica'],
 ['xyabrmamadamacecarz', 'aracecar'],
 ['aeiasymriical', 'asymamadaamatattarrattatevsyaseaeiymricalmmeticalbcedebaiical'],
 ['aaei', 'cecaraadam'],
 ['basymmetrbmaadaamasymmeticalicala', 'abba'],
 ['asymmetical', 'asymrical'],
 ['madaamasyaseaeiymrtattarrattatevicalammetical', 'aacecar'],
 ['aei', 'ev'],
 ['madaamasymmetical', 'leevel'],
 ['iasymmetical', 'asymmetrical'],
 ['abracecear', 'madmaam'],
 ['xtyaammetrz', 'xyzaaei'],
 ['XtMIzX', 'tMaceebIzX'],
 ['xxymlmmeyyzy', 'asytricalabcedasym'],
 ['ltricaasymmeticel', 'ltricaasymmeticel'],
 ['abcedasym', 'abmadaamasyasceaeiymricalmmeticalcedasymmra'],
 ['rmamadamacecar', 'abcedasymmriicaleba'],
 ['bcdfghjklmnpqvwxlyz', 'abcedasym'],
 ['mamdaam', 'madaam'],
 ['asasymmeetriasymmeticalicalytrical', 'asyormmeetricalkayak'],
 ['asymmeetrical', 'asymmeetricasl'],
 ['xbcdfghjklmrmamadamacecarnpqvwxyzz', 'xbcdfghjklmnpqvwxyzz'],
 ['madaam', 'mbcdfghjebazaam'],
 ['aasymmaetrical', 'ylmasymmetrical'],
 ['abcedeba', 'xabracecartatatarrattatyz'],
 ['tricaasymmeeticalacasymriicaleebl', 'aaor'],
 ['bcdfghjebaz', 'bcdfghjebaz'],
 ['arxyzazcecacr', 'arxyzacecar'],
 ['level', 'eleevel'],
 ['tricaasymmeticalacasymriicaleebl', 'tricaasymmeticalacasymriicaebl'],
 ['aaeasyormmeettricaaasymmeetricalkayarksymmeticallricalkayaki', 'aaei'],
 ['aasymmaetrical', 'ylacal'],
 ['arxyzazcecacr', 'ylmasymmettricaasymmeticalacasymriicaleeblrical'],
 ['xyabcedebabaz', 'kayak'],
 ['maam', 'xylmmeyz'],
 ['abba', 'abba'],
 ['amamada', 'lmxbcdfghjklmnpqvwxyzzaa'],
 ['asymmasymmetrotbcdfghjklmpqvwxyzatorricaletricalam', 'am'],
 ['arxyzacecacr', 'xllmeyz'],
 ['mamabmrmamadamacecaradambmrmamadamacm', 'mabmrmamadamacm'],
 ['asasymmeetricalytrical', 'yasymmetical'],
 ['XtMIzX', 'xllmeyz'],
 ['madaamasyasearoreiymricalmmetical', 'tatatarlasymyriyicaltricaasymmeticeltat'],
 ['cacebasymmetrbicalaeb', 'cacebasymmetrbicalaeb']]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-'
    b'rl~J+dr0lBHQibdSsmdJ9dB01Cw)*Bfa9zta3{V5p&rtlIB<$0DykvW758ak(9tRS_94+|3Pu>d|umh3fzFU;g9&_?LhE7yajd{`'
    b'-IbxBvQo|F2=W{QJNCkDN}PXY?99hnnJ9BU)^+?|E&UYuS4_ollhH_uLS}E^UvR`c3iLzyH7g{=fe9-'
    b'~Pv5JCE4LUBS*BVU3$kvL5-'
    b'm_g%)i>(;gU@^WfTcc$RME<btCx#=H|@i=|*q0;lHep;B<Q`~d56Y`3?SxYtd;3KaSPgtq87}FgijXZk($75Ps&0=o*#N0>SwR#-'
    b'kSgp2GNjt=`eCJq=Z?@t+_sx)Uzy12E;~$U7Y21^y$53i*eTFjvU&}k@nrA;b##YLnc~2kPmR`5TkmIQF_Wtvj)4a6Q$}K0RF-'
    b'~2bX&j*xKc(H&$5^|~l*&lU#*R1TyW8+uR<GIKeGH42&i37tkK1x)kj$UWm3FK(M@uWl-p{h_Gdb%M+C6*BQ1`T3-'
    b'klpuwa&qk)MUBd9ZK}lBTu&C>lUx4tuif~!ejUKd9zQ3T<0Ck#y=jDGDd<0$DH=uDU{o8F4?jyXQms68PnAp_SAL>{Q0(4Yl!^J+'
    b'4J2&<yrBDb?_KB*K3cs-A`(M^YSFuNO4VG^<GAQ!ahCT-ER#u?)&3Y7Tx;d^*z~Hz7}i5Cx(@PC)CXn)i9#BQT8@Z9?qGiTE{fP4'
    b'gYvdIIH$CnVuBm3bRJr%{QhV(^{jf5U$6SX1jGPT*7<61xKH}(<%Mkl{$MLo8A(CJ-+?M6Jt5H4ZFQqc4KnWWFdR(mh-'
    b'98)4F5LHmrsEGbrZ$EWibHu<n41+sVDuS?<0oTj1-3XKql!$C(W$-=mx0&3wN*sF&>K1|SnZ%Z)K(KX>f2&q%4Kd1sEZV=b{=-'
    b'@#)UC(e1IonBAqA=V$)oV-d-({Ecx=$i7#IKgRP1^>sigRb$En3#~Zz=vB#WCCrhQfhp6P^-'
    b'pdc%ZkrLcbU~=Gz3j?cP;W<253SUJKspo^uJro)v}v^&I<74}a$|HEgD*S0Fv4;<&O`kbSS4YawQZyRo$r7zBm^aQDHZ7-'
    b'S}<?eP=tR%6=wser%<^)m1jeV%#R?aUApT@@)hz7G%p@;2*Wj&1J{%zmtxXY($h?2~#4bG1>Avlv(gVdZwPXcaubtJbmA;ykcnm<'
    b'1<h&flFIA!r?}V7CimcDK?)WvWVqdq5FV!3Xq?I~F(waju2n#cGKSJo(B6A7kzgT-Sx+<{37A0YoKV6K9AQl$+-'
    b'OKDoBW(p?a3Fc@GEIJ@WFw}JFvG46X}Q{zI%<S?EM#+Ts)vFx^D2P7_zhvV|G?PJ0#%oxX4PVrmjHx~}n38@Xbxd4$#v~?#mv3iw'
    b'oS>_zUY6o~>WNq=on-EUWoUGjs+lsyI${XRKGxM-'
    b'k0Cdocx0sfLO*qvq#5*5gaGo*l)RNon2cqyY7PFT5D9m4em6&owwxJC02Vx1dq;(?VBrNY34g!Gaxo<U4!ec)BH!t{W;qC%Vki3&'
    b'ZGpO`w2Or|W)mLnlur#ok$mB!Tc?OOh3L*waM5n}eiHY;x=kBpV?uL!=^|R)Y5ij8W@&X6N1_d0Lx4}<G+P59Sjh!(+k8u+XDSXr'
    b'5st~9=N|0@XR3j6^^Nk^-'
    b'ECSjqfp=iT5yskhqw|$3<+o(GZY>E*Pix@4Si5yX4Q>r*+IS}qgb3$~p3Ie?$(*eYEaJBBz70z2j9hj`e~o?zy7eIIh;lgQDRcYc'
    b'!DEdBWwyiQ^Djz4+6}mR*&h$@i-'
    b'^bv@<4H*6YeEm)=@{9xgq1HRo^?8(L3uorK9r*toIx_{YVdVd&XchQjx)x=7?xvg~gLLvKr35TSqJhcZV{9R1HLlkPY<3N?%E@f8'
    b'}HNTK6OSZ4uYYGT~%6W+pHtQMc9+3LT@a?exaKNfq9Wb+8gSeC41zVY4)(A7(X%IcAJZ!6RC%z3)C^7`rgG(8?^fZ^pv0(ygrvgz'
    b'(GzHzB11b|Nedi4IpoT&`UP0>um;#eoX{qiW9ykE}M)_D&qXHfCAx2H!eEL-'
    b'8Mg0Qtrn)mk6iMJD&`cb;3}86bOL2HVtj*;yX%#cy}}!D3ikFCE`Iz&uEp!-'
    b'6>@vXlM~P(gGCbO!R=!Xk==!Lu7A5zY$v`GKvoP<Im~DFMlnyRl#cp;i=N2DCB2c;k}y+nEbdTh_fqJ<v6!U+tQ(dDmvl92H1Lq1'
    b'k}QhYADeVckIly)B?>+92!}Ood<D0U=v^PT{`1(>72}ev>vti+h}LY+hl+);v|7SJ0icw`B_si_PEG{la&#lVRtx({@WZDGtf-'
    b'K=eR12uM;6`jADmc0#{*6zG{S9S_9Uu%|7X-jjW&EUO`6tT&v~nfk$m1Xk;I!Vx_D;tY|X86f-'
    b'N8LBol!qw*T+IxL~VgnQ{;nWLezd+Yjh`BzswLFQ!Ddga(+<*kXE2VV~I$P77;~&kC`r3Yx+<D>tIH|`3(5$4;A4g*%FE|0#6N-'
    b'&>9QaZ}nO%JBwjb9VLM+=53j%PyrJD`3MsBI(&6@IWX4zIjmp)^#vAi#=6tUyO*H2_H{={KGd`jEJu)^3AV0)+Ys5Rh&3$~K7FJ6'
    b'ZUjxlIw(UC$c4u2Vooo^G<CPBe?Na_t)98QRNmRuYxE;e$gHW1c<!3R|I%A?7(KHEUxYGqLEYN4S@CnEGP*19f>g)&b7IdnLT+E8'
    b'LZyCiz;1SD8|`PIbaCGH2f%Yv;HM<ySrYG$Uxh2&w%X||A-{xt@DZ-)HV)=&`uAOAr`{muRU^OXV~vQFqglCS{b$DvagX%Ls!B5-'
    b'eHLWFQwVq#kxKAL-'
    b'81xR0S2N*~TF{Q$LP$%nJ!gFpp#DQHBD8v8r<7Mp|2JB^Col0RrE2p_vf0t1(oVbVfP=HQE=nduGfvLte7nF%t)3bOOZ0hm}os0l'
    b'19uc?Wv+ewnf?>#g*B0_&uHlCSU;y6lR(KRAbVH=W*8oz0^YG~CGhF^)-'
    b'23sVDW`%{jFqkqJ~ngWxfVF_VR1GTf;h$i7qlYjRD?(qVf%RBi0kFx>qUEp%dL)OsjzGy1X_e;0}4F*?gY5jM1spqI&|t-'
    b'YUhn%(KG%z<~p`pEETi~rz696?ZFVFHcu)*QD+&;<zd&bcAk7#FdOY4Wqu&NVF0}CnWwIupuru++OekAP|g+{=o!F$)qzNxC5>44'
    b'#}Oumar`GvS(Og%bsgk&IATQ&4D125K^UljBQ^_o#g^vu5*WXs*wItr!ux-?Uzt6`_?*yS?nmUo_*K-'
    b'2Hi8cBK_o$coAag`PAeAVm{<=Fd{=tBba;ZyL?J)`8;=M(!EP|Ne#9n3VIoM=b-'
    b'0WI=`HF6FCia@y|D$WKWBHmw*&C;V*fD7UW$}y5;6_P+$K_WCHVxZl~|F(bNJ625+UyA)I%}}kLndpu!+%y8SO1&s#p{BE#Z&w7z'
    b'ATYsUv_YthaT7et-<Uy}5uWD--qI;YS%-'
    b'f90ZRFt{Ykvw6zG<C!}k43d^F)UQ77fOxyF6I!gT8pMqE08d&icTD(x$kzI*SbxD{+t?AhH(|a)W;x1%8?Ha;7`|I>oe3Qa%q}`q'
    b'0^_pb4*3*>gk2qEG^jtGmy93ikAPvyLmq#}@PFDi5J164&qiaW5D79sLqBmr${|-'
    b'F!oG+#_Y5LaN6a5gLSC`T%@%)xFG#F3lL|Y4)UN>sqGM{*p&;mGw}U?$U8lD_v!ihCDvMC<CziKQgaA;*RlEq_Uj)PoE-'
    b'W4Uf#(rG?x&t*41|BZOElzI+64&Iak!VST&d#*4xh+`rqjzUEF82Twb3)dryOlQgNqk71whUwDo$u5(3Eg<d^g7=%wv3hE3h^Q`i'
    b'5rtRo+EX1njW-snfqZ#Wz~(d!23_L?gn?Gu{P?mtuHEV(%J>VK)&@kS7pFmIk_nP<~)|BlGpo!|?{2IuK7I5XlHuKhA)$JA`j1qP'
    b'rne()EY|60|Y*DH-fN^3}*-'
    b'(V$Rm)DLbJ!(ipl4~Uk4;UGyfQ{9;6khJO60`!!?OHAv8bZA=b@HdvIPkyi<r*C(xY<{IPycB$UyAfGkAro5bydaTS^RjMNDK6+3'
    b'eq4ENt!S@PI)DjOwp#8h{|pK@DDfseWHi2oDrGXmX>dlg=VD!Xsa|3C8~Y4NoFhieabfAVy}RI;s^cM{S7<+PTA)`Op3W2TPe2&)'
    b'i@DvN=C}@2*KQ#w&oO9Ge-@la-_DPnRnx3#pCB27f<{Nwd@>3sMoXRlsXbcd^%$Z36o_-'
    b'rGrWCtj8cbI_OWx_d*vQItyKb{1SG@bL>UWs=Ede{aA;%{8V63FZ~S4RP-fR&K%FLr$V$%uoji_Hf(4AWA$?%d;8vev`z*?;XuOt'
    b'vr1hO?Jbuo|2TD8O;b4?OuDv65@oXijdWkxgi+HWhPnWW74Pg!}9<cp8cdy@3Fk89BIzHwP!8DmgLcsQM5(Yi<AR4TpWX7B;?B02'
    b'L8QMu6rnvN#>0itX(%q6BBHL+5MxNMv>mw5578s~weu5AYR5P~#Bb3o5e7oeq%Wrc-'
    b'YweB&!j|KOFNcFf9@-w^JEPwW%?J>N2`(X0{18AwV8Ys;BS0iAaMKF>AHc*;dj^6JtB;Urd$evfm2{yCwT@T~I#LJ96HSaWe?%ha'
    b'---SN-'
    b'*E1Q9zrVe1$LEYR8dG1AZJl{kP&=)K#UY7PltCgu3w#0L{Ps3N`S453j#m@7Zx8A5SW;^7y|yZiwF#&zq4W}{Rc#dai1KM70k4H='
    b'={Cf(s4enQ?gXDG4WYvJ52o`-'
    b'VWllHZsuAwupo6GsQ2lEm$D<kZaKi2LzE3kJ1bLG4N{{Z(s<*!%@X}qL<NUJyswH+6I1?7r!*caJDr|Z3uYN7GZRVNT151RiYM%2'
    b'0KY(><aVR71~pf({tXAL4Z2%5|emm&Ma5r89D}1{{A@d!PL6LxNnAXi&Gj7M`Yf0<LS&-'
    b'&Je&;U$$a{zAv~OBX=D@8A=4wdM%B~=&>X;A;t&c!wOk(Tk`zckt6x-T>+hnoxLzrm~qs3E0L=C$cPM3j(-'
    b'_D@U>t?cS2jBVr6aYxkX59`OXB0m-'
    b'a;8!W*1$#g2jJoHEbi`#Xn*83*N*ADlt>zAy|=S)^9`(lI1>L$vQyFo#f0WIE$0Do@lIZ`%;JWkBbl^sVx89p73^HBRa9AFu`|O{'
    b'IO3?WL^SoQPN?a^(Tu_^|HeAaDuGr{p!Nl9L4*DM(02JPnw!va3J$r^;eL&<SMCkYwl#=vplmhTm^+`43VRB8d?w8$9(m=1|smT`'
    b'yblYdZWbXL#ct3?Y#zwv(0nw&GD9{O)(ujH!vpUb&C!X#13j3S6cmVO_>3TFXzOo;fndYSX!Q5>{K*8G0&9x!d^3tlMzQcvtHw*I'
    b'FfnbsnTM&L8E=?+%^5qmub0t9QiYh#&aTll;^rk&+UxBNo<AklIEQ8d5r*x5>T_kN_B13_j{K;oJaWbtHY%81j`i6QB-DiczSu<a'
    b'Lw+D4hJ2AX>&mpe9Ia6EdN~phHO2KGI~;=RjYxP{*vLSa<2bZ93W>GiY)0uiVTG-'
    b'f(%qxn<;|uJIhCzjoh<eo?$Tgap#$b<;TziV5L}O8C(M-'
    b'2CV%?eqsi<E|;Dp)}W<J&)l89n78QxiU+;WrDdb7Zua(6JUYRu<N_K0^emfR<V$>3k2)gnSuXZW-tk};k3-'
    b'RQg3z6T7qe}RaXUs=;ouQyx+bdIl(i#5WNZI)T!IF6Ik6T?X0Y2TL&Q=A*wdUDf{rVW95A^;pdY!IMYFs+C?hr(rpjB-'
    b'~qQm9CBU9*M^A(K8I?&$XaV*16Zdf>-J~cxp!TRXbhd8z-'
    b'Yxjz+Qu|KrvwJjW96dTmv^_*h#xOvWk61SzmeT!DGh=FfQ~k?=zSv=#i-V=Br5IS_AAKQ)mHB>k+5r*}hv{K>wdJ-'
    b'=qD(pnW^yX6$h#)@Oo36GD#)E<h6Up(<%1D0K<CRT%0eriU+OqWE@<RW}6lM#&Ihi9^^tf6jDX$^WLq!=eKTC~IiCdtAK!b-'
    b'U#^?+PG$n3cX8QNLMAqGEoNVL@Bh&=xkyRAk_J;f}VI)w_nZGpENtJ0?D3lNL!EbSDx;<`S`#g6;(kw3XmT+r<eA-'
    b'&)PsCQ<4t^LelOmHU2gtyK25FHe~SpwllwX<|#bUd*UxG)wj#CeC&mv0NumV0PWWa_`q(K9GdZS7v-'
    b'WWDEiH<e?`xuNd3Sx<IcytC8WR$Hobp@Owk`-'
    b'X{2({ar%)R)En4M~2m%yV07p7P#$VUH3rO@#pna3;oGGN*li~39u?Dpi<Cy_UB@^D<MgDL3QW>vkjqw$h=OU%HvqFD}-'
    b'WcL3ymq7VpB7e4qPaTi+!Tv2%W=I#VzP2Bj-HKB2`UG^O*7xTJ8QVfV6{M8AZoc1*IiO;q{H$Pm0&BZ4oG7)o!Faj;2LMM`0vys*'
    b'UEFOZc^MAo^YBfJ3u4KX_ROS4u9))P(-'
    b'P+~5ljNO9s>Iq7NmH|1SPk`paE}L#wB{U$UCCED8&V|Gnk#o1eC%|tD4JUWWd1RlC<()TMu*n{iB18`v^a%L5tp%n2fplIR!fj>W'
    b'B?9j-EhwDeZjPWt=s+lGO1wZnLS3MvU=qG}p>5-'
    b'Hu=HJ<3omWFytKE~HcZuY|4}>RIx^{~aM*Fs5zcc{D)qaM4y`@s5JQS%b%19sok_in#R^<)5pM73N9*2^PLOQ}bZ5YnYSF#LT{c3'
    b'!gE{Lqd^Rv=jBkFN;f}?$CY_Yo!g|IEj!vjN3Kg7G<45<9(7t!;Qi{X{kOj9*%>T<#Gffa1!c4$Uo~D!xaRcNt<u^<ar!u0jl)lf'
    b'rJ1db-SqZnmKKwh=cmm3J!shP8E;dV%(6i7%a7VkPGx2F<4Y!75>PtD==_(1NWn479n^L*qVFVl~k`DS<@QoW6Y$Ku0i|3dQa~Zu'
    b'<aJ}$gCg3C|exF=;<W~}tw_NimmpV0RjWB|;#*215dLWif-kqmKC><0Y)(%`lCzvOGS9z(Q7>-'
    b'j8NU+K(8LPUA!FBjd+hVABs}|MCItqi%pL{CQ$ZAdEXjmZq&n{%zz3~n~Bd=)$w0DhZ+CBLEy^xELh6BPWD@$pq>O!7D*p0u&FBL'
    b'*MthhycP?hD$`ez6e&#;|_Mf})x?`Q>uo#$W;f(KPZWT)_*#aYg+juXd5yuufhsgL%#Mf{ZU9mMO_(l`SoPzPP;KgH9*3HyBem<#'
    b'VRh%asr9i7-'
    b'u(4iZF&D|op5xaMSKY;)Z7BU3V!J0z=#kx=?Upd8X^JSD0KG73GlTl@5g$FaDMVBZBX_Au2#$`ON`Y${XW>CVP;&c2WpV_L<p`;N'
    b'|4>6X`AnsKY-_oVFCBdv52s~-RYX-);8o;^NSC%x(y|n<A=dzUQ)zbj5x~0|nZcs>MLY-aPy~@^Y#xJ5PbbXkSrnh$mUb=|zR(kt'
    b'Us*g2-(7d{k86YyV@H=pz2$xo#=S+3i*=illiH6DT3E3Oj^Rs&`E7;oD%L8TC4zYR}AM#6(-'
    b'cT?IHF(b81Kb)FoZGW~ttezAzPk;S5W!<sRo>Zk^EXC;470nm1se!pFyX7Cf7Q}z#Ct++ms}vE-'
    b'|_OLchv_pge{&&0NXOK{?v+7;sW7QPie@ji*m61jI3rQCJ?m|yZ5v0?C_x*jVPCO=Tg@zJKX=EZ|$NycjYy+wj7AY@#>&-'
    b'Pm8PbMxW!+w{isnuXc!~C+YeZY<nzKJ}QuHRY92%voXTg)s`nJi3ki4(p6W2)`tqr-48UNO&JhjA50GAgjq24CAtO|<TG{Yf-vmG'
    b'`e>GOR8}LlSpKNHo^+azMIdj8H7c3{N9-2{sSEnxSW!+j#1I$|BgRH}y7pl{>h7gfTqtOVQ!)0$ix-'
    b'{tS?{I<H$y(pd*DiSjpsxYWoX#0(#s8ep2dH-UmPr-&YlcbTOC=(de5bzFz4i+nJktXd|Go(5FU@y)dE6o(4wW!-'
    b'FZH3AfGCsL?5i-NMN{ie>Oocs-'
    b'3?ruv8VbAVx{&TiSBd9o_HTOOGs0Eh>)c{JVwuGg%V5Nk)L@5dV~943NX!mBk+O+9+A#clx7zud1R-'
    b'32VP58WB?YP*;Tjtw1adtOCWBDrZDx-1G}tDzB<M_WsFs2E&!I)vl_wvRJ&fZ-'
    b'8bd+_D=AvSjR`!0C*2(Bi8)<ax>perf|LcPZCVZaxuNz~6vQAh4nsyt}vF8*$AF#uZ$VBSM#VR87{`_qGOJOH`^)^}{gw!h=Dt5b'
    b'Kec#&~CrI?u;^9ai2@NN_lvs$=-}<5N`$0RVaz$1k{3Liz~&Q32UB{mM}5DOd~RGVjj&$Fa5jLS$}VxtsJ--qu?eSTKX3LI?@;2f'
    b'3WcqND1qEcvGU%L5@12nBVmSgqwU&K#|nk{U;Ow`k$Hs@HYA!5GGY0;JQ*QQBC*ay)Ek_Uin7DH9N*Qi%pA4|u9VSU-'
    b'd6gfeZf!44`etrR_nwDLNI`H@kv&JE8urOK$%?$xCo$Ort55Bz=8?LU9a(B3&;RQW0&XiC@aLm}jCxwaiu)g0-'
    b'nw&mHA$V{MX1zT!7Hhg79Z&T51UIt}caK@EJ&V&IR)!<xtR+I|ZJS!dt-'
    b'@~|z!ZC6usN!w>%?l1`gF<a64@3;ch)|qcRRX{lRlGtxS~_q`*b{y&e+89R!_l|$A%6JH2D4R6jcGrr76FTr_7ID_5F!E$Rfz)aN'
    b'$T9S)Q);YWdj9c{@Gdu1AvJ$b+VU~H$}j~2Ke<poDuC4Re}{!0_TY(AOs1!_;?%y&Y#CjWlbzQQ@^|IUPzWsD-'
    b'H`?6nIsi1w98asJ;OzN~LHBUnnb7)yp|1emo&Mh|g#^FDftIvdS_q^r{kUSK!&QP~|1-'
    b'+z7eHkO=Hsm1JK&bbBXh`mM`72cqJttG<*fSSJgaN9K2fvo79rDNOYx7SogWMK=%xKz5uJ1Nk_Eis+yPj<M|X5G0gY2NT@8nD`$Y'
    b'YpRMq<eEQdx(tT=B7P=$czF3J2L@2)larCqq3cdvtqW}q!+}%+DiEyqRmuz$r|Zyrq?$3$!<7GBoaKMlYvx~dbbMDuZdmd7+<8*<'
    b'CNaGMz(>@kj5uPmBAP{Nsvx$A&}G%C4V(|#@_B|DL{xqkl7`D^<6Ze91L2=^R9W&&uH%7Il*ush&?!ALf$2~03fx;|yG(+3L=}Hv'
    b'CRFNq)Z2R0PDxO08OeO!H&g>LQs@ixk8dAyZFT6lck%$$kM>y*W^wX=H3n0f^46ZU&P<Y0_*I$=2JNY!nMU{|KnxY)8Bdv7Wg-'
    b'I@_c^dC%V0N3NE~Vu(lbV(3IPg_KpW7*41S9G?4}Bh0l|NmyT}44JoBl`;DIz%;UNfh7|lQd5GaebS7z9N-'
    b'>0t!gdE7{R}Ii77Dm;d14FwqFNyt?SgU$fL|$dS<_x7)y1lAX@yVa4xpd@HyfOEut&OB8R<BG}H&Rtz^{^mF-nl{wJ3V!Uh(vv;B'
    b'x8Cx$K<;*!QUFxJ3?sqRp~XEpX%s!_;ch1;QP2YqLg5aLSx~LXA-E#Wk$O98#nJ9(%ZG27f-KyjH#rvRQkck(VWg-Vp8u0c>fYS%'
    b'96H9FRz78gv=;Q<Hw5ORX`WCQy2cBd(D(bj8Yzj;i}`qJ=a4zxfT&DKf0-~aJkslcv-'
    b'<b`{fPk9`chd54X{+DTm(ZEQ?`*vb^%?+Fz7sBq(Z}sv2{`=hC~a*|ZHE)UTr_G<$Y=k-'
    b'GV;o3uzCo6Vm8I)BZ+>uv$^(>njU{W)d5Aob8~!nq96v`_HAF5|&sn15?{!Be^~C@~$`em5e2R|nwjlW-MgQ{HZlJ;Bd))gC2fI6'
    b'TZ1HKj*u{~;8mU5?=+o{4J1rEcs$J0?2t&T3OsL*1tCHzPoR^1WlB%r4V#$|ee=eK2&wjS64EnxTfw&39%l<Q*W`0c0eC5x~{;X>'
    b'^%n#BD4u&>K0W`z&W5nveiZkf@0Qkv>f)i1ST+l@Jqm)+ywQgaQ>YC$u@-AVT52>bl4*YC5A$DOPX<Ug~89^U^lZuS``@F-'
    b'xRwR`kkMH}uYOr7!>~cM>QgbCvdDtzxOzJJ1A|nz%9);<Mm7sw`3$H#Sz#9zk8JN|w*Yn#YDToW>fcwH8WR_ZE3*Bc3UczS|GxSM'
    b'Dagbk{@mHTT`B^c53<H8xdmR#|zN+O@|y0Myb{e?!%A#v#aVl~$;Ael{~#Tre<bAJ~qSsOBQ5mJdF!TH+z9K)}%v0dQeh5LEk?N~'
    b'CK#vi^BYoC#eX2?v!33DtGA2zW|`_G3D7!r7P;%umhDLfESQ)^)*7)pB1x0))PHH_Tf!O3gN=w$bfO);1!7htls5_r!`6K?8V)lB'
    b'0o2SPDz?BZRUB!q*F-<E)-jh03FeuBt0ERd;0m8{_oB&s{V}($Np`Zb&P=yhZj-b&Pa%pq`XL!1AgV4m4bcfVvw)Nb`#7!(sPO-'
    b'c$f@tM=G>46e(-'
    b'@hb<Vi|`X+IwI5()fO6lq)m)Tlp<Ug@odED=rO^+*4hE#(iVQe8~Nw(L{FcI2Q)a&Z9;xbHDWV=jqj>hE`SE`shSOIza##ui`mjC'
    b'FDqXY4C8-E#qYx?C2OC#^CbNFtYVHTMs4n<BwGv@eWCOu)Uir{z1~T~a_eJscrny!i1?zux{~aaaZNmx9UX1q+H-'
    b'Ij@D~<uHeDe7%{wMj`_jO(N{Lq`^`FumnUfK9>5dfCU9ndbt&$m`zgU)T%r!M*$)D;NUlujLtC5S6HX(M6;H^v?)tOeV7ZX)+&VX'
    b'WA0$?P?C8#TW@wAKrQT^6W{To<pQj>)2g@s7KPKr)kJGX*}1h>+O38oS_%60`+3X^-'
    b'`{e(V%^G7ojm5^=Ws)p~VlMggKK&f3xxsb~GIg(d8b)G5^5Y}EnWs`0C%X{hCs(DKBo&KbdDs46$cuoV9ltwt7<Kv|~mtIx6MK4A'
    b'8RR<t~^sly?u6!@`FFFuZh^`TDrs=*JFrTk7p)2ZF#r7|nKTY6NmD~`nN@MttHk>=6Ct?z<K;5{jD*k9o45}f1wvKHY_E>ZWyUG~'
    b'4Dkih$<5wS^ytSJYlvH?3yFSD@BHnr~kyl;2>ez0DwqUgIxr006ZYnY_4rkh+{;}eP)x-'
    b'CBzRp_ubEJA$jCxdf5!$`R&Bl6$^;C97*RAMcc8Gmw+|PnX9hKE^O;_v*v?6>klQyo@ZoJ4(RW&!{;#HCrN^9@!lYrgr?OaF%-'
    b'Pn9V>0ebg+8KS}-'
    b'Qa0UZRV7PGjxep=Dm5YWm5^vr7McRyOqI9r8mE<!`wR_{?bAAmz_@)bz!t&GuAdOJoP?SJSo>5JM@^x_1Knf>?pvg(bVj=1CK$ww'
    b'cngH?W2t}r{MyGt37nPPFv@$q`^^GR9#PPIxJGf)wu)Vk*B)Z)wKS|GBtrIBS$kknNOe>OH*h>_^O_+de50Iu_o0kwN%x7nHQSKF'
    b'XsO3(wlpzi36(54zle^$yLS_pEG%7_v=n`hXt)ucY%SGSo6wDJ`w&Tl-B_srqYtA`hWvfZ=UAxrYpy@RU!`{K5;4y-qTV$WrStd-'
    b'u};4hqVEJj8jVp!Dn2q5j0`}Ymb@58+CKxsC*KB?52Ny686km_{uiqUClB2v3X-H;Q}a+0MCTJrOsj}w8b|FLzfX(-'
    b'H9S%ig*`v&gW)r=PBi;q0UxEr85h>{N_B4{9+=-'
    b'jp;;%dtNPf71y0j$Aw;oC4ZZV+PJr>F4v6Z><ebJ9z)mN9aRBB9$aPNoTkg@Mcosf(9RFtCpqI2V4hmLR|ujjVK~+(yT%cj4!mDA'
    b'uZb~r^bQMD8k4dJO$UtYdjIioIL4`9x%Lj=4FkM5YRZ_#;Rld$x-'
    b'Fjun5?TUHT0Pq!HdO%qsIGkR>xcQL|0QIm|EA(3R7^UwN6Y*{ME^(jxSNTJ*A9M;<#{<3tizSU`+mYM}%0^bbjY&%dUkT;6u1*u8'
    b'3rOQ0e_T;96H#_@Irb_Jh6)DtcevzKAdrFOzj49V~q^4?JOCc~o8H+2~g_18y+Nh!TUaWHkzFHwN$ssQQGv*7nj;cf*Vo(qqG0Ky'
    b'e`EHeEU`(^%wNwhB&%tS&7|%b1Pzc{#oPyU>rg0Q4W68H-'
    b'=M$*NtYAHCx<M6r1$kHHidQ{@mpQ>KAwOC8VqWOZa&I$YniWGWo5s;c@}*99|HCu@F{umDL)VLz2?3^>DMdE=L-'
    b'xQrH*IH67`sVj{h_-siBm5K5005oqk6dJpzml>pYS44=#&UEj0Ddbz1m*2^0<NaCU5}nl<Fep_)CHgIcYvo(J11_k<3GqpTSyJK+'
    b's5B)cSNL4RdZ~l%OC1q(kdwhzpqQ|u#xl<#xUOk*eu9OpF(fr(*A?Q{tNI;4-'
    b'E_xaf$D7#W%`e{&E4CG+75$1%p4o8rCBGQU~e_&wQ5+}8&f60h&(<$<xfWh)y{1yl3tWt2_&F3fZ^u|k(JejN!OJWFp!|7qBGf5M'
    b'Zc@w+?Ps^ot4HjF}r-%UZW~V`%w8~UBn-CS7pcr>5V#90c9BC){S;0y{u1e5}xO1Ej$eqB~VDJKx(1sMT{M5Q(rxm*~(@ZjbYBCs'
    b'=RY8A1fxTx*P%J-%n8|d!QemgHS02ouH$dItHnLhm{Mg=(e5GiMHr-'
    b'{KP5Du0Iz_@79(e^ceFjb*)zUXoB{muCLODb5_qUuRSOcOh*#_;|xc11M@{`E0ZNJoMzp#>ytVrlK7;#rX#QLu4{CW2bPODDSzlg'
    b'OzLJpGB~xg)NQ>CXH)O-'
    b'juRxTW2QL8CGh!CR*Fne!rCq(_DkE>zjTA(rQmz^hUtqb*#u?4%%ePTcq_E&9>q<TYQ`)uSDP56`@osjgm<)1zw$QMcO9NYWyltw'
    b'n`y3idq@}h+$UlBwp=@MQXLZTXT}y_9rq~$heIfP>C^s9hinC4HRcFD>tf>}pvt7^9f)CeTJZ&r<T|3N?g7U8Jhimeh+kRqL)RRT'
    b'f}z!R;w|1&LofA$6%d1G+gU9lF6KL9Jc3w^5s8ISUu7Bn45|jj9dFtXXrlZ@`M@QhX|gVNT%tLaq}uo=WhPmPZ73DOej0ybIIIt{'
    b'oM1p>fkQh%FAM<FHkja;zxArIp@fNLI_l)7o>si@fj_Bn;UMgkEvR~^2uyfPkC-lDAV*cFT-fVU@2#MEwD=hgjKbF0_uJK!mGy9l'
    b'vZ{ToD}n(^wrr@d!mY$#tluBP17%rzp62QWu@HFGOZi-<*-'
    b'Dv1TV5SFBiu6Z?tP#mSq~LH05mK{%n8F<&si@jQ&ne}Df^Ue2(gqaA9!w9YGR!AV1{N}y7<E|o`b!s1MYTroN*&GMTwHypT8{2h|'
    b';$ylWgnsYhEJjWW{RAgYbA&Wach?i*dul;$x5c+sbu@mrGN9TQ~DpZe+i-'
    b'C0}bOMDz&e;Z|KDS%sDmE!ubKU^qXZ#;yY&O)3!LYHqR_f+{k7>K8l2A0@16j!@|xPBpCG)kevcIj=U~37~~g49$o!@YVLy&83&m'
    b'r7)F6J@D}vR8BxQ9(X~K{i1RXX!G5Gc!sAe?yizPV1)W3U%^TH+#oQ_0)^fbd07~|=4z{G1@N}vNqkm0SW28&+PwgZl3UY`W_UZR'
    b'<E0|-FV*U}>O4NxV??a4AFu&mB%DRUf_oUM(twQ6e)?e`P;On-uGKOzWPN%pSyCm0*@+1}JgX^>{Z(HEILT-'
    b'5_{pTQio}B&b6J=v@3m1@H`-@Ubabdafj6ri_9`j^1v!n`peac`0qjZ8Z$$~VDmR?;rxS6mVpQLms<Me%OZ%0|p@3pVAW-'
    b'B2AVgdSRJp43DyMthC*>LmKAg~n(X#kIl9f2I5ZJ&r3(4f5URVuRqgNf(Chei%q79i;Ko5_9rNwB+`2G6~U$!ar(xBc+sr;_GkT0'
    b'd;qBB{*3(*_#XzwB7o9*C$*P&aMs<y#h=l-'
    b'pNvrS^v0B{0RZ=b&NbErCEUtqv#T}8lF=9NIW3%Mh@;px!fji!d2XyZnKA%<F13a0I^lpdAf(k0Z2+OO#>gCH4oEgHHu90U(R6-'
    b'Lig2W;XO#ssw$OJ(-vXHY8SfPDdH!Bmu*7+h59ikR=NT>Gjb^1M&Na6(_oK6V3odC^<r+r2AlR@t1`MBzI@V?g1ySS-'
    b'<21sm#wcU~QNA_g)PWvi(1an)sV|IG;ys{heUAJ&>!hmpi8{>IZ(Yi*q_a0htr#C%oCV(LN-TnPEt%ez<9lqJ)uoN{RIG9E|}q){'
    b'FdgDOKQMHjw-&ZsM@!n3L%puJF{!#w}ym8$9-j@}`_s{SKlsLlvAMR%Yx(1p-'
    b'pqEtvL>B_j8xxu!P>JZvfrhR2O+qX2s+2A(6ZI{1p?F?FiVImFV21#2y2<y8*fTa6`I^Nb5QCIz&`?-'
    b'Q&pfLD>yEsi&`D6&A@rxV$Rr@BCr~~gpvmu&JSb@AnR}R(woR$@}I)I)A#PJMJoZHeILuI#SFKPqHSYwCXD)Up<`Ra2Fs#^8X!SB'
    b'SIm*hOmPZzxST1VLxbnVtHu%OPpRdq5|7N}}-'
    b'7s)@uMP0A#;L1>u;yC|EkFIiv9#k1fdAx+63n@QpJTY$vbZRFeX$vsjOFSxtPYltb+`h9M%1c+&UMdFlJM;bIUlZfagcc=!7jU!#'
    b'H*rDlvmg<v=U0tPx(J{yRH^00=msJBG^$ImO(TlM%qOtJ4nMp}&4_iILRW@#4=dCZ79JC9gtAn)5q^_`$FHpZ^;Rmb-_mzQ#djTw'
    b'XLVJ#l}>8S3!LxjE+o^T77ZYPn<_oxt=db(mCJW_d}6A!|J1{QDyk2)`hX`?FcTa~pUR7Dmyj7JlrpKi5Wut50kQ7*VOwM5q^n>J'
    b'^hd4``v&i%?qdKJ=BLD>QzQ09jPYfsDH;~fP5oKlz7!_;rye?lx23il1bXd-Ok_nx`BZ|KsB%+hNgbX{LKR^A5NV&Ej@|ibD~b*q'
    b'xC8c0Ff8f;#wYK%rn|xm+Jc}NR-'
    b'D1Bm~Du?tH4}&S;358#Qsc3bvNnO1NAQp;ewPJYv+Y9g>Ina&YewZl;~UZhibI0w+jNOKC!O%t0Js~VpRXBatMIchw>g4umCqE{P'
    b'S=rXkPV(cFK|KhCi8^kHKXf8mp?+&1b9Gi84`+`kI`CAnOEF-r|P2@hyaGTA0^b-'
    b'+3OcZYYEIP3i~LGWeCAi*bReQFYQXls}2^K$it=`9VKnqP5%|)9mT*8g~DzTgNZeKK!m4y>Id2rWP5vYDhquIX^yd#|*JYiuAqUz'
    b'v^!kRWSA1v-<$yugVhc^X>F6<z_3rUF`v8k7ub^EU=K&Y+G$oMoDef%X>97c0?dSo}uvFR-B)?(VQK%0hzG!T4v-'
    b'sai|f5dC7C73%5X}t&9NON-'
    b'~Mc&)}bw|M|JE3E&}t&Uh+2D0dFCP+=iGw?S7BrqvGAM2E%N`Sv=Lqz$4GFv5Dbs>*B5@JdeGONS>cNmG{0QFcuZr{S1GSD_iq{H'
    b'wv9-K`UC-'
    b'F&=x>PCB06>0cI`qH|PUUWpZT#2l@1()Cu#D<H{t9(j!5auw{CwNb72;kuf1j_Y7@8eg_%}Z~y>xGN@nz%sKMfH^6JG-e_QrZqt)'
    b'pd%fA|0rYGEm|wi<6DFx1HiA{VRIE%HkB8tyh~9!+qtx)CEX|K6oK7UC@Qhf$@eFGxTJEvaA2*`%}M?3bZ>zP)?rlgr&+WrDWB}('
    b'uN=Wl((p?cztSm9@!Q|4Cw-yT&sNYC|)`(d+F38pf#3mDNm&|A*ytXdlu!UAnSE|EvDtl*x`?Mi2(PwD1e0p;uN35T7qJUL5bP<v'
    b'<1wb$p2svjSr>`hQ}E!KLyKza*onUB@3{TY`(toHrGoxPrhsy@*VUG+KR|gJL*r$^o7wRm1ESdGfFHfJ7B6p0Q~ZzO{BA)5QBl-'
    b'w+oP9F=g_V6`KmH9}i5!S)*vXK~-ar-(w7*IaCNk-a1=V@&0gD<#pd3)OQ`LW2=fn>b$N^q_dB9w-iydfwZ-Md@Fpqt7;`*j!iAB'
    b'r^>pizRCXN7ejqvT#HxcW7>8%+sfWy=?daTx#`9LQZLrjOK~myTiNDnOj6#R;#jo{uI-'
    b'|t3KTGAP~zwiW(DKf1MKA=4kE@F`kgyBxJ~cI>%bvC7cDE_AB9N?v7vr+tsFMW@9Pwmm1<AZvO|;zh?J8vcyB{RdlrcLayHOAjKZ'
    b'tmruzX9z=CfzX@sUeHbL1p{HbzOS=*-tIr!{LTVqq5Cr14gOL&QGz0}HJqIy(%1f7-'
    b'D(3<}uymX;>_Tkq}*KBp^v1av$a9!PlA1%=NB5l62IE$g;VgZVkKChyk7_n}|plkymrxr$q&>0f5k(7~(MU=|N@rHWeP7ZnLR!%E'
    b'@U=lbc+C!%VS>-'
    b'kHBd?gHTFCN^0@vDr){zR;9;b3YuDY#$;#54h;n8DAAl`1KT$>Rc=9X2)_F{O@FHrJc_{|==c!#P~p$aeQUD#ss3JY<QjyMYMMD('
    b'ag={z7<AO@aWmJUK(_ikbqIHz)z1u@j?=Qme5cq?i8oydSK)^4Xy=x1UyDX4NS>{V42RZFC229V;&kp2OssqHpDs?vu`ea@%8Ysc'
    b'ivDnMAv>VY`@uGt;>&|BFmH0IjWoE2Pn61r5WEd*5;Mh=v!ei4hG{z|)fskrXkZ7cA)N@!m^=-'
    b'xnB+bZF$qQ1zitQ+N4VhS)4;P7@t7~yO(__vE)!ibuo@GN`M&7NMTnn3E@wkOOuqXqXm2`^}3-'
    b'5}m7LfED>?3WJ+zKd<Wv{EbZGe<Y<2z6_oT&v1BfCTa0QkpXV_Enx<jqs%>L8W(Z>Tnx9h2IPm=m^-'
    b'I%5e^2ci2jN&d<dGHCP{ZR218pZO8>0FNS+z8(1oow*NWE?l&JL*xDHmUtGF3;3}|-q;o?M!i}o-'
    b'J8L}VPZr%(AKazL9_Dve4ymDSK9_DQ>0|%|Ur^i95HcvW4idaq70<b7vlVnqq^oyCFJu1fI~j#!SXN4hn(7e^T7pp#Cl+dhWhDkj'
    b'?LKJR=eoAzSi#<M#Sn<bpMur8@Rd3fV7j|1a+PxF+hz-_2Y3c6wpv5-<bZ_=1kR-'
    b'*>Rs(YKX;%J_}x9tTa_8R3c=dD65Z55V?*5d%TfkZt2@TphIndg>iP;J^&d!YSviw6H-'
    b'daqYCU1&xmV1~KpD``RTr&^aPh(}jCBPeGImoNl;CCQQ7&PrDbG#;Yl>9|(e+`Os62zYF6t8hpfzgB5YiP65%6Zw3FLPkWEa&yj&'
    b'aTt8O|X@Az5eX=BU|q)&(mUlEZuw=&eCCR7@WqorR@+d5a8+aGAz*?QA`xKmnSTUwdRcfys6q|Dn!#ptAK$W%7bj8PD5V^Cf=sk`'
    b'8aUm@W>jZbhdQ{8xXHVhabxS5*qkloDQ5pM#)TEktD_K3*RC%Y72x*)RT;>Mlrm$AFrJukzk=pKgnI$QqqE)%8}_W7Un~+4)soXM'
    b'NH>F_Zf_^>|Ap2Jn}+KzCtJ(Pf8iSbZ9ZkEKguP{Y)#I<u`2c@61^piL27`293T8hv|<s*47(YD@@7ryJ_vMp$sKYA5*AJyN@>OS'
    b'Yr_subdTe7}2?^DEEprdln7btqXCdr?7%P}HWcp0z>Xh`_z7k%U=v0yof2fM*75teRGTyBrFR3jaoqsm;4eGdbEMsgE^SsOwfKVx'
    b'L#t6;^7xfualvf-mly^V{8NEa(z(4twBHaCj%YLSg&FvCNb%7oYY^galvqtpA=fsidl>pBs{pO=t<SAStaLM9;8ew1Rm%ytWDn%o'
    b'{SQLQf7DJ^W}ST@+6#_5Aml@Bf~U`7QzdUB{!>+8wH0Vow#n5XzmssVM#)(P2wfWo)i;)zydT4wWoxrkZsy&9mO!1lQ{UPP>n_br'
    b'n78#1+lcCK``;*XM4E70_ChF<7nNrX+aqfR~*46T`Pi%L$Y35t7vLeQyXCoJdtQoFJm=$=!N;ZgVKBEX8DjHJRz<9om=l)N7SrnT'
    b'8BIC~Yf4aHz6m3pt3#DIX8uL_oBoIyOFZFg$fU6_=8gKZ(J{O9zn!NMq*Ts}f*;ZhpB9b#|FNue){|boa@P7la|Au}+=qv+swpid'
    b'WpSisMY(kQITs8&&`{-%rWInst0ut@AhDV8sCk8hQDr_3cZ8dZ{ewTY4%H?_yFNzoz2G*9*GDL!E>>KB)e3Fe1-'
    b'qjuom}lVeN0sjEvSlD^%_07#S+NlF%+4vu<2QD%qU+mhxf=ukK&D0Sl|pxZ#aG>lvss-JqITZIOa(j<1=S+_s??yL>cAj9um_Yxp'
    b'Z>i4GlfKkh(D;kV8zTJjAsm4t%Pmh6>iq0Uqw#nvwGToW<sfwdmp*kY7%sY2&T(+d#RsS3vBQ8-'
    b'js6s3ri&hKhrR#&}9NpEa71S9ROH~(8VCSaXRTuuaj!8asuR&hZ9m<SNc3uiP-nBWm!&-'
    b'J#{FnGpp3NXrZ8E@8U>i_=_|Dr!Hk=q)bUkw%=oT6$m80{U<vAR%8M3eHaJLhxbcd<vCMeVv8C~N?2z}S~;nW4CoYfLxR7sNV4em'
    b'Lbq2Hv3P`zL@pw$sK_*Pd9OEh5C-t_&m;K0=uZ#@oU=BGBmeUH^XCxUG!RhyoOV|6dx7&d&CNM{!pS-bpA+Wu+WuWlf}EZ`n}u*Q'
    b'st5Ol%_WAG)o4{JBH$PmE5e|p0Edds@F|EJ*?6tb%pU<#_{J*D0^Y>oJxI)MbD)KJxyk^7jh4%Cs)+7)VZ>m^@i6iJOaVJ@iUtNb'
    b'i=QW<3lyBemN0TGy68j4d&5I7n3h54ba)Kc+npAuv}g^WxD(GnVXt<Z{6En$`FvDZ3Ng8Z{o08rBnTHV46e|+jKLQ8x)H^g)6Al@'
    b's1b?gGxnu@6Hs}5otQZOKvB{#@y(RFlvs`m7UQK-6vjZ(Eu4J(s1AYPNts#CwwYE_>rIEsx5D-~-'
    b'~sh)89itD_L#jK(jy2>+Eer;^^7{Q2@9~zpn{)kYi*OamyUp3w0Wvd{Zn#ZkQowNVenJ>bldn&}CGuv_q4dG~=tCJZcJm^mC(Iu9'
    b'sRsz_KtEcl>xgY3H_%x~uD+TQ^$5@_Tbm^de+MKzlSWUTE8?v*wEVM5)hwlG1?Yk8J+~hac{vAJ$fwE3&`82E$97|VMQ<W`fRTYk'
    b'iI@l;<x3U4Y<aww7)pxFx8a5i%roA%M5JqiRjqkQ@K{KgKaLklXQwd?+t5SO%L>vEt+5S`xxhnk5vP{P_)kjCQTZ!4G9q(C)<T$I'
    b'UH?7fC^X5v}yP7Wtzuy|CE<=KgT;&xUw^dctD>jsqwp>G2$w*a@7#pE$JnSy$D%PkBthZAt*I|BpLzT^-'
    b'e)F*2Q>1oOvwf>5KN8#fF!PzVu1=MbApYtjKkV%SBsrnwIvSbZkVB>zafhldN)^cg-Q=-'
    b'P*)D>3f=0uvr>d{+=qS^dWm&wf?AAw5S9!ClGR^0r#7l=go^pu82|cP(ay(?JRZ~B@Nx{PQuRI=o=|=WjJ{4EYYF$=UAZWAx5#4='
    b'RYGaW_!S-{{aw{j98AJ{bO`<ALd#U!76|Szzu8(n$etwi%fA+kp^$rn2zbiQbWunq7`3XX``Np-tNuD0duhtANZ6Cf>NaDJwPCZT'
    b'sq@f)g3%7U+oIb<ypjcop{<*gjB(rKknwq)?b>I8s3cR#M_R`$EbRs0)>9K4b+MK6T$dkD#OYTH0B6Zo$)Wb(jt>13z%rkQ|iX*I'
    b'EzKHN$+^^S(|4Qnw5K$WHq?okvv03LBwhBHEUA5sg&J&@;0I{TUld4Ys>SnXd19S|n)Rk+lsFKRziMp0hk>YTP6p=N{c1eACSL0$'
    b';#cgVmRo-q3{K|&icO{hTsuotZ)CG^HC#;XKhCf-'
    b'rOwUrHzYhRF?eoG+IfgaTa_uDZ&i-Lr>g8i)DN8q+I@pfA_Eq~jSb2pD49uE`WhPEVWSbI-AVpcoc;4Pz&_*or9^In~4?uB<#rKT'
    b'Xb5tCK2|@{Q*JsOSsc!gPQ{}(}r|<4UzC_xth`uQ7R9~^W&ruoEu!Ntg;0zWc-'
    b'k<gs^HhQnoMozgaArmN>2IG;AzGbCuxDXTuf$nbpP_-'
    b'N=mH6GkJw{a4`vWu=FrsRdoZvx)~{~F`_2u?mr6JM%3=v`9jjM!?E#EpDX4V!wWz*BsT0i0HRmmQxx4{-'
    b'c_h5nEkvc=;p5>`AYaw<@$CY}>4x_zBM|PD*O){RqU1zx=;6CZ4UnCUV>cpIsUYO~EV#D_E8Gd4vef0~+He&n?GcxXH}K!2?%$*F'
    b'awtc@_-'
    b'XHzb*8w!v$r}hq@$qBZ!#0S%*iu`U<3<<S$H;mH8KQbgAWp+RL@rTU0hjD_LT_`5Vp!kP04Su^dxI$STiEu?cr_O@$IP*f0*UQ>#'
    b'1W=DZ1NjpE5dxQWZ;M6{6a(cb#C%$C(t^OkTVXgtncAf$GvC@4b?eBD;EXpFe$|PaCkzTe2N2jIXe!9*?q0UHPg!>?nO<<8VA>pB'
    b's??8~jjPqqh@h_%mrBSc#@Uy)*~$O-'
    b'XG^3)J9}8k#|xmiDjm4$53d5NHqllPiF~BPmvf)VJVmRQ1eJRkmFA(pI%;(+=z~nDs`x;I#x6C|P3GUcOF)TDo^WZwq2I)ll`en('
    b'{6P;xb(Pk1$@1A*)+;=B0>sgy^c8N?$psw|3g*Rqn)4*2UpDYHb8SHGRQb8wqBK_B2%6#w!NMr-'
    b'J(G1rgAI{*`CGzp~(wswX4Ab#71;8)h9?7&DkuNnCu=2~>WR)wN4G`KYs?dZ?|^()c?U@}JftI|3%fYDv$v8x>)8?2xsBKj>fVY_'
    b'ZG=J#6CG9nysIjK=pczWk~20%HP4)Lt&AF6`Eqbbu6Oa)>ls7ZujieCk)Xn$scD##?OPy}pw|LVI(@KNA6FA+BM-'
    b'8;TKh!_5b5f*IDm9hLdKgvwnJf@)z3)0uxxSuF&w_@jwz*g`%%y@p%dATeZ{wOeWp*K}T#5y`mZ)!n#*-;{dau55pYE}N-'
    b'(e1!Yple+9N_Z&piji5M4#gJ6LR|g4Ow?;Y<RIj`D`O1Xyw}Nj*N9Airm#RX0j;FUp%MR1trc%MJcu2TZQs2#GI%Pjk?f4r$o0%`'
    b'UreYd)z=xA++jpI9<&0*4ize-oh>oK4;%#<NFj?KyTnTn6yIwze>HMpwE17aHM7y&tG(jFy=IJs<C~V(R9cD}o*SdC7!d8hAHHLh'
    b'*3ioELA?1qN$vQvjgf+r-'
    b'j%qSYM8~VNDY*!KE006;cGag+Qyma#`rqda|EzO{9n_L9UNwM;!_wSX@D5KV<=r~`TC>9@Aepr*JB2_piwcWDE7IGS-'
    b'uFO3s=Is?p@#?!ctgTC!a|U=l$t7b!i4iy&tFw2K(ID-(5)9A`q2#PM-Laij`>a^9-'
    b'qLiQt4>iqM~L4#)Om%Fl`1lP=1W3y6&asrw74*{Gb2rU!MPbBYwf4l;W}O8uO@2cf;L%A&L7Ubk(XhV2!BDQf{@{O8pXzQGIRyY2'
    b'E$K{&Uf#VVJDh9U`$;T^~YJ3yVxxOWGpHQSISsP>~H-'
    b'>RhZJ#&4(2w>g2UZM^`NcgZt&T05&jDtLa?#37UwfioUx%GlS&=KQNA(I7;h-+ayDSJuS)vJMOHO!2Q=skh=@T?C-'
    b'68@^Q+O5sPr;a^8LgKmbpZ#8K_`TNMdY{5@UvjBtI`rM!TUC<EFuNJ;zj^N%Ng7xH*=dR`qVBd1heu2)%e2P*xAy?(1Zoc%S0ObL'
    b'}oS~|6gAvRK183ZA<IVx>DhQ|%MLGxN2KQ3O*afAGMBUFBG6QGcN_X`kAIP@~l^bf{;V=RtCI_jV4#Jo0!B1MDVv?C?G<N#RE4Fx'
    b'2SIc-?Lp93#@C4_nv7V+#QIIvdj65zBJU$(vYn-$B6BXm9u`iRU4qs-'
    b'7+cRTSd&@qz(tUBzh=9snUE&Ccy|$Xh)AxWNG%gDg%a<OE>zpJq5Da|{Yw1?z#i90?htGvRM1o)xTM1{V``z)#bk+H8r<Y^6E_@G'
    b'U#?el92Hbk-yiNrUWo@V+b*WPcnPkkq?)jt3n{w`gjPvE1c&PK_{kg_vzzGNpDl4Ug7rcGzaE`y`IMKtS<5NX@=gPDSyZ>o=yb)g'
    b'r>20Nl(@@`~57-+MTQ4jvs+b-'
    b'SQ&sA*>kzNzv2+=rW;K<1cO&PmoE7HkC@BTHUeCxl`EKo;yd+m8F`uR*ljTvf>JDDR1qo#)WPN)(@}(W$mv%K5Fnm>Tc^pqk?LJh'
    b'SFseQ?I>y00n7Q_en7cf802ZSkf{)VqZ~2K+m<>}nhK;0BzKt=Wyb)*{5ziY`mC(sL!gn=dD$+M+J8+}ji1lN|6{)Z?hH~fJ8DuK'
    b'iikc=Vg(AtIcn^%Srvgo%_oD7rmMm~J+?${L!BI*F2NLe$nqvqDYqyqWw6Rc%4C+9BM>(<W9i9eJ>Xm!!?Fu&QWOYM{AeB0f66Ut'
    b'9B!;q!c6e+S75TU~B_%Jw@Dp*U`MyOh7(O==RFx-'
    b'cSF;8+?;u7l1h2(4EsSMuP517MptwxwLk0j~(7+@rG``)6<)vbFzcUj8{MF4@A}@=UPSEWb-NAM(7$^@x9<|}K>eb8dK~3(R5nyj'
    b'~$6sBr&4O|vu0z&ZMq?8~RWoo*HI|Oa<5EE;;%e<uzgzp=c9|H9y3Bij^YO>59oh*sfB<N3A1ZO+cC~pzX|-Dp5DUs>{-'
    b'CbP%U1DdLO2{~kH7CY{{Psy>rg7~T#uTRIS}CmYGxYMqyahB;l>_M*3Gd}Ej%6gj)%K(*7zyQ1B6YYo5LOI1ap<`x~_6xTD++Z-'
    b'RV{iY@P`=m9~o0oqY(Wn;`tjgiy_GA~+#Ur3Yc<su(-'
    b'(3gQN=KDtl$71dATxi!p>uIZ&UV4~grNg7azS+o(MRxIZd8qZkWhMFEt)s$TO!n=40QRRLKgqUkA2U8<Zf8~|_w;rRu#OUFpGED('
    b'QwyOR}cIP^31UO5+d<QODFTjIVhxox)RmxYbXL-!|?|<bps(Z3JoV7VEdJR73=@;Ru=H!<L)m@3-YI=;OT`B0s$I||t`DyQ-Tv)1'
    b'=CD37tsb{y2&x*2)AnvY|3TVzMQ}$4`l1dHrM?HeL?NhcR^{D$}p>*g;+9xo_y3~&tAF9`nchofxlhws89XZ0wI#kh|U#*{Zk_eP'
    b'3l8rfEsHY0n4eaZjo&i4Py{N}86sxEW!*ej{fZ=wv2YWI1>il2-A4uc#Zv'
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
    candidate = reverse_delete  # noqa: F405
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
