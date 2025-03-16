import os
import zipfile

def create_game_package():
    # Files to include
    files_to_package = [
        'planet_lander.py',
        'README.md'
    ]
    
    # Create zip file
    with zipfile.ZipFile('mission_to_touchdown.zip', 'w') as zipf:
        for file in files_to_package:
            if os.path.exists(file):
                zipf.write(file)
                print(f"Added {file} to package")
            else:
                print(f"Warning: {file} not found")
    
    print("\nPackage created: mission_to_touchdown.zip")
    print("Share this file with others!")

if __name__ == "__main__":
    create_game_package() 