import os
import shutil

def copy_directory(src, dst):
    # Step 1: Clear the destination directory if it exists
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)  # Recreate the destination directory

    # Step 2: Recursively copy each item in the source directory
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
            print(f"Copied file: {dst_path}")
        elif os.path.isdir(src_path):
            os.mkdir(dst_path)
            print(f"Created directory: {dst_path}")
            copy_directory(src_path, dst_path)  # Recursive call for subdirectories