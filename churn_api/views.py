import pickle
import pandas as pd
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerChurnSerializer


def load_model():
    """Load the trained model and encoders"""
    try:
        with open(settings.MODEL_PATH, 'rb') as file:
            model_data = pickle.load(file)
        
        with open(settings.ENCODERS_PATH, 'rb') as file:
            encoders = pickle.load(file)
            
        return model_data["model"], model_data["features_names"], encoders
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None, None


def predict_churn(customer_data):
    """Make prediction for customer churn"""
    try:
        # Load model components
        model, feature_names, encoders = load_model()
        if model is None:
            return {"error": "Model not loaded"}
        
        # Convert input to DataFrame
        input_df = pd.DataFrame([customer_data])
        
        # Encode categorical features
        for col, encoder in encoders.items():
            if col in input_df.columns:
                try:
                    input_df[col] = encoder.transform(input_df[col])
                except ValueError as e:
                    # Handle unseen categories
                    print(f"Warning: {e}")
                    input_df[col] = 0  # Default encoding
        
        # Ensure all required features are present
        for feature in feature_names:
            if feature not in input_df.columns:
                input_df[feature] = 0
        
        # Reorder columns to match training data
        input_df = input_df[feature_names]
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]
        
        return {
            "prediction": int(prediction),
            "probability": float(probability),
            "churn_risk": "High" if probability > 0.7 else "Medium" if probability > 0.4 else "Low"
        }
        
    except Exception as e:
        print(f"Error making prediction: {e}")
        return {"error": str(e)}


@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({
        'status': 'OK',
        'message': 'Customer Churn Prediction API is running',
        'timestamp': pd.Timestamp.now().isoformat()
    })


@api_view(['GET'])
def get_features(request):
    """Get available features and their options"""
    features = [
        {'name': 'gender', 'type': 'categorical', 'options': ['Male', 'Female']},
        {'name': 'SeniorCitizen', 'type': 'binary', 'options': [0, 1]},
        {'name': 'Partner', 'type': 'categorical', 'options': ['Yes', 'No']},
        {'name': 'Dependents', 'type': 'categorical', 'options': ['Yes', 'No']},
        {'name': 'tenure', 'type': 'numerical', 'range': [0, 72]},
        {'name': 'PhoneService', 'type': 'categorical', 'options': ['Yes', 'No']},
        {'name': 'MultipleLines', 'type': 'categorical', 'options': ['Yes', 'No', 'No phone service']},
        {'name': 'InternetService', 'type': 'categorical', 'options': ['DSL', 'Fiber optic', 'No']},
        {'name': 'OnlineSecurity', 'type': 'categorical', 'options': ['Yes', 'No', 'No internet service']},
        {'name': 'OnlineBackup', 'type': 'categorical', 'options': ['Yes', 'No', 'No internet service']},
        {'name': 'DeviceProtection', 'type': 'categorical', 'options': ['Yes', 'No', 'No internet service']},
        {'name': 'TechSupport', 'type': 'categorical', 'options': ['Yes', 'No', 'No internet service']},
        {'name': 'StreamingTV', 'type': 'categorical', 'options': ['Yes', 'No', 'No internet service']},
        {'name': 'StreamingMovies', 'type': 'categorical', 'options': ['Yes', 'No', 'No internet service']},
        {'name': 'Contract', 'type': 'categorical', 'options': ['Month-to-month', 'One year', 'Two year']},
        {'name': 'PaperlessBilling', 'type': 'categorical', 'options': ['Yes', 'No']},
        {'name': 'PaymentMethod', 'type': 'categorical', 'options': ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)']},
        {'name': 'MonthlyCharges', 'type': 'numerical', 'range': [0, 200]},
        {'name': 'TotalCharges', 'type': 'numerical', 'range': [0, None]}
    ]
    return Response({'features': features})


@api_view(['POST'])
def predict(request):
    """Predict customer churn"""
    serializer = CustomerChurnSerializer(data=request.data)
    
    if serializer.is_valid():
        customer_data = serializer.validated_data
        prediction_result = predict_churn(customer_data)
        
        if 'error' in prediction_result:
            return Response(
                {'error': prediction_result['error']},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return Response({
            'success': True,
            'data': {
                'customer_data': customer_data,
                'prediction': prediction_result['prediction'],
                'probability': prediction_result['probability'],
                'churn_risk': prediction_result['churn_risk'],
                'interpretation': 'Customer is likely to churn' if prediction_result['prediction'] == 1 else 'Customer is likely to stay'
            }
        })
    else:
        return Response(
            {'error': 'Validation error', 'details': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
