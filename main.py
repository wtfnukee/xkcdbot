import requests
from bs4 import BeautifulSoup
import re
import os


def getcomics():
    url = "https://xkcd.ru/random/0/"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')


    url = soup.find('img').get('src')

    text = soup.find("div", class_="comics_text", text=True).get_text().strip()

    print(text, '\n', url)
    name = url[18:]
    return text + '\n'+ url


#
# def downloadcomics():
#    with open(name, 'wb') as handle:
#        response = requests.get(url, stream=True)
#
#        if not response.ok:
#            print(response)
#
#        for block in response.iter_content(1024):
#           if not block:
#                break
#
#            handle.write(block)
#


token = os.environ.get('TELETOKEN', None)


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def send_photo(self, chat_id, photo):
        params = {'chat_id': chat_id, 'photo': photo}
        method = 'sendPhoto'
        resp = requests.post(self.api_url + method, params)
        return resp

    def send_audio(self, chat_id, audio):
        params = {'chat_id': chat_id, 'audio': audio}
        method = 'sendAudio'
        resp = requests.post(self.api_url + method, params)
        return resp

    def send_document(self, chat_id, document):
        params = {'chat_id': chat_id, 'document': document}
        method = 'sendDocument'
        resp = requests.post(self.api_url + method, params)
        return resp

    def send_sticker(self, chat_id, sticker):
        params = {'chat_id': chat_id, 'sticker': sticker}
        method = 'sendSticker'
        resp = requests.post(self.api_url + method, params)
        return resp

    def send_video(self, chat_id, video):
        params = {'chat_id': chat_id, 'video': video}
        method = 'sendVideo'
        resp = requests.post(self.api_url + method, params)
        return resp

    def send_voice(self, chat_id, voice):
        params = {'chat_id': chat_id, 'voice': voice}
        method = 'sendVoice'
        resp = requests.post(self.api_url + method, params)
        return resp

    def send_location(self, chat_id, latitude, longitude):
        params = {'chat_id': chat_id, 'latitude': latitude, 'longitude': longitude}
        method = 'sendLocation'
        resp = requests.post(self.api_url + method, params)
        return resp

    def send_venue(self, chat_id, latitude, longitude, title, address):
        params = {'chat_id': chat_id, 'latitude': latitude, 'longitude': longitude, 'title': title, 'address': address}
        method = 'sendVenue'
        resp = requests.post(self.api_url + method, params)
        return resp

    def send_contact(self, chat_id, phone_number, first_name):
        params = {'chat_id': chat_id, 'phone_number': phone_number, 'first_name': first_name}
        method = 'sendContact'
        resp = requests.post(self.api_url + method, params)
        return resp

    def send_chatAction(self, chat_id, action):
        params = {'chat_id': chat_id, 'action': action}
        method = 'sendChatAction'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_userProfilePhotos(self, user_id):
        params = {'user_id': user_id}
        method = 'getUserProfilePhotos'
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result) - 1]

        print(last_update)

        return last_update


xkcdbot = BotHandler(token)


def main():
    new_offset = 0

    while True:
        try:
            xkcdbot.get_updates(new_offset)
            last_update = xkcdbot.get_last_update()

            last_update_id = last_update['update_id']
            last_chat_text = last_update['message']['text']
            last_chat_id = last_update['message']['chat']['id']
            last_chat_name = last_update['message']['chat']['first_name']

            if last_chat_text.lower() == r'/xkcd':
                xkcdbot.send_message(last_chat_id, getcomics())
            elif last_chat_text.lower() == r'/start':
                xkcdbot.send_message(last_chat_id, 'Добро пожаловать, {}!'.format(last_chat_name))
            elif last_chat_text.lower() == r'/help':
                xkcdbot.send_video(last_chat_id,
                                   'BAACAgIAAxkBAAIBRF7ClmA-oqskTgUOyZ_aSEbtFB5bAAKHBgACFZMRSmecvLZFUgqeGQQ)')
            elif last_chat_text.lower() == r'/rick':
                xkcdbot.send_audio(last_chat_id, 'https://imgs.xkcd.com/blag/xkcd_389.mp3')
            elif last_chat_text.lower() == r'привет':
                xkcdbot.send_message(last_chat_id, 'Привет, {}!'.format(last_chat_name))
            elif last_chat_text.lower() == r'пока':
                xkcdbot.send_message(last_chat_id, 'Прощай, {}('.format(last_chat_name))
            else:
                xkcdbot.send_message(last_chat_id, 'Ничего не понял(')

            new_offset = last_update_id + 1

        except Exception:
            pass


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
