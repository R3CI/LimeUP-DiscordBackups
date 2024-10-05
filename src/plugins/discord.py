from src import *
from src.plugins.sess import *
from src.plugins.log import *

class discord:
    def __init__(self, token):
        self.token = token
        self.headers, self.sess, self.cookies = getsess(self.token)
        self.userid = base64.b64decode(self.token.split('.')[0] + '==').decode()

        self.channelid = None

    def getservers(self):
        while True:
            servers = []
            r = self.sess.get(
                'https://discord.com/api/v9/users/@me/guilds', 
                headers=self.headers, 
                cookies=self.cookies
            )

            dlog(r.status_code, r.text)

            if r.status_code == 200:
                log(F.GREEN, F.GREEN, 'Got servers')
                for server in r.json():
                    servers.append((server['id'], server['name']))
                return servers
            
            elif r.status_code == 429:
                limit = float(r.json().get('retry_after', 0))
                log(F.YELLOW, F.YELLOW, f'Rate Limited (Waiting {limit}s)')
                time.sleep(limit)
                continue

            else:
                log(F.RED, F.RED, 'Failed to get servers')
                return []
            
    def getfriends(self):
        while True:
            friends = []
            r = self.sess.get(
                'https://discord.com/api/v9/users/@me/relationships', 
                headers=self.headers, 
                cookies=self.cookies
            )

            dlog(r.status_code, r.text)

            if r.status_code == 200:
                log(F.GREEN, F.GREEN, 'Got friends')
                for friend in r.json():
                    user = friend.get('user', {})
                    friends.append((user.get('id'), user.get('username')))
                return friends
            
            elif r.status_code == 429:
                limit = float(r.json().get('retry_after', 0))
                log(F.YELLOW, F.YELLOW, f'Rate Limited (Waiting {limit}s)')
                time.sleep(limit)
                continue

            else:
                log(F.RED, F.RED, 'Failed to get friends')
                return []

    def getgifs(self):
        while True:
            r = self.sess.get(
                'https://discord.com/api/v9/users/@me/settings-proto/2', 
                headers=self.headers, 
                cookies=self.cookies
            )

            dlog(r.status_code, r.text)

            if r.status_code == 200:
                log(F.GREEN, F.GREEN, 'Got gifs')
                return r.json()['settings']
            
            elif r.status_code == 429:
                limit = float(r.json().get('retry_after', 0))
                log(F.YELLOW, F.YELLOW, f'Rate Limited (Waiting {limit}s)')
                time.sleep(limit)
                continue

            else:
                log(F.RED, F.RED, 'Failed to get gifs')
                return []

    def getuserinfo(self):
        while True:
            r = self.sess.get(
                f'https://discord.com/api/v9/users/{self.userid}/profile', 
                headers=self.headers, 
                cookies=self.cookies
            )

            dlog(r.status_code, r.text)

            if r.status_code == 200:
                log(F.GREEN, F.GREEN, 'Got user info')
                return r.json()
            
            elif r.status_code == 429:
                limit = float(r.json().get('retry_after', 0))
                log(F.YELLOW, F.YELLOW, f'Rate Limited (Waiting {limit}s)')
                time.sleep(limit)
                continue

            else:
                log(F.RED, F.RED, 'Failed to get user info')
                return []
        
    def getchannels(self, serverid):
        while True:
            channels = []
            r = self.sess.get(
                f'https://discord.com/api/v9/guilds/{serverid}/channels', 
                headers=self.headers, 
                cookies=self.cookies
            )

            dlog(r.status_code, r.text)

            if r.status_code == 200:
                log(F.GREEN, F.GREEN, 'Got server channels')
                for channel in r.json()[:5]:
                    channels.append((channel['id']))
                return channels
            
            elif r.status_code == 429:
                limit = float(r.json().get('retry_after', 0))
                log(F.YELLOW, F.YELLOW, f'Rate Limited (Waiting {limit}s)')
                time.sleep(limit)
                continue

            else:
                log(F.RED, F.RED, 'Failed to get chanmels')
                return []
            
    def getvanity(self, serverid, servername):
        while True:
            r = self.sess.get(
                f'https://discord.com/api/v9/guilds/{serverid}', 
                headers=self.headers, 
                cookies=self.cookies
            )

            dlog(r.status_code, r.text)

            if r.status_code == 200:
                try:
                    vanity = r.json()['vanity_url_code']
                except:
                    vanity = 'Unknown'
                
                if vanity != 'Unknown':
                    log(F.GREEN, F.GREEN, f'Got vanity for {servername}')
                    return f'https://discord.gg/{r.json()['vanity_url_code']}'
                else:
                    log(F.RED, F.RED, f'Failed to get vanity for {servername}')
                    return 'Unknown'
            
            elif r.status_code == 429:
                limit = float(r.json().get('retry_after', 0))
                log(F.YELLOW, F.YELLOW, f'Rate Limited (Waiting {limit}s)')
                time.sleep(limit)
                continue

            else:
                log(F.RED, F.RED, f'Failed to get vanity for {servername}')
                return 'Unknown'

    def getinvite(self, channelids, servername, serverid):
            i = 0
            for channelid in channelids:
                r = self.sess.post(
                    f'https://discord.com/api/v9/channels/{channelid}/invites', 
                    headers=self.headers, 
                    cookies=self.cookies,
                    json={
                        'max_age': 0,
                        'max_uses': 0,
                        'target_type': None,
                        'temporary': False,
                        'flags': 0
                    }
                )

                dlog(r.status_code, r.text)

                if r.status_code == 200:
                    i += 1
                    log(F.GREEN, F.GREEN, f'Made an invite for {servername} {i}/5')
                    return f'https://discord.gg/{r.json()['code']}'
                
                elif r.status_code == 429:
                    limit = float(r.json().get('retry_after', 0))
                    log(F.YELLOW, F.YELLOW, f'Rate Limited (Waiting {limit}s)')
                    time.sleep(limit)
                    channelids.append(channelid)
                    continue

                elif r.status_code == 403:
                    vanity = self.getvanity(serverid, servername)
                    return f'https://discord.gg/{vanity}'
                    break

                else:
                    i += 1
                    log(F.RED, F.RED, f'Failed to make a inv for {servername} {i}/5')
                    continue
            
            log(F.RED, F.RED, f'Failed to make a inv for {servername} {i}/5')
            return ''
    
    # Restoring

    def restorebio(self, bio):
        while True:
            r = self.sess.patch(
                f'https://discord.com/api/v9/users/%40me/profile', 
                headers=self.headers, 
                cookies=self.cookies,
                json={
                    'bio': bio
                }
            )

            dlog(r.status_code, r.text)

            if r.status_code == 200:
                log(F.GREEN, F.GREEN, f'Restored bio')
                break
            
            elif r.status_code == 429:
                limit = float(r.json().get('retry_after', 0))
                log(F.YELLOW, F.YELLOW, f'Rate Limited (Waiting {limit}s)')
                time.sleep(limit)
                continue

            else:
                log(F.RED, F.RED, f'Failed to restore bio')
                break

    def createsever(self, avatarurl):
        r = requests.get(avatarurl)
        img_data = base64.b64encode(r.content).decode('utf-8')
        icon = f'data:image/jpeg;base64,{img_data}'

        while True:
            r = self.sess.post(
                'https://discord.com/api/v9/guilds', 
                headers=self.headers, 
                cookies=self.cookies,
                json={
                    'name': 'LimeUP - Discord backup',
                    'icon': None,
                    'channels': [],
                    'guild_template_code': '2TffvPucqHkN',
                    'icon': icon,
                    'system_channel_id': None
                }
            )

            dlog(r.status_code, r.text)

            if r.status_code == 201:
                log(F.GREEN, F.GREEN, f'Made the backup server')
                self.channelid = r.json()['system_channel_id']
                break
            
            elif r.status_code == 429:
                limit = float(r.json().get('retry_after', 0))
                log(F.YELLOW, F.YELLOW, f'Rate Limited (Waiting {limit}s)')
                time.sleep(limit)
                continue

            else:
                log(F.RED, F.RED, f'Failed to make the restore server')
                break

    def restoreavatar(self, avatarurl):
        r = requests.get(avatarurl)
        img_data = base64.b64encode(r.content).decode('utf-8')
        icon = f'data:image/jpeg;base64,{img_data}'

        while True:
            r = self.sess.patch(
                'https://discord.com/api/v9/users/@me', 
                headers=self.headers, 
                cookies=self.cookies,
                json={
                    'avatar': icon
                }
            )

            dlog(r.status_code, r.text)

            if r.status_code == 200:
                log(F.GREEN, F.GREEN, f'Restored avatar')
                break
            
            elif r.status_code == 429:
                limit = float(r.json().get('retry_after', 0))
                log(F.YELLOW, F.YELLOW, f'Rate Limited (Waiting {limit}s)')
                time.sleep(limit)
                continue

            else:
                log(F.RED, F.RED, f'Failed to restore avatar')
                break

    def sendmessage(self, msg):
        while True:
            r = self.sess.post(
                f'https://discord.com/api/v9/channels/{self.channelid}/messages', 
                headers=self.headers, 
                cookies=self.cookies,
                json={
                    'content': msg
                }
            )

            dlog(r.status_code, r.text)

            if r.status_code == 200:
                log(F.GREEN, F.GREEN, f'Sent a message for the backup')
                break
            
            elif r.status_code == 429:
                limit = float(r.json().get('retry_after', 0))
                log(F.YELLOW, F.YELLOW, f'Rate Limited (Waiting {limit}s)')
                time.sleep(limit)
                continue

            else:
                log(F.RED, F.RED, f'Failed to send a backup message')
                break

    def restoregifs(self, gifs):
        while True:
            r = self.sess.patch(
                'https://discord.com/api/v9/users/@me/settings-proto/2', 
                headers=self.headers, 
                cookies=self.cookies,
                json={
                    'settings': gifs
                }
            )

            dlog(r.status_code, r.text)

            if r.status_code == 200:
                log(F.GREEN, F.GREEN, f'Restored gifs')
                break
            
            elif r.status_code == 429:
                limit = float(r.json().get('retry_after', 0))
                log(F.YELLOW, F.YELLOW, f'Rate Limited (Waiting {limit}s)')
                time.sleep(limit)
                continue

            else:
                log(F.RED, F.RED, f'Failed to restore gifs')
                break