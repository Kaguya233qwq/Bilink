def create_headers() -> dict[str, str]:
    headers = {
        "authority": "api.vc.bilibili.com",
        "sec-ch-ua": '"Chromium";v="21", " Not;A Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)"
        " AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/62.0.3202.9 Safari/537.36",
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "accept-language": "zh-CN,zh;q=0.9",
        "Origin": "https://message.bilibili.com",
        "Referer": "https://message.bilibili.com/",
    }
    return headers


def print_banner() -> None:
    """
    打印banner
    """
    banner = """
 ███████████   ███  ████   ███             █████     
░░███░░░░░███ ░░░  ░░███  ░░░             ░░███      
 ░███    ░███ ████  ░███  ████  ████████   ░███ █████
 ░██████████ ░░███  ░███ ░░███ ░░███░░███  ░███░░███ 
 ░███░░░░░███ ░███  ░███  ░███  ░███ ░███  ░██████░  
 ░███    ░███ ░███  ░███  ░███  ░███ ░███  ░███░░███ 
 ███████████  █████ █████ █████ ████ █████ ████ █████
░░░░░░░░░░░  ░░░░░ ░░░░░ ░░░░░ ░░░░ ░░░░░ ░░░░ ░░░░░ 
    """
    print(f"\033[1;34m{banner}\033[0m")


from functools import reduce
from hashlib import md5
import urllib.parse
import time

mixinKeyEncTab = [
    46,
    47,
    18,
    2,
    53,
    8,
    23,
    32,
    15,
    50,
    10,
    31,
    58,
    3,
    45,
    35,
    27,
    43,
    5,
    49,
    33,
    9,
    42,
    19,
    29,
    28,
    14,
    39,
    12,
    38,
    41,
    13,
    37,
    48,
    7,
    16,
    24,
    55,
    40,
    61,
    26,
    17,
    0,
    1,
    60,
    51,
    30,
    4,
    22,
    25,
    54,
    21,
    56,
    59,
    6,
    63,
    57,
    62,
    11,
    36,
    20,
    34,
    44,
    52,
]


def get_mixin_key(orig: str) -> str:
    return reduce(lambda s, i: s + orig[i], mixinKeyEncTab, "")[:32]


def enc_wbi(params: dict, img_key: str, sub_key: str) -> dict:
    mixin_key = get_mixin_key(img_key + sub_key)
    curr_time = round(time.time())
    params["wts"] = curr_time
    params = dict(sorted(params.items()))
    params = {
        k: "".join(filter(lambda chr: chr not in "!'()*", str(v)))
        for k, v in params.items()
    }
    query = urllib.parse.urlencode(params)
    wbi_sign = md5((query + mixin_key).encode()).hexdigest()
    params["w_rid"] = wbi_sign
    return params
