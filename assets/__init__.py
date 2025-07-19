import os
import base64

def load_asset(asset):
    asset_path = os.path.join(os.path.dirname(__file__), asset)
    with open(asset_path, 'r') as file:
        return file.read()

def load_asset_as_base64(asset):
    asset_path = os.path.join(os.path.dirname(__file__), asset)
    with open(asset_path, 'rb') as file:
        return base64.b64encode(file.read()).decode("utf-8")

def image_base64(asset):
    b64_string = load_asset_as_base64(asset)
    return f"data:image/png;base64,{b64_string}"
