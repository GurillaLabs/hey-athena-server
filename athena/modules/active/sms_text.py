"""
    Uses the external IP to find geographical info

    Usage Examples:
        - "What time is it?"
        - "Where am I?"
"""

import re

from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena.apis import api_lib
from athena import settings


class SendTextTask(ActiveTask):

    def __init__(self):
        super().__init__(patterns=[r'.*\btext (.*)'])
        self.groups = {1: 'msg'}

    def match(self, text):
        return self.match_and_save_groups(text, self.groups)

    def action(self, text):
        for key_num, aliases in settings.CONTACTS.items():
            for alias in aliases:
                if alias in self.msg.lower():
                    self.msg = self.msg.lower().replace(alias, key_num, 1)
                    break

        num = None
        num_match = re.match(r'\b((\(\d{3}\)|\d{3})-?\d{3}-?\d{4})\s?(.*)', self.msg)
        if num_match:
            num = num_match.group(1).replace('(', '').replace(')', '').replace('-', '')
            self.msg = num_match.group(3)

        self.msg += ' - sent from Hey Athena'
        api_lib['sms_text_api'].send_text(self.msg, num)


class SmsText(Module):

    def __init__(self):
        tasks = [SendTextTask()]
        super().__init__('sms_text', tasks, priority=3)
