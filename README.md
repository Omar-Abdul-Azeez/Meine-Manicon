## This repo is not being used anymore. It is merely left as an archive. However, I decided to change to AniList instead of MAL and currently have a working script (for anime only and still needs some modifications to deal with similar names except for special chracters that are not allowed in Windows file names as in the case of the second season of Love is War)

# Meine Manicon
Add cover art from MAL as folder icons to your Anime collection. This is a fork of [dedsec](https://github.com/notdedsec)'s [anicon](https://github.com/notdedsec/anicon).

### Why use this fork?
Well... don't. This fork depends on your library being organized in a special way. both this project and the way i organize my library are still being heavily edited, so i don't recommend using this until atleast the way i organize my files is finished. however this code is public because i have a couple of features that the original doesn't.

-Support of Manga as well as Anime
-Downloads all media related to the Anime/Manga on MAL for easier access in the future as well as saves the ID of the Anime/Manga on MAL
-Blank input has been removed. You'll have to input 1 if you want the first search result, this is because it shows more than 5 results so you can input 1 even if the results showing are 11-15. However it searches 5 pages as well so if the numbers reset to count from 1 again this means you can't choose any results of the previous page (can change if needed)

#### AutoMode

If enabled, in addition to the normal behaviour of selecting the first Anime/Manga in the search results, it will also download the first media (if not already downloaded) and use that

### How do I use this?

There is no releases of this fork yet so you'll have to have Python installed on your system.

- Download anicon.py
- Run it in your Anime/Manga folder
- Choose when you're asked to
- Repeat till all folders are processed

### Okay so i did everything, but the icons aren't showing up. (*panicks*)
Your PC may take some time to index those icons. They should show up in 2 to 5 minutes. I guess.

### Alright. It works but I'm curious as to how?
It, uhhh
- Gets the Anime Name from the Folder Name
- Searches that name on MAL with Jikan API
- Asks you to choose the anime from results
- Gets the artwork and converts it into an icon
- Makes a `desktop.ini` file which sets the folder icon.

### I don't like these icons. How do i remove them?
If the file's icon is a different Anime/Manga then make sure to delete 'ID.txt' and the 'Artwork' folder as well as the '.ico' and 'desktop.ini' files. These files are hidden so make sure you have `Show Hidden Items` option ticked. You can just search and delete them all if you wanna batch remove all icons. But why would you wanna do that anyway?

### Any Tips or Suggestions?
Yeah, the most efficient way to use this (imo) would be to:
- Run it in AutoMode first so all folders are processed
- Move out the incorrectly tagged folders and delete their icons (and 'ID.txt' and 'Artwork' folder if needed)
- Run it in ManualMode and choose the correct results

### I was promised memes. Gib memes.
Alright here you go.

![meme](https://i.imgur.com/BXX93Rs.jpg)
