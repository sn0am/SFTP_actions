from SFTP_functions import *
import time

local_folder = ''  # Address for local folder.
remote_root_dir = ''  # Address for root SFTP folder.
remote_folder = 'Misc'  # Name of remote folder to store all local folder root files.

recursive_upload(remote_root_dir, remote_folder, local_folder)  #  Upload all files from local folder.

time.sleep(10)  # Sleep timer added so console output can be read.
