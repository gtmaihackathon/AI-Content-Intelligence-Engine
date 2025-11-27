# 🔧 Troubleshooting OpenAI API Key Issues

## Problem
You're seeing "Automated analysis - AI not available" or API key errors.

## Solution Steps

### Step 1: Run Diagnostics
```bash
cd content-intelligence-engine
python diagnose.py
```

This will check:
- ✅ If .streamlit directory exists
- ✅ If secrets.toml exists and is configured
- ✅ If API key format is correct
- ✅ If API key actually works

### Step 2: Fix Based on Diagnostics

#### If `.streamlit/secrets.toml` is missing:

**Option A: Run setup script**
```bash
python setup.py
```
Follow the prompts to enter your API key.

**Option B: Create manually**
```bash
mkdir -p .streamlit
echo 'OPENAI_API_KEY = "sk-proj-your-key-here"' > .streamlit/secrets.toml
```

Replace `sk-proj-your-key-here` with your actual API key from:
https://platform.openai.com/api-keys

#### If API key is invalid (401 error):

1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the new key
4. Update `.streamlit/secrets.toml`:
   ```toml
   OPENAI_API_KEY = "sk-proj-YOUR_NEW_KEY_HERE"
   ```

#### If you're using an old key format:

OpenAI updated their key format. Old keys start with `sk-`, new keys start with `sk-proj-`.

**Get a new key:**
1. Go to https://platform.openai.com/api-keys
2. Revoke old key (optional)
3. Create new key
4. Update secrets.toml

### Step 3: Verify Setup

```bash
python diagnose.py
```

You should see:
```
✅ All checks passed! You're ready to run the app
```

### Step 4: Restart Streamlit

**Kill any running Streamlit process:**
```bash
# Press Ctrl+C in terminal where Streamlit is running
```

**Restart:**
```bash
streamlit run app.py
```

## Common Issues

### Issue: "secrets.toml not found"
**Fix:** You're running the command from the wrong directory.
```bash
# Make sure you're in the project root
cd content-intelligence-engine
ls -la .streamlit/secrets.toml
```

### Issue: "Invalid API key"
**Causes:**
- Key has expired
- Key was revoked
- Key format is incorrect (missing quotes, extra spaces)
- Free trial credits expired

**Fix:**
- Check your OpenAI account: https://platform.openai.com/account/usage
- Verify billing is set up
- Generate a new key

### Issue: "Rate limit exceeded"
**Fix:**
- You've hit your API usage limit
- Check usage: https://platform.openai.com/account/usage
- Upgrade your plan or wait for limit reset

### Issue: Key works in terminal but not in Streamlit
**Fix:**
- Make sure secrets.toml is in the correct location:
  ```
  your-project/
  └── .streamlit/
      └── secrets.toml
  ```
- Restart Streamlit completely (Ctrl+C and restart)
- Clear Streamlit cache: Delete `.streamlit/cache` folder

## File Locations Checklist

Your project should look like this:
```
content-intelligence-engine/
├── .streamlit/
│   └── secrets.toml  ← API key goes here
├── app.py
├── config.py
├── setup.py
├── diagnose.py
└── utils/
    ├── content_analyzer.py
    └── ...
```

## Testing Your API Key

Run this Python script to test:
```python
from openai import OpenAI

# Replace with your actual key
api_key = "sk-proj-your-key"
client = OpenAI(api_key=api_key)

try:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello!"}],
        max_tokens=10
    )
    print("✅ API Key works!")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ Error: {e}")
```

## Still Having Issues?

1. **Check the error message carefully** - It usually tells you exactly what's wrong
2. **Run diagnose.py** - It will identify the specific problem
3. **Check OpenAI Status** - Visit https://status.openai.com/
4. **Verify billing** - Free trial might have expired

## Need to Start Fresh?

```bash
# Remove old configuration
rm -rf .streamlit/

# Run setup again
python setup.py

# Test
python diagnose.py

# Run app
streamlit run app.py
```
