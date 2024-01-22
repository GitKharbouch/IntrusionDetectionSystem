import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import StandardScaler
import tensorflow as tf

with open('/app/features.txt') as f:
    content = f.readlines()

model_path = '/app/CNN_NSL-KDD.tflite'  # Change to the path of your TensorFlow Lite model
data_folder_path = os.path.join(os.path.dirname(__file__), 'data', 'preprocessed')

for file_name in os.listdir(data_folder_path):
    data_path = os.path.join(data_folder_path, file_name)
    if file_name.endswith('.csv'):
        df = pd.read_csv(data_path)

# Using Standard scaler for normalizing
std_scaler = StandardScaler()

def standardization(df, col):
    for i in col:
        arr = df[i]
        arr = np.array(arr)
        df[i] = std_scaler.fit_transform(arr.reshape(len(arr), 1))
    return df

numeric_col = df.select_dtypes(include='number').columns
data = standardization(df, numeric_col)
x = pd.get_dummies(df, columns=['protocol_type', 'service', 'flag'], prefix="", prefix_sep="")  

# let's get the names of our new columns
x_columns = x.columns
content = [x.strip() for x in content]

# let's rename our columns using the txt file and create new columns if they don't exist
for i in content:
    if i not in x_columns:
        x[i] = 0 

x = x.reindex(columns=content)
x_test = x
x_test = x_test.astype(np.float32)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

# Load TensorFlow Lite model
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# Set input tensor
input_tensor_index = interpreter.get_input_details()[0]['index']
interpreter.set_tensor(input_tensor_index, x_test)

# Run inference
interpreter.invoke()

# Get output tensor
output_tensor_index = interpreter.get_output_details()[0]['index']
prediction_array = interpreter.get_tensor(output_tensor_index)

classes = np.array(['Dos', 'Probe', 'R2L', 'U2R', 'normal'])
predicted_classes_indices = np.argmax(prediction_array, axis=1)
predicted_classes = classes[predicted_classes_indices]

x['Dos'] = prediction_array[:, 0]
x['Probe'] = prediction_array[:, 1]
x['R2L'] = prediction_array[:, 2]
x['U2R'] = prediction_array[:, 3]
x['normal'] = prediction_array[:, 4]
x['predicted_classes'] = predicted_classes

x.to_csv('/app/data/predictions.csv', index=False)
