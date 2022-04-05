
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import json
from message_generator import *


with open("token.json") as token_file:
    json_file = json.load(token_file)
    token = json_file["token"]


vk_session = vk_api.VkApi(token=token, api_version='5.131')
longpoll = VkBotLongPoll(vk_session, 210242413)
vk = vk_session.get_api()

update_source()

# main polling
for event in longpoll.listen():
    print(event)
    try:
        if event.type == VkBotEventType.MESSAGE_NEW and len(event.message.text) > 0:
            write_source(event.message.text)  # saving new text
            if randint(0, 100) > -1:  # sending new message
                vk.messages.send(message=generate_text(), chat_id=event.chat_id, random_id=get_random_id())
    except Exception as e:
        try:
            vk.messages.send(message=f'Произошла ошибка!\n{e}', chat_id=event.chat_id, random_id=get_random_id())
        except Exception as e:
            pass

