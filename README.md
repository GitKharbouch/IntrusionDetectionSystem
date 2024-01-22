# IntrusionDetectionSystem

## Description
We will explore the possibility of creating a robust IDS using the NSL-KDD dataset, in this repository we will explore the dataset, visualize it, and use machine learning models to classify the attacks. We will also use a CNN model to classify the attacks as four main types. Then we will compare the results of the different models and choose the best one.
And finally group everything as docker microservices.

# Repository content

## File Structure
let's take a look at the file structure of the repository:
```bash
IntrusionDetectionSystem/ 
|-- data/
    |-- "All necessary data files including csv files, pcap files and txt files."
|-- docker/
    |-- Microservices "Contains all the microservices consisting of scripts and Dockerfiles."
        |-- Anomaly_detector/ "This microservice is used to detect the anomalies in the data."
        |-- Data/ "This the docker volume shared between the microservices."
        |-- File_retriever/ "This microservice is used to retrieve the files from the docker volume."
        |-- Preprocessor/ "This microservice is used to preprocess the data."
        .dockerignore
    docker-compose.yaml
|-- models/
    |-- "All the saved models used for the IDS."
|-- notebooks/
    |-- data_exploration.ipynb
    |-- ML_ids.ipynb
    |-- Multiclass_cnn_ids.ipynb
    |-- wireshark_local_preprocessing.ipynb
|-- nsl-kdd/
    |-- "The NSL-KDD dataset."
|-- scripts/
    |-- config.json "Contains the configuration for the IDS."
    |-- preprocess_packets.py "This script is used to preprocess the packets."
|-- wireshark_live_captures/
    |-- "Contains the captures from wireshark using the live capture feature."
```
## Dataset (nsl-kdd folder)

The dataset used for this project is the NSL-KDD dataset. It is a modified version of the KDDCup99 dataset. The NSL-KDD dataset has 41 features and 23 classes. The dataset is available at https://www.unb.ca/cic/datasets/nsl.html

# Local Setup 
The preleminarry steps to run the IDS locally before using docker are

## Data exploration (Data_Exploration.ipynb)
This notebook contains the data exploration and visualization. The data exploration steps include:
1. Loading the dataset
2. Getting a first glance at the data
3. Adding column headers and explaining the features
4. Data statistics
5. Data visualization
6. Data preprocessing (Scaling, Encoding, Dimensionality reduction, Splitting)

## Machine Learning approach (ML_IDS.ipynb)
This notebook contains the machine learning models used for the IDS. The models used are:
* *logistic regression*
* *decision tree*
* *random forest*
* *linear support vector machine*
* *naive bayes*
* *K-nearest neighbors*

## Deep Learning approach (MultiClass_CNN_IDS.ipynb)
This notebook contains the CNN model used for the IDS. In this approach we classified the attack labels as four main types, and tackled this as a multiclass classification problem. The four main types are:
* *DOS*
* *U2R*
* *R2L*
* *PROBE*

## Preprocessing (wireshark_local_preprocessing.ipynb, preprocess_packets.py)
This notebook contains the preprocessing steps to adapt the wireshark captures to the training dataset. The preprocessing steps include:
1. Loading the dataset
2. extracting the necessary features
3. mapping the features to the training dataset format 
4. saving the preprocessed data

The python script is used to preprocess the packets in the docker container in one execution.It uses the same steps as the notebook.

## Configuration (config.json)
This file contains the configuration for the IDS. to make all the necessary mappings and establish the different rules to keep the code lighter and more readable.

# Docker Setup

## orchestration (docker-compose.yaml)
Done using docker-compose, it contains the different services and the shared volume between them.
the microservices work in the following order File_retriever -> Preprocessor -> Anomaly_detector

## Microservices 

### File retriever (file_retriever folder)
-retrieve_files.sh is the script used to retrieve the files from the docker volume(from raw_captures to ready_to_process). It is used to move files after they are saved by wireshark automaticcally to the docker volume.
-dockerfile uses a lightweight linux image : alpine and installs the necessary packages to run the script.

### Preprocessor (preprocessor folder)
-preprocess_packets.py is the script used to preprocess the packets in the docker container in one execution.It uses the same steps as the notebook and moves the preprocessed files to the preprocessed folder and keeps a copy with additional features in the info folder and the original files in the archive folder.
-dockerfile uses python 3.8 and installs the necessary requirements to run the script.
-requirements.txt contains the necessary dependencies to run the script.
-config.json (see configuration section)

### Anomaly detector (anomaly_detector folder)
-detect.py is the script used to detect the anomalies in the data using the deep learning model. it then sends the results to the results folder.
-dockerfile uses a tensorflow image and installs the necessary requirements to run inference.
-requirements.txt contains the necessary dependencies to run the script.
-CNN_NSL_KDD.h5 is the saved model used for inference.

## Volume (Data folder)
This is the shared volume between the microservices. It contains the following folders:
-raw_captures: contains the raw captures from wireshark.
-ready_to_process: contains the files ready to be processed by the preprocessor.
-preprocessed: contains the preprocessed files.
-info: contains the files with additional features.
-archive: contains the original files.
-results: contains the results of the anomaly detection.