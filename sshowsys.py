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


    def parse_switchshow(self, sshowfile):
        skip = True
        switchshow = []
        alias = self
        director = ''

        with gzip.open(sshowfile, 'rt', encoding='utf8', errors='ignore') as f:
            for line in f:
                uline = line.strip()
                words = uline.split()
                if skip:
                    key = re.search(r'========================', uline)
                    if key:
                        skip = False
                else:
                    ports = re.search(r'\d+\s+\d+\s+[\w]{6}|\d+\s+\d+\s+\-{6}', uline)
                    if ports:
#                        words[1] = '/'.join(words[1:3])
#                        del (words[2])
#                        del (words[3])
                        del (words[4])
                        speed = re.findall(r'\d{1,2}', words[4])
                        words [4] = ''.join(speed)
                        words[6] = ' '.join(str(e) for e in words[6:])
                        del (words[7:])

#                        fport = re.findall(r'F-Port ((?:[0-9a-fA-F]:?){16})', words[5])
#                        for item in alias:
#                            if fport.group(0) == item[1]:
#                                words[5] = item[0]

#                        print(words)
                    #                    print('{:6s} {:7s} {:9s} {:6s} {:12s} {}'.format(*words))
                    #                            words[0], words[1], words[2], words[3], words[4], words[5]))
                        switchshow.append(words)
                    else:
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
                    key = re.search(r'g_eof', uline)
                    if key:
                        skip = False
                else:
                    ports = re.search(r' \d{1,3}|^\d{1,3}:', uline)
                    if ports:
                        words[0] = ''.join(re.findall(r'\d{1,3}', words[0]))

                        for ele in words:

                            ''' kilo '''
                            match = re.search(r'(\d{1,3}.\d{1})(?=k)', uline)
                            index = words.index(match.group(1))
                            if match:
                                words = int(float(''.join(match.group(1))) * 1000)
                                print(index, words)

#                        item = SshowSys.count_porterrs(words[1:])
#                        print(item)
#                        porterrshow.append(words)
#                        print(words)
                    else:
                        skip = True

#        return porterrshow


    def portinfo(self, switchshow, porterrshow):
        alias = self

        for p, e in switchshow + porterrshow:
            print(p, e)
#        print([i for i in switchshow + porterrshow if i in switchshow or i in porterrshow])
#        for ele in list:
#            print(ele)

        pass


    def count_porterrs(self):
        words = self

        for ele in words:
            if re.match(r'\d{1,3}.\d{1}(?=k)|\d{1,3}.\d{1}(?=g)|\d{1,3}.\d{1}(?=m)', ele):

                ''' kilo '''
                match = re.findall(r'\d{1,3}.\d{1}(?=k)', ele)
                if match:
                    words = int(float(''.join(match)) * 1000)
                    return words

                ''' mega '''
                match = re.findall(r'\d{1,3}.\d{1}(?=m)', ele)
                if match:
                    words = int(float(''.join(match)) * 1000000)
                    return words

                ''' giga '''
                match = re.findall(r'\d{1,3}.\d{1}(?=g)', ele)
                if match:
                    words = int(float(''.join(match)) * 1000000000)
                    return words
            else:
                return self