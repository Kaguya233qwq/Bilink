import httpx
import json
import qrcode
import asyncio

Notice = "\033[32m[Notice]\033[0m"


class BiliLogin:
    """登录类"""

    def __init__(self):
        self.url_qrcode = 'http://passport.bilibili.com/x/passport-login/web/qrcode/generate'
        self.url_poll = 'http://passport.bilibili.com/x/passport-login/web/qrcode/poll'

        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                '53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501',
        }

    async def get_qrcode(self):
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                url=self.url_qrcode,
                headers=self.headers
            )
            qrcode_obj = json.loads(resp.text)
            qrcode_url = qrcode_obj['data']['url']
            qrcode_key = qrcode_obj['data']['qrcode_key']
            return qrcode_url, qrcode_key

    @staticmethod
    async def save_qrcode(url_qrcode):
        global Notice
        qr_code = qrcode.QRCode()
        qr_code.add_data(url_qrcode)
        qr_code.print_ascii(invert=True)
        qr_code = qr_code.make_image()
        qr_code.save('qrCode.png')
        print(Notice + ' 二维码生成成功，请使用bilibili客户端扫描确认')

    async def polling(self, qrcode_key):
        """轮询扫码状态"""
        while True:
            async with httpx.AsyncClient() as client:
                params = {
                    'qrcode_key': qrcode_key
                }
                resp = await client.get(
                    url=self.url_poll,
                    headers=self.headers,
                    params=params
                )
                poll = json.loads(resp.text)
                state_code = poll['data']['code']
                message = poll['data']['message']
                if state_code == 0:
                    print(Notice + ' ' + '登录成功！')
                    sessdata = resp.cookies.get('SESSDATA')
                    dede_userid = resp.cookies.get('DedeUserID')
                    bili_jct = resp.cookies.get('bili_jct')
                    return sessdata, dede_userid, bili_jct
                elif state_code == 86038:
                    print(Notice + ' ' + message)
                    break
            await asyncio.sleep(2)
