import pycurl
import StringIO
import election_parser.utils
import gflags

FLAGS = gflags.FLAGS

gflags.DEFINE_string('input', 
                      'http://media.sos.ca.gov/media/X12PG.zip',
                      'URL for CA\'s XML election data')

class GenericLoader:
    def fetch(url=FLAGS.input):
        payload = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.WRITEFUNCTION, payload.write)
        c.perform()
        c.close()
        return election_parser.utils.ZipDict(payload), payload, os.path.basename(url)
    
