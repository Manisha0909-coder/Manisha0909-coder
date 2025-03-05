from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# Note model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return f"Note('{self.id}', '{self.title}')"

# Create the database
with app.app_context():
    db.create_all()

# Routes for CRUD operations

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Note-Taking API!"})

# Create a new note
@app.route('/api/notes', methods=['POST'])
def create_note():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    date = data.get('date')
    
    if not title or not content:
        return jsonify({'message': 'Title and content are required'}), 400
    
    new_note = Note(title=title, content=content, date=date)
    db.session.add(new_note)
    db.session.commit()

    return jsonify({'message': 'Note created successfully', 'note': {'id': new_note.id, 'title': new_note.title, 'content': new_note.content, 'date': new_note.date}}), 201

# Get all notes
@app.route('/api/notes', methods=['GET'])
def get_notes():
    notes = Note.query.all()
    output = []
    for note in notes:
        output.append({'id': note.id, 'title': note.title, 'content': note.content, 'date': note.date})
    return jsonify({'notes': output})

# Get a single note by ID
@app.route('/api/notes/<int:id>', methods=['GET'])
def get_note(id):
    note = Note.query.get(id)
    if note:
        return jsonify({'id': note.id, 'title': note.title, 'content': note.content})
    else:
        return jsonify({'message': 'Note not found'}), 404

# Update a note by ID
@app.route('/api/notes/<int:id>', methods=['PUT'])
def update_note(id):
    note = Note.query.get(id)
    if note:
        data = request.get_json()
        note.title = data.get('title', note.title)
        note.content = data.get('content', note.content)
        note.date = data.get('date', note.date)
        db.session.commit()

        return jsonify({'message': 'Note updated successfully', 'note': {'id': note.id, 'title': note.title, 'content': note.content, 'date':note.date}})
    else:
        return jsonify({'message': 'Note not found'}), 404

# Delete a note by ID
@app.route('/api/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    note = Note.query.get(id)
    if note:
        db.session.delete(note)
        db.session.commit()
        return jsonify({'message': 'Note deleted successfully'})
    else:
        return jsonify({'message': 'Note not found'}), 404

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
