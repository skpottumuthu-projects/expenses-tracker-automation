# from app import create_app

# app = create_app('development')

# if __name__ == '__main__':
#     app.run(debug=True, port=5001)
# requirements.txt


# app.py
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
from flask_socketio import SocketIO, emit
# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)



# PostgreSQL Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.getenv('DB_USER', 'postgres')}:"
    f"{os.getenv('DB_PASSWORD', 'postgres')}@"
    f"{os.getenv('DB_HOST', 'localhost')}:"
    f"{os.getenv('DB_PORT', '5432')}/"
    f"{os.getenv('DB_NAME', 'testdb')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Simple Message Model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(50), nullable=False, default='Anonymous')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Message {self.id}: {self.content[:20]}...>'

# Routes
@app.route('/')
def hello_world():
    """Display hello world with messages from database"""
    try:
        # Get all messages from database
        messages = Message.query.order_by(Message.created_at.desc()).limit(10).all()
        
        # Count total messages
        total_messages = Message.query.count()
        
        return render_template('index.html', 
                             messages=messages, 
                             total_messages=total_messages)
    except Exception as e:
        return f"Database Error: {str(e)}"

@app.route('/add_message', methods=['POST'])
def add_message():
    """Add a new message to the database"""
    try:
        content = request.form.get('content', '').strip()
        author = request.form.get('author', 'Anonymous').strip()
        
        if content:
            new_message = Message(content=content, author=author)
            db.session.add(new_message)
            db.session.commit()
        
        return redirect(url_for('hello_world'))
    except Exception as e:
        return f"Error adding message: {str(e)}"

@app.route('/api/messages')
def api_messages():
    """Get messages as JSON"""
    try:
        messages = Message.query.order_by(Message.created_at.desc()).limit(10).all()
        
        return {
            'success': True,
            'messages': [
                {
                    'id': msg.id,
                    'content': msg.content,
                    'author': msg.author,
                    'created_at': msg.created_at.isoformat()
                }
                for msg in messages
            ],
            'total_count': Message.query.count()
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.route('/db_status')
def db_status():
    """Check database connection status"""
    try:
        # Try to query the database
        result = db.session.execute(db.text('SELECT version()'))
        version = result.fetchone()[0]
        
        return {
            'status': 'connected',
            'database': 'PostgreSQL',
            'version': version,
            'total_messages': Message.query.count()
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }

def init_db():
    """Initialize database with tables"""
    try:
        db.create_all()
        
        # Add a welcome message if no messages exist
        if Message.query.count() == 0:
            welcome_msg = Message(
                content="Hello World from PostgreSQL! 🐘",
                author="System"
            )
            db.session.add(welcome_msg)
            db.session.commit()
            print("Database initialized with welcome message!")
        
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == '__main__':
    # Initialize database before running
    # with app.app_context():
    #     init_db()
    
    app.run(debug=True)


