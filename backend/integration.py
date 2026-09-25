import sys
import os


# ==========================================
# PROJECT ROOT
# ==========================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, PROJECT_ROOT)


# ==========================================
# IMPORT DATABASE
# ==========================================

from ai.alert_database import (
    create_database,
    save_alert
)


# ==========================================
# IMPORT BLOCKCHAIN
# ==========================================

from blockchain.blockchain import Blockchain


print("\n======================================")
print("     BORDER SURVEILLANCE SYSTEM")
print("======================================")


# ==========================================
# DATABASE
# ==========================================

print("\n[1] Initializing Database...")

create_database()

print("✓ Database connected")


# ==========================================
# BLOCKCHAIN
# ==========================================

print("\n[2] Initializing Blockchain...")

blockchain = Blockchain()

print("✓ Blockchain connected")


# ==========================================
# TEST ALERT
# ==========================================

print("\n[3] Creating security event...")

event_data, event_hash = save_alert(

    camera_id="CAM-01",

    event_type="PERSON_DETECTED",

    confidence=0.94,

    zone="RESTRICTED_ZONE"
)


print("✓ Event saved in SQLite")


# ==========================================
# ADD HASH TO EVENT
# ==========================================

event_data["event_hash"] = event_hash


# ==========================================
# ADD TO BLOCKCHAIN
# ==========================================

print("\n[4] Adding event to blockchain...")

block = blockchain.add_event(
    event_data
)

print("✓ Event recorded on blockchain")


# ==========================================
# DISPLAY BLOCK
# ==========================================

print("\n======================================")
print("          BLOCKCHAIN RECORD")
print("======================================")

print("Block Index :", block["index"])
print("Timestamp   :", block["timestamp"])
print("Event       :", block["event"])
print("Previous    :", block["previous_hash"])
print("Hash        :", block["hash"])


# ==========================================
# VERIFY BLOCKCHAIN
# ==========================================

print("\n[5] Verifying blockchain...")

if blockchain.verify_chain():

    print("✓ Blockchain integrity: VALID")

else:

    print("🚨 Blockchain integrity: INVALID")


# ==========================================
# SYSTEM STATUS
# ==========================================

print("\n======================================")
print("          SYSTEM STATUS")
print("======================================")

print("AI Detection : READY")
print("Database     : CONNECTED")
print("SHA-256      : ENABLED")
print("Blockchain   : CONNECTED")
print("Verification : ACTIVE")

print("======================================")