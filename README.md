# MACHINE_LEARNING_1
MY FIRST SUCCESFUL MACHINE LEARNING PREDICTION MODEL
🚗 ARCHIT CAR PRICE PREDICTION SPECIALIST
A futuristic and intelligent web application that predicts the resale price of used cars based on key features like brand, model, year, fuel type, and kilometers driven. This project uses Machine Learning (Linear Regression) and is served via a Flask web interface with a robotic-themed UI (yellow + grey with nut-and-screw styling).

🔍 Features
Predicts used car prices based on historical data.

Auto-fills model options based on selected company.

Futuristic dark-themed UI with robotic design (yellow + grey).

Real-time model prediction via Flask API.

Frontend powered by HTML, CSS, and JavaScript.

Backend ML model trained using scikit-learn and saved using pickle.

🛠 Tech Stack
Frontend: HTML, CSS, JavaScript

Backend: Python, Flask

ML Model: Linear Regression (scikit-learn)

Data Handling: pandas, NumPy

🚀 How to Run Locally
Clone this repository:

git clone https://github.com/yourusername/car-price-prediction.git
cd car-price-prediction


Install dependencies:
Create a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
pip install -r requirements.txt

Run the Flask app:
python application.py
Open your browser and go to: http://127.0.0.1:5000

📦 Folder Structure

car-price-prediction/
│
├── static/                 # CSS and JavaScript files
│   ├── style.css
│   └── script.js
│
├── templates/              # HTML templates
│   └── index.html
│
├── application.py          # Main Flask application
├── LinearRegressionModel.pkl  # Trained ML model
├── requirements.txt
└── README.md


📈 Model Training
Model is trained using LinearRegression from scikit-learn.
Categorical features (company, name, fuel_type) are encoded using OneHotEncoder.
The model was evaluated across multiple train/test splits for highest r2_score.
Best model is saved as LinearRegressionModel.pkl using pickle.

🧪 Inputs Expected by the Model
python

['name', 'company', 'year', 'kms_driven', 'fuel_type']
Ensure the same input order and format is maintained both in training and during live prediction.

🤖 Future Enhancements
Add support for more ML models (Random Forest, XGBoost).
Enable user login and data history saving.
Add animated UI elements to simulate car dashboards.
Deploy on Render, Vercel, or Heroku.

🤝 Contribution
Feel free to fork this project and submit a pull request. Any contributions are welcome!

📧 Contact
Developer: Archit Nevagi
Email: architnevagi@gmail.com


