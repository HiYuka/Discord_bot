#このコードは普段プライベート環境で書いているコードをコピーandペーストしたものです
#IDなど公開できないものは、別の数字などに置き換えています

from discord.ext import commands
import os
import traceback
import random
import time

#ここを書き換え-------------------------------------------------------------------------

#バージョン情報
version_val = "1.02"

'''
#～～～～～プライベートサーバーでのテスト～～～～～～～～～～～～～～～～～～～～～～～～～～～～～    
#カスタムamongusの時に役職を配布するチャンネル
amongus_channel = 00000000000000000
#ボイスチャットの開始を通知するチャンネル
voice_chat_channel = 00000000000000000
#通知が欲しいボイスチャンネル
voice_channel = 00000000000000000
#～～～～～少人数サーバーでのテスト～～～～～～～～～～～～～～～～～～～～～～～～～～～～～    
#カスタムamongusの時に役職を配布するテキストチャンネル
amongus_channel = 00000000000000000
#ボイスチャットの開始を通知するテキストチャンネル
voice_chat_channel = 00000000000000000
#通知が欲しいボイスチャンネル
voice_channel = 00000000000000000
'''

#～～～～～本番環境のサーバー～～～～～～～～～～～～～～～～～～～～～～～～～～～～～    
#カスタムamongusの時に役職を配布するテキストチャンネル
amongus_channel = 00000000000000000
#ボイスチャットの開始を通知するテキストチャンネル
voice_chat_channel = 00000000000000000
#通知が欲しいボイスチャンネル
voice_channel = 00000000000000000

#～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～

#--------------------------------------------------------------------------------------
prefix = '/ss ' 
bot = commands.Bot(command_prefix=prefix,help_command=None)
token = os.environ['DISCORD_BOT_TOKEN']

join_list = []
voice_chat_list = []
jadge_list = []

@bot.event
async def on_command_error(ctx, error): #エラー時の挙動
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

#～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～   
@bot.command()
async def version(ctx): #/ss version
    await ctx.channel.send('version:' + version_val)  
   
@bot.event
async def on_ready(): #botが起動したときの動作
    channelID = bot.get_channel(voice_chat_channel)
    await channelID.send('起動しました。version:' + version_val + '\n使い方は [/ss help]')


@bot.event
async def on_voice_state_update(member,before,after): #誰かがボイスチャットに入室したときに、通知を出す
    
    channelID = bot.get_channel(voice_chat_channel)
    #voice_channelID = bot.get_channel(voice_channel)
    #await channelID.send('Hi')
    #await channelID.send("Before channel is " + str(before.channel))
    #await channelID.send("After channel is " + str(after.channel))
    channel_name = bot.get_channel(voice_channel)
    
    if before.channel == after.channel:#同じチャンネル内での変化（マイクミュートなど）の場合
        #send_message_content = "```同じチャンネル内での変化```"
        #await channelID.send(send_message_content)
        pass
    else:

        if after.channel == channel_name:#新しく接続したチャンネルがこのチャンネルの場合
            if len(after.channel.members) == 1:#入室者が一人目の場合
                voicemention = '<@&0000000000000>' #メンションする役職のID
                send_message_content = "```誰かがボイスチャットを始めました```"  
                await channelID.send(voicemention + send_message_content)
            else:
                #await channelID.send("```二人目以降```")#チャンネルにメッセージを送信  
                pass
                
        else:#新しく接続したチャンネルが別のチャンネルの場合  
            #send_message_content = "```新しく接続したチャンネルが別のチャンネル```"
            #await channelID.send(send_message_content)
            pass#無視
#参考　https://teratail.com/questions/238571?link=qa_related_sp 
          
time_stamp_list = 
['<:19:0000000000000>','<:20:0000000000000>','<:21:0000000000000>','<:22:0000000000000>',
 '<:23:0000000000000>','<:24:0000000000000>','<:25:0000000000000>'] #それぞれ、絵文字のIDです

@bot.command()    
async def time(ctx): #/ss time  と打った時に、19時から25時までの絵文字をメッセージに付与する   
    for i in range(7):
        emoji = time_stamp_list[i]
        await ctx.message.add_reaction(emoji)

#among us というゲームをするときに、一人ランダムでメンションする機能です ～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～
@bot.command()
async def join(ctx): #/ss join
    join_list.append(ctx.author.id)
    await ctx.channel.send(str(ctx.author) + 'をプレイヤーに追加しました\n#watchingチャンネルを"@mentionのみ通知"に設定してください')
 
@bot.command() 
async def check(ctx): #/ss check
    await ctx.channel.send('参加者一覧')
    for i in join_list: #参加者リストから一人ずつメンションします
        mention = '<@'+ str(i) + '>'
        await ctx.send(mention) 
    await ctx.channel.send('以上')
   
@bot.command()
async def start(ctx): #/ss start 
    if len(join_list) != 0:
        await ctx.channel.send('役職を配布します')   
        channelID = bot.get_channel(amongus_channel) #役職を配布するチャンネル
        #time.sleep(3)
        list(set(join_list))
        fox = str(random.choice(join_list))
        mention = '<@'+ fox + '>' #参加者リストの中から一人をランダムで選んでメンションします
        await channelID.send(mention) 
    else:
        await ctx.channel.send('参加者が登録されていません')
        
@bot.command()
async def reset(ctx): #/ss reset
    join_list.clear()
    await ctx.channel.send('参加者をリセットしました')
    
#～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～
        
@bot.command()
async def help(ctx): #/ss help
    help_message = '''```
/ts とコマンドの間には" "半角スペースを空けてください
文章中にコマンドを打つ際には、一番上の行に入れてください。
【通常コマンド】
---[ /ts version     ] バージョン(適当)が分かります
---[ /ts time        ] 19~深夜 の時間帯リアクションを付与できます。
---[ /ts youtube     ] YouTubeチャンネルのURLが表示されます
【among us 系のコマンド】
メンバーが変わるとき・ゲームを終了するときには
必ず /ts reset をしてください
---[ /ts join  ] ゲームに参加します
---[ /ts check ] 参加者を確認します
---[ /ts start ] ランダムで参加者から一人をwatchingチャンネルにメンションします
---[ /ts reset ] 参加者登録を"全員分"解除します
【ボイスチャット通知について】
livingチャンネルに誰も入っていない状態で、
livingに入ると通知が飛びます。
```'''
    await ctx.channel.send(help_message)

@bot.command()
async def youtube(ctx): #/ss youtube
    await ctx.channel.send('URL') 
    await ctx.channel.send('URL')

bot.run(token)
