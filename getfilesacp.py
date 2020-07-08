#!/usr/bin/env python3
import argparse
import fnmatch
import gzip
import os
import re
import shutil
import tempfile
import zipfile


def main():
    outlist = []
    dinput = '/tmp/ss'
#    dinput = '/tmp/oper/SS/commander/202005200220'
    output = '/tmp/out'

#    parser = argparse.ArgumentParser(description='Process some integers.')
#    parser.add_argument('-i', '--dinput', help='Directory with supportsave files', required=True)
#    args = parser.parse_args()
#    dinput = args.dinput

    try:
        if os.path.isdir(dinput) and fnmatch.filter(os.listdir(dinput), '*.zip'):
            with tempfile.TemporaryDirectory() as tempdir:
                print('The created temp directory is %s.' % tempdir)

            if not os.path.exists(output):
                try:
                    os.mkdir(output)
                except Exception as e:
                    print('Unable to create directory %s.' % output)

            for files in sorted([f for f in os.listdir(dinput) if os.path.isfile(os.path.join(dinput, f))]):
                if re.match(r'supportsave_\w*\S*_\d+.zip', files):
                    zip = zipfile.ZipFile(os.path.join(dinput, files))
                    f = zipfile.ZipFile.namelist(zip)
                    switch = re.findall(r'(?<=_)\w*\S*(?=_)', files)
                    datass = re.findall(r'(?<=\_)\d+', files)
                    fileout = os.path.join(output, ''.join(datass)) + '.out'
#                    print('Waiting for processing supportsave {}'.format(*switch))
                    for item in f:
#                        print(item)
                        if re.findall(r'\w*\S*(S\dcp)\-\d+.SSHOW_PORT.txt.gz', item):
                            acp = re.findall(r'(?<=\-)\S\dcp', item)
                            print(switch, acp)
#                            pass

            try:
                shutil.rmtree(tempdir)
                print("Temp directory '%s' has been removed successfully." % tempdir)
            except OSError as e:
                print('Delete of the directory %s failed.' % tempdir, e)
                    
    except FileNotFoundError as e:
        print(e)


if __name__ == '__main__':
    main()
