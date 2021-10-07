from os import stat
import analyzer
import copy
catdic={'m':0,'p':1,'s':2,'z':3}
catrdic={0:'m',1:'p',2:'s',3:'z'}

class card():

    def __init__(self):
        self.data=[[0]*9,[0]*9,[0]*9]+[[0]*7]

    def __str__(self):

        return self.d2s(self)
    def  __add__(self,rhs):
        return [[self.data[i][j]+rhs.data[i][j] for j in range(len(self.data[i]))] for i in range(len(self.data))]
    @staticmethod
    def num2s(x):

        
        return str(x%9+1)+catrdic[x//9]
    @staticmethod
    def s2num(x):
        i=int(x[0])-1
        if i==-1:
            i=4
        return catdic[x[1]]*9+i
    @staticmethod
    def s2n(x):
        i=int(x[0])-1
        if i==-1:
            i=4
        return (catdic[x[1]],i)
    def addcard(self,x):
        i,j=self.s2n(x)
        self.data[i][j]+=1
    def dropcard(self,x):
        i,j=self.s2n(x)
        self.data[i][j]-=1
    @staticmethod
    def d2s(x):
        res=''
        for i in range(4):
            for j in range(9):
                if i==3 and j>=7:
                    break
                res+=str(j+1)*x.data[i][j]
            res+=catrdic[i]
        return res


class player():
    def __init__(self,name,game):
        self.xun=0
        self.name=name
        self.shoupai=card()
        self.view=card()
        self.effi=1
        self.errorlog=[]
        self.game=game
        self.paixiao={
            0:[],
            1:[],
            2:[],
            3:[],
            4:[],
            5:[],
            6:[],
            7:[]
        }
        self.mznum=0
        self.xtnum=0
        self.step=0
    def reset(self):
        self.shoupai=card()
        self.view=card()
        self.xun=0
        self.mznum=0
        self.xtnum=0
        self.step=0
    def __str__(self):
        print(self.name,self.shoupai)
        return ''
    def draw(self,x=None):

        self.shoupai.addcard(x)
        self.view.addcard(x)
    def removecard(self,x):
        self.shoupai.dropcard(x)
        self.view.dropcard(x)
    def discard(self,x):
        self.step+=1
        if not self.game.liqiflag:
            self.count(x)
        self.shoupai.dropcard(x)
        self.view.dropcard(x)

    def count(self,x):
        self.jinzhang_count={}
        shiye=self.game.publicview+self.view
        #print(shiye)
        a=analyzer.analyzer()
        a.analyze(self.shoupai.data,self.mznum)
        # print("jz",a.jinzhang)
        # print(a.qiezhang)
        jinzhang_count={}

        for i,j in a.jinzhang.items():
            countnum=sum([4-shiye[k//9][k%9] for k in j])
            jinzhang_count[i]=countnum
        #print([jinzhang_count[i] for i in jinzhang_count])
        maxjinzhang=max([jinzhang_count[i] for i in jinzhang_count])
        best=[card.num2s(i) for i in jinzhang_count if jinzhang_count[i]==maxjinzhang]

        xnum=card.s2num(x)
        
        if xnum not in jinzhang_count:
            err={
                'jushu':self.game.gamenum,
                'xunmu':self.step,
                'type':'tuixiangting',
                'situation':card.d2s(self.shoupai),
                'drop':x,
                'best':','.join(best)
            }
            self.errorlog.append(err)
            #print('shimata!')
            #print(err)
        elif jinzhang_count[xnum]<maxjinzhang:
            err={
                'jushu':self.game.gamenum,
                'xunmu':self.step,
                'type':'dipaixiao',
                'situation':card.d2s(self.shoupai),
                'drop':x,
                'best':','.join(best),
                'jinzhangnum':maxjinzhang,
                'mynum':jinzhang_count[xnum]
            }
            self.errorlog.append(err)
            #print('shimata!')
            #print(err)
            xtnum=a.minxt
            self.paixiao[xtnum].append(jinzhang_count[xnum]/maxjinzhang)
        else:
            #print('best paixiao!bang bang bang bang~')
            #print(card.d2s(self.shoupai))
            #print(x)
            pass

class game():
    def __init__(self):
        self.player=[player(i,self) for i in range(4)]
        self.publicview=card()
        self.step=0
        self.liqiflag=False
        self.gamenum=0
    def __str__(self):
        for i in self.player:
            print(i)
        return ''
    def draw(self,num,x):
        self.player[num].draw(x)
    def discard(self,num,x,is_liqi):
        self.step+=1
        if is_liqi==True:
            self.liqiflag=True
        self.player[num].discard(x)
        self.publicview.addcard(x)

    def openview(self,x):
        if isinstance(x,list):
            for i in x:
                self.publicview.addcard(i)
        else:
            self.publicview.addcard(x)
    def cpg(self,num,xlist):
        for i in xlist:
            self.player[num].removecard(i)
            self.publicview.addcard(i)
        self.player[num].mznum+=1
    def dora(self,x):
        self.openview(x)

    def start(self,x,dora):
        self.gamenum+=1
        self.step=0
        self.liqiflag=False

        self.publicview=card()
        for i in range(4):
            self.player[i].reset()

        for i in range(4):
            for j in x[i]:
                self.player[i].draw(j)
        self.openview(dora)


