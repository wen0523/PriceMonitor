def getMessage(limit,data):
    message = ''
    sorted_data = sorted(data, key=lambda x: x[1])
    
    if limit > len(data):
        limit = len(data)

    for i in range(0,limit):
        item = sorted_data[i]
        message += f"\nSymbol: {item[0]}, Price Change: {item[1]}%"
    
    return message