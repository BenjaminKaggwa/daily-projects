import sys
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def extract_palette(image_path, n_colors=6):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((200, 200))
    pixels = np.array(img).reshape(-1, 3)
    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
    kmeans.fit(pixels)
    colors     = kmeans.cluster_centers_.astype(int)
    labels     = kmeans.labels_
    counts     = np.bincount(labels)
    percentages = counts / len(labels) * 100
    order = np.argsort(-percentages)
    return [(tuple(colors[i]), percentages[i]) for i in order]

def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)

def display(palette, image_path):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    img = Image.open(image_path)
    ax1.imshow(img)
    ax1.set_title("Original Image")
    ax1.axis("off")
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, len(palette) + 1)
    ax2.set_title("Dominant Colour Palette")
    ax2.axis("off")
    for i, (color, pct) in enumerate(palette):
        y = len(palette) - i
        rect = patches.FancyBboxPatch((0.2, y-0.4), 2.5, 0.8,
               boxstyle="round,pad=0.05",
               facecolor=[c/255 for c in color], edgecolor="white", linewidth=2)
        ax2.add_patch(rect)
        hex_code = rgb_to_hex(color)
        ax2.text(3.2, y, f"{hex_code}  ({pct:.1f}%)", va="center", fontsize=11)
    plt.tight_layout()
    plt.savefig("palette_output.png", dpi=150, bbox_inches="tight")
    print("Palette saved to palette_output.png")
    plt.show()

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <image_path>")
        print("Example: python main.py photo.jpg")
        return
    path = sys.argv[1]
    try:
        n = int(input("Number of colours to extract (default 6): ") or 6)
    except:
        n = 6
    print(f"Extracting {n} dominant colours...")
    palette = extract_palette(path, n)
    print("\nColour Palette:")
    for i, (color, pct) in enumerate(palette, 1):
        print(f"  {i}. {rgb_to_hex(color)}  RGB{color}  {pct:.1f}%")
    display(palette, path)

if __name__ == "__main__":
    main()
