import pandas as pd
# from tensorflow.keras.models import load_model
from keras.models import load_model
import os
import pickle


MODEL_VERSION="1.0.0" # comes from ml flow 


#import the ml model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model=load_model(os.path.join(BASE_DIR, 'model.h5'))

MODEL_VERSION="1.0.0" # comes from ml flow 

# Load encoders
with open(os.path.join(BASE_DIR, "Onehot_encoder_geo.pkl"),"rb") as f:
     geo_encoder= pickle.load(f)

with open(os.path.join(BASE_DIR, "label_encoder_gender.pkl"),'rb') as f:
     gender_encoder=pickle.load(f)

with open(os.path.join(BASE_DIR, "scaler.pkl"),'rb') as f:
     scalar=pickle.load(f)
def predict_output(user_input:dict):
     input_df= pd.DataFrame([user_input])

    # One Hot Encoding for Geography
     geo_encoded = geo_encoder.transform(
            input_df[['Geography']]
        )
    
     geo_encoded_df = pd.DataFrame(
            geo_encoded.toarray(),
            columns=geo_encoder.get_feature_names_out(['Geography'])
        )
    
    
        # Label Encoding for Gender
     input_df['Gender'] = gender_encoder.transform(
            input_df['Gender']
        )
    
    
        # Remove original Geography
     input_df = input_df.drop(
            columns=['Geography']
        )
    
    
        # Combine encoded Geography with other features
     input_df = pd.concat(
            [input_df.reset_index(drop=True),
             geo_encoded_df.reset_index(drop=True)],
            axis=1
        )
    
        
        # Scaling
     input_scaled = scalar.transform(input_df)

     output= model.predict(input_scaled)   
     return output
    