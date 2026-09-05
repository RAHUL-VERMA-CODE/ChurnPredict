from fastapi import FastAPI
from fastapi.responses import JSONResponse
from model.predict_output import model,MODEL_VERSION
from schema.user_input import UserInput
from model.predict_output import predict_output

app=FastAPI()

@app.get("/")
def home():
    return {
        "message":"Customer Churn Prediction API is running"
    }

@app.get('/health')
def health_check():
    return{
        'status':'ok',
        'version':MODEL_VERSION,
        'model_loaded':model is not None
    }

# machine readable (for production)
@app.post('/predict')
def predict_churn(data:UserInput):
    user_input={
        'CreditScore':data.CreditScore,
        'Geography':data.Geography,
        'Gender':data.Gender,
        'Age':data.Age,
        'Tenure':data.Tenure,
        'Balance':data.Balance,
        'NumOfProducts':data.NumOfProducts,
        'HasCrCard':data.HasCrCard,
        'IsActiveMember':data.IsActiveMember,
        'EstimatedSalary':data.EstimatedSalary
    }

    try:
        # Model prediction
        prediction=predict_output(user_input)
        prediction_probability=float(prediction[0][0])

        # Convert probability into class
        if prediction_probability>=0.5:
            result="Customer will churn"
            churn=1
        else:
            result="Customer will not churn"
            churn=0

        return JSONResponse(
            status_code=200,
            content={
                "churn_probability":prediction_probability,
                "prediction":churn,
                "result":result
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error":str(e)
            }
        )


    # if we want we make response model (model kaise response dega usko pahle hi bata dega )