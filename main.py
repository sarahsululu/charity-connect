import click
from models.database import init_database
@click.group()
@click.version_option(version='1.0.0')
def main():
    """Charity Donation Platform - Connect donors with verified charities"""

    init_database()
if __name__ == '__main__':

    from cli import auth, campaigns, donations, profile
    
    main.add_command(auth.auth)
    main.add_command(campaigns.campaigns)
    main.add_command(donations.donations)
    main.add_command(profile.profile)
    
    main()