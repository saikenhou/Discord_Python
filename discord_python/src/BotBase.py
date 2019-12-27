
#import discord # インストールした discord.py
import random

import json
import glob
import os,sys

from ServerControl import *
from InitSetting import *
from TeamMaker import *


SETTING_FILE_NAME="../Setting/TeamSetting.json"
BOT_NAME = "TeamMaker"

class BOT_BASE():
    def __init__(self):
        self.members = []
        self.listIDs = []
        self.cup = []
        self.tm = TEAM_MAKER()

    def update(self, members, listIDs):
        self.members = members
        self.listIDs = listIDs
        self.tm.update(members, listIDs)

    def Main( self, message):
        sendMessage = ""
        image_list = "null"
        if message.content.startswith('/'):
            if message.content.startswith("/nekos"):
                sendMessage = "ネコＡ マーオ \n ネコＢ マーオ\nネコＡ マーーオ\n ネコＢ マーオ\nネコＡ マーーーオ！\n ネコＢ マーーオ！\n ネコＡ マーーーーーーーーオ！！！！！！\n ネコＢ マーーーーーーーオ！！！！！\nネコＡ＆Ｂ「ギャフベロハギャベバブジョハバ」\n"
            elif message.content.startswith("/neko"):
                sendMessage = "にゃーん"
            elif message.content.startswith("/check"):
                sendMessage = "Arsenal till I die!!"
                img_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../image/"
                image_list = [img_dir + "gunnersaurus.png"]
            else:
                sendMessage = "ちょっと何言ってるかわからない"
        elif message.content.startswith("!"):
            if message.content.startswith('!start'):
                sendMessage = self.tm.Print2Teams(message)
            elif message.content.startswith('!teams'):
                sendMessage = self.tm.PrintByTeamNum(message)
            elif message.content.startswith('!men'):
                sendMessage = self.tm.PrintByMemberNum(message)
            else:
                sendMessage = "ごめん。何言ってるかわからない。"

        return sendMessage, image_list

initInfo    = INIT_SETTING(SETTING_FILE_NAME)
sc          = SERVER_CONTROL(initInfo.serverName, BOT_NAME)
client      = sc.GetDiscordClient() # 接続に使用するオブジェクト
#client      = discord.Client() # 接続に使用するオブジェクト
botBase     = BOT_BASE()


# 起動時に通知してくれる処理
@client.event
async def on_ready():
    print('ログインしました')

@client.event
async def on_message(message):
    sendMessage = ""
    #sc      = SERVER_CONTROL(client, initInfo.serverName, BOT_NAME)
    # develop version
    #members = sc.GetOnlineUsers()
    # master version
    members, listIDs = sc.GetMemberAndListIDs(initInfo.mainChannel)

    listIDs = sc.GetListIDs(members)
    botBase.update(members, listIDs)

    if message.content.startswith('/') or message.content.startswith("!"):
        sendMessage, image_list = botBase.Main(message)
        if sendMessage != "":
            await sc.SendTextMessage(message.channel, sendMessage)
        if image_list != "null":
            for img in image_list:
                await sc.SendImage( message.channel, img)
                    #await channel.send(file= discord.File(img))
                    #await client.send_file(message.channel, img)


client.run(initInfo.token)
