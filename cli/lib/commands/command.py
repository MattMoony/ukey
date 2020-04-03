class Command(object):
    def __init__(self, client):
        self.cl = client

    def exec(self, args):
        raise NotImplementedError
    
    def compl(self, text):
        return None