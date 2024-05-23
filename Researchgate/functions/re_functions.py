import re

def split_text_and_numbers(text):
    # Use regular expressions to find alphabetic characters and everything else separately
    text_part = ''.join(re.findall(r'[A-Za-z]', text))
    other_part = ''.join(re.findall(r'[^A-Za-z]', text)) 
    return text_part, other_part