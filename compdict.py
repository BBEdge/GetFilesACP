import re

rx_dict = {
	'vf': re.compile(r'(?P<vf>)(?:VF)[^\S+]'),
	'nonvf': re.compile(r'(?P<nonvf>)Non-VF[\s]'),
	'switchshow': re.compile(r'(?P<switchshow>\w+ [\/\w]+switchshow)'),
#	'porterrshow': re.compile(r'(?P<porterrshow>\w+ [\/\w]+porterrshow)'),
	'porterrshow': re.compile(r'(?P<porterrshow>^/fabos/cliexec/porterrshow)'),
	'director': re.compile(r'(?P<director>^Index.(?:Slot))'),
	'switchName': re.compile(r'(?P<switchName>switchName.*)'),
	'switchType': re.compile(r'(?P<switchType>switchType.*)'),
	'switchState': re.compile(r'(?P<switchState>switchState.*)'),
	'switchMode': re.compile(r'(?P<switchMode>switchMode.*)'),
	'switchRole': re.compile(r'(?P<switchRole>switchRole.*)'),
	'switchId': re.compile(r'(?P<switchId>switchId.*)'),
	'switchDomain': re.compile(r'(?P<switchDomain>switchDomain.*)'),
	'switchWwn': re.compile(r'(?P<switchWwn>switchWwn.*)'),
	'FabricName': re.compile(r'(?P<FabricName>Fabric Name.*)'),
	'end': re.compile(r'(?P<END>[*]{2} \w+ \w+ \w+ [*]{2})'),
	'fid': re.compile(r'(?P<FID>(?<=FID\:\s)\d+)')
}

def search_line(line):
    for key, rx in rx_dict.items():
        #		print(key, rx)
        match = rx.search(line)
        if match:
            return key, match
    # if there are no matches
    return None, None