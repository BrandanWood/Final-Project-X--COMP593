# Final-Project-X--COMP593

3/19/2022 - Currently working on recieveing http connection and response
successful request to the nasa server though http connection with response 200

due to the fact that i've started working on lab 6 and wasn't working with functions before lab 6 we have decided to switch over to the requests module which we are using instead of using the stupid HTTP module that i hate. Thank you requests is so much better.

4/7/2022 - Didn't realize you needed to use the template provided. basically starting from scratch now. datetime module is being imported but for some reason doesn't know what datetime.strptime is? i'll figure this out soon i hope. moving on to getting that image url first.

4/15/2022 - strictly using the apod_desktop.py as a reference while i build it myself and taking only the parts of the code that i need, kind helps me become more familier with what the process of actually building something like this from the ground up us like

Reviewed the lab video to find out what things i needed to import, if i need to import anything else i guess i'll figure it out along the way. get_apod_info nabbing the apod date from before and then it now return the apod_dict. Not sure if i'll need to return the whole dictionary of just parts of this with this function but that's for later i guess if it doesn't work the way i need it to.

used sha256(image_url.encode()) to encode the image from the url and then used print(image_sha256.hexdigest()) to print out the hash for the image. and for the image size len(requests.get(image_url).content) and printed the image_size variable + bytes to print the image size. Need to figure out how to work with the local urls, assuming it has something to with with that os path module.

getting the image path was interesting, not sure if i was meant to do it this way but i'm going to do it this way anyway. imported re, using regex to make a capture group of the image name from the image_url. Joining the strings together to get the path with the image name added to the end.

so basically...
image_name = re.match('https://apod.nasa.gov/apod/image/\d*/(\w*.jpg)', image_url)
image_path = dir_path + image_name.group(1)
return image_path
    
hopefully this will work well until the end and i won't have to backtrack to my previous function.
The only issue i forsee doing this is having to add /'s to the end of a directory or figuring out a way to make that work without worrying about that?

regex proably won't work, probably can use path module to do something about this.

currently working with downloading the apod image, i have found several methods to get the job done but i just need to figure out how to get the reponse into the other function and save that file into the image path. once i figure that out everything else should be pretty simple.

4/16/2022 - got around to actually getting the file to download and it downloads to the current working directory. going to return that downloading of the file and use that for the save_image_file function

code looks something like this for the downloading of the apod image.

response = requests.get(image_url)
file = open(path.basename(image_url), 'wb')
return file.write(response.content)

it uses requests module to do this. Now i just have to figure out how to get it to save the image to the file path.

hey it works!

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
    
    nice!

4/17/2022 - Working on the database stuff and refering back to lab 3 to remember what i did previously. Created the table successfully and it's being made in the current proper folder. i have it set up to insert the information into the table and execute the addApodQuery, addApod and then commits and closes.

Seem to having this error. sqlite3.InterfaceError: Error binding parameter 2 - probably unsupported type.
  File "apod_desktop.py", line 59, in main
    add_image_to_db(db_path, image_path, image_size, image_sha256)
  File "apod_desktop.py", line 228, in add_image_to_db
    c.execute(addApodQuery, addApod)

The things related to these are probably the issue not these lines themselves.

just converted the data types into str and int where nessacary. it works now.

Now just need to figure out how to fix up image_already_in_db function then it's just setting the desktop background.

i struggled for a while the image already in db part, couldn't figure out how to use the varible in the c.execute to find the specific hash in the database but i found out that you can just put an =? and the ? will be filled with a varible you put after that part of the code. so

c.execute("SELECT image_sha256 FROM apod WHERE image_sha256=?", (hashie,)) the hashie variable value will take the place of the ?.

after that i just used the length of the return and if it's greater or equal to 1 then it returns true and if it's less than it returns false.

doing a little googling, i found the ctypes module and a quick couple searches on how to set desktop backgrounds with python told me how to do it so it was suprisingly very easy to do. just have to test the script and see if it actually works.

yo it works!!! it's kinda sick. might play around and see if i can add a gui to it for fun.

PROJECT COMPLETE!
