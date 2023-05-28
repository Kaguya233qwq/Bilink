import httpx
import json
import qrcode
import asyncio
from bilink.utils.logger import Logger


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
            'upgrade-insecure-requests': "1"
        }

    async def get_qrcode(self):
        """获取二维码"""
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                url=self.url_qrcode,
                headers=self.headers,
                follow_redirects=True
            )
            if resp.status_code == 200:
                qrcode_obj = resp.json()
                qrcode_url = qrcode_obj['data']['url']
                qrcode_key = qrcode_obj['data']['qrcode_key']
                return {
                    "url":qrcode_url,
                    "key":qrcode_key
                }
            else:
                Logger.warning(f"没有获取到二维码信息,返回值：{resp.status_code}")
                return None
        

    @staticmethod
    async def save_qrcode(url_qrcode):
        """保存二维码到本地并在终端输出"""
        qr_code = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
            border=2
        )
        qr_code.add_data(url_qrcode)
        qr_code.print_ascii(invert=True)
        qr_code = qr_code.make_image()
        qr_code.save('qrCode.png')
        Logger.success(' 二维码生成成功，请使用bilibili客户端扫描确认')

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
                    params=params,
                    follow_redirects=True
                )
                poll = json.loads(resp.text)
                state_code = poll['data']['code']
                message = poll['data']['message']
                if state_code == 0:
                    Logger.success('登录成功！')
                    sess_data = resp.cookies.get('SESSDATA')
                    user_id = resp.cookies.get('DedeUserID')
                    bili_jct = resp.cookies.get('bili_jct')
                    cookies = {
                        'SESSDATA': sess_data,
                        'DedeUserID': user_id,
                        'bili_jct': bili_jct
                    }
                    return cookies
                elif state_code == 86038:
                    Logger.warning(message)
                    return None
            await asyncio.sleep(2)
