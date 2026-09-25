from blockchain import Blockchain


print("\n======================================")
print("     BLOCKCHAIN SECURITY TEST")
print("======================================")


# Create blockchain
blockchain = Blockchain()


# Add test event
event = {
    "event_id": "EVT-001",
    "camera_id": "CAM01",
    "event_type": "PERSON_DETECTED",
    "confidence": 0.94,
    "zone": "RESTRICTED_ZONE"
}

blockchain.add_event(event)

print("\n[1] Security event added")
print("[2] Checking original blockchain...")


# Verify original blockchain
if blockchain.verify_chain():
    print("✓ Blockchain is VALID")
else:
    print("✗ Blockchain is INVALID")


# Simulate tampering
print("\n[3] Simulating data tampering...")

blockchain.chain[1]["event"]["confidence"] = 0.20


# Verify after tampering
print("[4] Checking blockchain after modification...")

if blockchain.verify_chain():
    print("⚠ WARNING: Tampering NOT detected")
else:
    print("🚨 TAMPERING DETECTED!")
    print("✓ Blockchain integrity compromised")


print("\n======================================")
print("       SECURITY TEST COMPLETE")
print("======================================")