#!/usr/bin/env python3
import argparse
import fnmatch
import gzip
import os
import re
import shutil
import tempfile
import zipfile


# bb43-111-S5cp-202007070226.SSHOW_PORT.txt.gz
# brocade61-S6cp-202007070229.SSHOW_PORT.txt.gz
# mega311_128-10.101.40.76-S6cp-202007070230.SSHOW_PORT.txt.gz


def extract_files(ssfiles, switch, acp, sshowfiles):
    switch = ''.join(switch)
    acp = ''.join(acp)

    for item in sshowfiles:
        result = re.search(r'((?:\S+-)' + acp + '\-\d+\.' + item + '\.\S+)', str(ssfiles))
        if result:
            print(result.group(0))


#    for files in os.listdir(ssdir):
#        if fnmatch.fnmatch(files, '*.zip'):
#            zip = zipfile.ZipFile(ssdir + files)
#            zipfiles.append(files)
#            zip.extractall(tempdir)

#            if values := ''.join(re.findall(r'(?<=\_)\w*(?=\_)', files)):
#                switchname.append(values)
#                switchdir = os.path.join(tempdir, values)

#                '''create dir to extract files from supportsave'''
#                try:
#                    os.mkdir(switchdir)
#                except OSError as e:
#                    print('Creation of the directory %s failed' % switchdir, e)


def main():
    sshowfiles = ['SSHOW_SYS.txt',
                 'SSHOW_PORT.txt',
                 'SSHOW_SERVICE.txt',
                 'SSHOW_FABRIC.txt']

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
#                    datass = re.findall(r'(?<=\_)\d+', files)
#                    fileout = os.path.join(output, ''.join(datass)) + '.out'
#                    print('Waiting for processing supportsave {}'.format(*switch))
                    for ssfiles in f:
                        if re.findall(r'\w*\S*(S\dcp)\-\d+.SSHOW_PORT.txt.gz', ssfiles):
                            acp = re.findall(r'(?<=\-)\S\dcp', ssfiles)
                            extract_files(f, switch, acp, sshowfiles)

            try:
                shutil.rmtree(tempdir)
                print("Temp directory '%s' has been removed successfully." % tempdir)
            except OSError as e:
                print('Delete of the directory %s failed.' % tempdir, e)
                    
    except FileNotFoundError as e:
        print(e)


if __name__ == '__main__':
    main()
