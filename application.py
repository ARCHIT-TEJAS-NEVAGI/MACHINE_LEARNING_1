from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)
cors = CORS(app)

# Load model and data
try:
    model = pickle.load(open('LinearRegressionModel.pkl', 'rb'))
    car = pd.read_csv('Cleaned cars data.csv')
    if 'Unnamed: 0' in car.columns:
        car = car.drop('Unnamed: 0', axis=1)
    print("Model and data loaded successfully!")
    
    # Get unique values from the dataset
    VALID_COMPANIES = sorted(car['company'].unique())
    VALID_MODELS = sorted(car['name'].unique())
    VALID_YEARS = sorted(car['year'].unique(), reverse=True)
    VALID_FUEL_TYPES = sorted(car['fuel_type'].unique())
    
    print(f"Loaded {len(VALID_COMPANIES)} companies")
    print(f"Loaded {len(VALID_MODELS)} models")
    print(f"Years range: {min(VALID_YEARS)} - {max(VALID_YEARS)}")
    print(f"Fuel types: {VALID_FUEL_TYPES}")
    
    # Create company to model mapping
    COMPANY_MODELS = {company: sorted(car[car['company'] == company]['name'].unique()) 
                     for company in VALID_COMPANIES}
    
except Exception as e:
    print(f"Error loading model or data: {e}")
    VALID_COMPANIES = []
    VALID_MODELS = []
    VALID_YEARS = []
    VALID_FUEL_TYPES = []
    COMPANY_MODELS = {}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', 
                         companies=VALID_COMPANIES,
                         years=VALID_YEARS,
                         fuel_types=VALID_FUEL_TYPES)

@app.route('/get_models', methods=['POST'])
def get_models():
    try:
        company = request.json.get('company')
        if not company:
            return jsonify({'error': 'Company name is required'}), 400
            
        # Get models for the selected company
        company_models = COMPANY_MODELS.get(company, [])
        
        if not company_models:
            return jsonify({'error': f'No models found for company: {company}'}), 404
            
        return jsonify(company_models)
    except Exception as e:
        print(f"Error in get_models: {e}")
        return jsonify({'error': 'Failed to fetch car models'}), 400

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print("\nReceived prediction request:", data)  # Debug print
        
        # Extract and validate input data
        company = data['company'].strip()
        car_model = data['car_model'].strip()
        year = int(data['year'])
        kms_driven = int(data['kilo_driven'])
        fuel_type = data['fuel_type'].strip()
        
        # Validate inputs against known values
        if company not in VALID_COMPANIES:
            raise ValueError(f"Invalid company: {company}")
        if car_model not in COMPANY_MODELS[company]:
            raise ValueError(f"Invalid model for {company}: {car_model}")
        if year not in VALID_YEARS:
            raise ValueError(f"Invalid year: {year}")
        if fuel_type not in VALID_FUEL_TYPES:
            raise ValueError(f"Invalid fuel type: {fuel_type}")
        if kms_driven < 0:
            raise ValueError("Kilometers driven cannot be negative")

        # Create DataFrame with exact column order as training data
        input_df = pd.DataFrame([[car_model, company, year, kms_driven, fuel_type]], 
                              columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'])
        
        # Debug prints
        print("\nPrediction Input DataFrame:")
        print(input_df)
        print("\nColumn Order:", input_df.columns.tolist())
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        formatted_price = f"₹ {int(prediction):,}"
        
        print(f"Prediction successful: {formatted_price}")
        return jsonify({'price': formatted_price})
        
    except ValueError as ve:
        print(f"Validation error: {ve}")
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        print(f"Prediction error:", str(e))
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Prediction failed. Please try again.'}), 500

if __name__ == '__main__':
    app.run(debug=True)