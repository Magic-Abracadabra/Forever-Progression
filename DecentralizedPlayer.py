# encrypt and decrypt
def encrypt(x):
	return x
def decrypt(x):
	return x
# Decentralized Player
from sys import argv
if len(argv)==2:
	argv = argv[1]
	length = 32
	if not argv.split('.')[-1].startswith('dc'):
		with open(argv, 'rb') as data:
			data = data.read()
		argv = argv.split('.')
		argv = '.'.join(argv[:-1])+'.dc'+argv[-1]
		with open(argv, 'wb') as file:
			file.write(encrypt(int.to_bytes(0, length, 'big', signed=False))+data)
		del data, file
	if argv.split('.')[-1].startswith('dc'):
		with open(argv, 'rb') as file:
			file = file.read()
		media = file[length:]
		breakpoint = int.from_bytes(decrypt(file[:length]), 'big', signed=False)
		del file
		file = argv.split('.dc')
		file = '.dc'.join(file[:-1])+'.'+file[-1]
		with open(file, 'wb') as data:
			data.write(media)
		try:
			import vlc
		except:
			from pip import main
			main(['install', 'python-vlc'])
			import vlc
		player = vlc.MediaPlayer(file)
		del file, data
		player.play()
		import mmap, ctypes
		memmove_local = ctypes.memmove
		while player.get_time() < 0:
			pass
		player.set_time(breakpoint)
		input('Press Enter to Stop')
		with open(argv, 'r+b') as file:
			with mmap.mmap(file.fileno(), length) as mm:
				base_addr = ctypes.addressof(ctypes.c_char.from_buffer(mm))
				memmove_local(base_addr, encrypt(player.get_time().to_bytes(length, 'big', signed=False)), length)
