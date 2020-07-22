# GetFilesACP
Get files from active CP


                fid = re.search(r'FID\:\s(\d+)', uline)
                if fid:
                    fid = fid.group(1)

                ports = re.search(r'\d+\s+\d+\s+[\w]{6}|\d+\s+\d+\s+\-{6}', uline)
                uline = line.strip()
                words = uline.split()
                if ports:
                    words[1] = '/'.join(words[1:3])
                    words[7] = ' '.join(str(e) for e in words[7:])
                    print(switchname, date, words[0], words[1], words[3], words[5], words[6], words[7])
                    
                    
                    
                    
                    
                    
            ''' porterrshow '''
            if skip:
                if key == 'porterrshow':
                    skip = False
            else:
                header = 'ftx frx  date pindx slot/port address speed status proto'.split()
#                print('{:12s} {:12s} {:12s} {:12s} {:8s} {:8s} {:11s} {:14s}'.format(*header))
#                SshowSys.parse_switchshow(switchname, date, header, uline)
#                    words = SshowSys.parse_switchshow(director, switchname, date, uline)
#                    result.append(words)

                '''end parsing'''
                if key == 'end':
                    skip = True
                    
                    
                    
                    
                    
                    
    with gzip.open(sshowfiles, 'rt', encoding='utf8', errors='ignore') as f:
        for line in f:
            uline = line.strip()
            key, match = search_line(uline)

            ''' switchshow '''
            if skip:
                if key == 'start_switch':
                    skip = False
            else:
                fid = re.search(r'FID\:\s(\d+)', uline)
                if fid:
                    fid = fid.group(1)

                if 'Speed' in uline:
                    header = uline
                    director = re.search(r'Index.(?:Slot)', header)
                    if director:
                        header = 'switch date pindx slot/port address speed status proto'.split()
#                        print('{:12s} {:12s} {:12s} {:12s} {:8s} {:8s} {:11s} {:14s}'.format(*header))
                    else:
                        header = 'switch date pindx port address speed status proto'.split()
#                        print('{:12s} {:12s} {:12s} {:12s} {:8s} {:8s} {:11s} {:14s}'.format(*header))

#                SshowSys.parse_switchshow(switchname, date, header, uline)
                words = SshowSys.parse_switchshow(director, switchname, date, uline)
#                print(words)
#                result.append(words)

                '''end parsing'''
                if key == 'end':
                    skip = True

            ''' porterrshow '''
            if skip:
                if key == 'porterrshow':
                    skip = False
            else:
                SshowSys.parse_porterror(uline)
                '''end parsing'''
                if key == 'end':
                    skip = True
                    
                    
                    
                errors = re.search(r'.{1}(?=\d*:)', uline)
                if errors:
                    print(words)
                    
                    
                    
                    
                    
                    
                    
            for line in f:
                uline = line.strip()
                words = uline.split()
                key, match = search_line(uline)
                if skip:
                    #                if key == 'director':
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
        #                    print('{:6s} {:7s} {:9s} {:6s} {:12s} {}'.format(*words))
        #                            words[0], words[1], words[2], words[3], words[4], words[5]))
















        with gzip.open(sshowfiles, 'rt', encoding='utf8', errors='ignore') as f:
        words = uline.split()
            if director:
                ports = re.search(r'\d+\s+\d+\s+[\w]{6}|\d+\s+\d+\s+\-{6}', uline)
                if ports:
                    words[1] = '/'.join(words[1:3])
                    del(words[2])
                    del(words[3])
                    words[5] = ' '.join(str(e) for e in words[5:])
                    del(words[6:])
    #                print('{:12s} {:12s} {:12s} {:12s} {:8s} {:8s} {:11s} {:14s}'.format(
#                      switchname, date, words[0], words[1], words[3], words[5], words[6], words[7])
                    switchshow.append(words)
                    return switchshow
            else:
                ports = re.search(r'\d+\s+\d+\s+[\w]{6}|\d+\s+\d+\s+\-{6}', uline)
                if ports:
                    words[1] = '/'.join(words[1:3])
                    del(words[2])
                    del(words[3])
                    words[6] = ' '.join(str(e) for e in words[6:])
                    del(words[7:])
#                   print('{:12s} {:12s} {:12s} {:12s} {:8s} {:8s} {:11s} {:14s}'.format(
#                      switchname, date, words[0], words[1], words[3], words[5], words[6], words[7]))
                    results.append(words)
                    return results