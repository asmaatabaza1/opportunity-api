from flask import Flask, request, jsonify
from gradio_client import Client
import os

app = Flask(__name__)

HF_SPACE_ID = "asmaaabd0/opportunity"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    volunteer_job_title = data.get('volunteer_job_title')
    volunteer_skills = data.get('volunteer_skills')
    opportunity_category = data.get('opportunity_category')
    opportunity_skills = data.get('opportunity_skills')

    if not all([volunteer_job_title, volunteer_skills, opportunity_category, opportunity_skills]):
        return jsonify({"error": "All fields are required"}), 400

    try:
        client = Client(HF_SPACE_ID)
        result = client.predict(
            volunteer_job_title,
            volunteer_skills,
            opportunity_category,
            opportunity_skills,
            api_name="/predict"
        )

        return jsonify({"recommendation": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "✅ Opportunity Recommendation API is running!"

# أهم تعديل هنا لتوافق Render:
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
