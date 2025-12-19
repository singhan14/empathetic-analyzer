from typing import Dict, List, Tuple
from textblob import TextBlob
import random
import re

class AnalyzerEngine:
    """
    Advanced analyzer with:
    - TextBlob for sentiment analysis
    - Component-Based Response Generation (Simulates LLM variety without API issues)
    """
    
    def __init__(self):
        print("Analyzer Engine initialized")
        print("- Sentiment: TextBlob (NLP)")
        print("- Response Generation: Component-Based Construction")
        
        # Load response components
        self._init_response_components()

    def _init_response_components(self):
        """Initialize components for building dynamic sentences."""
        
        self.components = {
            "Ability Issue": {
                "intros": [
                    "I hear you,", "I understand,", "Thank you for sharing that,", 
                    "I appreciate your honesty,", "I can see this is difficult,"
                ],
                "empathy": [
                    "financial constraints can be incredibly stressful.",
                    "it sounds like you're going through a tough time right now.",
                    "we know that unexpected expenses happen.",
                    "your situation sounds challenging.",
                    "managing finances during a crisis is never easy."
                ],
                "solutions": [
                    "Let's look at a payment holiday for a few weeks.",
                    "We can explore restructuring your loan to lower the EMI.",
                    "Would a temporary freeze on interest help you get back on track?",
                    "I can check if you qualify for our hardship assistance program.",
                    "How about we pause payments for this month?"
                ]
            },
            "Willingness Issue": {
                "intros": [
                    "I understand you have other priorities,", "I hear your frustration,", 
                    "I want to be transparent with you,", "I need to be direct,"
                ],
                "reality_check": [
                    "however, a default stays on your record for 7 years.",
                    "but delaying this further will severely impact your CIBIL score.",
                    "ignoring this won't make the debt go away.",
                    "but this account is scheduled for legal escalation next week.",
                    "consequences like legal notices are automated after 90 days."
                ],
                "actions": [
                    "Can we clear just the minimum due today?",
                    "Is there any partial amount you can pay right now to hold off action?",
                    "Let's avoid that - can you commit to a date this week?",
                    "I can hold off the legal team if you make a small payment today.",
                    "Please make a payment today to protect your credit score."
                ]
            },
            "Discovery": {
                "intros": [
                    "I'd like to understand help,", "To find the best solution,", 
                    "I'm here to work with you,", "Help me understand,"
                ],
                "questions": [
                    "could you tell me a bit more about what's causing the delay?",
                    "is this a temporary cash flow issue or something longer term?",
                    "what specifically is preventing payment right now?",
                    "are there other debts you are prioritizing at the moment?",
                    "what would make it easier for you to pay this month?"
                ]
            }
        }

    def analyze_sentiment(self, text: str) -> Dict:
        """TextBlob-based sentiment analysis."""
        if not text or len(text.strip()) < 3:
            return {"label": "NEUTRAL", "score": 0.5, "polarity": 0.0}
        
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.1:
                label = "POSITIVE"
                score = 0.5 + (polarity * 0.5)
            elif polarity < -0.1:
                label = "NEGATIVE"
                score = 0.5 + (abs(polarity) * 0.5)
            else:
                label = "NEUTRAL"
                score = 0.5
            
            return {"label": label, "score": min(0.99, score), "polarity": round(polarity, 2)}
        except Exception:
            return {"label": "NEUTRAL", "score": 0.5, "polarity": 0.0}

    def classify_intent(self, conversation_history: List[Dict]) -> Tuple[str, float, str]:
        """Classify intent based on weighted keywords."""
        relevant_msgs = [m.get('content', '').lower() for m in conversation_history if m.get('role') == 'borrower']
        full_text = " ".join(relevant_msgs[-3:]) 
        
        # Specific keywords
        ability_keywords = ["lost job", "hospital", "medical", "broke", "no money", "salary", "check", "wait", "please", "help", "constraints", "tight", "struggle", "financial", "afford", "cannot pay", "can't pay", "unable"]
        willingness_keywords = ["busy", "stop", "lawyer", "sue", "care", "won't", "will not", "scam", "harass", "don't want", "why should i", "refuse"]
        
        a_score = sum(2 for w in ability_keywords if w in full_text)
        w_score = sum(2 for w in willingness_keywords if w in full_text)
        
        # Keyword overrides for very short messages
        last_msg = relevant_msgs[-1] if relevant_msgs else ""
        if any(x in last_msg for x in ["cannot pay", "can't pay", "unable", "broke"]): a_score += 5
        if any(x in last_msg for x in ["won't pay", "will not", "refuse"]): w_score += 5

        if a_score > w_score:
            return "🟢 Ability Issue (Distress)", 0.85, "Detected financial constraint language."
        elif w_score > a_score:
            return "🔴 Willingness Issue (Strategic)", 0.85, "Detected refusal/avoidance language."
        else:
            return "🔵 Discovery Needed", 0.5, "Neutral or unclear response."

    def generate_agent_response(self, intent: str, borrower_message: str, conversation_context: str = "") -> str:
        """
        Generates a unique response by combining random components.
        """
        msg_lower = borrower_message.lower()
        
        if "Ability" in intent:
            # Check for specific triggers first
            if "job" in msg_lower or "unemployed" in msg_lower:
                return "I'm sorry to hear about the job loss. That is incredibly stressful. We have a hardship program for this exact situation - can we discuss pausing your payments for 90 days?"
            if "medical" in msg_lower or "hospital" in msg_lower:
                return "I hope your family recovers soon. Health is the priority here. I can put a 'Medical Hold' on your account for 30 days so you don't receive calls. Does that help?"
            
            # General Construction
            comps = self.components["Ability Issue"]
            return f"{random.choice(comps['intros'])} {random.choice(comps['empathy'])} {random.choice(comps['solutions'])}"

        elif "Willingness" in intent:
            comps = self.components["Willingness Issue"]
            return f"{random.choice(comps['intros'])} {random.choice(comps['reality_check'])} {random.choice(comps['actions'])}"
            
        else:
            comps = self.components["Discovery"]
            return f"{random.choice(comps['intros'])} {random.choice(comps['questions'])}"

    def recommend_strategy(self, intent: str, sentiment: Dict) -> Dict:
        """Returns strategic recommendation."""
        strat = {}
        if "Ability" in intent:
            strat["Action"] = "💚 Restructuring & Support"
            strat["Script"] = "Offer empathy + payment plan restructuring (NPV maximization)"
            strat["Tone"] = "Supportive"
            strat["Economic Principle"] = "Preserve long-term value via temporary relief"
        elif "Willingness" in intent:
            strat["Action"] = "🔶 Assertive Negotiation"
            strat["Script"] = "Highlight credit score damage (CIBIL) & legal escalation"
            strat["Tone"] = "Firm but Professional"
            strat["Economic Principle"] = "Increase cost of default"
        else:
            strat["Action"] = "🔵 Root Cause Analysis"
            strat["Script"] = "Ask diagnostic questions to categorize default type"
            strat["Tone"] = "Inquisitive"
            strat["Economic Principle"] = "Information asymmetry reduction"
            
        return strat
