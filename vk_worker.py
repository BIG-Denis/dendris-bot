
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import json
from message_generator import *
import re
from anekdots import *
from demotivator import *


# All functions

def updater():
    try:
        make_uniq()
        print('Source got updated!')
    except Exception as e:
        print(e)


def change_chance(new_chance: int):
    global chance
    with open('res/chance.txt', 'w') as file:
        file.write(str(new_chance))
    chance = new_chance


def get_random_photo_url():
    with open('res/img_sources.txt', 'r') as img_file:
        return choice(img_file.readlines())


def admin_check(_event, _vk) -> bool:
    admins = []
    for elem in _vk.messages.getConversationMembers(peer_id=_event.message.peer_id, fields='items')['items']:
        if elem.get('is_admin') and elem['is_admin'] is True:
            admins.append(elem['member_id'])
    if _event.message.from_id in admins:
        return True
    return False


# Reading things from files

with open("res/token.json") as token_file:
    json_file = json.load(token_file)
    token = json_file["token"]

with open("res/message_patterns.json") as mess_patt_file:
    json_file = json.load(mess_patt_file)
    help_msg = '\n'.join(json_file["help"])
    dem_error_msg = json_file["dem_error"]
    chance_error_msg = json_file["chance_error"]
    ok_msg = json_file["ok_msg"]
    wrong_msg = json_file["wrong_pattern_msg"]
    only_adm_msg = json_file["only_adm_msg"]

with open('res/chance.txt', 'r') as file:
    chance = int(file.read())


vk_session = vk_api.VkApi(token=token, api_version='5.131')
longpoll = VkBotLongPoll(vk_session, 210242413)
vk = vk_session.get_api()
upload = vk_api.VkUpload(vk)


update_source('old_srcs/old_src')


# main polling
for event in longpoll.listen():  # MAKE TRY/EXCEPT FOR POLLING

    try:
        if event.type == VkBotEventType.MESSAGE_NEW and len(event.message.text) > 0:

            if re.match('[Ss] .*', event.message.text) is not None:  # if Sglypa command
                continue

            elif re.match('[Dd] .*', event.message.text) is not None:  # if Dendris command
                if re.match('[Dd] [Hh]elp', event.message.text) is not None:
                    vk.messages.send(message=help_msg, chat_id=event.chat_id, random_id=get_random_id())
                elif re.match('[Dd] [Gg] [Aa]', event.message.text) is not None:
                    vk.messages.send(message=get_anekdot(), chat_id=event.chat_id, random_id=get_random_id())
                elif re.match('[Dd] [Gg] [Dd]', event.message.text) is not None:
                    dem_code = create_dem(get_random_photo_url(), generate_text(25), generate_text(50))
                    if dem_code == 0:
                        photo = upload.photo_messages('res/last_dem.jpg')
                        owner_id = photo[0]['owner_id']
                        photo_id = photo[0]['id']
                        access_key = photo[0]['access_key']
                        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                        vk.messages.send(chat_id=event.chat_id, random_id=get_random_id(), attachment=attachment)
                    else:
                        vk.messages.send(message=dem_error_msg, chat_id=event.chat_id, random_id=get_random_id())
                elif re.match('[Dd] c [\d]+', event.message.text) is not None:
                    if admin_check(event, vk):
                        new_chance = int(event.message.text.split(' ')[2])
                        if 0 <= new_chance <= 100:
                            change_chance(new_chance)
                            vk.messages.send(message=ok_msg, chat_id=event.chat_id, random_id=get_random_id())
                        else:
                            vk.messages.send(message=chance_error_msg, chat_id=event.chat_id, random_id=get_random_id())
                    else:
                        vk.messages.send(message=only_adm_msg, chat_id=event.chat_id, random_id=get_random_id())
                else:
                    vk.messages.send(message=wrong_msg, chat_id=event.chat_id, random_id=get_random_id())

            elif event.message.from_id != -190195384:  # if not a command and not from Sglypa
                write_source(event.message.text)  # saving new text
                if randint(0, 100) > (100 - chance):  # sending new message
                    vk.messages.send(message=generate_text(250), chat_id=event.chat_id, random_id=get_random_id())

        if event.type == VkBotEventType.MESSAGE_NEW and len(event.message.attachments) > 0 \
                and event.message.from_id != -190195384:  # save photos
            append_attaches = []
            for attach in event.message.attachments:
                if attach['type'] == 'photo':
                    append_attaches.append(attach['photo']['sizes'][-1]['url'])
            with open('res/img_sources.txt', 'a') as img_file:
                append_attaches = [f'{elem}\n' for elem in append_attaches]
                img_file.writelines(append_attaches)

    except Exception as e:  # something caused while running all from above
        try:
            vk.messages.send(message=f'Я обдристался :(\n{e}\nХорошо, что Денис обернул всё в try/except и я не упал.',
                             chat_id=event.chat_id, random_id=get_random_id())
            print(e)
        except Exception as e:
            print(f'Даже тут try/except не помог...\n{e}')
