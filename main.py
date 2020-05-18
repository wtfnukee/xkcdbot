import requests
from bs4 import BeautifulSoup


def getcomics():
    url = "https://xkcd.ru/random/1/"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    linkslist = []
    for link in soup.find_all('img'):
        url = link.get('src')
        linkslist.append(url)
    url = linkslist[0]
    name = url[18:]

    def downloadcomics():
        with open(name, 'wb') as handle:
            response = requests.get(url, stream=True)

            if not response.ok:
                print(response)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)

    return url


token = '870916754:AAEQ0uzA3rPo5DH-d0u3c6tks1V8stldNWk'


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

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update


xkcdbot = BotHandler(token)


def main():
    new_offset = None

    while True:
        xkcdbot.get_updates(new_offset)

        last_update = xkcdbot.get_last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        if last_chat_text.lower() == r'/xkcd':
            xkcdbot.send_message(last_chat_id, getcomics())
        if last_chat_text.lower() == r'/start':
            xkcdbot.send_message(last_chat_id, 'Привет, {}!'.format(last_chat_name))

        new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
