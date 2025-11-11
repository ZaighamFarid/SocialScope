# 🚀 Quick Setup Guide

Get Social Scope running in 5 minutes!

## Prerequisites Checklist

- [ ] macOS 13+ with Xcode 15+
- [ ] Python 3.10+
- [ ] OpenAI API Key ([Get here](https://platform.openai.com/api-keys))

---

## Backend Setup (3 minutes)

```bash
cd SocialScope/Backend

# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment
cp .env.example .env
# Open .env in your editor and add your OPENAI_API_KEY

# 4. Start the server
./run.sh
```

✅ Backend should now be running at `http://localhost:8000`  
📚 Check API docs at `http://localhost:8000/docs`

---

## iOS App Setup (2 minutes)

```bash
cd SocialScope/iOS-App

# Open in Xcode
open Package.swift
# OR if you have an .xcodeproj:
# open SocialScope.xcodeproj
```

**In Xcode:**
1. Select a simulator (e.g., iPhone 15)
2. Press `Cmd + R` to build and run

✅ App should launch in the simulator!

---

## Test It Out

### In the iOS App:
1. Tap the Wi-Fi icon to enable **Offline Demo Mode**
2. Paste any URL (e.g., `https://twitter.com/test`)
3. Select a comment tone
4. Tap **Analyze Post**
5. See AI-generated summary and comment!

### For Real Analysis:
1. Turn off Offline Mode (tap Wi-Fi icon again)
2. Make sure backend is running
3. Paste a real social media post URL
4. Enjoy real AI analysis!

---

## Troubleshooting

### "Cannot connect to server"
- Make sure backend is running (`./run.sh` in Backend folder)
- Check that the URL in `APIService.swift` is `http://localhost:8000`

### "OPENAI_API_KEY not set"
- Make sure you created `.env` file in Backend folder
- Check that your API key is correctly set

### Xcode build errors
- Try cleaning: `Cmd + Shift + K`
- Reset packages: File → Packages → Reset Package Caches

---

## Next Steps

- Read the full [README.md](README.md)
- Check out [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Explore the API docs at `/docs` endpoint

---

Happy analyzing! 🎉
