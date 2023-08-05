from pydrive2.drive import GoogleDrive
from pydrive2.auth import GoogleAuth
import os
import hashlib


ERROR_BYPASS_FILES = ["Organize.json", "Organize.lnk"]


def upload_files(drive, local_path, remote_folder_id=None):
    for x in os.listdir(local_path):
        file_path = os.path.join(local_path, x)
        if os.path.isdir(file_path):
            upload_folders(drive, x, file_path, remote_folder_id)
        elif os.path.isfile(file_path):
            upload_file(drive, x, file_path, remote_folder_id)


def upload_folders(drive, folder_name, folder_path, parent_folder_id=None):
    folder_metadata = {
        "title": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if parent_folder_id:
        folder_metadata["parents"] = [
            {"kind": "drive#fileLink", "id": parent_folder_id}
        ]
    remote_folder = find_file_by_name(drive, folder_name, parent_folder_id)
    if not remote_folder:
        remote_folder = drive.CreateFile(folder_metadata)
        remote_folder.Upload()
    upload_files(drive, folder_path, remote_folder["id"])


def upload_file(drive, file_name, file_path, parent_folder_id=None):
    remote_file = find_file_by_name(drive, file_name, parent_folder_id)
    if remote_file:
        if not is_file_content_same(remote_file, file_path):
            try:
                action_notice(
                    remote_file,
                    file_path,
                    "Overwritten (Different): ",
                    file_name,
                )
            except Exception as e:
                print(
                    f"Error overwriting {os.path.join(file_path, file_name)}: {str(e)}"
                )
            finally:
                remote_file = None
    elif file_name not in ERROR_BYPASS_FILES:
        try:
            f = drive.CreateFile(
                {
                    "title": file_name,
                    "parents": [{"kind": "drive#fileLink", "id": parent_folder_id}],
                }
            )
            action_notice(f, file_path, "Uploaded: ", file_name)
        except Exception as e:
            print(f"Error uploading {os.path.join(file_path, file_name)}: {str(e)}")
        finally:
            f = None


def action_notice(drive, file_path, action, file_name):
    drive.SetContentFile(file_path)
    drive.Upload()
    print(f"{action}{os.path.join(file_path, file_name)}")


def find_file_by_name(drive, filename, parent_id=None):
    query = f"title = '{filename}' and trashed = false"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    file_list = drive.ListFile({"q": query}).GetList()
    return file_list[0] if file_list else None


def is_file_content_same(remote_file, local_file_path):
    remote_md5_checksum = remote_file["md5Checksum"]
    with open(local_file_path, "rb") as local_file:
        local_md5_checksum = hashlib.md5(local_file.read()).hexdigest()
    return remote_md5_checksum == local_md5_checksum


def main():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_directory)
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("credentials.json")
    gauth.SaveCredentialsFile("credentials.json")
    drive = GoogleDrive(gauth)

    local_path = r"O:\Download"
    upload_files(drive, local_path)


if __name__ == "__main__":
    main()
