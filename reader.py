from __future__ import print_function
from os import listdir
from os.path import join
from pyzbar import pyzbar
from pyzbar.pyzbar import ZBarSymbol
from imghdr import what as is_image
from PIL import Image
import argparse

def load_images_from_folder():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--folder", required=True, help="path to image folder")
    args = vars(ap.parse_args())

    images = []
    file_names = []
    for filename in listdir(args["folder"]):
        file_path = join(args["folder"], filename)
        if is_image(file_path):
            image = Image.open(file_path).convert('RGB')
            if image is not None:
                images.append(image)
                file_names.append(filename)

    return args, images, file_names

def decode(image):
    # Find barcodes and QR codes
    decoded_objects = pyzbar.decode(image, symbols=[ZBarSymbol.CODE128])
    return decoded_objects

def reader():
    args, images, file_names = load_images_from_folder()

    # split the path by /
    path_splitted = args["folder"].split("/")
    # create the csv name, when the path is splitted we always want the 2 indexes before the end
    csv_name = path_splitted[len(path_splitted) - 2]
    detected_csv = open("output/{}.csv".format(csv_name), "w+")
    print("\n[i] output path: {}".format("output/{}.csv".format(csv_name)))
    # write header
    detected_csv.write("filename, barcode\n")

    for index, image in enumerate(images):
        decoded_objects = decode(image)
        
        print('\n[i] Filename: ', file_names[index])

        # Print results
        if decoded_objects:
            for obj in decoded_objects:
                # print('Type : ', obj.type)
                print('[i] Barcode : ', obj.data)

                # join the values comma separated
                line = "{}, {}\n".format(file_names[index], obj.data)
                # write into the file
                detected_csv.write(line)
        else:
            print("[x] No barcode detected, writing empty string")
            # join the values comma separated
            line = "{}, \n".format(file_names[index])
            # write into the file
            detected_csv.write(line)

# Read image
reader()