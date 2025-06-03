import json


class Core:
    def __init__(self, filename):
        self.filename = filename
        self.all_subs = {
            # '443720544': {
            #                 'Iphone13': 1000000 
            #              }
                         }
        self.load()
        
        
    def add_sub(self, chat_id, query, price):
        self.init_chat(chat_id)
        self.all_subs[chat_id][query] = price

    def remove_sub(self, chat_id, query):
        self.init_chat(chat_id)
        if chat_id in self.all_subs:
            if query in self.all_subs[chat_id]:
                self.all_subs[chat_id].pop(query)

    def get_subs(self, chat_id):
        self.init_chat(chat_id)
        return self.all_subs[chat_id]
    
    def init_chat(self, chat):
        if not chat in self.all_subs:
            self.all_subs[chat] = {}

    def dump(self):
        with open(self.filename, 'wb', encoding='utf-8') as f:
            json.dump(self.all_subs, f)

    def load(self):
        with open(self.filename, 'rb', encoding='utf-8') as f:
            self.all_subs.update(json.load(f))