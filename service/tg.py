import requests
from service import settings

def send_telegram(text=''):
    url = "https://api.telegram.org/bot{}/sendMessage".format(settings.DATABASE['TG_TOKEN'])
    channel_id = settings.DATABASE['TG_CHAT']
    try:
        r = requests.post(url, data={
                 "chat_id": channel_id,
                 "text": text
              })
    except Exception as ex:
        print('{}: {}'.format(r,ex))

if __name__=='__main__':
    send_telegram('wrgerger')
    send_telegram('kjwfblwjerbflwe')
    send_telegram('efwe4rwefc')