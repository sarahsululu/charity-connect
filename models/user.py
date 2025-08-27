from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.database import Base
import bcrypt
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(128), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    donations = relationship("Donation", back_populates="donor", cascade="all, delete-orphan")
    campaigns = relationship("Campaign", back_populates="creator", cascade="all, delete-orphan")
    
    def set_password(self, password):
        """Hash and set the password"""
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    
    def check_password(self, password):
        """Check if the provided password matches the hash"""
        password_bytes = password.encode('utf-8')
        hash_bytes = self.password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hash_bytes)
    
    @property
    def full_name(self):
        """Get the user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    def total_donated(self):
        """Calculate total amount donated by this user"""
        return sum(donation.amount for donation in self.donations)
    
    def donation_count(self):
        """Get the number of donations made by this user"""
        return len(self.donations)
    
    def __repr__(self):
        return f"<User {self.username}>"