import re
import gzip
from compdict import search_line


class SshowSys:

    def parse_alias(self, datess, sshowfile):
        alias = []

        with gzip.open(sshowfile, 'rt', encoding='utf8', errors='ignore') as f:
            for line in f:
                match = re.search(r'alias.(\w*):(\S*)', line)
                if match:
                    words = (match.group(1) + ' ' + match.group(2).replace(';', ' ')).split()
                    alias.append(words)

        return alias


    def parse_switchshow(self, datess, sshowfile):
        skip = True
        switchshow = []
        director = ''

        with gzip.open(sshowfile, 'rt', encoding='utf8', errors='ignore') as f:
            for line in f:
                uline = line.strip()
                words = uline.split()
                key, match = search_line(uline)
                if skip:
                    if key == 'switchshow':
                        skip = False
                else:
                    ports = re.search(r'\d+\s+\d+\s+[\w]{6}|\d+\s+\d+\s+\-{6}', uline)
                    if ports:
                        words[1] = '/'.join(words[1:3])
                        del (words[2])
                        del (words[3])
                        words[5] = ' '.join(str(e) for e in words[5:])
                        del (words[6:])
#                        print(words)
                    #                    print('{:6s} {:7s} {:9s} {:6s} {:12s} {}'.format(*words))
                    #                            words[0], words[1], words[2], words[3], words[4], words[5]))
                        switchshow.append(words)

                    '''end parsing'''
                    if key == 'end':
                        skip = True

        return switchshow


    def parse_porterrshow(self, datess, sshowfile):
        skip = True
        porterrshow = []

        with gzip.open(sshowfile, 'rt', encoding='utf8', errors='ignore') as f:
            for line in f:
                uline = line.strip()
                words = uline.split()
                key, match = search_line(uline)
                if skip:
                    if key == 'porterrshow':
                        skip = False
                else:
                    ports = re.search(r' \d{1,3}|^\d{1,3}:', uline)
                    if ports:
                        porterrshow.append(words)
#                        print(words)

                    '''end parsing'''
                    if key == 'end':
                        skip = True

        return porterrshow


    def portinfo(self, switchshow, porterrshow):
        pass