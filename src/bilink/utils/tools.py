def create_headers() -> dict:
    headers = {
        "authority": "api.vc.bilibili.com",
        "sec-ch-ua": '"Chromium";v="21", " Not;A Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)"
        " AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/62.0.3202.9 Safari/537.36",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "accept-language": "zh-CN,zh;q=0.9",
    }
    return headers


def create_banner() -> str:
    """
    生成banner
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
    return f"\033[1;34m{banner}\033[0m"
