from zipfile import ZipFile
import argparse, os, shutil, subprocess

def main(file: str, directory: str, width: int, height: int, fbt_path: str) -> None:
    # multiple animations
    if directory is not None:
        print("[*] Iterating through zips.. \n")
        list_of_files = list_all_zips(directory)
        for file_path in list_of_files:
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            output_folder_name = f"{base_name}_{width}x{height}"
            output_path = os.path.join(directory, output_folder_name)
            list_of_files = extract_frame_filenames(file_path, output_path)
            index = renamer_frames(output_path, list_of_files)
            meta_create(index, output_path, width, height)
            if fbt_path:
                move_to_external(fbt_path, output_path, output_folder_name)
                update_manifest(fbt_path, output_folder_name)
    else:
    # single animation
        output = file.replace(".zip", "")
        output_folder_name = os.path.splitext(os.path.basename(output))[0] + f"_{width}x{height}"
        output_path = os.path.join(os.path.dirname(output), output_folder_name)
        print("[*] Extracting file names.. \n")
        list_of_files = extract_frame_filenames(file, output_path)
        print("[*] Renaming Each Frame.. \n")
        index = renamer_frames(output_path, list_of_files)
        print("[*] Creating meta file for the frames..\n")
        meta_create(index, output_path, width, height)
        if fbt_path:
            move_to_external(fbt_path, output_path, output_folder_name)
            update_manifest(fbt_path, output_folder_name)

def list_all_zips(directory: list) -> list:
    # return list of zip files in the specified directory
    list_of_zips = []
    for root, _, files in os.walk(directory):
        for filename in files:
            list_of_zips.append(os.path.join(root, filename))
                              
    return list_of_zips

def extract_frame_filenames(file: str, output: str) -> list:
    # unzip files, extract file names
    # return list of file names
    try:
        zip = ZipFile(file)
    except Exception as e:
        # make sure the files in the directory are all zips... I don't wanna have to do any error handling..
        print(e)
    with ZipFile(file, "r") as zip_file:
        list_of_files = zip_file.namelist()
    zip.extractall(output)

    return list_of_files

def renamer_frames(output: str, list_of_files: list) -> int:
    # rename frames in a folder in ascending order "frame_0, frame_1... etc.
    # return number of frames (index)
    index = 0
    for file_name in list_of_files:
        source = os.path.join(output, file_name)
        destination = os.path.join(output, f"frame_{index}.png")
        try:
            os.rename(source, destination)
        except FileExistsError:
            pass
        index += 1

    return index

def meta_create(index: int, output: str, width: int, height: int) -> None:
    # create a basic meta file for each animation folder
    order = list(range(0, index))
    meta_text = f"Filetype: Flipper Animation\nVersion: 1\nWidth: {width}\nHeight: {height}\nPassive frames: {index}\nActive frames: 0\nFrames order: {' '.join(str(num) for num in order)}\nActive cycles: 0\nFrame rate: 5\nDuration: 3600\nActive cooldown: 0\n\nBubble slots: 0"
    with open(os.path.join(output, "meta.txt"), "w") as f:
        f.write(meta_text)

def move_to_external(fbt_path: str, output_path: str, output_folder_name: str) -> None:
    # move folders to path_to_fbt/assets/dolphin/external
    destination_dir = os.path.join(fbt_path, "assets", "dolphin", "external")
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    try:
        shutil.move(output_path, os.path.join(destination_dir, output_folder_name))
    except shutil.Error as e:
        if "Destination path" in str(e) and "already exists" in str(e):
            pass

def update_manifest(fbt_path: str, output_folder_name: str) -> None:
    # update manifest in \assets\dolphin\external\ to add
    meta_text = f"""
Name: {output_folder_name}
Min butthurt: 0
Max butthurt: 10
Min level: 3
Max level: 3
Weight: 4
"""
    manifest_path = os.path.join(fbt_path, "assets", "dolphin", "external", "manifest.txt")
    with open(manifest_path, "r+") as meta_file:
        lines = meta_file.readlines()
        # prevent duplicates in the manifest.. more or less if you accidentally compiled the same animation..
        exists = any(output_folder_name in line for line in lines)
        if not exists:
            meta_file.write("\n" + meta_text)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Change png file names to match flippers frame file naming convention", usage="python3 zip2Animations.py -h, --help")
    parser.add_argument("-z", "--zip", help="specify zip file", type=str, required=False)
    parser.add_argument("-d", "--directory", help="specify the directory for multiple zips files", required=False)
    parser.add_argument("-w", "--width", help="specify width of animation", type=int, default=128)
    parser.add_argument("-ht", "--height", help="specify height of animation", type=int, default=64)
    parser.add_argument("-fbt", "--fbt", help="specify flipper zero directory to auto. compile", type=str, required=False)

    args = parser.parse_args()
    file = args.zip
    directory = args.directory
    width = args.width
    height = args.height
    fbt_path = args.fbt

    if file == None and directory == None:
        print(parser.usage)
        exit(0)

    else:
        main(file, directory, width, height, fbt_path)
        if fbt_path:
            # compile the animation(s) with fbt (must have such downloaded)
            print("[*] Compiling with fbt..\n")
            subprocess.run(['powershell', f'cd "{fbt_path}"; .\\fbt dolphin_ext'], shell=True)
            
    print("[*] All Done.. noice animation ;)\n -> Time to let the world see it!!")
