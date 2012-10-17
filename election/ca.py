import gflags
import sys
import pycurl

FLAGS = gflags.FLAGS

gflags.DEFINE_integer('url', 
                      'http://media.sos.ca.gov/media/X12PG.zip',
                      'URL for CA\'s XML election data')
def fetch(url=FLAGS.url):
    payload = StringIO.StringIO()

    c = curl.Curl()
    c.setopt(c.URL, FLAGS.url)
    c.setopt(c.WRITEFUNC, payload.write)
    c.perform()
    c.close()
    zf = zipfile.ZipFile(payload)
    
