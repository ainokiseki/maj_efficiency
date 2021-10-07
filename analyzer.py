import copy
class analyzer:
    def __init__(self):
        self.minxt=7
        self.record=[]
        self.qiezhang=set()
        self.jinzhang={}
        self.huleflag=False
        self.mznum=0
    @staticmethod
    def setunion(x):
        res=set()
        for i in x:
            res=res.union(i)
        return res
    @staticmethod
    def makedazi(x):
        res=set()
        res.add(x)
        if x<27:
            for i in range(0,5):
                if (x+i-2)%9==x%9+i-2:
                    res.add(x+i-2)
        return res
    def dfs(self,x,dazi,mianzi,quetou,sanpai):
        def brk():
            if(len(quetou)==1):
                xtnum=3-self.mznum-len(mianzi)
            else:
                xtnum=4-len(mianzi)-self.mznum
            if len(dazi)<4-len(mianzi)-self.mznum:
                xtnum+=4-len(mianzi)-self.mznum-len(dazi)



            if xtnum<=self.minxt:
                if xtnum<self.minxt:
                    self.minxt=xtnum
                    self.record=[]
                    self.qiezhang=set()
                    self.jinzhang={}
                self.record.append({
                    'mianzi':tuple(mianzi),
                    'quetou':tuple(quetou),
                    'dazi':tuple(dazi),
                    'xtnum':xtnum,
                    'sanpai':copy.deepcopy(x)
                })

                jinzhang=set()
                for k in dazi:
                    if k[0]==k[1]:
                        jinzhang.add(k[0])
                    elif k[0]==k[1]-2:
                        jinzhang.add(k[0]+1)
                    else:
                        if k[0]%9!=0:
                            jinzhang.add(k[0]-1)
                        if k[1]%9!=8:
                            jinzhang.add(k[1]+1)
                qiezhang=[]
                for i in range(0,4):
                    for j in range(0,9):
                        if i==3 and j>=7:
                            break
                        for k in range(0,x[i][j]):
                            qiezhang.append(i*9+j)
                if len(dazi)<5-len(quetou)-len(mianzi)-self.mznum:
                    for i in range(len(qiezhang)):
                        if qiezhang[i] not in self.jinzhang:
                            self.jinzhang[qiezhang[i]]=set()
                        self.jinzhang[qiezhang[i]]=self.jinzhang[qiezhang[i]].union(self.setunion([self.makedazi(qiezhang[j]) for j in range(len(qiezhang)) if j!=i]))                  
                for i in qiezhang:
                    if i not in self.jinzhang:
                        self.jinzhang[i]=set()
                    self.jinzhang[i]=self.jinzhang[i].union(jinzhang)
                            


                                

            return False

        if len(mianzi)+self.mznum==4 and len(quetou)==1:
            self.huleflag=True
            return

        #全都没有，开始计算向听数
        if len(dazi)+len(mianzi)+self.mznum==4 :
            return brk()

        if len(quetou)==0:
            for i in range(0,4):
                for j in range(0,9):
                    if i==3 and j>=7:
                        break
                    if x[i][j]>=2:
                        x[i][j]-=2
                        quetou.append(i*9+j)
                        self.dfs(x,dazi,mianzi,quetou,sanpai)
                        quetou.pop()
                        x[i][j]+=2
        for i in range(0,4):
            for j in range(0,9):
                if i==3 and j>=7:
                     break
                if x[i][j]>=3:
                    x[i][j]-=3
                    mianzi.append(tuple([i*9+j,i*9+j,i*9+j]))
                    self.dfs(x,dazi,mianzi,quetou,sanpai)
                    mianzi.pop()
                    x[i][j]+=3

        for i in range(0,3):
            for j in range(0,7):
                if x[i][j]>0 and x[i][j+1]>0 and x[i][j+2]>0:
                    x[i][j]-=1
                    x[i][j+1]-=1
                    x[i][j+2]-=1
                    mianzi.append(tuple([i*9+j,i*9+j+1,i*9+j+2]))
                    self.dfs(x,dazi,mianzi,quetou,sanpai)
                    mianzi.pop()
                    x[i][j]+=1
                    x[i][j+1]+=1
                    x[i][j+2]+=1

        #对子搭子
        for i in range(0,4):
            for j in range(0,9):
                if i==3 and j>=7:
                     break
                if x[i][j]>=2:
                    x[i][j]-=2
                    dazi.append(tuple([i*9+j,i*9+j]))
                    self.dfs(x,dazi,mianzi,quetou,sanpai)

                    dazi.pop()
                    x[i][j]+=2
        
        #普通搭子
        for i in range(0,3):
            for j in range(0,7):
                if (x[i][j]>0) + (x[i][j+1]>0)+ (x[i][j+2]>0)==2:
                    dazilist=[i*9+j+k for k in range(0,3) if x[i][j+k]>0]

                    x[i][j]-=(x[i][j]>0)
                    x[i][j+1]-=(x[i][j+1]>0)
                    x[i][j+2]-=(x[i][j+2]>0)

                    dazi.append(tuple(dazilist))
                    self.dfs(x,dazi,mianzi,quetou,sanpai)
                    dazi.pop()
                    x[i][dazilist[0]-i*9]+=1
                    x[i][dazilist[1]-i*9]+=1
        


        return brk()



    
    def analyze(self,x,mznum=0):

        self.mznum=mznum

        avaliable=set()
        dazi=[]
        mianzi=[]
        quetou=[]


        sanpai=copy.deepcopy(x)

        qidui=[]
        xtest=copy.deepcopy(x)
        for i in range(0,4):
            for j in range(0,9):
                if i==3 and j>=7:
                    break
                if xtest[i][j]>=2:
                    xtest[i][j]-=2
                    qidui.append(i*9+j)
        self.minxt=6-len(qidui)
        qiezhang=[]
        for i in range(0,4):
            for j in range(0,9):
                if i==3 and j>=7:
                    break
                if xtest[i][j]>0 and (i*9+j) not in  qidui:
                    qiezhang.append(i*9+j)
        for i in qiezhang:
            self.jinzhang[i]=set([j for j in qiezhang if j!=i])


        self.dfs(x,dazi,mianzi,quetou,sanpai)
        #print(self.record)
        


        sanpai=sanpai[0]+sanpai[1]+sanpai[2]+sanpai[3]
        for i,j in self.jinzhang.items():
            count=sum([4-sanpai[i] for i in j])
            #print(i,j,count)
        #print (self.jinzhang)
        #print(self.minxt)
def n2p(x):
    catdic={0:'m',1:'p',2:'s',3:'z'}
    return str(x%9+1)+catdic[x//9]
def trans_analyze(x):
    ls={}
    
    inp=[[0]*9,[0]*9,[0]*9,[0]*7]
    catdic={'m':0,'p':1,'s':2,'z':3}
    for i in x:
        if i in catdic:
            for j,k in ls.items():
                inp[catdic[i]][j]+=k
            ls={}
        else:
            y=int(i)-1
            if y==-1:
                y=4
            if y not in ls:
                ls[y]=0
            ls[y]+=1
    a=maj()
    print(inp)
    a.analyze(inp)
    print('xiangting is:',a.minxt)
    sanpai=inp[0]+inp[1]+inp[2]+inp[3]
    prtlist=[]
    for i,j in a.jinzhang.items():
        st=''
        j=sorted(list(j))
        count=sum([4-sanpai[i] for i in j])
        st+=n2p(i)+':'
        st+=' '.join([n2p(k) for k in j])
        st+=',count is:'+str(count)
        prtlist.append((st,count))
    prtlist=sorted(prtlist,key= lambda x:-x[1])
    for i in prtlist:
        print(i[0])
    
    #print(a.record)
        
        #print(i,j,count)

