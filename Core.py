import json
import os
import datetime


class Core:
    def __init__(self, filename):
        self.filename = filename
        self.__all_subs = {}
        if os.path.exists(filename):
            self.load()
        
    def add_sub(self, chat_id, query, price):
        chat_id = str(chat_id)
        self.init_chat(chat_id)
        self.__all_subs[chat_id][query] = { 
            'price': price,
            'founded': False
            }
        
    def remove_sub(self, chat_id, query):
        chat_id = str(chat_id)
        self.init_chat(chat_id)
        if chat_id in self.__all_subs:
            if query in self.__all_subs[chat_id]:
                self.__all_subs[chat_id].pop(query)

    def get_subs(self, chat_id):
        chat_id = str(chat_id)
        self.init_chat(chat_id)
        return self.__all_subs[chat_id]
    
    def init_chat(self, chat_id):
        if not str(chat_id) in self.__all_subs:
            self.__all_subs[str(chat_id)] = {}

    def get_users(self):
        return list(self.__all_subs.keys())
    
    def get_query(self, chat_id, query):
        chat_id = str(chat_id)
        return self.__all_subs[chat_id][query]

    def set_founded(self, chat_id, query):
        chat_id = str(chat_id)
        self.__all_subs[chat_id][query]['founded'] = True

    def dump(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.__all_subs, f)

    def load(self):
        with open(self.filename, 'r', encoding='utf-8') as f:
            self.__all_subs.update(json.load(f))