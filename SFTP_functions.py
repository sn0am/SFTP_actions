import paramiko
from stat import S_ISDIR, S_ISREG
import os


#  Form SFTP Connection
def connect_sftp():
    host = ""  # IP or FQDN of the SFTP Server
    username = ""  # SSH Username
    password = ""  # SSH Password
    with paramiko.SSHClient() as client:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)
        sftp = client.open_sftp()
    return sftp


#  Functions to upload all files in local_folder to remote folders.
def recursive_upload(remote_root_dir, remote_folder, local_folder):
    sftp = connect_sftp()

    if remote_folder not in sftp.listdir(path=remote_root_dir):
        print(f"Creating '{remote_folder}' in {remote_root_dir}")
        sftp.mkdir(remote_root_dir + '/' + remote_folder)

    remote_misc_list = sftp.listdir(path=remote_root_dir + '/' + remote_folder)

    for item in os.scandir(local_folder):
        if item.is_file():
            if item.name not in remote_misc_list:
                sftp.put(local_folder + '/' + item.name, remote_root_dir + '/' + remote_folder + '/' + item.name,
                         confirm=True)
                print(f"Copying '{item.name}' to {remote_root_dir}/{remote_folder}")

    for root, dirs, files in os.walk(local_folder):
        for dir in dirs:
            linux_dir = root.replace('\\', '/')
            folder_tree = linux_dir.replace(f'{local_folder}', '')
            if dir not in sftp.listdir(path=remote_root_dir + folder_tree + '/'):
                sftp.mkdir(f'{remote_root_dir}' + f'{folder_tree}' + '/' + f'{dir}')
                print(f'Creating "{dir}" in {remote_root_dir + folder_tree}')

            for item in os.scandir(linux_dir + '/' + dir):
                if item.is_file():
                    if item.name not in sftp.listdir(path=remote_root_dir + folder_tree + '/' + dir):
                        print(f'Copying {item.name} to {remote_root_dir + folder_tree}' + '/' + dir)
                        sftp.put(linux_dir + '/' + dir + '/' + item.name,
                                 remote_root_dir + folder_tree + '/' + dir + '/' + item.name, confirm=True)
    print('No new items to upload at this time.')


#  Function to download all files in the root remote folder.
def remote_root_download(remote_root_dir, local_folder):
    sftp = connect_sftp()

    for file in sftp.listdir_attr(remote_root_dir):
        if not os.path.exists(local_folder):
            os.mkdir(local_folder)
        if S_ISREG(file.st_mode):
            if file.filename not in os.listdir(local_folder):
                print("Downloading: " + file.filename +
                      " from remote directory: " + remote_root_dir)
                sftp.get(remote_root_dir + '/' + file.filename, local_folder + '/' + file.filename)
    print("No new files available to download from the remote root directory.")


#  This function requires the remote variable path, the consistent remote root path, and the local path.
#  This function downloads all files within remote subfolders.
def recursive_download(remote_variable_path, remote_consistent_root_path, local_folder):
    if not os.path.exists(local_folder):
        os.mkdir(local_folder)
    sftp = connect_sftp()
    folders = []
    for folder in sftp.listdir_attr(remote_variable_path):
        if S_ISDIR(folder.st_mode):
            folders.append(folder.filename)
    for folder in folders:
        new_path = os.path.join(remote_variable_path + '/' + folder)
        comparison_path = new_path.replace(remote_consistent_root_path, '')
        remote_item_list = sftp.listdir_attr(path=new_path)
        if not os.path.exists(local_folder + '/' + comparison_path):
            os.mkdir(local_folder + '/' + comparison_path)
        local_save_folder = local_folder + '/' + comparison_path
        for item in remote_item_list:
            if S_ISREG(item.st_mode):
                if item.filename not in os.listdir(local_save_folder):
                    print("Downloading: " + item.filename +
                          f' from remote directory: {new_path}')
                    sftp.get(new_path + '/' + item.filename, local_save_folder + '/' + item.filename)
        recursive_download(new_path, remote_consistent_root_path, local_folder)
