import os
import getpass
from install import get_3dsmax_startup_script_paths, get_nuke_startup_script_paths

def uninstall():
    # windows
    if os.name == 'nt':
        # 3dsmax
        for path in get_3dsmax_startup_script_paths():
            if os.path.exists(path):
                os.remove(path)
                print 'deleted {0}'.format(path)

        # nuke
        for path in get_nuke_startup_script_paths():
            if os.path.exists(path):
                os.remove(path)
                print 'deleted {0}'.format(path)

    # linux
    if os.name == 'posix':
        pass

    raw_input("AMCRS Connect successfully uninstalled. Press any key to continue...")

if __name__ == '__main__':
    uninstall()