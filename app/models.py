


# Define the User model
class User(db.Model):
    id = db.Column(db.UUID, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    city = db.Column(db.String(50))
