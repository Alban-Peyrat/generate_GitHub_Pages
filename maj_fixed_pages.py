# -*- coding: utf-8 -*-
# Needs environmental variable PAGES_TEMPLATE to be set as the absolute path
# to the html template file.

import os
# External import
import bs4

def main(originalFilePath, newDirPath=""):
    """Applies the template to the html file. Keeps the content of the div with
    the id "contenu".

    Arguments:
        originalFilePath {rString} -- absolute path to the html file.
        newDirPath {rString} -- directory of the output file.

    Returns the absolute path  of the created file."""
    fileName = originalFilePath[originalFilePath.rfind("\\")+1:]

    # Gets Pages template
    PAGES_TEMPLATE = os.getenv("PAGES_TEMPLATE")
    with open(PAGES_TEMPLATE, mode="r", encoding="utf-8") as f:
        template = bs4.BeautifulSoup(f, "html.parser")

    with open(originalFilePath, mode="r+", encoding="utf-8") as f:
        soup = bs4.BeautifulSoup(f, "html.parser")
        content = soup.find(id="contenu")
        template.find(id="contenu").clear()
        template.find(id="contenu").append(content)
        title = template.find(id="pageName").string
        template.title.append(title)
        template.find(id="pageName").string = title

    # Applies changes
    with open(newDirPath + "\\" + fileName, mode="w", encoding="utf-8") as f:
        f.seek(0 , 0)
        f.truncate()
        f.write(str(template))

    return newDirPath + "\\" + fileName

##main(r"D:\transform_github\original_repos\404.html", r"D:\transform_github\a_upload")