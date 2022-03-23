# -*- coding: utf-8 -*-
from tkinter import *
import requests
import json
import os

headers = {
    'Referer': 'https://y.qq.com/portal/search.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/77.0.3865.90 Safari/537.36 '
}
music_data = []
def search_song():
    global music_data
    music_info_list = []
    text.delete(0, END)
    name = entry.get()
    page = '1'
    num = '10'
    url = f'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?p={page}&n={num}&w={name}'
    response = requests.get(url).text
    music_json = response[9:-1]
    music_data = json.loads(music_json)
    music_list = music_data['data']['song']['list']
    for music in music_list:
        music_name = music['songname']  # 歌名
        singer_name = music['singer'][0]['name']  # 歌手
        songmid = music['songmid']
        if 'media_mid' in music.keys():
            media_mid = music['media_mid']
            music_info_list.append((music_name, singer_name, songmid, media_mid))
    # 获取vkey
    music_data = []
    for music in music_info_list:
        music_name = music[0]
        singer_name = music[1]
        songmid = music[2]
        url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?data={"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"8846039534","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"8846039534","songmid":["%s"],"songtype":[0],"uin":"1152921504784213523","loginflag":1,"platform":"20"}},"comm":{"uin":"1152921504784213523","format":"json","ct":24,"cv":0}}' % songmid
        response = requests.get(url).json()  # 转换字典
        purl = response['req_0']['data']['midurlinfo'][0]['purl']
        full_media_url = 'http://dl.stream.qqmusic.qq.com/' + purl
        music_data.append(
            {
                'music_name': music_name,
                'singer_name': singer_name,
                'full_media_url': full_media_url
            }

        )
        text.insert(END, '%s:--%s' % (music_name,singer_name))
        text.see(END)
    text.update()


def downlaod_song():
    tuple1=text.curselection()
    global music_data
    for tup in tuple1:
        print(music_data[tup])
        music_name = music_data[tup]['music_name']
        singer_name = music_data[tup]['singer_name']
        full_url = music_data[tup]['full_media_url']
        music_response = requests.get(full_url, headers=headers).content
        #下载到本层级文件夹
        with open('%s-%s.mp3' % (music_name, singer_name), 'wb')as fp:
            fp.write(music_response)
            
# 1.创建窗口
root = Tk()
# 2.窗口标题
root.title('QQ音乐')
# 3.窗口大小以及显示位置,中间是小写的x
root.geometry('660x385+550+230')
# 窗口显示位置
# 4.标签控件
lable = Label(root, text='请输入需要下载的歌手或歌曲:', font=('微软雅黑', 10))
lable.grid(row=0, column=0)
button0 = Button(root, text='查询', width=10, font=('微软雅黑', 10), command=search_song)
button0.grid(row=0, column=4, sticky=E)
# 5.输入控件
entry = Entry(root, font=('微软雅黑', 25))
entry.grid(row=0, column=1)
# 6.列表框控件
text = Listbox(root, selectmode=MULTIPLE,font=('微软雅黑', 16), width=45, height=10)
# # columnspan组件所跨月的列数
text.grid(row=1, columnspan=4)
# 7.按钮控件
button = Button(root, text='开始下载', width=10, font=('微软雅黑', 10), command=downlaod_song)
button.grid(row=2, column=0, sticky=W)
button1 = Button(root, text='退出', width=10, font=('微软雅黑', 10), command=root.quit)
button1.grid(row=2, column=4, sticky=E)

# 消息循环,显示窗口
root.mainloop()
