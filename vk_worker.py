
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import json
from message_generator import *
import re
from anekdots import *
from demotivator import *


def updater():
    try:
        make_uniq()
        print('Source got updated!')
    except Exception as e:
        print(e)


def change_chance(new_chance: int):
    global chance
    with open('chance.txt', 'w') as file:
        file.write(str(new_chance))
    chance = new_chance


def get_random_photo_url():
    with open('img_sources.txt', 'r') as img_file:
        return choice(img_file.readlines())


with open("token.json") as token_file:
    json_file = json.load(token_file)
    token = json_file["token"]

with open("message_patterns.json") as mess_patt_file:
    json_file = json.load(mess_patt_file)
    help_msg = '\n'.join(json_file["help"])
    dem_error_msg = json_file["dem_error"]
    chance_error_msg = json_file["chance_error"]

with open('chance.txt', 'r') as file:
    chance = int(file.read())


vk_session = vk_api.VkApi(token=token, api_version='5.131')
longpoll = VkBotLongPoll(vk_session, 210242413)
vk = vk_session.get_api()
upload = vk_api.VkUpload(vk)

update_source()


# main polling
for event in longpoll.listen():
    print(f'New msg! {event.message.text}')
    try:
        if event.type == VkBotEventType.MESSAGE_NEW and len(event.message.text) > 0:
            if re.match('[Ss] .*', event.message.text) is not None:
                continue
            elif re.match('[Dd] .*', event.message.text) is not None:
                if re.match('[Dd] help', event.message.text) is not None:
                    vk.messages.send(message=help_msg, chat_id=event.chat_id, random_id=get_random_id())
                elif re.match('[Dd] g a', event.message.text) is not None:
                    vk.messages.send(message=get_anekdot(), chat_id=event.chat_id, random_id=get_random_id())
                elif re.match('[Dd] g d', event.message.text) is not None:
                    dem_code = create_dem(get_random_photo_url(), generate_text(), generate_text())
                    if dem_code == 0:
                        photo = upload.photo_messages('last_dem.jpg')
                        owner_id = photo[0]['owner_id']
                        photo_id = photo[0]['id']
                        access_key = photo[0]['access_key']
                        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                        vk.messages.send(chat_id=event.chat_id, random_id=get_random_id(), attachment=attachment)
                    else:
                        vk.messages.send(message=dem_error_msg, chat_id=event.chat_id, random_id=get_random_id())
                elif re.match('[Dd] c [\d]+', event.message.text) is not None:
                    new_chance = int(event.message.text.split(' ')[2])
                    if 0 <= new_chance <= 100:
                        change_chance(new_chance)
                    else:
                        vk.messages.send(message=chance_error_msg, chat_id=event.chat_id, random_id=get_random_id())
            else:
                write_source(event.message.text)  # saving new text
                if randint(0, 100) > (100 - chance):  # sending new message
                    vk.messages.send(message=generate_text(), chat_id=event.chat_id, random_id=get_random_id())
        if event.type == VkBotEventType.MESSAGE_NEW and len(event.message.attachments) > 0:
            append_attaches = []
            for attach in event.message.attachments:
                if attach['type'] == 'photo':
                    append_attaches.append(attach['photo']['sizes'][-1]['url'])
            with open('img_sources.txt', 'a') as img_file:
                img_file.writelines(append_attaches)
    except Exception as e:
        try:
            vk.messages.send(message=f'Я обдристался :(\n{e}\nХорошо, что Денис обернул всё в try/except и я не упал.',
                             chat_id=event.chat_id, random_id=get_random_id())
        except Exception as e:
            print(e)

