from zipfile import ZipFile
import argparse, time, os

def main():
    parser = argparse.ArgumentParser(description='png2Animation Utility for FlipperZero Animations')
    parser.add_argument('-z', '--zip', help='specify zip file', type=str, required=True)
    parser.add_argument('-o', '--output', help='specify output file', type=str, default='frames')
    parser.add_argument('-w', '--width', help='specify width of animation', type=int, default=128)
    parser.add_argument('-ht', '--height', help='specify height of animation', type=int, default=64)

    args = parser.parse_args()
    file = args.zip
    output = args.output
    width = args.width
    height = args.height
    
    print('[*] Extracting folders from zip file..\n')
    time.sleep(1)
    listOfiles = extract(file, output)
    print('[*] Changing file names\n')
    index = renamer(output, listOfiles)
    print('[#] Creating basic meta file..\n')
    metaCreate(index, output, width, height)
    print('[$] Done')

def extract(file, output):
    zip = ZipFile(file)
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

    metaText = f"Filetype: Flipper Animation\nVersion: 1\nWidth: {width}\nHeight: {height}\nPassive frames: {index - 1}\nActive frames: 1\nFrames order: {' '.join(str(num) for num in order)}\nActive cycles: 1\nFrame rate: 5\nDuration: 3600\nActive cooldown: 7\n\nBubble slots: 0"

    with open(f'{output}/meta.txt', 'w') as f:
        f.write(f'{metaText}')

main()
