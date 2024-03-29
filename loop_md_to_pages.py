# -*- coding: utf-8 -*-

# USe python_param/README to launch the script

import os
import shutil
# Internal imports
import md_to_pages as mtp
import maj_fixed_pages as mfp
import python_ressources.output_file as rscOf

html_files = ["index.html", "404.html", r"special-pages\control-tools.html"] # Apply template to the these HTML files
raw_files = [r"ub-svs\dumas\generateur-notice.html",
            r"ub-svs\dumas\dumas_indexes.json",
            r"ub-svs\dumas\generateur_erreur_liste.json",
            r"ub-svs\dumas\aideDepot_addCopyHtml.js",
            r"ub-svs\dumas.html"] # Import those files unedited
readme_to_index = [r"WinIBW\README.md",
                r"ub-svs\README.md",
                r"ub-svs\dumas\README.md"] # README that should be index.html


def main(root, outputPath, outputFileName, sub="outils"):
    """Loops through a directory and prepares files for my GitHub Pages.

    Arguments (pathes are without \ at the end):
        root {rString} -- root directory
        outputPath {rString} -- output root directory
        outputFileName {string} -- name of the text files that will contain
    all the created files (located at the root of outputPath).
        sub {string} -- name of the subdirectory to add to outputPath for all
    non fixed files."""
    root = MY_PATH + "\\" + root
    outputPath = MY_PATH + "\\" + outputPath
    f = rscOf.def_output_file(outputPath+"\\"+outputFileName)
    if sub != "":
        rootOutputPath = outputPath
        outputPath += "\\" + sub
    outputPath += "\\" + repo

    for path, subdirs, files in os.walk(root):
        for name in files:
            print(name)
            if ".md" in name:
                if "temp.md" in name:
                    continue
                res = mtp.main(repo, os.path.join(path, name), htmlDirPath=outputPath, rootPath=root)
                res = change_to_index(os.path.join(path, name), res, outputPath)
                f.write(res+"\n")
            elif ".png" in name and not "Louise\\" in path:
                os.makedirs(outputPath+path[len(root):] , exist_ok=True)
                shutil.copyfile(os.path.join(path, name), outputPath+path[len(root):]+"\\"+name)
                f.write(outputPath+path[len(root):]+"\\"+name + "\n")
            else:
                for html_file in html_files: # Applies the template to HTML files
                    if root + "\\" + html_file == os.path.join(path, name):
                        res = mfp.main(os.path.join(path, name), rootOutputPath)
                        f.write(res+"\n")
                for raw_file in raw_files: # Import files unedited
                    if root + "\\" + raw_file == os.path.join(path, name):
                        os.makedirs(os.path.dirname(outputPath + "\\" + raw_file), exist_ok=True)
                        shutil.copyfile(os.path.join(path, name), outputPath + "\\" + raw_file)
                        f.write(outputPath + "\\" + raw_file + "\n")

    f.close()
    try:
        os.remove(outputPath+"\\"+"temp.md")
    except:
        pass
    os.startfile(f.name)

def change_to_index(originalFilePath, path, outputPath):
    """Changes specific files in index.html."""
    for readme in readme_to_index:
        if originalFilePath.endswith(readme):
            readme = readme[:-9] + "index.html"
            os.makedirs(outputPath + "\\" + readme[:readme.rfind("\\")], exist_ok=True)
            os.replace(path, outputPath + "\\" + readme)
            return outputPath + "\\" + readme
    return path


repo = input("Nom du repo a transformer : ")
main(repo, r"\GitHub_Pages\Alban-Peyrat.github.io", "list_created_files")