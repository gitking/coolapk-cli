#coding=utf-8
import requests
import re

class InputError(Exception):
    pass

s = requests.session()

headers = {'Connection':'close'}

searchinput = input('应用名:')

searchurl = 'http://coolapk.com/apk/search/?q='+searchinput

searchpage = s.get(searchurl, headers=headers).text

searchpatch = re.findall(r'<a href="\S+">'+searchinput+'(.*?)</a>', searchpage)

if searchpatch == []:
    searchpatch = re.findall(r'<a href="\S+">(.*?)'+searchinput+'</a>', searchpage)
    searchoutput = searchpatch[0]+searchinput
elif '帐号登录' in searchpatch:
    searchpatch = ['']
    searchoutput = searchinput
elif len(searchpatch) >= 3:
    searchpatch = ['']
    searchoutput = searchinput
else:
    searchpatch = searchinput+searchpatch[0]

packname = re.findall(r'<a href="/apk/(\S+)">'+searchoutput+'</a>', searchpage, re.I)

if packname == []:
    raise InputError('找不到匹配')

apkurl = 'http://coolapk.com/apk/'+packname[0]

apkpage = s.get(apkurl, headers=headers).text

name8version = re.findall(r'<h1 class="media-heading ex-apk-view-title">(\S+) <small>(\S+)</small></h1>', apkpage)

developer = re.findall(r'<dt>开发者：</dt><dd>(.*?)</dd>', apkpage)

print('应用名称:'+name8version[0][0],'版本:'+name8version[0][1],'包名:'+packname[0],'开发者:'+developer[0])

basicinfo = re.findall(r'<span class="pull-left hidden-sm hidden-xs">(\S+)</span><span>(.*?)</span>', apkpage)

print(basicinfo[0][0]+basicinfo[0][1])

downloadurl = re.findall('var apkDownloadUrl = "(\S+)"', apkpage)[0]

editorcomments = re.findall(r'<strong>酷安点评：</strong>(\S+) <a href="/n/(\S+)">', apkpage)
if editorcomments != []:
    print(editorcomments[0][1]+'点评:'+editorcomments[0][0])

rankscore = re.findall(r'<span class="ex-apk-rank-score">(\S+)</span>',apkpage)
rankstat = re.findall(r'<a class="ex-gray-link" href="">(\S+)</a>', apkpage)
rankpercent = re.findall(r'<span class="ex-apk-rank-percent">(\S+)</span>', apkpage)

print('评分'+rankscore[0])
print(rankstat[0])
print('五星'+rankpercent[0])
print('四星'+rankpercent[1])
print('三星'+rankpercent[2])
print('二星'+rankpercent[3])
print('一星'+rankpercent[4])

sumpermission = re.findall(r'<a href="#ex-apk-permission-pane" data-toggle="tab">(\S+)</a>', apkpage)
print(sumpermission[0])

temp1 = re.findall(r'<div class="ex-card-content">.*?</div>', apkpage, flags=re.DOTALL)[0]
temp2 = temp1.replace('<div class="ex-card-content">\n','')
temp3 = re.sub(r'</?\S\S\S\S>', '', temp2)
temp4 = re.sub(r'</?\S>', '', temp3)
temp5 = temp4.replace('  ','')
introduction = temp5.replace('<br />','\r\n')
print('\n======================应用简介=========================')
print(introduction)

temp1 = re.findall(r'<h2>'+name8version[0][1]+'</h2>.*?</div>.*?\W<div class="ex-card-wrapper">(.*?)</div>', apkpage, flags=re.DOTALL)[0]
temp2 = temp1.replace('<br />','')
whatsnew = temp2.replace('  ','')
print('======================更新了啥=========================')
print(whatsnew)

if not '(0)' in sumpermission[0]:
    if input('打印权限?(y/N)') == 'y':
        temp1 = re.findall(r'<div id="ex-apk-permission-pane" class="tab-pane ex-apk-permission-pane">.*</dl>\W+/div>', apkpage, flags=re.DOTALL)[0]
        temp2 = temp1.replace(' ', '')
        temp3 = temp2.replace('</dt><dd><strong>', ' ')
        temp4 = temp3.replace('<dt>','')
        temp5 = temp4.replace('<divid="ex-apk-permission-pane"class="tab-paneex-apk-permission-pane">\n<dlclass="dl-horizontal">','')
        temp6 = temp5.replace('</dl>\n</div>','')
        temp7 = temp6.replace('</strong>',' ')
        temp8 = temp7.replace('</dd>','')
        permissions = temp8.replace('</dt>','')
        print('======================所需权限=========================')
        print(permissions)
else:
    print('没有权限 ...')
if input('下载?(Y/n)') != 'n':
    with open(packname[0]+'_'+name8version[0][1]+'.apk','wb') as file:
        file.write(s.get(downloadurl+'&extra=0', headers=headers).content)
else:
    exit(0)
