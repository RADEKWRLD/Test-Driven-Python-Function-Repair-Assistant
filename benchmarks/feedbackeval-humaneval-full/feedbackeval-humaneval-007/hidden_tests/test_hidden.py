import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [[[], 'john'],
 [['xxx', 'asd', 'xxy', 'john doe', 'xxxAAA', 'xxx'], 'xxx'],
 [['xxx', 'asd', 'aaaxxy', 'john doe', 'xxxAAA', 'xxx'], 'xx'],
 [['grunt', 'trumpet', 'prune', 'gruesome'], 'run'],
 [['banana', 'apple', 'kiwi', 'peach'], 'a'],
 [['hello', 'world', 'python', 'numpy', 'pandas'], 'py'],
 [[], ''],
 [['abc', 'bcd', 'cbd', 'dbc', 'cda'], 'bc'],
 [['a', 'ab', 'abc', 'abcd', 'abcde', 'bcde', 'cde'], 'cd'],
 [['123', '456', '789', '101112'], '12'],
 [['cat', 'dog', 'elephant', 'rhinoceros', 'seagull'], 'e'],
 [['supercalifragilisticexpialidocious',
   'antidisestablishmentarianism',
   'floccinaucinihilipilification'],
  'ili'],
 [['moon', 'stars', 'sun', 'planets'], 's'],
 [['earth', 'mars', 'jupiter', 'saturn', 'uranus'], 's'],
 [['hello', 'world', 'python', 'numpy', 'pandas', 'numpy'], 'py'],
 [['supercalifragilisticexpialidocious',
   'antidisestablishmentarianism',
   'floccinaucinihilipilification',
   'floccinaucinihilipilificatnion'],
  'ili'],
 [['hello', 'world', 'python', 'numpy', 'pandas'], 'antidisestablishmentarianismpy'],
 [['supercalifragilisticexpialidocious',
   'antidisestablishmentarianism',
   'floccinaucinihilipilification',
   'floccinaucinihilipilificatnion'],
  'ili12'],
 [['supercalifragilisticexpialidocious',
   'antidisesshmentarianism',
   'floccinaucinihilipilification',
   'floccinaucinihilipilificatnion',
   'floccinaucinihilipilificatilinion'],
  'ili'],
 [['supercalifragilisticexpialidocious', 'sun', 'floccinaucinihilipilificatioearthn'], 'ili'],
 [['123', '456', '789', '101112'], '122'],
 [['supercalifragilisticexpialidocious',
   'antidisestablishementarianism',
   'floccinaucinihilipilification'],
  'ili'],
 [['abc', 'bcd', 'cbd', 'dbc', 'cda', 'cfloccinaucinihilipilificatilinionda'], 'bc'],
 [['earth', 'mars', 'jupiter', 'saturn', 'uranus'], 'numpuranusys'],
 [['supercalifragilisticexpialidocious',
   'antidisestablishementarianism',
   'floccinaucinihilipilification',
   'supercalifragilisticexpialidocious'],
  'ili'],
 [['hello', 'world', 'python', 'numpy', 'pandas'], 'antidisestablishmentariasaturnnismpy'],
 [['supercalifragilisticexpialidocious',
   'antidisesshmentarianism',
   'floccinaucinihilipilification',
   'floccinaucinihilipilificatnion',
   'floccinaucinihilipilificatilinion',
   'floccinaucinihilipilifi101112cation'],
  'ili'],
 [['supercalifragilisticexpialidocious',
   'antidisestablishmentarianism',
   'floccinaucinihilipilification',
   'floccinaucinihilipilificatnion'],
  'floccinaucinihilipilificatioearthn'],
 [['hello', 'world', 'python', 'numpy', 's'], 'antidisestablishmentariasaturnnismpy'],
 [['hello', 'world', 'python', 'numpy'], 'antidisestablishmentarianismpy'],
 [['antidisesshmentarianism',
   'floccinaucinihilipilification',
   'floccinaucinihilipilificatnion',
   'floccinaucinihilipilificatilinion'],
  'ili'],
 [['hello', 'world', 'python', 'numpy', 'pandas', 'numpy'], 'antidisestablishmentarianismpy'],
 [['abc', 'bcd', 'cbd', 'dbc', 'cda', 'cfloccinaucinihilipilificatilinionda', 'dcbd'], 'bbc'],
 [['abc',
   'bcd',
   'cbd',
   'dbc',
   'cda',
   'cfloccinaucinihilipilificatilinionda',
   'dcbd',
   'cfloaccinaucinihilipilificatilinionda'],
  'bbc'],
 [['123', '456', '789', '101112', '456'], '12'],
 [['Washington', 'DC', 'New York City', 'Boston', 'Los Angeles', 'San Francisco', 'Miami'], 'an'],
 [['The quick brown fox jumps over the lazy dog',
   'Pack my box with five dozen liquor jugs',
   'How vexingly quick daft zebras jump',
   'Jackdaws love my big sphinx of quartz'],
  'ox'],
 [['The cat in the hat', 'Green eggs and ham', 'One fish two fish', 'Red fish blue fish'], 'fish'],
 [['The Shawshank Redemption',
   'The Godfather',
   'The Dark Knight',
   'The Lord of the Rings',
   'Star Wars',
   'Inception',
   'Forrest Gump'],
  'he'],
 [['We the people of the United States of America, in order to form a more perfect union, '
   'establish justice, insure domestic tranquility, provide for the common defense, promote the '
   'general welfare, and secure the blessings of liberty to ourselves and our posterity, do ordain '
   'and establish this Constitution for the United States of America.',
   'To be or not to be, that is the question.',
   'It is a truth universally acknowledged, that a single man in possession of a good fortune, '
   'must be in want of a wife.',
   'I have a dream that one day this nation will rise up and live out the true meaning of its '
   'creed: "We hold these truths to be self-evident, that all men are created equal."',
   'Four score and seven years ago our fathers brought forth on this continent, a new nation, '
   'conceived in Liberty, and dedicated to the proposition that all men are created equal.'],
  'equal.'],
 [['abcdefg'], ''],
 [['abc(d)e', 'ba%cd', 'cde', 'array', '12345'], '(d)'],
 [['wsrefgtrh', 'zxyvtru', 'asxwaqzx', 'kjbncxz'], 'tr'],
 [['The Shawshank Redemption',
   ' The Godfather ',
   'The Dark Knight',
   '  The Lord of the Rings   ',
   '   Star Wars',
   ' Inception     ',
   'Forrest Gump'],
  ' '],
 [['The Shawshank Redemption',
   ' The Godfather ',
   'The Dark Knight',
   '  The Lord of the Rings   ',
   '   Star Wars',
   ' Inception     ',
   'Forrest Gump',
   ' Inception     '],
  ' '],
 [['Washington',
   'DC',
   'New York City',
   'Boston',
   'Los Angeles',
   'San Francisco',
   'Miami',
   'Washington'],
  'an'],
 [['Washington', 'DC', 'New York City', 'Boston', 'Los Angeles', 'San Francisco', 'Miami'], 'York'],
 [['The quick brown fox jumps over the lazy dog',
   'Pack my box with five dozen liquor jugs',
   'How vexingly quick daft zebras jump',
   'Jackdaws love my big sphinx of quartz'],
  'oConstitutionx'],
 [['The quick brown fox jumps over the lazy dog',
   'Pack my box with five dozen liquor jugs',
   'Jackdaws love my big sphinx of quartz'],
  'created'],
 [['Pack my box with five dozen liquor jugs', 'Jackdaws love my big sphinx of quartz'], 'creeated'],
 [['abcdefg'], 'universally'],
 [['The quick brown fox jumps over the lazy dog',
   'Pack my box with five dozen liquor jugs',
   'Jackdaws love my big sphinx of quartz'],
  'creataed'],
 [['We the people of the United States of America, in order to form a more perfect union, '
   'establish justice, insure domestic tranquility, provide for the common defense, promote the '
   'general welfare, and secure the blessings of liberty to ourselves and our posterity, do ordain '
   'and establish this Constitution for the United States of America.',
   'To be or not to be, that is the question.',
   'It is a truth universally acknowledged, that a single man in possession of a good fortune, '
   'must be in want of a wife.',
   'I have a dream that one day this nation will rise up and live out the true meaning of its '
   'creed: "We hold these truths to be self-evident, that all men are created equal."',
   'Four score and seven years ago our fathers brought forth on this continent, a new nation, '
   'conceived in Liberty, and dedicated to the proposition that all men are created equal.',
   'I have a dream that one day this nation will rise up and live out the true meaning of its '
   'creed: "We hold these truths to be self-evident, that all men are created equal."'],
  'equal.'],
 [['We the people of the United States of America, in order to form a more perfect union, '
   'establish justice, insure domestic tranquility, provide for the common defense, promote the '
   'general welfare, and secure the blessings of liberty to ourselves and our posterity, do ordain '
   'and establish this Constitution for the United States of America.',
   'To be or not to be, that is the question.',
   'It is a truth universally acknowledged, that a single man in possession of a good fortune, '
   'must be in want of a wife.',
   'I have a dream that one day this nation will rise up and live out the true meaning of its '
   'creed: "We hold these truths to be self-evident, that all men are created equal."',
   'Four score and seven years ago our fathers brought forth on this continent, a new nation, '
   'conceived in Liberty, and dedicated to the proposition that all men are created equal.'],
  'ordain'],
 [['abcdefg', 'abcdefg'], 'universally'],
 [['Washington', 'New York City', 'Boston', 'Los Angeles', 'San Francisco', 'Miami', 'Washington'],
  'nan'],
 [['Washington', 'Boston', 'Los Angeles', 'San Francisco', 'Miami', 'Washington'], 'nan'],
 [['Washington',
   'The cat in the hat',
   'New York City',
   'Boston',
   'Los Angeles',
   'San Francisco',
   'Miami',
   'Washington'],
  'nation,'],
 [['Washington', 'New York City', 'Boston', 'Los Angeles', 'San Francisco', 'Miami', 'Washington'],
  'nabc(d)e'],
 [['abcdeits'], 'universally'],
 [['We the people of the United States of America, in order to form a more perfect union, '
   'establish justice, insure domestic tranquility, provide for the common defense, promote the '
   'general welfare, and secure the blessings of liberty to ourselves and our posterity, do ordain '
   'and establish this Constitution for the United States of America.',
   'To be or not to be, that is the question.',
   'It is a truth universally acknowledged, that a single man in possession of a good fortune, '
   'must be in want of a wife.',
   'I have a dream that one day this nation will rise up and live out the true meaning of its '
   'creed: "We hold these truths to be self-evident, that all men are created equal."',
   'Four score and seven years ago our fathers brought forth on this continent, a new nation, '
   'conceived in Liberty, and dedicated to the proposition that all men are created equal.'],
  'equ'],
 [['abcdefg', 'abcdefg'], 'upromoteniversally'],
 [['The cat in the hat', 'Green eggs and ham', 'One fish two fish', 'Red fish blue fish'], 'ffis'],
 [['Washington', 'New York City', 'Los Angeles', 'San Francisco', 'Miami', 'Washington'],
  'nabc(d)e'],
 [['abcdefg', 'abcdefg', 'abcdefg'], 'universally'],
 [['The quick brown fox jumps over the lazy dog',
   'Pack my box with five dozen liquor jugs',
   'How vexingly quick daft zebras jump',
   'Jackdaws love my big sphinx of quartz'],
  'oConstituti'],
 [['Washington',
   'New York Ciity',
   'The cat in the hat',
   'New York City',
   'Boston',
   'Los Angeles',
   'Miami',
   'Washington'],
  'nation,'],
 [['Pack my box with five dozen liqugor jugs',
   'The quick brown fox jumps ove  zy dog',
   'The quick brown fox jumps over the lazy dog',
   'Pack my box with five dozen liquor jugs',
   'Jackdaws love my big sphinx of quartz'],
  'created'],
 [['Washington', 'New York City', 'Boston', 'Los Angeles', 'San Francisco', 'Miami', 'Washington'],
  'want'],
 [['The quick brown fox jumps over the lazy dog',
   'Pack my box with five dozen liquor jugs',
   'Pack my box with five dozen lisevenquor jugs',
   'How vexingly quick daft zebras jump',
   'Jackdaws love my big sphinx of quartz'],
  'ox'],
 [['The q uick brown fox jumps over the lazy dog',
   'Pack my box with five dozen liquor jugs',
   'How vexingly quick daft zebras jump',
   'Jackdaws love my big sphinx of quartz'],
  'oConstitutionx'],
 [['The quick brown fox jumps over the lazy dog',
   'San Francisco',
   'Pack my box with five dozen liquor jugs',
   'How vexingly quick daft zebras jump',
   'Jackdaws love my big sphinx of quartz'],
  'oConstitutionx'],
 [[],
  'It is a truth universally acknowledged, that a single man in possession of a good fortune, must '
  'be in want of a wife.'],
 [['The quick brown fox jumps over the lazy dog',
   'Pack my box with five dozen liquor jugs',
   'Pack my box with five dozen lisevenquor jugs',
   'forth',
   'Jackdaws love my big sphinx of quartz'],
  'ox'],
 [['Washington', 'New York City', 'Los Angeles', 'San Francisco', 'zebras', 'Washington'],
  'nabc(d)e'],
 [['We the people of the United States of America, in order to form a more perfect union, '
   'establish justice, insure domestic tranquility, provide for the common defense, promote the '
   'general welfare, and secure the blessings of liberty to ourselves and our posterity, do ordain '
   'and establish this Constitution for the United States of America.',
   'To be or not to be, that is the question.',
   'It is a truth universally acknowledged, that a single man in possession of a good fortune, '
   'must be in want of a wife.',
   'I have a dream that one day this nation will rise up and live out the true meaning of its '
   'creed: "We hold these truths to be self-evident, that all men are created equal."',
   'Four score and seven years ago our fathers brought forth on this continent, a new nation, '
   'conceived in Liberty, and dedicated to the proposition that all men are created equal.',
   'I have a dream that one day this nation will rise up and live out the true meaning of its '
   'creed: "We hold these truths to be self-evident, that all men are created equal."'],
  'eaqual.'],
 [[], 'universally'],
 [['Washington',
   'New York City',
   'Boston',
   'Los Angeles',
   'San Francisco',
   'Miami',
   'Washington',
   'Miami'],
  'want'],
 [['Washington', 'New York City', 'Boston', 'Los Angeles', 'San Francisco', 'Miami', 'Washington'],
  'New York Citywant'],
 [[], 'Star'],
 [['The Shawshank Redemption',
   'The Godfather',
   'The Dark Knight',
   'The Lord of the Rings',
   'Star Wars',
   'Inception',
   'universally'],
  'he'],
 [['Washington',
   'cRedemptionread',
   'New York City',
   'Boston',
   'Los Angeles',
   'San Francisco',
   'Miami',
   'Washington'],
  'nation,'],
 [['abcgdefg', 'aasxwaqzxbcdefg', 'want', 'abcdefg', 'abcdefg', 'abcdefg'], 'universally'],
 [['Washington', 'New York City', 'Boston', 'Los Angeles', 'San Francisco', 'Miami', 'Washington'],
  'New York Citywan'],
 [['Washington',
   'New York City',
   'nWashington',
   'Los Angeles',
   'San Francisco',
   'zebras',
   'Washington'],
  'nabc(d)e'],
 [['abcdeits'], 'fortune,'],
 [['B"Weoston',
   'Washington',
   'DC',
   'New York City',
   'Boston',
   'Los Angeles',
   'San Francisco',
   'Miami'],
  'York'],
 [['abcgdefg', 'aasxwaqzxbcdefg', 'want', 'abcdefg', 'abcdefg', 'abcdefg'], 'box'],
 [['peoplbige', 'abcdefg', 'abcdefg'], 'universally'],
 [['We the people of the United States of America, in order to form a more perfect union, '
   'establish justice, insure domestic tranquility, provide for the common defense, promote the '
   'general welfare, and secure the blessings of liberty to ourselves and our posterity, do ordain '
   'and establish this Constitution for the United States of America.',
   'To be or not to be, that is the question.',
   'It is a truth universally acknowledged, that a single man in possession of a good fortune, '
   'must be in want of a wife.',
   'I have a dream that one day this nation will rise up and live out the true meaning of its '
   'creed: "We hold these truths to be self-evident, that all men are created equal."',
   'Four score and seven years ago our fathers brought forth on this continent, a new nation, '
   'conceived in Liberty, and dedicated to the proposition that all men are created equal.'],
  'for'],
 [['Pack my box with five dozen liqugor jugs',
   'The quick brown fkjbncxzox jumps ove  zy dog',
   'The quick brown fox jumps over the lazy dog',
   'Pack my box with five dozen liquor jugs',
   'Jackdaws love my big sphinx of quartz',
   'Jackdaws love my big sphinx of quartz'],
  'createdd'],
 [['We the people of the United States of America, in order to form a more perfect union, '
   'establish justice, insure domestic tranquility, provide for the common defense, promote the '
   'general welfare, and secure the blessings of liberty to ourselves and our posterity, do ordain '
   'and establish this Constitution for the United States of America.',
   'To be or not to be, that is the question.',
   'It is a truth universally acknowledged, that a single man in possession of a good fortune, '
   'must be in want of a wife.',
   'I have a dream that one day this nation will rise up and live out the true meaning of its '
   'creed: "We hold these truths to be self-evident, that all men are created equal."',
   'Four score and seven years ago our fathers brought forth on this continent, a new nation, '
   'conceived in Liberty, and dedicated to the proposition that all men are created equal.'],
  'Citywan'],
 [['The Shawshank Redemption',
   ' The Godfather ',
   'The Dark Knight',
   '  The Lord of the Rings   ',
   '   Star Wars',
   ' Inception     ',
   'Forrest Gump'],
  'nation'],
 [['Washington', 'DC', 'New York City', 'ton', 'Boston', 'Los Angeles', 'San Francisco', 'Miami'],
  'York'],
 [['The quick brown fox jumps over the lazy dog',
   'Pack my box with five dozen liquor jugs',
   'Jackdaws love my big sphinx of quartz'],
  'tthese'],
 [['The quick brown fox jumps over the lazy dog',
   'San Francisco',
   'Pack my box with five dozen liquor jugs',
   'How vexingly quick daft zebras jump',
   'Jackdaws love my big sphinx of quartz'],
  'oConstitStar Warsutionx'],
 [['Washington', 'New York City', 'Los Angeles', 'San Francisco', 'Miami', 'Washington'],
  'nab(((The Dark Knightdthese)cc(d)e'],
 [['Washington',
   'New York City',
   'San Francisco',
   'Miami',
   'New York Cicreateddty',
   'Washington',
   'New York Cicreateddty'],
  'nabc(d)e'],
 [['Washington',
   'MMiami',
   'New York City',
   'San Francisco',
   'Miami',
   'New York Cicreateddty',
   'Washington',
   'New York Cicreateddty'],
  'nabc(d)e'],
 [['an', 'abcdeits'], 'universally'],
 [['The Shawshank Redemption',
   ' The Godfather ',
   'The Dark Knight',
   '  The Lord of the Rings   ',
   '   Star Wars',
   ' Inception     ',
   'Forrest Gump'],
  ' l.'],
 [['We the people of the United States of America, in order to form a more perfect union, '
   'establish justice, insure domestic tranquility, provide for the common defense, promote the '
   'general welfare, and secure the blessings of liberty to ourselves and our posterity, do ordain '
   'and establish this Constitution for the United States oef America.',
   'To be or not to be, that is the question.',
   'It is a truth universally acknowledged, that a single man in possession of a good fortune, '
   'must be in want of a wife.',
   'I have a dream that one day this nation will rise up and live out the true meaning of its '
   'creed: "We hold these truths to be self-evident, that all men are created equal."',
   'Four score and seven years ago our fathers brought forth on this continent, a new nation, '
   'conceived in Liberty, and dedicated to the proposition that all men are created equal.'],
  'City'],
 [['th'], '(((The Dark Knightdtmeaninghese)'],
 [['abcdefg', 'abcdefg', 'abcdefg'], 'univerhavely'],
 [['We the people of the United States of America, in order to form a more perfect union, '
   'establish justice, insure domestic tranquility, provide for the common defense, promote the '
   'general welfare, and secure the blessings of liberty to ourselves and our posterity, do ordain '
   'and establish this Constitution for the United States of America.',
   'To be or not to be, that is the question.',
   'It is a truth universally acknowledged, that a single man in possession of a good fortune, '
   'must be in want of a wife.',
   'I have a dream that one day this nation will rise up and live out the true meaning of its '
   'creed: "We hold these truths to be self-evident, that all men are created equal."',
   'Four score and seven years ago our fathers brought forth on this continent, a new nation, '
   'conceived in Liberty, and dedicated to the proposition that all men are created equal.',
   'I have a dream that one day this nation will rise up and live out the true meaning of its '
   'creed: "We hold these truths to be self-evident, that all men are created equal."'],
  'Star Wars'],
 [['daft', 'UEZ', '(((The Dark Knightdthese)', 'of', 'New York Ciitypcerfefct'],
  'RRed fish blue fish'],
 [['Pack my box with five dozen liqugor jugs',
   'The quick brown fkjbncxzox jumps ove  zy dog',
   'The quick brown fox jumps over the lazy dog',
   'Pack my box with five dozen liquor jugs',
   'Jackdaws love my big sphinx of quartz'],
  'The quick b over the lazy dog'],
 [['The quick brown fox jumps ove  zy dog',
   'The quick brown fox jumps over the lazy dog',
   'Pack my box with five dozen liquor jugs',
   'Jackdaws love my big sphinx of quartz',
   'The quick brown fox jumps ove  zy dog'],
  'oxx'],
 [['We the people of the United States of America, in order to form a more perfect union, '
   'establish justice, insure domestic tranquility, provide for the common defense, promote the '
   'general welfare, and secure the blessings of liberty to ourselves and our posterity, do ordain '
   'and establish this Constitution for the United States of America.',
   'To be or not to be, that is the question.',
   'It is a truth universally acknowledged, that a single man in possession of a good fortune, '
   'must be in want of a wife.',
   'I have a dream that one day this nation will rise up and live out the true meaning of its '
   'creed: "We hold these truths to be self-evident, that all men are created equal."',
   'Four score and seven years ago our fathers brought forth on this continent, a new nation, '
   'conceived in Liberty, and dedicated to the proposition that all men are created equal.',
   'To be or not to be, that is the question.'],
  'ordain'],
 [['Washington',
   'New York City',
   'Boston',
   'Los Angeles',
   'San Francisco',
   'Miami',
   'Washington',
   'Miami'],
  'daft'],
 [['Pack my box with five dozen liqugor jugs',
   'The quick brown fox jumps ove  zy dog',
   'The quick brown fox jumps over the lazy dog',
   'Pack my box with five dozen liquor jugs',
   'Redemption'],
  'created'],
 [['Washington', 'Boston', 'Los Angeles', 'San Francisco', 'Miami', 'Washington'], 'nann'],
 [['The quick brown fox jumps over the lazy dog',
   'Pack my box with five dozen liquor jugs',
   'Jackdaws love my big sphinx of quartz',
   'Pack my box with five dozen liquor jugs'],
  'createt'],
 [['Washington',
   'MMiami',
   'New York City',
   'San Francisco',
   'Miami',
   'New York Cicreateddty',
   'Washington',
   'New York Cicreateddty'],
  'nabc)e'],
 [['The Shawshank Redemption',
   'The Godfather',
   'The Lord of the Rings',
   'Star Wars',
   'Inception',
   'Forrest Gump'],
  'he'],
 [['The quick brown fox jumps over the lazy dog',
   'Pack my box with five dozen liquor jugs',
   'Pack my box with five dozen lisevenquor jugs',
   'How vexingly quick daft zebras jump',
   'Jackdaws love my big sphinx of quartz'],
  'quiickox'],
 [['The quick brown fox jumps over the lazy dog',
   'Pack my box with five dozen liquor jugs',
   'Jackdaws love my big sphinx of quartz'],
  'propmtr'],
 [['The quick brown fox jumps over tPacFour score and seven years ago our fathers brought forth on '
   'this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all '
   'men are crzyeated equal.he lazy dog',
   'San Francisco',
   'Pack my box with five dozen liquor jugs',
   'How vexingly quick daft zebras jump',
   'Jackdaws love my big sphinx of quartz'],
  'oConstittutionx'],
 [['Thee quick brown fox jumps ove  zy dog',
   'The quick brown fox jumps over the lazy dog',
   'Pack my box with five dozen liquor jugs',
   'Jackdaws love my big sphinx of quartz',
   'The quick brown fox jumps ove  zy dog'],
  'oxxNew York Citywan'],
 [[], 'abc'],
 [[], 'substring'],
 [['', '', ''], 'substring'],
 [['substring', 'substring', 'substring'], 'substring'],
 [['string', 'bingo', 'frost', 'parka'], 'substring'],
 [['', '', ''], ''],
 [['', 'a', '', 'b'], ''],
 [[''], ''],
 [['abc', 'bcd', 'cde', 'def'], 'a'],
 [['The Godfather',
   'The Dark Knight',
   'The Lord of the Rings',
   'Star Wars',
   'posterity,',
   'Forrest Gump'],
  'he'],
 [['abcdefg'], 'form'],
 [[], 'Green'],
 [['The quick brown fox jumps over the lazy dog',
   'Pack my box with five dozen liquor jugs',
   'How vexingly quick daft zebras jump',
   'Jackdaws love my big sphinx of quartz'],
  'tranquility,ox'],
 [['abcdefg'], 'fom'],
 [['Washington', 'DC', 'New York City', 'Boston', 'Los Angeles', 'San Francisco', 'Miami'],
  'liberty'],
 [['The Godfather',
   'The Dark Knight',
   'The Lord of the Rings',
   'union,',
   'posterity,',
   'Forrest Gump',
   'union,'],
  'h'],
 [['abcdefg', 'abcdefg'], 'm'],
 [['fom', 'abcdefg'], 'fom'],
 [['We the people of the United States of America, in order to form a more perfect union, '
   'establish justice, insure domestic tranquility, provide for the common defense, promote the '
   'general welfare, and secure the blessings of liberty to ourselves and our posterity, do ordain '
   'and establish this Constitution for the United States of America.',
   'To be or not to be, that is the question.',
   'It is a truth universally acknowledged, that a single man in possession of a good fortune, '
   'must be in want of a wife.',
   'I have a dream that one day this nation will rise up and live out the true meaning of its '
   'creed: "We hold these truths to be self-evident, that all men are created equal."',
   'Four score and seven years ago our fathers brought forth on this continent, a new nation, '
   'conceived in Liberty, and dedicated to the proposition that all men are created equal.'],
  'eqal.'],
 [['abcdbefg'], 'form'],
 [['abbcdefg', 'fom', 'abcdefg'], 'fom'],
 [['The Shawshank Redemption',
   'The Godfather',
   'The Dark Knight',
   'Star Wars',
   'Inception',
   'Forrest Gump'],
  'he'],
 [['Washington', 'DC', 'New York City', 'Boston', 'Los Angeles', 'San Francisco', 'Miami'],
  'libertequal.y'],
 [['The Shawshank Redemption',
   ' The Godfather ',
   'The Dark Knight',
   '  The Lord of the Rings   ',
   '   Star Wars',
   ' Inception     ',
   'Forrest Gump'],
  'Angeles'],
 [['Washington',
   'DC',
   'New York City',
   'Boston',
   'Los Angeles',
   'San Francisco',
   'Miami',
   'New York City'],
  'an'],
 [['The Godfather',
   'The Dark Knight',
   'The Lord of the Rings',
   'Star Wars',
   'posterity,',
   'Forrest Gump'],
  'h'],
 [['Washington', 'DC', 'New York City', 'Boston', 'San Francisco', 'Miami'], 'libertequal.y'],
 [['abcdefg'], 'fofm'],
 [['Washington',
   'DC',
   'New York City',
   'Boston',
   'Los Angeles',
   'San Francisco',
   'Miami',
   'New York City'],
  'aan'],
 [['The Shawshank Redemption',
   'The Godfather',
   'The Dark Knight',
   'Star Wars',
   'Inception',
   'Forrest Gump'],
  'hhe'],
 [['abbcdefg', 'fom', 'abcdefg', 'abbcdefg'], 'fom'],
 [['abcdefg', 'abcdefg'], 'To be or not to be, that is the question.'],
 [['The Godfatosacknowlledged,phinxxher',
   'The Dark Knight',
   'The Lord of the Rings',
   'union,',
   'tranquility,oxunion,',
   'posterity,',
   'Forrest Gump',
   'union,'],
  'h'],
 [['osafortune,cknowlledged,p', 'abcdefg', 'abcdefg'], 'fom'],
 [['The Shawshank Redemption',
   'The Godfather',
   'justice,The Dark Knight',
   'The Lord of the Rings',
   'and',
   'Inception',
   'Forrest Gump'],
  'he'],
 [['abc(d)e', 'ba%cd', 'cde', 'array', '12345'], 'dozen'],
 [['The Godfather',
   'The Dark Knight',
   'DCt',
   'The Lord of the Rings',
   'union,',
   'posterity,',
   'Forrest Gump',
   'union,'],
  'h'],
 [['osafortune,cknowlledged,p', 'abcdefg'], 'fom'],
 [['wsrefgtrh', 'zxyvtru', 'asxwaqzx', 'zxyvtConstitutionru', 'kjbncxz'], 'tr'],
 [['kQEHdzw', 'for', 'asxwaqzx', '  The Lord of the Rings   ', 'Mi', 'its', 'kZWuN'], 'Green'],
 [['abc(d)e', 'ba%cd', 'cde', 'array', '12345', '12345'], 'Saabc(d)en'],
 [['abc(d)e', 'ba%cd', 'cde', 'array', 'dog'], 'doquartuzzen'],
 [['The Shawshank Redemption',
   'The Godfather',
   'justice,The Dark Knight',
   'The Lord of the Rings',
   'and',
   'Inception',
   'Forrest Gump'],
  'hhate'],
 [['Washinestablishon',
   'DC',
   'New York City',
   'Boston',
   'Los Angeles',
   'San Francisco',
   'Miami',
   'New York City'],
  'an'],
 [['abcdefg'], 'rtr'],
 [['The Dark Knight', 'The Lord of the Rings', 'union,', 'posterity,', 'Forrest Gump', 'union,'],
  'h'],
 [['The Godfatosacknowlledged,phinxxher',
   'The Dark Knight',
   'The Lord of the Rings',
   'union,',
   'tranquility,oxunion,',
   'posterity,',
   'Forrest Gump',
   'union,'],
  'ourselvesh'],
 [['Washinestablishon',
   'DC',
   'New York City',
   'Boston',
   'Los Angeles',
   'San Francisco',
   'Miami',
   'New York City'],
  'aan'],
 [['We the people of the United States of America, in order to form a more perfect union, '
   'establish justice, insure domestic tranquility, provide for the common defense, promote the '
   'general welfare, and secure the blessings of liberty to ourselves and our posterity, do ordain '
   'and establish this Constitution for the United States of America.',
   'To be or not to be, that is the question.',
   'It is a truth universally acknowledged, that a single man in possession of a good fortune, '
   'must be in want of a wife.',
   'I have a dream that one day this nation will rise up and live out the true meaning of its '
   'creed: "We hold these truths to be self-evident, that all men are created equal."',
   'Four score and seven years ago our fathers brought forth on this continent, a new nation, '
   'conceived in Liberty, and dedicated to the proposition that all men are created equal.'],
  'eqal.osacknsowlledged,phinxx'],
 [['Washinestablishon',
   'DC',
   'New York City',
   'Boston',
   'Los Angeles',
   'San Francisco',
   'Miami',
   'DCC',
   'New York City'],
  'an'],
 [['fI have a dream that one day this nation will rise up and live out the true meaning of its '
   'creed: "We hold these truths to be self-evident, that all men are created equal."om',
   'abcdefg'],
  'fom'],
 [['We the people of the United States of America, in order to form a more perfect union, '
   'establish justice, insure domestic tranquility, provide for the common defense, promote the '
   'general welfare, and secure the blessings of liberty to ourselves and our posterity, do ordain '
   'and establish this Constitution for the United States of America.',
   'To be or not to be, that is the question.',
   'I have a dream that one day this nation will rise up and live out the true meaning of its '
   'creed: "We hold these truths to be self-evident, that all men are created equal."',
   'Four score and seven years ago our fathers brought forth on this continent, a new nation, '
   'conceived in Liberty, and dedicated to the proposition that all men are created equal.'],
  'eqal.'],
 [['Washington', 'DC', 'New York City', 'Boston', 'Los Angeles', 'San Francisco', 'Miami'], 'nan'],
 [['Washinestablishon',
   'DC',
   'New York City',
   'Boston',
   'Los Angeles',
   'San Francisco',
   'Miami',
   'DCC',
   'New York City'],
  'Guoxxplibertequal.yan'],
 [[], 'form'],
 [['Washington', 'DC', 'New York City', 'Boston', 'Los Angeles', 'San Francisco', 'Miami'],
  'tranquility,oxunion,doquartuzzen'],
 [['Washington', 'DC', 'New York CitYy', 'Boston', 'Los Angeles', 'San Francisco', 'Miami'],
  'liberty'],
 [['abcdefg', 'abcdefg'], 'To be or not to be,  that is the question.'],
 [['The Godfather',
   'The Dark Knight',
   'The Lord of the Rings',
   'union,',
   'pyeathesersrity,',
   'Forrest Gump',
   'union,'],
  'h'],
 [['The Shawshank Redemption',
   'The Godfather',
   'justice,The Dark Knight',
   'The Lord of the Rings',
   'and',
   'Inception',
   'Forrest Gump'],
  'hhatethThe'],
 [['The Shawshank Redemption',
   'To be or not to be, that is the quesetion. Godfather',
   'The Godfather',
   'justice,The Dark Knight',
   'The Lord of the Rings',
   'and',
   'Inception',
   'Forrest Gump'],
  'hhatetmyhThe'],
 [['osafortune,cknowlledged,p', 'abcdefg', 'orm', 'abcdefg'], 'fom'],
 [['Washington', 'DC', 'New York City', 'Boston', 'Los Angeles', 'San Francisco', 'Miami'],
  'tranquility,oxunion,doquartuzLoszen']]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-rk+JCYsA4U`P&EV2|;D0~W@E+PY;s#sqakhPXf>b}Zm%+Qpfc-r8SZ^($5nCXYcFB6IG`sbhi{VV<9>(}4E{N-'
    b'PN{>LvtqF?^?x2UMCHI5Fi@S#^1<v7$)RY_^qgkLDlOXK9JGlTb%^mX-)FTZ~I<&Q8!d89S{di$(-+(>Gq=Aw0tGnO55vn07^C-'
    b'>Us(`(%8W7dZmX4x`LcFf53@)I<(uDa@C*q^t;R){vc&!tVfq<ePdfyoaulko>GqkXgCC_WZ)?9kTbcdTixrS~{Zb-MS8RNui@w5'
    b'CLVn4vLeXK@R>*W*6?u)yR+5aJfvs}PK8El*sWrYz;VhvaPe^v2_y=uFaRQa_E9mQ(ONgLepZp6u;1hRg}KU~$Hp(-'
    b'EZQXNq4_sclnnNf^a;rM*@2Ox{G!+m?peID3vpWlHx&rY3UUNcfFC&W9N(!taPtNfJ3)k!wvo$l=)bHCWW2=};{?sUkhP_Tgb`*S'
    b'DZ#%prrP8ae_o4S3!2a<^_O4Fq+*W*8-'
    b'FImuL{%59ZxX`d<HBpnkqIo9rbtThhrjuzo#8~K$H2VK$kjytcxv&DNd@`Y<YgPJs*bnXgWhImXbya=R)7atgs2#x6rorGRNhH{G'
    b'Hwt1OpuMacFhO_i^DZwpn2GYrEMRlW(QgRQDcJ$vBfC9~sd$+2iqsTwKId_P`Yl;r<f%NmWaO4wxa?U998Jt5yO}%l{=aJ9{eFJD'
    b'%`eA0c@y^9)1qXE8{4NK=mZ7-'
    b'F5YH$5%~g_0c7T~VmsrjfK%9M;!M%3ut0#nkYsA|rXCulxpIYD}yW#FdSYynPtAskmxaXiJ>a|_`GBDIo4!tYpvd7Hs&PFZK12ND'
    b'!vl2BLC_9p;BT@LecP;YgS083_-_4wf-ilyf$RywbZVMH|7YM^kec0Rq)=TOujLLGlGm`Y$pkCC)FCvN;1$9lgGtirZjgBl(0pR7'
    b'J_iHqYZkI_UC>f1+hU@GG34njxb;pZS923ly;sNs7_LX$jYW&O#nC@i^wkf`tbU8z5oy1+HgQ%8DewSc)ks03zaTt)qw;AkmHb!s'
    b'Ixg2**x;$K54gdv+fvng}L$}UDWXpc!+`MSqb)Q-'
    b'sb_tB6zH9EJJ0i<LUk3tWJW?rrU!+`P4G<0d1l*x!f<9^MWEJrk@DQK1xyrz9c{CF>Gw3$g0UX6Wx6sC$q2T1KUbw;f#FVg{F)?l'
    b'7y(1zFiCl0R!!|JMzuwar$_OP!OSIa|K>&0%hRwYnW)=g)Ajn)0RuTvu(<NP2^CKe>8oKIi&Vde!<M?EUK}YSTRo^6}9Sj`6J|Mv'
    b'k8HWAYis>l4w%UOVg|Y-R*9le(FKgQq3F;icaD1{K(9O@R2H`Ut@-@8!We*(~xQPhP-jjq(y-'
    b'nzucLia(9XU+@OfjKr(A^0MXcH{SXPr|OT^PYfP+mc9j`$_ivf$Ac$QN+2f~4nXZa~YnDu`Meqt`J#Fti|84gD2<7BsRzEoc|u1}'
    b'eS)6~xypL0MydDvJL4v5ATYAqCh0mLY-yiSES)X~JWZvdIL&GWi^c4O3($wCyKt^)BQCDxEJtaOMEUp;83G*Y+aYNcV=v_$L$E4+'
    b'3~u0XkhnHpOeZ81!4~=;Ke~KcTvAQfUh#f%~q5?c*G6!~J=0ha3T*7P`|y;{3>b^L?3tzJTb=BFIswle-'
    b';PopdZ@mlBf_iVGm9M?!!+7FMppPNW*ZyV|!UF#z2@1hB|n5LLr--RVcbT$sF=EjsqzXzT%iLg6mZ2~Z1+Qq;Rrzc({4qV#u)-'
    b')8<7GgzCCVAFtP6M6<ru|ViEc6;<AC<+tBmtUR(+woSZh4y=d!s&!$dgtcn%*~Hk@YksHcZz?5XInp@F0Sole#YI9c092iW7U9~9'
    b'2}fv^MpQj4S%+h=RSljC**nHh9>NH!QYF}+sxa{Pi^MCK>uFMoKZ{d2F>1+eH&^9)vR~x)RmRpbOvW(1J0hemg{5K#x#=kR$D)*n'
    b'c6hydDl0egA%xuR~pgystxFQ8JK;98ER=d^t$ApA`kFk&&G@2PqC!QsOZIGC2p1uCW%-'
    b'ctHC*Nvh%Kdo@RT`jA|^6BQC8=XMMi)7%XFB`{3NxL65S#STt{D4tlU~PJ^~s+3<5hCc?wGQ&?!$x7QVo+v4IBS6SL;>AKH*%w0X'
    b'@`0j;8MMZt>)PUm%P_k^qo^kBc%s?JMq{}CtJFHF(B*F5m?g`%9=VB}N)I)Pbmw-vj*82K-'
    b'*!O3Ou|?56FfVRbye1(ytWx(;XYrgV*`%S#-ZxvYd5veQzV6QfnZ4g&_|2X|eqWVRHAhQQX<bZ-'
    b'^&F_0yIUI*{T}jsUX^Spe)RL$LmmVUxtG`Squ*zxUK7-'
    b'=TecI3J<t1je18r*jOXQ%nV1mW=Y$5SrnC+&p3n0P@;RSF8vI@6=0$JI-'
    b'hA_W>Ec&C6^Ny{DjzQxW1s6eDFc%jrE~486RMJSj*e9rhT8CTK}inod-K&KdSRAJ7&9NCLY>sueCIetkOok-O_$0swlTnqApnpvF'
    b'S5d1fAuk*?+XksdddHW=Kq~UUv;K!<aA4dV1(oyt!S=R<rw$Q80)SOA6LK<vj$|V?IRcJ^=hIa^IfUms#0$=KbaZA>=OnV$F3Tf('
    b'dRiEYg>uQhv3J0uxNUVCE_`bofw)EW4+Hf?`P@%-OTyxe*l@v3w{'
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
    candidate = filter_by_substring  # noqa: F405
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
