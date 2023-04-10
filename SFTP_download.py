from SFTP_functions import *
import time

remote_root_dir = ''  # Address for root SFTP folder.
local_folder = ''  # Address for local folder.

remote_root_download(remote_root_dir, local_folder)

recursive_download(remote_root_dir, remote_root_dir, local_folder)

print("No new files available to download from the remote subdirectories.")

time.sleep(10)
