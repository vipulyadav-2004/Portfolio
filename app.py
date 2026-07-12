from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv
import os
import smtplib
import re
from time import time
from collections import defaultdict, deque
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

app = Flask(__name__)
app.debug = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

RATE_LIMIT_WINDOW_SECONDS = int(os.environ.get('CONTACT_RATE_WINDOW_SECONDS', '300'))
RATE_LIMIT_MAX_REQUESTS = int(os.environ.get('CONTACT_RATE_MAX_REQUESTS', '5'))
contact_rate_buckets = defaultdict(deque)


def get_client_ip():
    forwarded_for = request.headers.get('X-Forwarded-For', '')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return request.remote_addr or 'unknown'


def is_rate_limited(client_ip):
    now = time()
    bucket = contact_rate_buckets[client_ip]
    while bucket and now - bucket[0] > RATE_LIMIT_WINDOW_SECONDS:
        bucket.popleft()
    if len(bucket) >= RATE_LIMIT_MAX_REQUESTS:
        return True
    bucket.append(now)
    return False


def is_valid_email(email):
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email or ""))

def send_contact_email(name, sender_contact, message):
    receiver = os.environ.get('RECEIVER_EMAIL', 'yadavvipul707@gmail.com')
    sender = os.environ.get('SENDER_EMAIL')
    password = os.environ.get('SENDER_PASSWORD')
    smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', '587'))
    
    if not sender or not password:
        print("SMTP Credentials not set (SENDER_EMAIL / SENDER_PASSWORD). Logging submission to console.")
        return False, "Email service is not configured yet."
        
    try:
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = f"New Portfolio Contact Form Submission from {name}"
        msg['Reply-To'] = sender_contact
        
        body = f"New message received from your portfolio contact form:\n\nName: {name}\nEmail: {sender_contact}\n\nMessage:\n{message}"
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(smtp_host, smtp_port, timeout=15)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
        print(f"Email sent successfully to {receiver}")
        return True, "Message sent successfully!"
    except Exception as e:
        print(f"Error sending email: {e}")
        return False, "Could not send email right now. Please try again later."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/contact', methods=['POST'])
def contact():
    is_json_request = request.is_json
    client_ip = get_client_ip()

    if is_json_request:
        data = request.get_json(silent=True) or {}
    else:
        data = request.form.to_dict()

    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip()
    message = (data.get('message') or '').strip()
    website = (data.get('website') or '').strip()

    if website:
        success_message = "Message sent successfully!"
        if is_json_request:
            return jsonify({"success": True, "message": success_message}), 200
        return redirect(url_for('home', _anchor='contact', contact_status='success', contact_message=success_message))

    if is_rate_limited(client_ip):
        error_message = "Too many requests. Please wait a few minutes and try again."
        if is_json_request:
            return jsonify({"success": False, "message": error_message}), 429
        return redirect(url_for('home', _anchor='contact', contact_status='error', contact_message=error_message))

    if not name or not email or not message:
        error_message = "Please fill in name, email, and message."
        if is_json_request:
            return jsonify({"success": False, "message": error_message}), 400
        return redirect(url_for('home', _anchor='contact', contact_status='error', contact_message=error_message))

    if not is_valid_email(email):
        error_message = "Please enter a valid email address."
        if is_json_request:
            return jsonify({"success": False, "message": error_message}), 400
        return redirect(url_for('home', _anchor='contact', contact_status='error', contact_message=error_message))
    
    print("-" * 40)
    print("New Contact Form Submission:")
    print(f"IP:      {client_ip}")
    print(f"Name:    {name}")
    print(f"Email:   {email}")
    print(f"Message: {message}")
    print("-" * 40)
    
    # Send email notification
    sent, result_message = send_contact_email(name, email, message)

    if is_json_request:
        status_code = 200 if sent else 500
        return jsonify({"success": sent, "message": result_message}), status_code

    redirect_status = 'success' if sent else 'error'
    return redirect(url_for('home', _anchor='contact', contact_status=redirect_status, contact_message=result_message))
    
PROJECTS = {
    'data-science': [
        {
            'id': 'house-price-prediction',
            'title': 'House Price Prediction',
            'category': 'Regression Models',
            'subcategory': 'ml',
            'description': 'A robust machine learning model to predict house prices based on multiple housing features and geographic data.',
            'image': 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?q=80&w=2070&auto=format&fit=crop',
            'demo_link': 'https://github.com/vipulyadav-2004/House_price_prediction_ames',
            'code_link': 'https://github.com/vipulyadav-2004/House_price_prediction_ames'
        },
        {
            'id': 'digit-classification',
            'title': ' Handwritten Digit Classification',
            'category': 'SVM(Support Vector Machine) & Vision',
            'subcategory': 'cv',
            'description': 'A classification model utilizing Support Vector Machines (SVM) and OpenCV for recognizing handwritten digits. Employs morphological processing for image cleaning and grid-segmentation to improve recognition accuracy.',
            'image': 'https://images.unsplash.com/photo-1564630322990-4a9e93d13946?q=80&w=2070&auto=format&fit=crop',
            'demo_link': 'https://github.com/vipulyadav-2004/Handwritten-digit-classification',
            'code_link': 'https://github.com/vipulyadav-2004/Handwritten-digit-classification'
        },
        {
            'id': 'cluster-segmentation',
            'title': 'Cluster Segmentation - RFM',
            'category': 'Unsupervised Learning - Clusters and KNN',
            'subcategory': 'ml',
            'description': 'An analytics project using clustering algorithms to segment customers and discover underlying trends in unlabeled data.',
            'image': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=2015&auto=format&fit=crop',
            'demo_link': 'https://github.com/vipulyadav-2004/Customer-Segmentation-RFM',
            'code_link': 'https://github.com/vipulyadav-2004/Customer-Segmentation-RFM'
        },
        {
            'id': 'netflix-eda',
            'title': 'Netflix Movies & TV Shows EDA',
            'category': 'Exploratory Data Analysis & Visualization',
            'subcategory': 'eda',
            'description': 'An in-depth exploratory data analysis of Netflix content dataset. Cleansed and structured the raw dataset to extract insights regarding content growth over the years, geographic distribution of titles, and genre preferences using Matplotlib and Seaborn.',
            'image': 'https://images.unsplash.com/photo-1574375927938-d5a98e8edd86?q=80&w=2070&auto=format&fit=crop',
            'demo_link': 'https://github.com/vipulyadav-2004/Netflix-Data-Analysis',
            'code_link': 'https://github.com/vipulyadav-2004/Netflix-Data-Analysis'
        },
        {
            'id': 'sentiment-analyzer',
            'title': 'BERT Sentiment Analyzer',
            'category': 'Natural Language Processing',
            'subcategory': 'nlp',
            'description': 'A Natural Language Processing model utilizing fine-tuned BERT (Bidirectional Encoder Representations from Transformers) to perform sentiment analysis on movie and product reviews. Built using PyTorch and Hugging Face library, achieving high classification accuracy.',
            'image': 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=2070&auto=format&fit=crop',
            'demo_link': 'https://github.com/vipulyadav-2004/Sentiment-Analysis',
            'code_link': 'https://github.com/vipulyadav-2004/Sentiment-Analysis'
        },
        {
            'id': 'brain-tumor-segmentation',
            'title': 'Brain Tumor MRI Segmentation',
            'category': 'Deep Learning / Medical Image Vision',
            'subcategory': 'deep-learning',
            'description': 'A medical image segmentation pipeline utilizing a deep Convolutional Neural Network (U-Net) to identify and segment brain tumors in MRI scans. Optimized using dice loss and binary cross-entropy, delivering high intersection-over-union scores for medical diagnostics.',
            'image': 'https://images.unsplash.com/photo-1559757175-5700dde675bc?q=80&w=2070&auto=format&fit=crop',
            'demo_link': 'https://github.com/vipulyadav-2004/Brain-Tumor-Segmentation',
            'code_link': 'https://github.com/vipulyadav-2004/Brain-Tumor-Segmentation'
        },
        {
            'id': 'ipl-score-metrics',
            'title': 'IPL Score Metrics Analysis',
            'category': 'Analysis & Visualization',
            'subcategory': 'eda',
            'description': 'A comprehensive analysis and visualization project exploring IPL cricket match data, uncovering scoring patterns, team performance metrics, and player statistics through interactive charts and dashboards.',
            'image': 'https://images.unsplash.com/photo-1531415074968-036ba1b575da?q=80&w=2067&auto=format&fit=crop',
            'demo_link': 'https://github.com/vipulyadav-2004/IPL-Score-Metrics-Analysis',
            'code_link': 'https://github.com/vipulyadav-2004/IPL-Score-Metrics-Analysis'
        },
        {
            'id': 'customer-churn-prediction',
            'title': 'Customer Churn Prediction',
            'category': 'Machine Learning - Survival Analysis',
            'subcategory': 'ml',
            'description': 'A survival analysis model leveraging the Cox Proportional Hazards framework to predict customer churn probability over time, identifying key risk factors and estimating customer lifetime with hazard ratios and survival curves.',
            'image': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=2070&auto=format&fit=crop',
            'demo_link': 'https://github.com/vipulyadav-2004/Customer-Churn-Prediction',
            'code_link': 'https://github.com/vipulyadav-2004/Customer-Churn-Prediction'
        },
        {
            'id': 'resume-screening-app',
            'title': 'Resume Screening App',
            'category': 'Machine Learning - NLP',
            'subcategory': 'nlp',
            'description': 'An intelligent resume screening application that ranks and filters candidate resumes using TF-IDF vectorization and Sentence Transformers for semantic similarity matching, streamlining the recruitment pipeline.',
            'image': 'https://images.unsplash.com/photo-1586281380349-632531db7ed4?q=80&w=2070&auto=format&fit=crop',
            'demo_link': 'https://github.com/vipulyadav-2004/Resume-Screening-App',
            'code_link': 'https://github.com/vipulyadav-2004/Resume-Screening-App'
        },
        {
            'id': 'face-mask-detector',
            'title': 'Face Mask Detector',
            'category': 'OpenCV & Deep Learning',
            'subcategory': 'deep-learning',
            'description': 'A real-time face mask detection system combining OpenCV Cascade Classifiers for face localization with a neural network built using PyTorch\'s nn module and Torchvision for mask/no-mask classification on live video feeds.',
            'image': 'https://images.unsplash.com/photo-1585559604959-6388fe69c92a?q=80&w=2070&auto=format&fit=crop',
            'demo_link': 'https://github.com/vipulyadav-2004/Face-Mask-Detector',
            'code_link': 'https://github.com/vipulyadav-2004/Face-Mask-Detector'
        }
    ],
    'web-development': [
        {
            'id': 'ayushara',
            'title': 'Ayushara',
            'category': 'A Dedicated Platform for Writers and Poets',
            'description': 'A full-stack web application tailored for writers and poets to publish their work and build an audience.',
            'image': 'assets/images/Ayushara.png',
            'demo_link': '#',
            'code_link': 'https://github.com/vipulyadav-2004/Ayushara'
        },
        {
            'id': 'flask-todo',
            'title': 'To-Do App (Flask)',
            'category': 'Full-Stack Python Backend',
            'description': 'A robust To-Do list application built with a Flask backend to manage tasks efficiently, featuring full CRUD operations and dynamic routing.',
            'image': 'https://images.unsplash.com/photo-1540350394557-8d14678e7f91?q=80&w=2032&auto=format&fit=crop',
            'demo_link': '#',
            'code_link': 'https://github.com/vipulyadav-2004/Flask-Todo-App'
        },
        {
            'id': 'weather-web',
            'title': 'Weather Web App',
            'category': 'Frontend / HTML, CSS, JS',
            'description': 'A dynamic weather forecasting application built purely with HTML, CSS, and Vanilla JavaScript, integrating asynchronous live API data.',
            'image': 'https://images.unsplash.com/photo-1592210454359-9043f067919b?q=80&w=2070&auto=format&fit=crop',
            'demo_link': 'https://collaborative-todo-uagn.onrender.com/',
            'code_link': 'https://github.com/vipulyadav-2004/Weather-Web-App'
        },
      
    ],
    'internship-work': [
        {
            'id': 'dubai-house-price',
            'title': 'Dubai House Price Analysis',
            'category': 'Dashboarding / BI',
            'description': 'A comprehensive BI dashboard analyzing historical Dubai real estate pricing trends and spatial house market distributions.',
            'image': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070&auto=format&fit=crop',
            'demo_link': '#',
            'code_link': 'https://github.com/vipulyadav-2004/Dubai-House-Price-Analysis'
        },
        {
            'id': 'phonepe-pulse',
            'title': 'PhonePe Pulse Visualization',
            'category': 'Data Visualization / Interactive Dashboard',
            'description': 'An interactive visualization suite that renders India-wide transaction metrics and trends utilizing PhonePe open pulse data.',
            'image': 'assets/images/Phonepe.webp',
            'demo_link': '#',
            'code_link': 'https://github.com/vipulyadav-2004/PhonePe-Pulse'
        },
        {
            'id': 'video-game-sales',
            'title': 'Video Game Sales Analysis',
            'category': 'EDA + SQL + Dashboard',
            'description': 'An end-to-end data pipeline containing exploratory data analysis (EDA), advanced SQL querying, and a final BI dashboard tracking global game sales.',
            'image': 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?q=80&w=2070&auto=format&fit=crop',
            'demo_link': '#',
            'code_link': 'https://github.com/vipulyadav-2004/Video-Game-Sales-Analysis'
        },
         {
            'id': 'bird-species-analysis',
            'title': 'Birds Species Analysis',
            'category': 'EDA + SQL + Streamlit',
            'description': 'An end-to-end data pipeline containing exploratory data analysis (EDA), advanced SQL querying, and a final streamlit dashboard tracking global birds species.',
            'image': 'https://images.unsplash.com/photo-1484704324500-528d0ae4dc7d?q=80&w=870&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            'demo_link': '#',
            'code_link': 'https://github.com/vipulyadav-2004/Bird-Species-Analysis'
        },
         {
            'id': 'food-waste-management',
            'title': 'Food Waste Management',
            'category': 'EDA + SQL + Streamlit',
            'description': 'An end-to-end data pipeline containing exploratory data analysis (EDA), advanced SQL querying, and a final streamlit web for food waste management.',
            'image': 'https://images.unsplash.com/photo-1542624771497-851f77d79349?q=80&w=866&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            'demo_link': '#',
            'code_link': 'https://github.com/vipulyadav-2004/Food-Waste-Management'
        }
    ]
}

CATEGORY_INFO = {
    'data-science': {
        'title': 'Data Science & Analytics',
        'description': 'Explore my projects focusing on AI, Machine Learning algorithms, and insightful Data Analytics.'
    },
    'web-development': {
        'title': 'Web Development',
        'description': 'Explore my robust, scalable full-stack web applications and interactive UI designs.'
    },
    'internship-work': {
        'title': 'Internship Work',
        'description': 'Explore professional projects and contributions made during my industry internships.'
    }
}

from flask import abort

@app.route('/category/<category_id>')
def category_detail(category_id):
    info = CATEGORY_INFO.get(category_id)
    projects = PROJECTS.get(category_id)
    if not info or projects is None:
        abort(404)
    return render_template('category.html', info=info, projects=projects, category_id=category_id)

@app.route('/project/<project_id>')
def project_detail(project_id):
    # Search for project within categories
    for category_id, cat_projects in PROJECTS.items():
        for p in cat_projects:
            if p['id'] == project_id:
                return render_template('project.html', project=p, category_id=category_id)
    abort(404)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
