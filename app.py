from flask import Flask, render_template, request, jsonify
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.debug = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

def send_contact_email(name, sender_contact, message):
    receiver = os.environ.get('RECEIVER_EMAIL', 'yadavvipul707@gmail.com')
    sender = os.environ.get('SENDER_EMAIL')
    password = os.environ.get('SENDER_PASSWORD')
    
    if not sender or not password:
        print("SMTP Credentials not set (SENDER_EMAIL / SENDER_PASSWORD). Logging submission to console.")
        return False
        
    try:
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = f"New Portfolio Contact Form Submission from {name}"
        
        body = f"New message received from your portfolio contact form:\n\nName: {name}\nEmail: {sender_contact}\n\nMessage:\n{message}"
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
        print(f"Email sent successfully to {receiver}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
        
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    
    print("-" * 40)
    print("New Contact Form Submission:")
    print(f"Name:    {name}")
    print(f"Email:   {email}")
    print(f"Message: {message}")
    print("-" * 40)
    
    # Send email notification
    send_contact_email(name, email, message)
    
    return jsonify({"success": True, "message": "Message sent successfully!"})
    
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
    app.run(debug=True, port=5000)
