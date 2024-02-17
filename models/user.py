from extensions import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(75), nullable=False, unique=True)
    password = db.Column(db.String(150))
    gender = db.Column(db.String(10))
    birthDate = db.Column(db.Date)
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    department = db.Column(db.String(25))
    municipality = db.Column(db.String(25))
    address = db.Column(db.String(100))
    phoneNumber = db.Column(db.Integer)
    
    is_active = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    created_at = db.Column(
        db.DateTime(), 
        nullable=False,
        server_default=db.func.now()
    )
    updated_at = db.Column(
        db.DateTime(),
        nullable=False,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
