import sys
from services.user_service import UserService
from services.campaign_service import CampaignService
from services.donation_service import DonationService
from models.database import init_database
init_database()
from utils.helpers import (
    display_success,
    display_error,
    format_currency
)

class CharityPlatformMenu:
    def __init__(self):
        self.user_service = UserService()
        self.campaign_service = CampaignService()
        self.donation_service = DonationService()
        self.current_user = None

    def clear_screen(self):
        import os
        os.system('cls' if os.name == 'nt' else 'clear')

    def pause(self):
        input("\nPress Enter to continue...")

    def show_guest_menu(self):
        while True:
            self.clear_screen()
            print("🌟 CHARITY DONATION PLATFORM 🌟")
            print("=" * 40)
            print("GUEST MENU")
            print("=" * 40)
            print("1. Register")
            print("2. Login")
            print("3. Browse Campaigns")
            print("4. Exit")
            print("=" * 40)

            choice = input("Enter choice: ").strip()

            if choice == '1':
                self.register()
            elif choice == '2':
                self.login()
            elif choice == '3':
                self.browse_campaigns()
            elif choice == '4':
                print("👋 Thank you for visiting! Goodbye!")
                sys.exit(0)
            else:
                print("❌ Invalid choice. Please enter 1-4.")
                self.pause()

    def register(self):
        try:
            username = input("Username: ").strip()
            email = input("Email: ").strip()
            first_name = input("First name: ").strip()
            last_name = input("Last name: ").strip()
            password = input("Password: ").strip()

            user = self.user_service.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            if user:
                display_success(f"User {username} registered successfully!")
                self.current_user = user
                display_success(f"You are now logged in as {user.username}.")
                self.show_user_menu()
            else:
                display_error("Registration failed. Username or email may already exist.")
        except Exception as e:
            display_error(f"Error: {e}")
        self.pause()

    def login(self):
        try:
            username_or_email = input("Username or Email: ").strip()
            password = input("Password: ").strip()
            
            user = self.user_service.authenticate_user(username_or_email, password)
            
            if user:
                self.current_user = user
                display_success(f"Welcome back, {user.username}!")
                self.show_user_menu()
            else:
                display_error("❌ Invalid credentials or inactive account.")
        except Exception as e:
            display_error(f"❌ Error: {e}")
        self.pause()

    # ===== User Menu =====
    def show_user_menu(self):
        while True:
            self.clear_screen()
            print(f"🌟 Welcome {self.current_user.username} 🌟")
            print("=" * 40)
            print("USER MENU")
            print("=" * 40)
            print("1. Browse Campaigns")
            print("2. Create Campaign")
            print("3. Make Donation")
            print("4. View Profile")
            print("5. Logout")
            print("=" * 40)

            choice = input("Enter choice: ").strip()
            if choice == '1':
                self.browse_campaigns()
            elif choice == '2':
                self.create_campaign()
            elif choice == '3':
                self.make_donation()
            elif choice == '4':
                self.view_profile()
            elif choice == '5':
                self.current_user = None
                display_success("Logged out successfully!")
                return
            else:
                print("❌ Invalid choice. Enter 1-5.")
                self.pause()

    def browse_campaigns(self):
        self.clear_screen()
        campaigns = self.campaign_service.get_all_campaigns(active_only=True)
        if not campaigns:
            print("📭 No campaigns found.")
        else:
            print("🎯 Active Campaigns:")
            for c in campaigns:
                print(
                    f"- {c.title} ({c.category}) - "
                    f"Goal: {format_currency(c.goal_amount)} - "
                    f"Raised: {format_currency(c.current_amount)}"
                )
        self.pause()

    def create_campaign(self):
        try:
            title = input("Campaign Title: ").strip()
            organization_name = input("Organization Name: ").strip()
            category = input("Category: ").strip()
            goal_amount = float(input("Goal Amount: "))
            description = input("Description: ").strip()  

            campaign = self.campaign_service.create_campaign(
                title=title,
                description=description,          
                organization_name=organization_name,
                category=category,
                goal_amount=goal_amount,
                creator_id=self.current_user.id
            )

            if campaign:
                display_success(f"Campaign '{title}' created successfully!")
            else:
                display_error("Failed to create campaign.")

        except Exception as e:
            display_error(f"Error: {e}")
        self.pause()

    def make_donation(self):
        try:
            campaign_id = int(input("Enter Campaign ID to donate: "))
            amount = float(input("Enter donation amount: "))
            
            donation = self.donation_service.create_donation(
                campaign_id=campaign_id,
                donor_id=self.current_user.id,
                amount=amount
            )
            
            if donation:
                display_success(f"Successfully donated {format_currency(amount)}!")
            else:
                display_error("Failed to donate. Check campaign ID.")
        except Exception as e:
            display_error(f"Error: {e}")
        self.pause()

    def view_profile(self):
        self.clear_screen()
        user = self.user_service.get_user_by_id(self.current_user.id)
        if not user:
            display_error("User not found.")
            self.pause()
            return

        print("=== Your Profile ===")
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Name: {user.full_name}")
        self.pause()


if __name__ == "__main__":
    menu = CharityPlatformMenu()
    menu.show_guest_menu()
