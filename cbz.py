import os
import zipfile
import rarfile
import shutil

source_folder = r""

# Ensure unrar is installed
rarfile.UNRAR_TOOL = "C:\\Program Files\\WinRAR\\unrar.exe"  # Adjust if necessary

def convert_cbr_to_cbz(cbr_path):
    cbz_path = cbr_path.replace(".cbr", ".cbz")
    extract_folder = cbr_path.replace(".cbr", "_temp")

    try:
        # Detect file type
        if rarfile.is_rarfile(cbr_path):
            with rarfile.RarFile(cbr_path) as rf:
                rf.extractall(extract_folder)
        elif zipfile.is_zipfile(cbr_path):
            with zipfile.ZipFile(cbr_path, 'r') as zf:
                zf.extractall(extract_folder)
        else:
            print(f"Skipping {cbr_path}: Not a valid RAR or ZIP archive.")
            return

        # Create CBZ (ZIP) archive
        with zipfile.ZipFile(cbz_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(extract_folder):
                for file in files:
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, extract_folder)
                    zf.write(full_path, arcname)

        # Cleanup
        shutil.rmtree(extract_folder)
        os.remove(cbr_path)

        print(f"Converted: {cbr_path} → {cbz_path}")

    except Exception as e:
        print(f"Error converting {cbr_path}: {e}")

# Process all CBR files
for file in os.listdir(source_folder):
    if file.lower().endswith(".cbr"):
        convert_cbr_to_cbz(os.path.join(source_folder, file))
