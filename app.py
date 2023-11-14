import os
import shutil
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
import argparse
import pandas as pd
from tabulate import tabulate
import numpy as np


def classify_image(image_paths, model, processor, labels):
    images = []
    for image_path in image_paths:
        try:
            images.append(Image.open(image_path))
        except IOError:
            print(f"Cannot process {image_path}. Unsupported format or corrupted file.")

    inputs = processor(text=labels, images=images, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    probs = outputs.logits_per_image.softmax(dim=1)
    max_probs, label_indices = torch.max(probs, dim=1)
    return label_indices, max_probs


def process_images(directory, labels, dry_run, threshold, batch_size):
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    logs = []
    image_files = [
        filename
        for filename in os.listdir(directory)
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff"))
    ]
    image_batches = [
        image_files[i : i + batch_size] for i in range(0, len(image_files), batch_size)
    ]

    for batch in image_batches:
        image_paths = [
            os.path.join(directory, filename)
            for filename in batch
            if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff"))
        ]
        if not image_paths:
            continue

        label_indices, max_probs = classify_image(image_paths, model, processor, labels)

        batch_labels = np.array(labels)[label_indices]

        for filepath, label, max_prob in zip(image_paths, batch_labels, max_probs):
            if label == "error" or label == labels[-1] or max_prob < threshold:
                logs.append([f"![{filepath}]({filepath})", label, "", "Skipping"])
                continue

            target_dir = os.path.join(directory, label)

            if not dry_run and not os.path.exists(target_dir):
                os.makedirs(target_dir)

            if dry_run:
                logs.append(
                    [
                        f"![{filepath}]({filepath})",
                        label,
                        round(max_prob.item(), 2),
                        "Moved (Dry Run)",
                    ]
                )
            else:
                shutil.move(
                    os.path.join(directory, filepath),
                    os.path.join(target_dir, filepath),
                )
                logs.append(
                    [
                        f"![{filepath}]({filepath})",
                        label,
                        round(max_prob.item(), 2),
                        "Moved",
                    ]
                )

    logs_df = pd.DataFrame(logs, columns=["file", "class", "probability", "status"])
    return logs_df


def main():
    parser = argparse.ArgumentParser(description="Sort images into folders using CLIP.")
    parser.add_argument("dir", type=str, help="Directory containing images")
    parser.add_argument(
        "--labels",
        type=str,
        nargs="+",
        default=[
            "a screenshot of a software interface or a screen capture from phone",
            "a photo of an invoice or a receipt",
            "a photo of a real-world scene, an object, a person, or any image not fitting the description of a screenshot, receipt, or invoice",
        ],
        help="Labels for sorting images",
    )
    parser.add_argument(
        "-dr",
        "--dry-run",
        action="store_true",
        help="Simulate the sorting process without moving files",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        type=float,
        default=0.5,
        help="Minimum confidence score for classification",
    )
    parser.add_argument(
        "-b",
        "--batch-size",
        type=int,
        default=4,
        help="Number of images to process at a time",
    )

    args = parser.parse_args()

    if not os.path.isdir(args.dir):
        print(f"The directory {args.dir} does not exist.")
        return

    logs_df = process_images(
        args.dir,
        args.labels,
        args.dry_run,
        args.threshold,
        args.batch_size,
    )
    print(tabulate(logs_df, headers="keys", tablefmt="github"))


if __name__ == "__main__":
    main()
