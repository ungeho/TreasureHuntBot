# 環境変数用 標準ライブラリなのでインストール不要
import os
import subprocess
# 文字エンコード
import json
# 正規表現
import re
# インストールした discord.py を読み込む
import discord


# Botのアクセストークン 環境変数から
TOKEN = os.environ['COORDBOT_TOKEN']


# 接続に必要なオブジェクトを生成
client = discord.Client()

def readtext():
    with open('areas.txt', mode='r',encoding="utf-8") as f:
        areas = f.readlines()
    return areas


# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    # if message.content == "/areas":
    #     areas = readtext()
    #     for area in areas:
    #         await message.channel.send(area)

    if message.content == "/clear":
        await message.channel.purge()
        await message.channel.send("履歴を全て削除しました。")

    else:
        split_messages = message.content.splitlines()
        # orの部分はインスタンスに使用される特殊文字
        pattern = '.*?(.*?)[ |||].*?(\d+\.\d+).*?(\d+\.\d+).*'

        for split_message in split_messages:
            result = re.match(pattern, split_message)
            if result: #none以外
                coord = "/coord X:" + result.group(2) + "Y:" + result.group(3) + ":" + result.group(1)
                await message.channel.send(coord)

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
