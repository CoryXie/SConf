#!/usr/bin/env python

"""
This is a Python script to copy files with specific name pattern 'pat' from 
'src' directory tree to 'dst' directory tree. For example, you can use this
to copy the Kconfig files in the whole Linux Kernel to 'SConf/linux' so that
can be used to test our sconf.py without going to the original Linux Kernel 
tree. The following is the work flow that I used to debug SConf for Linux 
Kernel. The same procedure can be used to debug other projects. 

	$ git clone https://github.com/CoryXie/SConf.git SConf
	$ cd SConf
	$ python scopy.py ../linux-4.2 ./linux Kconfig*
	$ cd linux
	$ KERNELVERSION=4.2 ARCH=arm64 SRCARCH=arm64 python ../sconf.py Kconfig
	$ cd ..; rm -rf linux # before you want to commit changes for SConf itself

Note that the in the pattern 'Kconfig*', the '*' is to copy also things such 
as Kconfig.debug in the Kernel. In other projects you may have other config 
file naming such as what we recommended "SConfigure", then you should adapt.

Of course, in practice you will use Sconf by copying sconf.py/kconf.py
into the source tree and run sconf.py in the source tree. This script is used
for SConf development purpose.
"""

import os
import sys
import fnmatch
import shutil

# http://blog.ziade.org/2008/07/08/shutilcopytree-small-improvement/
def scopy(src, dst, pat): 
    for root, dirs, files in os.walk(src):
        for file in fnmatch.filter(files, pat):
            srcfile = os.path.join(root, file)
            if os.path.isfile(srcfile) and fnmatch.fnmatch(file, pat):
                dstfile = srcfile.replace(src, dst, 1)
                dstdir = os.path.split(dstfile)[0]
                if not os.path.exists(dstdir):
                    os.makedirs(dstdir)
                print("Copying " + srcfile + " to " + dstfile)
                shutil.copyfile(srcfile, dstfile)
                
if __name__ == "__main__":
    
    if len(sys.argv) <= 3:
        print("Useage: " + sys.argv[0] + " src dst pat")
        sys.exit(0)

    src = sys.argv[1] 
    dst = sys.argv[2]    
    pat = sys.argv[3]
    
    scopy(src, dst, pat)