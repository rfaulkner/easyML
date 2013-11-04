
import sys
sys.stdout = sys.stderr     # replace the stdout stream
from horsebeater.web.run import app as application