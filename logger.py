import logging
import os
import time
from datetime import datetime 

"""
    Comprehensive Logging System for Calendar Summary Assistant

    Description:
    ------------
    This module provides a structured, multi-stream logging system designed for debugging,
    monitoring, and auditing the calendar assistant application. It automatically creates
    timestamped session directories and maintains separate log files for different operational
    concerns, enabling easy troubleshooting and performance analysis.

    Logging Architecture:
    --------------------
    Each application run generates a unique timestamped directory under `logs/` with the format
    `run_YYYY-MM-DD_HH-MM-SS`, containing four specialized log files:

    - `user_input.log` - Natural language queries, user interactions, input validation
    - `calendar.log` - Google Calendar API requests, event data, timing information  
    - `gemini.log` - AI model prompts, responses, profile inference, and summarization
    - `system.log` - Runtime metrics, authentication flows, errors, and performance warnings

    Session Management:
    ------------------
    The logging system provides visual session boundaries with ASCII banners to clearly
    demarcate different operational phases (System Startup, User Query, Gemini Session, etc.).
    This makes log analysis easier when debugging multi-step operations.

    Log Format:
    -----------
    All log entries follow a consistent timestamp format:
    `YYYY-MM-DD HH:MM:SS | LEVEL | MESSAGE`

    This standardized format enables easy parsing by log analysis tools and provides
    clear chronological ordering of events across all log streams.

    Directory Structure:
    -------------------
    ```
    logs/
    ├── run_2025-08-05_19-47-30/
    │   ├── user_input.log
    │   ├── calendar.log
    │   ├── gemini.log
    │   └── system.log
    ├── run_2025-08-05_20-01-24/
    │   └── ... (same structure)
    └── old_logs/ (manual archive directory)
    ```
"""

# Create a new log directory with timestamp for every new run
timestamp_str = datetime.now().strftime("run_%Y-%m-%d_%H-%M-%S")
LOG_DIR = os.path.join("logs", timestamp_str)
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger(name, log_file, level=logging.INFO):
    """
    Creates and configures a named logger instance with file output.

    This function initializes a logger with standardized formatting and automatic
    directory creation. It prevents duplicate handler registration and ensures
    consistent log formatting across all application components.

    Parameters:
    -----------
    name (str): Unique identifier for the logger instance
               Used internally by Python's logging system for logger retrieval
               
    log_file (str): Absolute or relative path to the target log file
                   Parent directories will be created automatically if they don't exist
                   
    level (int, optional): Minimum logging level for this logger
                          Defaults to logging.INFO
                          Common values: DEBUG(10), INFO(20), WARNING(30), ERROR(40)

    Returns:
    --------
    logging.Logger: Configured logger instance ready for use
                   Can be used immediately for logging operations

    Behavior:
    ---------
    - Automatically creates parent directories for the log file path
    - Applies standardized timestamp format: 'YYYY-MM-DD HH:MM:SS | LEVEL | MESSAGE'
    - Prevents duplicate handlers if the logger already exists
    - Thread-safe for concurrent access across multiple modules

    Notes:
    ------
    - Each logger name should be unique to avoid conflicts
    - Log files are opened in append mode, preserving previous entries
    """
    
    # Ensure the directory for the log file exists
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding duplicate handlers if already set
    if not logger.hasHandlers():
        logger.addHandler(handler)
    return logger



def log_session_start(logger, label="SESSION"):
    """
    Creates a visual session boundary marker in log files.

    This function generates a prominent ASCII banner to clearly demarcate different
    operational phases within log files. The banner includes the session type and
    timestamp, making it easy to identify when different operations began during
    log analysis and debugging.

    Parameters:
    -----------
    logger (logging.Logger): The logger instance to write the banner to
                             Should be one of the configured loggers (system, user, etc.)
                             
    label (str, optional): Descriptive label for the session type
                          Defaults to "SESSION"
                          Common values: "System Run", "User Query", "Gemini Session", "Calendar API"

    Output Format:
    --------------
    The banner creates an 80-character wide ASCII box with the following structure:
    ```
    ################################################################################
    #                                                                              #
    #                            >>> SESSION LABEL <<<                            #
    #                          TIME: YYYY-MM-DD HH:MM:SS                          #
    #                                                                              #
    ################################################################################
    ```

    Notes:
    ------
    - The banner is logged at INFO level and will appear in all standard log outputs
    - The timestamp uses the system's local timezone
    """

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    block = (
        "\n"
        + "#" * 80 + "\n"
        + "# " + " " * 76 + "#\n"
        + f"# >>> {label.upper()} <<<".center(78) + " #\n"
        + f"# TIME: {timestamp}".center(78) + " #\n"
        + "# " + " " * 76 + "#\n"
        + "#" * 80 + "\n"
    )

    logger.info(block)

# Define loggers
user_logger = setup_logger("user_input", os.path.join(LOG_DIR, "user_input.log"))
calendar_logger = setup_logger("calendar", os.path.join(LOG_DIR, "calendar.log"))
gemini_logger = setup_logger("gemini", os.path.join(LOG_DIR, "gemini.log"))
system_logger = setup_logger("system", os.path.join(LOG_DIR, "system.log"))

# Export these so main.py can access them via `from logger import ...`
__all__ = [
    "user_logger",
    "calendar_logger",
    "gemini_logger",
    "system_logger",
    "log_session_start",
    "LOG_DIR"
]