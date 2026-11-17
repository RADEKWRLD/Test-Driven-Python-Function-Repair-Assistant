import base64
import copy
import hashlib
import math

import pickle
import zlib

import numpy as np

from solution import *  # noqa: F403

INPUTS = [['Hello world'],
 ['Is the sky blue?'],
 ['I love It !'],
 ['bIt'],
 ['I feel good today. I will be productive. will kill It'],
 ['You and I are going for a walk'],
 ['I am very happy today. I love spending time with my friends.'],
 ['I want to eat pizza for dinner. What do you think, should we order pizza?'],
 ['I enjoy reading books. They help me learn new things.'],
 ['I forgot my phone in the car. Oh no, now I have to go back and get it.'],
 ['In the morning, I like to have a cup of coffee to start my day off right. How about you?'],
 ['Have you ever gone skydiving before? I did it once and it was amazing.'],
 ['I think I want to try cooking something new for dinner tonight. Do you have any favorite '
  'recipes?'],
 ['The movie we saw last night was really good, but I think I would have enjoyed it more if I had '
  'some popcorn. Do you like popcorn?'],
 ['I love to read books. What about you?'],
 ['I have a lot of work to do today. I wish I could take a nap instead.'],
 ['The movie we saw last night was really good, but I think I would have enjoyed it more if I had '
  'some popicorn. Do you like popcorn?'],
 ['I am very happy today. I love s'],
 ['The movie we saw last night was really good, but I think I would have enjoyed it more if I had '
  'some popicorn. oDo you like popcorn?'],
 ['I forgot my phone in the car. Oh no, now I have to The movie we saw last night was really good, '
  'but I think I would have enjoyed it more if Ip had some popcorn. Do you like popcorn?and get '
  'it.'],
 ['I forgot my phone in the car. Oh no, now I have to The movie we saw last night was really good, '
  'but I think I would have enjoyed it more if Ip had some popcorn. Do you like popcorn?and get '
  'rit.'],
 ['I am very happy today. I love spending time with my friiends.'],
 ['The movie we saw last night was really good, but I think I would have enjoI am very happy '
  'today. I love spending time with my friiends.yed it more if I had some popicorn. Do you like '
  'popcorn?'],
 ['In the morning, I lI forgot my phone in the car. Oh no, now I have to go back and get it.ike to '
  'have a cup of coffee to start my day off right. How about you?'],
 ['The movie we saw last night was really good, but?'],
 ['I want to eat pizza for dinn. What do you think, s'],
 ['I have a lot of work to do today. I wish I could take a nap iI enjoy reading bo oks. They help '
  'me learn new things.nstead.'],
 ['I am very happy today. I love spending time with my friienI forgot my phone in the car. Oh no, '
  'now I have to The movie we saw last night was really good, but I think I would have enjoyed it '
  'more if Ip had some popcorn. Do you like popcorn?and get it.ds.'],
 ['I think I want to try cooking something new for dinner tonight. Do you have anoy favorite '
  'recipes?'],
 ['I forgot my phone in the car. Oh no, now I haI have a lot of work to do today. I wish I could '
  'take a nap iI enjoy reading bo oks. They help me learn new things.nstead.ve to go back and get '
  'it.'],
 ['I have today. I wish I could take a nap instead.'],
 ['I am very happy toroday. I love s'],
 ['I enjoy reading books. They help me learn newthings.'],
 ['I enjoy reading boorks. They help me learn newthings.'],
 ['The movie we saw last night was really goodThe movie we staw last night was really good, but I '
  'think I would have enjoI am very happy today. I love spending time with my friiends.yed it more '
  'if I had some popicorn. Do you like popcorn?, but?'],
 ['I enjoy reading books. TheyI think I want to try cooking something new for dinner tonight. Do '
  'you have any favorite recipes? help me learn new things.'],
 ['I have a lot of work to do today. I wish I could take a naI forgot my phone in the car. Oh no, '
  'now I have to go back and get it.p iI enjoy reading bo oks. They help me learn new '
  'things.nstead.'],
 ['I think I want to try cooking something new for dinner tonight. Do you have anoy favorite rI '
  'forgot my phone in the car. Oh no, now I have to The movie we saw last night was really good, '
  'but I think I would have enjoyed it more if Ip had some popcorn. Do you like popcorn?and get '
  'it.ecipes?'],
 ['I am very happy today. I ltoveThe movie we saw last night was really gooThe movie we saw last '
  'night was really goodThe movie we staw last night was really good, but I think I would have '
  'enjoI am very happy today. I love spending time with my friiends.yed it more if I had some '
  'popicorn. Do you like popcorn?, but?d, but I think I would have enjoyed it more if I had some '
  'popicorn. oDo you like popcorn? s'],
 ['I have a lot of work to do today. I wish I could take a nap iI enjoy reading bo oks. They help '
  'me learn new things'],
 ['The movie we saw last night was really good, but I think I would have enjoyed it more if I had '
  'some popcornI think I want to try cooking something new for dinner tonight. Do you have anoy '
  'favorite rhone in the car. Oh no, now I have to The movie we saw last night was really good, '
  'but I think I would have enjoyed it more if Ip had some popcorn. Do you like popcorn?and get '
  'it.ecipes?. Do you like popcorn?'],
 ['mThe movie we saw last night was really good, but I think I would have enjoyed it more if I had '
  'some popicorn. oDo you like popcosrn?'],
 ['I forgot my phone in the car. Oh no, now I have to The movie we saw last night was really good, '
  'but I think I would have enjoyed it more if Ip had some popcorn. Do you likeIn the morning, I '
  'like to have a cup of coffee to start my day off right. How about you? popcorn?and get rit.'],
 ['I am very happy today. I ltoveThe movieh we saw last night was really gooThe movie we saw last '
  'night was really goodThe movie we staw last night was really good, but I think I would have '
  'enjoI am very happy today. I love spending time with my friiends.yed it more if I had some '
  'popicorn. Do you like popcorn?, but?d, but I think I would have enjoyed it more if I had some '
  'popicorn. oDo you like popcorn? s'],
 ['I want tyo eat pizza for dinner. What do you think, should we orderu pizza?'],
 ['I enjoy reading books. They hhelp me learn newthings.'],
 ['I think I want to try cooking something new for dinner tonight. Do you have anoy favorite rI '
  'forgot my phone in the car. Oh no, now I have to The movie we saw last night was really good, '
  'but I think I would have enjoyed it more if Ip had some popcorn. Do you like popcorn?and get '
  'ilt.ecipes?'],
 ['I have a lot of work to do tloday. I wish I could take a nap instead.'],
 ['I forgot my phone in the car. Oh no, now I have to The movie we saw last niI want to eat pizza '
  'for dinner. What do you think, should we order pizza?ght was really good, but I think I would '
  'have enjoyed it more if Ip had some popcorn. Do you like popcorn?and get rit.'],
 ['I forgot my phone in the car. Oh no, now I have to The movie we saw last night was really good, '
  'but I think I would have enjooyed it more if Ip had some popcorn. Do you like popcorn?and get '
  'rit.'],
 ['The movie we saw last night was really good, but I think I would have enjoyed it more if I had '
  'some popcorn. Do you like popcThe movie we saw last night was really good, but?orn?'],
 ['The movie we saw last night was really good, but I think I would have enjoyed it more if I had '
  'some popcornI think I want to try cooking something new for dinner tonight. Do you have anoy '
  'favorite rhone in the car. Oh no, now I have to The movie we saw last night was really good, '
  'but I think I woultd have enjoyed it more if Ip had some popcorn. Do you like popcorn?and get '
  'it.ecipes?. Do you like popcorn?'],
 ['The movie we saw last night was really good, but I think oI would have enjoyed it  popcorn?'],
 ['The movie we saw last night was really good,  but I think oI would have enjoyed it  popcorn?'],
 ['I enjoy reading books. They help me learn new thing s.'],
 ['I enjoy reading boorks. They help me lThe movie we saw last night was really good, but I think '
  'I would have enjoyed it more if I had some popcornI think I want to try cooking something new '
  'for dinner tonight. Do you have anoy favorite rhone in the car. Oh no, now I have to The movie '
  'we saw last night was really good, but I think I would have enjoyed it more if Ip had some '
  'popcorn. Do you like popcorn?and get it.ecipes?. Do you like popcorn?eI have a lot of work to '
  'do today. I wish I could take a naI forgot my phone in the car. Oh no, now I have to go back '
  'and get it.p iI enjoy reading bo oks. They help me learn new things.nstead.arn newthings.'],
 ['I enjoy reading bjooks. They help me learn new thing s.'],
 ['The movie we saw last night was really good,  but I think oI would ghave enjoyed it  popcorn?'],
 ['The movie we saw last night was really good, but I think I would have enjoyed it more if I had '
  'some popcornI think I want to try cookinwe saw last night was really good, but I think I woultd '
  'have enjoyed it more if Ip had some popcorn. Do you like popcorn?and get it.ecipes?. Do you '
  'like popcorn?'],
 ['I think I want to try cooking something new for dinner tonighThe movie we saw last night was '
  'really good, but I think oI would have enjoyed it  popcorn?t. Do you have anoy favorite '
  'recipes?'],
 ['I forgot my phone in the car. Oh no, now I have to ThI forgot my phone in the car. Oh no, now I '
  'haI have a lot of work to do today. I wish I could take a nap iI enjoy reading bo oks. They '
  'help me learn new things.nstead.ve to go back and get it.e movie we saw last night was really '
  'good, but I think I would have enjoyed it more if Ip had some popcorn. Do you like popcorn?and '
  'get rit.'],
 ['I am very happy today. I love spending time with my friienI forgot my phone in the car. Oh no, '
  'now I have to The movie we saw last night was really good, but I think I would have enjoyed it '
  'mI want tyo eat pizza for dinner. What do you think, should we orderu pizza?ore if Ip had some '
  'popcorn. Do you like popcorn?and get it.ds.'],
 ['I think I wanI am very happy today. I love spending time with my friends.t to try cooking '
  'something new for dinner tonighThe movie we saw last night was really good, but I think oI '
  'would have enjo yed it  popcorn?t. Do you have anoy favorite recipes?'],
 ['The movie we saw last night was really good, but I think I would have enjoyed it more if I had '
  'some popicorn. oDo you like popco'],
 ['I have a lot of work to do tlodaya. I wish I could take aI think I want to try cooking '
  'something new for dinner tonighThe movie we saw last night was really good, but I think oI '
  'would have enjoyed it  popcorn?t. Do you have anoy favorite recipes? nap instead.'],
 ['I think I want to try cooking something new for dinner tonight. Do you have anoy favorite rI '
  'forgot my phone in the car. Oh no, now I have to The movie we saw last night was really good, '
  'but I think I would have enjoyed it more if Ip had some popcoron. Do you like popcorn?and get '
  'it.ecipes?'],
 ['I forgot my phone in the car. Oh no, now I have to The movie we saw last night was really good, '
  'but I think I would have enjooyed it more if Ip had some popcorn. Do you like popcorn?and I '
  'think I want to try cooking something new for dinner tonighThe movie we saw last night was '
  'really good, but I think oI would have enjoyed it  popcorn?t. Do you have anoy favorite '
  'recipes?get rit.'],
 ['I think I want to try cooking somethinnew for dinner tonight. Do you have any favorite '
  'recipes?'],
 ['I have a lot of work to do tlodaya. I wish I could take aI think I want to try cooking '
  'somtething new for dinner tonighThe movie we saw last night was really good, but I think oI '
  'would have enjoyed it  popcorn?t. Do you have anoy favorite recipes? nap instead.'],
 ['The movie we saw last night was really good, but I think I would have enjoy I had some popcorn. '
  'Do you like popcorn?'],
 ['I am very happy today. I love spending time with my friendsI love to read books. What about '
  'you?.'],
 ['I forgot my phone in the car. Oh no, now I have to ThI forgotHave you ever gone skydiving '
  'before? I did it once and it was amazing. my phone in the car. Oh no, now I haI have a lot of '
  'work to do today. I wish I could take a nap iI enjoy reading bo oks. They help me learn new '
  'things.nstead.ve to go back and get it.e movie we saw last night was really good, but I think I '
  'would have enjoyed it more if Ip had some popcorn. Do you like popcorn?and get rit.'],
 ['I love to read bookus. What about you?'],
 ['The movie we saw last night was really good, but I think I would have enjoyed it more if I had '
  'some popThe movie we saw last night was really good,  but I think oI would have enjoyed it  '
  'popcorn?corn. Do you like popcorn?'],
 ['The movie we saw last night was really goo?'],
 ['The movie we saw last night was really good, butI enjoy reading boorks. They help me learn '
  'newthings. I think I would have enjoy I had some popcorn. Do you like popcorn?'],
 ['I am very happy today. I love spending time with my friitends.'],
 ['I think I want to try cooking something new for dinner tonight. Do you have anoy favorite rI '
  'forgot my phone in the car. Oh no, now I have to The movie we saw last night was really good, '
  'but I think I would have enjoyed it more if Ip had some popcoron. Do you like propcorn?and get '
  'it.ecipes?'],
 ['The movie we saw last night was really good, but I think I would have enjoyed it more if I had '
  'some popcornI think I waont to try cookinwe saw last night was really good, but I think I '
  'woultd have enjoyed it more if Ip had some popcorn. Do you like popcorn?and get it.ecipes?. Do '
  'you like popcorn?'],
 ['The movie we saw last night was really good,  but I think oI would ghave I forgot my phone in '
  'the car. Oh no, now I have to The movie we saw last night was really good, but I think I would '
  'have enjoyed it more if Ip had some popcorn. Do you likeIn the morning, I like to have a cup of '
  'coffee to start my day off right. How about you? popcorn?and get rit.enjoyed it  popcorn?'],
 ['I enjoy reading bjooks. They helThe movie we saw last night was really good, but I think I '
  'would have enjoyed it more if I had some popicorn. Do you like popcorn?p me learn new thing s.'],
 ['I forgot my phone in the car. Oh no, now I have to The movie we saw last night was really good, '
  'but I think I would have enjoyed it more if Ip had some popcorn. Do you likeIn the morning, I '
  'like to have a cup of coffee to start my day off right. How about you? popcorn?and g'],
 ['I think I want to try cooking somethinnew for dinner tonight. Do you have any avorite recipes?'],
 ['The movie we saw last night was really good, but I think I would have enjoyed it more if I had '
  'some popThe movie we saw last night was really good,  but I think oI would have enjoyeI love to '
  'read books. What about you?d it  popcorn?corn. Do you like popcorn?'],
 ['I think I want to try cooking soI forgot my phone in the car. Oh no, now I haI have a lot of '
  'work to do today. I wish I could take a nap iI enjoy reading bo oks. They help me learn new '
  'things.nstead.ve to go back and get it.mething new for dinner tonight. Do you have anoy '
  'favorite recipes?'],
 ['I have a lot of work to do tlodaya. I wish I could take aI think I want to try cooking '
  'somtething new for dinner tonighThe movie we saw good, but I think oI would have enjoyed it  '
  'popcorn?t. Do you have anoy favorite recipes? nap instead.'],
 ['I think I want to try cooking something new for I forgot my phone in the car. Oh no, now I have '
  'to The movie we saw last night was really good, but I think I would have enjoyed it more if Ip '
  'had some popcorn. Do you like popcorn?and get rit.dinner tonight. Do you have anoy favorite '
  'recipes?'],
 ['I enjoy reading boorks. They help me leI have a lot of work to do today. I wish I could take a '
  'nap iI enjoy reading bo oks. They help me learn new thingsngs.'],
 ['I think I want to tryou have any favorite recipes?'],
 ['I think I wThe movie we saw last night was really good, but I think oI would have enjoyed it  '
  'popcorn?ant to try cooking somethinnew for dinner tonight. Do you have any favorite recipes?'],
 ['T he movie we saw last night was really good, but I think I would have enjoyed it more if I had '
  'some popThe movie we saw last night was really good,  but I think oI would have enjoyeI love to '
  'read books. What about you?d it  popcorn?corn. Do you like popcorn?'],
 ['I forgot my phone in the car. Oh no, now I have to The movie we saw last night was really good, '
  'but I think I would have enjooyed it morhe if Ip had some popcorn. Do you like popcorn?and get '
  'rit.'],
 ['I enjoy reading books. TheyI think I want to try cooking something new for dinner tonight. Do '
  'yI am very happy today. I ltoveThe movieh we saw last night was really gooThe movie we saw last '
  'night was really goodThe movie we staw last night was really good, but I think I would have '
  'enjoI am very happy today. I love spending time with my friiends.yed it more if I had some '
  'popicorn. Do you like popcorn?, but?d, but I think I would have enjoyed it more if I had some '
  'popicorn. oDo you like popcorn? sou have any favorite recipes? help me learn new things.'],
 ['I forgot my pho think, should we order pizza?ght was really good, but I think I would have '
  'enjoyed it more if Ip had some popcorn. Do you like popcorn?and get rit.'],
 ['I thfavorite recipesI enjoy reading books. TheyI think I want to try cooking something new for '
  'dinner tonight. Do yI am very happy today. I ltoveThe movieh we saw last night was really '
  'gooThe movie we saw last night was really goodThe movie we staw last night was really good, but '
  'I think I would have enjoI am very happy today. I love spending time with my friiends.yed it '
  'more if I had some popicorn. Do you like popcorn?, but?d, but I think I would have enjoyed it '
  'more if I had some popicorn. oDo you like popcorn? sou have any favorite recipes? help me learn '
  'new things.?'],
 ['The movie we saw last night was really good, ed it more if I had some popcorn. Do you like '
  'popcorn?'],
 ['I think I want to try cooking somethinnew for dinner tThe movie we saw last night was really '
  'good, but I think I would have enjoyed it more if I had some popicorn. oDo you like '
  'popcorn?onight. Do you have any favorite recipes?'],
 ['The mgoo?'],
 ['I forgot my phone in the car. Oh no, now I have to The movie we saw last niI want to eat pizza '
  'for dinner. What do you think, should we order pizza?ght was really good, but I think I woul d '
  'have enjoyed it more if Ip had some popcorn. Do you like popcorn?and get rit.'],
 ['I enjoy reading books. They help me learn nI think I want to try cooking soI forgot my phone in '
  'the car. Oh no, now I haI have a lot of work to do today. I wish I could take a nap iI enjoy '
  'reading bo oks. They help me learn new things.nstead.ve to go back and get it.mething new for '
  'dinner tonight. Do you have anoy favorite recipes?ewthings.'],
 ['In the morning, I lI forgot my phone in the car. Oh n o, now I have to go back and get it.ike '
  'to have a cup of coffee to start my day off right. How about you?'],
 ['mThe movie we saw last nightld have enjoyed it more if I had some popicorn. oDo you like '
  'popcosrn?'],
 ['I think I want to try cooking something new for dinner tonight. Do e enjoyed it more if Ip hhad '
  'some popcorn. Do you like popcorn?and get it.ecipes?'],
 ['I have a lot of work to do tlodaya. I wish kI could take aI think I want to try cooking '
  'somtething new for dinner tonighThe movie we saw goodI forgot my phone in the car. Oh no, now I '
  'have to The movie we saw last night was really good, but I think I would have enjoyed it more '
  'if Ip had some popcorn. Do you like popcorn?and get rit., but I think oI would have enjoyed i '
  't  popcorn?t. Do you have anoy favorite recipes? nap instead.'],
 ['I enjoy reading books. TheyI think I want to try coonking something new for dinner tonight. Do '
  'you have any favorite recipes? help me learn new things.'],
 ['The movie we saw last night wasI enjoy reading bjooks. They helThe movie we saw last night was '
  'really good, but I think I would have enjoyed it more if I had some popicorn. Do you like '
  'popcorn?p me learn new thing s. really good, but?'],
 ['Hello world. I am feeling good today. Are the plants green? Who knows! I bet It is hot '
  'outside.'],
 ['I really need to finish this project. It is due tomorrow. I hope I can get it done in time. If '
  'not, I will have to ask for an extension. I hate having to do that.'],
 ['The train is always crowded during rush hour. I have to stand the whole way to work. I wish I '
  'could just drive, but parking is too expensive. It is a real pain.'],
 ['I saw her on the street. I smiled at her. She smiled back. I wanted to talk to her but I was '
  'too shy. She walked away. I was sad. She turned around and came back to me. We talked for '
  'hours. We went to get some food. We laughed and had a great time. We exchanged numbers. I hope '
  'I see her again soon!'],
 ['When I visited Paris, I spent a lot of time exploring the museums and art galleries. It was a '
  'great opportunity to learn about history and culture.'],
 ['Although I live in the suburbs, I enjoy visiting the city. There are so many things to do and '
  'see. I especially like visiting the parks and gardens.'],
 ['I went to the store and bought some milk. I also saw a movie last night. Why are you still in '
  'bed?'],
 ['Are you feeling good? I hope so. I really want to go to the beach today. It is such a beautiful '
  'day outside.'],
 ['It is so hot outside today. I hate this weather. I wish I could just stay inside all day. Ugh!'],
 ['Yesterday was really busy for me. I had to attend three meetings and complete a report. '
  'However, I still managed to go for a run. I love being active!'],
 ['I went to the store and bought some milk. I also saw a movie last night. Why are you stgill in '
  'bed?'],
 ['wish'],
 ['DtiHeMkfeY'],
 ['Yesterday was re ally busy for me. I had to attend three meetings and complete a report. '
  'However, I still managed to go for a run. I love being active!'],
 ['stgill'],
 ['Yesterday was re ally busy for me. I had to attend three meetings and complete a report. '
  'Howcever, I still managed to go for a run. I love being active!'],
 ['Hello world. I am feeling good today. Are the plants green? Who knows! I bet It isday. hot '
  'outside.'],
 ['will'],
 ['Yesterday was really busy for me. I had to attend three meetings and ctalkgo for a run. I love '
  'being active!'],
 ['Hello world. I adm feeling good today. Are the plants green? Who knows! I bet It is hot '
  'outside.'],
 ['time.'],
 ['Yesterday was really busy for me. I had to attend three meetings and complete a report. '
  'However, I still managed to back.go for a run. I love being active!'],
 ['lxzoTZlWQp'],
 ['museums'],
 ['I'],
 ['Yesterday was really busy for me. nI had to attend three meetings and complete a Ugh!report.i '
  'However, I still manyaged to back.go for a run. I love being active!'],
 ['Yesterday was really busy for me. I had to attend three meetinkgo for a run. I love being '
  'active!'],
 ['Ugh!report.i'],
 ['I saw her on the street. I smiled at her. She smiled back. I wanted to talk to her but I was '
  'too shy. She od. We laughed and had a great time. We exchanged numbers. I hope I see her again '
  'soon!'],
 ['have'],
 ['I went to the store and bought some milk. I also saw a movie last night. Why are you sti in '
  'bed?'],
 ['I really need to finish this project. It is due tomorrow. I hope I can get it done in time. '
  'Ifwanted not, I will have to ask for an extension. I hate having to do that.'],
 ['you'],
 ['Yesterday was really busy for me. nI had to attend three meetings and complete a Ugh!report.i '
  'However, Howcever,yaged to back.go for a run. I love being active!'],
 ['When I visited Paris, I spent a lot of time exploring the museums and art galleries. It was a '
  'grat opportunity to learn about history and culture.'],
 ['opportunity'],
 ['I went to the store and bought some milk. I also laughedsaw a movie last night. Why are you '
  'still in bed?'],
 ['It is so hot outside today. I hate this weaUgh!'],
 ['hoYesterday was really busy for me. I had to attend three meetinkgo for a forrun. I love being '
  'active!pe'],
 ['Yesterday was really busstistill manyaged to back.go for a run. I love being active!'],
 ['hoYesterday was really busy foar me. I had to attend three meetinkgo for a forrun. I love being '
  'active!pe'],
 ['around'],
 ['expensive.'],
 ['hate'],
 ['The train is always crowded during rush hour. I have to stand the whole way to work. I wish I '
  'could just drive, but parking is too expensive. It is a real pain.her'],
 ['duue'],
 ['Hello world. I am feeling goohd today. Are the plants green? Who knows! I bet It is hot '
  'outside.'],
 ['inside'],
 ['Although I live in the suburbs, I enjoy visiting the city. There ahoYesterday was really busy '
  'for me. I had to attend three meetinkgo for a forrun. I love being active!pere so many things '
  'to do and see. I especially like visiting the parks and gardens.'],
 ['hod.ave'],
 ['Yesterday was really busy for me. I had to attend three meetinkgo for a run. mI love being '
  'active!'],
 ['DtiHeMYkfeY'],
 ['gooAlthough I live in the suburbs, I enjoy visiting the city. There ahoYesterday was really '
  'busy for me. I had to attend three meetinkgo for a forrun. I love being active!pere so many '
  'things to do and see. I especially like visiting the parks and gardens.hd'],
 ['DtiHeMeYkfeY'],
 ['w'],
 ['When I visited Paris, I spent a lot of tihme exploring the museums and art galleries. It was a '
  'great opportunity to learn about history and culture.'],
 ['Yesterday was really busy for me. nI had to attend three meetings and complete a Ugh!report.i '
  'However, Howcever,yaged to back.go for a run.c I love being active!'],
 ['Hello world. I am feeling goohd today. Are the plants greent? Who knows! I bet It is hot '
  'outside.'],
 ['this'],
 ['just'],
 ['DtiHeMkYkfeY'],
 ['I saw her on the street. I smiled at her. She smiled back. I wanted to talk to her but I was '
  'too shy. She od. We laughed and had a great time. We exchanged numbders. I hope I see her again '
  'soon!'],
 ['Yesterday was really busstistill manyaged to back.go for a run.l I love being active!'],
 ['talked'],
 ['wanted'],
 ['thigngs'],
 ['spedrive,nt'],
 ['movie'],
 ['Yesterday was really busy for mehope. nI had to attend three meetings and complete a '
  'Ugh!report.i However, Howcever,yaged to back.go for a run. I love being active!'],
 ['some'],
 ['report.'],
 ['stggill'],
 ['wishbought'],
 ['stand'],
 ['Yesterday was really busy for me. I had to attend three mieetings and complete a report. '
  'However, I still managed to go for a run. I love being active!'],
 ['always'],
 ['abackround'],
 ['She'],
 ['exchanged'],
 ['I went to the store and bought some milk. I also saw a movie last getnight. Why are you sti in '
  'bed?'],
 ['her.'],
 ['The train isactive!pere. It is a real pain.her'],
 ['som'],
 ['nI'],
 ['Hello world. I am feeling good today. Are the plants green? Who gknows! I bet It is hot '
  'outside.'],
 ['extension.'],
 ['DtiHeknows!MYkfeY'],
 ['go'],
 ['DtiHeMYDtiHeMkfeYYkfeY'],
 ['not,'],
 ['urun.l'],
 ['gooAlthough'],
 ['Yesterday was really busy for me. I had to attend threeYesterday was re ally busy for me. I had '
  'to attend three meetings and complete a report. Howcever, I still managed to go for a run. I '
  'love being active! meetinkgo for a run. I love being active!'],
 ['parks'],
 ['milk.'],
 ['We'],
 ['me.'],
 ['Hello world. I adm feeling good today. Are the plants green? Woknows! I  bet It is hot '
  'outside.'],
 ['Hello world. I adm feeling good today. Are the plants green? Woknows! I  bet It is hot outide.'],
 ['lahughedsaw'],
 ['Yesterday was really busy for me. I had to attend three meetinkgo for Thetreove being active!'],
 ['the'],
 ['edxchanged'],
 ['project.'],
 ['talk'],
 ['spent'],
 ['behistoryt'],
 ['When I visited Paris, I spent a lot of time exploring the museums and art galleries. Itt was a '
  'grat opportunity to learn about history and culture.'],
 ['opportbeachunity'],
 ['gggooAlthough'],
 ['today.'],
 ['I went to the store and bought some milk. I also saw a movie last getnight. Why are you sti '
  'inher bed?'],
 ['hour.'],
 ['Yesterday was really busy for me. nI had to attend three meetings and complete a Ugh!report.i '
  'However, Howcever,yaged to back.go for a run.c I love beiYesterday was really busy for me. I '
  'had to attend three meetings and ctalkgo for a run. I love being active!ng active!'],
 ['The train isactive!pere.standpain.her'],
 ['day'],
 ['finish'],
 ['The train isactive!per.her'],
 ['Hello'],
 ['jusst'],
 ['gooAlthou'],
 ['DtiHeMeYYkfeY'],
 ['duuego'],
 ['gooAlthough I live in theHello world. I adm feeling good today. Are the plants green? Who '
  'knows! I bet It is hot outside. suburbs, I enjoy visiting the city. There ahoYesterday was '
  'really busy for me. I had to attend three meetinkgo for a forrun. I love being active!pere so '
  'many things to do and see. I especially like visiting the parks and gardens.hd'],
 ['Are you feeling good? I hope so. I really want to go tol the beach today. It is such a '
  'beautiful day outside.'],
 ['The train isactive!pere. It is a real andain.her'],
 ['The train is always crowded during rush hour. I have to stand the whole way to work. I wish I '
  'could just drive, but pain.parking is too expensive. It is a real pain.her'],
 ['The traiculture.n is always crowded during rush hour. I have to stand the whole way to work. I '
  'wish I could just drive, but parking is too expensive. It is a real pain.her'],
 ['timet.'],
 ['Hello world. I am feeling good today. Are the plants green? Who knfood. I bet It is hot '
  'outside.'],
 ['rert.'],
 ['get'],
 ['Are'],
 ['vkcaRSvxRr'],
 ['ggooAlthoughgoohd'],
 ['was'],
 ['Yesterday was really busy for me. I had to attend threeYesterday was re ally busy for me. I had '
  'to attend three meetings and complete a report. Howcevera, I still managed to go for a run. I '
  'love being active! meetinkgo for a run. I love being active!'],
 ['YesterdayahoYesterday was really busy for me. I had to attend three meetinkgo for a run. I love '
  'being active!'],
 ['exepnloring'],
 ['The train is always crowded during rush hour. I have to stand the whole way to work. I wish I '
  'could just drive, but parking is too expensive. It is a real pYesterday was really busstistill '
  'manyaged to back.go for a run.l I love being active!ain.her'],
 ['traiculture.n'],
 ['gdot'],
 ['spedtrit'],
 ['It is so hoot outside today. I hate this weaUgh!'],
 ['hoYesterday was really busy foar me. I had to attend three meetingknows!kgo for a forrun. I '
  'love being active!pe'],
 ['Yesterday was really bu!sy for me. I had to attend three mieetings and complete a report. '
  'However, I still managed to go for a run. I love being active!'],
 ['Arspentelive'],
 ['spedrive,nctalkgot'],
 ['Are you feeling good? I hop I really want to go to the beach today. It is such a beautiful day '
  'outside.'],
 ['active!ng'],
 ['beiYesteerday'],
 ['DtiHfeMeYkfeY'],
 ['Dt'],
 ['beiYeteerday'],
 ['haave'],
 ['t'],
 ['Hello world. I am feeling good today. Are the plants green? Who knows! I bet It isI went to the '
  'store and bought some milk. I also saw a movie last getnight. Why are you sti in bed?day. hot '
  'outside.'],
 ['opbportbeachunity'],
 ['want'],
 ['meetings'],
 ['hoYesterday was really busy foar me.too I Hello world. I am feeling goohd today. Are the plants '
  'green? Who knows! I bet It is hot outside.hanrrun. I love being active!pe'],
 ['projectc.'],
 ['Yesterday was really busy for  I love being active!'],
 ['Hello world. I am feelihe plants greent? Who knows! I bet It is hot outside.'],
 ['Yesterday was really busy for me. I had t three meetinkgo for a run. mI love being active!'],
 ['hDptiHeMkfeYope'],
 ['I saw her on the street. I smiled at her. She smiled back. I wanted to talk to her but I was '
  'too shy. She od . We laughed and had a great time. We exchanged numbders. I hope I see her '
  'again soon!'],
 ['soo.'],
 ['Itof'],
 ['spedcrive,nctallkgot'],
 ['opHowever,bportbeachunity'],
 ['I saw her on the street. I smiled at her. She smiled back. I wanted to talk to her but I was '
  'too shy. She od . We laughed and had a great time. We exchanged numbders. I hope I see her '
  'again soon!me.'],
 ['hoYesterday was really busy foar me.too I Hello world. I am feeling goohd today. Are the plants '
  'green? Who knreport.ows! I bet It is hot outside.hanrrun. I love being active!pe'],
 ['DtareiHeMYkfeY'],
 ['visited'],
 ['art'],
 ['ggooAlHello world. I am feelihe plants greent? Who knows! I bet It is hot outside.houghgoohd'],
 ['back'],
 ['parking'],
 ['Dtspedcrive,nctallkgot'],
 ['wgoohdishbought'],
 ['Yesterday was re ally busy for me. I had to attened three knows!meetings and compleete a '
  'report. However, I still managed to go for a run. I love being active!'],
 ['beautiful'],
 ['The'],
 ['Yesterday was really busy for me.ad to attend three meetinkgo for yThetreove being active!'],
 ['Although I live in lahughedsawthe suburbs, I enjoy visiting the city. There are so many things '
  'to do and see. I especially like visiting the parks and gardens.'],
 ['work.'],
 ['many'],
 ['also'],
 ['vkcaRSvxR'],
 ['learntalk'],
 ['things'],
 ['good?'],
 ['manyaged'],
 ['Hello world. I adm feeling good today. Are the plants green? Woknows! IH  bet It is hot '
  'outside.'],
 ['ahod.ave'],
 ['retoort.'],
 ['Yesterday was really busy for me. I had to attend three meetings and complete a report. '
  'However, I still managed to go for a run. I love beinvg active!'],
 ['Howeverr,'],
 ['eo.n.'],
 ['repwgoohdishboughtort.'],
 ['Are you feeling good? I hop I really want to go to the beach today. It is such a beautiful day '
  'outsride.'],
 ['beautifuenjoyl'],
 ['I really need to finish this project. It is duen tomorrow. I hope I can get it done in time. If '
  'not, I will have to ask for an extension. I hate having to do that.'],
 ['to'],
 ['TIt is so hot outside today. I hate this weaUgh!he'],
 ['pYesterday'],
 ['Yesterday was really busstistill manyaged to back.go foer a run.l I love being active!'],
 ['beiYesterday'],
 ['ggooAlth'],
 ['The train n.her'],
 ['reopwgoohdigdotshboughtort.'],
 ['spedrivve,nt'],
 ['Hello world. I am feeling goohd today. Are the plants greent? Who knows! I beHello world. I am '
  'feelihe plants greent? Who knows! I bet It is hot outside. outside.'],
 ['goo'],
 ['traiculturecomplete.n'],
 ['someleaopbportbeachunityrntalk'],
 ['Hello world. dI adm feeling good today. Are the plants green? Woknows! I  bet It is hot '
  'outside.'],
 ['too'],
 ['Yesterday was really busy for me.ad to attend three meetinkgo for yThvetreove being active!'],
 ['omeetingsever,bportbeachunity'],
 ['honaave'],
 ['Yesterday was really busy for  I love beingHello active!'],
 ['Yesterday was really busy for me. nI had to attend three meetings and complete a Ugh!report.i '
  'However, Howcever,yaged to back.go for a run.c I love beiYesterday was really busy for me. I '
  'had to attend three meetings and bctalkgo for a run. I love being active!ng active!'],
 ['hDptacYope'],
 ['wantleearned'],
 ['spedpcrive,nctallkgtrain'],
 ['can'],
 ['so'],
 ['Ifwanted'],
 ['grat'],
 ['timefeeling'],
 ['aart'],
 ['Yesterday was really busy for me mI love being active!'],
 ['Thetreove'],
 ['tactivehoot'],
 ['hoYesterday was really busy foar me.too I Hello world. I am feeling goohd today. Are the plants '
  'green? Who knows! I bet It is hot outside.hanrrun. I lovextension.e being active!pe'],
 ['The traiculture.n is always crowded during rush horert.ur. I have to stand the whole way to '
  'work. I wish I could just drive, but parking is too expensive. It is a real pain.her'],
 ['hDptacYoe'],
 ['green?'],
 ['beachggooAlHello'],
 ['aYesterday was really busy for mehope. nI had to attend three meetings and complete a '
  'Ugh!report.i However, Howcever,yaged to back.go for a run. I love being active!lways'],
 ['turned'],
 ['The traiin is always crowded during rush hour. I have to stand the whole way to work. I wish I '
  'could just drive, but pain.parking is too expensive. It is a real pain.her'],
 ['I went to the store and bought some milk. I also sabutw a movie last night. Why are you stgill '
  'in bed?'],
 ['extensioen.'],
 ['projjectc.'],
 ['Yesterday was really busy for me.aYesterday was really busy for me. I had to attend three '
  'meetings and ctalkgo for a run. I love being  active!o for yThetreove being active!'],
 ['eHUAgcb'],
 ['The train is always crowded during rush hour. I have to stand the whole way to work. I wish I '
  'could just drive, but parkinIg is too expensive. It is a real pain.her'],
 ['youThe train is always crowded during rush ho parkinIg is too expensive. It is a real pain.her'],
 ['Ugh!'],
 ['stgillgooAlthough'],
 ['DtiH'],
 ['me.too'],
 ['parkinIg'],
 ['beiYestetrday'],
 ['eHUAgHoweverr,cb'],
 ['Yest!erday was really busy for me. I had to attend three mieetings and complete a report. '
  'However, I still managed to go for a run. I love being ac!'],
 ['er.I saw her on the street. I smiled at her. She smiled back. I wanted to talk to her but I was '
  'too shy. She walked away. I was sad. She turned around and came back to me. We talked for '
  'hours. We went to get some food. We laughed and had a great time. We exchanged numbers. I hope '
  'I see her again soon!'],
 ['aPhAa'],
 ['googardens.hd'],
 ['partomorrow.kinisactive!per.herIg'],
 ['I saw her on the street. I smiled at her. She smiled back. I wanted to talk to her but I was '
  'too shy. Shehope I see her again soon!me.'],
 ['When I visitedyou Paris, I spent a lot of tihme exploring the museums and art galleries. It was '
  'a great opportunity to learn about history and culture.'],
 ['Yesterday was really busstistill manyaged  to back.go foer a run.l I love being activeIt is so '
  'hot outside today. I hate this weaUgh!!'],
 ['When I visitedyou Paris, I spent a lot of tiretoort.hme exploring the museums and art '
  'galleries. It was a great opportunity to learn about history and culture.'],
 ['Hello world. I am feelihe plants greent? Who knowfs! I bet It is hot outside.'],
 ['ally'],
 ['lastDtiHeknows!MYkfeY'],
 ['Are you fee ling good? I hope so. I really want to go tol the beach today. It is such a '
  'beautiful day outside.'],
 ['TIt is soher. hot outside today. I hate this weaUgh!he'],
 ['isactive!per.her'],
 ['Are you feeling good? I hop I really want to go to the beach today. It is such a sride.'],
 ['ac!'],
 ['forrun.'],
 ['musems'],
 ['su'],
 ['Are Yesterday was really busy for me. nI had to attend three meetings and complete a '
  'Ugh!report.i However, Howcever,yaged to back.go for a run.c I love being active!ul day '
  'outside.'],
 ['hope'],
 ['Yesterday was really busy for me. I had to attend three mbeing active!'],
 ['When I visited Paris, I spent a lot of time exhoYesterday was really busy foar me. I had to '
  'attend three meetingknows!kgo for a forrun. I love being active!pees. Itt was a grat '
  'opportunity to learn about history and culture.'],
 ['The train is always crowded during rush hour. I have to stand tduringhe whole way to work. I '
  'wish I could just drive, but parking is too expensive. It is a real pain.'],
 ['Yesterday was really busy for mehope. nI chad to attend three meetings and complete a '
  'Ugh!report.i However, Howcever,yaged to back.go for a run. I love being active!'],
 ['hoYesterday was really busy foar me.too I Hello world. I am feeling goohd today. Are the plants '
  'green? Who knrepomoviert.ows! I bet It is hot outside.hanrrun. I love being active!pe'],
 ['Thetereove'],
 ['I went to the store and bought some milk. I also laughen bed?'],
 ['n'],
 ['Shhe'],
 ['somreleaopbportbeachunityboughttalk'],
 ['isI'],
 ['I saw her on the street. I smiled at her. She smiled back. I wanted to talk to her but I was '
  'too shy. She od. We laughed and had a great time. We exchanged numbderss. I hope I see her '
  'again soon!'],
 ['I saw her on the street. I smiled at her. She smiled baYesterday was really busy for me.ad to '
  'attend three meetinkgo for yThetreove being active!ck. I wanted to talk to her but I was too '
  'shy. She od. We laughed and had a great time. We exchanged numbderss. I hope I see her again '
  'soon!'],
 ['foer'],
 ['DtiHfeMeYkfeHello world. I am feeling goohd today. Are the plants greent? Who knows! I beHello '
  'world. I am feelihe plants greent? Who knows! I bet It is hot outside. outside.'],
 ['project.n.her'],
 ['wafinishs'],
 ['drive,'],
 ['AreWhen I visited Paris, I spent a lot of tihme exploring the museums and art galleries. It was '
  'a great opportunity to learn about history and culture.'],
 ['Yesterday was reabetlly busy for me. I had t three meetinkgo for a run. mI love being active!'],
 ['wnishs'],
 ['Hello world. I am feeling good today. Are the plants green? Who knfood. I bet It is huot '
  'outside.'],
 ['The traiculture.n is always crowded during rush huour. I have to stand the whole way to work. I '
  'wish I could just drive, but parking is too expensive. It is a real pain.her'],
 ['pars'],
 ['nII'],
 ['gggooAlthoughThe'],
 ['sti'],
 ['bet'],
 ['I went to the store and bought some milk. I also saw a movie lasto night. Why are you sti in '
  'bed?'],
 ['The train ier'],
 ['movibute'],
 ['Howcevera,'],
 ['activve!ng'],
 ['came'],
 ['gggooAlthouYesterday was really busy for me.ad to attend three meetinkgo for yThvetreove being '
  'active!gh'],
 ['good'],
 ['outside.houghgoohd'],
 ['bu!sy'],
 ['AreWhen I visited Paris, I spent a lot of tihme exploring the museums and art galleries. It was '
  'a great opportunity to learn about hnistory and culture.'],
 ['learnatalk'],
 ['exchacnged'],
 ['such'],
 ['Yesterday was really bu!sy for me. I had to attend three mieetings and tcomplete a report. '
  'However, I still managed to go for a run. I love being active!'],
 ['DtiHfeMeYkfeHello world. I am feeling goohd today. Are the plants gde.'],
 ['hoYesterday was reduenally busy foar me. I had to attend three meetinkgo for a fWhenorrun. I '
  'love being active!pe'],
 ['mfeelinganaged'],
 ['cThetereovean'],
 ['ItdI'],
 ['back.go'],
 ['aYesterday was really busry for mehope. nI had to attend three meetings and complete a '
  'Ugh!report.i However, Howcever,yaged to back.go for a run. I love being active!lways'],
 ['reporpt.'],
 ['beeiYeteerday'],
 ['Yest!erday'],
 ['weather.'],
 ['beautifuenjoyjl'],
 ['WWe'],
 ['laughed'],
 ['parsShe'],
 ['fph'],
 ['gde.work.'],
 ['I went to the store and bought s ome milk. I also saw a movie last night. Why are you sti in '
  'bed?'],
 ['isday.'],
 ['I went to the store and bgoodght some milk. I also saw a movie last night. Why are you still in '
  'bed?'],
 ['opportunitbeautifuly'],
 ['Hello world. I am feeling good today. Are the plants green? Who knows! I bet It isI went to the '
  'store and bought some milk. I also saw a movie last getnight. Why are you sti in '
  'bed?day.repwgoohdishboughtort. hot outside.'],
 ['gggooAlthouYesterday was realley busy for me.ad to attend three meetinkgo for yThvetreove being '
  'active!gh'],
 ['The train aAreWhen I visited Paris, I spent a lot of tihme exploring the museums and art '
  'galleries. It was a great opportunity to learn about history and culture.d.aveisactive!per.her'],
 ['went'],
 ['It is. so hot outside today. I hate this weaUgh!'],
 ['I really need to finish this project. It is due tomorrow. I hope I can get it done in time. If '
  'not, I will have to ask for an extension. I hate halving to do that.'],
 ['Dtspedlkgot'],
 ['rert'],
 ['opbportbeacbgoodghthunity'],
 ['mums'],
 ['duuduringe'],
 ['It is so hoot ioutside today. I hate this weaUgh!'],
 ['Yesat!erday'],
 [''],
 ['fee'],
 ['trai'],
 ['hThe'],
 ['getnight.'],
 ['The train is always crowded during rush hour. I have to stag is too expensive. It is a real '
  'pain.her'],
 ['suchmany'],
 ['Yesterday was really busy for mel. I had to attend three meetings and complete a report. '
  'However, I still managed to back.go for a run. I love being active!'],
 ['great'],
 ['seppent'],
 ['Yesterday was really busy for me. I had to attend thnreeYesterday was re ally busy for me. I '
  'had to attend three meetings and complete a report. Howcever, I still managed to go for a run. '
  'I love being active! meetinkgo for a run. I love being active!'],
 ['gdeThe train is always crowdhoYesterday was really busy foar me.too I Hello world. I am feeling '
  'goohd today. Are the plants green? Who knrepomoviert.ows! I bet It is hot outside.hanrrun. I '
  'love being active!peed during rush hour. I have to stand the whole way to work. I wish I could '
  'just driveis a real pain.her.work.'],
 ['andain.her'],
 ['Yesterday was really busy for me. I haYesterday was really busy for me.ad to attend three '
  'meetinkgo for yThvetreove being active!eport. However, I still managed to go for a run. I love '
  'being active!'],
 ['alsyss'],
 ['wantleearwnishsned'],
 ['hinsideThe'],
 ['tgdeThehis'],
 ['horert.ur.'],
 ['exchangecd'],
 ['ADtareiHeMYkfeYrspentelive'],
 ['projectec.'],
 ['W'],
 ['me.aYesterday'],
 ['sactive!pYesterday was really busy for me. nI had to attend three meetings and complete a '
  'Ugh!report.i However, Howcever,yaged to back.go for a run.c I love beiYesterday was really busy '
  'for me. I had to attend three meetings and bctalkgo for a run. I love being active!ng '
  'active!eo'],
 ['TThe traiculture.n is always crowded during rush huour. I have to stand the whole way to work. '
  'I wish I could just drive, but parking is too expensive. It is a real pain.herhe train ier'],
 ['gooAlthough I live in the suburbs, I enjoy visiting the city. Ther parks and gardens.hd'],
 ['yThetreeove'],
 ['gdoThe train is always crowded during rush hour. I have to stand the whole way to work. I wish '
  'I could just drive, but parkinIg is too expensive. It is a real pain.hert'],
 ['behistoryotlastDtiHeknows!MYkfeY'],
 ['DtiHeMbackkfeY'],
 ['bask'],
 ['edxopportbeachunitychanged'],
 ['Yesterday was re ally busy for me. I had to attend three meetings and complete a report. '
  'Howcever, I still m being active!'],
 ['tooo'],
 ['ctalkgo'],
 ['n.her'],
 ['Yesterday was really bIfwantedusstistill manyaged  to back.go foer a run.l I love being '
  'activeIt is so hot outside today. I hate this weaUgh!!'],
 ['ecd'],
 ['hoave'],
 ['pain.herhe'],
 ['tai'],
 ['duued.'],
 ['I saw her on the street. I smiled at her. She smiled back. Ibctalkgo wanted to talk to her but '
  'I was too shy. She od . We laughed and had a greasoon!me.t time. We exchanged numbders. I hope '
  'I see her again soon!me.'],
 ['IH'],
 ['Yest!t. However, I still managed to go for a run. I love being ac!'],
 ['lreabetlly'],
 ['AreWhen I visited Paris, I spent a lot of tihmrt galleries. It was a great opportunity to learn '
  'about history and culture.'],
 ['cThetereoHello world. I am feeling good today. Are the plants green? Who knows! I bet It is hot '
  'outside.vean'],
 ['I saw her on the street. I smiled at her. She smiled back. I wanted to talk to her but I was '
  'too shy. She walked away. I was sad. She turned around and came back to me. We talked for '
  'hours. We went to get some food. We la ughed and had a great time. We exchanged numbers. I hope '
  'I see her again soon!'],
 ['waactivehoots'],
 ['edxopportbeachunityouTheychanged'],
 ['exchansugecd'],
 ['tart'],
 ['bed?ay.spedpcrive,nctallkgtrain'],
 ['wwill'],
 ['rthigntraings'],
 ['abackdround'],
 ['WWerert'],
 ['greasoon!me.t'],
 ['TI really need to finish this project. It is due tomIorrow. I hope I can get it done in time. '
  'If not, I will have to ask for an extension. I hate having to do that.hetreove'],
 ['city.'],
 ['galleries.'],
 ['active!lways'],
 ['gggooAlthouYesterday was realley busy for me.ad to attend three treove being  active!gh'],
 ['beachggooAlHelsomreleaopbpogrtbeachuanityboughttalko'],
 ['gggooAlthotraiinThe'],
 ['vhonavave'],
 ['Yest!erday was really busy for me. I had to attend three mieetings and complete a report. '
  'Howjusstever, I still managed to go for a run. I love being ac!'],
 ['haYesterday'],
 ['active!Hello world. I adm feeling good today. Are the plants green? Woknows! I  bet It is hot '
  'outside.ng'],
 ['lovesom'],
 ['active!peed'],
 ['When I visited Paris, I spent a lot of time exploas a grat opportunity tor learn about history '
  'and culture.'],
 ['rtor'],
 ['huour.ited'],
 ['beiYestereday'],
 ['wanYesterday was really busstistill manyaged to back.go foer a run.l I love being active!ted'],
 ['aPhAamI'],
 ['I saw her on the stWWereet. I smiled at her. She smiled baYesterday was really busy for me.ad '
  'to attend three meetinkgo for yThetreove being active!ck. I wanted to talk to her but I was too '
  'shy. She od. We laughed and had a great time. We exchanged numbderss. I hope I see her again '
  'soon!'],
 ['It is so hooth ioutside today. I hate this weaUgh!'],
 ['gisIggooAlthouYesterday was realley busy for me.ad to attend three meetinkgo for yThvetreove '
  'being active!gh'],
 ['When I visited Paris, I spent a lot of time exploring the museums and art galleries. It was a '
  'great opportunity tobeeiYeteerday learn about history and culture.'],
 ['Yesterday was really busy for me. I had t three meetinkback.gogo for a r un. mI love being '
  'active!'],
 ['edxoppdortbeachunitychanged'],
 ['Ther'],
 ['partomorrow.kinisactive!per.hestayrIg'],
 ['seppenHello world. I adm feeling good today. Are the plants green? Who knows! I bet It is hot '
  'outside.t'],
 ['tactive'],
 ['isday.hoYesterday was really busy foar me.too I Hello world. I am feeling goohd today. Are the '
  'plants green? Who knows! I bet It is hot outside.hanrrun. I love being active!pe'],
 ['so!'],
 ['ggooAlthoughdgoohd'],
 ['back.'],
 ['F'],
 ['opportbeachuninity'],
 ['YesterdayahoYesterday'],
 ['wehather.'],
 ['Yesterday was really rbusy for me. I haYesterday was really busy for me.ad to attend three '
  'meetinkgo for yThvetreove being active!eport. However, I still managed to go for a run. I love '
  'being active!'],
 ['Hello world. I adm feeling good today. Are the plants green? WoIknows! I  bet It is hot '
  'outside.'],
 ['Paris,'],
 ['Drusht'],
 ['hDptiHeMkfope'],
 ['I really need to finish this project. It is due tomorrow. I hope I can get it done in time. If '
  'not, I will have to ask for an extension. I hate halving to d o that.'],
 ['The traiin is always crowded during rush hour. I have to stand the whole way to work. I '
  'wioIknows!n.her'],
 ['ling'],
 ['b!u!sy'],
 ['manyyaaged'],
 ['meetingknows!kgo'],
 ['Hello world. I am feeling good todbaYesterdayay. Are the plants green? Who knows! I bet It is '
  'hot outside.'],
 ['specompleetedtrit'],
 ['active!pepain.herhe'],
 ['Yesterday was really busy for me. I had to attend threeYesterday was re ally busy for me. I had '
  'to attend three meetings and complete a report. Howcevera, I still managed to go for a run. I '
  'locve being active! meetinkgo for a run. I love being active!'],
 ['gdoThe train is always crowded during rush hour. I have to stand the whole way to work. I wish '
  'I could just drive, but parkinIg is too exrpensive. It is a real pain.hert'],
 ['beiYestea'],
 ['ctalkThe train isactive!pere. It is a real andain.hergo'],
 ['I went to the store and bought some milk. I also saw a movoie last night. Why are you sti in '
  'bed?'],
 ['Yesterday was really busy for mee.ad to attend three meetinkgo for yThetreove being active!'],
 ['exploaas'],
 ['tihme'],
 ['Yesterday was really busy for me. I had to attend threeYesterday was re ally busy for me. I '
  'hThe train aAreWhen I visited Paris, I spent a lot of tihme exploring the museums and art '
  'galleries. It was a great opportunity to learn about history and '
  'culture.d.aveisactive!per.herad to attend three meetings and complete a report. Howcevera, I '
  'still managed to go for a run. I love being active! meetinkgo for a run. I love being active!'],
 ['edxoppsride.ortbeachunitychanged'],
 ['I really need to finish this project. It is due tomorrow. I hope I can get it done in time. '
  'Ifwanted not, I will have to askh for an extension. I hate having to do that.'],
 ['I went to the store and bought some milk. I also saw a movieAre you feeling good? I hope so. I '
  'really want to go tol the beach today. It is such a beautiful day outside. last night. Why are '
  'you sti in bed?'],
 ['numbderss.'],
 ['movoie'],
 ['turbeiYesteerdayned'],
 ['UmvV'],
 ['It is so hooth ioutside toexpensive.day. I hate this weaUgh!'],
 ['ssoo.'],
 ['eIt is so hoot ioTIt is so hot outside today. I hate this weaUgh!heutside today. I hate this '
  'weaUgh!eo.n.'],
 ['wiwsh'],
 ['rerlxzoTZlWQpt'],
 ['laugghed'],
 ['hoYesterday was really busy foar me.too I Hel lo world. I am feeling goohd today. Are the '
  'plants green? Who knreport.ows! I bet It is hot outside.hanrrun. I love being active!pe'],
 ['Yesterdays was really busy for mee.ad to attend three meetinkgo for yThetreove being active!'],
 ['see.'],
 ['proWhen I visitedyou Paris, I spent a lot of tihme exploring the museums and art galleries. It '
  'was a great opportunity to learn about history and culture.ject.'],
 ['pYesterday was really busy for me. I had to attend three meetinkgo for Thetreove being '
  'active!rojectc.'],
 ['Helloelihe plants greent? Who knowfs! I bet It is hot outside.'],
 ['hoYesterday was really busy foar me.too I Hello world. I am feeling goohd today. Are the plants '
  'green? Who knrepomoviert.ows! I bet It is  outside.hanrrun. I love being active!pe'],
 ['RXNeOJO'],
 ['stag'],
 ['ecdayd'],
 ['I saw her on the street. I smiled at her. She smiled back. I wanted to talk to her but I was '
  'too shy. She od. We laughed and had a greatknreport.ows!n!'],
 ['beautihalvingfuenjoyjl'],
 ['dItdI'],
 ['omeetingsever,bportbeachunityyou'],
 ['Yesterday was really busy for me. I had to attend three mbeing activesabutw!'],
 ['Shhegde.work.'],
 ['DtThe train is always crowded during rush hour. I have to stand the whole way to work. I wish I '
  'could just drive, but parking is too expensive. It is a real pain.kspedlkgot'],
 ['suchmamny'],
 ['way'],
 ['stWWereet.'],
 ['I feel good today. I will be productive. will kill It.'],
 ['I feel good today? I will be productive. will kill It'],
 ['I feel good today! I will be productive. will kill It'],
 ['I feel good today.. I will be productive. will kill It'],
 ['I feel good today! I will be productive. will kill It!'],
 ['I feel good today I will be productive'],
 ['I feel good today. I will be productive. will kill It Bla bla bla.'],
 [' I am wearing a blue shirt today. It is my lucky shirt. I hope I win the contest. I am going to '
  'gym. I hear people there do a lot of cardio!'],
 ['Althounight.gh I live in the sub urbs, I enjoy visiting the city. There are so many things to '
  'do and see. I especially like visiting the parks and gardens.'],
 ['Yesterday was really busy for me. I had to atvtend three meetings and complete a report. '
  'However, I still managed to go for a run. I love being active!'],
 ['about'],
 ['see'],
 ['a'],
 ['Yesterday was really busy for me. I had to atvtend three meetings and complete a report. n. I '
  'love being active!'],
 ['anHowever,d'],
 ['Yesterday was really busy for me. I had to atvtend three meetings and complete a report. n. I '
  'love btraineing active!'],
 ['Although I live in the suburbs, I enjoy visiparksgs to do and see. I especially like visiting '
  'the parks and gardens.'],
 ['Although I live in the suburbs, I enjoy visiparksgs to do and seetomorrow.. I especially like '
  'visiting the pthisarks and gardens.'],
 ['vlive'],
 ['Yesterday was really busy for me. I had to atvtItend three meetings and complete a report. '
  'However, I still managed to go for a run. I love being active!'],
 ['D'],
 ['I saw her on the street. I smiled at her. She smiled back. I wanted to talk to her but I was '
  'too shy. She walked away. I was sad. She turned around and came back to me. We talked for '
  'hours. We went to get some food. We laughed and had a great time. We exchanged numbers. I hope '
  'getI see her again soon!'],
 ['for'],
 ['It is so hot outside today. Iwill hate this weather. I wish I could just stay inside all day. '
  'Ugh!'],
 ['do'],
 ['sstore'],
 ['It is so hot outside today. Iwill hate this weather. I wish I could just stay inside alday. '
  'Ugh!'],
 ['seetomorrow..'],
 ['Why'],
 ['during'],
 ['whorushle'],
 ['live'],
 ['d'],
 ['urbs,'],
 ['at'],
 ['urbss,'],
 ['Yesterday was really busy for me. I had to atvtend thoree meetings andgo complete a report. '
  'However, I still managed to go for a run. I love being active!'],
 ['notcould,'],
 ['stoday.dee'],
 ['complete'],
 ['Althounight.gh I live in the sub urbs, I enjoy visiting the city. There are so many things to '
  'do and see. I especially like visiting the paerks and gardens.'],
 ['nigh.'],
 ['When I visited Paris, I spent a lot of time exploring tthe museums and art galleries. It was a '
  'great opportunity to learn about history and culture.'],
 ['Althounight.gh I livve in the sub utrbs, I enjoy visiting the city. There are so many things to '
  'do and see. I especially like visiting the paerks and gardens.'],
 ['street.'],
 ['folivver'],
 ['Hello world. I am feeling good today. Are the plants green? Who knows! I bet It is hot '
  'outstoreside.'],
 ['Yesterday'],
 ['Although I live in the suburbs, Ithiske visiting the pthisarks and gardens.'],
 ['I saw her on the street. I smiled at her. She smiled back. I wanted to talk to her but I was '
  'too shy. She walked away. I was sad. She turned around and came back to me. We talked for '
  'hours. We went to get some food. We laughewholed and had a great time. We exchanged numbers. I '
  'hope I see her again soon!'],
 ['However,'],
 ['att'],
 ['Although I live in the suburbs, I enjoy visiting the city. There are so many things to do and '
  'seAlthough I live in the suburbs, Ithiske visiting the pthisarks and gardens.visiting the parks '
  'and gardens.'],
 ['foobetd.'],
 ['ur'],
 ['notocould,'],
 ['walked'],
 ['udady.rbs,'],
 ['nopaerks'],
 ['aboYesterday was really busy for me. I had to atvtItend three meetings and complete a report. '
  'However, I still managed to go for a run. I love being active!ut'],
 ['I went to the store and bought some milk. I also saw a movie last night. Why are you still in '
  'bed?,'],
 ['It is so hot outside today. Iwill hate this weather. I wish I  could just stay inside all day. '
  'Ugh!'],
 ['Who'],
 ['sstorte'],
 ['selike'],
 ['The train is always crowded during rush hour. I havehole way to work. I wish I could just '
  'drive, but parking is too expensive. It is a real pain.'],
 ['I saw her on the street. I smiled at her. She smiled back. I wanted to talk to her but I was '
  'too shy. She walked away. I was sad. She turned around and came back to me. We talked foaughed '
  'and had a great time. We exchanged numbers. I hope getI see her again soon!'],
 ['abouIt is so hot outside today. Iwill hate this weather. I wish I could just stay inside all '
  'day. Ugh!'],
 ['enjoy'],
 ['aboYesterday was really busy for me.parking I had to atvtItend three meetings and complete a '
  'reporet. However, I still managed to go for a run. I love being active!ut'],
 ['wl'],
 ['Wo'],
 ['Parsehaveliksmiledeis,'],
 ['I went to the store and bought some milk. I also saw a movie last night. Whysstorte are you '
  'still in bed?,'],
 ['in'],
 ['Yesterday was really busy for me. I had to attend three meetings and complete a report. '
  'However, I still managed to go for a runc. I love being active!'],
 ['UJHpsxQi'],
 ['all'],
 ['vlivUJHpsxQie'],
 ['nopaerksHello world. I am feeling good today. Are the plants green? Who knows! I bet It is hot '
  'outside.'],
 ['aboYesterday was raeally busy for me.parking I had to atvtItend three meetings and complete a '
  'reporet. However, I stiworld.ll managed to go for a run. I love being active!ut'],
 ['sub'],
 ['hot'],
 ['notcouldstore,'],
 ['Hello world. I am feeling good today. Are the  plants green? Who knows! I bet It is hot '
  'outside.'],
 ['Wsawho'],
 ['caAlthough'],
 ['I went to the store and bought some milk. I also saw a movie last night. Whysstorte are you '
  'still in be?,'],
 ['seAlthough'],
 ['lvisitedive'],
 ['aa'],
 ['aboYesterday was really busy for me.parking I had to atvtItend three meetings and complete a '
  'reporet. However, I still managed tove being active!ut'],
 ['Hello world. ants green? Who knows! I bet It is hot outsidego.'],
 ['night.'],
 ['today.yyou'],
 ['toaboYesterday was really busy for me. I had to atvtItend three meetings and complete a report. '
  'However, I still managed to go for a run. I love being active!utday.yyou'],
 ['seetohours.morrow..'],
 ['outstoreside.'],
 ['sw..'],
 ['If'],
 ['Althounight.gh I live in the sub urbs, I enjoy visiting the city. There are so many thike '
  'visiting the parks and gardens.'],
 ['Althounight.gh I livve in the sub The train is always crowded during rush hour. I havehole way '
  'to work. I wish I could just drive, but parking is too expensive. It is a real pain.utrbs, I '
  'enjoy visiting the city. There are so many things to do and see. I especially like visiting the '
  'paerks and gardens.'],
 ['asstwillorea'],
 ['rreal'],
 ['aall'],
 ['Although I live in the suburbs, Ithiske viIsiting the pthisarks and gardens.'],
 ['Iftime'],
 ['store'],
 ['aaa'],
 ['Althounight.gh I live in the sub urbs, I enjoy visiting the city. Theng the paerks and '
  'gardens.'],
 ['alwways'],
 ['aboYesterday was really busy for me. I had to atvtItend three meetings and complete a report. '
  'However, I still managed to go  for a run. I love being active!ut'],
 ['seetohours.moorrow..'],
 ['seetohatvtItendours.moorrow..'],
 ['nibackght.'],
 ['P,aris,'],
 ['ask'],
 ['away.'],
 ['gardens.'],
 ['on'],
 ['arodunnd'],
 ['caday.n'],
 ['seAlthoAugh'],
 ['dbtraineing'],
 ['wwZQ'],
 ['Althounight.gh I live in the sub urbs, I enjoy visiting the city. There isare so many thike '
  'visiting the parks and gardens.'],
 ['so.'],
 ['I went eto the store and bought some milk. I also saw a movie last night. Why are you still in '
  'bed?'],
 ['greenworld.?'],
 ['arou'],
 ['had'],
 ['n.UJHpsxQi'],
 ['aroseAlthoAughund'],
 ['visiparksgsWo'],
 ['Arlthough I live in the suburbs, I enjoy visiparksgs to do and see. I especially like visiting '
  'the parks and gardens.'],
 ['nibacht.'],
 ['runbought.'],
 ['extensiaboYesterday was really busy for me. I had to atvtItend three meetings and complete a '
  'report. However, I still managed to go  for a run. I love being active!uton.'],
 ['Are you feeling good? I hope iso. I really want to go to the beach today. It is such a '
  'beautiful day outside.'],
 ['I went eto the store and bought some milk. I also saw a movieenjoy last night. Why are you '
  'still in bed?'],
 ['atfood.'],
 ['lvisitedaughd'],
 ['knows!'],
 ['UJHpsxQiapain.utrbs,aa'],
 ['aactive!utday.yyouall'],
 ['Hello world. I am feeling good today. Are the  plants green? Who knows! I bet It is hot o '
  'utside.'],
 ['allenjoy'],
 ['seAlthtough'],
 ['mtomorrow.e.'],
 ['arexpensive.ound'],
 ['liv'],
 ['I went to the store and bought some millk. I also saw a movie last night. Why are you still in '
  'bed?,'],
 ['I went to the store and bought some millk. I also saw a movite last night. Why are you still in '
  'bed?,'],
 ['visiting'],
 ['assk'],
 ['seAlthtougAlthough I live in the suburbs, Ithiske viIsiting the UJHpsxQipthisarks and '
  'gardens.h'],
 ['notcouldstore'],
 ['stcity.'],
 ['Whoa'],
 ['The train is always crowded during rush hour. I have to stand the whole wayt to work. I wish I '
  'could just drive, but parking is too expensive. It is a real pain.'],
 ['raeally'],
 ['but'],
 ['seli'],
 ['.gardens.'],
 ['atvtend'],
 ['There'],
 ['lviin'],
 ['lean'],
 ['exbe?,tension.'],
 ['dbtrg'],
 ['suburbs,'],
 ['crowded'],
 ['aaall'],
 ['no'],
 ['ssasstwilloreatore'],
 ['notcoudld,'],
 ['aboYesterday was real complete a report. However, I still managed to go  for a run. I love '
  'being active!ut'],
 ['movieenjoy'],
 ['garden'],
 ['.gardenns.'],
 ['I went to the store and bought some milk. I also saw a movie last night.gardens. Whysstorte are '
  'you still in bed?,'],
 ['aactiraeallyve!utday.yyouall'],
 ['nibachAlthounight.gh I live in the sub urbs, I enjoy visiting the city. There are so many '
  'things to do and see. I especially like visiting the paerks and gardens.t.'],
 ['ithen'],
 ['aboYesterday was really busy for me.parking I had to atvtItend three meetings and complete a '
  'reporet. However, I still managed tove being active!utfolivver'],
 ['so.abouIt'],
 ['wlsw..'],
 ['WhThe train is always crowded during rush hour. I have to stand the whole wayt to work. I wish '
  'I could just drive, but parking is too expensive. It is a real pain.o'],
 ['feeling'],
 ['Whorunbought.'],
 ['nhight.'],
 ['outstorecanside.'],
 ['eto'],
 ['Ifte'],
 ['outside.'],
 ['Arlthough'],
 ['uwholerbs,'],
 ['Although I live in the suburbs, Ithiske viIsiting the pthisarks atvtItendand garden.'],
 ['wayt'],
 ['Althounight.gh I livve in the sub The train is always crowded during rush hour. I havehole way '
  'to work. I wish I could just drive, but parking is too expensive. It is ame. real pain.utrbs, I '
  'enjoy visiting the city. There are so many things to do and see. I especially like visiting the '
  'paerks and gardens.'],
 ['aboYesterday was really busy for me. I had to atvtItend three meetings and complete a report. '
  'Howeverl, I still managed to go for a run. I love being active!ut'],
 ['Yesterday was really buwantedsy for me. I had to atvtend three meetings and complete a report. '
  'n. I love btraineing active!'],
 ['wuhorushle'],
 ['When I visited Paris, I spent a lot of time exploring the museums afolivvernd art galleries. It '
  'was a great opportunity to learn about history and culture.'],
 ['seetohours..morrow..'],
 ['Woo'],
 ['odo'],
 ['Iextension.f'],
 ['eseeli'],
 ['WhThe train is always crowded during rush hour. I have to stand the whole wayt to work. I wish '
  'I could just drive, but parking is too expensive. It is a r.o'],
 ['having'],
 ['atfood.done'],
 ['vliv'],
 ['Yesterday was really buwantedsy for me. I had to atvtend three meetings and complete a repaort. '
  'n. I love btraineing active!'],
 ['Althounight.gh I livve in the sub The train is always crowded during rush hour. I havehole way '
  'to work. I wish I could just drive, but parking is too expensive. It is a real pain.utrbs, I '
  'enjoy visiting the city. There are so many things to do and see. I especially like visiting the '
  'paerks and gardens.amovieenjoy'],
 ['rrWholeal'],
 ['movieennjoy'],
 ['aboYesterday was really busy foSher me. I had to atvtItend three meetings and complete a '
  'report. However, I still managed to go  for a run. I love being active!ut'],
 ['suburbsus,'],
 ['I went to the store and bought some milk. I also saw a movie last night.gardens. Whysstorte are '
  'you stsuchill in bed?,'],
 ['gyouarden'],
 ['anlvisitedive'],
 ['hours.'],
 ['alwwexploringays'],
 ['notcoudldlivve'],
 ['dd'],
 ['I saw her on the street. I smiled at her. She smiled back. I wYesterday was really buwantedsy '
  'for me. I had to atvtend three meetings and complete a report. n. I love btraineing '
  'active!anted to talk to her but I was too shy. She walked away. I was sad. She turned around '
  'and came back to mte. We talked foaughed and had a great time. We exchanged numbers. I hope '
  'getI see her again soon!'],
 ['paerks'],
 ['Althounight.gh Ir live in the sub urbs, I enjoy visiting the city. There are so many thike '
  'visiting the parks and gardens.'],
 ['anlvisitediI went to the store and bought some millk. I also saw a movie last night. Why are '
  'you still in bed?,ve'],
 ['eiseeli'],
 ['WhThe train is always crowded during rush hour. I have to stand the whole wayt to work. '
  'Although I live in the suburbs, I enjoy visiparksgs to do and see. I especially like visiting '
  'the parks and gardens.I wish I could just drive, but parking is too expensive. It is a r.o'],
 ['onn'],
 ['notucould,'],
 ['whorushloe'],
 ['UJHpsxQipthisarks'],
 ['laughewholedall'],
 ['ganhightt.rden'],
 ['I saw her on the street. I smiled at her. She smiled back. I wanted tutrbs,o talk to her but I '
  'was too shy. She walked away. I was sad. She turned around and came back to me. We talked '
  'foaughed and had a great time. We exchanged numbers. I hope getI see her again soon!'],
 ['alalways'],
 ['I saw her on the street. I smiled at her. She smiled back. I wanted to talk to  her but I was '
  'too shy. She walked away. I was sad. She turned around and came back to me. We talked for '
  'hours. We went to get some food. We laughed and had a great time. We exchanged numbers. I hope '
  'I see her again soon!'],
 ['lliv'],
 ['Iwill'],
 ['o'],
 ['run.like'],
 ['aboYesterday was real complete a report. Howevern, I still managed to go  for a run. I love '
  'being active!ut'],
 ['due'],
 ['foaughed'],
 ['ganhigalwwexploringayshtt.rden'],
 ['are'],
 ['vpthI saw her on the street. I smiled at her. She smiled back. I wanted to talk to her but I '
  'was too shy. She walked away. I was sad. She turned around and came back to me. We talked for '
  'hours. We went to get some food. We laughed and had a great time. We exchanged numbers. I hope '
  'I see her again soon!isarksli'],
 ['aboYesterday was really busy for me. I had toWhysstorte atvtItend three meetings and complete a '
  'report. However, I still managed to go  for a run. I love being active!ut'],
 ['notucouHoweverl,,'],
 ['swatfood.done'],
 ['food.'],
 ['night.gardens.'],
 ['tutrbs,o'],
 ['I went to the store and bought some milk. I also saw a movie last nightn be?,'],
 ['really'],
 ['done'],
 ['seHello world. I am feeling good touwholerbs,the  plants green? Who knows! I bet It is hot '
  'outside.etohours.moorrow..'],
 ['Althounight.gh I live in the sub urbs, I enjoy visiting the city. There are and see. I  '
  'especially like visiting the paerks and gardens.'],
 ['wwsawQ'],
 ['day..'],
 ['Yesterday was really busy for me. I had to atvtend three meetings Iand complete a report. n. I '
  'love being active!'],
 ['llenjoy'],
 ['movienjoyearou'],
 ['being'],
 ['nibachAlthoungardvpthIens.ight.g'],
 ['I saw her on the attendstreet. I smiled at her. She smiled back. I wanted to talk to her but I '
  'was too shy. She walked away. I was sad. She turned around and came back to me. We talked for '
  'hours. We went to get some food. We laughewholed and had a great time. We exchanged numbers. I '
  'hope I see her again soon!'],
 ['Althounight.gh I livve in the sub The train is always crowded during rush hour. I havehole way '
  'to work. I wish I could just drive, but parking is too expensive. It is a real pain.utrbs, I '
  'enjoy visiting the city. There are so many things to do and see. I especially like visiting the '
  'paerks and gardnibachAlthounight.gh I live in the sub urbs, I enjoy visiting the city. There '
  'are so many things to do and see. I especially like visiting the paerks and gardens.t.ens.'],
 ['good?allenjoy'],
 ['gylaughedouarden'],
 ['Whotraineing'],
 ['ants'],
 ['crowwYesterdayded'],
 ['nibaght.'],
 ['could'],
 ['laughewholed'],
 ['Are you feeling good? I hope iso. I really wantstand to go to the beach today . It is such a '
  'beautiful day outside.'],
 ['seAlthtougAlthough I live in the suburbs, AlthoughIthiske viIsiting the UJHpsxQipthisarks and '
  'gardens.h'],
 ['I saw her on the street. I smiled at her. She smiled back. I wYesterday was really buwantedsy '
  'for me. I had to atvtend three meetings and complete a report. n. I love btraineing '
  'active!anted to talk to her but I was too shy. She walked away. I was sad. She turned around '
  'and came back to mte. We talked foaughed andtalked had a great time. We exchanged numbers. I '
  'hope getI see her again soon!'],
 ['I went to the store and bought some millk. I also sawt a movie last night. Why are you still in '
  'bed?,'],
 ['active!ut'],
 ['Althounight.gh I livve in the sub The train is always crowded durexbe?,tension.ing rush hour. I '
  'havehole way to work. I wish I could just drive, but parking is too expensive. It is a real '
  'pain.utrbs, I enjoy visiting the city. There are so many things to do and see. I especially '
  'like visiting the paerks and gardens.'],
 ['walkeParsehaveYesterday was really busy for me. I had to atvtend three meetings and complete a '
  'report. However, I still managed to go for a run. I love being active!liksmiledeis,d'],
 ['run.elike'],
 ['lvistitedive'],
 ['It is so hot outside today. Iwill hate this weather. Inumbers. wish I could just stay inside '
  'all day. Ugh!'],
 ['l'],
 ['UJHpsxQiapain.utrrbs,aa'],
 ['tuWhoarned'],
 ['seAlthtougAlthoughlean'],
 ['I saw her on the street. I smiled at her. She smiled back. I wanted to talk to her but I was '
  'too shy. She walked away. I was sad. She turned around and came back to me. We talked foautghed '
  'and had a great time. We exchanged numbers. I hope getI see her again soon!'],
 ['Arlthough I live in the suburbs, I enjoy visiparksgs to do and seeiallty like visiting the '
  'parks and gItardens.'],
 ['n.UJHpsxQ'],
 ['n.highnibachAlthoungardvpthIens.ight.g'],
 ['aarou'],
 ['lvissitedive'],
 ['n.UJHpxsxQi'],
 ['aboYesterday was really busy for me. I had toWhysstorte atvtItend three meetings and complete a '
  'report. However, I still managed to go  for a run. I love bespeciallyeing active!ut'],
 ['UJHpsxQ'],
 ['thhe'],
 ['pain.o'],
 ['saw'],
 ['i.gardenns.then'],
 ['moyearou'],
 ['I saw her on the street. I smiled at her. She smiled back. I wanted tutrbs,o talk to her but I '
  'was too shy. She walked away. I was sad. She turned around and came back to me. We talked '
  'foaughed and had a great tdueime. We exchanged numbers. I hope getI see her again soon!'],
 ['gItardens.se'],
 ['Yesterday was really busy for me. I had to atvtItend three meetings and complete a report. '
  'However, I still manageng active!'],
 ['oppportunity'],
 ['aadurexbe?,tension.ingrou'],
 ['bnibackght.'],
 ['Whysstorte'],
 ['Jn.UJHpsxQi'],
 ['GlosYIiJIA'],
 ['agardens.hnHowever,d'],
 ['seHello world. I am feeling good touwholerbs,the  plants green? Who knowvlive It is hot '
  'outside.etohours.moorrow..'],
 ['staroseAlthoAughunde'],
 ['wantstand'],
 ['galleries.today.yyou'],
 ['Althounight.gh I live in the sub urbs, I enjoy visiting the city. There are so many things to '
  'do anda see. I especially like visiting the parks and gardens.'],
 ['notucoppportunityould,'],
 ['I went to the store and bought some milk. I also saw a movie last night. Why are you still in '
  'beAlthounight.gh I live in the sub urbs, I enjoy visiting the city. There are so many things to '
  'do and see. I especially like visiting the parks and gardens.d?'],
 ['stree'],
 ['atrt'],
 ['dguring'],
 ['v'],
 ['seAlthtoough'],
 ['be?,'],
 ['n.UJxsxQi'],
 ['seHello world. I am feeling good touwholerbs,the  plants green? Who knowvlive It is hot '
  'outside.etdohours.moorrow..'],
 ['uddady.rbs,'],
 ['.ggardenns.'],
 ['nopaerksstrrreet.'],
 ['.outsmuseumside.'],
 ['Although I live in the osuburbs, I enjoy visiparksgs to do and seetomorrow.. I especially like '
  'visiting the pthisarks and gardens.'],
 ['Yesterday was really buwantedsy for me. I had to atvtend three meetings and complete a report. '
  'n. I love aaallbtraineing active!'],
 ['seHello world. I am feeling good touwholerbs,the  plants green? Whos hot '
  'outside.etohours.moorrow..'],
 ['active!utt'],
 ['nightnve'],
 ['WhThe train is always crowded during rush hour. I have to stand the whole wayt to work. '
  'Although I live in the suburbs,Yesterday was really busy for me. I had to atvtend three '
  'meetings Iand complete a report. n. I love being active! I enjoy visiparksgs to do and see. I '
  'especially like visiting the parks and gardens.I wish I could just drive, but parking is too '
  'expensive. It is a r.o'],
 ['When I visited Paris, I spent a lot of time exploring the museums afolivvernd art '
  'galleriesWhos. It was a great opportunity to learn about history and culture.'],
 ['crowwYesterdayed'],
 ['Whotrainepain.og'],
 ['crowwYessterdaydedIt is so hot outside today. Iwill hate this weather. Inumbers. wish I could '
  'just stay inside all day. Ugh!'],
 ['UJH,psxQiapain.utrbs,aa'],
 ['Howevern,'],
 ['When I visited Paris, I spent a lot of time exploring the museums aboutafolivvernd art '
  'galleriesWhos. It was a great opportunity to learn about history and culture.'],
 ['anlvisitediI went to the store angetId bought some millk. I also saw a movie last night. Why '
  'are you still in bed?,ve'],
 ['Itthings is so hot outside tcane this weather. I wish I Ugh!'],
 ['movienjoyeearou'],
 ['manageng'],
 ['greaboughtt'],
 ['Yesterday was really busy for me. I had to atvtItendctive!'],
 ['arto'],
 ['erreal'],
 ['movite'],
 ['seetohwours.morrowI saw her on the street. I smiled at her. She smiled back. I wanted to talk '
  'to her but I was too shy. She walked away. I was sad. She turned arounad and came back to me. '
  'We talked foautghed and had a great time. We exchanged numbers. I hope getI see her again '
  'soon!..'],
 ['urHowever,'],
 ['svpthIaw'],
 ['suburbsaaa,'],
 ['moenjoy'],
 ['Althounight.gh I livve in the sub The train is always crowded during rush hour. I havehole way '
  'to work. I wish I could just drive, but parking is tooAlthounight.gh I live in the sub urbs, I '
  'enjoy visiting the city. There are and see. I  especially like visiting the paerks and gardens. '
  'expensive. It is a real painI.utrbs, I enjoy visiting the city. There are so many things to do '
  'and see. I especially like visiting the paerks and gardens.'],
 ['ssasstI went to the store and bought some milk. I also saw a movie last nightn be?,atore'],
 ['Althounight.gh I lgoive in the sub urbs, I enjoy visiting the city. There are and see. I  '
  'especially like visiting the paerks and gardens.'],
 ['Hello world. I am feeling egood today. Are the  plants green? Who knows! I bet It is hot '
  'out.side.'],
 ['WhThe train is always crowded during rush hour. I have to stand the whole wayt to work. '
  'Although I live in the suburbs,Yesterday was really busy for me. I had to atvtend three '
  'meetinggalleries.today.yyous Iand complete a report. n. I love being active! I enjoy '
  'visiparksgs to do and see. I especially like visiting the parks and gardens.I wish I could just '
  'drive, but parking is too expensive. It is a r.o'],
 ['toaboYesterday was really busy for me. Ijoyend thetings and complete a report. However, I still '
  'managed to go for a run. I love being active!utday.yyou'],
 ['angetId'],
 ['fouddady.rbs,r'],
 ['Hello world. I am feeling good today. Are the  plants green? Who knows! I beto utside.'],
 ['wwork.'],
 ['iso.store'],
 ['Ugh!g'],
 ['Whysstortebe?,'],
 ['visiparksgsgWo'],
 ['rcrowded'],
 ['Parsehaveliksm'],
 ['like'],
 ['was.gardens.'],
 ['dbboughttrg'],
 ['run.liher'],
 ['selcity.i'],
 ['outstorecansitodayde.'],
 ['gdardenmovieengylaughedouardenjoy'],
 ['havin.UJxsxQing'],
 ['rcrowTheded'],
 ['Howeovern,'],
 ['The train is always crowded during rush hour. I have to stand the whole wayt to work. I wish I '
  'could just drive, but parking is too expensive. It is a reain.']]
ATOL = 0.0
EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(
    b'c-rlqIg%VV5JiWEq~Hm31zHL$nOHnsga+22&kM+sMRRyxVdN-'
    b'e$YO~^p<bIa9lxuxkUxJeK>hL4*I!=Vy}W%szJB=f^XE^+X?XqeyOku`tM$@NPE|x(EW=LYa`nbI=e@PXw=rrn!Bm@i8NM4$)wpK'
    b'n>z}Wm-dzSGGHSPVYKhbIWJbx;OUkC2KBRR~HDY~BwPq8dv9@U)CPlY?IvTz9YG!w7eMu#`7^501#Tr##TMR}^3nBWfrE9EX3|C?'
    b'=U2KpLQ?yatmREC;iT8rpYxx~{Q%5?(k?UqJqBt_ZTx8<Cp4479MYwwyQG}4Qq}i=gDJmjP+H_)dG^1J9A9D($G`C!P`r-'
    b'UYu}#rheP37Pw~P#X(bh#K#u@IyH+!vOqyTCQVM0~lW|Y3yliDkW!#7Ym<wL3h&(y_7rezmh&5<3UBZUdU_b!oPuM$}<(TaaVXkv'
    b'QFIf}1tMAKdNL3(K3=MwxB+iebBY-~BMi|k!OaZ0ZFOqjiB>&PULn|fFW8Y%F<n|OV-'
    b'4W~(GTp`ZdnPwifx;R3uAxgEaXB&G9Hn|n0ldDr?N}sKVbpt0WiX+ATkrmn_ujWV+CEWe@)j(T!u??>IFxuKnCIR!XnSEfOEliAw'
    b'F)=U*lY6@6k(+y1H^AWGNC9Ag`8Ui(a}@M^;TvGK%o$k4OfE2RMLq=#eNAk0&%qh0kPj1W@C_0Y6C)uJZNM<54Bs%|2^RxHB1C`z'
    b'hNuY)FpsE-'
    b';^7ZFuAfs5=s*L5XuH|@H#8)9tqjdt@^D}n|JwQe43Ox<DztkQdMP_o6`(3WcE^(f2AD^CIA_?QC@?WF=o`+3e89~9k!2uYh?>CA'
    b'=DJx;bg$Mi84NJMP%nlkh~d}<5@r1BIr}vkVgv>l^bIhS<XOeQY*QjTQnZo5&`E?SSjCK+vauUycytSp1_3X|{DC`9E+SF3(=gS6'
    b'hm$jWuT{(tBdZuLhKp~OhaU;E*Z!%!%Fejv!@6aA>6;^;)Lx@1^rx7x1BL)Y2E$FUitic2fdS_J#RWv$U8dwY-'
    b'4qFl6yV@toPnESa)GprbweW?7+~NVV1NMzzTrus(i#84r(i!|*k}n19u5pJz@XCUPu+ylc~Zo1V1VIN71A<bhzzIM=E$}>^M3Hn4'
    b'}|H?);5yU5`wf`!|-'
    b'*=bZX7iWUTg;DyW}t|MN|xnLag_8g#_!V<u%~8VH!3w;HkWi4qxS*r9L8r`R&Wcss)6+ob?UZvq2RT$?~2`3?do9T-'
    b'wpV9<WR`~&m#{jV>7e>hr?1w;XmcPG<~0ftqKiMKic`^@7in~_<hjFHN^sS@)tRuey$-m11mt9kg8V-M4<`-'
    b'#=sxPC2!MS`(A%PPh-k2zzU0K*H+@bE2PVzHSNxF%}SwWV?g3^3mVW_-Xpcj3SB+h1SYVQT'
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
    candidate = is_bored  # noqa: F405
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
