from pydantic import BaseModel,Field,computed_field
from typing import Literal,Annotated

## pydantic model to validate incoming data
class UserInput(BaseModel):
    CreditScore:Annotated[float,Field(..., ge=350, le=850 ,  description="Credit score of the customer")]
    Geography:Annotated[Literal['France', 'Spain', 'Germany'],Field(...,description="Country where the customer’s bank branch/account is located.")]
    Gender:Annotated[Literal['Female', 'Male'],Field(..., description='Gender of the customer ')]
    Age:Annotated[int,Field(...,gt=0,description='Age of the customer')]
    Tenure:Annotated[int,Field(...,ge=0,description='Number of years the customer has been with the bank.')]
    Balance:Annotated[float,Field(...,gt=0,description="Balance of the client in bank account")]
    NumOfProducts:Annotated[int,Field(...,gt=0,description="Number of banking products/services used by the customer.")]
    HasCrCard:Annotated[int,Field(...,ge=0,description='Whether the customer has a credit card or not (1 = Yes, 0 = No).')]
    IsActiveMember:Annotated[int,Field(...,ge=0,description="Whether the customer is an active member of the bank (1 = Yes, 0 = No).")]
    EstimatedSalary:Annotated[float,Field(...,gt=0,description='Estimated annual salary/income of the customer.')]