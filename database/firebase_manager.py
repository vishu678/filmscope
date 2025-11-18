import firebase_admin
from firebase_admin import credentials, db
import os

class FirebaseManager:
    def __init__(self):
        cred = credentials.Certificate(os.getenv("FIREBASE_KEY_PATH"))
        firebase_admin.initialize_app(cred, {
            "databaseURL": os.getenv("FIREBASE_DB_URL")
        })
        self.ref = db.reference("favorites")

    def add_favorite(self, movie):
        entry = {
            "movie_id": movie.movie_id,
            "title": movie.title,
            "rating": movie.rating,
            "release_date": movie.release_date
        }
        self.ref.push(entry)

    def get_favorites(self):
        data = self.ref.get()
        return data if data else {}

    def remove_favorite(self, key):
        self.ref.child(key).delete()
