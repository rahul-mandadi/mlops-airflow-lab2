#!/bin/bash

echo "=========================================="
echo "Setting up Airflow 3.0 Lab 3 Environment"
echo "=========================================="
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv airflow_new_venv

# Activate virtual environment
echo "Activating virtual environment..."
source airflow_new_venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install Airflow 3.0
echo "Installing Apache Airflow 3.0.6..."
pip install apache-airflow==3.0.6

# Install other dependencies
echo "Installing dependencies..."
pip install scikit-learn pandas numpy

# Set Airflow home
export AIRFLOW_HOME=$(pwd)/airflow

# Initialize Airflow database
echo "Initializing Airflow database..."
airflow db migrate

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Create admin user (run this command):"
echo "   airflow users create --username admin --firstname Admin --lastname User --role Admin --email admin@example.com"
echo ""
echo "2. To start Airflow, open 2 terminals:"
echo ""
echo "   Terminal 1 (Webserver):"
echo "   source airflow_new_venv/bin/activate"
echo "   export AIRFLOW_HOME=\$(pwd)/airflow"
echo "   airflow webserver --port 8080"
echo ""
echo "   Terminal 2 (Scheduler):"
echo "   source airflow_new_venv/bin/activate"
echo "   export AIRFLOW_HOME=\$(pwd)/airflow"
echo "   airflow scheduler"
echo ""