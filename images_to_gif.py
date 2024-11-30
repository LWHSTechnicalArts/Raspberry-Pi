from PIL import Image
import os

# Path to the folder containing images
folder_path = input("Enter the path to the folder of images: ").strip()
output_gif = os.path.join(folder_path, "animated_compressed.gif")

# Collect all image file paths in the folder
images = [os.path.join(folder_path, file) for file in sorted(os.listdir(folder_path)) if file.endswith(('.png', '.jpg', '.jpeg'))]

# Ensure there are images to process
if not images:
    print("No images found in the folder.")
    exit()

# Open the images and compress them while creating the GIF
print("Creating compressed GIF...")
frames = []

for img_path in images:
    img = Image.open(img_path).convert("RGBA")  # Ensure consistent format
    # Resize to a smaller resolution (optional)
    img = img.resize((img.width // 2, img.height // 2), Image.LANCZOS)  # Use LANCZOS resampling
    # Reduce the number of colors (optional, reduces file size)
    img = img.quantize(colors=128)  # Reduce to 128 colors
    frames.append(img)

# Save the GIF with optimizations
frames[0].save(
    output_gif,
    save_all=True,
    append_images=frames[1:],
    optimize=True,  # Optimize the GIF for smaller file size
    duration=200,   # Frame duration in milliseconds
    loop=0          # Infinite loop
)

print(f"Compressed GIF saved as {output_gif}")
