# -*- coding: utf-8 -*-

import os
# Internal imports
import md_to_pages as mtp
import maj_fixed_pages as mfp
import ressources.output_file as rscOf

html_files = ["index.html", "404.html"]

def main(root, outputPath, outputFileName, sub="outils"):
    f = rscOf.def_output_file(outputPath+"\\"+outputFileName)
    if sub != "":
        rootOutputPath = outputPath
        outputPath += "\\" + sub

    for path, subdirs, files in os.walk(root):
        for name in files:
            repo = path[len(root)+1:]
            subdirInd = repo.find("\\")
            if ".md" in name:
                if "temp.md" in name:
                    continue
                res = mtp.main(repo, os.path.join(path, name), htmlDirPath=outputPath, rootPath=root)
                res = change_to_index(repo, name, res, outputPath)
                f.write(res+"\n")
            else:
                for html_file in html_files:
                    if root + "\\" + html_file == os.path.join(path, name):
                        res = mfp.main(os.path.join(path, name), rootOutputPath)
                        f.write(res+"\n")

    f.close()
    try:
        os.remove(outputPath+"\\"+"temp.md")
    except:
        pass
    os.startfile(f.name)

def change_to_index(repo, name, path, outputPath):
    """Changes specific files in index.html."""
    if repo == "WinIBW" and name == "README.md":
        os.replace(path, outputPath + "\\WinIBW\\index.html")
        return outputPath + "\\WinIBW\\index.html"
    else:
        return path

##main(r"D:\transform_github\original_repos", r"D:\transform_github\a_upload", "list_created_files")