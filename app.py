from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {
    "origins": ["https://iplfans.live", "http://localhost:3000", "http://localhost:8000"],
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"],
    "supports_credentials": True
}})

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iplvotes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Vote model
class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Vote {self.team_name}>'

# Create database tables
with app.app_context():
    db.create_all()

# Valid IPL teams
VALID_TEAMS = [
    "Chennai Super Kings",
    "Delhi Capitals",
    "Gujarat Titans",
    "Kolkata Knight Riders",
    "Lucknow Super Giants",
    "Mumbai Indians",
    "Punjab Kings",
    "Rajasthan Royals",
    "Royal Challengers Bangalore",
    "Sunrisers Hyderabad"
]

@app.route('/')
def home():
    return jsonify({"message": "Welcome to IPL Voting API"})

@app.route('/vote', methods=['POST'])
def vote():
    try:
        data = request.get_json()
        team_name = data.get('team_name', '').strip()
        
        if not team_name:
            return jsonify({"error": "Team name is required"}), 400
            
        if team_name not in VALID_TEAMS:
            return jsonify({"error": "Invalid team name"}), 400
        
        # Create new vote
        new_vote = Vote(team_name=team_name)
        db.session.add(new_vote)
        db.session.commit()
        
        return jsonify({"message": f"Vote recorded for {team_name}"}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while processing your vote"}), 500

@app.route('/stats')
def stats():
    try:
        # Get vote counts for each team
        vote_counts = {}
        for team in VALID_TEAMS:
            count = Vote.query.filter_by(team_name=team).count()
            vote_counts[team] = count
            
        return jsonify({
            "total_votes": sum(vote_counts.values()),
            "team_votes": vote_counts
        })
        
    except Exception as e:
        return jsonify({"error": "An error occurred while fetching stats"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 