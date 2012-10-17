import gflags
import sys
import pycurl
import StringIO
import election.utils

FLAGS = gflags.FLAGS

gflags.DEFINE_string('url', 
                      'http://media.sos.ca.gov/media/X12PG.zip',
                      'URL for CA\'s XML election data')
def fetch(url=FLAGS.url):
    payload = StringIO.StringIO()

    c = pycurl.Curl()
    c.setopt(c.URL, FLAGS.url)
    c.setopt(c.WRITEFUNCTION, payload.write)
    c.perform()
    c.close()
    return election.utils.ZipDict(payload)
    
