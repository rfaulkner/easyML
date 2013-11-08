
import sys
sys.stdout = sys.stderr     # replace the stdout stream
from test.web.run import app as application