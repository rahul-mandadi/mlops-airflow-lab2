import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from airflow.sdk.bases.hook import BaseHook  # Changed

def send_success_email(**kwargs):
    """Send a success email with model training results."""
    try:
        conn = BaseHook.get_connection('email_smtp')
        sender_email = conn.login
        password = conn.password
    except:
        print("Email connection 'email_smtp' not configured. Skipping email.")
        return
    
    receiver_emails = 'your_email@example.com'  # UPDATE THIS
    
    # Get model info from previous task
    ti = kwargs.get('ti')
    model_info = ti.xcom_pull(task_ids='build_save_model_task') if ti else {}
    
    best_model = model_info.get('best_model', 'Unknown')
    accuracy = model_info.get('accuracy', 'N/A')
    all_scores = model_info.get('all_scores', {})
    timestamp = model_info.get('timestamp', 'Unknown')
    
    # Format accuracy
    accuracy_str = f"{accuracy:.2%}" if isinstance(accuracy, float) else str(accuracy)
    
    # Format all model scores
    scores_text = "\n".join([f"  - {name}: {score:.2%}" for name, score in all_scores.items()])
    
    # Define subject and body
    subject = f'Airflow Success: {kwargs["dag"].dag_id} - Ad Click Prediction Model Ready'
    
    body = f'''Hi Team,

The Ad Click Prediction pipeline has completed successfully!

MODEL COMPARISON RESULTS:
{scores_text}

BEST MODEL SELECTED:
  - Algorithm: {best_model}
  - Accuracy: {accuracy_str}
  - Trained: {timestamp}

DATASET INFO:
  - Name: Advertising Click Data
  - Samples: 1000
  - Task: Binary Classification

PIPELINE STAGES COMPLETED:
  1. Data Loading
  2. Data Summary & Validation
  3. Data Preprocessing
  4. Model Training (3 algorithms)
  5. Model Comparison & Selection
  6. Model Saved Successfully

Best regards,
Airflow MLOps Bot
'''
    
    # Create email
    email_message = MIMEMultipart()
    email_message['Subject'] = subject
    email_message['From'] = sender_email
    email_message['To'] = receiver_emails
    email_message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_emails, email_message.as_string())
        print(f"Success email sent to {receiver_emails}!")
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        try:
            server.quit()
        except:
            pass