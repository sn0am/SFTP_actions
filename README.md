# SFTP_actions

SFTP_upload.py can be used to recursively upload all files and folders within a local directory to a remote directory. Folder structure is kept the same between local and remote files for the most part. 

*Files that exist within the root local folder are placed in the 'Misc' remote folder, this name can be changed.
*Files that exist within subfolders in the root local folder are placed within folders of the same name on the remote folder.
*Only files that don't exist on the remote folder are uploaded, if no new files are detected in the local folder, upload is skipped.


SFTP_download.py can be used to recursively download all files and folders from a given remote folder.
Only files that don't exist within a local folder are downloaded. If no new files are detected, download is skipped.

*These scripts were hastily written for home use, so the SFTP authentication function is not secure. If using this script for any other use case, I would recommend updating the SFTP authentication function.
