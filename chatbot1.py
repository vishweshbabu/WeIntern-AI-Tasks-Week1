import re
import random

class RuleBasedChatbot:
    def __init__(self):
        # Dictionary containing intents, regex patterns, and possible responses
        self.rules = {
            "greetings": {
                "patterns": [r"\b(hi|hello|hey|namaste|morning|evening)\b"],
                "responses": ["Hello! How can I help you today?", "Hi there! What's on your mind?", "Hey! Nice to meet you."]
            },
            "bot_info": {
                "patterns": [r"\b(who are you|what are you|your name|what can you do)\b"],
                "responses": ["I am a simple rule-based chatbot created for WeIntern Week 1 task.", "I'm a bot! I can answer basic greetings and talk about the weather."]
            },
            "weather": {
                "patterns": [r"\b(weather|rain|sunny|hot|cold|temperature)\b"],
                "responses": ["I don't have real-time data, but I hope the weather is nice where you are!", "It's always perfectly digital in my world. How's the weather there?", "I suggest checking a weather app for the exact temperature!"]
            },
            "farewell": {
                "patterns": [r"\b(bye|goodbye|see you|exit|quit)\b"],
                "responses": ["Goodbye! Have a great day ahead.", "See you later! Take care.", "Bye! It was nice chatting with you."]
            }
        }
        # Fallback responses for unrecognized inputs
        self.fallback_responses = [
            "I'm sorry, I don't quite understand that.",
            "Could you rephrase that? I'm still learning.",
            "I'm just a simple bot, I don't know everything yet!",
            "Interesting! But I don't have an answer for that."
        ]

    # Intent recognition using regex keyword mapping[cite: 3]
    def get_intent(self, user_input):
        user_input = user_input.lower()
        
        for intent, data in self.rules.items():
            for pattern in data["patterns"]:
                if re.search(pattern, user_input):
                    return intent
        return None

    def generate_response(self, user_input):
        intent = self.get_intent(user_input)
        
        if intent:
            return random.choice(self.rules[intent]["responses"])
        else:
            return random.choice(self.fallback_responses)

    def start_chat(self):
        print("🤖 Chatbot Started! (Type 'exit' or 'bye' to stop)")
        print("-" * 50)
        
        while True:
            user_input = input("You: ")
            response = self.generate_response(user_input)
            print(f"Bot: {response}")
            
            # Exit condition
            if self.get_intent(user_input) == "farewell":
                break

if __name__ == "__main__":
    chatbot = RuleBasedChatbot()
    chatbot.start_chat()