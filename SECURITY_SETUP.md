# 🚨 SECURITY SETUP REQUIRED 🚨

**IMPORTANT**: This repository does NOT include sensitive authentication files. You must set these up before the application will work.

## Required Security Setup

### 1. Google Calendar API Setup

1. **Create Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable the Google Calendar API

2. **Create OAuth 2.0 Credentials**:
   - Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
   - Choose "Desktop Application"
   - Download the JSON file

3. **Install Client Secret**:
   ```bash
   # Rename and move the downloaded file to:
   auth/client_secret.json
   ```

### 2. Gemini API Setup

1. **Get Gemini API Key**:
   - Go to [Google AI Studio](https://aistudio.google.com/)
   - Create an API key for Gemini

2. **Configure API Keys**:
   ```bash
   # Copy the template file
   cp auth/api_keys.json.template auth/api_keys.json
   
   # Edit auth/api_keys.json and replace YOUR_GEMINI_API_KEY_HERE with your actual key
   ```

## File Structure After Setup

```
auth/
├── client_secret.json         # Your Google OAuth credentials (NEVER commit)
├── api_keys.json              # Your API keys (NEVER commit)
├── api_keys.json.template     # Template file (safe to commit)
└── token.json                 # Auto-generated OAuth tokens (NEVER commit)
```

## Security Notes

-  All sensitive files are in `.gitignore`
-  Only template files are committed to Git
-  API keys are loaded securely at runtime
-   **NEVER** commit files containing real API keys or secrets
-   **ALWAYS** use the template files for reference

## Testing Your Setup

Run the application to test your configuration:

```bash
python main.py
```

If setup is correct, you should see:
- `[Gemini API] API key loaded successfully.` in the logs
- OAuth browser window opens for Google Calendar (first run only)

## Troubleshooting

### "API key file not found" Error
- Make sure you copied `api_keys.json.template` to `api_keys.json`
- Make sure you edited `api_keys.json` with your real API key

### OAuth Errors
- Make sure `client_secret.json` exists in the `auth/` folder
- Make sure you enabled Google Calendar API in Google Cloud Console
- Delete `auth/token.json` and try again to re-authorize

### Permission Errors
- Make sure the `auth/` folder has write permissions
- Make sure your Google account has access to the calendar you're trying to read
