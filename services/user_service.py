from sqlalchemy.exc import IntegrityError
from models.database import get_session
from models.user import User

class UserService:
    def __init__(self):
        self.session = get_session()
    
    def create_user(self, username, email, password, first_name, last_name, phone=None, address=None):
        """Create a new user account"""
        try:
            existing_user = self.session.query(User).filter(
                (User.username == username) | (User.email == email)
            ).first()
            
            if existing_user:
                return None  
            
            user = User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                address=address
            )
        
            user.set_password(password)
            
            self.session.add(user)
            self.session.commit()
            
            return user
            
        except IntegrityError:
            self.session.rollback()
            return None
        except Exception as e:
            self.session.rollback()
            raise e
    
    def authenticate_user(self, username_or_email, password):
        """Authenticate user login"""
        try:
            user = self.session.query(User).filter(
                (User.username == username_or_email) | (User.email == username_or_email)
            ).first()
            
            if user and user.check_password(password) and user.is_active:
                return user
            
            return None
            
        except Exception as e:
            raise e

    def get_user_by_id(self, user_id):
        """Fetch a user by their ID"""
        try:
            return self.session.query(User).filter(User.id == user_id).first()
        except Exception as e:
            raise e
