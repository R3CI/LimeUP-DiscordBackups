DBG = True # DEBUG ,MODE use if u actualy know reqs and have smth broken

import os
import time
try:
    import tls_client
    import requests
    import re
    from colorama import Fore as F, init; init(autoreset=True)
    import base64
    from Crypto.Cipher import AES
    from win32crypt import CryptUnprotectData
    import json
    import sys
except:
    for lib in ['tls-client', 'typing-extensions', 'colorama', 'pycryptodome', 'pypiwin32', 'requests']:
        os.system(f'pip install {lib}')
    
    os.system('cls')
    for _ in range(25):
        print('Now restart the software!!!')
    input('')