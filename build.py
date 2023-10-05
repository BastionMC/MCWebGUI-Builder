from xmltodict import parse as parse_xml
from PIL import Image as image
from colorama import *
import os

just_fix_windows_console()

def create_dist():
    print(Back.YELLOW + Fore.BLACK + " WRN " + Style.RESET_ALL + " Please create a " + Fore.BLACK + Style.BRIGHT + "dist " + Style.RESET_ALL + "folder before running this program.")
def dist_filled():
    print(Back.YELLOW + Fore.BLACK + " WRN " + Style.RESET_ALL + " The " + Fore.BLACK + Style.BRIGHT + "dist " + Style.RESET_ALL + "folder has some files in it. Please clear it first.")
def no_source():
    print(Back.RED + Fore.BLACK + " ERR " + Style.RESET_ALL + " The " + Fore.BLACK + Style.BRIGHT + "source " + Style.RESET_ALL + "folder doesn't seem to exist. Cannot continue.")
def no_files(format, folder):
    print(Back.RED + Fore.BLACK + " ERR " + Style.RESET_ALL + " No " + Fore.BLACK + Style.BRIGHT + "." + format + Style.RESET_ALL + " files were found in the " + Fore.BLACK + Style.BRIGHT + folder + Style.RESET_ALL + " folder!")
def got_file(file):
    print(Back.GREEN + Fore.BLACK + " GOT " + Style.RESET_ALL + " Found the file " + Fore.BLACK + Style.BRIGHT + file + Style.RESET_ALL + ".")
def require_file(file):
    print(Back.MAGENTA + Fore.BLACK + " REQ " + Style.RESET_ALL + " Requested the file " + Fore.BLACK + Style.BRIGHT + file + Style.RESET_ALL + ".")
def pillow_action(string):
    print(Back.CYAN + Fore.BLACK + " PIL " + Style.RESET_ALL + " " + string)
def end():
    print(Back.WHITE + Fore.BLACK + " END " + Style.RESET_ALL + " All files have been processed.")
def invalid_xml():
    print(Back.RED + Fore.BLACK + " ERR " + Style.RESET_ALL + " This XML file is invalid, it cannot be processed.")
def no_part_list(part):
    print(Back.YELLOW + Fore.BLACK + " NIL " + Style.RESET_ALL + " No " + part + " parts were found.")

xml_files, png_files = [], []

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

# "Sorry for indent hell." - Jae

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
                except:
                    invalid_xml()
            end()
        except:
            no_source()
except:
    create_dist()

os.system("pause")