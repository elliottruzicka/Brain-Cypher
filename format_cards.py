def start(cardList):

    # Define variables
    printString = ""

    for i in range(len(cardList)):  # Format the card list into a single string for text output
        printString += "------------------------------\n\n"
        card = cardList[i]
        card.insert(2-i, "\n")
        for n in range(len(card)):
            printString += card[n] + "\n\n"
        printString += "\n------------------------------\n\n"

    return printString