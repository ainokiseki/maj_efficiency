catdic={'m':0,'p':1,'s':2,'z':3}
catrdic={0:'m',1:'p',2:'s',3:'z'}

class card():
    def __init__(self):
        self.data=[[0]*9,[0]*9,[0]*9]+[[0]*7]

    def __str__(self):

        return self.d2s(self.data)
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
                res+=str(j+1)*x[i][j]
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
    def __str__(self):
        print(self.name,self.shoupai)
        return ''
    def draw(self,x):
        self.shoupai.addcard(x)
        self.view.addcard(x)
    def discard(self,x):
        self.shoupai.dropcard(x)
    

class game():
    def __init__(self):
        self.player=[player(i,self) for i in range(4)]
        self.publicview=card()
        self.step=0
    def __str__(self):
        for i in self.player:
            print(i)
        return ''
    def draw(self,num,x):
        self.player[num].draw(x)
    def discard(self,num,x):
        self.player[num].discard(x)
        self.publicview.addcard(x)
    def openview(self,x):
        if isinstance(x,list):
            for i in x:
                self.publicview.addcard(i)
        else:
            self.publicview.addcard(x)
    def start(self,x,dora):
        for i in range(4):
            for j in x[i]:
                self.player[i].draw(j)
        self.openview(dora)

    