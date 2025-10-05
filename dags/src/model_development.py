import pandas as pd
import os
import pickle
from datetime import datetime
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.compose import make_column_transformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
import numpy as np

def load_data():
    """Loads advertising data from CSV file."""
    # Try multiple paths to find the CSV
    possible_paths = [
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "advertising.csv"),  # dags/data/advertising.csv
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "advertising.csv"),  # root/advertising.csv
        "/home/mlops_fall_2024/advertising.csv",  # absolute path if deployed
        "advertising.csv"  # fallback
    ]
    
    for csv_path in possible_paths:
        if os.path.exists(csv_path):
            print(f"Loading data from: {csv_path}")
            data = pd.read_csv(csv_path)
            return data
    
    raise FileNotFoundError(f"Could not find advertising.csv. Tried: {possible_paths}")
def print_data_summary(data):
    """Print dataset statistics."""
    print("\n=== Dataset Summary ===")
    print(f"Total Samples: {len(data)}")
    print(f"Features: {data.columns.tolist()}")
    print(f"\nTarget Distribution:")
    print(data['Clicked on Ad'].value_counts())
    print(f"\nAge Statistics:")
    print(data['Age'].describe())
    print(f"\nIncome Statistics:")
    print(data['Area Income'].describe())
    return True

def data_preprocessing(data):
    """Preprocess data by splitting features/target and applying scaling."""
    X = data.drop(['Timestamp', 'Clicked on Ad', 'Ad Topic Line', 'Country', 'City'], axis=1)
    y = data['Clicked on Ad']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    num_columns = ['Daily Time Spent on Site', 'Age', 'Area Income', 'Daily Internet Usage', 'Male']

    ct = make_column_transformer(
        (MinMaxScaler(), num_columns),
        (StandardScaler(), num_columns),
        remainder='passthrough'
    )

    X_train = ct.fit_transform(X_train)
    X_test = ct.transform(X_test)

    return X_train.tolist(), X_test.tolist(), y_train.tolist(), y_test.tolist()

def build_model(data, filename):
    """Train multiple models, compare performance, and save the best one."""
    X_train, X_test, y_train, y_test = data
    X_train = np.array(X_train)
    X_test = np.array(X_test)
    y_train = np.array(y_train)
    y_test = np.array(y_test)
    
    # Train 3 different models
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Decision Tree': DecisionTreeClassifier(random_state=42)
    }
    
    best_model = None
    best_score = 0
    best_name = ""
    all_scores = {}
    
    print("\n=== Model Comparison ===")
    for name, model in models.items():
        model.fit(X_train, y_train)
        score = model.score(X_test, y_test)
        all_scores[name] = score
        print(f"{name}: {score:.4f}")
        
        if score > best_score:
            best_score = score
            best_model = model
            best_name = name
    
    print(f"\nBest Model: {best_name} with accuracy {best_score:.4f}")
    
    # Save model
    output_dir = os.path.join(os.path.dirname(__file__), "../model")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_path = os.path.join(output_dir, filename)
    pickle.dump(best_model, open(output_path, 'wb'))
    
    metadata = {
        'best_model': best_name,
        'accuracy': best_score,
        'all_scores': all_scores,
        'timestamp': str(datetime.now()),
        'model_path': output_path
    }
    
    print(f"Model saved to: {output_path}")
    return metadata

def load_model(data, filename):
    """Load a saved model and make predictions."""
    X_train, X_test, y_train, y_test = data
    output_path = os.path.join(os.path.dirname(__file__), "../model", filename)
    
    loaded_model = pickle.load(open(output_path, 'rb'))
    predictions = loaded_model.predict(X_test)
    print(f"Model score on test data: {loaded_model.score(X_test, y_test)}")
    
    return predictions[0]

if __name__ == '__main__':
    x = load_data()
    print_data_summary(x)
    x = data_preprocessing(x)
    metadata = build_model(x, 'ad_click_model.sav')
    print(f"\nMetadata: {metadata}")