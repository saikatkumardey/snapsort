# SnapSort

SnapSort can help you identify & sort images into different directories. It uses OpenAI's CLIP model locally. No internet connection required.

## Features

- **Automated Image Classification**: Leverages CLIP's deep learning model for precise image recognition.
- **Custom Sorting Labels**: Allows flexibility in sorting images into user-defined categories.
- **Batch Processing**: Efficiently handles large volumes of images.
- **Dry Run Mode**: Test sorting criteria without moving files to ensure precision.
- **Simple CLI**: Easy-to-use command-line interface for seamless operation.

## Installation

SnapSort can be installed using poetry. To install, clone the repository and run the following commands:

```
poetry shell
poetry install
```


## Usage

```
python app.py --dir /path/to/your/images
```

The default labels are for a use-case that detects screenshots & receipts and sorts them into separate folders. Any other images are left in the original directory. 

```
[
    "a screenshot of a software interface or a screen capture from phone",
    "a photo of an invoice or a receipt",
    "a photo of a real-world scene, an object, a person, or any image not fitting the description of a screenshot, receipt, or invoice",
]
```

The last label should be a catch-all label for images that do not match any of the other labels.

The threshold is the minimum confidence score required for an image to be sorted into a category. You need to experiment with this value to find the best threshold for your use case. Set it with `--threshold` flag. The default value is 0.5.

To dry run without moving files, add the `--dry-run` flag.

Set an appropriate batch size with the `--batch-size` flag. The default value is 4.

## Demo

```
python app.py demo/ -t 0.5 --dry-run
```

---

|    | file                                                                                                                                                    | class                                                                                                                             | probability   | status          |
|----|---------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|---------------|-----------------|
|  0 | ![demo/dc-Cover-47hlqdbsggeu2d33kvdqkjthc2-20200316192609.Medi.jpeg](demo/dc-Cover-47hlqdbsggeu2d33kvdqkjthc2-20200316192609.Medi.jpeg)                 | a screenshot of a software interface or a screen capture from phone                                                               | 0.98          | Moved (Dry Run) |
|  1 | ![demo/1000_F_56617167_ZGbrr3mHPUmLoksQmpuY7SPA8ihTI5Dh.jpg](demo/1000_F_56617167_ZGbrr3mHPUmLoksQmpuY7SPA8ihTI5Dh.jpg)                                 | a photo of an invoice or a receipt                                                                                                | 0.97          | Moved (Dry Run) |
|  2 | ![demo/MS-Paint-Windows-Full-Screen-Screenshot.png](demo/MS-Paint-Windows-Full-Screen-Screenshot.png)                                                   | a photo of a real-world scene, an object, a person, or any image not fitting the description of a screenshot, receipt, or invoice |               | Skipping        |
|  3 | ![demo/take-screenshot-1.jpg](demo/take-screenshot-1.jpg)                                                                                               | a screenshot of a software interface or a screen capture from phone                                                               | 0.76          | Moved (Dry Run) |
|  4 | ![demo/prescription.jpg](demo/prescription.jpg)                                                                                                         | a photo of an invoice or a receipt                                                                                                | 0.99          | Moved (Dry Run) |
|  5 | ![demo/chinese-dog-breeds-4797219-hero-2a1e9c5ed2c54d00aef75b05c5db399c.jpg](demo/chinese-dog-breeds-4797219-hero-2a1e9c5ed2c54d00aef75b05c5db399c.jpg) | a photo of a real-world scene, an object, a person, or any image not fitting the description of a screenshot, receipt, or invoice |               | Skipping        |
|  6 | ![demo/MacOS_Sonoma_Desktop.png](demo/MacOS_Sonoma_Desktop.png)                                                                                         | a screenshot of a software interface or a screen capture from phone                                                               | 0.63          | Moved (Dry Run) |
|  7 | ![demo/9483508eeee2b78a7356a15ed9c337a1-bengaluru-bangalore.jpg](demo/9483508eeee2b78a7356a15ed9c337a1-bengaluru-bangalore.jpg)                         | a photo of a real-world scene, an object, a person, or any image not fitting the description of a screenshot, receipt, or invoice |               | Skipping        |
|  8 | ![demo/l511jc41xpi01.jpg](demo/l511jc41xpi01.jpg)                                                                                                       | a screenshot of a software interface or a screen capture from phone                                                               | 0.76          | Moved (Dry Run) |
|  9 | ![demo/5_c6f4bb44bd.png](demo/5_c6f4bb44bd.png)                                                                                                         | a photo of a real-world scene, an object, a person, or any image not fitting the description of a screenshot, receipt, or invoice |               | Skipping        |
| 10 | ![demo/Outdoors-man-portrait.jpg](demo/Outdoors-man-portrait.jpg)                                                                                       | a photo of a real-world scene, an object, a person, or any image not fitting the description of a screenshot, receipt, or invoice |               | Skipping        |
| 11 | ![demo/26._smiling-couple-family-digital-painting-30-24.jpg](demo/26._smiling-couple-family-digital-painting-30-24.jpg)                                 | a photo of a real-world scene, an object, a person, or any image not fitting the description of a screenshot, receipt, or invoice |               | Skipping        |



## Requirements

- Python 3.6+
- PyTorch
- PIL (Python Imaging Library)
- transformers by HuggingFace

## Contributing

We welcome contributions to SnapSort. Feel free to open a pull request or issue.

## License

SnapSort is made available under the MIT License.
