import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Model names configuration
MODEL_NAMES = {
    "event_analysis": os.getenv("EVENT_ANALYSIS_MODEL", "facebook/bart-large-mnli"),
    "text_generator": os.getenv("TEXT_GENERATOR_MODEL", "gpt2")
}

# Fact check API endpoint
FACT_CHECK_API = os.getenv("FACT_CHECK_API", "https://en.wikipedia.org/api/rest_v1/page/summary")
