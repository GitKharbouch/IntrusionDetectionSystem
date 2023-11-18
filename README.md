# IntrusionDetectionSystem
We will explore the possibility of creating a robust IDS using the NSL-KDD dataset

## Repository content

## Dataset
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
