import re
import gzip


class SshowSys:

    def parce_sshowsys(item):
        skip = True

        with gzip.open(item[3], 'rt', encoding='utf8', errors='ignore') as f:
            for line in f:
                switchshow = re.search(r'(\w+ [\/\w]+switchshow)', line)
                if skip:
                    if switchshow:
                        skip = False
                else:
                    '''parcing here'''
                    print(line)

                    '''end parcing'''
                    end = re.search(r'([*]{2} \w+ \w+ \w+ [*]{2})', line)
                    if end:
                        skip = True