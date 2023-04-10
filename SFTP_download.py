from SFTP_functions import *
import time

remote_root_dir = ''  # Address for root SFTP folder.
local_folder = ''  # Address for local folder.

remote_root_download(remote_root_dir, local_folder)  # Only download files placed in the remote root directory.

recursive_download(remote_root_dir, remote_root_dir, local_folder)  # Download all files within folders and subfolders within the remote root directory.

print("No new files available to download from the remote subdirectories.")

time.sleep(10)  # Sleep timer added so console output can be read.
