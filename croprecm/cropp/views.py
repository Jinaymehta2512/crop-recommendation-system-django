import os
import pickle
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CropRecommendationSerializer
import numpy as np
from django.shortcuts import render

# Load the model with the correct path
model_path = os.path.join(settings.BASE_DIR, 'cropp', 'model', 'model.pkl')

with open(model_path, 'rb') as f:
    model = pickle.load(f)

# Crop dictionary to map numeric predictions to crop names
crop_dict = {
    1: 'rice',
    2: 'maize',
    3: 'jute',
    4: 'cotton',
    5: 'coconut',
    6: 'papaya',
    7: 'orange',
    8: 'apple',
    9: 'muskmelon',
    10: 'watermelon',
    11: 'grapes',
    12: 'mango',
    13: 'banana',
    14: 'pomegranate',
    15: 'lentil',
    16: 'blackgram',
    17: 'mungbean',
    18: 'mothbeans',
    19: 'pigeonpeas',
    20: 'kidneybeans',
    21: 'chickpea',
    22: 'coffee'
}

@api_view(['POST'])
def recommend_crop(request):
    serializer = CropRecommendationSerializer(data=request.data)
    if serializer.is_valid():
        N = serializer.validated_data['N']
        P = serializer.validated_data['P']
        K = serializer.validated_data['K']
        temperature = serializer.validated_data['temperature']
        humidity = serializer.validated_data['humidity']
        ph = serializer.validated_data['ph']
        rainfall = serializer.validated_data['rainfall']

        # Prepare the input for the model
        input_features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])

        # Get prediction (numeric value)
        predicted_crop_number = model.predict(input_features)[0]

        # Map the predicted number to the crop name using crop_dict
        predicted_crop_name = crop_dict.get(predicted_crop_number, "Unknown crop")

        # Return the response with the crop name
        return Response({'recommended_crop': predicted_crop_name})
    return Response(serializer.errors, status=400)



def crop_recommendation_page(request):
    return render(request, 'crop_recommendation.html')