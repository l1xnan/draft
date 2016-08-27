#!/usr/bin/python3
#coding:utf-8
"""
    这是一个用来使用SmartQQ的模块
    这也是我用Python正式编写的第一个代码
    送给常来我站点的朋友们
    Code By OET//183
    Blog    HexBlog.Net
"""
import os
#import curses
from urllib import request,response,parse
import requests
from time import sleep
import json
class SmartQQ(object):
#    初始化
    def __init__(self):
        print("SmartQQ 已经启动...")
        #    读取脚本路径并保存
        self.__path=os.getcwd()

        #    定义一个全局Cookie，用来保存Cookie字符串
        self.__cookie=""

        #    定义ptwebqq，这个以后常用
        self.__ptwebqq=""

        #    定义vfwebqq，获取好友及群列表使用
        self.__vfwebqq=""

        #    定义一个hash用与获取好友及群列表
        self.__hash=""

        #    定义登录UIN
        self.__uin=""

        #    定义一个全局的Header，用来模拟浏览器请求头
        self.__header={
            "User-Agent":"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
            "Referer":"",
            "Cookie":""
        }
        #    创建一个全局的opener
        self.__redirect=request.HTTPRedirectHandler()
        #    这么干....不说了
        self.__redirect.redirect_request=self.__redirect_request
        opener=request.build_opener(self.__redirect,request.HTTPRedirectHandler)
        #    安装全局屏蔽掉302跳转
        request.install_opener(opener)

    #----------------------------------------------------------------------
    #    用于记录cookie
    def __readCookie(self,res):
        for key,value in res.info().items():
            if(key=="Set-Cookie"):
                self.__cookie+=value[:value.find(";")+1]

    #----------------------------------------------------------------------
    #    记录跳转后的Cookie，否则无法记录
    def __redirect_request(self, req, fp, code, msg, headers, newurl):
        #    记录跳转后的Cookie，这真的挺牛掰的
        self.__readCookie(fp)

    #----------------------------------------------------------------------
    #    定义一个Http方法用于获取网页内容
    #    并且将Cookie保存下来
    def __http(self,url,referer="",data=None,bit=False ):

        #    更新headers内容
        self.__header["Referer"]=referer
        self.__header["Cookie"]=self.__cookie
        req=request.Request(url=url,data=data,headers=self.__header)

        try:
            res=request.urlopen(req)
        #    Python3中已经将错误语法进行转变，原来的,修改长了 as
        except request.HTTPError as  e:
            print("Http Error:%s" %e.code)
            return None
        #    读取Cookie并保存
        self.__readCookie(res)
        #    返回读取的字节流
        result=res.read()
        if(not bit):
            return result.decode("utf8")
        else:
            return result

    #----------------------------------------------------------------------
    #    下载二维码
    def __ptqrshow(self):
        png= self.__http(url="https://ssl.ptlogin2.qq.com/ptqrshow?appid=501004106&e=0&l=M&s=5&d=72&v=4&t=0.4139144900254905",
                         referer="",
                         data=None,
                         bit=True)
        if(png!=None):
            pngfile=open(self.__path+"/temp.png","wb")
            pngfile.write(png)
            pngfile.close()
            print("二维码下载完毕，请打开扫描...")
            return True
        else:
            print("二维码下载失败，请检查网络...")
            return False

    #----------------------------------------------------------------------
    #    进行循环检测认证进度
    def __ptqrlogin(self):
        html=self.__http("https://ssl.ptlogin2.qq.com/ptqrlogin?webqq_type=10&remember_uin=1&login2qq=1&aid=501004106"+
                         "&u1=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10&ptredirect=0&ptlang=2052"+
                         "&daid=164&from_ui=1&pttype=1&dumy=&fp=loginerroralert&action=0-0-4088&mibao_css=m_webqq&t=undefined"+
                         "&g=1&js_type=0&js_ver=10145&login_sig=&pt_randsalt=0",
                         "https://ui.ptlogin2.qq.com/cgi-bin/login")
        if(html!=None):
            temp=html.find("登录成功")
            if(temp==-1):
                #print(html)
                sleep(1)
                #    递归继续登录，一定要return 进行调用，否则无返回值
                return self.__ptqrlogin()
            elif(temp!=-1):
                #    进行二次登录验证
                #print(self.__cookie)
                return self.__check_sig(html[html.find("http"):html.find("','0','登录成功！'")])
            else:
                return False
        else:
            return False


    #----------------------------------------------------------------------
    #    再一次进行登录验证
    def __check_sig(self,url):
        html=self.__http(url=url,referer="https://ui.ptlogin2.qq.com/cgi-bin/login")
        if(html!=None):
            temp=self.__cookie.find("ptwebqq")+8;
            self.__ptwebqq=self.__cookie[temp:self.__cookie.find(";",temp)]
            #    打印ptwebqq
            #print(self.__ptwebqq)
            #    获取vfwebqq
            self.__getvfwebqq()

            return self.__login2()
        else:
            return False


    #----------------------------------------------------------------------
    #    获取vfwebqq用于获取好友及群列表
    def __getvfwebqq(self):
        html=self.__http(url="http://s.web2.qq.com/api/getvfwebqq?ptwebqq="+self.__ptwebqq+"&clientid=53999199&psessionid=&t=1446710396202",
                         referer="http://d.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1")
        if(html!=None):
            #    尝试用Json解析
            jsn=json.loads(html)
            self.__vfwebqq=jsn["result"]["vfwebqq"]

    #----------------------------------------------------------------------
    #    最后一次登录验证，如果成功即便是成功了
    def __login2(self):
        #    此处需要直接进行编码，否则返回100001，
        data="r=%7B%22ptwebqq%22%3A%22"+self.__ptwebqq+"%22%2C%22clientid%22%3A53999199%2C%22psessionid%22%3A%22%22%2C%22status%22%3A%22online%22%7D"

        html=self.__http(url="http://d1.web2.qq.com/channel/login2",
                         referer="http://d.web2.qq.com/proxy.html?v=20130916001&callback=1&id=2",
                         data=data.encode(encoding="utf8"))
        if (html==None):
            return False
        #    尝试使用Json
        jsn=json.loads(html)
        if(jsn["retcode"]==0):
            #    获取登录UID及计算friendshash
            self.__uin=jsn["result"]["uin"]
            self.__hash= self.__friendsHash(self.__uin,self.__ptwebqq)
            #    登录成功，可以获取好友及群列表
            self.__get_user_friends2()
            return True
        else:
            return False
    #----------------------------------------------------------------------
    #    为了获取好友，我们需要计算好友的Hash
    def __friendsHash(self,X,K):
        #    本段代码完全参考腾讯的JS进行编写,只不过我现在爱上了Python
        N=[0 for x in range(4)]
        V=[0 for x in range(4)]
        U=[0 for x in range(8)]
        #    字符串转换为字符数组
        k=K.encode(encoding="UTF8")
        n=["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
        for x in range(len(k)):
            N[x%4]^=k[x]
        x=int(X)
        V[0] = x >> 24 & 255 ^ 69;
        V[1] = x >> 16 & 255 ^ 67;
        V[2] = x >> 8 & 255 ^ 79;
        V[3] = x & 255 ^ 75;
        for x in range(8):
            U[x]=(x%2==0) and N[x>>1] or V[x>>1]
        result=""
        for x in U:
            result+=n[x>>4&15]
            result+=n[x&15]
        return result

    #    拉取好友列表http://s.web2.qq.com/api/get_user_friends2
    def __get_user_friends2(self):
        data="r=%7B%22vfwebqq%22%3A%22"+self.__vfwebqq+"%22%2C%22hash%22%3A%22"+self.__hash+"%22%7D"
        html=self.__http(url="http://s.web2.qq.com/api/get_user_friends2",
                         referer="http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1",
                         data=data.encode(encoding="utf8"))
        if(html!=None):
            #    记录好友列表
            jsn=json.loads(html)
            if(jsn["retcode"]==0):
                #    正确返回列表后
                for x in jsn["result"]["marknames"]:
                    print (x["markname"])


    #----------------------------------------------------------------------
    #    执行代码
    def run(self):
        #    下载二进制二维码图像
        if(self.__ptqrshow()):
            if(self.__ptqrlogin()):
                print("登录成功...")


    #----------------------------------------------------------------------
    #   销毁
    def __del__(slef):
        print("SmartQQ 已经退出...")


if  __name__ == '__main__':
    qq=SmartQQ()
    qq.run()
    x=input()
    del qq