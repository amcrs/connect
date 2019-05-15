import os
import getpass

AMCRS_CONNECT_PATH = os.path.dirname(os.path.abspath(__file__))

def get_3dsmax_startup_script_paths():
    startup_script_paths = []
    directory = os.path.join('C:\\Users', getpass.getuser() ,'AppData\\Local\\Autodesk\\3dsMax')
    if os.path.exists(directory):
        for version in os.listdir(directory):
            startup_script_directory = os.path.join(directory, version, 'ENU\\scripts\\startup')
            if os.path.exists(startup_script_directory):
                startup_script_paths.append(os.path.join(startup_script_directory, 'amcrs_connect.ms'))
    return startup_script_paths

def get_nuke_startup_script_paths():
    startup_script_paths = []
    directory = os.path.join('C:\\Users', getpass.getuser() ,'.nuke')
    if os.path.exists(directory):
        startup_script_paths.append(os.path.join(directory, 'init.py'))
    return startup_script_paths

def install():
    # windows
    if os.name == 'nt':
        # 3dsmax
        for path in get_3dsmax_startup_script_paths():
            with open(path, 'w+') as file:
                file.write('python.ExecuteFile "{0}"'.format(os.path.join(AMCRS_CONNECT_PATH, "app", "3dsmax", 'init.py').replace("\\", "\\\\")))
            print 'created {0}'.format(path)

        # nuke
        for path in get_nuke_startup_script_paths():
            with open(path, 'w+') as file:
                file.write('import nuke\nnuke.pluginAddPath("{0}")'.format(os.path.join(AMCRS_CONNECT_PATH, "app", "nuke").replace("\\", "\\\\")))
            print 'created {0}'.format(path)

    # linux
    if os.name == 'posix':
        pass

    raw_input("AMCRS Connect successfully installed. Press any key to continue...")

if __name__ == '__main__':
    install()