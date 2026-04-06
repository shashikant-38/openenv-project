This project implements a Content Moderation Environment using OpenEnv and FastAPI, designed to simulate how an AI system learns to moderate user-generated content.

It models a real-world moderation workflow where an agent evaluates text and decides whether to:

✅ ALLOW
⚠️ FLAG
❌ REMOVE
🎯 Objective

To create a reinforcement learning-style environment where:

The system provides a text (state)
The agent takes an action (moderation decision)
The environment returns a reward based on correctness
⚙️ Features
✅ 1. Rule-Based Moderation Logic
Uses predefined dataset and rules
Classifies content into:
Toxic
Neutral
Safe
✅ 2. Reinforcement Learning Structure

Implements core RL components:

Component	Description
reset()	Generates new text (state)
step()	Takes action and returns reward
reward	Based on correctness
done	Episode ends after one step
✅ 3. Toxicity Scoring
Detects toxic words like:
"hate", "idiot", "useless", "stupid"
Calculates a simple toxicity score (0–1)
✅ 4. Difficulty Levels

Each input is categorized into:

🟢 Easy → clearly toxic/safe
🟡 Medium → ambiguous
🔴 Hard → sarcasm or subtle tone
✅ 5. OpenEnv API Integration

Provides REST endpoints:

POST /reset → Get new content
POST /step → Submit action and get reward
