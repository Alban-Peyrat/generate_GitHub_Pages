# -*- coding: utf-8 -*-

import os
import md_to_pages as mtp
import ressources.output_file as rscOf


def main(root, outputFileName):
    f = rscOf.def_output_file(root+"\\"+outputFileName)

    for path, subdirs, files in os.walk(root):
        for name in files:
            repo = path[len(root)+1:]
            subdirInd = repo.find("\\")
            if ".md" in name:
                if "temp.md" in name:
                    continue
                print(os.path.join(path, name))
                res = mtp.main(repo, os.path.join(path, name))
                f.write(res+"\n")

    f.close()
    os.startfile(f.name)
