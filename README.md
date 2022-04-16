# Final-Project-X--COMP593

3/19/2022 - Currently working on recieveing http connection and response
successful request to the nasa server though http connection with response 200

due to the fact that i've started working on lab 6 and wasn't working with functions before lab 6 we have decided to switch over to the requests module which we are using instead of using the stupid HTTP module that i hate. Thank you requests is so much better.

4/7/2022 - Didn't realize you needed to use the template provided. basically starting from scratch now. datetime module is being imported but for some reason doesn't know what datetime.strptime is? i'll figure this out soon i hope. moving on to getting that image url first.

4/17/2022 - strictly using the apod_desktop.py as a reference while i build it myself and taking only the parts of the code that i need, kind helps me become more familier with what the process of actually building something like this from the ground up us like

Reviewed the lab video to find out what things i needed to import, if i need to import anything else i guess i'll figure it out along the way. get_apod_info nabbing the apod date from before and then it now return the apod_dict. Not sure if i'll need to return the whole dictionary of just parts of this with this function but that's for later i guess if it doesn't work the way i need it to.

used sha256(image_url.encode()) to encode the image from the url and then used print(image_sha256.hexdigest()) to print out the hash for the image. and for the image size len(requests.get(image_url).content) and printed the image_size variable + bytes to print the image size. Need to figure out how to work with the local urls, assuming it has something to with with that os path module.

getting the image path was interesting, not sure if i was meant to do it this way but i'm going to do it this way anyway. imported re, using regex to make a capture group of the image name from the image_url. Joining the strings together to get the path with the image name added to the end.

so basically...
image_name = re.match('https://apod.nasa.gov/apod/image/\d*/(\w*.jpg)', image_url)
image_path = dir_path + image_name.group(1)
return image_path
    
hopefully this will work well until the end and i won't have to backtrack to my previous function.
The only issue i forsee doing this is having to add /'s to the end of a directory or figuring out a way to make that work without worrying about that?
