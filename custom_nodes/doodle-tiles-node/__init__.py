from PIL import Image, ImageOps, ImageFilter
import numpy as np
import random
from skimage.restoration import denoise_nl_means, estimate_sigma
from skimage import img_as_float, img_as_ubyte
import torch

# Tensor to PIL
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

# PIL to Tensor
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

class DoodleTilesGenerator:
    """
    A node for creating a mosaic image with solid color background and black & white tiles merged such that
    white areas become transparent and black areas retain color.

    This node applies a denoising filter to enhance tile quality and resizes tiles for a unique artistic effect.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        """
        Define input types for ComfyUI node.
        """
        return {
            "required": {
                "images": ("IMAGE",),
                "tile_width": ("INT", {
                    "default": 128,
                    "min": 1,
                    "max": 1024,
                    "step": 1,
                }),
                "tile_height": ("INT", {
                    "default": 128,
                    "min": 1,
                    "max": 1024,
                    "step": 1,
                }),
                "bg_width": ("INT", {
                    "default": 1024,
                    "min": 100,
                    "max": 5000,
                    "step": 1,
                }),
                "bg_height": ("INT", {
                    "default": 1024,
                    "min": 100,
                    "max": 5000,
                    "step": 1,
                }),
                "bg_color": ("STRING", {
                    "default": "(254, 80, 0)",
                    "multiline": False,
                }),
                "stroke_color": ("STRING", {
                    "default": "(171, 54, 0)",
                    "multiline": False,
                })
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "create_mosaic"
    CATEGORY = "image"

    def create_mosaic(self, images, tile_width, tile_height, bg_width, bg_height, bg_color, stroke_color):        
        # Process the background color string input
        bg_color = eval(bg_color)

        # Process the stroke color string input
        stroke_color = eval(stroke_color)

        # Create a solid color background image
        background = Image.new('RGBA', (bg_width, bg_height), color=bg_color)

        # Load tiles and prepare masks
        tiles = []
        for image in images:
            original_tile = tensor2pil(image).convert('L')
            resized_tile = original_tile.resize((int(tile_width * 0.8), int(tile_height * 0.8)), Image.LANCZOS)
            mask = resized_tile.point(lambda p: p <= 128 and 255)
            tile_image = ImageOps.colorize(resized_tile, stroke_color, stroke_color)

            np_image = np.array(tile_image)
            float_image = img_as_float(np_image)
            sigma_est = np.mean(estimate_sigma(float_image, channel_axis=-1))
            denoised_image = denoise_nl_means(float_image, h=2.0 * sigma_est, fast_mode=True,
                                                patch_size=7, patch_distance=11, channel_axis=-1)
            denoised_tile = Image.fromarray(img_as_ubyte(denoised_image))
            denoised_tile = denoised_tile.filter(ImageFilter.EDGE_ENHANCE_MORE)

            centered_tile = Image.new('RGBA', (tile_width, tile_height), bg_color+(0,))
            centered_mask = Image.new('L', (tile_width, tile_height), 0)
            top_left_corner = ((tile_width - denoised_tile.width) // 2, (tile_height - denoised_tile.height) // 2)
            centered_tile.paste(denoised_tile, top_left_corner)
            centered_mask.paste(mask, top_left_corner)

            tiles.append((centered_tile, centered_mask))

        random.shuffle(tiles)

        # Place tiles on the background using masks
        num_tiles_x = int(np.ceil(bg_width / tile_width))
        num_tiles_y = int(np.ceil(bg_height / tile_height))

        for y in range(num_tiles_y):
            for x in range(num_tiles_x):
                tile, mask = tiles[(x + y * num_tiles_x) % len(tiles)]
                background.paste(tile, (x * tile_width, y * tile_height), mask)

        # Convert the final PIL image to a format that ComfyUI can handle as an output
        output_image = pil2tensor(background)
        return (output_image,)

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "Doodle Tiles Generator": DoodleTilesGenerator
}
