def depolymerize(data):
    data = list(data)
    i = 0
    while i < len(data) - 1:
        ca = data[i]
        cb = data[i + 1]
        if ca != cb and ca.lower() == cb.lower():
            data[i : i + 2] = []
            continue
        i += 1
    return ''.join(data)


input_data = open('input-day5.txt', 'r').read().strip()
while True:
    new_data = depolymerize(input_data)
    if new_data == input_data:
        break
    input_data = new_data
print('->', len(new_data))