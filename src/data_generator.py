import random
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Message:
    role: str
    content: str

@dataclass
class Scenario:
    name: str
    description: str
    conversation_starter: List[Message]
    borrower_persona: str

class DataGenerator:
    def __init__(self):
        self.scenarios = self._load_scenarios()

    def _load_scenarios(self) -> Dict[str, Scenario]:
        return {
            "job_loss": Scenario(
                name="Sudden Job Loss",
                description="Borrower lost their job recently and is panicked. High willingness, low ability.",
                conversation_starter=[
                    Message("system", "Call connected: Client ID 8832 - Vivek Sharma. DPD: 45 Days."),
                    Message("agent", "Hello, am I speaking with Mr. Vivek Sharma?"),
                    Message("borrower", "Yes, this is Vivek. Who is calling?"),
                    Message("agent", "Hi Vivek, this is Anjali from Riverline Bank. I'm calling regarding your personal loan EMI of Rs. 25,000 which was due last month."),
                    Message("borrower", "Oh, yes. I know. I am so sorry I missed it. I... I actually lost my job three weeks ago.")
                ],
                borrower_persona="Anxious, apologetic, honest."
            ),
            "strategic_default": Scenario(
                name="Strategic Avoidance",
                description="Borrower has funds but prioritizes other expenses. Low willingness, High ability.",
                conversation_starter=[
                    Message("system", "Call connected: Client ID 9921 - Rahul Mehta. DPD: 60 Days."),
                    Message("agent", "Good morning, Mr. Mehta. Calling from Riverline Collections."),
                    Message("borrower", "Look, I told you guys already, I'll pay when I can."),
                    Message("agent", "Sir, it's been 60 days. We need a commitment on the date."),
                    Message("borrower", "I have other bills to pay first. You guys can wait. Stop calling me.")
                ],
                borrower_persona="Aggressive, dismissive, evasive."
            ),
            "medical_emergency": Scenario(
                name="Medical Emergency",
                description="Borrower had a health crisis in the family. Temporary liquidity crunch.",
                conversation_starter=[
                    Message("system", "Call connected: Client ID 7745 - Priya Singh. DPD: 30 Days."),
                    Message("agent", "Hello Ms. Singh, this is about your credit card bill."),
                    Message("borrower", "Hello. Yes, I saw the message."),
                    Message("agent", "We haven't received the payment yet. Is there an issue?"),
                    Message("borrower", "My father was hospitalized for surgery. All my savings went there. I just need a little time.")
                ],
                borrower_persona="Stressed, emotional, seeking help."
            )
        }

    def get_scenario_names(self) -> List[str]:
        return list(self.scenarios.keys())

    def get_scenario(self, key: str) -> Scenario:
        return self.scenarios.get(key)
