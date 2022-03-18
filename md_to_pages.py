# -*- coding: utf-8 -*-
# Needs environmental variable PAGES_TEMPLATE to be set as the absolute path
# to the html template file.

import os
import urllib.parse
# External import
import markdown # uses third-party extensions mdx_truly_sane_lists and prependnewline
import bs4
import unidecode
# Internal import
import ressources.normalize as rscNz

# Defines global variables
ext = ['toc', 'prependnewline','mdx_truly_sane_lists']
##ext = ['toc', 'mdx_truly_sane_lists']
githubPath = r"https://github.com/Alban-Peyrat/"
pagesPath = r"https://alban-peyrat.github.io/outils/"
# Je crois pas avoir besoin de ça en fait
fileExtensionsToExclude = ["pdf", "xlsx", "xls", "xlsm", "zip", "py", "js", "css", "json", "xml"]

def remove_accents_link(str):
    return unidecode.unidecode(urllib.parse.unquote(str))

# Je crois pas avoir besoin de ça en fait
def is_excluded_file(str):
    for format in fileExtensionsToExclude:
        if str == format:
            return True
    return False

def main(repo, mdFilePath, htmlDirPath="", rootPath=""):
    # Defines all file paths
    PAGES_TEMPLATE = os.getenv("PAGES_TEMPLATE")
    path = mdFilePath[:mdFilePath.rfind("\\")+1]
    fileName = mdFilePath[len(path):mdFilePath.rfind(".")]
    if fileName == "README":
        fileName = repo
        if path[path[:-1].rfind("\\")+1:-1] == repo:
            path = path[:path[:-1].rfind("\\")+1]
    htmlFilePath = path + fileName + ".html"
    mdTempFilePath = path + "temp.md"
    if htmlDirPath != "":
        htmlFilePath = htmlDirPath + htmlFilePath[len(rootPath):]
        os.makedirs(htmlFilePath[:htmlFilePath.rfind("\\")], exist_ok=True)
##        subDirList = htmlFilePath[len(htmlDirPath)+1:].split("\\")
##        subDirList.pop(len(subDirList)-1)
##        print(subDirList)
##        for dir in subDirList:
##            os.makedirs(dir,)
##            pass
        mdTempFilePath = htmlDirPath + r"\temp.md"


    # Retrieves data from the markdown file
    with open(mdFilePath, mode="r+", encoding="utf-8") as f:
        title = f.readline()[2:-1]
        md = f.read()

    # Writes a temporay file that can be edited
    md = rscNz.upgrade_md_headers(md)
    with open(mdTempFilePath, mode="w", encoding="utf-8") as f:
        f.write("[TOC]\n")
        f.write(md)

    # Creates the HTML file from the temporary file
    markdown.markdownFromFile(input=mdTempFilePath, output=htmlFilePath, encoding="utf-8", extensions=ext)

    # Gets Pages template
    with open(PAGES_TEMPLATE, mode="r", encoding="utf-8") as f:
        template = bs4.BeautifulSoup(f, "html.parser")

    # Opens the new HTML file
    with open(htmlFilePath, mode="r+", encoding="utf-8") as f:
        soup = bs4.BeautifulSoup(f, "html.parser")
        # Loop through each links
        links = soup.findAll('a')
        for lnk in links:
            href = lnk.get("href")
            if href[:1] == "#": # Internal file link
                lnk["href"] = remove_accents_link(href)
            elif href.find("/") == -1 or href[:1] == ".": # Same directory file /!\ needs to be changed
                format = href[href.rfind(".")+1:href.rfind(".")+3]
                if format == "md":
                    lnk["href"]  = href[:href.rfind(".")+1] + "html"+ remove_accents_link(href[href.rfind(".")+3:])
            elif href[:len(githubPath)] == githubPath: # Link to my GitHub files
                dotIndex = href.rfind(".", len(githubPath))
                hashIndex = href.rfind("#", len(githubPath))
                # Link to a repository (probably)
                if dotIndex == -1 and hashIndex == -1:
                    lnk["href"] = pagesPath + lnk["href"][len(githubPath):]
                # Link to a file (might be a .md)
                elif dotIndex > -1 and hashIndex == -1:
                    format = href[dotIndex+1:len(href)]
                    if format == "md":
                        print(lnk["href"])
                        lnk["href"] = pagesPath + lnk["href"][len(githubPath):]
                        print(lnk["href"])
                # Link to a file with an internal link (might be a .md)
                elif dotIndex > -1 and hashIndex > -1:
                    lnk["href"] = lnk["href"][:hashIndex] + remove_accents_link(lnk["href"][hashIndex:])
                    format = href[dotIndex+1:hashIndex]
                    if format == "md":
                        lnk["href"] = pagesPath + lnk["href"][len(githubPath):]
                # Link to a repository (probably) with an internal link
                elif dotIndex == -1 and hashIndex > -1:
                    lnk["href"] = lnk["href"][:hashIndex] + remove_accents_link(lnk["href"][hashIndex:])
                    lnk["href"] = pagesPath + lnk["href"][len(githubPath):]

        # Adding the template
        # Adds the page title
        template.title.append(title)
        template.find(id="pageName").string = title
        # Adds the table of contents as an ordered list
        toc = soup.findAll("div",{"class":"toc"})
        if len(toc) > 0:
            if toc[0].li == None:
                template.find(id="tableMatieres").decompose()
            else:
                toc = toc[0].contents[1]
                for this in toc.findAll("ul"):
                    this.name = "ol"
                template.find(id="tableMatieres").append(toc)

        # Adds links to GitHub
        ghLinks = template.find(id="lienGitHub")
        ghLinks.li.a.append(repo)
        ghLinks.li.a["href"] = ghLinks.li.a["href"] + repo

        # Adds the page to the template
        template.find(id="main").append(soup)

        # Applies changes
        f.seek(0 , 0)
        f.truncate()
        f.write(str(template))

        return htmlFilePath


##main("WinIBW", r"D:\test_python\EDIT_MARKDOWN.md")
##print(main("WinIBW", r"D:\transform_github\original_repos\WinIBW\README.md", r"D:\transform_github\a_upload", r"D:\transform_github\original_repos"))

