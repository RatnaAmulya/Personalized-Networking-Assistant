import logging
import random
from typing import List
from transformers import pipeline, set_seed
from app.config import MODEL_NAMES
from app.schemas import UserProfile, EventContext

logger = logging.getLogger("app.services.topic_generator")

# Set seed for reproducibility
set_seed(42)

_generator = None

def get_generator():
    """
    Get or initialize the HuggingFace text generator pipeline.
    Falls back to 'fallback' if loading fails (e.g. out of memory, no internet).
    """
    global _generator
    if _generator is None:
        try:
            logger.info(f"Loading text generator model: {MODEL_NAMES['text_generator']}")
            _generator = pipeline(
                "text-generation",
                model=MODEL_NAMES["text_generator"]
            )
        except Exception as e:
            logger.error(f"Failed to load text generator: {e}. Using template-based generator.")
            _generator = "fallback"
    return _generator

def generate_template_starters(profile: UserProfile, event: EventContext, themes: List[str]) -> List[str]:
    """
    Generate highly personalized, professional, and natural conversation starters
    using structured templates based on user profile, interests, and event context.
    This acts as a reliable backup and enhancement.
    """
    theme_str = themes[0] if themes else "innovation"
    second_theme = themes[1] if len(themes) > 1 else theme_str
    interest_str = profile.interests[0] if profile.interests else "technology"
    second_interest = profile.interests[1] if len(profile.interests) > 1 else interest_str
    skill_str = profile.skills[0] if profile.skills else "problem solving"

    starters = [
        # Starter 1: Theme and Interest Intersection
        f"Hi! I noticed the discussions here are heavily centering around {theme_str}. As a {profile.profession} interested in {interest_str}, I'm curious: how do you see {theme_str} shaping your field lately?",
        
        # Starter 2: Goal and Event Focus
        f"Hello, I'm {profile.name} from {profile.company}. I'm attending {event.event_name} with the goal of {profile.goals.lower().strip('.')}. What highlights have you encountered at this {event.event_type} so far?",
        
        # Starter 3: Skill and Event Theme Focus
        f"Hi there! I've been applying some {skill_str} techniques in my work as a {profile.profession}. Given the event's theme of {second_theme}, I'd love to know if you're seeing any interesting crossovers in your industry.",
        
        # Starter 4: Profession and Bio Context
        f"Hi, I'm {profile.name}. My background is in {profile.profession}, and I'm really passionate about {profile.bio.lower().strip('.')}. I was drawn to this session on {theme_str}—what are your thoughts on where this trend is heading?",
        
        # Starter 5: General Professional/Interest Icebreaker
        f"Hi! I'm {profile.name}. I'm deeply interested in {second_interest} and wanted to see how others at {event.event_name} are addressing {theme_str}. What projects or challenges are keeping you busy these days?"
    ]
    return starters

def generate_topics(profile: UserProfile, event: EventContext, themes: List[str]) -> List[str]:
    """
    Generates 5 personalized networking conversation starters.
    Combines GPT-2 generation (if available) with high-quality structured templates.
    """
    generator = get_generator()
    
    if generator == "fallback":
        logger.info("Using template generator fallback.")
        return generate_template_starters(profile, event, themes)
        
    try:
        theme_str = ", ".join(themes[:3])
        interests_str = ", ".join(profile.interests[:3])
        
        # GPT-2 prompt optimized for generating starting questions/icebreakers
        prompt = (
            f"Here are creative networking conversation starters for an event focused on {theme_str}.\n"
            f"Attendee: {profile.name}, a {profile.profession} interested in {interests_str}.\n"
            f"Starters:\n"
            f"1."
        )
        
        outputs = generator(
            prompt, 
            max_new_tokens=100,
            num_return_sequences=1,
            pad_token_id=50256,
            temperature=0.7,
            top_k=50,
            top_p=0.9,
            repetition_penalty=1.2
        )
        
        generated_text = outputs[0]["generated_text"]
        # Extract the new generated text
        new_text = generated_text[len(prompt):]
        
        # Parse output for lines that look like list items
        lines = []
        for line in new_text.split("\n"):
            line = line.strip()
            # Clean list numbering or bullets
            if line.startswith(("-", "*", "1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.")):
                # Strip the prefix
                cleaned = line.lstrip("-*123456789. ")
                if len(cleaned) > 15:
                    lines.append(cleaned)
            elif len(line) > 25 and "?" in line:
                lines.append(line)
        
        # Deduplicate
        lines = list(dict.fromkeys(lines))
        
        # Fallback templates to complement if not enough generated
        templates = generate_template_starters(profile, event, themes)
        
        result = []
        # Add generated lines first
        for line in lines:
            if len(result) < 5:
                result.append(line)
                
        # Fill rest with templates
        for template in templates:
            if len(result) < 5:
                result.append(template)
                
        return result
        
    except Exception as e:
        logger.error(f"Error during GPT-2 generation: {e}. Falling back to templates.")
        return generate_template_starters(profile, event, themes)
