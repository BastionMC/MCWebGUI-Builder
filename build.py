# If you are confused about this code, please contact me on Discord (@jaegerwald)

from xmltodict import parse as parse_xml
from PIL import Image as image
from colorama import *
import os, time

just_fix_windows_console() # :>

xml_files = []
output = "[               MCWEBGUI BUILDER LOG FILE               ]\n"

def intify_list(string_list):
    integer_list = []
    for item in string_list:
        integer_list.append(int(item))
    return integer_list

def convert2xy(position_list):
    return (position_list[0], position_list[1])

def write_output(write):
    global output
    output += write + "\n"

    with open("build.log.txt", "w") as log_file:
        log_file.write(output)
        log_file.close()
def create_dist():
    print(Back.YELLOW + Fore.BLACK + " WRN " + Style.RESET_ALL + " Please create a " + Fore.BLACK + Style.BRIGHT + "dist " + Style.RESET_ALL + "folder before running this program.")
    write_output("[WRN] Please create a \"dist\" folder before running this program.")
def dist_filled():
    print(Back.YELLOW + Fore.BLACK + " WRN " + Style.RESET_ALL + " The " + Fore.BLACK + Style.BRIGHT + "dist " + Style.RESET_ALL + "folder has some files in it. Please clear it first.")
    write_output("[WRN] The \"dist\" folder has some files in it. Please clear it first.")
def no_source():
    print(Back.RED + Fore.BLACK + " ERR " + Style.RESET_ALL + " The " + Fore.BLACK + Style.BRIGHT + "source " + Style.RESET_ALL + "folder doesn't seem to exist. Cannot continue.")
    write_output("[ERR] The \"source\" folder doesn't seem to exist. Cannot continue.")
def no_files(format):
    print(Back.RED + Fore.BLACK + " ERR " + Style.RESET_ALL + " No " + Fore.BLACK + Style.BRIGHT + "." + format + Style.RESET_ALL + " files were found in the " + Fore.BLACK + Style.BRIGHT + "source" + Style.RESET_ALL + " folder!")
    write_output("[ERR] No \"." + format + "\" files were found in the \"source\" folder!")
def got_file(file):
    print(Back.GREEN + Fore.BLACK + " GOT " + Style.RESET_ALL + " Found the file " + Fore.BLACK + Style.BRIGHT + file + Style.RESET_ALL + ".")
    write_output("[GOT] Found the file \"" + file + "\".")
def require_file(file):
    print(Back.MAGENTA + Fore.BLACK + " REQ " + Style.RESET_ALL + " Requested the file " + Fore.BLACK + Style.BRIGHT + file + Style.RESET_ALL + ".")
    write_output("[REQ] Requested the file \"" + file + "\".")
def pillow_action(string):
    print(Back.CYAN + Fore.BLACK + " PIL " + Style.RESET_ALL + " " + string)
    write_output("[PIL] " + string)
def end():
    print(Back.WHITE + Fore.BLACK + " END " + Style.RESET_ALL + " All files have been processed.")
    write_output("[END] All files have been processed.")
def invalid_xml():
    print(Back.RED + Fore.BLACK + " ERR " + Style.RESET_ALL + " This XML file is invalid, it cannot be processed.")
    write_output("[ERR] This XML file is invalid, it cannot be processed.")
def no_part_list(part):
    print(Back.YELLOW + Fore.BLACK + " NIL " + Style.RESET_ALL + " No " + part + " parts were found.")
    write_output("[NIL] No " + part + " parts were found.")
def removed_empty_folders():
    print(Back.WHITE + Fore.BLACK + " CLR " + Style.RESET_ALL + " Removed empty folders.")
    write_output("[CLR] Removed empty folders.")
def missing_information():
    print(Back.RED + Fore.BLACK + " ERR " + Style.RESET_ALL + " There seems to be some information missing. Cannot continue.")
    write_output("[ERR] There seems to be some information missing. Cannot continue.")

def rearrange_part(part, tree, original_image, suffix):
    try:
        size = tree[part]["size"].split(",")
        size = convert2xy(intify_list(size))

        new_image = image.new(
            "RGBA",
            size,
            (255, 255, 255, 0)
        )
        pillow_action("Created new empty image.")

        instructions = tree[part]["move"].split("|")

        for instruction in instructions:
            parts = instruction.split(":")

            new_position = parts[1].split(",")
            new_position = convert2xy(intify_list(new_position))

            old_part = parts[0].split(";")
            old_position = old_part[0].split(",")
            old_position = intify_list(old_position)

            old_size = old_part[1].split(",")
            old_size = intify_list(old_size)

            crop_area = (
                old_position[0],
                old_position[1],
                old_position[0] + old_size[0],
                old_position[1] + old_size[1]
            )

            new_part = original_image.crop(crop_area)

            new_image.paste(new_part, new_position)
        pillow_action("Rearranged parts of the original image.")

        new_image.save("dist/" + tree["result-file"] + suffix + ".png", format="PNG")
        pillow_action("Saved newly created image.")
    except: no_part_list(part)

def rearrange(tree):
    require_file(tree["file"])
    original = image.open("source/" + tree["file"])
    pillow_action("Opened file to rearrange.")

    rearrange_part("non-repeating", tree, original, "")
    rearrange_part("vertically-repeating", tree, original, "_vertical")
    rearrange_part("horizontally-repeating", tree, original, "_horizontal")

def split_spritesheet(spritesheet, tree):
    size = tree["size"].split(",")
    size = intify_list(size)

    sprites = []

    for y in range(0, spritesheet.height, int(size[1])):
        for x in range(0, spritesheet.width, size[0]):
            crop_area = (
                x,
                y,
                x + size[0],
                y + size[1]
            )

            sprite = spritesheet.crop(crop_area)
            sprite = sprite.convert("RGBA")
            sprites.append(sprite)

    return sprites

def make_apng(tree):
    require_file(tree["file"])
    spritesheet = image.open("source/" + tree["file"])
    pillow_action("Opened file to make APNG.")

    try:
        frames = split_spritesheet(spritesheet, tree)
        pillow_action("Split all APNG frames.")

        frame_time = int(tree["frame-time"])

        if tree["loop"] == "none":
            frames[0].save("dist/" + tree["result-file"] + ".png", format="PNG", save_all=True, append_images=frames[1:], duration=frame_time, loop=1)
        else:
            frames[0].save("dist/" + tree["result-file"] + ".png", format="PNG", save_all=True, append_images=frames[1:], duration=frame_time, loop=int(tree["loop"]))
        pillow_action("Saved APNG image.")
    except: missing_information()

def split(tree):
    require_file(tree["file"])
    spritesheet = image.open("source/" + tree["file"])
    pillow_action("Opened file for image splitting.")

    try:
        files = tree["files"].split(",")

        images = split_spritesheet(spritesheet, tree)
        pillow_action("Split all images.")

        for i in range(0, len(images)):
            try:
                images[i].save("dist/" + files[i] + ".png", format="PNG")
            except: continue

        pillow_action("Saved splitted images.")
            
    except: missing_information()

def rescale(tree):
    require_file(tree["file"])
    original = image.open("source/" + tree["file"])
    pillow_action("Opened image for rescaling.")

    try:
        size = tree["size"].split(",")
        size = convert2xy(intify_list(size))

        rescaled_image = original.resize(size, image.NEAREST)
        pillow_action("Rescaled image.")

        rescaled_image.save("dist/" + tree["result-file"] + ".png", format="PNG")

        pillow_action("Saved rescaled image.")

    except: missing_information()



# "Indent hell is kinda gone, you're welcome." - Jaegerwald

def do_action(action, tree):
    match action:
        case "rearrange": rearrange(tree)
        case "make-apng": make_apng(tree)
        case "split": split(tree)
        case "rescale": rescale(tree)  

def execute_xml_actions(xml_file):
    for action in xml_file["build"]:
        is_list = isinstance(xml_file["build"][action], list)

        if is_list:
            for item in xml_file["build"][action]:
                do_action(action, item)
        else:
            do_action(action, xml_file["build"][action])

def go_through_xml_file(xml_file):
    got_file(xml_file)

    os.makedirs("dist/" + xml_file.replace(".xml", ""))
    try:
        with open("source/" + xml_file, "r") as file:
            file_content = file.read()
            file.close()
            file_content = file_content.replace("    ", "").replace("\n", "")

        xml_file = parse_xml(file_content)
        execute_xml_actions(xml_file)
    except:
        invalid_xml()

def remove_empty_folders():
    for root, directorys, files in os.walk("dist/", topdown=False):
        for directory in directorys:
            directory_path = os.path.join(root, directory)
            if not os.listdir(directory_path): os.rmdir(directory_path)
    removed_empty_folders()

def get_xml_files():
    for file in os.listdir("source"):
        if file.endswith(".xml"):
            xml_files.append(file)

dont_continue = False
try:
    if len(os.listdir("dist")) > 0:
        dist_filled()
        dont_continue = True
    if not dont_continue:
        try:
            get_xml_files()

            if xml_files == []:
                no_files("xml")

            for xml_file in xml_files:
                go_through_xml_file(xml_file)

            remove_empty_folders()

            end()
        except:
            no_source()
except:
    create_dist()

time.sleep(15)