from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.debug = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

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
    
    # Normally you would save this to a database or send an email here.
    print("-" * 40)
    print("New Contact Form Submission:")
    print(f"Name:    {name}")
    print(f"Email:   {email}")
    print(f"Message: {message}")
    print("-" * 40)
    
    return jsonify({"success": True, "message": "Message sent successfully!"})
    
PROJECTS = {
    'data-science': [
        {
            'id': 'house-price-prediction',
            'title': 'House Price Prediction',
            'category': 'Regression Models',
            'description': 'A robust machine learning model to predict house prices based on multiple housing features and geographic data.',
            'image': 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?q=80&w=2070&auto=format&fit=crop',
            'demo_link': 'https://github.com/vipulyadav-2004/House_price_prediction_ames'
        },
        {
            'id': 'digit-classification',
            'title': ' Handwritten Digit Classification',
            'category': 'SVM(Support Vector Machine) & Vision',
            'description': 'A neural network architecture developed to classify handwritten digits with high accuracy using standard datasets.',
            'image': 'assets/images/Screenshot2026-03-05 222854.png',
            'demo_link': 'https://github.com/vipulyadav-2004/Handwritten-digit-classification'
        },
        {
            'id': 'cluster-segmentation',
            'title': 'Cluster Segmentation - RFM',
            'category': 'Unsupervised Learning - Clusters and KNN',
            'description': 'An analytics project using clustering algorithms to segment customers and discover underlying trends in unlabeled data.',
            'image': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=2015&auto=format&fit=crop',
            'demo_link': 'https://github.com/vipulyadav-2004/Customer-Segmentation-RFM'
        }
    ],
    'web-development': [
        {
            'id': 'ayushara',
            'title': 'Ayushara',
            'category': 'A Dedicated Platform for Writers and Poets',
            'description': 'A full-stack web application tailored for writers and poets to publish their work and build an audience.',
            'image': 'assets/images/Ayushara.png',
            'demo_link': '#'
        },
        {
            'id': 'flask-todo',
            'title': 'To-Do App (Flask)',
            'category': 'Full-Stack Python Backend',
            'description': 'A robust To-Do list application built with a Flask backend to manage tasks efficiently, featuring full CRUD operations and dynamic routing.',
            'image': 'https://images.unsplash.com/photo-1540350394557-8d14678e7f91?q=80&w=2032&auto=format&fit=crop',
            'demo_link': '#'
        },
        {
            'id': 'weather-web',
            'title': 'Weather Web App',
            'category': 'Frontend / HTML, CSS, JS',
            'description': 'A dynamic weather forecasting application built purely with HTML, CSS, and Vanilla JavaScript, integrating asynchronous live API data.',
            'image': 'https://images.unsplash.com/photo-1592210454359-9043f067919b?q=80&w=2070&auto=format&fit=crop',
            'demo_link': 'https://collaborative-todo-uagn.onrender.com/'
        },
      
    ],
    'internship-work': [
        {
            'id': 'dubai-house-price',
            'title': 'Dubai House Price Analysis',
            'category': 'Dashboarding / BI',
            'description': 'A comprehensive BI dashboard analyzing historical Dubai real estate pricing trends and spatial house market distributions.',
            'image': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070&auto=format&fit=crop',
            'demo_link': '#'
        },
        {
            'id': 'phonepe-pulse',
            'title': 'PhonePe Pulse Visualization',
            'category': 'Data Visualization / Interactive Dashboard',
            'description': 'An interactive visualization suite that renders India-wide transaction metrics and trends utilizing PhonePe open pulse data.',
            'image': 'assets/images/Phonepe.webp',
            'demo_link': '#'
        },
        {
            'id': 'video-game-sales',
            'title': 'Video Game Sales Analysis',
            'category': 'EDA + SQL + Dashboard',
            'description': 'An end-to-end data pipeline containing exploratory data analysis (EDA), advanced SQL querying, and a final BI dashboard tracking global game sales.',
            'image': 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?q=80&w=2070&auto=format&fit=crop',
            'demo_link': '#'
        },
         {
            'id': 'bird-species-analysis',
            'title': 'Birds Species Analysis',
            'category': 'EDA + SQL + Streamlit',
            'description': 'An end-to-end data pipeline containing exploratory data analysis (EDA), advanced SQL querying, and a final streamlit dashboard tracking global birds species.',
            'image': 'https://images.unsplash.com/photo-1484704324500-528d0ae4dc7d?q=80&w=870&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            'demo_link': '#'
        },
         {
            'id': 'food-waste-management',
            'title': 'Food Waste Management',
            'category': 'EDA + SQL + Streamlit',
            'description': 'An end-to-end data pipeline containing exploratory data analysis (EDA), advanced SQL querying, and a final streamlit web for food waste management.',
            'image': 'https://images.unsplash.com/photo-1542624771497-851f77d79349?q=80&w=866&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            'demo_link': '#'
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
