import hashlib, uuid, json, os
from datetime import datetime, timedelta

class LicenseManager:
    def __init__(self):
        self.secret_key = "ARX2026-RESUME-PRO"
        self.license_file = "licenses.json"
        self.licenses = {}
        if os.path.exists(self.license_file):
            with open(self.license_file) as f:
                self.licenses = json.load(f)
    
    def save(self):
        with open(self.license_file, 'w') as f:
            json.dump(self.licenses, f, indent=2)
    
    def generate_key(self, email, tier="standard"):
        uid = str(uuid.uuid4())[:8]
        raw = f"{email}{uid}{self.secret_key}{tier}"
        key = hashlib.sha256(raw.encode()).hexdigest()[:20].upper()
        formatted = f"ARX-{key[:4]}-{key[4:8]}-{key[8:12]}"
        self.licenses[formatted] = {
            "email": email, "tier": tier,
            "created": datetime.now().isoformat(),
            "expires": (datetime.now() + timedelta(days=365)).isoformat()
        }
        self.save()
        return formatted
    
    def validate(self, key, email=""):
        if key in self.licenses:
            data = self.licenses[key]
            if datetime.now() > datetime.fromisoformat(data["expires"]):
                return False, "Expired"
            if email and data["email"].lower() != email.lower():
                return False, "Email mismatch"
            return True, "Valid"
        return False, "Invalid"

if __name__ == "__main__":
    lm = LicenseManager()
    email = input("Buyer email: ")
    tier = input("Tier (basic/standard/premium): ")
    key = lm.generate_key(email, tier)
    print(f"\nLICENSE: {key}")