# -*- coding: utf-8 -*-
# @Date    : '2018/8/10 0010'
# @Author  : Terry feng  (fengshaomin@qq.com)
import sys
import itchat
from itchat.content import *

from_chatname = "信管03驻京办"


def get_from_chatroomid(li):
    for i in li:
        if i["NickName"] == from_chatname:
            return i['UserName']


def get_to_chatroomid(li):
    for i in li:
        if i["NickName"] == "驻京办":
            return i['UserName']


# 自动回复文本等类别消息
# isGroupChat=False表示非群聊消息
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isGroupChat=False)
def text_reply(msg):
    itchat.send('这是我的小号，暂无调戏功能，有事请加群', msg['FromUserName'])


# 自动回复图片等类别消息
# isGroupChat=False表示非群聊消息
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=False)
def download_files(msg):
    itchat.send('这是我的小号，暂无调戏功能，有事请加群', msg['FromUserName'])


# 自动处理添加好友申请
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text'])  # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.send_msg(u'你好哇', msg['RecommendInfo']['UserName'])


# 自动回复文本等类别的群聊消息
# isGroupChat=True表示为群聊消息
@itchat.msg_register([TEXT, SHARING], isGroupChat=True)
def group_reply_text(msg):
    # 消息来自于哪个群聊
    chatroom_id = msg['User']['UserName']
    print(msg['User']['UserName'])
    # 发送者的昵称
    username = msg['ActualNickName']
    print(chatroom_id)
    # 消息并不是来自于需要同步的群
    if chatroom_id != from_chatroomid:
        return

    if msg['Type'] == TEXT:
        content = msg['Content']
    elif msg['Type'] == SHARING:
        content = msg['Text']

    # 根据消息类型转发至其他需要同步消息的群聊
    if msg['Type'] == TEXT:

        itchat.send('消息由群%s内的%s转发:\n%s' % (from_chatname, username, msg['Content']), to_chatroomid)
    elif msg['Type'] == SHARING:

        itchat.send('%s\n%s\n%s' % (username, msg['Text'], msg['Url']), to_chatroomid)


# 扫二维码登录
itchat.auto_login(hotReload=True)
# 获取所有通讯录中的群聊
# 需要在微信中将需要同步的群聊都保存至通讯录
chatrooms = itchat.get_chatrooms(update=True, contactOnly=True)
print(chatrooms)
# chatroom_ids = [c['UserName'] for c in chatrooms]

from_chatroomid = get_from_chatroomid(chatrooms)
to_chatroomid = get_to_chatroomid(chatrooms)
print('正在监测的群聊：', len(chatrooms), '个')
print(from_chatroomid, to_chatroomid)

# 开始监测
itchat.run(True)
