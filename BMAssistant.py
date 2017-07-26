#-*- coding:utf-8 -*-
import wx
import webbrowser
import shelve
import dbhash

'''基本功能：
(1)按钮区：
'增加书签':弹出新窗口，输入，名称，网址，然后保存
'删除书签':弹出窗口，输入书签名，确认后删除
'退出按钮':结束程序
(2)书签区：
'书签按钮’:每个书签一个按钮，点击后打开网页

'''

class AddButtonFrame(wx.Frame):     #添加书签窗口
    def __init__(self):
        wx.Frame.__init__(self,None,-1,'Add',size=(400,350))
        panel=wx.Panel(self,-1)
        self.Text1=wx.StaticText(panel,label='Name:',   #静止文本wx.StaticText
                                pos=(40,80),size=(40,25))
        self.TextCtrl1=wx.TextCtrl(panel,pos=(80,80),size=(250,25))
        self.Text2=wx.StaticText(panel,label='URL:',
                                 pos=(40,120),size=(40,25))
        self.TextCtrl2=wx.TextCtrl(panel,pos=(80,120),size=(250,25))
        self.Button1=wx.Button(panel,-1,'Save',pos=(90,200),size=(100,50))
        self.Button2=wx.Button(panel,-1,'Exit',pos=(205,200),size=(100,50))
        self.Bind(wx.EVT_BUTTON,self.SaveClick,self.Button1)
        self.Bind(wx.EVT_BUTTON,self.QuitClick,self.Button2)

    def SaveClick(self,event):      #保存事件
        Name=str(self.TextCtrl1.GetValue()) #注意要用str()转换为字符串
        URL=str(self.TextCtrl2.GetValue())
        
        database=shelve.open(r'F:\FavouriteWeb.dat')    
        l=len(database)
        database.close()
        if l ==25 or l>25:   #判断书签是否过多
            raise Exception('Database Overload')

        database=shelve.open(r'F:\FavouriteWeb.dat')
        database[Name]=URL
        database.close()
        self.Destroy()      #关闭增加书签窗口
        win.Destroy()       #关闭主界面
        main()              #重启主界面(即刷新主界面)
        
        
    def QuitClick(self,event):
        self.Destroy()

    
class DelButtonFrame(wx.Frame):     #删除书签窗口
    def __init__(self):
        wx.Frame.__init__(self,None,-1,'Del',size=(400,300))
        panel=wx.Panel(self,-1)
        self.Text=wx.StaticText(panel,label="Name:",pos=(40,80),
                                size=(40,25))
        self.TextCtrl=wx.TextCtrl(panel,pos=(80,80),size=(250,25))
        self.Button1=wx.Button(panel,-1,'Del',pos=(90,150),size=(100,50))
        self.Button2=wx.Button(panel,-1,'Exit',pos=(205,150),size=(100,50))
        self.Bind(wx.EVT_BUTTON,self.DelClick,self.Button1)
        self.Bind(wx.EVT_BUTTON,self.QuitClick,self.Button2)

    def DelClick(self,event):   #删除事件
        Name=str(self.TextCtrl.GetValue())
        database=shelve.open(r'F:\FavouriteWeb.dat')
        try:                    #尝试着删除用户希望删除的书签
            database.pop(Name)
        finally:                #不管有没有删除成功，都执行以下操作：
            database.close()    #关闭数据库
            self.Destroy()      #关闭删除书签窗口
            win.Destroy()       #关闭主界面
            main()              #重启主界面(即刷新主界面)
        
    def QuitClick(self,event):
        self.Destroy()


def main():         #程序主体
    app=wx.App()
    global win      #按钮事件win.Destroy()重置主界面，因此使用全局变量
    win=wx.Frame(None,title='BookMark Asisitance',size=(500,500))
    panel=wx.Panel(win,-1)

    addButton=wx.Button(panel,-1,label='Add',pos=(420,50),size=(50,50))
    addButton.Bind(wx.EVT_BUTTON,addButtonClick)    #添加按钮

    delButton=wx.Button(panel,-1,label='Del',pos=(420,100),size=(50,50))
    delButton.Bind(wx.EVT_BUTTON,delButtonClick)    #删减按钮

    exitButton=wx.Button(panel,-1,label='Exit',pos=(420,150),size=(50,50))
    exitButton.Bind(wx.EVT_BUTTON,exitButtonClick) #删减按钮


    database=shelve.open(r'F:\FavouriteWeb.dat')
    nameList=database.keys()
    database.close() #及时关闭数据库   
    nameList.sort()  #sort()方法没有返回值，不能nameList=nameList.sort()

    global BMdict    #事件BookMarkClick()中使用
    BMdict={}
    try:             #try/except避免数据库为空时出错
        for i in range(1,len(nameList)+1):  #从label1 开始
            BMdict['label'+str(i)]=nameList[i-1]
    except:pass

    try:             #try/except避免数据库长度为25时出错
        for i in range(len(nameList)+1,26):
            BMdict['label'+str(i)]='Free'   #空闲书签标记
    except:pass
    
    for i in range(1,6):    #通过lambada 的方法传递多个参数到事件函数
        BMButtoni=wx.Button(panel,label=BMdict['label'+str(i)],
                            pos=(10+75*(i-1),10),size=(75,75))
        BMButtoni.Bind(wx.EVT_BUTTON,
                       lambda event,mark=i:BookMarkClick(event,mark))
    for i in range(6,11):
        BMButtoni=wx.Button(panel,label=BMdict['label'+str(i)],
                            pos=(10+75*(i-6),95),size=(75,75))
        BMButtoni.Bind(wx.EVT_BUTTON,
                       lambda event,mark=i:BookMarkClick(event,mark))
    for i in range(11,16):
        BMButtoni=wx.Button(panel,label=BMdict['label'+str(i)],
                            pos=(10+75*(i-11),180),size=(75,75))
        BMButtoni.Bind(wx.EVT_BUTTON,
                       lambda event,mark=i:BookMarkClick(event,mark))
    for i in range(16,21):
        BMButtoni=wx.Button(panel,label=BMdict['label'+str(i)],
                            pos=(10+75*(i-16),265),size=(75,75))
        BMButtoni.Bind(wx.EVT_BUTTON,
                       lambda event,mark=i:BookMarkClick(event,mark))
    for i in range(21,26):
        BMButtoni=wx.Button(panel,label=BMdict['label'+str(i)],
                            pos=(10+75*(i-21),350),size=(75,75))
        BMButtoni.Bind(wx.EVT_BUTTON,
                       lambda event,mark=i:BookMarkClick(event,mark))

    win.Show()
    app.MainLoop()
    
def BookMarkClick(event,mark):  #书签按钮点击事件
    try:
        Name=BMdict['label'+str(mark)]  #从BMdict字典中获取label对应的书签名
        database=shelve.open(r'F:\FavouriteWeb.dat')
        URL=database[Name]
        database.close()
        webbrowser.open(URL)
    except:pass             #try/except略过点击空闲书签时的出错
    
def addButtonClick(event):  #增加书签按钮点击事件
    ABF=AddButtonFrame()
    ABF.Show()  

def delButtonClick(event):  #删除书签按钮点击事件
    DBF=DelButtonFrame()
    DBF.Show()

def exitButtonClick(event): #退出按钮点击事件
    win.Destroy()
    
if __name__=='__main__':
    main()
