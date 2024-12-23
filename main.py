import asyncio

from src.bilink import main

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('用户退出')
