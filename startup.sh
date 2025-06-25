# gunicorn -b 0.0.0.0:8000 --timeout 600 app:app

#!/bin/bash

export FLASK_APP=app.py
export FLASK_ENV=production

# Jalankan Flask server
python3 -m flask run --host=0.0.0.0 --port=8000
