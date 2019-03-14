import os
import json
import hashlib

class FileWorker:
    
    def __init__(self, f_name):

        self.lib_path = os.path.dirname(__file__)
        self.file_path = '{lib_path}/data/{filename}'.format(lib_path=self.lib_path, filename=f_name) 

    def look(self):

        if os.path.isfile(self.file_path):
            return True
        else:
            return False

    def create(self):
        
        fi = open(self.file_path, 'w+')
        fi.write('[]')
        fi.close()
    
    def load(self):
        
        fi = open(self.file_path, 'r')
        store = json.loads(fi.read())
        fi.close()
        return store

    def dump(self, store):

        obj = json.dumps(store, sort_keys=True, indent=4)
        
        return obj
    
    def hash(self, store):
        
        md5 = hashlib.md5(store)
        md5hash = md5.hexdigest()
        return md5hash

    def saveStore(self, store):
        fi = open(self.file_path, 'w+')
        fi.write(store)
        fi.close()


    