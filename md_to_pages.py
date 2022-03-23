# -*- coding: utf-8 -*-
# Needs environmental variable PAGES_TEMPLATE to be set as the absolute path
# to the html template file.

import os
import urllib.parse
# External import
import markdown # uses third-party extensions mdx_truly_sane_lists
import bs4
import unidecode
# Internal import
import ressources.normalize as rscNz

# Defines global variables
##ext = ['toc', 'prependnewline','mdx_truly_sane_lists']
ext = ['toc', 'mdx_truly_sane_lists']
githubPath = r"https://github.com/Alban-Peyrat/"
pagesPath = r"https://alban-peyrat.github.io/outils/"
specificScripts = {"aide-depot":["./aideDepot_addCopyHtml.js"]}
# Je crois pas avoir besoin de ça en fait
fileExtensionsToExclude = ["pdf", "xlsx", "xls", "xlsm", "zip", "py", "js", "css", "json", "xml"]

def remove_accents_link(str):
    """Returns the URL removing accents."""
    return unidecode.unidecode(urllib.parse.unquote(str))

# Je crois pas avoir besoin de ça en fait
def is_excluded_file(str):
    for format in fileExtensionsToExclude:
        if str == format:
            return True
    return False

def get_first_char(line):
    """Returns the numbers of spaces before the first character and the first
    character.

    Arguments:
        line {string} -- a line. Must not be a empty line"""
    ind = 0
    for chr in line:
        if chr == " ":
            ind += 1
        else:
            return ind, chr

def is_list(ind, chr, line):
    """Returns if the line is part of a list or not.

    Arguments:
        ind {integer} -- the indentation
        chr {string} -- the first character of the line after the identention
        line {string} -- the whole line"""
    if chr == "*":
        if line[ind + 1] == " ":
            return True
        else:
            return False
    elif chr.isnumeric():
        if line[ind + 1:ind + 3] == ". ":
            return True
        else:
            return False
    else:
        return False

def prepend_new_lines_to_list(f): # It seems to work perfectly.
    # Which honnestly doesn't feel right because I had no bugs when I finished
    # the reverse loop. I did forget to add a break that absolutely did not
    # matter in the html file but still, I'm feeling suspicious.
    """Insert a new line before markdown lists (not sublists).
    /!\ It is designed for my markdown files.

    Arguments:
        f {string} -- the markdown file as a string (afetr a read()

    Returns a list."""
    lines = f.split("\n")
    output = []
    for ii, line in enumerate(lines):
        if len(line) > 0:
            if line.strip() == "":
                output.append("")
                continue
            ind, chr = get_first_char(line)
            if is_list(ind, chr, line):
                for jj in reversed(range(len(output))):
                    if output[jj] == "":
                        output.append("")
                        break
                    else:
                        ind, chr = get_first_char(output[jj])
                        if is_list(ind, chr, output[jj]):
                            break
                output.append(line)
            else:
                output.append(line)
        else:
            output.append(line)
    return output

def main(repo, mdFilePath, htmlDirPath="", rootPath=""):
    """Transforms a markdown file to a html files applying a template.
    /!\ Designed for my GitHub Pages.

    Arguments:
        repo {string} -- Name of the GitHub repository (/!\ is used in a link)
        mdFilePath {rString} -- absolute path to the markdown file.
        htmlDirPath {rString} -- absolute path of directory of the output html file.
        rootPath {rString} --

    Returns the absolute path  of the created file."""
    # Defines all file paths
    PAGES_TEMPLATE = os.getenv("PAGES_TEMPLATE")
    path = mdFilePath[:mdFilePath.rfind("\\")+1]
    fileName = mdFilePath[len(path):mdFilePath.rfind(".")]
    if fileName == "README":
        fileName = repo[repo.rfind("\\")+1:]
        if path[path[:-1].rfind("\\")+1:-1] == repo:
            path = path[:path[:-1].rfind("\\")+1]
    htmlFilePath = path + fileName + ".html"
    mdTempFilePath = path + "temp.md"
    if htmlDirPath != "":
        htmlFilePath = htmlDirPath + htmlFilePath[len(rootPath):]
        os.makedirs(htmlFilePath[:htmlFilePath.rfind("\\")], exist_ok=True)
        mdTempFilePath = htmlDirPath + r"\temp.md"


    # Retrieves data from the markdown file
    with open(mdFilePath, mode="r+", encoding="utf-8") as f:
        title = f.readline()[2:-1]
        md = f.read()

    # Writes a temporay file that can be edited
    md = rscNz.upgrade_md_headers(md)
    md = prepend_new_lines_to_list(md)
    with open(mdTempFilePath, mode="w", encoding="utf-8") as f:
        f.write("[TOC]\n")
        for line in md:
            f.write(line + "\n")

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
                toc = toc[0]
##                toc = toc[0].contents[1]
                tocType = ["I", "A", "1", "a", "i"]
                for this in toc.findAll("ul"):
                    this.name = "ol"
                    thisParent = this.find_parent("ol")
                    if thisParent == None:
                        this["type"] = tocType[0]
                    else:
                        tocTypeInd = tocType.index(thisParent["type"]) + 1
                        if tocTypeInd == 5:
                            tocTypeInd = 0
                        this["type"] = tocType[tocTypeInd]
                template.find(id="tableMatieres").append(toc)

        # Adds links to GitHub
        ghLinks = template.find(id="lienGitHub")
        ghLinks.li.a.append(repo)
        if "\\" in repo:
            subRepo = repo[:repo.find("\\")] + "/tree/main/" + repo[repo.find("\\")+1:]
            ghLinks.li.a["href"] = ghLinks.li.a["href"] + subRepo
        else:
            ghLinks.li.a["href"] = ghLinks.li.a["href"] + repo

        # Adds the page to the template
        template.find(id="main").append(soup)

        # Adds complementary scripts if needed
        if fileName in specificScripts:
            for script in specificScripts[fileName]:
                scriptTag = template.new_tag("script", src=script)
                template.html.append(scriptTag)

        # Applies changes
        f.seek(0 , 0)
        f.truncate()
        f.write(str(template))

        return htmlFilePath

##main("WinIBW", r"D:\test_python\EDIT_MARKDOWN.md")
##main("ub-svs", r"D:\transform_github\original_repos\ub-svs\dumas\README.md", r"D:\transform_github\a_upload\outils", r"D:\transform_github\original_repos")
##main("ub-svs", r"D:\transform_github\original_repos\ub-svs\dumas\aide-depot.md", r"D:\transform_github\a_upload\outils", r"D:\transform_github\original_repos")
##print(main("WinIBW", r"D:\transform_github\original_repos\WinIBW\scripts.md", r"D:\transform_github\a_upload", r"D:\transform_github\original_repos"))
