""" 
COMP 593 - Final Project

Description: 
  Downloads NASA's Astronomy Picture of the Day (APOD) from a specified date
  and sets it as the desktop background image.

# k3C4uX9rjMstIF0L157GikrllFdp0TVVuJkijxUp api key

Usage:
  python apod_desktop.py image_dir_path [apod_date]

Parameters:
  image_dir_path = Full path of directory in which APOD image is stored
  apod_date = APOD image date (format: YYYY-MM-DD)

History:
  Date        Author    Description
  2022-03-11  J.Dalby   Initial creation
  2022-04-07  B.Wood    Changes Made
"""
import requests
import sqlite3
from datetime import datetime, date
from hashlib import sha256
from sys import argv, exit
from os import path
import ctypes


def main():

    # Determine the paths where files are stored
    image_dir_path = get_image_dir_path()
    db_path = path.join(image_dir_path, 'apod_images.db')

    # Get the APOD date, if specified as a parameter
    apod_date = get_apod_date()

    # Create the images database if it does not already exist
    create_image_db(db_path)

    # Get info for the APOD
    apod_dict = get_apod_info(apod_date)
    
    # Download today's APOD
    image_url = apod_dict['url']
    image_sha256 = sha256(image_url.encode()).hexdigest()
    image_size = len(requests.get(image_url).content)
    image_path = get_image_path(image_url, image_dir_path)
    image_msg = download_apod_image(image_url)


    # Print APOD image information
    print_apod_info(image_url, image_path, image_size, image_sha256)

    # Add image to cache if not already present
    if not image_already_in_db(db_path, image_sha256):
        save_image_file(image_msg, image_path)
        add_image_to_db(db_path, image_path, image_size, image_sha256)



    # Set the desktop background image to the selected APOD
    set_desktop_background_image(image_path)






def get_image_dir_path():
    """
    Validates the command line parameter that specifies the path
    in which all downloaded images are saved locally.

    :returns: Path of directory in which images are saved locally
    """
    if len(argv[1]) >= 2:
        dir_path = argv[1]
        if path.isdir(dir_path):
            print("Images directory:", dir_path)
            return dir_path
        else:
            print('Error: Non-existent directory', dir_path)
            exit('Script execution aborted')
    else:
        print('Error: Missing path parameter.')
        exit('Script execution aborted')

def get_apod_date():
    """
    Validates the command line parameter that specifies the APOD date.
    Aborts script execution if date format is invalid.

    :returns: APOD date as a string in 'YYYY-MM-DD' format
    """    
    if len(argv) >= 3:
        # Date parameter has been provided, so get it
        apod_date = argv[2]

        # Validate the date parameter format
        try:
            datetime.strptime(apod_date, '%Y-%m-%d')
        except ValueError:
            print('Error: Incorrect date format; Should be YYYY-MM-DD')
            exit('Script execution aborted')
    else:
        # No date parameter has been provided, so use today's date
        apod_date = datetime.today().isoformat()
    
    print("APOD date:", apod_date)
    return apod_date

def get_image_path(image_url, dir_path):
    """
    Determines the path at which an image downloaded from
    a specified URL is saved locally.

    :param image_url: URL of image
    :param dir_path: Path of directory in which image is saved locally
    :returns: Path at which image is saved locally
    """
    image_name = path.basename(image_url)
    image_path = dir_path + '\\' + image_name
    return image_path

def get_apod_info(apod_date):
    """
    Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.

    :param date: APOD date formatted as YYYY-MM-DD
    :returns: Dictionary of APOD info
    """
    data = {'date': apod_date}
    r = requests.get('https://api.nasa.gov/planetary/apod?api_key=k3C4uX9rjMstIF0L157GikrllFdp0TVVuJkijxUp', params=data)
    apod_dict = r.json()
    print(apod_dict)
    return apod_dict

def print_apod_info(image_url, image_path, image_size, image_sha256):
    """
    Prints information about the APOD

    :param image_url: URL of image
    :param image_path: Path of the image file saved locally
    :param image_size: Size of image in bytes
    :param image_sha256: SHA-256 of image
    :returns: None
    """
    print(image_url)
    print(image_path)
    print(image_size, 'bytes')
    print(image_sha256)

def download_apod_image(image_url):
    """
    Downloads an image from a specified URL.

    :param image_url: URL of image
    :returns: Response message that contains image data
    """
    response = requests.get(image_url)
    return response.content


def save_image_file(image_msg, image_path):
    """
    Extracts an image file from an HTTP response message
    and saves the image file to disk.

    :param image_msg: HTTP response message
    :param image_path: Path to save image file
    :returns: None
    """
    file = open(image_path, 'wb')
    file.write(image_msg)
    file.close()

def create_image_db(db_path):
    """
    Creates an image database if it doesn't already exist.

    :param db_path: Path of .db file
    :returns: None
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    createApodTable = """ CREATE TABLE IF NOT EXISTS apod (
                            image_location TEXT,
                            image_size INTEGER,
                            image_sha256 TEXT,
                            time_added TEXT
                            );"""
    conn.execute(createApodTable)
    conn.commit()
    conn.close()

def add_image_to_db(db_path, image_path, image_size, image_sha256):
    """
    Adds a specified APOD image to the DB.

    :param db_path: Path of .db file
    :param image_path: Path of the image file saved locally
    :param image_size: Size of image in bytes
    :param image_sha256: SHA-256 of image
    :returns: None
    """
    now = datetime.now()
    current_time = now.strftime("%Y-/%m-/%d %H:%M:%S")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    addApodQuery = """INSERT INTO apod (
                        image_location,
                        image_size,
                        image_sha256,
                        time_added
                        )
                        VALUES (?, ?, ?, ?);"""


    addApod = (
        str(image_path),
        int(image_size),
        str(image_sha256),
        str(current_time)
        )
    c.execute(addApodQuery, addApod)
    conn.commit()
    conn.close()


def image_already_in_db(db_path, image_sha256):
    """
    Determines whether the image in a response message is already present
    in the DB by comparing its SHA-256 to those in the DB.

    :param db_path: Path of .db file
    :param image_sha256: SHA-256 of image
    :returns: True if image is already in DB; False otherwise
    """
    conn = sqlite3.connect(db_path)
    hashie = image_sha256
    c = conn.cursor()
    c.execute("SELECT image_sha256 FROM apod WHERE image_sha256=?", (hashie,))
    results = c.fetchall()
    print(results)
    if len(results) >= 1:
        print('yes')
        return True
    else:
        print('no')
        return False



def set_desktop_background_image(image_path):
    """
    Changes the desktop wallpaper to a specific image.

    :param image_path: Path of image file
    :returns: None
    """
    path = image_path
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)

main()