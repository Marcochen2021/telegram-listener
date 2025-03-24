from telethon import TelegramClient, events
from flask import Flask
import threading
import os
import requests

# ===== 环境变量读取 =====
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
your_user_id = int(os.getenv("USER_ID"))

# ===== 监听群组 & 用户设置 =====
target_group = -1001964321520  # 牛牛军团 ID
target_user_ids = [1812894386, 1800869159]  # marco_chen2020 和 niuge_eth

# ===== 创建 Telegram 客户端（使用手机号登录）=====
client = TelegramClient('user_session', api_id, api_hash)

# ===== Flask 保活服务（防止 Railway 休眠）=====
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ 监听器在线运行中！"

def run_web():
    app.run(host='0.0.0.0', port=8080)

# ===== 推送提醒 =====
def send_telegram_message(text):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': your_user_id,
        'text': text
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"❌ 推送失败：{e}")

# ===== 监听消息事件 =====
@client.on(events.NewMessage(chats=target_group))
async def handler(event):
    sender = await event.get_sender()
    sender_id = sender.id
    sender_name = sender.username or sender.first_name or "未知用户"
    text = event.message.message or "<无文字内容>"

    if sender_id in target_user_ids:
        print(f"
🟡 群内发言 - 用户：[ {sender_name} ] (ID: {sender_id})\n内容: {text}\n")
        send_telegram_message(f"📣 监听到目标用户 [{sender_name}] 发言：{text}")

# ===== 主程序入口 =====
async def main():
    await client.start()
    print(f"✅ 已登录 Telegram，开始监听群组 [{target_group}] 中指定用户发言...")
    await client.run_until_disconnected()

def start_all():
    threading.Thread(target=run_web).start()
    import asyncio
    asyncio.run(main())

start_all()