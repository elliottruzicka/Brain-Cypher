def start(cypherKey):

    # Define variables
    cypherKey = list(cypherKey)
    cardDict = {0: [0, 1], 1: [0, 2], 2: [1, 2]}
    keyLineDict = {}
    cardList = []
    length = len(cypherKey)
    part = int(length / 3)
    remainder = length % 3
    extra = 0

    for i in range(3):  # Splits the cypher key into three parts
        keyLine1 = ""
        if remainder != 0:
            extra += 1
            remainder -= 1
        else:
            extra = 0
        for _ in range(part + extra):
            try:
                keyLine1 += cypherKey.pop(0)
            except IndexError:
                pass
        keyLineDict[i] = keyLine1
        extra -= 1

    for i in range(3):  # Compiles the parts into a list of pairs
        card = []
        for n in range(2):
            index = cardDict[i][n]
            card.append(keyLineDict[index])
        cardList.append(card)

    return cardList
