import click
from services.user_service import UserService
from utils.helpers import save_session, clear_session
from utils.validators import validate_email, validate_password

@click.group()
def auth():
    """User authentication commands"""
    pass

@auth.command()
def register():
    """Register a new user account"""
    click.echo("=== User Registration ===")
    
    try:
        user_data = {} 
        user_data['username'] = click.prompt("Username", type=str).strip()
        user_data['email'] = click.prompt("Email", type=str).strip()
        
        if not validate_email(user_data['email']):
            click.echo("Error: Invalid email format")
            return
        
        user_data['first_name'] = click.prompt("First name", type=str).strip()
        user_data['last_name'] = click.prompt("Last name", type=str).strip()
        user_data['phone'] = click.prompt("Phone (optional)", type=str, default="").strip() or None
        user_data['address'] = click.prompt("Address (optional)", type=str, default="").strip() or None
        
        password = click.prompt("Password", hide_input=True, confirmation_prompt=True)
        if not validate_password(password):
            click.echo("Error: Password must be at least 8 characters long")
            return
        
        user_service = UserService()
        user = user_service.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=password,
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            phone=user_data['phone'],
            address=user_data['address']
        )
        
        if user:
            click.echo(f"✅ User account created successfully!")
            click.echo(f"Welcome, {user.full_name}!")
            save_session(user.id)
            click.echo("You are now logged in.")
        else:
            click.echo("❌ Registration failed. Username or email may already exist.")
            
    except Exception as e:
        click.echo(f"❌ Registration error: {e}")

@auth.command()
def login():
    """Login an existing user"""
    click.echo("=== User Login ===")
    
    try:
        login_data = {} 
        login_data['username_or_email'] = click.prompt("Username or Email", type=str).strip()
        login_data['password'] = click.prompt("Password", hide_input=True)
        
        user_service = UserService()
        user = user_service.authenticate(login_data['username_or_email'], login_data['password'])
        
        if user:
            save_session(user.id)
            click.echo(f"✅ Login successful! Welcome back, {user.full_name}.")
        else:
            click.echo("❌ Invalid username/email or password.")
            
    except Exception as e:
        click.echo(f"❌ Login error: {e}")

@auth.command()
def logout():
    """Logout the currently logged-in user"""
    clear_session()
    click.echo("👋 You have been logged out successfully.")
