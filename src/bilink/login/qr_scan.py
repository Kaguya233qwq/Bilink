from typing import Optional, Dict

import httpx
import json
import qrcode
import asyncio

from ..models import Api
from ..utils.logger import Logger
from ..utils.tools import create_headers


class Login:
    """登录类"""

    @classmethod
    async def get_qrcode(cls) -> Optional[Dict[str, str]]:
        """获取二维码"""
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                url=Api.QRCODE_GENERATE,
                headers=create_headers(),
                follow_redirects=True
            )
            if resp.status_code == 200:
                qrcode_obj = resp.json()
                qrcode_url = qrcode_obj['data']['url']
                qrcode_key = qrcode_obj['data']['qrcode_key']
                return {
                    "url": qrcode_url,
                    "key": qrcode_key
                }
            else:
                Logger.warning(f"没有获取到二维码信息,返回值：{resp.status_code}")
                return None

    @staticmethod
    async def save_qrcode(url_qrcode) -> None:
        """保存二维码到本地并在终端输出"""
        qr_code = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
            border=2
        )
        qr_code.add_data(url_qrcode)
        qr_code.print_ascii(invert=True)
        qr_code = qr_code.make_image()
        qr_code.save('qrCode.png')

    @classmethod
    async def polling(cls, qrcode_key) -> Optional[Dict[str, str]]:
        """轮询扫码状态"""
        while True:
            async with httpx.AsyncClient() as client:
                params = {
                    'qrcode_key': qrcode_key
                }
                resp: httpx.Response = await client.get(
                    url=Api.QRCODE_POLL,
                    headers=create_headers(),
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
                    ck_md5 = resp.cookies.get('DedeUserID__ckMd5')
                    bili_jct = resp.cookies.get('bili_jct')
                    sid = resp.cookies.get('sid')
                    cookies = {
                        'SESSDATA': sess_data,
                        'DedeUserID': user_id,
                        'bili_jct': bili_jct,
                        'DedeUserID__ckMd5': ck_md5,
                        'sid': sid
                    }
                    return cookies
                elif state_code == 86038:
                    Logger.warning(message)
                    return None
                elif state_code == 86101:
                    await asyncio.sleep(2)
                elif state_code == 86090:
                    Logger.success('已扫码，请在手机上确认')
                    await asyncio.sleep(2)
                else:
                    Logger.error(message)
                    return None


async def login_by_qrcode() -> Optional[Dict[str, str]]:
    """
    通用bilibili扫码登录
    """
    qr = await Login.get_qrcode()
    if qr:
        url = qr.get('url')
        key = qr.get('key')
        await Login.save_qrcode(url)  # 保存二维码图片并输出至终端
        Logger.success('二维码生成成功，请使用bilibili客户端扫描确认')
        cookies: dict = await Login.polling(key)
        if cookies:
            return cookies
        else:
            Logger.error('未能返回正确数据，登陆失败')
            return None
    else:
        return None
