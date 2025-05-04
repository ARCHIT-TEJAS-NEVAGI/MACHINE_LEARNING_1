document.addEventListener('DOMContentLoaded', function() {
    const companySelect = document.getElementById('company');
    const modelSelect = document.getElementById('car_model');
    const form = document.getElementById('predict-form');
    const resultDiv = document.getElementById('result');

    // Helper function to show error messages
    function showError(message) {
        resultDiv.innerHTML = `<div class="error">${message}</div>`;
    }

    // Helper function to show loading state
    function showLoading() {
        resultDiv.innerHTML = '<div class="loader"></div>';
    }

    companySelect.addEventListener('change', function() {
        const company = this.value;
        modelSelect.innerHTML = '<option value="">Loading...</option>';
        modelSelect.disabled = true;

        if (!company) {
            modelSelect.innerHTML = '<option value="">Select Model</option>';
            modelSelect.disabled = false;
            return;
        }

        fetch('/get_models', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({company: company})
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            modelSelect.innerHTML = '<option value="">Select Model</option>';
            data.forEach(model => {
                const opt = document.createElement('option');
                opt.value = model;
                opt.textContent = model;
                modelSelect.appendChild(opt);
            });
        })
        .catch(error => {
            modelSelect.innerHTML = '<option value="">Error loading models</option>';
            console.error('Error:', error);
        })
        .finally(() => {
            modelSelect.disabled = false;
        });
    });

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        showLoading();

        // Validate inputs
        const kilosDriven = document.getElementById('kilo_driven').value;
        if (kilosDriven < 0) {
            showError("Kilometers driven cannot be negative");
            return;
        }

        const data = {
            company: companySelect.value,
            car_model: modelSelect.value,
            year: document.getElementById('year').value,
            fuel_type: document.getElementById('fuel_type').value,
            kilo_driven: kilosDriven
        };

        // Validate all fields are filled
        for (let key in data) {
            if (!data[key]) {
                showError(`Please fill in all fields (${key} is missing)`);
                return;
            }
        }

        fetch('/predict', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            resultDiv.innerHTML = `<div class="prediction">${data.price}</div>`;
        })
        .catch(error => {
            showError(error.message || "Prediction failed. Please check your input.");
            console.error('Error:', error);
        });
    });
});