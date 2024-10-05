from src.plugins.discord import *
from src.plugins.gettoken import *

args = sys.argv[1:]
forcetoken = None
if len(args) > 0:
    startup = True
    forcetoken = args[0]
else:
    startup = False

while True:
    os.system('cls')
    print(fr'''{F.LIGHTGREEN_EX}
   __   ______  _________  _______
  / /  /  _/  |/  / __/ / / / _  /
 / /___/ // /|_/ / _// /_/ / ___/
/____/___/_/  /_/___/\____/_/    
    ''')

    print(f'''{F.LIGHTGREEN_EX}
INFO > If you use a token protector or sum shit like that disable it as the script gets your token to get servers create invites etc
INFO2 > Only supports if you have Discord APP installed no browsers/canary etc (vencord is fine)

1 > Backup
2 > Restore
3 > Add to startup (no cmd no discord open or anything) 
4 > Remove from startup
    ''')
    if startup:
        e = input(f'{F.LIGHTGREEN_EX}-> ')
    else:
        e = '1'
    if e == '1':
        if not startup:
            tokens = gettoken() or []
            if tokens:
                for index, (token, username) in enumerate(tokens):
                    print(f'{F.GREEN}> {index + 1} - {username} - {token[:35]}...   ')

                choice = input(f'{F.LIGHTGREEN_EX}-> ')
                selected_index = int(choice) - 1
                if 0 <= selected_index < len(tokens):
                    selected_token, selected_username = tokens[selected_index]

                else:
                    log(F.RED, F.RED, 'Not a valid choice')
                    continue

            else:
                log(F.RED, F.RED, 'No tokens found')
                time.sleep(2)
                continue
        
        else:
            selected_token = forcetoken

        discord = discord(selected_token)

        if not os.path.exists('backups'):
            os.makedirs('backups')
        backup_path = 'backups\\backup.json'
        if os.path.exists(backup_path):
            os.remove(backup_path)
        
        with open(backup_path, 'w') as backupfile:
            json.dump({'README': 'The gifs variable (the big chunk) is just a list of all the gifs and looks like that bc they are encoded with base64', 'servers': [], 'friends': [], 'gifs': '', 'avatar': '', 'bio': ''}, backupfile, indent=4)

        with open(backup_path, 'r+') as backupfile:
            bkup = json.load(backupfile)

            # SERVERS
            servers_failed = []
            servers_good = []

            servers = discord.getservers()
            i = 0
            for serverid, servername in servers:
                i += 1
                log(F.GREEN, F.GREEN, f'Getting invite for {servername} {i}/{len(servers)}')
                channels = discord.getchannels(serverid)
                invite = discord.getinvite(channels, servername, serverid)

                if invite != '':
                    bkup['servers'].append({
                        'serverid': serverid,
                        'servername': servername,
                        'invite': invite
                    })
                else:
                    servers_failed.append((servername, serverid,))

            # FRIENDS
            friends = discord.getfriends()
            log(F.GREEN, F.GREEN, f'Got {len(friends)} friends!')
            for friendid, friendname in friends:
                bkup['friends'].append({
                    'friendid': friendid,
                    'friendname': friendname
                })

            # GIFS
            gifs = discord.getgifs()
            log(F.GREEN, F.GREEN, f'Got gifs!')

            bkup['gifs'] = gifs

            # USER INFO
            userinfo = discord.getuserinfo()
            log(F.GREEN, F.GREEN, f'Got userinfo!')

            bkup['avatar'] = f'https://cdn.discordapp.com/avatars/{discord.userid}/{userinfo['user']['avatar']}.jpg'
            bkup['bio'] = userinfo['user']['bio']


            backupfile.seek(0)
            json.dump(bkup, backupfile, indent=4)
            backupfile.truncate()

        log(F.GREEN, F.GREEN, 'Heres a summary of what happened!')

        print('')

        log(F.LIGHTGREEN_EX, F.LIGHTGREEN_EX, 'Amount of servers that we were able to make an invite for')
        print(f'{F.GREEN}> {len(bkup['servers'])}')

        print('')

        log(F.LIGHTGREEN_EX, F.LIGHTGREEN_EX, 'Amount of friends we ware able to make a backup for')
        print(f'{F.GREEN}> {len(bkup['friends'])}')

        print('')

        log(F.LIGHTGREEN_EX, F.LIGHTGREEN_EX, 'Ware we able to backup gifs')
        if bkup['gifs']:
            print(f'{F.GREEN}> Yes')
        else:
            log(F.RED, F.RED, 'No')

        print('')

        log(F.LIGHTGREEN_EX, F.LIGHTGREEN_EX, 'Ware we able to backup avatar')
        if bkup['avatar']:
            print(f'{F.GREEN}> Yes')
        else:
            log(F.RED, F.RED, 'No')

        print('')

        log(F.LIGHTGREEN_EX, F.LIGHTGREEN_EX, 'Ware we able to backup bio')
        if bkup['bio']:
            print(f'{F.GREEN}> Yes')
        else:
            log(F.RED, F.RED, 'No')
        
        print('')

        log(F.LIGHTGREEN_EX, F.LIGHTGREEN_EX, 'Servers that we ware not able to make an invite for')
        for server, serverid in servers_failed:
            print(f'{F.GREEN}> {server} ({serverid})')
        
        print('')
        
        log(F.GREEN, F.GREEN, 'Done (saved backup to backups/backup.json)\nEnter to continue!')
        input('')

    elif e == '2':
        tokens = gettoken() or []
        if tokens:
            for index, (token, username) in enumerate(tokens):
                print(f'{F.GREEN}> {index + 1} - {username} - {token[:35]}...   ')

            choice = input(f'{F.LIGHTGREEN_EX}-> ')
            selected_index = int(choice) - 1
            if 0 <= selected_index < len(tokens):
                selected_token, selected_username = tokens[selected_index]

            else:
                log(F.RED, F.RED, 'Not a valid choice')
                continue

        else:
            log(F.RED, F.RED, 'No tokens found')
            time.sleep(2)
            continue

        discord = discord(selected_token)

        with open('backups/backup.json', 'r') as backupfile:
            bkup = json.load(backupfile)

        discord.createsever(bkup['avatar'])
        discord.restorebio(bkup['bio'])
        discord.restoreavatar(bkup['avatar'])
        discord.restoregifs(bkup['gifs'])

        discord.sendmessage(f'# 💫 Servers')
        for server in bkup['servers']:
            discord.sendmessage(f'```{server['servername']} ({server['serverid']}) ```{server['invite']}')

        discord.sendmessage(f'# 💫 Friends')
        for friend in bkup['friends']:
            discord.sendmessage(f'```{friend['friendname']} ({friend['friendid']}) ```')

        discord.sendmessage(f'# 💫 Finished')
        discord.sendmessage(f'## Restored the backup! Make sure to star the repo and join the discord discord.gg/spamming')

        log(F.GREEN, F.GREEN, 'Done!')
        input('')

    elif e == '3':
        log(F.GREEN, F.GREEN, 'IMPORTANT!! - The token that you set NOW will be used to backup EVERYTIME YOU START UR PC! If the token is invalided ex you log out you will need to remove the current startup (option 4) and run this again!!!')
        tokens = gettoken() or []
        if tokens:
            for index, (token, username) in enumerate(tokens):
                print(f'{F.GREEN}> {index + 1} - {username} - {token[:35]}...   ')

            choice = input(f'{F.LIGHTGREEN_EX}-> ')
            selected_index = int(choice) - 1
            if 0 <= selected_index < len(tokens):
                selected_token, selected_username = tokens[selected_index]

            else:
                log(F.RED, F.RED, 'Not a valid choice')
                continue

        else:
            log(F.RED, F.RED, 'No tokens found')
            time.sleep(2)
            continue

        apptata = os.getenv('APPDATA')

        os.makedirs(f'{apptata}\\LimeUP', exist_ok=True)

        with open(f'{apptata}\\LimeUP\\StartupToken.txt', 'w') as f:
            f.write(selected_token)

        with open(f'{apptata}\\LimeUP\\Startup.txt', 'w') as f:
            f.write('1')

        script_folder = os.path.abspath(__file__)
        startup = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        
        with open(f'{startup}\\LimeUP-AutoBackup.py', 'w') as f:
            f.write(f'''
import os
import subprocess
from tkinter import Tk, messagebox

with open(r'{apptata}\\LimeUP\\StartupToken.txt', 'r') as f:
    tkn = f.read().strip()

with open(r'{apptata}\\LimeUP\\Startup.txt', 'r') as f:
    var = f.read().strip()

def run_main():
    if var != '1':
        exit()

    try:
        subprocess.run(['py', r'{script_folder}\\main.py', tkn], check=True)
    except subprocess.CalledProcessError:
        messagebox.showerror('Error', 'Failed to run the backup on start (LimeUP folder moved?). Try to remove and re-add the startup!')

run_main()
''')

        log(F.GREEN, F.GREEN, 'Done!')
        input('')
    
    else:
        log(F.RED, F.RED, 'Not a valid choice')
        time.sleep(2)