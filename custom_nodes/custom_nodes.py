import folder_paths
import torch

import os
import sys
import json
import hashlib
import traceback
import math
import time
import random

from PIL import Image, ImageOps
from PIL.PngImagePlugin import PngInfo
import numpy as np
import safetensors.torch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "comfy"))

import comfy.diffusers_load
import comfy.samplers
import comfy.sample
import comfy.sd
import comfy.utils

import comfy.clip_vision

import comfy.model_management
from comfy.cli_args import args

import importlib

import folder_paths
import latent_preview


class CustomCLIPTextEncode:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"text": ("STRING", {"multiline": True}), "clip": ("CLIP",)}}

    RETURN_TYPES = ("CONDITIONING", "STRING")
    FUNCTION = "encode"

    CATEGORY = "Vdoc Custom Nodes"

    def encode(self, clip, text):
        tokens = clip.tokenize(text)
        cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
        return ([[cond, {"pooled_output": pooled}]], text)




class CustomSaveImage:
    def __init__(self):
        self.output_dir = "F:\\Art\\stable_diffusion_outputs\\ComfyUI"
        self.type = "output"

    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"images": ("IMAGE",),
                     "text_prompt": ("STRING", {"multiline": True}),
                     "seed_num":("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff})
                     },

                "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
                }

    RETURN_TYPES = ()
    FUNCTION = "save_images"

    OUTPUT_NODE = True

    CATEGORY = "Vdoc Custom Nodes"

    def save_images(self, images, text_prompt, seed_num, prompt=None, extra_pnginfo=None):
        results = list()
        for image in images:
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            metadata = None
            if not args.disable_metadata:
                metadata = PngInfo()
                if prompt is not None:
                    metadata.add_text("prompt", json.dumps(prompt))
                if extra_pnginfo is not None:
                    for x in extra_pnginfo:
                        metadata.add_text(x, json.dumps(extra_pnginfo[x]))
            # seed = prompt["3"]["inputs"]["seed"]
            with open('counter.txt', 'r') as file:
                current_value = int(file.read().strip())

            new_value = current_value + 1
            with open('counter.txt', 'w') as file:
                file.write(str(new_value))

            file = f'{current_value:05d}-{seed_num}-{text_prompt}.png'
            img.save(os.path.join(self.output_dir, file), pnginfo=metadata, compress_level=4)
            # results.append({
            #     "filename": file,
            #     "subfolder": self.output_dir,
            #     "type": self.type
            # })
            results.append({
                "filename": os.path.join(self.output_dir, file),
                "subfolder": "",
                "type": self.type
            })

        # return { "ui": { "images": results } }

        return {"ui": {"text": "something"}}
    


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "CustomSaveImage": CustomSaveImage,
    "CustomCLIPTextEncode": CustomCLIPTextEncode
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "CustomSaveImage": "Custom Save Image",
    "CustomCLIPTextEncode": "Custom CLIP Text Encode"
}
