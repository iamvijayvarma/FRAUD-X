import random
from datetime import datetime, timedelta
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.account import Account
from app.models.device import Device, AccountDevice
from app.models.transaction import Transaction
from app.utils.geo import KNOWN_CITIES

MERCHANT_CATEGORIES = [
    ("Flipkart", "E-COMMERCE"),
    ("Swiggy Online", "FOOD_DELIVERY"),
    ("Zomato Delivery", "FOOD_DELIVERY"),
    ("Reliance Digital", "ELECTRONICS"),
    ("Croma Electronics", "ELECTRONICS"),
    ("DMart Supermarket", "GROCERY"),
    ("BigBasket", "GROCERY"),
    ("IRCTC Express Booking", "TRAVEL"),
    ("MakeMyTrip Flights", "TRAVEL"),
    ("Indian Oil Petrol Pump", "FUEL"),
    ("Bharat Petroleum", "FUEL"),
    ("Apollo Pharmacy", "HEALTHCARE"),
    ("BESCOM Electricity Bill", "UTILITIES"),
    ("Tanishq Jewellery", "LUXURY"),
    ("Amazon India", "E-COMMERCE")
]

PAYMENT_MODES = [
    "UPI", "Debit Card", "Credit Card", "Net Banking", "IMPS", "NEFT", "POS", "QR Payment"
]

INDIAN_BANKS = [
    "HDFC Bank", "SBI", "ICICI Bank", "Axis Bank", "Kotak Mahindra Bank"
]

DEVICE_TYPES = [
    "Samsung Galaxy S24 Ultra (Android 14)",
    "Apple iPhone 15 (iOS 17)",
    "OnePlus 12 (OxygenOS 14)",
    "Xiaomi Redmi Note 13 Pro (MIUI)",
    "Vivo V30 Pro (Funtouch OS)",
    "Dell Inspiron 15 (Windows 11)",
    "MacBook Air M2 (macOS)"
]

USER_NAMES = [
    "Aarav Sharma", "Priya Patel", "Rajesh Iyer", "Ananya Reddy", "Vikram Malhotra",
    "Sneha Kulkarni", "Karthik Subramanian", "Divya Nair", "Rohan Verma", "Meera Joshi",
    "Arjun Singhania", "Pooja Deshmukh", "Sanjay Menon", "Deepa Nambiar", "Aditya Rao",
    "Nithya Ramachandran", "Suresh Krishnan", "Kavita Choudhury", "Ashwin Balaji", "Ritu Sen",
    "Manish Tiwari", "Shreya Banerjee", "Harish Natarajan", "Geetha Sundaram", "Gaurav Kapoor",
    "Lavanya Venkataraman", "Naveen Chawla", "Preeti Das", "Manoj Pillai", "Swati Bhatia",
    "Varun Hegde", "Anjali Mukherjee", "Pradeep Varma", "Sunita Nair", "Akash Mittal",
    "Gayatri Seshadri", "Deepak Saxena", "Archana Ganesan", "Ramesh Babu", "Vandana Sethi",
    "Gautam Ghosh", "Bhavana Kulkarni", "Kishore Kumar", "Tanvi Agarwal", "Siddharth Bose",
    "Malini Parthasarathy", "Nitin Aggarwal", "Shalini Raghavan", "Rahul Dravid", "Kavitha Murugan"
]

async def seed_database(session: AsyncSession):
    """Populates the database with 50 diverse Indian accounts, devices, and baseline transactions."""
    res = await session.execute(select(func.count(Account.id)))
    count = res.scalar() or 0
    if count >= 30:
        return

    print("Seeding FRAUD-X intelligence database with Indian financial baseline profiles...")

    cities = list(KNOWN_CITIES.items())
    accounts_created = []

    # 1. Create 50 user accounts with distinct Indian spending personas (in INR ₹)
    for i, name in enumerate(USER_NAMES):
        acc_id = f"ACC-IN-{1000 + i}"
        city_name, (lat, lon, state_country) = random.choice(cities)
        bank = random.choice(INDIAN_BANKS)

        # Spending personas (in INR)
        persona_idx = i % 5
        if persona_idx == 0: # Daily commuter / retail (UPI frequent)
            avg = round(random.uniform(1200.0, 3200.0), 2)
            std = round(avg * 0.22, 2)
        elif persona_idx == 1: # High-earning IT Professional
            avg = round(random.uniform(18000.0, 48000.0), 2)
            std = round(avg * 0.30, 2)
        elif persona_idx == 2: # Family Household groceries/utilities
            avg = round(random.uniform(4500.0, 11500.0), 2)
            std = round(avg * 0.25, 2)
        elif persona_idx == 3: # College student / UPI micro-spends
            avg = round(random.uniform(350.0, 1200.0), 2)
            std = round(avg * 0.28, 2)
        else: # Regular corporate employee
            avg = round(random.uniform(2800.0, 7500.0), 2)
            std = round(avg * 0.24, 2)

        email = f"{name.lower().replace(' ', '.')}.{1000+i}@upi.in"

        account = Account(
            id=acc_id,
            holder_name=name,
            email=email,
            created_at=datetime.utcnow() - timedelta(days=random.randint(90, 365)),
            avg_amount=avg,
            std_amount=std,
            typical_city=city_name,
            typical_country="India",
            typical_location_lat=lat,
            typical_location_lon=lon,
            primary_bank=bank,
            status="ACTIVE",
            risk_rating="LOW"
        )
        session.add(account)
        accounts_created.append(account)

    await session.flush()

    # 2. Associate dedicated trusted primary devices for each account
    account_primary_devices = {}
    for acc in accounts_created:
        dev_id = f"DEV-IN-{acc.id[7:]}-PRIM"
        dev = Device(
            id=dev_id,
            first_seen=acc.created_at,
            last_seen=datetime.utcnow() - timedelta(hours=random.randint(1, 24)),
            browser_os=random.choice(DEVICE_TYPES),
            is_known_proxy=False,
            risk_score=0
        )
        session.add(dev)
        trusted_devs = [dev]
        account_primary_devices[acc.id] = trusted_devs

        link = AccountDevice(
            account_id=acc.id,
            device_id=dev.id,
            first_used_at=acc.created_at,
            last_used_at=datetime.utcnow() - timedelta(hours=random.randint(2, 24)),
            usage_count=random.randint(12, 60)
        )
        session.add(link)

    await session.flush()

    # 3. Generate ~200 legitimate historical baseline transactions in INR
    for acc in accounts_created:
        num_tx = random.randint(3, 6)
        trusted_devs = account_primary_devices[acc.id]
        
        for t in range(num_tx):
            tx_time = datetime.utcnow() - timedelta(days=random.randint(1, 30), hours=random.randint(0, 23))
            amount = max(50.0, round(random.gauss(acc.avg_amount, acc.std_amount), 2))
            merchant_name, category = random.choice(MERCHANT_CATEGORIES)
            payment_mode = random.choice(PAYMENT_MODES)
            dev = random.choice(trusted_devs)

            tx = Transaction(
                id=f"TXN-IN-HIST-{uuid.uuid4().hex[:6].upper()}",
                timestamp=tx_time,
                account_id=acc.id,
                target_account_id=None,
                amount=amount,
                currency="INR",
                merchant_name=merchant_name,
                merchant_category=category,
                transaction_type=payment_mode,
                bank_name=acc.primary_bank,
                device_id=dev.id,
                ip_address=f"103.21.{random.randint(1, 254)}.{random.randint(1, 254)}",
                location_city=acc.typical_city,
                location_country="India",
                location_lat=acc.typical_location_lat + random.uniform(-0.02, 0.02),
                location_lon=acc.typical_location_lon + random.uniform(-0.02, 0.02),
                risk_score=random.uniform(2.0, 16.0),
                risk_level="LOW",
                action_taken="ALLOW",
                evidence_json='{"signals": []}',
                is_synthetic=True
            )
            session.add(tx)

    await session.commit()
    print("Database seeded with 50 Indian accounts and historical INR baseline transactions.")
