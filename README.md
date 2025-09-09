# Book Recommendation Engine

A smart web application that suggests books you'll love based on your reading preferences. Powered by machine learning and beautiful design.


## Features
- **Personalized Recommendations**: Get book suggestions based on your favorites
- **Beautiful Interface**: Custom-designed with elegant colors and smooth animations
- **Instant Results**: Fast recommendations powered by machine learning algorithms
- **Detailed Book Information**: Explore authors, categories, and descriptions
- **Responsive Design**: Works perfectly on desktop and mobile devices

## Live Demo
**Experience the app now:**  
https://books-prdb.onrender.com

## Built With
- **Python** - Core programming language
- **Streamlit** - Web application framework
- **Pandas** - Data processing and analysis
- **Scikit-learn** - Machine learning algorithms
- **NLTK** - Natural language processing

## Installation
1. **Clone the repository**

git clone https://github.com/heli-sun/Books
cd book-recommendation


2. **Install dependencies**

pip install -r requirements.txt


3. **Run the application**

streamlit run app.py


4. **Open your browser** and navigate to `http://localhost:8501`

## Project Structure

book-recommendation/

├── 01_app.py                 # Main application

├── 02_recommender.py         # Recommendation algorithm  

├── 03_data_fetcher.py        # Data loading and processing

├── 04_books_data.csv         # Book dataset

├── 05_requirements.txt       # Dependencies

├── 06_bookshop.jpg           # Background image

├── 07_favicon.png            # Icon image

└── 08_README.md              # Documentation


## How to Use
1. **Enter** a book title you enjoy in the search box
2. **Click** "Find similar books" 
3. **Explore** recommendations including:
   - Books by the same author
   - Books with similar genres and themes
   - Detailed information about each suggestion

## How It Works
The system uses advanced machine learning techniques:
- **Content-based filtering** to match book features
- **Cosine similarity** to find the closest matches
- **TF-IDF vectorization** to analyze text content
- **Natural language processing** to understand book descriptions

## Deployment
Deployed on **Render** cloud platform with:
- Automatic continuous deployment from GitHub
- Scalable cloud infrastructure
- Professional-grade reliability

## Technologies
- **Frontend**: Streamlit, Custom CSS, HTML5
- **Backend**: Python, Scikit-learn, Pandas
- **Deployment**: Render, Git version control
- **Data Processing**: NLTK, NumPy

## Skills Demonstrated
- Full-stack web development
- Machine learning implementation
- Data processing and analysis
- UI/UX design
- Cloud deployment
- Project documentation
