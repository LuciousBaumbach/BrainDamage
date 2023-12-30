# Based on the works of https://github.com/AlessandroZ/LaZagne/blob/master/Windows/lazagne/
import win32api, win32con, win32crypt


class Outlook():
    def __init__(self):
        options = {'command': '-o', 'action': 'store_true', 'dest': 'outlook',
                   'help': 'outlook - IMAP, POP3, HTTP, SMTP, LDPAP (not Exchange)'}

    def run(self):

        accessRead = win32con.KEY_READ | win32con.KEY_ENUMERATE_SUB_KEYS | win32con.KEY_QUERY_VALUE
        keyPath = 'Software\\Microsoft\\Windows NT\\CurrentVersion\\Windows Messaging Subsystem\\Profiles\\Outlook'

        try:
            hkey = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, keyPath, 0, accessRead)
        except Exception, e:
            return

        num = win32api.RegQueryInfoKey(hkey)[0]
        pwdFound = []
        for x in range(0, num):
            name = win32api.RegEnumKey(hkey, x)
            skey = win32api.RegOpenKey(hkey, name, 0, accessRead)

            num_skey = win32api.RegQueryInfoKey(skey)[0]
            if num_skey != 0:
                for y in range(0, num_skey):
                    name_skey = win32api.RegEnumKey(skey, y)
                    sskey = win32api.RegOpenKey(skey, name_skey, 0, accessRead)
                    num_sskey = win32api.RegQueryInfoKey(sskey)[1]
                    for z in range(0, num_sskey):
                        k = win32api.RegEnumValue(sskey, z)
                        if 'password' in k[0].lower():
                            values = self.retrieve_info(sskey, name_skey)
                            # write credentials into a text file
                            if len(values) != 0:
                                pwdFound.append(values)

        # print the results
        return pwdFound

    def retrieve_info(self, hkey, name_key):
        values = {}
        num = win32api.RegQueryInfoKey(hkey)[1]
        for x in range(0, num):
            k = win32api.RegEnumValue(hkey, x)
            if 'password' in k[0].lower():
                try:
                    password = win32crypt.CryptUnprotectData(k[1][1:], None, None, None, 0)[1]
                    values[k[0]] = password.decode('utf16')
                except Exception, e:
                    values[k[0]] = 'N/A'
            else:
                try:
                    values[k[0]] = str(k[1]).decode('utf16')
                except:
                    values[k[0]] = str(k[1])
        return values


