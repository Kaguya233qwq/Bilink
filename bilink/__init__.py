from bilink.utils.login import BiliLogin as Login
from asyncio import run
from bilink.utils import listening

if __name__ == '__main__':
    login = Login()
    url, key = run(login.get_qrcode())
    run(login.save_qrcode(url))
    sessdata, userid, jct = run(login.polling(key))
    listening.run(sessdata, userid, jct)
