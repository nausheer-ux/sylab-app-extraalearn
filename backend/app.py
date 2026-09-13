import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize Flask app with a name
app = Flask("ExtraaLearn Lead Conversion Predictor")

# Load the trained lead conversion model
model = joblib.load("backend_files/lead_conversion_model_v1_0.joblib")

# Define a route for the home page
@app.get('/')
def home():
    return "Welcome to the ExtraaLearn Lead Conversion Prediction API"

# Define an endpoint to predict lead conversion for a single lead
@app.post('/v1/lead')
def predict_lead():
    # Get JSON data from the request
    lead_data = request.get_json()

    # Extract relevant lead features from the input data matching ExtraaLearn dataset features
    sample = {
        'age': lead_data['age'],
        'current_occupation': lead_data['current_occupation'],
        'first_interaction': lead_data['first_interaction'],
        'profile_completed': lead_data['profile_completed'],
        'website_visits': lead_data['website_visits'],
        'time_spent_on_website': lead_data['time_spent_on_website'],
        'page_views_per_visit': lead_data['page_views_per_visit'],
        'last_activity': lead_data['last_activity'],
        'print_media_type1': lead_data['print_media_type1'],
        'print_media_type2': lead_data['print_media_type2'],
        'digital_media': lead_data['digital_media'],
        'educational_channels': lead_data['educational_channels'],
        'referral': lead_data['referral']
    }

    # Convert the extracted data into a DataFrame
    input_data = pd.DataFrame([sample])

    # Make a conversion prediction using the trained model
    prediction = model.predict(input_data).tolist()[0]

    # Map prediction result to a human-readable label
    prediction_label = "Converted" if prediction == 1 else "Not Converted"

    # Return the prediction as a JSON response
    return jsonify({'Prediction': prediction_label})

# Define an endpoint to predict lead conversion for a batch of leads
@app.post('/v1/leadbatch')
def predict_lead_batch():
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the file into a DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for the batch data and convert raw predictions into a readable format
    predictions = [
        'Converted' if x == 1
        else "Not Converted"
        for x in model.predict(input_data.drop("ID", axis=1)).tolist()
    ]

    lead_id_list = input_data.ID.values.tolist()
    output_dict = dict(zip(lead_id_list, predictions))

    return output_dict

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
