from flask import Flask, session, jsonify
from flask_migrate import Migrate
from models import db, Article

app = Flask(__name__)
app.secret_key = b'a\xdb\xd2\x13\x93\xc1\xe9\x97\xef2\xe3\x004U\xd1Z'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/articles/<int:id>')
def show_article(id):
    session['page_views'] = session.get('page_views', 0) + 1

    if session['page_views'] > 3:
        return jsonify({"message": "Maximum pageview limit reached"}), 401

    article = Article.query.filter_by(id=id).first()
    if not article:
        return jsonify({"error": f"Article with the id {id} not found"}), 404

    return jsonify({
        'id': article.id,
        'author': article.author,
        'title': article.title,
        'content': article.content,
        'preview': article.preview,
        'minutes_to_read': article.minutes_to_read,
        'date': article.date.isoformat() if article.date else None
    }), 200