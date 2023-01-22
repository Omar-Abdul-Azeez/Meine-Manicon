import os
from time import sleep

import cfscrape
import regex
import requests
from PIL import Image, ImageOps


def createicon(folder: str, name: str, pic: str):
    img = Image.open(pic)
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
    img.save(folder + "\\" + name + ".ico")
    img.close()
    return folder + "\\" + name + ".ico"


def process(folder: str):
    name = regex.sub(r" \[anidb-\d+]", "", folder)
    query = """
    query ($name: String) {
      Media (search: $name, type: ANIME) {
        id
        title {
          romaji
        }
        bannerImage
        coverImage {
          extraLarge
        }
      }
    }
    """
    variables = {
        "name": name
        }
    url = 'https://graphql.anilist.co'
    response = requests.post(url, json={'query': query, 'variables': variables}).json()["data"]["Media"]
    id = response["id"]
    banner = response["bannerImage"]
    cover = response["coverImage"]["extraLarge"]
    if not os.path.exists(folder + "\\Cover"):
        os.mkdir(folder + "\\Cover")
    scraper = cfscrape.create_scraper()
    if not os.path.exists(folder + "\\Cover\\" + str(id) + "b.png"):
        if banner:
            bannerimg = scraper.get(banner)
            with open(folder + "\\Cover\\" + str(id) + "b.png", 'wb') as f:
                bannerimg.decode_content = True
                f.write(bannerimg.content)
    if not os.path.exists(folder + "\\Cover\\" + str(id) + "c.png"):
        coverimg = scraper.get(cover)
        with open(folder + "\\Cover\\" + str(id) + "c.png", 'wb') as f:
            coverimg.decode_content = True
            f.write(coverimg.content)
    if os.path.exists(folder + "\\" + name + ".ico") or os.path.exists(folder + "\\desktop.ini"):
        print(name + " Already done")
        return
    try:
        icon = createicon(folder, name, folder + "\\Cover\\" + str(id) + "c.png")
    except:
        print("Ran into an error. Blame the Dev :(")
        return

    f = open(folder + "\\desktop.ini", "w+", encoding="ANSI")
    f.write("[.ShellClassInfo]\nConfirmFileOp=0\n")
    f.write(f"IconResource={name}.ico,0")
    f.write(f"\nIconFile={name}.ico\nIconIndex=0")
    f.close()
    os.system('attrib +r \"{}\\{}\"'.format(os.getcwd(),folder))
    os.system('attrib +h \"{}\\desktop.ini\"'.format(folder))
    os.system('attrib +h \"{}\"'.format(icon))


folders = next(os.walk('.'))[1]
count = 0
for folder in folders:
    if (count == 89):
        sleep(60)
    process(folder)
    count += 1
