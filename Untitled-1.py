import protocol_pb2

import game


g=game.game()


test=protocol_pb2.Wrapper()

with open('210','rb') as f:
    data=f.read()

msg=test.ParseFromString(data)

ttst=protocol_pb2.GameDetailRecords()
ttst.ParseFromString(test.data)

s=[set() for i in range(5)]
namedic={'.lq.RecordHule':0, '.lq.RecordChiPengGang':1, '.lq.RecordDealTile':2, '.lq.RecordDiscardTile':3,
 '.lq.RecordAnGangAddGang':4, '.lq.RecordNewRound':5,'':6}
for i in ttst.actions[10:12]:
    t=protocol_pb2.Wrapper()
    t.ParseFromString(i.result)
    num=namedic[t.name]
    print(num)
    if num==0:
        hl=protocol_pb2.RecordHule()
        
    elif num==1:
        hl=protocol_pb2.RecordChiPengGang()
    elif num==2:
        hl=protocol_pb2.RecordDealTile()
        hl.ParseFromString(t.data)
        print(hl)
        print(hl.seat)
    elif num==3:
        hl=protocol_pb2.RecordDiscardTile()
        hl.ParseFromString(t.data)
        #print(hl)
    elif num==4:
        hl=protocol_pb2.RecordAnGangAddGang()
    elif num==5:
        hl=protocol_pb2.RecordNewRound()
        hl.ParseFromString(t.data)
        haj=[hl.tiles0]+[hl.tiles1]+[hl.tiles2]+[hl.tiles3]
        g.start(haj,hl.doras[0])
        print(hl)
    else:
        continue

    #print(g)
    #print(g.publicview)