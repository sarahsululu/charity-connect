import click
from services.user_service import UserService
from services.donation_service import DonationService
from utils.helpers import (
    get_current_user, format_currency, display_error, format_date
)

@click.group()
def profile():
    """User profile management commands"""
    pass

@profile.command()
def view():
    """View your profile information"""
    current_user = get_current_user()
    if not current_user:
        display_error("You must be logged in to view your profile.")
        return
    
    try:
        click.echo("=" * 60)
        click.echo(f"👤 Profile: {current_user.full_name}")
        click.echo("=" * 60)
        
        basic_info = [
            ["Full Name", current_user.full_name],
            ["Username", current_user.username],
            ["Email", current_user.email],
            ["Phone", current_user.phone or "Not provided"],
            ["Member Since", format_date(current_user.created_at)],
            ["Account Status", "Active" if current_user.is_active else "Inactive"]
        ]
        
        click.echo("📋 Basic Information:")
        for row in basic_info:
            click.echo(f"{row[0]:<20}: {row[1]}")

        settings = {
            "Notifications": "Enabled" if getattr(current_user, "notifications", False) else "Disabled",
            "Two-Factor Auth": "Enabled" if getattr(current_user, "two_factor", False) else "Disabled",
            "Language": getattr(current_user, "language", "English")
        }
        click.echo("\n Settings:")
        for key, value in settings.items():
            click.echo(f"{key:<20}: {value}")

        account_summary = (
            current_user.username,
            current_user.full_name,
            current_user.email,
            getattr(current_user, "current_balance", 0)
        )
        click.echo("\n💰 Account Summary:")
        click.echo(f"Username         : {account_summary[0]}")
        click.echo(f"Full Name        : {account_summary[1]}")
        click.echo(f"Email            : {account_summary[2]}")
        click.echo(f"Balance          : {format_currency(account_summary[3])}")
        
    except Exception as e:
        display_error(f"Failed to load profile: {e}")
