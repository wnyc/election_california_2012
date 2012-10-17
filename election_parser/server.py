import election_parser.ca
import gflags
import paramiko 
from StringIO import StringIO
import itertools
import os.path
import Queue
import os
import threading
import scpclient
import contextlib

"""fetch_parse_and_upload_election_data

This process fetches data from the CA election server (or optionally
the fake_election_server process included as part of this package),
parases the data into NYPR's much easier to understand format and
writes the data out someplace.  

The user may elect for the data to be written to one or more of Amazon
S3, SSH or the local file system.  If none is selected, the "all.json"
file is written to stdout.

The files written are: 

all.json - A json file including all of the data
...
*.xml - The original california XML files, unzipped.
*.zip - The original california XML files as zipped
"""
FLAGS = gflags.FLAGS

gflags.DEFINE_multistring('ssh', [], 'SSH targets to write to')
gflags.DEFINE_multistring('local', [], 'Local file system paths to write to')
gflags.DEFINE_multistring('s3', [], 'S3 targets to write to')


class Writer:
    def __init__(self, path):
        self.path = path

    def absolute_path(self, filename):
        return os.path.join(self.path, filename)

    def run(self, channel):
        name, data = channel.get()
        while not (name is None and data is None):
            self.write_file(name, data)
            name, data = channel.get()

class LocalWriter(Writer):
    def write_file(self, name, data):
        f = open(self.absolute_path(name), "w+")
        print type(data)
        f.write(data)
        f.close()

    

class SSHWriter(Writer):
    
    def __init__(self, path):
        Writer.__init__(self, path)
        self.target, self.path = self.path.split(':', 1)
        self.username, self.hostname = self.target.split('@', 1)
        self.ssh_client = paramiko.SSHClient()
        print "Hostname: ", self.hostname
        print "Username: ", self.username
        print "Path    : ", self.path
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(self.hostname, username=self.username, port=22)

    def write_file(self, name, data):
        name = name.strip()
        with contextlib.closing(scpclient.Write(self.ssh_client.get_transport(), self.absolute_path(''))) as scp:
            scp.send(StringIO(data), name, '0644', len(data))


class AggregateWriter:
    def __init__(self, *children):
        children = itertools.chain(*map(iter, children))
        self.channels = []
        self.children = []
        for child in children:
            que = Queue.Queue(maxsize=0)
            thread = threading.Thread(target=child.run,
                             args=[que])
            self.children.append(thread)
            thread.start()
            self.channels.append(que)


    def write_file(self, name, data):
        if hasattr(data, 'read'):
            data = data.read()
        for channel in self.channels:
            channel.put((name, data))
    
    def close(self):
        self.write_file(None, None)
        for child in self.children:
            child.join()


def main(argv, stdout, doc=__doc__):
    try:
        argv = FLAGS(argv[1:])
    except gflags.FlagsError,e:
        print >>sys.stderr, "Usage: %s %s ARGS\\n%s" % (doc, sys.argv[0], FLAGS)
        return 1 

    if FLAGS.s3:
        print >>sys.stderr, "No S3 support yet, we suck" 
        return 1

    data, original, name = election.ca.fetch()

    
    if not FLAGS.ssh and not FLAGS.s3 and not FLAGS.local:
        # This really should be all.json.  And yes, we'll need a
        # special all.json only call here.
        print str(data.keys())
        return 0

    writer = AggregateWriter(
        (LocalWriter(path) for path in FLAGS.local),
        (SSHWriter(path) for path in FLAGS.ssh))

    writer.write_file(name, original)
    for key in data:
        writer.write_file(key, data[key])

    # Insert parser here.  Yes, its better to start sending stuff that
    # doesn't require parsing before we start the laborous process of parsing.


    parsed_results = {}

    for key in parsed_results:
        writer.write_file(key, parsed_results[key])

    writer.close()
    
