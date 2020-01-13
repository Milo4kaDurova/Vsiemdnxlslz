# Настроечки

api_id = 
api_hash = ""
session_name = ""

bot_username = "@StartupWarsBot"
jarvis_username = "@SWTelecomBot"

squad_chat_id = "startupwarschat"

sw_bot_id = 227859379
sw_informator_id = 376592453
sw_battle_bot_id = 500004356

jarvis_id = 345393111

sw_bots = [sw_bot_id]
sw_informers = [sw_informator_id, sw_battle_bot_id]

battle_points = ["10:10:13", "13:07:34" ,"16:09:45", "19:10:13", "22:08:12"]

#--------------


from telethon import TelegramClient, events
import time
import re
from datetime import datetime
import random
import asyncio

client = TelegramClient(session_name, api_id, api_hash)

#
# вейкап
#
@client.on(events.NewMessage(from_users=sw_bots, pattern=r"Опа, тебя начал грабить"))
async def rob_handler(event):
	print("rob_handler called")
	time.sleep(23 + random.randint(15,180))
	await event.click(0)

#
# Репорты битв
#

battle_handling = False

@client.on(events.NewMessage(from_users=sw_bots))
async def battle_report_handler(event):
	global battle_handling
	print(f"battle_report_handler called\n└ battle_handling={battle_handling}")
	if not battle_handling:
		return
		
	# send_read_acknowledge - читает сообщение
	# чтобы оно не висело в увемдолениях
	if "Твои результаты в битве" in event.raw_text:
		await client.send_read_acknowledge(bot_username, event.message)
		time.sleep(1)
		await event.forward_to(jarvis_username)
		time.sleep(23 + random.randint(15,180))
		await client.send_message(bot_username, "/eat")
	
			
	if "Ты ушёл поесть, восстановить силы." in event.raw_text:
		await client.send_read_acknowledge(bot_username, event.message)
	
	if "Поедим ещё?" in event.raw_text:
		await client.send_read_acknowledge(bot_username, event.message)
		battle_handling = False
		print("battle end")
	
		
#
# Битвы
#

# Пины
@client.on(events.NewMessage(chats=(squad_chat_id), from_users=sw_informers))
async def battle_pin_handler(event):
	print("battle_pin_handler called")
	if "⚔️В атаку на" in event.raw_text:
		await event.click(0)

	if "🛡Все в защиту" in event.raw_text:
		await event.click(0)

# Жарвис
@client.on(events.NewMessage(chats=(squad_chat_id), from_users=(jarvis_id)))
async def jarvis_stats_handler(event):
	print("jarvis_stats_handler called")
	if "Готовы к битве:" in event.raw_text:
		await event.click(0)

#
# Отправка /battle в бота св
# после битв
#
async def battle_job():
	global battle_handling
	print("battle started called")
	battle_handling = True
	await client.send_message(bot_username, "/battle")

#
# костыль, который каждую секунду чекает время
# и если текущее время совпадает с заданным, то
# отправляет боту /battle
#
async def battle_timer():
	while True:
		clock = datetime.strftime(datetime.now(), "%H:%M:%S")
		if clock in battle_points:
			await asyncio.sleep(random.randint(15,180))
			await battle_job()
		await asyncio.sleep(1)

#
# уведомление о том, что бот запустился
#
async def started():
	print("started called")
	me = await client.get_me()
	await client.send_message(me, "Bot started!")


#
# Запуск всего
#
client.start()
client.loop.run_until_complete(started())
client.loop.create_task(battle_timer())
client.run_until_disconnected()
