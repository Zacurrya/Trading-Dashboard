#!/bin/bash

cd PythonProject
source .venv/Scripts/activate 

pip install -r requirements.txt

echo "Launching Dashboard..."
streamlit run dashboard.py