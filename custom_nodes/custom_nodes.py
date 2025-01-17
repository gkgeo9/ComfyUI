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
        for image in images:
            print("save iomage seedddd", seed_num)
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

            with open('counter.txt', 'r') as file:
                current_value = int(file.read().strip())

            new_value = current_value + 1
            with open('counter.txt', 'w') as file:
                file.write(str(new_value))
            
            with open('previous_seeds.txt', 'w') as file:
                file.write(str(seed_num))

            # print(str(text_prompt)[0:30])

            file = f'{current_value:05d}-{seed_num}-{str(text_prompt)[0:30]}.png'
            print("2nd")
            img.save(os.path.join(self.output_dir, file), pnginfo=metadata, compress_level=4)

        return {"ui": {"text": "something"}}
    
class PreviousSeed:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {
                     "seed_num":("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff})
                     },
                }
    
    RETURN_TYPES = ("INT", )
    FUNCTION = "return_"

    OUTPUT_NODE = True

    CATEGORY = "Vdoc Custom Nodes"
    def return_(self, seed_num):
        if seed_num == 0:
            temp = 0
            with open('previous_seeds.txt', 'r') as file:
                current_value = int(file.read().strip())
                temp = current_value
                # print("Seed:", current_value)
            print("Seed:", temp)
            return (int(temp),)
        return (int(seed_num),)

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "CustomSaveImage": CustomSaveImage,
    "CustomCLIPTextEncode": CustomCLIPTextEncode,
    "PreviousSeed":PreviousSeed
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "CustomSaveImage": "Custom Save Image",
    "CustomCLIPTextEncode": "Custom CLIP Text Encode",
    "PreviousSeed":"PreviousSeed"
}
