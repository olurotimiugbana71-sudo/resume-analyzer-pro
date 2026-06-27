import sys
from license_gen import LicenseManager

if len(sys.argv) < 3:
    print("Usage: python generate_license.py <email> <tier>")
    print("Tiers: basic, standard, premium")
    sys.exit(1)

email = sys.argv[1]
tier = sys.argv[2]

lm = LicenseManager()
key = lm.generate_key(email, tier)

print(f"""
{'='*50}
  LICENSE KEY GENERATED
{'='*50}

  Email: {email}
  Tier: {tier}
  Valid: 1 year

  KEY: {key}

  Send this to the buyer!
{'='*50}
""")