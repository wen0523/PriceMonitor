def getMessage(limit,data):
    message = ''
    sorted_data = sorted(data, key=lambda x: abs(x[1]), reverse=True)
    
    if limit > len(data):
        limit = len(data)

    for i in range(0,limit):
        item = sorted_data[i]
        message += f"\nSymbol: {item[0]}, Price Change: {item[1]}%"
    
    return message