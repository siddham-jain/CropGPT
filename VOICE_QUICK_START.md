# Voice Input - Quick Start Guide 🎤

## ✅ Installation Complete!

The Deepgram Nova-2 voice input feature has been successfully installed and configured.

## 🚀 Quick Start (3 Steps)

### Step 1: Add Your Deepgram API Key

1. Get a free API key at: https://console.deepgram.com/signup
2. Add to your `.env` file in `/backend/.env`:

```bash
DEEPGRAM_API_KEY=your_deepgram_api_key_here
```

### Step 2: Start the Backend

```bash
cd backend
source ../venv/bin/activate
uvicorn server:app --reload --port 8000
```

### Step 3: Test It!

1. Open your app in the browser
2. Click the **🎤 microphone button**
3. **Speak** your query: "What is the wheat price in Punjab?"
4. Click **🎤 again** to stop recording
5. Watch the text appear in the input box
6. Edit if needed, then click **Send**

## ✨ What's New

### Voice Button Behavior
- **Before**: Voice → AI response automatically
- **Now**: Voice → Text in input box → User reviews → User clicks Send

This gives users **full control** to review and edit the transcription before sending.

## 🎯 Testing the Setup

### Test 1: Check Voice Capabilities

```bash
curl http://localhost:8000/api/voice/capabilities
```

Expected response:
```json
{
  "available": true,
  "model": "nova-2",
  "provider": "Deepgram",
  "supported_languages": [...]
}
```

### Test 2: Try Different Languages

The system supports 10+ languages:
- 🇬🇧 **English**: "What is the wheat price?"
- 🇮🇳 **Hindi**: "गेहूं की कीमत क्या है?"
- 🇮🇳 **Punjabi**: "ਕਣਕ ਦੀ ਕੀਮਤ ਕੀ ਹੈ?"
- 🇮🇳 **Tamil**: "கோதுமை விலை என்ன?"
- And more...

## 🔧 Troubleshooting

### Issue: "Deepgram API key not configured"

**Fix**: 
1. Check `.env` file has `DEEPGRAM_API_KEY=...`
2. Restart the backend server
3. Test with `/api/voice/capabilities`

### Issue: Microphone not working

**Fix**:
1. Grant browser microphone permissions
2. Ensure you're using HTTPS (required for mic access)
3. Check browser console for errors

### Issue: Poor transcription quality

**Fix**:
1. Speak clearly and at moderate pace
2. Reduce background noise
3. Select the correct language in the UI
4. Check microphone quality

## 📊 Performance

- **Transcription speed**: < 1 second
- **Accuracy**: Nova-2 is Deepgram's latest and most accurate model
- **Cost**: ~$0.0125 per minute (Free tier: $200 credit)

## 🎓 Learn More

- **Setup Guide**: `backend/VOICE_STT_SETUP.md`
- **Implementation Details**: `VOICE_INPUT_IMPLEMENTATION.md`
- **Deepgram Docs**: https://developers.deepgram.com/

## 🎉 You're All Set!

The voice input feature is ready to use. Just add your Deepgram API key and start the backend server.

**Tip**: Test with the voice capabilities endpoint first to ensure everything is configured correctly!
