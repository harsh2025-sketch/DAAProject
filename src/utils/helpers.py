"""
Utility functions for data generation and analysis
"""
import random
from typing import List

def generate_random_data(n: int, seed: int = 42) -> List[int]:
    """Generate n random integers"""
    random.seed(seed)
    return [random.randint(0, n * 10) for _ in range(n)]

def generate_sequential_data(n: int) -> List[int]:
    """Generate sequential integers from 0 to n-1"""
    return list(range(n))

def generate_reverse_data(n: int) -> List[int]:
    """Generate reverse sequential integers"""
    return list(range(n-1, -1, -1))

def format_time(ms: float) -> str:
    """Format time in human-readable format"""
    if ms < 1:
        return f"{ms * 1000:.2f} μs"
    elif ms < 1000:
        return f"{ms:.2f} ms"
    else:
        return f"{ms / 1000:.2f} s"

def calculate_complexity_match(actual_growth: float, expected_complexity: str) -> str:
    """
    Determine if observed growth matches expected complexity.
    Returns a match quality string.
    """
    if "O(1)" in expected_complexity:
        if actual_growth < 1.5:
            return "✅ Excellent match"
        elif actual_growth < 2.5:
            return "⚠️ Acceptable (amortized)"
        else:
            return "❌ Poor match"
    
    elif "O(log n)" in expected_complexity:
        # log growth should be minimal
        if actual_growth < 3:
            return "✅ Excellent match"
        elif actual_growth < 5:
            return "⚠️ Acceptable"
        else:
            return "❌ Poor match"
    
    elif "O(n)" in expected_complexity:
        # Linear growth expected
        if 8 < actual_growth < 15:
            return "✅ Excellent match"
        elif 5 < actual_growth < 20:
            return "⚠️ Acceptable"
        else:
            return "❌ Poor match"
    
    return "⚪ Unknown"
