from xmltodict import parse as parse_xml
from PIL import Image as image
from colorama import *
import os, time

just_fix_windows_console()

xml_files, png_files = [], []
output = "[ MCWEBGUI BUILDER LOG FILE ]\n"

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
def no_files(format, folder):
    print(Back.RED + Fore.BLACK + " ERR " + Style.RESET_ALL + " No " + Fore.BLACK + Style.BRIGHT + "." + format + Style.RESET_ALL + " files were found in the " + Fore.BLACK + Style.BRIGHT + folder + Style.RESET_ALL + " folder!")
    write_output("[ERR] No \"." + format + "\" files were found in the " + folder + " folder!")
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

def rearrange(tree):
    require_file(tree["file"])
    original = image.open("source/" + tree["file"])
    pillow_action("Opened file to rearrange.")

    try:
        non_repeating_size = tree["non-repeating"]["size"].split(",")

        non_repeating = image.new(
            "RGBA",
            (int(non_repeating_size[0]), int(non_repeating_size[1])),
            (255, 255, 255, 0)
        )
        pillow_action("Created new empty image.")

        non_repeating_instructions = tree["non-repeating"]["move"].split("|")

        for instruction in non_repeating_instructions:
            parts = instruction.split(":")
            new_position = parts[1].split(",")
            old_part = parts[0].split(";")
            old_position = old_part[0].split(",")
            size = old_part[1].split(",")

            crop_area = (int(old_position[0]), int(old_position[1]), int(size[0]) + int(old_position[0]), int(size[1]) + int(old_position[1]))
            new_part = original.crop(crop_area)

            position = (int(new_position[0]), int(new_position[1]))
            non_repeating.paste(new_part, position)
        pillow_action("Rearranged parts of the original image.")

        non_repeating.save("dist/" + tree["result-file"] + ".png", format="PNG")
        pillow_action("Saved newly created image.")
    except:
        no_part_list("non-repeating")

    #

    try:
        vertically_repeating_size = tree["vertically-repeating"]["size"].split(",")

        vertically_repeating = image.new(
            "RGBA",
            (int(vertically_repeating_size[0]), int(vertically_repeating_size[1])),
            (255, 255, 255, 0)
        )
        pillow_action("Created new empty image.")

        vertically_repeating_instructions = tree["vertically-repeating"]["move"].split("|")

        for instruction in vertically_repeating_instructions:
            parts = instruction.split(":")
            new_position = parts[1].split(",")
            old_part = parts[0].split(";")
            old_position = old_part[0].split(",")
            size = old_part[1].split(",")

            crop_area = (int(old_position[0]), int(old_position[1]), int(size[0]) + int(old_position[0]), int(size[1]) + int(old_position[1]))
            new_part = original.crop(crop_area)

            position = (int(new_position[0]), int(new_position[1]))
            vertically_repeating.paste(new_part, position)
        pillow_action("Rearranged parts of the original image.")

        vertically_repeating.save("dist/" + tree["result-file"] + "_vertical.png", format="PNG")
        pillow_action("Saved newly created image.")
    except:
        no_part_list("vertically-repeating")

    #

    try:
        horizontally_repeating_size = tree["horizontally-repeating"]["size"].split(",")

        horizontally_repeating = image.new(
            "RGBA",
            (int(horizontally_repeating_size[0]), int(horizontally_repeating_size[1])),
            (255, 255, 255, 0)
        )
        pillow_action("Created new empty image.")

        horizontally_repeating_instructions = tree["horizontally-repeating"]["move"].split("|")

        for instruction in horizontally_repeating_instructions:
            parts = instruction.split(":")
            new_position = parts[1].split(",")
            old_part = parts[0].split(";")
            old_position = old_part[0].split(",")
            size = old_part[1].split(",")

            crop_area = (int(old_position[0]), int(old_position[1]), int(size[0]) + int(old_position[0]), int(size[1]) + int(old_position[1]))
            new_part = original.crop(crop_area)

            position = (int(new_position[0]), int(new_position[1]))
            horizontally_repeating.paste(new_part, position)
        pillow_action("Rearranged parts of the original image.")

        horizontally_repeating.save("dist/" + tree["result-file"] + "_horizontal.png", format="PNG")
        pillow_action("Saved newly created image.")
    except:
        no_part_list("horizontally-repeating")

def make_apng(tree):
    require_file(tree["file"])
    spritesheet = image.open("source/" + tree["file"])
    pillow_action("Opened file to make APNG.")
    frames = []

    try:
        size = tree["size"].split(",")

        for y in range(0, spritesheet.height, int(size[1])):
            for x in range(0, spritesheet.width, int(size[0])):
                frame = spritesheet.crop((x, y, x + int(size[0]), y + int(size[1])))
                frame = frame.convert("RGBA")
                frames.append(frame)

        pillow_action("Split all APNG frames.")

        if tree["loop"] == "none":
            frames[0].save("dist/" + tree["result-file"] + ".png", format="PNG", save_all=True, append_images=frames[1:], duration=int(tree["frame-time"]), loop=1)
        else:
            frames[0].save("dist/" + tree["result-file"] + ".png", format="PNG", save_all=True, append_images=frames[1:], duration=int(tree["frame-time"]), loop=int(tree["loop"]))

        pillow_action("Saved APNG image.")

    except Exception as e:
        missing_information()
        print(e)

def split(tree):
    require_file(tree["file"])
    spritesheet = image.open("source/" + tree["file"])
    pillow_action("Opened file for image splitting.")
    images = []

    try:
        size = tree["size"].split(",")
        files = tree["files"].split(",")
        
        for y in range(0, spritesheet.height, int(size[1])):
            for x in range(0, spritesheet.width, int(size[0])):
                sprite = spritesheet.crop((x, y, x + int(size[0]), y + int(size[1])))
                sprite = sprite.convert("RGBA")
                images.append(sprite)

        pillow_action("Split all images.")

        for i in range(0, len(images)):
            try:
                images[i].save("dist/" + files[i] + ".png", format="PNG")
            except:
                return
        
        pillow_action("Saved images.")
            
    except Exception as e:
        missing_information()
        print(e)

# "Sorry for indent hell lol" - Jaegerwald

dont_continue = False
try:
    if len(os.listdir("dist")) > 0:
        dist_filled()
        dont_continue = True
    if not dont_continue:
        try:
            for file in os.listdir("source"):
                if file.endswith(".xml"):
                    xml_files.append(file)
                elif file.endswith(".png"):
                    png_files.append(file)

            if xml_files == []:
                no_files("xml", "source")

            for xml_file in xml_files:
                got_file(xml_file)

                os.makedirs("dist/" + xml_file.replace(".xml", ""))
                try:
                    with open("source/"+xml_file, "r") as file:
                        file_content = file.read()
                        file.close()
                        file_content = file_content.replace("    ", "").replace("\n", "")

                    xml_file = parse_xml(file_content)

                    for action in xml_file["build"]:
                        is_list = isinstance(xml_file["build"][action], list)

                        match action:
                            case "rearrange":
                                if is_list:
                                    for item in xml_file["build"][action]:
                                        rearrange(item)
                                else:
                                    rearrange(xml_file["build"][action])
                            case "make-apng":
                                if is_list:
                                    for item in xml_file["build"][action]:
                                        make_apng(item)
                                else:
                                    make_apng(xml_file["build"][action])
                            case "split":
                                if is_list:
                                    for item in xml_file["build"][action]:
                                        split(item)
                                else:
                                    split(xml_file["build"][action])
                except:
                    invalid_xml()
            for root, directorys, files in os.walk("dist/", topdown=False):
                for directory in directorys:
                    directory_path = os.path.join(root, directory)
                    if not os.listdir(directory_path):
                        os.rmdir(directory_path)
            
            removed_empty_folders()
            end()
        except:
            no_source()
except:
    create_dist()

time.sleep(15)