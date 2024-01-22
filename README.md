# IntrusionDetectionSystem

## Description
We will explore the possibility of creating a robust IDS using the NSL-KDD dataset, in this repository we will explore the dataset, visualize it, and use machine learning models to classify the attacks. We will also use a CNN model to classify the attacks as four main types. Then we will compare the results of the different models and choose the best one. And finally group everything as docker microservices.

## Repository content

## File Structure

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

## Dataset (nsl-kdd folder)

The dataset used for this project is the NSL-KDD dataset. It is a modified version of the KDDCup99 dataset. The NSL-KDD dataset has 41 features and 23 classes. The dataset is available at https://www.unb.ca/cic/datasets/nsl.html

## Data_Exploration.ipynb
This notebook contains the data exploration and visualization. The data exploration steps include:
1. Loading the dataset
2. Getting a first glance at the data
3. Adding column headers and explaining the features
4. Data statistics
5. Data visualization
6. Data preprocessing (Scaling, Encoding, Dimensionality reduction, Splitting)

## ML_IDS.ipynb
This notebook contains the machine learning models used for the IDS. The models used are:
* *logistic regression*
* *decision tree*
* *random forest*
* *linear support vector machine*
* *naive bayes*
* *K-nearest neighbors*

## MultiClass_CNN_IDS.ipynb
This notebook contains the CNN model used for the IDS. In this approach we classified the attack labels as four main types, and tackled this as a multiclass classification problem. The four main types are:
* *DOS*
* *U2R*
* *R2L*
* *PROBE*
