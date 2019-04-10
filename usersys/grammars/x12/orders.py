from bots.botsconfig import *

syntax = {}

structure = [
{ID:'message',MIN:0,MAX:99999,LEVEL:[
    {ID:'partys',MIN:0,MAX:99999,LEVEL:[
        {ID:'party',MIN:0,MAX:99999},
    ]},
    {ID:'lines',MIN:0,MAX:99999,LEVEL:[
        {ID:'line',MIN:0,MAX:99999,LEVEL:[
            {ID:'details',MIN:0,MAX:99999},
        ]},
    ]},
]},
]

recorddefs = {
    'message':[
            ['BOTSID','M',255,'A'],
            ['sender', 'M', 35, 'AN'],
            ['receiver', 'M', 35, 'AN'],
            ['testindicator', 'C', 3, 'AN'],
            ['docsrt', 'C', 3, 'AN'],
            ['docnum', 'M', 35, 'AN'],
            ['docdtm', 'C', 35, 'AN'],
            ['deldtm', 'C', 35, 'AN'],
            ['earldeldtm', 'C', 35, 'AN'],
            ['latedeldtm', 'C', 35, 'AN'],
            ['currency', 'C', 3, 'AN'],
          ],
    'partys':[
            ['BOTSID','M',255,'A'],
          ],
    'party':[
            ['BOTSID','M',255,'A'],
            ['qual', 'C', 3, 'AN'],
            ['gln', 'C', 13, 'AN'],
            ['DUNS', 'C', 13, 'AN'],
            ['internalID', 'C', 17, 'AN'],
            ['externalID', 'C', 17, 'AN'],
            ['name1', 'C', 70, 'AN'],
            ['name2', 'C', 70, 'AN'],
            ['address1', 'C', 70, 'AN'],
            ['address2', 'C', 70, 'AN'],
            ['city', 'C', 70, 'AN'],
            ['pcode', 'C', 17, 'AN'],
            ['state', 'C', 35, 'AN'],
            ['country', 'C', 3, 'AN'],
          ],
    'lines':[
            ['BOTSID','M',255,'A'],
          ],
    'line':[
            ['BOTSID','M',255,'A'],
            ['linenum', 'C', 6, 'AN'],
            ['gtin', 'C', 14, 'AN'],
            ['suart', 'C', 35, 'AN'],
            ['byart', 'C', 35, 'AN'],
            ['ordqua', 'C', 20, 'R'],
            ['ordunit', 'C', 3, 'AN'],
            ['desc', 'C', 70, 'AN'],
            ['price', 'C', 20, 'R'],
          ],
     }
 
