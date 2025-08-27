import time
from logger import setup_logger, log_session_start, user_logger, calendar_logger, gemini_logger, system_logger, LOG_DIR
from modules.calendar_handler import get_this_week_events, get_next_week_events, get_events_for_today, get_events_for_tomorrow
from modules.gemini_handler import summarize_schedule, infer_user_profile_from_events

# Add visual boundaries at the top of each log file for this run
log_session_start(system_logger, "System Run")
log_session_start(user_logger, "User Query")
log_session_start(gemini_logger, "Gemini Session")
log_session_start(calendar_logger, "Calendar API")
print(f"Logs for this run are saved in: {LOG_DIR}")

"""
    Main Execution Script for Calendar Summary Assistant

    Description:
    ------------
    This is the entry point of the calendar enrichment system designed for users with memory 
    challenges, particularly those with dementia. It reads natural language user queries from a 
    text file and uses the Google Calendar API and Gemini language model to:
        - Fetch relevant calendar events (this week, next week, today, tomorrow)
        - Infer a user profile based on event patterns to enable personalization
        - Enrich each event with helpful contextual notes and preparation reminders
        - Summarize the schedule in warm, human-readable language suitable for memory care

    Supported Query Types:
    ---------------------
    - "this week" - Returns all events for the current Monday-Sunday period
    - "next week" - Returns all events for the following Monday-Sunday period  
    - "today" - Returns all events for the current day (midnight to 11:59 PM)
    - "tomorrow" - Returns all events for the next day (midnight to 11:59 PM)

    Workflow:
    ---------
    1. Initialize structured logging system with timestamped session logs
    2. Load user query from `user_data/user_responses.txt`
    3. Parse query to determine time range (this week, next week, today, tomorrow)
    4. Use `calendar_handler` to fetch corresponding calendar events via Google Calendar API
    5. Use `gemini_handler` to:
        a. Infer user lifestyle traits and preferences from event patterns
        b. Enrich events lacking descriptions with helpful preparation notes
        c. Generate a supportive, narrative-style schedule summary
    6. Log final response and display it in the terminal for the user

    Architecture:
    -------------
    - `modules/calendar_handler.py` - Google Calendar API integration and event fetching
    - `modules/gemini_handler.py` - AI-powered profile inference, event enrichment, and summarization
    - `modules/auth_handler.py` - OAuth 2.0 authentication flow for Google Calendar access
    - `modules/speech_input.py` - Speech-to-text capabilities (not yet implemented)
    - `logger.py` - Comprehensive logging system with separate logs for different concerns

    Dependencies:
    -------------
    - `google-api-python-client` - Google Calendar API access
    - `google-auth`, `google-auth-oauthlib` - OAuth 2.0 authentication
    - `google-generativeai` - Gemini AI model integration
    - `psutil`, `platform` - System diagnostics and performance monitoring
    - `datetime`, `time` - Date/time calculations and performance timing

    Input Files:
    ------------
    - `user_data/user_responses.txt` - Plain text file containing user's natural language query
    - `auth/client_secret.json` - Google OAuth 2.0 client credentials (from Google Cloud Console)
    - `auth/token.json` - Stored OAuth access tokens (auto-generated on first run)

    Output:
    -------
    - Console output: Friendly schedule summary displayed to the user
    - Log files: Timestamped session logs in `logs/run_YYYY-MM-DD_HH-MM-SS/` containing:
        * `system.log` - Runtime metrics, errors, and performance data
        * `user_input.log` - User queries and interaction history
        * `gemini.log` - AI prompts, responses, and model interactions
        * `calendar.log` - Calendar API requests, responses, and event data
"""

def handle_user_query(query: str):
    """
    Processes natural language user queries and returns appropriate calendar summaries.

    This function serves as the main query router, parsing user input to determine the requested
    time range and coordinating between calendar fetching, profile inference, and AI summarization.
    It supports four main query types with different AI temperature settings for optimal responses.

    Processing Pipeline:
    -------------------
    1. Convert query to lowercase for case-insensitive matching
    2. Iterate through supported keywords to find a match
    3. Call appropriate calendar handler function to fetch events
    4. Generate user profile inference from event patterns using Gemini AI
    5. Summarize schedule with context-appropriate AI temperature setting
    6. Log performance metrics and return formatted response

    Parameters:
    -----------
    query (str): Natural language user input string containing time-related keywords
                Example inputs: "What do I have this week?", "Show me tomorrow's schedule"

    Returns:
    --------
    str: Human-readable schedule summary formatted for users with memory challenges,
         or error message if processing fails or no keywords are recognized

    """
    
    start_time = time.time()
    query_lower = query.lower()

    query_handlers = {
        "this week":    {"func": get_this_week_events,    "label": "this week", "temp": 0.3},
        "next week":    {"func": get_next_week_events,    "label": "next week", "temp": 0.3},
        "today":        {"func": get_events_for_today,    "label": "today",     "temp": 0.8},
        "tomorrow":     {"func": get_events_for_tomorrow, "label": "tomorrow",  "temp": 0.8},
    }

    try:
        for keyword, handler in query_handlers.items():
            if keyword in query_lower:
                user_logger.info(f"Interpreted query as: '{keyword}'")  # Optional
                events = handler["func"]()
                profile = infer_user_profile_from_events(events)
                result = summarize_schedule(events, profile, handler["label"], temperature=handler["temp"])

                duration = round(time.time() - start_time, 2)
                system_logger.info(f"[User Query] Processed in {duration} seconds")
                if duration > 30:
                    system_logger.warning(f"[Runtime] Slow response: {duration} seconds")
                return result

        # If no keyword matched:
        system_logger.warning(f"[User Query] No recognizable keyword in query: '{query}'")
    
    except Exception as e:
        system_logger.error(f"[User Query] Error: {e}")
        return "There was an error processing your request."

if __name__ == "__main__":

    # Read user query from file
    with open("user_data/user_responses.txt", "r") as f:
        query = f.read().strip()
        if not query:
            system_logger.error("[User Query] Empty input detected.")
        user_logger.info(f"User input: {query}")

    # Process and summarize the calendar schedule
    response = handle_user_query(query)
    
    # Log the final response
    gemini_logger.info("=" * 40)
    gemini_logger.info(f"[FINAL RESPONSE]\n{response}")
        
    print("\nGemini Response:\n")
    print(response)