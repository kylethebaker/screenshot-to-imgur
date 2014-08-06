import requests
import json
import time
import sys

from base64 import b64encode
from subprocess import call


"""''''''''''''''''''''''''''''''''''

    put your settings here

''''''''''''''''''''''''''''''''''"""

#
# your imgur api info goes here
#

client_id = 'aece57a63fe95f9'
client_secret = '3add50559f0b5339744dcfff7ed65667f67bb5a4'
api = "https://api.imgur.com/3/upload.json"


#
# set the directory and filename of screenshots you take
#

image_dir = '/home/kyle/images/ss/'
image_name = 'imgur_ss_' + str(int(time.time())) + '.png'
image_path = image_dir + image_name
date_time = time.strftime("%m/%d/%y %I:%M%P", time.localtime())
image_title = "Screenshot from " + date_time


#
# use whatever program you want to actually grab the screenshot
#

ss_prog = ['import', '-window', 'root', image_path]


#
# do you want to open the image in a browser after its uploaded?
#

open_in_browser = True
browser_command = 'firefox %s'


#
# do you want to log the image title and url to a file for later reference?
#

log_to_file = True
log_file = image_dir + 'imgur.upload.log'


"""''''''''''''''''''''''''''''''''''

    try to save the screenshot

''''''''''''''''''''''''''''''''''"""

try:
    retcode = call(ss_prog)
except FileNotFoundError as e:
    print('Can\'t find the screenshot program', file=sys.stderr)
    print(e, file=sys.stderr)
    sys.exit()


# if we don't get a successful return code, bye
if retcode != 0:
    print('The screenshot program returned an error', file=sys.stderr)
    sys.exit()


# we've made it this far, lets serialize that image
try:
    with open(image_path, 'rb') as f:
        image_encoded = b64encode(f.read())
except IOError as e:
    print('Can\'t read the image file', file=sys.stderr)
    print('Check image_path or ss_prog', file=sys.stderr)
    print(e, file=sys.stderr)


"""''''''''''''''''''''''''''''''''''

    try to post to imgur

''''''''''''''''''''''''''''''''''"""


header = {'Authorization': 'Client-ID ' + client_id}

post_data = {
    'key':      client_secret,
    'image':    image_encoded,
    'type':     'base64',
    'name':     image_name,
    'title':    image_title
}

response = requests.post(api, headers=header, data=post_data)
imgur_data = response.json()

# if we don't get a succesful response, exit
if response.status_code != 200 or not imgur_data['success']:
    print('Upload to imgur failed', file=sys.stderr)
    sys.exit()


"""''''''''''''''''''''''''''''''''''

    handle the image link

''''''''''''''''''''''''''''''''''"""


the_link = imgur_data['data']['link']


#
# just print it.
#

print(the_link)


#
# open in browser?
#

if open_in_browser is True:
    browser_command = browser_command.replace('%s', the_link)
    browser_prog = browser_command.split(' ')

    try:
        retcode = call(browser_prog)
    except FileNotFoundError as e:
        print('Can\'t find the browser program', file=sys.stderr)
        print('Check browser_command', file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit()

    # if we don't get a successful return code, bye
    if retcode != 0:
        print('Opening the browser returned an error', file=sys.stderr)
        print('Check browser_command, use %s for imgur url', file=sys.stderr)
        sys.exit()


#
# log to file?
#

if log_to_file is True:

    try:
        with open(log_file, 'a') as f:
            f.write('{}\t{}\n'.format(image_title, the_link))

    except IOError as e:
        print('Can\'t write to the log file', file=sys.stderr)
        print('Check path or permissions', file=sys.stderr)
        print(e, file=sys.stderr)
