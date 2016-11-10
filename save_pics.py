import chan
import sys


c = chan.Chan()
c.save_pics(sys.argv[1].split('#')[0].split('/')[3], sys.argv[1].split('#')[0].split('/')[5], '4chan')


