# Calendar Summary AI Assistant

## IMPORTANT: Security Setup Required

**Before using this application, you MUST complete the security setup.**

**[READ SECURITY_SETUP.md FIRST](./SECURITY_SETUP.md)**

This repository does not include API keys or authentication files for security reasons.

## Features

- **Smart Calendar Integration**: Connects to Google Calendar via secure OAuth
- **AI-Powered Summaries**: Uses Gemini AI for supportive schedule descriptions  
- **Memory Care Optimized**: Language and tone designed for users with dementia
- **Event Enrichment**: Adds helpful preparation notes to calendar events
- **Time Ranges**: Supports "today", "tomorrow", "this week", "next week"
- **Comprehensive Logging**: Detailed logs for debugging and monitoring
- **Security**: API keys and credentials stored securely, never committed to Git

## Quick Start

1. **Complete Security Setup** (Required!)
   - Follow instructions in [SECURITY_SETUP.md](./SECURITY_SETUP.md)

2. **Install Dependencies**
   ```bash
   pip install google-api-python-client google-auth google-auth-oauthlib google-generativeai
   ```

3. **Add Your Query**
   ```bash
   echo "What do I have this week?" > user_data/user_responses.txt
   ```

4. **Run the Application**
   ```bash
   python main.py
   ```

## Supported Queries

- `"What do I have today?"` - Today's events with conversational AI responses
- `"What do I have tomorrow?"` - Tomorrow's events for evening planning
- `"What do I have this week?"` - Current week overview (Monday-Sunday)
- `"What do I have next week?"` - Following week planning

## Architecture

```
main.py                    # Main application entry point
├── logger.py             # Comprehensive logging system
├── modules/
│   ├── auth_handler.py   # Google OAuth 2.0 authentication
│   ├── calendar_handler.py # Google Calendar API integration
│   ├── gemini_handler.py # AI-powered event processing
│   └── speech_input.py   # Voice input (future feature)
├── auth/                 # Secure credential storage (not in Git)
├── logs/                 # Timestamped session logs (not in Git)
└── user_data/           # User queries and responses (not in Git)
```

## Memory Care Design

This application is specifically designed for users with memory challenges:

- **Warm, Supportive Language**: AI responses use encouraging, gentle tone
- **Clear Preparation Notes**: Events include helpful reminders about what to bring
- **Narrative Summaries**: Schedule presented as reassuring stories, not cold lists  
- **Consistent Structure**: Predictable interaction patterns reduce confusion
- **Comprehensive Logging**: Detailed logs help caregivers understand system behavior

## Development

### Running Tests
```bash
cd tests
python run_tests.py
```

### Documentation
Each module includes comprehensive documentation designed for onboarding. See individual module files for detailed documentation.

### Contributing
1. Ensure all sensitive data remains in the `auth/` folder
2. Never commit real API keys or credentials
3. Follow the existing logging patterns for new features
4. Maintain the warm, supportive tone in all AI prompts

## Security & Privacy

- **No Sensitive Data in Git**: All API keys and credentials excluded via `.gitignore`
- **Read-Only Calendar Access**: Application only reads calendar data, never modifies
- **Local Processing**: User data processed locally, not transmitted to external servers
- **Secure Authentication**: Uses Google's OAuth 2.0 standard for calendar access
- **Structured Logging**: Comprehensive logs for debugging without exposing secrets

## License

Meant for EQUI-Tech Lab/NJIT project investigators/REU/employees under grant # 2433349. Please use responsibly and in accordance with privacy regulations when handling user data. 

## Support

If you encounter issues:
1. Check [SECURITY_SETUP.md](./SECURITY_SETUP.md) for configuration problems
2. Review the logs in `logs/run_YYYY-MM-DD_HH-MM-SS/` for detailed error information
3. Ensure all dependencies are installed correctly
