import os

PROJECT_DIR = os.getcwd()
ASSET_DIR = f'{PROJECT_DIR}/assets'
PROFILE_PHOTO_DIR = f'{PROJECT_DIR}/dataset/profile_photo'

for path in [ASSET_DIR, PROFILE_PHOTO_DIR]:
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
