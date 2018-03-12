from key_format import formatDict
from random import SystemRandom


def start(format):

    random = SystemRandom()

    randomCharacterList = formatDict.get(format)[1]  # Get encoding alphabet based on user input
    random.shuffle(randomCharacterList)  # Randomize the alphabet order for extra random
    keyListLength = len(randomCharacterList)
    keyList = []

    for _ in range(formatDict.get(format)[0]):  # Add random characters from the encoding alphabet to a list
        i = random.randint(1, keyListLength)
        n = randomCharacterList[i-1]
        keyList.append(n)

    privateKey = "".join(keyList)  # Join the character list into a key string

    return privateKey
