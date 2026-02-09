import re

class PIIRedactor:
    def __init__(self):
        self.email_pattern = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
        self.phone_pattern = re.compile(r'\+?\d{10,12}')

    def redact(self, text: str) -> str:
        text = self.email_pattern.sub("[EMAIL]", text)
        text = self.phone_pattern.sub("[PHONE]", text)
        return text