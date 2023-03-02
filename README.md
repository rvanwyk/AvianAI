# AvianAI
AvianAI: Predicting Bird Species with Machine Learning




## Dataset
The dataset used for this project is the Birds-150 dataset. This dataset contains 11,788 images of 200 bird species. The dataset is split into a training set of 8,855 images and a validation set of 2,933 images.

## Dependencies
The following Python packages are required to run this project:

* tensorflow
* keras
* numpy
* matplotlib

## Usage
To train the model, run the following command:

```
python train.py
```
This will train the model on the training set and save the trained model in the "models" folder.

To predict the species of a bird from an image, run the following command:

```
python predict.py --image <path_to_image>
```
Replace <path_to_image> with the path to the input image. The predicted species label will be displayed on the console.

## Credits
This project was created by Sai Oruganti and Ryan VanWyk as a project for the Carolina Engage Grant at the University of South Carolina. The code is released under the MIT License. The Bird-150 dataset is the property of its respective owners and is licensed under the Creative Commons Attribution-ShareAlike 3.0 License.


