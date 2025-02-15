#this is test version-main version comming soon-you can full recovery and hack crypto wallets with main versio
#developed by Navid Navidjouy with 
#MIT license
#If you have any comments or suggestions or any questions, send an this email:(navidnavidjouy.programming@gmail.com)

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QTextEdit,
    QPushButton, QStackedWidget, QMessageBox, QFileDialog
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from mnemonic import Mnemonic
from eth_account import Account
import time
import sys
import logging

# -------------------- first seeting --------------------
logging.basicConfig(
    filename="app.log",
    format="%(asctime)s - %(funcName)s - %(message)s",
    level=logging.INFO
)

Account.enable_unaudited_hdwallet_features()
mnemo = Mnemonic("english")

# --------------------  main class  --------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wallet tools(imperfect version-main version commingsooon)")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("logo.png"))
        
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        
        self.menu_page = self.create_menu_page()
        self.main_page = self.create_main_page()
        
        self.central_widget.addWidget(self.menu_page)
        self.central_widget.addWidget(self.main_page)
        
        self.dark_mode = True
        self.update_theme()

    # -------------------- menu page --------------------
    def create_menu_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        
        logo_label = QLabel()
        pixmap = QPixmap("main.png")
        logo_label.setPixmap(pixmap.scaled(1000, 500))
        layout.addWidget(logo_label)
        
        label = QLabel("choose:")
        label.setStyleSheet("font-size: 18px; margin-bottom: 10px;")
        layout.addWidget(label)
        
        btn_generate = QPushButton("Generating addresses from 12-word phrases")
        btn_generate.setStyleSheet("font-size: 16px; padding: 10px;")
        btn_generate.clicked.connect(self.switch_to_main_page)
        layout.addWidget(btn_generate)
        
        theme_btn = QPushButton("change theme ☾")
        theme_btn.clicked.connect(self.toggle_theme)
        layout.addWidget(theme_btn)
        
        page.setLayout(layout)
        return page

    # --------------------  main page --------------------
    def create_main_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        
        label = QLabel("Enter your recovery phrases:(like: word1 worde2 word3 ... word12)")
        label.setStyleSheet("font-size: 18px; margin-bottom: 10px;")
        layout.addWidget(label)
        
        self.input_area = QTextEdit()
        self.input_area.setStyleSheet("font-size: 16px; height: 150px;")
        layout.addWidget(self.input_area)
        
        process_btn = QPushButton("start generate addresses ☢")
        process_btn.clicked.connect(self.process_seed_phrases)
        layout.addWidget(process_btn)
        
        load_btn = QPushButton("Upload the recovery phrase file")
        load_btn.clicked.connect(self.load_seed_phrases_from_file)
        layout.addWidget(load_btn)
        
        save_btn = QPushButton("Save the output in file")
        save_btn.clicked.connect(self.save_output_to_file)
        layout.addWidget(save_btn)
        
        output_label = QLabel("result:")
        output_label.setStyleSheet("font-size: 18px; margin-top: 20px;")
        layout.addWidget(output_label)
        
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        layout.addWidget(self.output_area)
        
        back_btn = QPushButton("return to menu")
        back_btn.clicked.connect(self.switch_to_menu_page)
        layout.addWidget(back_btn)
        
        page.setLayout(layout)
        return page

    # -------------------- Page switch functions --------------------
    def switch_to_menu_page(self):
        self.central_widget.setCurrentWidget(self.menu_page)
    
    def switch_to_main_page(self):
        self.central_widget.setCurrentWidget(self.main_page)

    # --------------------  theme --------------------
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.update_theme()
    
    def update_theme(self):
        style_sheet = """
            background-color: #2E2E2E;
            color: white;
            QPushButton { background-color: #4A4A4A; padding: 10px; }
            QTextEdit { background-color: #1E1E1E; }
        """ if self.dark_mode else """
            background-color: white;
            color: black;
            QPushButton { background-color: lightgray; padding: 10px; }
            QTextEdit { background-color: white; }
        """
        self.setStyleSheet(style_sheet)
        for widget in self.findChildren((QLabel, QPushButton, QTextEdit)):
            widget.setStyleSheet(style_sheet)

    # -------------------- Functions processing retrieval expressions --------------------
    def process_seed_phrases(self):
        input_text = self.input_area.toPlainText().strip()
        if not input_text:
            QMessageBox.warning(self, "Error", "Please enter the recovery phrase correctly!")
            return
        
        seed_phrases = input_text.splitlines()
        self.output_area.clear()
        
        for index, phrase in enumerate(seed_phrases, 1):
            try:
                start_time = time.time()
                result = self.get_eth_address(phrase)
                processing_time = time.time() - start_time
                
                if len(result) == 2:
                    output_line = f"▣ phrase: {result[0]}\n◈ addresses: {result[1]}\nProcessing time: {processing_time:.2f} secend\n{'-'*40}"
                else:
                    output_line = f"▨ Error in phrase : {result[0]}\n✖ reason: {result[1]}\n{'-'*40}"
                
                self.output_area.append(output_line)
                QApplication.processEvents()
                time.sleep(0.1)
                
            except Exception as e:
                self.output_area.append(f"Unexpected error: {str(e)}")
    
    def get_eth_address(self, seed_phrase):
        try:
            if not mnemo.check(seed_phrase):
                return seed_phrase, "Invalid expression"
            
            time.sleep(0.5)
            account = Account.from_mnemonic(seed_phrase)
            return seed_phrase, account.address
        
        except Exception as e:
            return seed_phrase, f"Error: {str(e)}"
    
    def load_seed_phrases_from_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "File upload", "", "Text Files (*.txt)")
        if file_name:
            with open(file_name, 'r', encoding='utf-8') as file:
                self.input_area.setPlainText(file.read())
    
    def save_output_to_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save the output", "", "Text Files (*.txt)")
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(self.output_area.toPlainText())

# -------------------- Run the program --------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
