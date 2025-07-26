from assets import image_base64

class AssetBridge:
    def get_icon(self):
        return image_base64("img/frankenstein.png")

    def frankenstein_colour_logo(self):
        return image_base64("img/frankenstein_colour.png")
