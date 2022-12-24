from zipfile import ZipFile
import argparse, time, os

def main():
    parser = argparse.ArgumentParser(description='Change png file names to match flippers frame file naming convention', usage='python3 zip2Animations.py [options]')
    parser.add_argument('-z', '--zip', help='specify zip file', type=str, required=False)
    parser.add_argument('-d', '--directory', help='specify the directory for multiple zips files', required=False)
    parser.add_argument('-o', '--output', help='specify output file', type=str, default='frames')
    parser.add_argument('-w', '--width', help='specify width of animation', type=int, default=128)
    parser.add_argument('-ht', '--height', help='specify height of animation', type=int, default=64)

    args = parser.parse_args()
    file = args.zip
    directory = args.directory
    output = args.output
    width = args.width
    height = args.height

    if file == None and directory == None:
        print(parser.usage)
    
    if directory != None:
        listOfZips, fileNames = unzipAll(directory)
        for file in listOfZips:
            output = file.replace('.zip', '')
            listOfiles = extract(file, output)
            index = renamer(output, listOfiles)
            metaCreate(index, output, width, height)
    else:
        listOfiles = extract(file, output)
        index = renamer(output, listOfiles)
        metaCreate(index, output, width, height)
        
        
def unzipAll(directory):
    print("[*] Iterating through all zips.. \n")
    listOfZips = []
    fileNames = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            listOfZips.append(os.path.join(root, filename))
            fileNames.append(os.path.join(filename))
    return listOfZips, fileNames

def extract(file, output):
    print("[*] Extracting File Names.. \n")
    try:
        zip = ZipFile(file)
    except Exception as e:
        print(e)
    with ZipFile(file, 'r') as zipObj:
        listOfiles = zipObj.namelist()
    zip.extractall(output)
    return listOfiles


def renamer(output, listOfiles):
    print("[*] Renaming Each Frame.. \n")
    index = 0
    for fileName in listOfiles:
            source = output + '/' + fileName
            destination = output + '/' + f'frame_{index}.png'
            os.rename(source, destination)
            index += 1
    return index

def metaCreate(index, output, width, height):
    print("[*] Creating a basic meta file.. \n")
    order = []
    for num in range(0, index):
        order.append(num)

    metaText = f"Filetype: Flipper Animation\nVersion: 1\nWidth: {width}\nHeight: {height}\nPassive frames: {index - 1}\nActive frames: 1\nFrames order: {' '.join(str(num) for num in order)}\nActive cycles: 1\nFrame rate: 5\nDuration: 3600\nActive cooldown: 7\n\nBubble slots: 0"

    with open(f'{output}/meta.txt', 'w') as f:
        f.write(f'{metaText}')

main()
