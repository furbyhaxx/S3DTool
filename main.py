import winreg
import argparse
import os

import xml.etree.ElementTree as ET


REG_PATH = r"Software\Simplify3D\S3D-Software\FFFWindow"

"""
sorts a list object linked to another list object
@version 1
"""


def sort_list(list1, list2):
    zipped_pairs = zip(list2, list1)

    z = [x for _, x in sorted(zipped_pairs)]

    return z


"""
set_reg
sets a registry entry
"""


def set_reg(name, value):
    try:
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0,
                                      winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_MULTI_SZ, value)
        winreg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False


'''
get_reg
return a list object
'''


def get_reg(name):
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0,
                                      winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(registry_key, name)
        winreg.CloseKey(registry_key)
        return value
    except WindowsError:
        return None

def write_file(filename, contents):
    f = open(filename, "w+")
    f.write(contents)
    f.close()

def make_filename_valid(filename):
    filename = filename.replace("/", "").replace("\\", "").replace(":", "").replace("*", "").replace("<", "").replace(">", "").replace("|", "")

    return filename

def s3dtool():
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--sorting', action='store_true', help="sorts all profiles")
    parser.add_argument('-e', '--exporting', help="exports all profiles to path")
    parser.add_argument('-i', '--importing', help="imports all profiles from path")
    parser.add_argument('-x', '--xmltest', action='store_true', help="imports all profiles from path")

    args = parser.parse_args()

    if args.sorting:
        print("sorting")
        profile_xml = get_reg('profileDatabaseContents')
        profile_names = get_reg('profileDatabaseNames')

        # profile_xml = get_reg('test1')
        # profile_names = get_reg('profileDatabaseNames')

        profile_names_sorted = sorted(profile_names)

        profile_xml_sorted = sort_list(profile_xml, profile_names)

        # myarray = profiles_xml.split("\n\n")

        # for line in slist:
        # print(line)
        # print("Next Line")

        # set_reg('profileDatabaseNames', profile_names_sorted)
        # set_reg('profileDatabaseContents', profile_xml_sorted)

        print(profile_xml)
        print(profile_names)

        print("sorted")

        print(profile_xml_sorted)
        print(profile_names_sorted)

        set_reg('profileDatabaseNames', profile_names_sorted)
        set_reg('profileDatabaseContents', profile_xml_sorted)

        # for i in range(len(profile_names_sorted)):
        #     # print(list[i])
        #     f = open("c:/s3d_backup/" + profile_names_sorted[i] + ".fff", "w+")
        #     f.write(profile_xml_sorted[i])
        #     f.close()

    if args.exporting:
        print("exporting")
        print(args.exporting)
        path = args.exporting

        profile_xml = get_reg('profileDatabaseContents')
        profile_names = get_reg('profileDatabaseNames')

        profile_names_sorted = sorted(profile_names)
        profile_xml_sorted = sort_list(profile_xml, profile_names)

        for i in range(len(profile_names_sorted)):
            root = ET.fromstring(profile_xml_sorted[i])
            filename = root.attrib['name']
            write_file(path + "\\" + make_filename_valid(filename) + ".fff", profile_xml_sorted[i])


    if args.importing:
        print("importing")
        print(args.importing)
        path = args.importing

        profile_xml = get_reg('profileDatabaseContents')
        profile_names = get_reg('profileDatabaseNames')

        for filename in os.listdir(path):
            if filename.endswith(".fff"):
                print(filename)
                f = open(path + "\\" + filename, 'r')
                lines = f.read()
                # print(lines)
                root = ET.parse(path + "\\" + filename).getroot()
                filename = root.attrib['name']  # get filename for duplicate checking

                if filename in profile_names:  # check if profile already exists
                    listindex = profile_names.index(filename)
                    profile_xml[listindex] = lines
                    print("duplicate profile:"+filename + ", updating")
                else:
                    profile_names.append(filename)
                    profile_xml.append(lines)
                    print("new profile:" + filename + ", adding")
                continue
            else:
                continue

        profile_names_sorted = sorted(profile_names)
        profile_xml_sorted = sort_list(profile_xml, profile_names)

        set_reg('profileDatabaseNames', profile_names_sorted)
        set_reg('profileDatabaseContents', profile_xml_sorted)

    if args.xmltest:
        print(make_filename_valid("testetst / \\ test :.fff"))






if __name__ == '__main__':
    s3dtool()