class _Handler:
    def __init__(self):
        self.handle_list = []

    def _callback_func(keywords: str, reply: str): ...

    def register(self, keywords: str, reply: str):
        self.handle_list.append((keywords, reply))

    def handle_all(self):
        for h in self.handle_list:
            self._callback_func(h[0], h[1])


handler = _Handler()
