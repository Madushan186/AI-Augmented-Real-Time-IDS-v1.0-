
import os
import shutil
import glob

# LIST OF FILES TO DELETE (JUNK / RUNTIME DATA)
JUNK_FILES = [
    ".DS_Store",
    "ids_state.json",       # Runtime state (auto-created)
    "ids_state.json.tmp",   # Temp state
    "ai_status.json",       # Old state file?
    "attack_log.csv",       # Runtime logs (user likely wants a clean slate)
    "__pycache__"           # Python compiled files
]

# LIST OF FILES TO KEEP (SOURCE CODE & DATA)
# Just for verification printout
KEEP_FILES = [
    "realtime_ids.py",
    "dashboard.py",
    "run_ids.sh",
    "dummy_server.py", 
    "requirements.txt",
    "simulate_attack.py",
    "README.md",
    "models/",
    "data/",
    ".streamlit/"
]

def clean_project():
    print("🧹 Starting Project Cleanup for Handover...")
    
    deleted_count = 0
    
    # 1. Delete specific files
    for item in JUNK_FILES:
        # Handle Wildcards if needed, or recursive walks
        # Simple local directory check
        if os.path.exists(item):
            try:
                if os.path.isdir(item):
                    shutil.rmtree(item)
                    print(f"   🗑️ Removed Directory: {item}")
                else:
                    os.remove(item)
                    print(f"   🗑️ Removed File: {item}")
                deleted_count += 1
            except Exception as e:
                print(f"   ❌ Error removing {item}: {e}")
                
    # 2. Recursive __pycache__ cleanup
    for root, dirs, files in os.walk("."):
        for d in dirs:
            if d == "__pycache__":
                path = os.path.join(root, d)
                try:
                    shutil.rmtree(path)
                    print(f"   🗑️ Removed {path}")
                    deleted_count += 1
                except Exception as e:
                    print(f"   ❌ Error removing {path}: {e}")
        
    print("-" * 40)
    print(f"✅ Cleanup Complete! Removed {deleted_count} items.")
    print("\n📦 The following KEY files are ready for zip/sharing:")
    for k in KEEP_FILES:
        if os.path.exists(k):
            print(f"   📄 {k}")
        else:
            print(f"   ⚠️ WARNING: Essential file {k} is missing!")
            
if __name__ == "__main__":
    confirm = input("This will delete logs and temp files. Type 'yes' to proceed: ")
    if confirm.lower() == "yes":
        clean_project()
    else:
        print("Cancelled.")
