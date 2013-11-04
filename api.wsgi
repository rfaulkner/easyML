
import sys
sys.stdout = sys.stderr     # replace the stdout stream
from versus.web.run import app as application