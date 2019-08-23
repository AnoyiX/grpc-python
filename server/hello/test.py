def say(i, message):
    print(str(i) + ':' + message)
    return 'received id :' + str(i)


def error():
    x = 1 / 0
    return 'error'
