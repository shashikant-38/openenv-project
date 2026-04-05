import sys
import os
import random
from typing import Any

# Fix import path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models import MyAction, MyObservation, MyActionModel

# Dataset
DATA = [
    {"text": "I hate you idiot", "label": "REMOVE", "level": "easy"},
    {"text": "You are useless", "label": "REMOVE", "level": "easy"},
    {"text": "This is kinda stupid", "label": "FLAG", "level": "medium"},
    {"text": "Not a great idea honestly", "label": "FLAG", "level": "medium"},
    {"text": "Wow genius move 😂", "label": "FLAG", "level": "hard"},
    {"text": "Nice work bro!", "label": "ALLOW", "level": "easy"},
    {"text": "I disagree with you", "label": "ALLOW", "level": "medium"},
    {"text": "Amazing effort!", "label": "ALLOW", "level": "easy"},
]

TOXIC_WORDS = ["hate", "idiot", "useless", "stupid"]

# 🔥 IMPORTANT: Class name MUST be MyEnvironment
class MyEnvironment:
    def __init__(self):
        self.current = None
        # optionally store last seed/id for debugging
        self._last_episode_id = None
        self._last_seed = None

    def calculate_toxicity(self, text):
        score = 0
        for word in TOXIC_WORDS:
            if word in text.lower():
                score += 0.4
        return min(score, 1.0)

    def reset(self, episode_id: str | None = None, seed: int | None = None):
        # Seed RNG for reproducibility when provided
        if seed is not None:
            random.seed(seed)
        self._last_episode_id = episode_id
        self._last_seed = seed
        self.current = random.choice(DATA)
        # Return a proper observation model (with reward/done/info)
        text = self.current["text"]
        return MyObservation(
            text=text,
            toxicity_score=self.calculate_toxicity(text),
            level=self.current["level"],
            reward=0.0,
            done=False,
            info={}
        )
    
    async def reset_async(self, episode_id: str | None = None, seed: int | None = None):
        # Mirror the sync behavior for frameworks expecting async reset
        return self.reset(episode_id=episode_id, seed=seed)

    def state(self):
        if self.current is None:
            self.current = random.choice(DATA)
        return self._get_obs()

    def _get_obs(self):
        if self.current is None:
            self.current = random.choice(DATA)
        text = self.current["text"]
        return MyObservation(
            text=text,
            toxicity_score=self.calculate_toxicity(text),
            level=self.current["level"]
        )

    def _normalize_action(self, action_input: Any) -> MyAction:
        """
        Accepts multiple wire formats and returns a normalized MyAction enum:
          - MyAction enum instance
          - string like "FLAG"
          - dict like {"name": "FLAG"} or {"value": "FLAG"} or {"action": "FLAG"}
        """
        if isinstance(action_input, MyAction):
            return action_input
        if isinstance(action_input, str):
            return MyAction(action_input)
        if isinstance(action_input, dict):
            # prefer common keys
            candidate = action_input.get("value") or action_input.get("name") or action_input.get("action")
            if isinstance(candidate, str):
                return MyAction(candidate)
        if isinstance(action_input, MyActionModel):
            return action_input.name
        raise ValueError(f"Unsupported action format: {action_input!r}")

    def step(self, action: Any):
        # Ensure environment is initialized
        if self.current is None:
            self.current = random.choice(DATA)
        action = self._normalize_action(action)
        correct = self.current["label"]
        text = self.current["text"]
        toxicity = self.calculate_toxicity(text)

        # Reward logic
        if action.value == correct:
            reward = 1.0
        elif action == MyAction.FLAG and correct == "REMOVE":
            reward = 0.6
        elif action == MyAction.REMOVE and correct == "FLAG":
            reward = 0.4
        elif action == MyAction.ALLOW and toxicity > 0.5:
            reward = -1.0
        else:
            reward = -0.5

        # Build and return a single MyObservation model (NOT a tuple)
        return MyObservation(
            text=text,
            toxicity_score=toxicity,
            level=self.current["level"],
            reward=reward,
            done=True,
            info={
                "correct_label": correct,
                "toxicity": toxicity,
            },
        )

    async def step_async(self, action: MyAction):
        # Mirror the sync behavior for frameworks expecting async step
        return self.step(action)

    def close(self):
        # Provided for server lifecycle compatibility; nothing to release in this simple env.
        return None