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
# (?:\S+\-)\S\dcp\-\d+\.\S+
# ((?:\S+\-)\S\dcp\-\d+\.\w+(\.\w+){2})
# bb43-111-S4cp-202007070222.SSHOW_SYS.txt.gz
# bb43-111-S5cp-202007070223.SSHOW_SYS.txt.gz

def extract_files(zip, switch, datass, ssfiles, tempdir, acp, sshowfiles):
    switch = ''.join(switch)
    datass = ''.join(datass)
    acp = ''.join(acp)
    ssfiles = ' '.join(ssfiles)
    gzfiles = []

    for item in sshowfiles:
        match = re.search(r'((?:\S+-)' + acp + '\-\d+\.' + item + '\.gz)', ssfiles)
        if match:
            zip.extract(match.group(0), tempdir)
            gz = os.path.join(tempdir, match.group(0))
            words = (switch, datass, item, gz)
            gzfiles.append(words)

    return gzfiles


def parce_sshowsys(item):
    skip = True
    count = 0

    with gzip.open(item[3], 'rt', encoding='utf8', errors='ignore') as f:
        for line in f:
            key, match = search_line(line)
            if skip:
                if key == 'start_switch':
                    skip = False
            else:
                count = count + 1
                print(count)
                if key == 'end':
                    skip = True

        #print(line)




def main():
    sshowfiles = ['SSHOW_SYS.txt',
                 'SSHOW_PORT.txt',
                 'SSHOW_SERVICE.txt',
                 'SSHOW_FABRIC.txt']
    dinput = '/tmp/ss'
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

            # get archive supportsave files
            for files in sorted([f for f in os.listdir(dinput) if os.path.isfile(os.path.join(dinput, f))]):
                if re.match(r'supportsave_\w*\S*_\d+.zip', files):
                    zip = zipfile.ZipFile(os.path.join(dinput, files))
                    f = zipfile.ZipFile.namelist(zip)
                    switch = re.findall(r'(?<=_)\w*\S*(?=_)', files) # get switchname from file name
                    datass = re.findall(r'(?<=\_)\d+', files) # get data from file name
#                    fileout = os.path.join(output, ''.join(datass)) + '.out'
#                    print('Waiting for processing supportsave {}'.format(*switch))
                    for ssfiles in f:
                        if re.findall(r'\w*\S*(S\dcp)\-\d+.SSHOW_PORT.txt.gz', ssfiles):
                            acp = re.findall(r'(?<=\-)\S\dcp', ssfiles)
                            gzfiles = extract_files(zip, switch, datass, f, tempdir, acp, sshowfiles)

                    for item in gzfiles:
                        if item[2] in sshowfiles[0]:
                            '''parce SSHOW_SYS'''
                            parce_sshowsys(item)

            try:
                shutil.rmtree(tempdir)
                print("Temp directory '%s' has been removed successfully." % tempdir)
            except OSError as e:
                print('Delete of the directory %s failed.' % tempdir, e)
                    
    except FileNotFoundError as e:
        print(e)


if __name__ == '__main__':
    main()
