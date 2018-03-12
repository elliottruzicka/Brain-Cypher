from functools import partial
import generate_private_key
import create_cypher
import split_cypher_into_pairs
import format_cards
import cards_output
from PySide.QtCore import QByteArray, QThread, Signal, Qt
from PySide.QtGui import QImage, QApplication, QClipboard, QTextEdit, QMainWindow, QPixmap, QIcon, QHBoxLayout, \
    QVBoxLayout, QLabel, QComboBox, QPushButton, QFont, QSpinBox, QTextOption, QFrame, QWidget, QSplashScreen
import sys
import os
import ctypes
from time import sleep
from key_format import formatDict
from splash import *
from icon import *


# Convert binary image strings to usable images
baSplash = QByteArray.fromBase64(splashString)
splashByteArray = QImage.fromData(baSplash, 'PNG')
baIcon = QByteArray.fromBase64(iconString)
iconByteArray = QImage.fromData(baIcon, 'PNG')

app = QApplication(sys.argv)  # Define application

# Set some global variables
directory = os.getcwd()
clip = QClipboard()
privateKeyFormats = list(formatDict.keys())
privateKeyFormats.sort(reverse=True)
ethDonationAddress = '0x50Adc7CfDB7b52D26E3820740D0A15f614098A35'
btcDonationAddress = '1LPZ1mfSftiTcEvAfMrHEq1NhjyBVdeZLj'

# Application Information
__appname__ = 'Brain Cypher'
myappid = u'orion.brain-cypher.1.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class Worker(QThread):  # Thread class for resizing the window
    updateWindowSize = Signal()

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        sleep(.1)
        self.updateWindowSize.emit()


class GrowingTextEdit(QTextEdit):  # Sub-class for a TextEdit that can change size with its content

    def __init__(self):
        super(GrowingTextEdit, self).__init__()
        self.document().contentsChanged.connect(self.size_change)

        self.heightMin = 0
        self.heightMax = 65000

    def size_change(self):
        docHeight = self.document().size().height()
        if self.heightMin <= docHeight <= self.heightMax:
            self.setMinimumHeight(docHeight + 10)


class MainWindow(QMainWindow):  # Sets up the main window

    def resize_window(self):  # Function for resizing the window
        self.resize(self.minimumSizeHint())

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Set window Icon
        self.setWindowTitle(__appname__)
        iconImage = QImage(iconByteArray)
        iconPixmap = QPixmap(iconImage)
        self.setWindowIcon(QIcon(iconPixmap))

        # Set up private key format widgets
        privateKeyFormatLayout = QHBoxLayout()
        privateKeyFormatLabel = QLabel('Select Key Format: ')
        self.privateKeyTypeCombobox = QComboBox()
        self.privateKeyTypeCombobox.addItems(privateKeyFormats)
        self.privateKeyLengthLabel = QLabel('0')
        privateKeyFormatLayout.addWidget(privateKeyFormatLabel)
        privateKeyFormatLayout.addWidget(self.privateKeyTypeCombobox)
        privateKeyFormatLayout.addWidget(self.privateKeyLengthLabel)

        # Set up private key text widgets
        privateKeyLayout = QVBoxLayout()
        privateKeyButtonsLayout = QHBoxLayout()
        generatePrivateKeyButton = QPushButton('Generate Key')
        generatePrivateKeyButton.clicked.connect(self.get_private_key)
        self.copyPrivateKeyButton = QPushButton('Copy Key')
        self.copyPrivateKeyButton.setDisabled(True)
        self.copyPrivateKeyButton.clicked.connect(self.copy_private_key)
        privateKeyButtonsLayout.addWidget(generatePrivateKeyButton)
        privateKeyButtonsLayout.addWidget(self.copyPrivateKeyButton)
        self.privateKeyEdit = GrowingTextEdit()
        self.privateKeyEdit.setFont(QFont('Courier'))
        self.privateKeyEdit.textChanged.connect(self.private_key_or_code_changed)
        privateKeyLayout.addLayout(privateKeyButtonsLayout)
        privateKeyLayout.addWidget(self.privateKeyEdit)

        # Set up cypher code widgets
        codeLayout = QHBoxLayout()
        codeLabel = QLabel('Select Cypher Code: ')
        self.codeSelect = QSpinBox()
        self.codeSelect.setValue(10)
        self.codeSelect.setMinimum(2)
        self.codeSelect.setDisabled(True)
        self.codeSelect.valueChanged.connect(self.private_key_or_code_changed)
        codeLayout.addWidget(codeLabel)
        codeLayout.addWidget(self.codeSelect)

        # Set up cypher text widgets
        cypherLayout = QVBoxLayout()
        cypherButtonsLayout = QHBoxLayout()
        cardButtonsLayout = QHBoxLayout()
        self.generateCypherButton = QPushButton('Generate Cypher')
        self.generateCypherButton.clicked.connect(self.get_cypher)
        self.generateCypherButton.setDisabled(True)
        self.copyCypherButton = QPushButton('Copy Cypher')
        self.copyCypherButton.setDisabled(True)
        self.copyCypherButton.clicked.connect(self.copy_cypher)
        cypherButtonsLayout.addWidget(self.generateCypherButton)
        cypherButtonsLayout.addWidget(self.copyCypherButton)
        self.cypherEdit = GrowingTextEdit()
        self.cypherEdit.setFont(QFont('Courier'))
        self.cypherEdit.setReadOnly(True)
        self.cypherEdit.setVisible(False)
        self.cypherEdit.textChanged.connect(self.resize_window)
        self.cypherPreviewLabel = QLabel('-CYPHER PREVIEW-')
        self.cypherPreviewLabel.setAlignment(Qt.AlignCenter)
        self.cypherPreviewLabel.setVisible(False)
        self.cypherPreview = GrowingTextEdit()
        self.cypherPreview.setFont(QFont('Courier'))
        self.cypherPreview.setAlignment(Qt.AlignHCenter)
        self.cypherPreview.setWordWrapMode(QTextOption.NoWrap)
        self.cypherPreview.setReadOnly(True)
        self.cypherPreview.setVisible(False)
        self.cypherCardsPrintButton = QPushButton('Print Cypher Cards')
        self.cypherCardsPrintButton.setVisible(False)
        self.cypherCardsPrintButton.clicked.connect(partial(self.cards, True))
        self.cypherCardsCopyButton = QPushButton('Copy Cypher Cards')
        self.cypherCardsCopyButton.setVisible(False)
        self.cypherCardsCopyButton.clicked.connect(partial(self.cards, False))
        cardButtonsLayout.addWidget(self.cypherCardsPrintButton)
        cardButtonsLayout.addWidget(self.cypherCardsCopyButton)
        cypherLayout.addLayout(cypherButtonsLayout)
        cypherLayout.addWidget(self.cypherEdit)
        cypherLayout.addWidget(self.cypherPreviewLabel)
        cypherLayout.addWidget(self.cypherPreview)
        cypherLayout.addLayout(cardButtonsLayout)

        # Set up donation widgets
        donationsLayout = QVBoxLayout()
        separater = QFrame()
        separater.setFrameShape(QFrame.HLine)
        self.donationButton = QPushButton('Donate')
        self.donationButton.setVisible(False)
        self.donationButton.clicked.connect(self.donate)
        self.copyEthAddressButton = QPushButton('ETH: Copy Address')
        self.copyEthAddressButton.clicked.connect(self.copy_eth_donation_address)
        self.copyEthAddressButton.setVisible(False)
        self.copyBtcAddressButton = QPushButton('BTC: Copy Address')
        self.copyBtcAddressButton.clicked.connect(self.copy_btc_donation_address)
        self.copyBtcAddressButton.setVisible(False)
        donationsLayout.addWidget(separater)
        donationsLayout.addWidget(self.donationButton)
        donationsLayout.addWidget(self.copyEthAddressButton)
        donationsLayout.addWidget(self.copyBtcAddressButton)

        # Add all widgets and sub-layouts to the master layout
        self.master_layout = QVBoxLayout()
        self.master_layout.addLayout(privateKeyFormatLayout)
        self.master_layout.addLayout(privateKeyLayout)
        self.master_layout.addLayout(codeLayout)
        self.master_layout.addLayout(cypherLayout)
        self.master_layout.addLayout(donationsLayout)
        self.master_widget = QWidget()
        self.master_widget.setLayout(self.master_layout)
        self.setCentralWidget(self.master_widget)

        # Start and connect the window resizing thread
        self.worker = Worker()
        self.worker.updateWindowSize.connect(self.resize_window)

    def copy_private_key(self):  # Copies the private key text to the system clipboard
        clip.setText(self.privateKeyEdit.toPlainText())
        self.copyPrivateKeyButton.setText('Key Copied')
        app.processEvents()
        sleep(2)
        self.copyPrivateKeyButton.setText('Copy Key')

    def copy_cypher(self):  # Copies the cypher text to the system clipboard
        clip.setText(self.cypherEdit.toPlainText())
        self.copyCypherButton.setText('Cypher Copied')
        app.processEvents()
        sleep(2)
        self.copyCypherButton.setText('Copy Cypher')

    def copy_eth_donation_address(self):  # Copies the ETH donation address to the system clipboard
        clip.setText(ethDonationAddress)
        self.copyEthAddressButton.setText('ETH: Address Copied\nThanks!')
        app.processEvents()
        sleep(2)
        self.copyEthAddressButton.setText('ETH: Copy Address')

    def copy_btc_donation_address(self):  # Copies the BTC donation address to the system clipboard
        clip.setText(btcDonationAddress)
        self.copyBtcAddressButton.setText('BTC: Address Copied\nThanks!')
        app.processEvents()
        sleep(2)
        self.copyBtcAddressButton.setText('BTC: Copy Address')

    def get_private_key(self):  # Generates a key of the desired format using two instances of the SystemRandom function
        privateKey = generate_private_key.start(self.privateKeyTypeCombobox.currentText())
        self.privateKeyEdit.setText(privateKey)
        self.private_key_or_code_changed()
        self.copyPrivateKeyButton.setDisabled(False)

    def private_key_or_code_changed(self):  # Changes visibility and ability of some widgets based on user input
        self.privateKeyLengthLabel.setText(str(len(self.privateKeyEdit.toPlainText())))
        self.copyCypherButton.setDisabled(True)
        self.cypherEdit.setText('')
        self.cypherPreview.setText('')
        self.cypherEdit.setVisible(False)
        self.cypherPreviewLabel.setVisible(False)
        self.cypherPreview.setVisible(False)
        if len(self.privateKeyEdit.toPlainText()) <= 2:
            self.copyPrivateKeyButton.setDisabled(True)
            self.generateCypherButton.setDisabled(True)
            self.codeSelect.setDisabled(True)
        else:
            self.codeSelect.setMaximum(len(self.privateKeyEdit.toPlainText()) - 1)
            self.copyPrivateKeyButton.setDisabled(False)
            self.generateCypherButton.setDisabled(False)
            self.codeSelect.setDisabled(False)
        self.cypherCardsPrintButton.setDisabled(True)
        self.cypherCardsPrintButton.setVisible(False)
        self.cypherCardsCopyButton.setDisabled(True)
        self.cypherCardsCopyButton.setVisible(False)
        self.worker.start()

    def get_cypher(self):  # Converts the raw key into a cypher based on the codeSelect value
        if not 1 >= len(self.privateKeyEdit.toPlainText()) >= int(self.privateKeyLengthLabel.text()):
            self.generateCypherButton.setDisabled(False)
            cypherRows, cypherSeed = create_cypher.start(self.privateKeyEdit.toPlainText(),
                                                         self.codeSelect.value())
            self.copyCypherButton.setDisabled(False)
            self.cypherEdit.setVisible(True)
            self.cypherEdit.setText(cypherSeed)
            self.cypherPreviewLabel.setVisible(True)
            self.cypherPreview.setVisible(True)
            previewText = ''
            for i in cypherRows:
                previewText += i + '\n'
            self.cypherPreview.setText(previewText)
            self.worker.start()
            self.cypherCardsPrintButton.setDisabled(False)
            self.cypherCardsPrintButton.setVisible(True)
            self.cypherCardsCopyButton.setDisabled(False)
            self.cypherCardsCopyButton.setVisible(True)
            self.donationButton.setVisible(True)
        else:
            self.generateCypherButton.setDisabled(True)

    def cards(self, print):  # Creates and prints the output.txt file
        cardList = split_cypher_into_pairs.start(self.cypherEdit.toPlainText())
        printString = format_cards.start(cardList)
        if print:
            self.cypherCardsPrintButton.setText('Printing')
            app.processEvents()
            cards_output.start(printString)
            self.cypherCardsPrintButton.setText('Print Cypher Cards')
        else:
            clip.setText(printString)
            self.cypherCardsCopyButton.setText('Cards Copied')
            app.processEvents()
            sleep(2)
            self.cypherCardsCopyButton.setText('Copy Cypher Cards')

    def donate(self):  # Adjusts the visibility of the donation buttons
        if self.donationButton.text() == 'Donate':
            self.copyEthAddressButton.setVisible(True)
            self.copyBtcAddressButton.setVisible(True)
            self.donationButton.setText('Hide')
        elif self.donationButton.text() == 'Hide':
            self.copyEthAddressButton.setVisible(False)
            self.copyBtcAddressButton.setVisible(False)
            self.donationButton.setText('Donate')
        self.worker.start()

    def cleanup(self):  # Clears the clipboard of any copied text
        clip.setText('')



form = MainWindow()  # Define program window

# Set up and display splash screen
splashImage = QImage(splashByteArray)
splashPixmap = QPixmap(splashImage)
splashScr = QSplashScreen(splashPixmap, Qt.WindowStaysOnTopHint)
splashScr.setMask(splashPixmap.mask())
splashScr.show()
sleep(1)
app.processEvents()
splashScr.hide()
splashScr.deleteLater()

form.show()
app.aboutToQuit.connect(form.cleanup)  # Clears the clipboard when exiting
app.exec_()
