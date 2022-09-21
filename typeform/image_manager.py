import os
from logging_dir.logging import logger
import re
import rest




def image_consultant(app_data):
    logger.info(f"Beginning typeform image extraction process")
    list_of_images = url_extractor(app_data.full_condensed_typeform)
    if not list_of_images:
        logger.info("No images provided, exiting out of process")
        return 
    else:
        try:
            folder_path = folder_creator(app_data)
        except Exception as err:
            raise err
        for image in list_of_images['items']:
            imageHandler(image, folder_path)


class imageHandler(object):

    def __init__(self, image, folder_path) -> None:
        self.image_name = image['filename']
        self.url = image['url']
        self.path = folder_path
        self.controller()

    def controller(self):
        self.file_downloader()
    
    def file_downloader(self):
        logger.info(f"Downloading {self.image_name}")
        downloaded_obj = rest.get(self.url)
        # Get the filetype from the header
        file_extension = (downloaded_obj.headers['Content-Type'].split("/",1)[1])
        # Write the file to new dir
        with open(f"{self.path}/{self.image_name}.{file_extension}", "wb") as file:
            file.write(downloaded_obj.content)


# Create dir for images to live
def folder_creator(app_data):
    cwd = os.getcwd() 
    parent_dir = f"{cwd}/typeform/temp/"
    dir = (app_data.app_name[0].lower()).replace(" ", "_")
    logger.info(f"Creating dir for {dir}")
    path = os.path.join(parent_dir, dir)
    print(path)
    if not os.path.isdir(path):
        os.mkdir(path)
    else:
        logger.info(f"{path} already exists.")
    return path


# Function to extract file urls from response data
def url_extractor(data):
    #print(f"{data}")
    responses_with_urls = {"items": []}
    for response in data['fields']:
        #print(response)
        if 'file_url' in response['type']:
            logger.info("found file url")
            visual_name = image_name_creator(response['title'])
            url = response['response']
            image_block = {"filename": visual_name, "url": url}
            #print(image_block)
            responses_with_urls['items'].append(image_block)
    #print(responses_with_urls)
    if len(responses_with_urls['items']) == 0:
        logger.info("No uploaded images provided")
        return False
    else:
        return responses_with_urls


# Function to create the unqique key for each image found in the list
def image_name_creator(response_title):
    #print(response_title)
    if "app visual" in response_title:
        logger.info(f"Creating image name from: {response_title}")
        # extract the first number from the title of the questions - format is:
        # 'Upload app visual 1 out of 5' - in this example we'd extract '1'
        try:
            image_name = "visual_{0}".format(re.search(r'\d+', response_title).group())
        except Exception as err:
            raise err
    elif "logo" in response_title:
        logger.info(f"Logo found, creating image name.")
        image_name = "logo"
    return image_name