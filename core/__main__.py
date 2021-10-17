import sys
from .test import test_commit, test_packdb

if __name__ == "__main__":
    if sys.argv[1] == 'commit':
        test_commit()
    elif sys.argv[1] == 'pack':
        test_packdb()