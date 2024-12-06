# setup.py

from __init__ import bl_info
import os
import subprocess
from pathlib import Path

# mklink /D "C:\Users\name\AppData\Roaming\Blender Foundation\Blender\2.90\scripts\addons\my-addon" "C:\Users\name\Desktop\my-addon"
# ln -s /Users/tuo_nome/Desktop/my-addon /Users/tuo_nome/Library/Application\ Support/Blender/2.90/scripts/addons/my-addon

PATH = "~/Library/Application Support/Blender"

def select_blender_version(bl_info, available_versions):
    major, minor, patch = bl_info['blender']

    major_versions = [v for v in available_versions if v.startswith(f"{major}.")]

    if not major_versions:
        return "No versions found"
    
    if len(major_versions) == 1:
        return major_versions[0]
    
    minor_versions = [v for v in major_versions if f"{major}.{minor}" in v]

    if not minor_versions:
        return "No versions found"
    
    if len(minor_versions) == 1:
        return minor_versions[0]
    
    patch_versions = [v for v in minor_versions if f"{major}.{minor}.{patch}" in v]

    if not patch_versions:
        return "No versions found"
    
    if len(patch_versions) == 1:
        return patch_versions[0]

def main(): 

    # Usa os.path.join per garantire che gli spazi nel nome della directory siano gestiti correttamente 
    PATH = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 'Blender') 
    
    available_versions = os.listdir(PATH)
    blender_version = select_blender_version(bl_info, available_versions)
    # print(availble)

    addon_name = bl_info['name'].lower().replace(" ", "_")

    current_addon_folder_path = os.path.dirname(os.path.abspath(__file__))
    new_addon_folder_path = os.path.join(os.path.dirname(current_addon_folder_path), addon_name)

    symlink_path = os.path.join(PATH, str(blender_version), "scripts", "addons", addon_name)

    try: 
        if new_addon_folder_path != current_addon_folder_path:
            # Rinomina la directory corrente 
            subprocess.run(["mv", current_addon_folder_path, new_addon_folder_path], check=True) 
            print(f"Directory rinominata da '{current_addon_folder_path}' a '{new_addon_folder_path}'") 
            # Assicurati che la directory di destinazione del symlink esista 
        Path(os.path.dirname(symlink_path)).mkdir(parents=True, exist_ok=True) 
        # Crea il symlink 
        subprocess.run(["ln", "-s", new_addon_folder_path, symlink_path], check=True) 
        print(f"Symlink creato da '{symlink_path}' a '{new_addon_folder_path}'") 
    except subprocess.CalledProcessError as e: 
        print(f"Errore durante l'esecuzione del subprocess: {e}") 
    except Exception as e: 
        print(f"Errore inaspettato: {e}")

if __name__ == "__main__":
    main()