import telegram
import asyncio
import subprocess
from easydict import EasyDict
from simplejson import loads
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
config = {}

with open(os.path.join(dir_path, "config.json"), 'r', encoding='utf-8') as file_data:
	text = file_data.read()
	print("text :", text)
	config = EasyDict(loads(text))
bot = telegram.Bot(token = config.token)

cmd = "vnstat -i tun0 --json"
results = subprocess.run(cmd, shell=True, capture_output=True, encoding="utf-8")
stdout = results.stdout
vnstat = EasyDict(loads(stdout))
traffic = vnstat.interfaces[0].traffic

async def send_message(text):
	await bot.sendMessage(chat_id = config.chat_id, text = text)

message = "(daily) " + str(traffic.day[0].date.year) + "-" + str(traffic.day[0].date.month) + "-" + str(traffic.day[0].date.day) + "\n"
message += "received: " + str(round(traffic.day[0].rx / (1024 * 1024),1)) + "MB\n"
message += "transmitted: " + str(round(traffic.day[0].tx / (1024 * 1024), 1)) + "MB\n"
message += "=========================\n"
message += "(monthly) " + str(traffic.month[0].date.year) + "-" + str(traffic.month[0].date.month) + "\n" 
message += "received: " + str(round(traffic.month[0].rx / (1024 * 1024),1)) + "MB\n"
message += "transmitted: " + str(round(traffic.month[0].tx / (1024 * 1024), 1)) + "MB\n"

print(message)

asyncio.run(send_message(message))
