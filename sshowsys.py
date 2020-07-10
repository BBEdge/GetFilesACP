import re
import gzip


class SshowSys:
    global fid
    def parce_sshowsys(item):
        skip = True

        with gzip.open(item[3], 'rt', encoding='utf8', errors='ignore') as f:
            for line in f:
                uline = line.strip()
                words = uline.split()
                switchshow = re.search(r'(\w+ [\/\w]+switchshow)', uline)
                if skip:
                    if switchshow:
                        skip = False
                else:
                    '''parcing here'''
                    ''' find FID '''
                    fid = re.search(r'FID\:\s(\d+)', uline)
                    if fid:
                        fid = fid.group(1)
                    ''' make Director '''
                    director = re.search(r'Index.(?:Slot)', uline)
                    if director:
                        print(item[0], fid, "Director")

                    '''end parcing'''
                    end = re.search(r'([*]{2} \w+ \w+ \w+ [*]{2})', uline)
                    if end:
                        skip = True