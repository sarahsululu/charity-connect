import uuid
from decimal import Decimal
from models.database import get_session
from models.donation import Donation
from models.campaign import Campaign
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

    def get_donation_history(self, donor_id):
        """Retrieve all donations made by a specific donor"""
        try:
            donations = (
                self.session.query(Donation)
                .filter(Donation.donor_id == donor_id)
                .order_by(Donation.created_at.desc())  
                .all()
            )
            return donations
        except Exception as e:
            self.session.rollback()
            raise e
