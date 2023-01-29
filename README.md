# zip2Animation
Utility to assist in creating flipper zero animations.

# Description
 - renames the png files in order from a zip file. 
 - Creates a basic meta file with a straight forward animation frame order
 - added "width/height" argument to declare it in meta file

# PREREQUISITES
```
Python3
Zip file with your png frames
```

# USAGE
```
options:
  -h, --help           show this help
                       message and exit
  -z ZIP, --zip ZIP    specify zip file
  -d DIRECTORY, --directory DIRECTORY
                       specify the directory 
                       for multiple zip files
  -o OUTPUT, --output OUTPUT
                       specify output file
  -w WIDTH, --width WIDTH
                       specify width of
                       animation
  -ht HEIGHT, --height HEIGHT
                       specify height of
                       animation
```

# Default Example (128x64)
```
python3 zip2Animation.py -z Mario.zip -o Mario
```
* This will rename the frames as frames_0.. etc. and create a basic meta.txt file
  that will play the animation (as normal).

• Key note
 - the width default is 128, and the height default is 64. 
 - Specify the width and height of your animation otherwise. 
# Multiple Zip files
```
python3 zip2Animation.py -d Animations/
```
 - Unzips all files, renames all frames in each file, creates basic meta file for each folder. 
 - Folders are named the same as each zip file name. 

• Key Note
 - Be sure every file in the directory is a ZIP file.. I'm lazy..
# Custom Width Height Example
```
python3 zip2Animation.py -z Mario.zip -o Mario -w 97 -ht 61
```
* This will automatically change the width and height in the meta file. 

# Honorable mentions
Talking Sasquach
https://github.com/skizzophrenic/Talking-Sasquach
 - thank him for the addition of allowing multiple zip files to be processed

# Extra
BADUSB Repo https://github.com/CharlesTheGreat77/BADUSB

# Token Grabber for BADUSB
https://github.com/CharlesTheGreat77/token2Discord

### 💬 Contact Me 

![Gmail Badge](https://img.shields.io/badge/-doobthegoober@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white)

### 🚦 Stats

<a href="https://github.com/CharlesTheGreat77">
  <img src="https://github-readme-stats.vercel.app/api?username=CharlesTheGreat77&show_icons=true&hide=commits" />
</a>
<a href="https://github.com/CharlesTheGreat77">
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=CharlesTheGreat77&layout=compact" />
</a>

<p align="center"> 
  <img src="https://profile-counter.glitch.me/CharlesTheGreat77/count.svg" />
</p>

---
⭐️ From [Charles](https://github.com/CharlesTheGreat77)

