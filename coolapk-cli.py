#!/usr/bin/env python3
#coding=utf-8

import requests
import json

class InputError(Exception):
    pass

#apikey=都是定值,
#cookie=自己抓包XD

url = 'http://api.coolapk.com/market/v2/api.php?apikey='+apikey

s = requests.session()

headers = {'Connection':'close','Cookie': 'coolapk_did='+cookie,'Host': 'api.coolapk.com'}

searchinput = input('应用名:')

searchurl = url+'&method=getSearchApkList&q='+searchinput

searchpage = s.get(searchurl, headers=headers)

jsonpage = json.loads(searchpage.text)

print('apk name','id')
for i in jsonpage:
    print(i['title'],i['id'])


apknum = input('请输入序号:')
    
apkurl = url+'&method=getApkField&id='+apknum

apkpage1 = s.get(apkurl, headers=headers)

try:
    apkpage = json.loads(apkpage1.text)
except:
    raise InputError('输入有误')


print()
print('应用名称:'+apkpage['field']['title'],'版本:'+apkpage['field']['version'],'包名:'+apkpage['field']['apkname'],'开发者:'+apkpage['meta']['developername'])
print('软件大小:'+apkpage['field']['apksize'],'下载数量'+apkpage['meta']['downnum'],apkpage['field']['softtype'],apkpage['field']['language'])
print('ROM版本:'+apkpage['field']['romversion']+'+')
print()
print('酷安点评:'+apkpage['field']['remark'])
print()
print('评分'+apkpage['meta']['score'])
print('评分人数:'+apkpage['meta']['votenum'])
print('五星'+apkpage['field']['votenum5'])
print('四星'+apkpage['field']['votenum4'])
print('三星'+apkpage['field']['votenum3'])
print('二星'+apkpage['field']['votenum2'])
print('一星'+apkpage['field']['votenum1'])

print('\n======================应用简介=========================')
print(apkpage['field']['introduce'].replace('<br />','\r\n'))

print('\n======================更新日志=========================')
print(apkpage['field']['changehistory'].split('\n')[0])
print(apkpage['field']['changelog'])



a = input('打印权限?(y/N)')
if a == 'y':
    print('\n======================所需权限=========================')
    print(apkpage['field']['permissions'])
elif a == 'n' or a == '':
    pass

b = input('下载?(Y/n)')
if b == 'y' or b == '':
    from contextlib import closing
    print("下载中...")
    downloadurl = apkpage['field']['apkfile'].replace(' ', '')
    percentage = 0
    with closing(requests.get(downloadurl, stream=True)) as r:
        content_size = int(r.headers['content-length'])
        chunk_size = 1024
        print('共%.2f MB' %(int(r.headers['content-length'])/1048576))
        with open(apkpage['field']['apkname']+'_'+apkpage['field']['version']+'.apk','wb') as file:
            for data in r.iter_content(chunk_size=chunk_size):
                file.write(data)
                percentage += 100*len(data)/content_size
                print("%.2f%%" % percentage, end="\r")
    print("\n完成")
else:
    exit(0)
