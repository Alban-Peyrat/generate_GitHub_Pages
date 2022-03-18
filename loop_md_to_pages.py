# -*- coding: utf-8 -*-

import os
import md_to_pages as mtp
import ressources.output_file as rscOf


def main(root, outputPath, outputFileName):
    f = rscOf.def_output_file(outputPath+"\\"+outputFileName)

    for path, subdirs, files in os.walk(root):
        for name in files:
            repo = path[len(root)+1:]
            subdirInd = repo.find("\\")
            if ".md" in name:
                if "temp.md" in name:
                    continue
                res = mtp.main(repo, os.path.join(path, name), htmlDirPath=outputPath, rootPath=root)
                f.write(res+"\n")

    f.close()
    os.remove(outputPath+"\\"+"temp.md")
    os.startfile(f.name)

##def change_to_index(res)

##main(r"D:\transform_github\original_repos", r"D:\transform_github\a_upload", "list_created_files")