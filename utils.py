CHARSET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encode(num: int) -> str:
    if num == 0: return CHARSET[0]
    
    result = ""
    
    while num > 0:
        remainder = num % 62
        num = num // 62
        result += CHARSET[remainder]
    
    return result[::-1]
    
    
def decode(code: str) -> int:
    total = 0
    
    for char in code:
        total = (total * 62) + CHARSET.index(char)
    
    return total

print(decode(encode(833849921432123332)) == 833849921432123332)