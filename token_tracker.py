import tiktoken
from datetime import datetime
import json
import os

class TokenTracker:
    def __init__(self):
        """Initialize the token tracker."""
        self.encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        self.costs = {
            "gpt-3.5-turbo": {
                "input": 0.0000015,  # $0.0015 per 1K tokens
                "output": 0.000002   # $0.002 per 1K tokens
            }
        }
        self.usage_file = "token_usage.json"
        self.load_usage()
    
    def load_usage(self):
        """Load usage data from file."""
        if os.path.exists(self.usage_file):
            with open(self.usage_file, 'r') as f:
                self.usage = json.load(f)
        else:
            self.usage = {
                "total_tokens": 0,
                "total_cost": 0.0,
                "daily_usage": {},
                "model_usage": {}
            }
    
    def save_usage(self):
        """Save usage data to file."""
        with open(self.usage_file, 'w') as f:
            json.dump(self.usage, f)
    
    def count_tokens(self, text):
        """Count tokens in a text string."""
        return len(self.encoding.encode(text))
    
    def calculate_cost(self, model, input_tokens, output_tokens):
        """Calculate cost for token usage."""
        if model not in self.costs:
            return 0.0
        
        input_cost = (input_tokens / 1000) * self.costs[model]["input"]
        output_cost = (output_tokens / 1000) * self.costs[model]["output"]
        return input_cost + output_cost
    
    def track_usage(self, model, input_text, output_text):
        """Track token usage and costs."""
        input_tokens = self.count_tokens(input_text)
        output_tokens = self.count_tokens(output_text)
        total_tokens = input_tokens + output_tokens
        cost = self.calculate_cost(model, input_tokens, output_tokens)
        
        # Update total usage
        self.usage["total_tokens"] += total_tokens
        self.usage["total_cost"] += cost
        
        # Update daily usage
        today = datetime.now().strftime("%Y-%m-%d")
        if today not in self.usage["daily_usage"]:
            self.usage["daily_usage"][today] = {
                "tokens": 0,
                "cost": 0.0
            }
        self.usage["daily_usage"][today]["tokens"] += total_tokens
        self.usage["daily_usage"][today]["cost"] += cost
        
        # Update model usage
        if model not in self.usage["model_usage"]:
            self.usage["model_usage"][model] = {
                "tokens": 0,
                "cost": 0.0
            }
        self.usage["model_usage"][model]["tokens"] += total_tokens
        self.usage["model_usage"][model]["cost"] += cost
        
        self.save_usage()
        return total_tokens, cost
    
    def get_usage_summary(self):
        """Get a summary of token usage and costs."""
        return {
            "total_tokens": self.usage["total_tokens"],
            "total_cost": self.usage["total_cost"],
            "today_tokens": self.usage["daily_usage"].get(
                datetime.now().strftime("%Y-%m-%d"), 
                {"tokens": 0}
            )["tokens"],
            "today_cost": self.usage["daily_usage"].get(
                datetime.now().strftime("%Y-%m-%d"), 
                {"cost": 0.0}
            )["cost"]
        } 