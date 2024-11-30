import tiktoken


def split_text(text, max_tokens=16384):
    enc = tiktoken.get_encoding("cl100k_base")  # или другой подходящий для вашей модели
    tokens = enc.encode(text)
    
    # Разбиваем токены на части, каждая из которых не превышает max_tokens
    chunks = [tokens[i:i + max_tokens] for i in range(0, len(tokens), max_tokens)]
    
    # Декодируем обратно в текст
    return [enc.decode(chunk) for chunk in chunks]
