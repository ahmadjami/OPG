# -*- coding: utf-8 -*-
"""mini_project_preprocessing and base_model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18pETR5WUsD_BbkE6oCl-Xumsn3YLPXQp
"""

import os
import sys
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the Drive helper and mount
from google.colab import drive

# This will prompt for authorization.
drive.mount('/content/gdrive')

pip install pydicom

from PIL import Image

import glob
files_dcm = glob.glob('/content/gdrive/MyDrive/Mini Project/Dataset/OPG FOLDER_1/**/*.DCM', recursive = True) #Jpeg,jpg,DCM
files_jpeg = glob.glob('/content/gdrive/MyDrive/Mini Project/Dataset/OPG FOLDER_1/**/*.Jpeg', recursive = True)


print(len(files_dcm))
print(len(files_jpeg))

import pydicom

# function to convert dcm to jpg
def convert_dcm_jpg(name):
    
    im = pydicom.dcmread(name)

    im = im.pixel_array.astype(float)

    rescaled_image = (np.maximum(im,0)/im.max())*255 # float pixels
    final_image = np.uint8(rescaled_image) # integers pixels

    final_image = Image.fromarray(final_image)

    return final_image

#convrt dcm to jpg and rename
for name in files_dcm:
    image = convert_dcm_jpg(name)
    name=name.replace(".DCM",'')

    image.save(name+'.jpg')
    # print(name)

# convert Jpeg to JPG
for name in files_jpeg:
    im = Image.open(name)
    rgb_im = im.convert("RGB")
    name=name.replace(".Jpeg",'')
    rgb_im.save(name+".jpg")
    # print('saved',name)

files_jpg = glob.glob('/content/gdrive/MyDrive/Mini Project/Dataset/OPG FOLDER_1/**/*.jpg', recursive = True) #Jpeg,jpg,DCM
# print(files_jpg)

for name in files_jpg:
    if name.endswith(" .jpg"):
        im = Image.open(name)
        rgb_im = im.convert('RGB')
        name=name.replace(" .jpg",'')
        rgb_im.save(name+".jpg")

    if name.endswith("  .jpg"):
        im = Image.open(name)
        rgb_im = im.convert('RGB')
        name=name.replace("  .jpg",'')
        rgb_im.save(name+".jpg")

dir_name = "/content/gdrive/MyDrive/Mini Project/Dataset/OPG FOLDER_1/"
files = os.listdir(dir_name)
st = (" .jpg","  .jpg",".DCM",".Jpeg")
for item in files:
    if item.endswith(st):
        os.remove(os.path.join(dir_name, item))

df = pd.read_csv('/content/gdrive/MyDrive/Mini Project/Dataset/metadata.csv')
df.head()

df = df.drop(labels = ["DOE","DOB","Chronological age"], axis = 1)
df.head()

df.isnull().sum()

df = df.dropna()
df.isnull().sum()

df.head()

df['m-f'].unique()

df['m-f'] = df['m-f'].str.strip()
df['m-f'] = df['m-f'].str.upper()
df['m-f'].unique()

len('/content/gdrive/MyDrive/Mini Project/Dataset/OPG FOLDER_1/')

# files_final = glob.glob('/content/gdrive/MyDrive/Mini Project/Dataset/OPG FOLDER/**/*.jpg', recursive = True)
# files_final

image_path = [item for item in sorted(glob.glob('/content/gdrive/MyDrive/Mini Project/Dataset/OPG FOLDER_1/**/*.jpg', recursive = True),key = lambda x:int(x[58:-4]))]
image_path

# for f in files_final:
# path = "/content/gdrive/MyDrive/Mini Project/Dataset/OPG FOLDER"
# for fig in df['OPG Slide NO']:
        #load images into images of size 100x100x3
        # if os.path.exists(path+"/"+fig):

df.values

#splitting data acording to M/F


img_dir =r'/content/gdrive/MyDrive/Mini Project/Dataset/OPG FOLDER_1'

DR = r"/content/gdrive/MyDrive/Mini Project/Dataset/class"
if not os.path.exists(DR):
    os.mkdir(DR)

for filename, class_name in df.values:
    # Create subdirectory with `class_name`
    if not os.path.exists(DR +'/'+ str(class_name)):
        os.makedirs(DR +'/'+ str(class_name))
    src_path = img_dir + '/'+ str(filename) + '.jpg'
    dst_path = DR+'/' + str(class_name) + '/' + str(filename) + '.jpg'
    try:
        shutil.copy(src_path, dst_path)
        print("sucessful")
    except IOError as e:
        print('Unable to copy file {} to {}'
              .format(src_path, dst_path))
    except:
        print('When try copy file {} to {}, unexpected error: {}'
              .format(src_path, dst_path, sys.exc_info()))

pip install split-folders

pip install split-folders[full]

input_folder = '/content/gdrive/MyDrive/Mini Project/Dataset/class'
output_folder = '/content/gdrive/MyDrive/Mini Project/Dataset/processed_data'

import splitfolders
splitfolders.ratio(input_folder, output=output_folder,
    seed=1337, ratio=(.7, .3), group_prefix=None, move=False

path, dirs, fileF = next(os.walk("/content/gdrive/MyDrive/Mini Project/Dataset/processed_data/val/F"))
file_countF = len(fileF)
file_countF

path, dirs, fileM = next(os.walk("/content/gdrive/MyDrive/Mini Project/Dataset/processed_data/val/M"))
file_countM = len(fileM)
file_countM



############################################

from tensorflow.keras.layers import Input, Lambda, Dense, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator,load_img
from tensorflow.keras.models import Sequential

# re-size all the images to this
IMAGE_SIZE = [224, 224]

train_path = '/content/gdrive/MyDrive/Mini Project/Dataset/processed_data/train'
valid_path = '/content/gdrive/MyDrive/Mini Project/Dataset/processed_data/val'

"""# VGG16"""

# Import the VGG16 library as shown below and add preprocessing layer to the front of VGG
# Here we will be using imagenet weights

vgg16 = VGG16(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)

# don't train existing weights
for layer in vgg16.layers:
    layer.trainable = False

from glob import glob

# useful for getting number of output classes
folders = glob('/content/gdrive/MyDrive/Mini Project/Dataset/processed_data/train/*')
folders

# our layers 
x_vgg16 = Flatten()(vgg16.output)

len(folders)

prediction = Dense(len(folders), activation='softmax')(x_vgg16)

# create a model object
model1 = Model(inputs=vgg16.input, outputs=prediction)

# view the structure of the model
model1.summary()

# tell the model what cost and optimization method to use
model1.compile(
  loss='categorical_crossentropy',
  optimizer='adam',
  metrics=['accuracy']
)

# Use the Image Data Generator to import the images from the dataset
from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)

# Make sure you provide the same target size as initialied for the image size
training_set = train_datagen.flow_from_directory('/content/gdrive/MyDrive/Mini Project/Dataset/processed_data/train',
                                                 target_size = (224, 224),
                                                 batch_size = 32,
                                                 class_mode = 'categorical') #class_mode = 'binary'/'categorical'

training_set.class_indices

test_set = test_datagen.flow_from_directory('/content/gdrive/MyDrive/Mini Project/Dataset/processed_data/val',
                                            target_size = (224, 224),
                                            batch_size = 32,
                                            class_mode = 'categorical')

# fit the model
# Run the cell. It will take some time to execute
r1 = model1.fit_generator(
  training_set,
  validation_data=test_set,
  epochs=20,
  steps_per_epoch=len(training_set),
  validation_steps=len(test_set)
)

# plot the loss
plt.plot(r1.history['loss'], label='train loss')
plt.plot(r1.history['val_loss'], label='val loss')
plt.legend()
plt.show()
# plt.savefig('LossVal_loss')

# plot the accuracy
plt.plot(r1.history['accuracy'], label='train acc')
plt.plot(r1.history['val_accuracy'], label='val acc')
plt.legend()
plt.show()
# plt.savefig('AccVal_acc')

# finding the training accuracy 
print('Accuracy of the model: ',r1.history['accuracy'][-1])

# finding the training loss 
print('Loss of the model: ',r1.history['loss'][-1])

"""# Inception"""

from tensorflow.keras.applications.inception_v3 import InceptionV3
inceptionV3 = InceptionV3(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)

for layer in inceptionV3.layers:
    layer.trainable = False

# our layers 
x_inc = Flatten()(inceptionV3.output)
prediction = Dense(len(folders), activation='softmax')(x_inc)

# create a model object
model2 = Model(inputs=inceptionV3.input, outputs=prediction)

# tell the model what cost and optimization method to use
model2.compile(
  loss='categorical_crossentropy',
  optimizer='adam',
  metrics=['accuracy']
)

# fit the model
# Run the cell. It will take some time to execute
r2 = model2.fit_generator(
  training_set,
  validation_data=test_set,
  epochs=20,
  steps_per_epoch=len(training_set),
  validation_steps=len(test_set)
)

plt.plot(r2.history['loss'], label='train loss')
plt.plot(r2.history['val_loss'], label='val loss')
plt.legend()
plt.show()
# plt.savefig('LossVal_loss')

# plot the accuracy
plt.plot(r2.history['accuracy'], label='train acc')
plt.plot(r2.history['val_accuracy'], label='val acc')
plt.legend()
plt.show()
# plt.savefig('AccVal_acc')

# finding the training accuracy 
print('Accuracy of the model: ',r2.history['accuracy'][-1])

# finding the training loss 
print('Loss of the model: ',r2.history['loss'][-1])



"""# ResNet50"""

from tensorflow.keras.applications import ResNet50

resnet50 = ResNet50(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)

for layer in resnet50.layers:
    layer.trainable = False

# our layers 
x_res = Flatten()(resnet50.output)
prediction = Dense(len(folders), activation='softmax')(x_res)

# create a model object
model3 = Model(inputs=resnet50.input, outputs=prediction)


# tell the model what cost and optimization method to use
model3.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

# fit the model
# Run the cell. It will take some time to execute
r3 = model3.fit_generator(
  training_set,
  validation_data=test_set,
  epochs=20,
  steps_per_epoch=len(training_set),
  validation_steps=len(test_set)
)

plt.plot(r3.history['loss'], label='train loss')
plt.plot(r3.history['val_loss'], label='val loss')
plt.legend()
plt.show()
# plt.savefig('LossVal_loss')

# plot the accuracy
plt.plot(r3.history['accuracy'], label='train acc')
plt.plot(r3.history['val_accuracy'], label='val acc')
plt.legend()
plt.show()
# plt.savefig('AccVal_acc')

# finding the training accuracy 
print('Accuracy of the model: ',r3.history['accuracy'][-1])

# finding the training loss 
print('Loss of the model: ',r3.history['loss'][-1])

