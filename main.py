from time import sleep
from telethon import errors
from telethon import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.tl.functions.channels import InviteToChannelRequest
import asyncio
import csv
import random

api_id = #year id
api_hash = 'year hash'
phone = 'year phone'


async def save_csv():
    chanel = 't.me/bulkin_live'
    added_users = set()
    with open('user.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['UserID', 'AccessHash', 'First Name', 'Username', 'Phone'])
        client = TelegramClient('session_name', api_id, api_hash)
        await client.start(phone, password='9380')

        async for message in client.iter_messages(chanel, limit=10):
            if message.replies:
                async for comment in client.iter_messages(chanel, reply_to=message.id, limit=50):
                    user = comment.sender
                    if user and user.id not in added_users:  # Проверяем, добавлен ли пользователь
                        writer.writerow(
                            [user.id, user.access_hash if hasattr(user, 'access_hash') else 0, user.first_name,
                             user.username])
                        added_users.add(user.id)  # Добавляем в множество

    await client.disconnect()


async def add_in_chanel():
    chanel_add = 't.me/NewVVavve'
    limit = 60
    with open('user.csv', 'r', newline='', encoding='utf-8') as file:
        client = TelegramClient('session_name', api_id, api_hash)
        await client.start(phone, password='9380')
        rider = csv.reader(file)
        next(rider)
        for i, row in enumerate(rider, start=1):
            id, hash, name, username = row
            try:
                await client(InviteToChannelRequest(channel=chanel_add, users=[InputPeerUser(int(id), int(hash))]))
                print(f'добавлен: {username}')

                await asyncio.sleep(random.randint(10, 15))
                if i % 20 == 0:
                    await asyncio.sleep(60)
                if i == 60:
                    break
            except errors.FloodWaitError as e:
                print(f"Флуд-бан. Ждем {e.seconds} сек")
                await asyncio.sleep(e.seconds + 10)
            except Exception as e:
                print(f"Ошибка: {e}")
                await asyncio.sleep(10)


async def main():
    print('начало')
    #await save_csv()
    print('начало добавления')
    await add_in_chanel()

    print('конец')


asyncio.run(main())