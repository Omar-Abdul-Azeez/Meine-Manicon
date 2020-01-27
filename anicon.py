import os
import re
from warnings import filterwarnings

from PIL import Image, ImageOps
from jikanpy import Jikan
from requests import get

print('''Run this in your anime folder
For help, info and memes, check out
https://github.com/notdedsec/anicon
''')

jikan = Jikan()
filterwarnings("ignore")
folders = next(os.walk('.'))[1]
type = os.getcwd().rpartition('\\')[2].lower()
automode = True if input('Use AutoMode? Y/N : ').upper() == 'Y' else False


def getname(name: str) -> str:
    lastwords = ['BD', '480p', '720p', '1080p']
    if "Season" in name:
        name = name.partition(" - ")[2]
    else:
        for word in lastwords:
            rexstr = word + "(?s)(.*$)"
            name = re.sub(rexstr, '', name)

    return name.strip()


def getartwork(folder: str, name: str, type: str) -> tuple:
    # print the current title
    print('\n' + name.title(), end='')
    # check if MAL ID is already found
    if os.path.isfile(folder + "\\ID.txt"):
        id = int(open(folder + "\\ID.txt", "r").read())
    else:  # search 5 pages tops for the anime/manga
        page = 1
        results = jikan.search(type, name, page)

        for page in range(min((results["last_page"], 5))):
            if page != 1:
                results = jikan.search(type, name, page)
            counter = 1
            for result in results['results']:
                if automode:
                    print(' - ' + result['title'])
                    ch = "1"
                    break
                else:
                    print('\n' + str(counter) + ' - ' + result['title'], end='')
                    ch = "m"
                if counter % 5 == 0:
                    print("\nm - more", end="")
                    ch = input("\n>")
                counter += 1
            else:
                if ch != "m":
                    break
        else:
            print("\nNo more", end="")
            ch = input('\n>')
        id = results['results'][int(ch) - 1]['mal_id']
        open(folder + "\\ID.txt", "w").write(str(id))

    folder = folder + "\\Artwork"

    # pull pictures related to anime/manga
    def getresults(ext: str = None):
        if type == "anime":
            return jikan.anime(id, extension=ext)
        elif type == "manga":
            return jikan.manga(id, extension=ext)

    results = getresults("pictures")
    # if autoMode just grab first picture and save in Artwork folder for later use (or use existing one)
    if automode:
        if not os.path.isfile(folder + "\\1.jpg"):
            open(folder + "\\1.jpg", "wb").write(get(results["pictures"][0]["large"]).content)
    else:  # grab existing pictures and list them for use
        counter = 1
        fileslist = next(os.walk(folder))[2]
        if fileslist is not None:
            for _ in range(len(fileslist)):
                jpgfile = folder + "\\" + str(counter) + ".jpg"
                print("\n - " + str(counter) + ".jpg", end="")
                Image.open(jpgfile).show()
                if counter % 5 == 0:
                    print("\nm - more", end="")
                    ch = input("\n>")
                    if ch != "m":
                        return folder + "\\" + ch + ".jpg", results["type"]
                counter += 1
        # if not yet chosen list the rest of the pictures online and save them for later use
        for pic in results["pictures"][counter - 1:len(results["pictures"])]:
            jpgfile = folder + "\\" + str(counter) + ".jpg"
            open(jpgfile, "wb").write(get(pic["large"]).content)
            print("\n - " + str(counter) + ".jpg", end="")
            Image.open(jpgfile).show()
            if counter % 5 == 0:
                print("\nm - more", end="")
                ch = input("\n>")
                if ch != "m":
                    break
            counter += 1
        else:
            print("\nNo more", end="")
            ch = input("\n>")
    return folder + "\\" + ch + ".jpg", getresults()["type"]


def createicon(jpgfile: str, iconfile: str):
    img = Image.open(jpgfile)
    img = ImageOps.expand(img, (69, 0, 69, 0), fill=0)
    img = ImageOps.fit(img, (300, 300)).convert("RGBA")

    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            newData.append((0, 0, 0, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(iconfile)
    img.close()


def process(folder: str, name: str, type: str):
    iconfile = folder + '\\' + name.replace(' ', '_') + '.ico'

    if os.path.isfile(iconfile):
        print('An icon is already present. Delete the older icon before applying a new one')
        return

    jpgfile, type = getartwork(folder, name, type)

    try:
        icon = createicon(jpgfile, iconfile)
    except:
        print('Ran into an error. Blame the dev :(')
        return

    f = open(folder + "\\desktop.ini", "w+")

    f.write("[.ShellClassInfo]\nConfirmFileOp=0\n")
    f.write("IconResource={},0".format(iconfile.replace(folder, "").strip("\\")))
    f.write("\nIconFile={}\nIconIndex=0".format(iconfile.replace(folder, "").strip("\\")))

    if type is not None and len(type) > 0:
        # If the result has a type, then using this as the infotip for the desktop icon.
        f.write("\nInfoTip={}".format(type))

    # Closing the output stream. All the text will be written into `desktop.ini` file only when the output is being
    # closed.
    f.close()

    # Not marking the `desktop.ini` file as a system file. This will make sure that the file can be seen if display
    # hidden items is enabled.
    os.system('attrib +r \"{}\\{}\"'.format(os.getcwd(), folder))
    os.system('attrib +h \"{}\\desktop.ini\"'.format(folder))
    os.system('attrib +h \"{}\"'.format(icon))


for folder in folders:
    process(folder, getname(folder), type)
    if type == "anime":
        for minifolder in next(os.walk(folder + "\\Anime"))[1]:
            process(folder + "\\Anime\\" + minifolder, getname(minifolder), "anime")
