#  我真诚地保证：
#  我自己独立地完成了整个程序从分析、设计到编码的所有工作。
#  如果在上述过程中，我遇到了什么困难而求教于人，那么，我将在程序实习报告中
#  详细地列举我所遇到的问题，以及别人给我的提示。
#  在此，我感谢王慧老师对我的启发和帮助。下面的报告中，我还会具体地提到
#  他们在各个方法对我的帮助。
#  我的程序里中凡是引用到其他程序或文档之处，
#  例如教材、课堂笔记、网上的源代码以及其他参考书上的代码段,
#  我都已经在程序的注释里很清楚地注明了引用的出处。

#  我从未没抄袭过别人的程序，也没有盗用别人的程序，
#  不管是修改式的抄袭还是原封不动的抄袭。
#  我编写这个程序，从来没有想过要去破坏或妨碍其他计算机系统的正常运转。
#  <何玮>

from django.http import HttpResponse
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import json

#获取json格式数据
def getInfo(url,form_data):
    temp=requests.post(url,form_data)
    res=temp.json()
    return res

#爬取网页表格里的所有内容
def getDetail(url,form_data):
    list=[]
    temp=requests.post(url,form_data)
    soup = BeautifulSoup(temp.text, 'lxml')

    #判断结果为不为空
    wu = soup.select(
        'body > div.main-wrapper > div.container.clearfix > div > div.zsml-list-box > table > tbody > tr > td')
    if wu[0].string=='很抱歉，没有找到您要搜索的数据！':
        return list
    else:
        #计算有表格有多少页
        total=soup.select('body > div.main-wrapper > div.container.clearfix > div > div.zsml-page-box > ul > li > a')
        max = 0
        for item in total:
            str = item.string
            if str.isdigit():
                if int(str) > max:
                    max = int(str)

        #从表格的第一页开始爬取
        cur = 1
        while True:
            form_data['pageno'] = cur
            res = requests.post(url, form_data)
            soup = BeautifulSoup(res.text, 'lxml')
            mc = soup.select('#form3 > a')
            addr = soup.select(
                'body > div.main-wrapper > div.container.clearfix > div > div.zsml-list-box > table > tbody > tr > td:nth-child(2)')
            len1 = len(mc)
            i = 0
            while True:
                href = "http://127.0.0.1:8000/info/?url=" + mc[i]['href'][1:]
                list.append({'mc': mc[i].string, 'addr': addr[i].string, 'href': href})
                i = i + 1
                if i == len1:
                    break
            cur = cur + 1
            if cur > max:
                break
        return list

#根据不同的get请求，爬取对应页面的信息
def getMore(request):
    if request.method == 'GET':
        more=[]
        #处理get请求参数
        pre=request.GET.get('url')
        dwmc=request.GET.get('dwmc')
        mldm=request.GET.get('mldm')
        mlmc=request.GET.get('mlmc')
        yjxkdm=request.GET.get('yjxkdm')
        xxfs=request.GET.get('xxfs')
        zymc=request.GET.get('zymc')
        #根据get请求参数拼接出对应的url
        url='https://yz.chsi.com.cn/'+pre+'&dwmc='+dwmc+'&mldm='+mldm+'&mlmc'+mlmc+'&yjxkdm='+yjxkdm+'&xxfs='+xxfs+'&zymc='+zymc
        temp=requests.get(url)
        soup=BeautifulSoup(temp.text,'lxml')
        ksfs = soup.select(
            'body > div.main-wrapper > div.container.clearfix > div > div.zsml-list-box > table > tbody > tr > td:nth-child(1)')
        yxs = soup.select(
            'body > div.main-wrapper > div.container.clearfix > div > div.zsml-list-box > table > tbody > tr > td:nth-child(2)')
        zy = soup.select(
            'body > div.main-wrapper > div.container.clearfix > div > div.zsml-list-box > table > tbody > tr > td:nth-child(3)')
        yjfx = soup.select(
            'body > div.main-wrapper > div.container.clearfix > div > div.zsml-list-box > table > tbody > tr > td:nth-child(4)')
        ksfw = soup.select(
            'body > div.main-wrapper > div.container.clearfix > div > div.zsml-list-box > table > tbody > tr > td:nth-child(8)>a')
        i=0
        len1=len(ksfs)
        while True:
            dict={}
            dict['ksfs']=ksfs[i].string
            dict['yxs'] = yxs[i].string
            dict['zy'] = zy[i].string
            dict['yjfx'] = yjfx[i].string

            #根据爬取的网页地址，进一步爬取更详细信息
            url1='https://yz.chsi.com.cn'+ksfw[i]['href']
            res = requests.get(url1)
            soup = BeautifulSoup(res.text, 'lxml')
            rs = soup.select(
                'body > div.main-wrapper > div.container.clearfix > div.zsml-left > div.zsml-wrapper > table > tbody > tr:nth-child(5) > td.zsml-summary')
            zz = soup.select(
                'body > div.main-wrapper > div.container.clearfix > div.zsml-left > div.zsml-wrapper > div > table > tbody > tr > td:nth-child(1)')
            wy = soup.select(
                'body > div.main-wrapper > div.container.clearfix > div.zsml-left > div.zsml-wrapper > div > table > tbody > tr > td:nth-child(2)')
            ss = soup.select(
                'body > div.main-wrapper > div.container.clearfix > div.zsml-left > div.zsml-wrapper > div > table > tbody > tr > td:nth-child(3)')
            zyk = soup.select(
                'body > div.main-wrapper > div.container.clearfix > div.zsml-left > div.zsml-wrapper > div > table > tbody > tr > td:nth-child(4)')
            dict['rs']=rs[0].string
            dict['zz']=deal(zz)
            dict['wy'] = deal(wy)
            dict['ss'] = deal(ss)
            dict['zyk'] = deal(zyk)
            more.append(dict)
            i = i + 1
            if i == len1:
                break
    return render(request,'info.html',context={'dwmc':dwmc,'more':more})

#处理表单value
def judge(str):
    if str=='--选择专业--':
        str=""
    if str!='':
        if str.isdigit()==False:
            str=""
    return str

#处理文本内容
def deal(temp):
    temp=temp[0].get_text().split(' ')
    for item in temp:
        if item != '\r\n' and item != '':
            str = item.replace("\n", "").replace("\r", "")
            break
    return str

#动态获取学科列表
def getXk(request):
    if request.method=='POST':
        ml=request.POST.get('mldm')
        data={'mldm':ml}
        xk=getInfo('https://yz.chsi.com.cn/zsml/pages/getZy.jsp',data)
        return HttpResponse(json.dumps({'xk':xk}))

#动态获取专业列表
def getZy(request):
    if request.method=='POST':
        q=request.POST.get('q')
        data={'q':q}
        zy=getInfo('https://yz.chsi.com.cn/zsml/code/zy.do',data)
        return HttpResponse(json.dumps({'zy':zy}))

#根据用户post的数据爬取符合的所有大学信息
def getList(request):
    data={}
    ss = getInfo('https://yz.chsi.com.cn/zsml/pages/getSs.jsp', data)
    ml = getInfo('https://yz.chsi.com.cn/zsml/pages/getMl.jsp', data)
    xk = getInfo('https://yz.chsi.com.cn/zsml/pages/getZy.jsp', data)
    if request.method=='POST':
        #处理POST请求参数
        form_data={}
        ssdm=judge(request.POST.get('ssdm'))
        dwmc=request.POST.get('dwmc')
        mldm=judge(request.POST.get('mldm'))
        yjxkdm=judge(request.POST.get('yjxkdm'))
        zymc=judge(request.POST.get('zymc'))
        xxfs=request.POST.get('xxfs')
        xxlb=request.POST.get('xxlb')
        if xxlb!=None:
            form_data['xxlb']=xxlb
        form_data['ssdm']=ssdm
        form_data['dwmc']=dwmc
        form_data['mldm']=mldm
        form_data['yjxkdm']=yjxkdm
        form_data['zymc']=zymc
        form_data['xxfs']=xxfs
        list=getDetail('https://yz.chsi.com.cn/zsml/queryAction.do',form_data)
        send={'ss':ss,'ml':ml,'xk':xk,'list':list}
        if list==[]:
            send.update({'tip':'很抱歉，没有找到您要搜索的数据！'})
        return render(request,'list.html',context=send)

#初始化表单选项
def init(request):
    data={}
    ss=getInfo('https://yz.chsi.com.cn/zsml/pages/getSs.jsp',data)
    ml=getInfo('https://yz.chsi.com.cn/zsml/pages/getMl.jsp',data)
    xk=getInfo('https://yz.chsi.com.cn/zsml/pages/getZy.jsp',data)
    return render(request,'index.html',context={'ss':ss,'ml':ml,'xk':xk})