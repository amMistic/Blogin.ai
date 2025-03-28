import logging
import os

# Create logs directory if not exists
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def setup_logger(name, log_file, level=logging.INFO):
    """Creates a logger with a specified file and level."""
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    
    file_handler = logging.FileHandler(os.path.join(LOG_DIR, log_file), encoding="utf-8")
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()  # Print logs to console
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger

# Create different loggers
super_agent_logger = setup_logger("SuperAgent", "super_agent.log")
keyword_logger = setup_logger("KeywordExtractionAgent", "keyword_extraction.log")
research_logger = setup_logger("ResearchAgent", "research_agent.log")
app_logger = setup_logger("App", "app.log")

reddit_logger = setup_logger("RedditAPI","reddit.log")
google_trend_logger = setup_logger("GoogleTrendAPI", "google_trend.log")
twitter_trend_logger = setup_logger("TwitteTrendAPI", "twitter_trend.log")