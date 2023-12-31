# USING VOXEL51 TO DOWNLOAD DATASET FROM GOOGLE OPEN IMAGES DATASET (V7):

# importing libraries
import cv2
import fiftyone as f
import glob
import os

splits = ["train", "validation"] # splits of dataset

for s in splits:
        if(s == "validation"):
                samples = 10
        else:
                samples = 1000
        # boilerplate code for dataset download:
        dataset = f.zoo.load_zoo_dataset(
                "open-images-v7",
                split = s, # split of dataset
                label_types=["detections"], # type of labels
                classes = ["Plastic bag"], # class of labels
                max_samples=samples, # max number of samples to download
        )