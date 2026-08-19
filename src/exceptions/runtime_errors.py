class BrowserNotSupportedError(RuntimeError):

    def __init__(self, browser: str):
        super().__init__(f"Browser not supported {browser}")
