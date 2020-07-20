# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 10:27:42 2020

@author: j-3
"""
import re
import uuid
import subprocess
import urllib.request
import ssl
import requests
import os
import datetime

context = ssl._create_unverified_context() #访问https
QUALITY = 'ld' #低清晰度
headers ={

"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",

}

#获取TS链接
def get_video_ids_from_url(url):
    
    #获取TXT里面m3u8地址
    m3u8UrlArr = [] #m3u8地址的数组
    with open(r'C:/Users/j-3/Desktop/pyDamo/m3u8Transform/m3u8Urls.txt',"r") as fff:
        for lines in fff:
            m3u8UrlArr.append(lines)
    fff.close()
    print("m3u8地址：")  
    print(m3u8UrlArr)      
    
    #请求M3U8地址
    ts_Part_Arr = []  #挑出含有。ts
    for index in range(len(m3u8UrlArr)):
        all_content = requests.get(m3u8UrlArr[index], headers = headers).text
        
        if "#EXTM3U" not in all_content:
            raise BaseException("非M3U8链接")
            
        file_line = all_content.split("\n")  #根据换行符分割
        
        for line in file_line:
            if ".ts" in line:
                ts_url = 'https://embedwistia-a.akamaihd.net{}'.format(line) #拼接成完整的ts片段下载地址
                ts_Part_Arr.append(ts_url)

    return ts_Part_Arr
    
#下载TS文件
def downLoad(tsUrlArr):
    
    #下载m3u8文件，获取里面的ts编码
    download_path = os.getcwd()+"\download" #下载文件夹=根目录+下载文件用的文件夹子目录
    if not os.path.exists(download_path):    #检查是否存在下载TS用的文件夹
        os.mkdir(download_path)  #不存在，则建立目录
    
    #建立一个当天的目录，防止重复
    download_path = os.path.join(download_path,datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))#拼接目录
    os.mkdir(download_path)
    
    tsUrlArr = get_video_ids_from_url(url="")   #ts地址
    
    #下载TS文件到指定路径
    try:
        print("下载中。。。")
        for index in range(len(tsUrlArr)):
            res = requests.get(tsUrlArr[index])
            c_full_name = tsUrlArr[index].rsplit("/",1)[-1]
#            res = requests.get(ts_url)
#            c_full_name = ts_url.rsplit("/",1)[-1]  #文件名---从右到左分割第一个“/”，然后取最后一个对象
            with open(os.path.join(download_path,c_full_name),'ab') as f:  #以二进制方式打开，追加写入
                f.write(res.content)
                f.flush()
                f.close()
    except requests.RequestException as e:
        print(e)
        print('下载链接异常')
    finally:
        print('---下载完成---\n'+'---开始合成MP4---\n')
        compositeVideoFromPath(download_path)
     
#把TS文件合成MP4
def compositeVideoFromPath(path):
    os.chdir(path)
    cmd = "copy /b * new.tmp"
    os.system(cmd)
    os.system('del /Q *.ts')
    os.system('del /Q *.mp4')
    os.rename("new.tmp", "new.mp4")

if __name__ == '__main__':

    downLoad([])
    
    # compositeVideoFromPath(os.getcwd()+"\download")
    