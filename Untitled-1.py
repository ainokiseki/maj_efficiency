import protocol_pb2

import game


g=game.game()


test=protocol_pb2.Wrapper()

with open('yq1','rb') as f:
    data=f.read()

msg=test.ParseFromString(data)

ttst=protocol_pb2.GameDetailRecords()
ttst.ParseFromString(test.data)

s=[set() for i in range(5)]
namedic={'.lq.RecordHule':0, '.lq.RecordChiPengGang':1, '.lq.RecordDealTile':2, '.lq.RecordDiscardTile':3,
 '.lq.RecordAnGangAddGang':4, '.lq.RecordNewRound':5,'':7,'.lq.RecordNoTile':6,'.lq.RecordLiuJu':8}

for index,i in enumerate(ttst.actions):
    t=protocol_pb2.Wrapper()
    t.ParseFromString(i.result)
    num=namedic[t.name]
    
    #print("num is:",num)

    if num==0:
        hl=protocol_pb2.RecordHule()
    elif num==1:
        hl=protocol_pb2.RecordChiPengGang()
        hl.ParseFromString(t.data)
        tilelist=[hl.tiles[i] for i in range(len(hl.tiles)) if hl.tiles[i]==hl.seat]
        g.cpg(hl.seat,tilelist)
    elif num==2:
        hl=protocol_pb2.RecordDealTile()
        hl.ParseFromString(t.data)
        #print(hl)
        g.draw(hl.seat,hl.tile)
        if len(hl.doras)>0:
            g.openview(hl.doras[-1])
            print('add dora')

    elif num==3:
        hl=protocol_pb2.RecordDiscardTile()
        hl.ParseFromString(t.data)

        g.discard(hl.seat,hl.tile,hl.is_liqi)
        print(hl.tile,index,hl.is_liqi)

        if(index==161):
            print(hl)
        
    elif num==4:
        #type=2为加杠，type=4为暗杠
        hl=protocol_pb2.RecordAnGangAddGang()
    elif num==5:
        hl=protocol_pb2.RecordNewRound()
        hl.ParseFromString(t.data)
        haj=[hl.tiles0]+[hl.tiles1]+[hl.tiles2]+[hl.tiles3]
        g.start(haj,hl.doras[0])

        #print(hl)
    else:
        continue

#print(g.player[2].errorlog)
for i in g.player[0].errorlog:
    if i['type']=='tuixiangting':
        print(i)
print('====================')
for i in g.player[1].errorlog:
    if i['type']=='tuixiangting':
        print(i)
print('====================')
for i in g.player[2].errorlog:
    if i['type']=='tuixiangting':
        print(i)
print('====================')
for i in g.player[3].errorlog:
    if i['type']=='tuixiangting':
        print(i)
    #print(g)
    #print(g.publicview)