import chan
import sys

if len(sys.argv) != 2:
	raise Exception('too few or too many args. get ur shit together.')
c = chan.Chan()
split = sys.argv[1].split('#')[0].split('/')
if len(split) < 6:
	raise Exception('malformed url')
board = split[3]
post_id = split[5]
directory = '4chan' #default dir to save in
c.save_pics(board, post_id, directory)
