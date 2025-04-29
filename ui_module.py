from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QAction, QPushButton, QListWidget, QComboBox, QLabel, QSpacerItem, QSizePolicy, QFileDialog, QInputDialog, QMessageBox
from PyQt6.QtGui import QIcon


class MyWindow(QMainWindow):
    def __init__(self, db, graphics):
        super().__init__()
        self.db = db
        self.graphics = graphics
        self.setWindowTitle("Analytic Program")
        self.resize(800, 600)
        self.allData = None
        self.paperName = None
        self.putOrCall = "put"
        self.tableName = None
        self.init_ui()
        
    def init_ui(self):
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        buttonMenuOpenDB = QAction(self, icon=QIcon("OpenButPicture.png"), text="Open database")
        buttonMenuOpenDB.setStatusTip("Открыть базу данных по ценным бумагам")
        buttonMenuOpenDB.triggered.connect(self.openDB)
        file_menu.addAction(buttonMenuOpenDB)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        self.control_panel = QWidget(self)
        self.control_layout = QVBoxLayout(self.control_panel)
        self.control_panel.setFixedWidth(200)

        self.graph_widget = QWidget(self)
        self.graph_layout = QVBoxLayout(self.graph_widget)

        self.listOfDatesExp = QListWidget(self)
        self.listOfDatesExp.setSelectionMode(QListView.SelectionMode.ExtendedSelection)

        self.listOfTradingDates = QListWidget(self)
        self.listOfTradingDates.setSelectionMode(QListView.SelectionMode.ExtendedSelection)

        self.buttonCreateGraph = QPushButton(self)
        self.buttonCreateGraph.setText("Create Graphic")
        self.buttonCreateGraph.clicked.connect(self.createGraphics)

        self.main_layout.addWidget(self.graph_widget)
        self.main_layout.addWidget(self.control_panel)

        self.comboboxNameOfPapers = QComboBox(self)
        self.textNameOfPapers = QLabel("Choose your paper:", self)

        self.textDateOfExp = QLabel("Choose your datas:", self)
        self.textTradingDatas = QLabel("Choose your trading datas:", self)

        self.buttonPutOrCall = QPushButton(f"Mode: {self.putOrCall}", self)
        self.buttonPutOrCall.clicked.connect(self.putOrCallMethod)

        self.comboboxGraphicOptions = QComboBox(self)
        self.comboboxGraphicOptions.addItems(["Vol/Strike Graph", "OI/Strike Graph"])

        self.control_layout.setSpacing(5)
        self.control_layout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        self.control_layout.addWidget(self.textNameOfPapers)
        self.control_layout.addWidget(self.comboboxNameOfPapers)
        self.control_layout.addWidget(self.comboboxGraphicOptions)
        self.control_layout.addWidget(self.textDateOfExp)
        self.control_layout.addWidget(self.listOfDatesExp)
        self.control_layout.addWidget(self.buttonPutOrCall)
        self.control_layout.addWidget(self.buttonCreateGraph)
        self.control_layout.addWidget(self.textTradingDatas)
        self.control_layout.addWidget(self.listOfTradingDates)
        self.control_layout.addStretch(1)

        self.comboboxNameOfPapers.currentTextChanged.connect(self.loadDateOfExp)

    def openDB(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "*.db")
        if file_path:
            self.db.open_db(file_path)
            tables = self.db.get_tables()
            tables, okPressed = QInputDialog.getItem(self, "Select table", "Choose your table:", tables, 0, False)
            if tables and okPressed:
                self.tableName = tables
                self.arrOfPapers = self.db.get_symbols(tables)
                self.comboboxNameOfPapers.clear()
                self.comboboxNameOfPapers.addItems(self.arrOfPapers)

    def loadDateOfExp(self, paper_name):
        self.paperName = paper_name
        expiration_dates = self.db.get_expiration_dates(paper_name, self.tableName)
        self.listOfDatesExp.clear()
        self.listOfDatesExp.addItems(expiration_dates)
        trading_dates = self.db.get_trading_dates(paper_name, self.tableName)
        self.listOfTradingDates.clear()
        self.listOfTradingDates.addItems(trading_dates)

    def createGraphics(self):
        selected_dates = [item.text() for item in self.listOfDatesExp.selectedItems()]
        selected_trading_dates = [item.text() for item in self.listOfTradingDates.selectedItems()]
        self.graphics.create_graphic(selected_dates, selected_trading_dates, self.comboboxGraphicOptions.currentText(), self.tableName, self.paperName, self.putOrCall)

    def putOrCallMethod(self):
        if self.putOrCall == "put":
            self.putOrCall = "call"
        elif self.putOrCall == "call":
            self.putOrCall = "put and call"
        else:
            self.putOrCall = "put"
        self.buttonPutOrCall.setText(f"Mode: {self.putOrCall}")