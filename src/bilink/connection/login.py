import json
import asyncio
import qrcode  # type: ignore
from typing import Optional

from ..utils.models import Api
from ..utils.logger import Logger
from ..utils.tools import create_headers
from ..utils.exception import GetLoginQrcodeFailedError
from .client import BilibiliClient


class LoginApi:
    """登录专用API服务"""

    def __init__(self, client: BilibiliClient):
        self.client = client

    async def get_qrcode(self) -> Optional[dict[str, str]]:
        """获取二维码"""
        http = self.client.get_client()
        resp = await http.get(
            url=Api.QRCODE_GENERATE,
            headers=create_headers(),
            follow_redirects=True,  # type: ignore
        )
        if resp.status_code == 200:
            qrcode_obj = resp.json()
            qrcode_url = str(qrcode_obj["data"]["url"])
            qrcode_key = str(qrcode_obj["data"]["qrcode_key"])
            return {"url": qrcode_url, "key": qrcode_key}
        else:
            raise GetLoginQrcodeFailedError()

    async def save_qrcode(self, url_qrcode: str) -> None:
        """保存二维码到本地并在终端输出"""
        qr_code = qrcode.QRCode(
            # Using int manually, ERROR_CORRECT_L is 1 usually or qrcode.constants.ERROR_CORRECT_L
            error_correction=1,
            box_size=1,
            border=2,
        )
        qr_code.add_data(url_qrcode)
        qr_code.print_ascii(invert=True)
        # Type ignorance to skip Pillow related static issues
        img = qr_code.make_image()  # type: ignore
        # Since 'make_image' returns an image instance, we write to a file via Pillow
        with open("qrCode.png", "wb") as f:
            img.save(f)  # type: ignore

    async def polling(self, qrcode_key: str) -> Optional[dict[str, str]]:
        """轮询扫码状态"""
        while True:
            http = self.client.get_client()
            params = {"qrcode_key": qrcode_key}
            resp = await http.get(
                url=Api.QRCODE_POLL,
                headers=create_headers(),  # type: ignore
                params=params,
                follow_redirects=True,  # type: ignore
            )
            poll = json.loads(resp.text)
            state_code = poll["data"]["code"]
            message = str(poll["data"]["message"])
            if state_code == 0:
                Logger.success("登录成功！")
                sess_data = resp.cookies.get("SESSDATA")
                user_id = resp.cookies.get("DedeUserID")
                ck_md5 = resp.cookies.get("DedeUserID__ckMd5")
                bili_jct = resp.cookies.get("bili_jct")
                sid = resp.cookies.get("sid")
                cookies = {
                    "SESSDATA": str(sess_data),
                    "DedeUserID": str(user_id),
                    "bili_jct": str(bili_jct),
                    "DedeUserID__ckMd5": str(ck_md5),
                    "sid": str(sid),
                }
                return cookies
            elif state_code == 86038:
                Logger.warning(message)
                return None
            elif state_code == 86101:
                await asyncio.sleep(2)
            elif state_code == 86090:
                Logger.success("已扫码，请在手机上确认")
                await asyncio.sleep(2)
            else:
                Logger.error(message)
                return None


async def login_by_qrcode(client: BilibiliClient) -> Optional[dict[str, str]]:
    """通用bilibili扫码登录"""
    api = LoginApi(client)
    qr = await api.get_qrcode()
    if qr is None:
        return None
    await api.save_qrcode(qr.get("url", ""))  # 保存二维码图片并输出至终端
    Logger.success("二维码生成成功，请使用bilibili客户端扫描确认")
    return await api.polling(qr.get("key", ""))
