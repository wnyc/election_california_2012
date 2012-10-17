import zipfile

class ZipDict:
    def __init__(self, payload):
        self.zf = zipfile.ZipFile(payload)
    def __iter__(self):
        return iter(self.zf.namelist())

    def keys(self):
        return self.zf.namelist()

    def values(self):
        for key in self.keys():
            yield self[key]

    def __getitem__(self, key):
        return self.zf.open(key)
    
    def get(self, key, default=None):
        try:
            return self.zf.open(key)
        except KeyError:
            return default
        
        

