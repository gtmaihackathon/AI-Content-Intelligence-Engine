"""
Setup script for AI Content Intelligence Engine
Run this to configure your OpenAI API key
"""

import os
import sys

def setup_api_key():
    print("\n🔧 AI Content Intelligence Engine - Setup\n")
    print("=" * 50)
    
    # Check if .streamlit directory exists
    streamlit_dir = ".streamlit"
    if not os.path.exists(streamlit_dir):
        print(f"Creating {streamlit_dir} directory...")
        os.makedirs(streamlit_dir)
        print("✅ Directory created")
    
    # Get API key from user
    print("\n📝 Please enter your OpenAI API key:")
    print("   (Get it from: https://platform.openai.com/api-keys)")
    print("   Your key should start with 'sk-proj-' or 'sk-'")
    print()
    
    api_key = input("Enter API key: ").strip()
    
    # Validate key format
    if not api_key:
        print("❌ Error: No API key provided")
        sys.exit(1)
    
    if not (api_key.startswith("sk-proj-") or api_key.startswith("sk-")):
        print("⚠️  Warning: API key doesn't look correct (should start with 'sk-')")
        confirm = input("Continue anyway? (y/n): ").strip().lower()
        if confirm != 'y':
            sys.exit(1)
    
    # Create secrets.toml
    secrets_path = os.path.join(streamlit_dir, "secrets.toml")
    try:
        with open(secrets_path, 'w') as f:
            f.write(f'OPENAI_API_KEY = "{api_key}"\n')
        print(f"\n✅ API key saved to {secrets_path}")
        
        # Verify it was written correctly
        with open(secrets_path, 'r') as f:
            content = f.read()
            if "OPENAI_API_KEY" in content:
                print("✅ Configuration verified")
            else:
                print("❌ Error: Failed to write configuration")
                sys.exit(1)
        
    except Exception as e:
        print(f"❌ Error writing configuration: {e}")
        sys.exit(1)
    
    # Check if .gitignore exists and includes secrets
    gitignore_path = ".gitignore"
    secrets_ignored = False
    
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            if '.streamlit/secrets.toml' in f.read():
                secrets_ignored = True
    
    if not secrets_ignored:
        print("\n⚠️  Important: Add '.streamlit/secrets.toml' to your .gitignore file")
        print("   This prevents your API key from being committed to Git")
    
    print("\n" + "=" * 50)
    print("✅ Setup complete!")
    print("\nNext steps:")
    print("1. Run: pip install -r requirements.txt")
    print("2. Run: streamlit run app.py")
    print("=" * 50 + "\n")

if __name__ == "__main__":
    setup_api_key()
