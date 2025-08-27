from decimal import Decimal
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from models.database import get_session, close_session
from models.campaign import Campaign
from models.user import User
class CampaignService:
    def __init__(self):
        self.session = get_session()
    
    def create_campaign(self, creator_id, title, description, goal_amount, category, 
                       organization_name, end_date=None, beneficiary_info=None, image_url=None):
        """Create a new campaign"""
        try:
            campaign = Campaign(
                creator_id=creator_id,
                title=title,
                description=description,
                goal_amount=Decimal(str(goal_amount)),
                category=category,
                organization_name=organization_name,
                end_date=end_date,
                beneficiary_info=beneficiary_info,
                image_url=image_url
            )
            
            self.session.add(campaign)
            self.session.commit()
            
            return campaign
            
        except Exception as e:
            self.session.rollback()
            raise e
    
    def get_all_campaigns(self, active_only=True, category=None, featured_only=False):
        """Get all campaigns with optional filters"""
        try:
            query = self.session.query(Campaign)
            
            if active_only:
                query = query.filter(Campaign.is_active == True)
            
            if category:
                query = query.filter(Campaign.category == category)
            
            if featured_only:
                query = query.filter(Campaign.is_featured == True)
            
            return query.order_by(Campaign.created_at.desc()).all()
            
        except Exception as e:
            raise e