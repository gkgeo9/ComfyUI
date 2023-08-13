from PIL import Image
import json
import re
def print_image_metadata(image_path):
    try:
        image = Image.open(image_path)
        metadata = image.info

        print("Metadata for image:", image_path)
        for key, value in metadata.items():
            if key == "prompt":
                metadata_output = str(json.loads(value))
                noise_seed_match = re.search(r"'noise_seed': (\d+)", metadata_output)
                if noise_seed_match:
                    noise_seed = int(noise_seed_match.group(1))
                    print("noise_seed:", noise_seed)

                # Extract text_prompt value
                text_prompt_match = re.search(r"'text_prompt': '([^']*)'", metadata_output)
                if text_prompt_match:
                    text_prompt = text_prompt_match.group(1)
                    print("text_prompt:", text_prompt)

        image.close()
    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    image_path = "F:\\Art\\stable_diffusion_outputs\\ComfyUI\\00199-528583360473403-racecar morphing into pirate ship through cinematic rough ocean, white caps.png"  # Replace with the actual image path
    print_image_metadata(image_path)
