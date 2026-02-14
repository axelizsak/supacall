"""
Test script to verify the system configuration.
"""
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()


def check_env_variables():
    """Checks that all required environment variables are defined"""
    print("🔍 Checking environment variables...\n")

    required_vars = {
        "TWILIO_ACCOUNT_SID": "Twilio Account SID",
        "TWILIO_AUTH_TOKEN": "Twilio Auth Token",
        "TWILIO_PHONE_NUMBER": "Twilio phone number",
        "OPENAI_API_KEY": "OpenAI API key",
        "BASE_URL": "Server base URL"
    }

    optional_vars = {
        "RESTAURANT_NAME": "Restaurant name",
        "RESTAURANT_OPENING_HOURS": "Opening hours",
        "RESTAURANT_MAX_CAPACITY": "Maximum capacity"
    }

    all_good = True

    # Required variables
    print("📋 Required variables:")
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if "KEY" in var or "TOKEN" in var:
                display_value = value[:8] + "..." if len(value) > 8 else "***"
            else:
                display_value = value
            print(f"  ✅ {var}: {display_value}")
        else:
            print(f"  ❌ {var}: MISSING - {description}")
            all_good = False

    # Optional variables
    print("\n📋 Optional variables:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            print(f"  ✅ {var}: {value}")
        else:
            print(f"  ⚠️  {var}: Not set (default value will be used)")

    return all_good


async def test_database():
    """Tests the database connection"""
    print("\n🗄️  Testing database...\n")

    try:
        from database import db

        # Initialize the database
        await db.init_db()
        print("  ✅ Database initialized")

        # Create a test reservation
        test_reservation = await db.create_reservation(
            nom="Test User",
            telephone="+33123456789",
            date="2026-02-15",
            heure="19:30",
            nombre_personnes=4,
            commentaires="Test reservation"
        )
        print(f"  ✅ Test reservation created (ID: {test_reservation['id']})")

        # Check availability
        available = await db.check_availability("2026-02-15", "19:30", 4)
        print(f"  ✅ Availability check: {'Available' if available else 'Fully booked'}")

        # Retrieve all reservations
        reservations = await db.get_all_reservations()
        print(f"  ✅ {len(reservations)} reservation(s) in the database")

        return True

    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_openai_key():
    """Tests the validity of the OpenAI API key"""
    print("\n🔑 Testing OpenAI key...\n")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("  ❌ OPENAI_API_KEY not set")
        return False

    if not api_key.startswith("sk-"):
        print("  ⚠️  API key does not start with 'sk-' (unusual format)")

    print("  ✅ Valid key format")
    print("  ℹ️  Note: Actual key validity will be tested on the first call")

    return True


def test_twilio_config():
    """Tests the Twilio configuration"""
    print("\n📞 Testing Twilio configuration...\n")

    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    phone_number = os.getenv("TWILIO_PHONE_NUMBER")

    all_good = True

    if account_sid and account_sid.startswith("AC"):
        print("  ✅ Account SID format valid")
    else:
        print("  ❌ Invalid Account SID (must start with 'AC')")
        all_good = False

    if phone_number and phone_number.startswith("+"):
        print("  ✅ Phone number format valid")
    else:
        print("  ⚠️  Phone number should start with '+' (E.164 format)")

    if auth_token and len(auth_token) == 32:
        print("  ✅ Auth Token format valid")
    else:
        print("  ⚠️  Unusual Auth Token format")

    return all_good


def print_next_steps():
    """Prints the next steps"""
    base_url = os.getenv("BASE_URL", "https://your-domain.com")

    print("\n" + "="*60)
    print("🎉 CONFIGURATION VERIFIED")
    print("="*60)

    print("\n📝 Next steps:\n")

    print("1. Start the server:")
    print("   python main.py\n")

    print("2. If developing locally, expose with ngrok:")
    print("   ngrok http 8000\n")

    print("3. Configure Twilio:")
    print("   - Go to Phone Numbers → Your number")
    print("   - Voice Configuration → Webhook:")
    print(f"   - URL: {base_url}/incoming-call")
    print("   - Method: HTTP POST\n")

    print("4. Test by calling your Twilio number!")

    print("\n📊 Available endpoints:")
    print(f"   - Home page: {base_url}/")
    print(f"   - Reservations: {base_url}/reservations")
    print(f"   - Twilio webhook: {base_url}/incoming-call")

    print("\n" + "="*60)


async def main():
    """Main test function"""
    print("\n" + "="*60)
    print("🧪 SUPACALL SYSTEM TEST")
    print("="*60 + "\n")

    # Check environment variables
    env_ok = check_env_variables()

    # Test OpenAI
    openai_ok = test_openai_key()

    # Test Twilio
    twilio_ok = test_twilio_config()

    # Test database
    db_ok = await test_database()

    # Summary
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60 + "\n")

    print(f"  Environment variables: {'✅' if env_ok else '❌'}")
    print(f"  OpenAI configuration: {'✅' if openai_ok else '❌'}")
    print(f"  Twilio configuration: {'✅' if twilio_ok else '❌'}")
    print(f"  Database: {'✅' if db_ok else '❌'}")

    if env_ok and openai_ok and twilio_ok and db_ok:
        print_next_steps()
        return True
    else:
        print("\n⚠️  Some tests failed. Check your configuration in .env")
        print("   Copy .env.example to .env and fill in the required values.")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
