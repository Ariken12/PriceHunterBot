import json
import os
import datetime


class Core:
    def __init__(self, filename):
        self.filename = filename
        self.all_subs = {
                         }
        if os.path.exists(filename):
            self.load()
        
        
    def add_sub(self, chat_id, query, price):
        chat_id = str(chat_id)
        self.init_chat(chat_id)
        self.all_subs[chat_id][query] = price

    def remove_sub(self, chat_id, query):
        chat_id = str(chat_id)
        self.init_chat(chat_id)
        if chat_id in self.all_subs:
            if query in self.all_subs[chat_id]:
                self.all_subs[chat_id].pop(query)

    def get_subs(self, chat_id):
        chat_id = str(chat_id)
        self.init_chat(chat_id)
        return self.all_subs[chat_id]
    
    def init_chat(self, chat):
        if not chat in self.all_subs:
            self.all_subs[str(chat)] = {}

    def dump(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.all_subs, f)
        with open(datetime.datetime.now().strftime('%Y-%m-%d,%H:%M:%S'), 'w', encoding='utf-8') as f:
            json.dump(self.all_subs, f)

    def load(self):
        with open(self.filename, 'r', encoding='utf-8') as f:
            self.all_subs.update(json.load(f))