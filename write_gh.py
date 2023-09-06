"""This script uploads the contents of the working directory to Google Drive

Requirements:
1. A `credentials.json` file must be present in the working directory. This file contains the credentials needed to authenticate to the Google Drive API. This file can be generated from the Google Cloud Console.
2. The first time the script is run, it will prompt the user for permission to access Google Drive. Once permission is granted, it will generate a `token.json` file. This file should be kept private and not shared.
"""
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def parse_gitignore(directory_path='.'):
    """This function uses .gitignore file to determine which files should be uploaded to Google Drive."""
    gitignore_path = os.path.join(directory_path, '.gitignore')
    if not os.path.exists(gitignore_path):
        print(f"Could not find .gitignore file in {directory_path}. Skipping parsing .gitignore.")
        return []

    with open(gitignore_path, 'r') as f:
        # Read and sanitize each line: remove spaces and ignore comments
        return [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]

def should_upload(item_path, gitignore_rules):
    for rule in gitignore_rules:
        if rule in item_path:
            return False
    return True

def authenticate_drive():
    """Authenticate to Google Drive API"""
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = None

    # Load credentials from the file
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')

    # If there are no (valid) credentials available, create token.json
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)

def create_or_get_drive_folder(drive_service, folder_name, parent_folder_id):
    """Create a folder in Google Drive or return the ID of an existing folder with the same name"""
    folder_mime_type = "application/vnd.google-apps.folder"
    
    existing_folder_id = find_item_in_drive(drive_service, folder_name, parent_folder_id, folder_mime_type)
    if existing_folder_id:
        return existing_folder_id
    
    folder_metadata = {
        'name': folder_name,
        'mimeType': folder_mime_type
    }
    if parent_folder_id:
        folder_metadata['parents'] = [parent_folder_id]
    
    folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
    return folder.get('id')

def find_item_in_drive(drive_service, item_name, parent_folder_id, mime_type=None):
    """Find an item in Google Drive by name and parent folder ID"""
    query = f"name = '{item_name}' and '{parent_folder_id}' in parents and trashed = false"
    if mime_type:
        query += f" and mimeType = '{mime_type}'"
    
    results = drive_service.files().list(q=query, fields="files(id)").execute()
    items = results.get('files', [])
    return items[0]['id'] if items else None


def upload_directory_to_drive(drive_service, directory_path='.', parent_folder_id=None, gitignore_rules=None):
    """Upload a directory to Google Drive"""
    for item_name in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item_name)

        # Check if the item should be uploaded based on .gitignore rules
        if not should_upload(item_path, gitignore_rules) and not should_upload(item_name, gitignore_rules):
            print(f"Skipping {item_path} due to .gitignore rules.")
            continue

        # Check if the item is a directory and upload its contents
        if os.path.isdir(item_path):
            folder_id = create_or_get_drive_folder(drive_service, item_name, parent_folder_id)
            upload_directory_to_drive(drive_service, item_path, folder_id, gitignore_rules)
        
        # Upload the files
        else:
            existing_file_id = find_item_in_drive(drive_service, item_name, parent_folder_id)

            media = MediaFileUpload(item_path)
            file_metadata = {
                'name': item_name,
            }

            if existing_file_id:
                # Update the existing file
                print(f"Updating {item_path} on Google Drive...")
                drive_service.files().update(fileId=existing_file_id, body=file_metadata, media_body=media).execute()
            else:
                # Upload a new file
                print(f"Uploading {item_path} to Google Drive...")
                if parent_folder_id:
                    file_metadata['parents'] = [parent_folder_id]
                drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

def main():
    # Initialize the Drive API 
    service = authenticate_drive()

    # Set the target parent directory in Google Drive
    drive_folder_id = '1tgpoGv69m_5rr5lGFDEGkeZWN716HP-0'
    
    # Upload the working directory and its contents
    gitignore_rules = parse_gitignore('.')
    upload_directory_to_drive(service, '.', drive_folder_id, gitignore_rules)

if __name__ == '__main__':
    main()