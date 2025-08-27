import click
from services.campaign_service import CampaignService
from utils.helpers import (
    format_currency, format_percentage, 
    truncate_text, display_error, 
    create_progress_bar
)

@click.group()
def campaigns():
    """Campaign management commands"""
    pass

@campaigns.command()
def list():
    """List all active campaigns"""
    try:
        campaign_service = CampaignService()
        campaigns_list = campaign_service.get_all_campaigns(active_only=True)
        
        if not campaigns_list:
            click.echo("📭 No active campaigns found.")
            click.echo("💡 Use 'python main.py campaigns create' to create a new campaign.")
            return

        campaigns_data = []
        for c in campaigns_list:
            campaigns_data.append((
                c.id,
                truncate_text(c.title, 30),
                truncate_text(c.organization_name, 20),
                c.category,
                format_currency(c.current_amount),
                format_currency(c.goal_amount),
                format_percentage(c.progress_percentage),
                create_progress_bar(float(c.current_amount), float(c.goal_amount), 15),
                c.donation_count
            ))

        click.echo("🎯 Active Campaigns:\n")
        headers = ("ID", "Title", "Organization", "Category", "Raised", "Goal", "Progress", "Bar", "Donations")
        header_line = " | ".join(f"{h:<12}" for h in headers)
        click.echo(header_line)
        click.echo("-" * len(header_line))

        for data in campaigns_data:
            row = " | ".join(str(d) for d in data)
            click.echo(row)

        click.echo(f"\nTotal campaigns: {len(campaigns_list)}")

    except Exception as e:
        display_error(f"Failed to list campaigns: {e}")
