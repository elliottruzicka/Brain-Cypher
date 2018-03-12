import base64
from FileData import FileData

file = FileData('icon.py')

with open("brain-cypher.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

file.write_file('brainCypherString = ' + str(encoded_string))
