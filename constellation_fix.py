from typing import Dict
import os
import re
import tarfile


mapping = {
	'0x04e79a0e': '0x144776d9',
	'0x95c4ad49': '0x04e79a0e',
	'0x2659f41f': '0x95c4ad49',
	'0xf3fb3e48': '0x2659f41f',
	'0xaa2ec1cc': '0xf3fb3e48',
	'0x73146abf': '0xaa2ec1cc',
	'0xb4acd96c': '0x73146abf',
	'0x98db2e1c': '0xb4acd96c',
	'0x68824eed': '0x98db2e1c',
	'0x0d682e7b': '0x68824eed',
	'0xfc82a7df': '0x0d682e7b',
	'0xe983216a': '0xfc82a7df',
}

def strings_read(file: str) -> Dict[str, str]:
	content = {}

	with open(file) as f:
		for line in f.read().splitlines():
			if (m := re.match(r'(0x[0-9a-f]{8}): (.*)', line)):
				addr, text = m.group(1), m.group(2)
				content[addr] = text

	return content

def strings_write(file: str, strings: Dict[str, str]):
	with open(file, 'w') as f:
		for i, (addr, text) in enumerate(strings.items()):
			# f-string expression part cannot include a backslash
			n = '\n'
			f.write(f'{n if i else ""}{addr}: {text}')

def main():
	basedir = os.path.dirname(__file__)
	os.chdir(basedir)

	folder = 'constellation_fix'
	destination = os.path.join(basedir, folder)
	os.makedirs(destination, exist_ok=True)

	for file in os.listdir('.'):
		if not file.endswith('.str') or not os.path.isfile(file):
			continue

		strings = strings_read(file)
		strings_patched = {k: strings[v] for k, v in mapping.items()}
		strings_write(os.path.join(destination, file.replace('_hashed', '_mod')), strings_patched)

	try:
		tar = tarfile.open(folder + '.tar.xz', 'x:xz')
		tar.add(folder)
		tar.close()
	except FileExistsError:
		pass
	
main()