import vk
import time
from messages.private_dialog import Private_dialog


id = 452
delay = 0.1

file = open('tokens.txt', 'r')
token = file.readline().rstrip()
print(token[:10])

session = vk.Session(token)
api = vk.API(session)
api.VK_API_VERSION = 5.139

profile_info = api.account.getProfileInfo(v=api.VK_API_VERSION)

while True:
    dialog = Private_dialog()
    dialog.setup(api, None, profile_info, id)
    dialog.setupUI()
    print('ID №{} done'.format(id))
    id += 1
    time.sleep(delay)
