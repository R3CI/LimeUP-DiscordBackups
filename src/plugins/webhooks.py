from src import *
from src.plugins.log import *

class webhook:
    def log(hook, msg):
        requests.post(
            hook, 
                json={
                'content': msg
            }
        )