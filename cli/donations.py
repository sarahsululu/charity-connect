import click
from services.donation_service import DonationService
from services.campaign_service import CampaignService
from utils.helpers import (
    get_current_user, format_currency, truncate_text,
    display_success, display_error, display_info, format_date
)
from utils.validators import validate_amount

@click.group()
def donations():
    """Donation management commands"""
    pass

@donations.command()
@click.argument('campaign_id', type=int)
def donate(campaign_id):
    """Make a donation to a campaign"""
    current_user = get_current_user()
    if not current_user:
        display_error("You must be logged in to make a donation.")
        click.echo("💡 Use 'python main.py auth login' to sign in.")
        return
    
    try:
        campaign_service = CampaignService()
        campaign = campaign_service.get_campaign_by_id(campaign_id)
        
        if not campaign:
            display_error(f"Campaign with ID {campaign_id} not found.")
            return
        
        if not campaign.is_active:
            display_error("This campaign is no longer active.")
            return

        click.echo("=" * 60)
        campaign_info = (
            campaign.title,
            campaign.organization_name,
            format_currency(campaign.current_amount),
            format_currency(campaign.goal_amount),
            format_currency(campaign.remaining_amount)
        )
        click.echo(f"🎯 Donating to   : {campaign_info[0]}")
        click.echo(f"🏢 Organization : {campaign_info[1]}")
    except Exception as e:
        display_error(f"An error occurred: {e}")
