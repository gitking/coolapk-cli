import json
import requests
from contextlib import closing

request = requests.session()

def dler(url, name, size):
    percentage = 0
    with closing(request.get(url, stream=True)) as r:
        content_size = int(r.headers['content-length'])
        if size != content_size: print('发现劫持')
        print('Total %.2f MB' %(content_size/1048576))
        with open(name,'wb') as file:
            for data in r.iter_content(1024):
                file.write(data)
                percentage += 100*len(data)/content_size
                print("%.2f%%" % percentage, end="\r")
    print("Done!  ")

def geter(url):
    data = request.get(url,headers={'？？？？': '？？？？'})
    return json.loads(data.text)


search = input('搜索:')

json_data = geter('https://www.coolapk.com/search?q='+search)

for num in json_data['dataRows']:
    print(num, json_data['dataRows'][num]['title'],
          json_data['dataRows'][num]['apkRomVersion'],
          json_data['dataRows'][num]['apksize'])

num = input('序号:')

apk_page = geter('https://www.coolapk.com/apk/'+num)



print('开发者:',apk_page['dataRow']['developername'])
print(apk_page['dataRow']['language'], apk_page['dataRow']['softtype'])
print('包名:',apk_page['dataRow']['apkname'])
print('大小:',apk_page['dataRow']['apksize'])
print('版本:',apk_page['dataRow']['apkversionname'])


print('点评')
print(apk_page['dataRow']['description'])

print('应用简介')
print(apk_page['dataRow']['introduce'])


print('新版特性')
print(apk_page['dataRow']['changehistory'].split('\n')[0])
print(apk_page['dataRow']['changelog'])


permissions = apk_page['dataRow']['permissions']
if len(permissions):
    print(len(permissions),'项权限',end=' ')
    if input('打印?(y/N)') == 'y':
        for i in permissions:
            print(i)
else:
    print('没有权限')
            
if input('下载?(Y/n)')!='n':
    dl_url = apk_page['apkDetailDownloadUrl']
    size = apk_page['dataRow']['apklength']
    name = apk_page['dataRow']['apkname']
    ver = apk_page['dataRow']['apkversionname']
    code = apk_page['dataRow']['apkversioncode']
    dl_name = '{}_v{}({}).apk'.format(name, ver, code)
    dler(dl_url, dl_name, size)
    
