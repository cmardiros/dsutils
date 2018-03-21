import time
from time import gmtime, strftime
import subprocess


class Timer(object):

    def __init__(self,
                 label,
                 prefix='',
                 say=False,
                 log=True):
        self.label = label
        self.prefix = prefix
        self.log = log
        self.say = say

    def __enter__(self):
        now = strftime('%Y-%m-%d %H:%M:%S', gmtime())
        msg = "\n_ Starting -- {0} @ {1}".format(self.label, now)
        if self.log:
            print('{}{}'.format(self.prefix, msg))
        self.start = time.time()
        if self.say:
            cmd_say(msg)
        return self

    def __exit__(self, *exc):
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
        self.interval = time.time() - self.start
        msg = "_ Finished -- {} -- in {:.1f}secs"
        msg = msg.format(self.label, self.interval)
        msg += " @ {0}\n".format(now)
        if self.log:
            print('{}{}'.format(self.prefix, msg))
        if self.say:
            cmd_say(msg)
        return False


def cmd_say(msg):
    subprocess.call("say '{}'".format(msg), shell=True)
