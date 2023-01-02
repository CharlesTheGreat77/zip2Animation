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
        print("[*] Iterating through all zips.. \n")
        listOfZips = unzipAll(directory)
        print("[*] Iterating through files & Renaming frames.. \n")
        for file in listOfZips:
            output = file.replace('.zip', '')
            listOfiles = extract(file, output)
            index = renamer(output, listOfiles)
            metaCreate(index, output, width, height)
    else:
        print("[*] Extracting File Names.. \n")
        listOfiles = extract(file, output)
        print("[*] Renaming Each Frame.. \n")
        index = renamer(output, listOfiles)
        metaCreate(index, output, width, height)
    
    print("[*] All Done with meta file(s) created.. and noice animation ;)")
        
        
def unzipAll(directory):
    listOfZips = []
    fileNames = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            listOfZips.append(os.path.join(root, filename))
            
    return listOfZips

def extract(file, output):
    try:
        zip = ZipFile(file)
    except Exception as e:
        print(e)
    with ZipFile(file, 'r') as zipObj:
        listOfiles = zipObj.namelist()
    zip.extractall(output)
    return listOfiles


def renamer(output, listOfiles):
    index = 0
    for fileName in listOfiles:
            source = output + '/' + fileName
            destination = output + '/' + f'frame_{index}.png'
            os.rename(source, destination)
            index += 1
    return index

def metaCreate(index, output, width, height):
    order = []
    for num in range(0, index):
        order.append(num)
        
    metaText = f"Filetype: Flipper Animation\nVersion: 1\nWidth: {width}\nHeight: {height}\nPassive frames: {index}\nActive frames: 0\nFrames order: {' '.join(str(num) for num in order)}\nActive cycles: 0\nFrame rate: 5\nDuration: 3600\nActive cooldown: 0\n\nBubble slots: 0"

    with open(f'{output}/meta.txt', 'w') as f:
        f.write(f'{metaText}')

main()
