def start(key, code):

    # Define variables
    listOfKeyCharacters = list(key)
    length = len(listOfKeyCharacters)
    column = int(length / code)
    remainder = length % code
    extra = 0
    cypherRows = []
    cypherKey = ""
    keyLines = []

    for _ in range(code):  # Reorders the key into rows based on the user input code
        keyLine = ""
        if remainder != 0:
            extra += 1
            remainder -= 1
        else:
            extra = 0
        for i in range(column + extra):
            try:
                keyLine += listOfKeyCharacters.pop(0)
            except IndexError:
                pass
        keyLines.append(list(keyLine))
        extra -= 1

    for n in range(column + 1):  # Creates output versions of both the cypher text and its row format
        line = ''
        for i in range(code):
            try:
                columnList = keyLines[i]
                line += columnList[n]
            except IndexError:
                pass

        cypherKey += line
        cypherRows.append(line)

    return cypherRows, cypherKey
