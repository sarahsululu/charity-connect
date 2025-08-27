import uuid
from decimal import Decimal
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from models.database import get_session, close_session
from models.donation import Donation
from models.campaign import Campaign
from models.user import User
from services.campaign_service import CampaignService
class DonationService:
    def __init__(self):
        self.session = get_session()
        self.campaign_service = CampaignService()
    
    def create_donation(self, donor_id, campaign_id, amount, message=None, 
                       is_anonymous=False, payment_method='card'):
        """Create a new donation"""
        try:
            if amount <= 0:
                raise ValueError("Donation amount must be greater than 0")
            
            campaign = self.session.query(Campaign).filter(
                Campaign.id == campaign_id,
                Campaign.is_active == True
            ).first()
            
            if not campaign:
                raise ValueError("Campaign not found or inactive")
            
            transaction_id = f"TXN_{uuid.uuid4().hex[:12].upper()}"
            
            donation = Donation(
                donor_id=donor_id,
                campaign_id=campaign_id,
                amount=Decimal(str(amount)),
                message=message,
                is_anonymous=is_anonymous,
                payment_method=payment_method,
                transaction_id=transaction_id,
                status='completed'  
            )
            
            self.session.add(donation)
            
            campaign.add_donation(Decimal(str(amount)))
            
            self.session.commit()
            
            return donation
            
        except Exception as e:
            self.session.rollback()
            raise e