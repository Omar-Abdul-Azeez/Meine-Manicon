import os
from time import sleep

import cfscrape
import regex
import requests
from PIL import Image, ImageOps


def ask(msg, choices, limit=0):
    print(msg)
    for i in range(len(choices)):
        if limit != 0 and i != 0 and i % limit:
            ans = input('>')
            if ans != '':
                ans = int(ans) - 1
                if -1 < ans < i:
                    return ans
            print(msg)
        print(f'{i + 1})  {choices[i]}')

    ans = input('>')
    if ans == '':
        return None
    ans = int(ans) - 1
    if -1 < ans < len(choices):
        return ans
    else:
        return None

def createicon(folder: str, title: str, pic: str):
    img = Image.open(pic)
    w, h = img.size
    size = max(256, w, h)
    ico = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    ico.paste(img, (int((size - w) / 2), int((size - h) / 2)))
    img.close()
    ico.save(folder + "\\" + title + ".ico")
    ico.close()
    return folder + "\\" + title + ".ico"


def process(folder: str):
    if os.path.exists(folder + "\\desktop.ini"):
        print(folder + " Already done")
        return False
    query = """
    query ($page: Int) {
      Page (page: $page) {
        pageInfo {
          hasNextPage
        }
        media (search: """ + f'"{folder}"' + """, type: ANIME) {
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
    }
    """
    variables = {}
    url = 'https://graphql.anilist.co'
    if choice:
        page = 1
        variables['page'] = page
        response = requests.post(url, json={'query': query, 'variables': variables}).json()["data"]
        hasNextPage = response["Page"]["pageInfo"]["hasNextPage"]
        medias = response["Page"]["media"]
        mediass = []
        ans = ask(folder + ' :', [media['title']['romaji'] for media in medias], limit=10)
        while ans is None:
            mediass.extend(medias)
            if hasNextPage:
                page += 1
                variables['page'] = page
                response = requests.post(url, json={'query': query, 'variables': variables}).json()["data"]
                hasNextPage = response["Page"]["pageInfo"]["hasNextPage"]
                medias = response["Page"]["media"]
                ans = ask(folder + ' :', [media['title']['romaji'] for media in medias], limit=10)
            else:
                medias = []
                ans = ask(folder + ' :', [media['title']['romaji'] for media in mediass], limit=10)
        if ans >= len(medias):
            media = mediass[ans]
        else:
            media = mediass[ans]
    else:
        response = requests.post(url, json={'query': query, 'variables': variables}).json()["data"]
        media = response["page"]["media"][0]
    id = media["id"]
    banner = media["bannerImage"]
    cover = media["coverImage"]["extraLarge"]
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
    try:
        icon = createicon(folder, folder, folder + "\\Cover\\" + str(id) + "c.png")
    except:
        print(folder + " ran into an error. Blame the Dev :(")
        return

    f = open(folder + "\\desktop.ini", "w+", encoding="ANSI")
    f.write("[.ShellClassInfo]\nConfirmFileOp=0\n")
    f.write(f"IconResource={folder}.ico,0")
    f.write(f"\nIconFile={folder}.ico\nIconIndex=0")
    f.close()
    os.system('attrib +r \"{}\\{}\"'.format(os.getcwd(),folder))
    os.system('attrib +h \"{}\\desktop.ini\"'.format(folder))
    os.system('attrib +h \"{}\"'.format(icon))
    return True


folders = next(os.walk('.'))[1]
choice = bool(input('Press enter for auto mode, enter anything for manual.\n'))
count = 0
for folder in folders:
    if count == 89:
        sleep(60)
    if process(folder):
        count += 1
