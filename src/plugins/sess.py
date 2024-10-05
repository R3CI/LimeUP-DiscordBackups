from src import *

def getsess(token):
    sess = tls_client.Session(
        client_identifier='chrome_120',
        random_tls_extension_order=True
    )

    heads = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,pl;q=0.9',
        'Content-Type': 'application/json',
        'Authorization': token,
        'Origin': 'https://discord.com',
        'Priority': 'u=1, i',
        'Sec-Ch-Ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9164 Chrome/124.0.6367.243 Electron/30.2.0 Safari/537.36',
        'X-Debug-Options': 'bugReporterEnabled',
        'X-Discord-Locale': 'en-US',
        'X-Discord-Timezone': 'Europe/Berlin',
        'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MTY0Iiwib3NfdmVyc2lvbiI6IjEwLjAuMjI2MzEiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJ4NjQiLCJzeXN0ZW1fbG9jYWxlIjoiZW4tR0IiLCJicm93c2VyX3VzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBkaXNjb3JkLzEuMC45MTY0IENocm9tZS8xMjQuMC42MzY3LjI0MyBFbGVjdHJvbi8zMC4yLjAgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjMwLjIuMCIsIm9zX3Nka192ZXJzaW9uIjoiMjI2MzEiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjozMzAyNzEsIm5hdGl2ZV9idWlsZF9udW1iZXIiOjUyODI2LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=='
    }

    r = sess.get(
        'https://discord.com',
        headers=heads
    )

    cookievals = r.cookies.get_dict()
    cocks = {
        '__dcfduid': cookievals['__dcfduid'],
        '__sdcfduid': cookievals['__sdcfduid'],
        '_cfuvid': cookievals['_cfuvid'],
        'locale': 'en-US',
        '__cfruid': cookievals['__cfruid']
    }

    return heads, sess, cocks