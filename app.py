"""
Main Flask application file for the CekFakta AI Chatbot.

This file sets up the Flask web server, defines API endpoints for text analysis
and health checks, and integrates with the CekFakta AI Service.
It uses Flask-CORS to handle cross-origin requests.
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from services.ai_service import CekFaktaAIService   
from config.azure_config import AzureConfig
import os
import logging
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))

app = Flask(__name__)
app.config['SECRET_KEY'] = AzureConfig.SECRET_KEY
CORS(app)

# Initialize AI Service
ai_service = CekFaktaAIService()

@app.route('/')
def index():
    """Renders the main landing page."""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """
    Analyzes the input text for fact-checking.

    This endpoint receives a JSON payload with a 'text' field. It validates
    the input and passes it to the CekFaktaAIService for analysis. It handles
    various success and failure scenarios from the service.

    Request Body:
        {
            "text": "The text to be analyzed."
        }

    Responses:
        - 200 OK: Analysis was successful.
            {
                "success": true,
                "result": { ...analysis_result... }
            }
        - 200 OK (with fallback): The service had a partial error but provided a fallback explanation.
            {
                "success": true,
                "result": { "error": "...", "penjelasan": "..." }
            }
        - 400 Bad Request: The input text is empty or invalid.
        - 500 Internal Server Error: An error occurred either in the AI service
          or within the server itself.

    Returns:
        A JSON response tuple containing the data and a status code.
        The data includes the analysis result or an error message.
    """
    try:
        data = request.get_json()
        text = data.get('text', '')
        # Tidak perlu decode base64

        # Validasi unicode-aware (bisa handle teks Arab, dll)
        if not isinstance(text, str) or not any(c.strip() for c in text):
            return jsonify({
                'success': False,
                'error': 'Teks tidak boleh kosong'
            }), 400

        result = ai_service.analyze_text(text)

        # Handle cases where the model returns an error but also a fallback explanation.
        # This is treated as a "successful" response to the client.
        if 'error' in result and 'penjelasan' in result:
            return jsonify({
                'success': True,
                'result': result
            }), 200

        # Handle a complete failure from the AI service.
        if 'error' in result:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500

        # Normal successful response.
        return jsonify({
            'success': True,
            'result': result
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Terjadi kesalahan server: {str(e)}'
        }), 500


@app.route('/api/health')
def health_check():
    """
    Provides a simple health check endpoint.

    Returns:
        A JSON response indicating the service status.
    """
    return jsonify({'status': 'healthy', 'service': 'CekFakta AI'})

if __name__ == '__main__':
    # Runs the Flask app in debug mode.
    # The host '0.0.0.0' makes the server accessible from any network interface.
    app.run(debug=True, host='0.0.0.0', port=5000)