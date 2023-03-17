# 環境変数用 標準ライブラリなのでインストール不要
import os
import subprocess
# 文字エンコード
import json
# 正規表現
import re
# 距離の計算に使用
import math
# インストールした discord.py を読み込む
import discord

# Botのアクセストークン 環境変数から
TOKEN = os.environ['COORDBOT_TOKEN']


# Intentsオブジェクトを生成
# 全てのIntentをTrue
intents = discord.Intents.all()
# 接続に必要なオブジェクトを生成
client = discord.Client(intents=intents)

# エリア情報の読み込み
def read_areas():
    # ファイルを読み込んで行毎にリストに格納
    with open('areas.txt', mode='r',encoding="utf-8") as f:
        areas = f.readlines()
    # 改行を取り除く
    for i , area in enumerate(areas):
        areas[i] = area.replace('\n','')
    return areas

# メッセージを座標形式に変換
def convert_coords_message(receive_message):
    # 行ごとに分ける
    split_messages = receive_message.splitlines()
    # orの部分はインスタンスに使用される特殊文字
    pattern = '.*?(.*?)[ |||].*?(\d+\.\d+).*?(\d+\.\d+).*'
    #メッセージの変換と作成
    coords = []
    for split_message in split_messages:
        result = re.match(pattern, split_message)
        if result: #none以外
            coords.append("/coord X:" + result.group(2) + "Y:" + result.group(3) + ":" + result.group(1))
    return coords

# エリア毎に優先順を付与する
def coords_area_priority(coords):
    areas = read_areas()
    priority = []
    # 地図対象外のマップは-1
    for i,coord in enumerate(coords):
        priority.append(-1)
    for i,coord in enumerate(coords):
        for j,area in enumerate(areas):
            search = re.search(area,coord)
            if search:
                priority.insert(i,j*8)
                break
    return priority

# XY座標の抽出
def extract_coord(coords):
    x_coords = []
    y_coords = []
    xpattern = "X:(\d+.\d+)"
    ypattern = "Y:(\d+.\d+)"
    for coord in coords:
        xresult = re.search(xpattern,coord)
        yresult = re.search(ypattern,coord)
        if xresult:
            x_coords.append(xresult.group(1))
        if yresult:
            y_coords.append(yresult.group(1))
    return x_coords,y_coords

# 2点間の距離
def distance(x1,y1,x2,y2):
    return math.sqrt((x2-float(x1)) * (x2-float(x1)) + (y2-float(y1)) * (y2-float(y1)))


# 既知の宝箱の場所のどれに該当するかで優先度を付与する
def treasure_maps(x,y,area_idx):
    treasure_priority = 0
    dist  = 10000
    dist2 = 10000
    err   = 0

    # 暁月地域(地図G15)

    # エルピス
    if   area_idx == 0 :
        dist  = distance(x,y,13,9)
        dist2 = distance(x,y,30,10)
        if(dist > dist2):
            treasure_priority = 1
            dist = dist2
        dist2 = distance(x,y,29,18)
        if(dist > dist2):
            treasure_priority = 2
            dist = dist2
        dist2 = distance(x,y,37,19)
        if(dist > dist2):
            treasure_priority = 3
            dist = dist2
        dist2 = distance(x,y,23,25)
        if(dist > dist2):
            treasure_priority = 4
            dist = dist2
        dist2 = distance(x,y,27,24)
        if(dist > dist2):
            treasure_priority = 5
            dist = dist2
        dist2 = distance(x,y,12,33)
        if(dist > dist2):
            treasure_priority = 6
            dist = dist2
        dist2 = distance(x,y,17,31)
        if(dist > dist2):
            treasure_priority = 7
            dist = dist2


    # 暁月地域(地図G14)

    # ラヴィリンソス
    elif   area_idx == 1 :
        dist  = distance(x,y,32,14)
        dist2 = distance(x,y,23,10)
        if(dist > dist2):
            treasure_priority = 1
            dist = dist2
        dist2 = distance(x,y,18,18)
        if(dist > dist2):
            treasure_priority = 2
            dist = dist2
        dist2 = distance(x,y,25,21)
        if(dist > dist2):
            treasure_priority = 3
            dist = dist2
        dist2 = distance(x,y,24,29)
        if(dist > dist2):
            treasure_priority = 4
            dist = dist2
        dist2 = distance(x,y,21,37)
        if(dist > dist2):
            treasure_priority = 5
            dist = dist2
        dist2 = distance(x,y,8,30)
        if(dist > dist2):
            treasure_priority = 6
            dist = dist2
        dist2 = distance(x,y,7,20)
        if(dist > dist2):
            treasure_priority = 7
            dist = dist2
    # サベネア島
    elif area_idx == 2 :
        dist  = distance(x,y,31,14)
        dist2 = distance(x,y,27,9)
        if(dist > dist2):
            treasure_priority = 1
            dist = dist2
        dist2 = distance(x,y,14,8)
        if(dist > dist2):
            treasure_priority = 2
            dist = dist2
        dist2 = distance(x,y,19,14)
        if(dist > dist2):
            treasure_priority = 3
            dist = dist2
        dist2 = distance(x,y,22,19)
        if(dist > dist2):
            treasure_priority = 4
            dist = dist2
        dist2 = distance(x,y,27,29)
        if(dist > dist2):
            treasure_priority = 5
            dist = dist2
        dist2 = distance(x,y,21,27)
        if(dist > dist2):
            treasure_priority = 6
            dist = dist2
        dist2 = distance(x,y,15,26)
        if(dist > dist2):
            treasure_priority = 7
            dist = dist2
    # ガレマルド
    elif area_idx == 3 :
        dist  = distance(x,y,34,17)
        dist2 = distance(x,y,34,9)
        if(dist > dist2):
            treasure_priority = 1
            dist = dist2
        dist2 = distance(x,y,25,12)
        if(dist > dist2):
            treasure_priority = 2
            dist = dist2
        dist2 = distance(x,y,16,12)
        if(dist > dist2):
            treasure_priority = 3
            dist = dist2
        dist2 = distance(x,y,15,18)
        if(dist > dist2):
            treasure_priority = 4
            dist = dist2
        dist2 = distance(x,y,11,26)
        if(dist > dist2):
            treasure_priority = 5
            dist = dist2
        dist2 = distance(x,y,27,26)
        if(dist > dist2):
            treasure_priority = 6
            dist = dist2
        dist2 = distance(x,y,29,35)
        if(dist > dist2):
            treasure_priority = 7
            dist = dist2
    # 嘆きの海
    elif area_idx == 4 :
        dist  = distance(x,y,17,19)
        dist2 = distance(x,y,18,25)
        if(dist > dist2):
            treasure_priority = 1
            dist = dist2
        dist2 = distance(x,y,12,26)
        if(dist > dist2):
            treasure_priority = 2
            dist = dist2
        dist2 = distance(x,y,16,34)
        if(dist > dist2):
            treasure_priority = 3
            dist = dist2
        dist2 = distance(x,y,23,36)
        if(dist > dist2):
            treasure_priority = 4
            dist = dist2
        dist2 = distance(x,y,25,33)
        if(dist > dist2):
            treasure_priority = 5
            dist = dist2
        dist2 = distance(x,y,30,25)
        if(dist > dist2):
            treasure_priority = 6
            dist = dist2
        dist2 = distance(x,y,35,30)
        if(dist > dist2):
            treasure_priority = 7
            dist = dist2
    # ウルティマ・トゥーレ
    elif area_idx == 5 :
        dist  = distance(x,y,30,9)
        dist2 = distance(x,y,25,17)
        if(dist > dist2):
            treasure_priority = 1
            dist = dist2
        dist2 = distance(x,y,13,13)
        if(dist > dist2):
            treasure_priority = 2
            dist = dist2
        dist2 = distance(x,y,5,18)
        if(dist > dist2):
            treasure_priority = 3
            dist = dist2
        dist2 = distance(x,y,7,30)
        if(dist > dist2):
            treasure_priority = 4
            dist = dist2
        dist2 = distance(x,y,18,26)
        if(dist > dist2):
            treasure_priority = 5
            dist = dist2
        dist2 = distance(x,y,21,36)
        if(dist > dist2):
            treasure_priority = 6
            dist = dist2
        dist2 = distance(x,y,26,35)
        if(dist > dist2):
            treasure_priority = 7
            dist = dist2

    # 漆黒地域(地図G12)

    # レイクランド
    elif area_idx == 6 :
        dist  = distance(x,y,8,21)
        dist2 = distance(x,y,10,25)
        if(dist > dist2):
            treasure_priority = 1
            dist = dist2
        dist2 = distance(x,y,10,11)
        if(dist > dist2):
            treasure_priority = 2
            dist = dist2
        dist2 = distance(x,y,13,12)
        if(dist > dist2):
            treasure_priority = 3
            dist = dist2
        dist2 = distance(x,y,17,17)
        if(dist > dist2):
            treasure_priority = 4
            dist = dist2
        dist2 = distance(x,y,18,7)
        if(dist > dist2):
            treasure_priority = 5
            dist = dist2
        dist2 = distance(x,y,34,25)
        if(dist > dist2):
            treasure_priority = 6
            dist = dist2
        dist2 = distance(x,y,38,13)
        if(dist > dist2):
            treasure_priority = 7
            dist = dist2

    # コルシア島
    elif area_idx == 7 :
        dist  = distance(x,y,7,18)
        dist2 = distance(x,y,11,13)
        if(dist > dist2):
            treasure_priority = 1
            dist = dist2
        dist2 = distance(x,y,13,16)
        if(dist > dist2):
            treasure_priority = 2
            dist = dist2
        dist2 = distance(x,y,20,17)
        if(dist > dist2):
            treasure_priority = 3
            dist = dist2
        dist2 = distance(x,y,21,9)
        if(dist > dist2):
            treasure_priority = 4
            dist = dist2
        dist2 = distance(x,y,30,17)
        if(dist > dist2):
            treasure_priority = 5
            dist = dist2
        dist2 = distance(x,y,34,10)
        if(dist > dist2):
            treasure_priority = 6
            dist = dist2
        dist2 = distance(x,y,33,31)
        if(dist > dist2):
            treasure_priority = 7
            dist = dist2

    # アム・アレーン
    elif area_idx == 8 :
        dist  = distance(x,y,12,14)
        dist2 = distance(x,y,13,30)
        if(dist > dist2):
            treasure_priority = 1
            dist = dist2
        dist2 = distance(x,y,27,13)
        if(dist > dist2):
            treasure_priority = 2
            dist = dist2
        dist2 = distance(x,y,26,23)
        if(dist > dist2):
            treasure_priority = 3
            dist = dist2
        dist2 = distance(x,y,30,30)
        if(dist > dist2):
            treasure_priority = 4
            dist = dist2
        dist2 = distance(x,y,32,8)
        if(dist > dist2):
            treasure_priority = 5
            dist = dist2
        dist2 = distance(x,y,36,11)
        if(dist > dist2):
            treasure_priority = 6
            dist = dist2
        dist2 = distance(x,y,34,17)
        if(dist > dist2):
            treasure_priority = 7
            dist = dist2


    # イルメグ
    elif area_idx == 9 :
        dist  = distance(x,y,31,4)
        dist2 = distance(x,y,33,10)
        if(dist > dist2):
            treasure_priority = 1
            dist = dist2
        dist2 = distance(x,y,25,12)
        if(dist > dist2):
            treasure_priority = 2
            dist = dist2
        dist2 = distance(x,y,21,7)
        if(dist > dist2):
            treasure_priority = 3
            dist = dist2
        dist2 = distance(x,y,10,13)
        if(dist > dist2):
            treasure_priority = 4
            dist = dist2
        dist2 = distance(x,y,7,17)
        if(dist > dist2):
            treasure_priority = 5
            dist = dist2
        dist2 = distance(x,y,12,20)
        if(dist > dist2):
            treasure_priority = 6
            dist = dist2
        dist2 = distance(x,y,14,27)
        if(dist > dist2):
            treasure_priority = 7
            dist = dist2

    # ラケティカ大森林
    elif area_idx == 10 :
        dist  = distance(x,y,24,15)
        dist2 = distance(x,y,34,17)
        if(dist > dist2):
            treasure_priority = 1
            dist = dist2
        dist2 = distance(x,y,35,22)
        if(dist > dist2):
            treasure_priority = 2
            dist = dist2
        dist2 = distance(x,y,24,27)
        if(dist > dist2):
            treasure_priority = 3
            dist = dist2
        dist2 = distance(x,y,22,32)
        if(dist > dist2):
            treasure_priority = 4
            dist = dist2
        dist2 = distance(x,y,26,34)
        if(dist > dist2):
            treasure_priority = 5
            dist = dist2
        dist2 = distance(x,y,13,24)
        if(dist > dist2):
            treasure_priority = 6
            dist = dist2
        dist2 = distance(x,y,11,19)
        if(dist > dist2):
            treasure_priority = 7
            dist = dist2

    # テンペスト
    elif area_idx == 11 :
        dist  = distance(x,y,30,20)
        dist2 = distance(x,y,37,17)
        if(dist > dist2):
            treasure_priority = 1
            dist = dist2
        dist2 = distance(x,y,32,5)
        if(dist > dist2):
            treasure_priority = 2
            dist = dist2
        dist2 = distance(x,y,25,11)
        if(dist > dist2):
            treasure_priority = 3
            dist = dist2
        dist2 = distance(x,y,19,8)
        if(dist > dist2):
            treasure_priority = 4
            dist = dist2
        dist2 = distance(x,y,12,11)
        if(dist > dist2):
            treasure_priority = 5
            dist = dist2
        dist2 = distance(x,y,13,14)
        if(dist > dist2):
            treasure_priority = 6
            dist = dist2
        dist2 = distance(x,y,16,18)
        if(dist > dist2):
            treasure_priority = 7
            dist = dist2

    else :
        err = 1

    if err == 0 :
        return area_idx * 8 + treasure_priority
    elif err == 1:
        return -1

# エリア毎に巡回優先度を付与する
def treasure_priority(x_coords,y_coords,treasure):
    priority = []
    i        = 0
    # 対象エリア数
    while(i < len(treasure)):
        j = 0
        # 宝箱の数
        while(j < treasure[i]):
            priority.append(treasure_maps(x_coords[i+j],y_coords[i+j],i))
            j += 1
        i += 1
    return priority



# 座標メッセージを巡回順に整理
def sort_coords_message(coords):
    # 座標メッセージをエリアで整理
    area_priority = coords_area_priority(coords)
    # 対象外のマップを後ろへ
    i = len(coords)
    while(i > 0):
        j = i - 1
        while(j >= 0):
            if(area_priority[i] > area_priority[j]):
                area_priority[i],area_priority[j] = area_priority[j],area_priority[i]
                coords[i],coords[j] = coords[j],coords[i]
            j-=1
        i-=1
    i = 0
    # 対象外マップを省く
    while(i < len(coords)):
        if(area_priority[i] < 0):
            break
        i+=1
    # エリア毎に整列
    coord_max = i
    i = 0
    while(i < coord_max - 1):
        j = i + 1
        while(j < coord_max):
            if(area_priority[i] > area_priority[j]):
                area_priority[i],area_priority[j] = area_priority[j],area_priority[i]
                coords[i],coords[j] = coords[j],coords[i]
            j += 1
        i += 1

    # エリア毎の宝箱の数を確認
    i        = 0
    area_idx = 0  #地域
    count    = 0  #宝箱の数のカウント
    treasure = [] #エリア毎の宝箱, len()で対象エリア数
    while(area_priority[i]!=-1):
        i        += 1
        count    += 1
        if(area_priority[i]!=area_idx):
            treasure.append(count)
            count     = 0
            area_idx += 8

    # 座標の抽出
    x_coords,y_coords = extract_coord(coords)

    # 宝箱の巡回優先度を付与
    priority = []
    priority = treasure_priority(x_coords,y_coords,treasure)

    # 宝箱の巡回優先度で整列
    i = 0
    while(i < coord_max - 1):
        j = i + 1
        while(j < coord_max):
            if(priority[i] > priority[j]):
                priority[i],priority[j] = priority[j],priority[i]
                coords[i],coords[j] = coords[j],coords[i]
            j += 1
        i += 1


    #最後に対象外のマップの優先度を-1にしておく
    i = coord_max
    while(i < len(coords)) :
        priority.append(-1)
        i += 1

    # return coords,priority,treasure,x_coords,y_coords
    return coords,priority


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
        # 受け取ったメッセージを変換
        coords = convert_coords_message(message.content)
        # priority = coords_area_priority(coords)

        # coords,priority,treasure,x_coords,y_coords = sort_coords_message(coords)
        coords,priority = sort_coords_message(coords)


        # res_message  = str(x_coords) + "\n"
        # res_message += str(y_coords) + "\n"
        # res_message += str(len(treasure)) + "\n"
        # res_message += str(treasure) + "\n"
        # res_message += "```\n"
        res_message = "```\n"
        for i,coord in enumerate(coords):
            if(priority[i] != -1):
                res_message += coord + "\n"
            # res_message += coord + str(priority[i]) + "\n"
        res_message += "```"
        await message.channel.send(res_message)


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
