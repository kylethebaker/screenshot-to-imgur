# screenshot-to-imgur

The idea is to be able to take a screenshot and have it directly uploaded to imgur.
It is intended to be bound to a hotkey for easy screenshotting, though it runs just as
well directly from the shell. The actual taking of the screenshot is handled externally
by a command line program of your choosing, which you can specify in **ss_prog**. By
default it will try to use _import_, which is a command lind tool provided by ImageMagick. 
Uploading via the imgur api is accomplished using the requests module.

## Setting It Up

Before you can get started you need to change a few variables to match your system.

### imgur API keys

First you will need to [register to use the imgur api](https://api.imgur.com/oauth2/addclient).
Its a really simple process and this will provide you with your **client_id** and **client_secret**

### image settings

Next, you'll want to change **image_dir** to the directory you want to save the screenshots in
(note the trailing slash). You can also change the **image_name** and **image_title**. Its a 
good idea to use some sort of timestamp or other unique name for the image_name to prevent
your screenshot program from overwriting previously saved images.

### screenshot program

Now you need to define which command line program you want to use to actually take the
screenshot. This goes in **ss_prog** and eventually gets used in
[subprocess.call](https://docs.python.org/3/library/subprocess.html#subprocess.call), so
keep that in mind and use the appropriate syntax. 

### opening uploaded images in a browser

If you'd like to open the imgur link of the newly uploaded image in a browser immediately
after the upload finishes, you can set **open_in_browser** to _True_. **browser_command** is the
command to be executed when the images finished uploading, with %s being a placeholder for
the imgur link. You don't have to use a browser neccesarily, you can pass the link to any
arbitrary command line application by defining it in browser_command.

### logging imgur links to a file

If you'd like to keep a log of all the uploaded image titles and urls, you can set
**log_to_file** to _True_. You will need to set the path for the log file in **log_file**. The
log format is _image_title \<tab\> imgur_url_.

## Disclaimer

It works for me, but it might not work for you. You need to make sure your settings are 
correct. If something catches on fire or gets irrevocably ruined, you have my condolances.
