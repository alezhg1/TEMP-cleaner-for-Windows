#!/usr/bin/env python3
"""
Windows Temporary Files Cleanup Utility
Removes files and folders from Temp folder with error handling
"""

import os
import shutil
from pathlib import Path


def get_temp_directory():
    """Get the path to the Temp folder of the current user"""
    username = os.getlogin()
    temp_path = f'C:/Users/{username}/AppData/Local/Temp'
    return temp_path


def is_protected_folder(folder_name):
    """Check if a folder is protected from deletion"""
    protected = ['chocolatey', 'system', 'windows']
    return any(protected_name in folder_name.lower() for protected_name in protected)


def extract_item_name(full_path):
    """Extract file/folder name from full path"""
    return os.path.basename(full_path)


def delete_file(file_path, item_name):
    """Delete file with error handling"""
    try:
        os.unlink(file_path)
        print(f'✓ File deleted: {item_name}')
        return True
    except PermissionError:
        print(f'✗ Access denied: {item_name}')
        return False
    except Exception as e:
        print(f'✗ Error deleting {item_name}: {str(e)}')
        return False


def delete_directory(dir_path, item_name):
    """Delete folder with error handling"""
    if is_protected_folder(item_name):
        print(f'⊘ Folder is protected, skipping: {item_name}')
        return False
    
    try:
        shutil.rmtree(dir_path)
        print(f'✓ Folder deleted: {item_name}')
        return True
    except PermissionError:
        print(f'✗ Access denied: {item_name}')
        return False
    except Exception as e:
        print(f'✗ Error deleting {item_name}: {str(e)}')
        return False


def cleanup_temp_folder(temp_directory):
    """Main function to clean temporary folder"""
    files_removed = 0
    folders_removed = 0
    
    print(f'📁 Starting cleanup: {temp_directory}')
    print('=' * 60)
    
    try:
        items = os.listdir(temp_directory)
    except PermissionError:
        print('❌ Error: Cannot access Temp folder')
        return files_removed, folders_removed
    
    for item in items:
        item_path = os.path.join(temp_directory, item)
        item_name = extract_item_name(item_path)
        
        if os.path.isfile(item_path):
            if delete_file(item_path, item_name):
                files_removed += 1
        
        elif os.path.isdir(item_path):
            if delete_directory(item_path, item_name):
                folders_removed += 1
    
    return files_removed, folders_removed


def main():
    """Main application function"""
    print("It would be better if you run it as administrator.")
    print('\n' + '=' * 60)
    print('🧹 WINDOWS TEMPORARY FILES CLEANUP UTILITY')
    print('=' * 60 + '\n')
    
    temp_folder = get_temp_directory()
    
    deleted_files, deleted_folders = cleanup_temp_folder(temp_folder)
    
    print('=' * 60)
    print(f'\n📊 Cleanup Results:')
    print(f'   Files deleted: {deleted_files}')
    print(f'   Folders deleted: {deleted_folders}')
    print(f'   Total items deleted: {deleted_files + deleted_folders}\n')
    
    input('Press Enter to exit...')


if __name__ == '__main__':
    main()
