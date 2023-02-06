# import pyqt module
import sys
from PyQt6.QtWidgets import(
    QApplication,
    QFormLayout,
    QLineEdit,
    QPlainTextEdit,
    QWidget,
    QDialog,
    QDialogButtonBox,
    QVBoxLayout,
    QHBoxLayout
)

from datetime import datetime
import jinja2
import pdfkit

class Login(QDialog):
    def __init__(self):
        super().__init__()
        self.loginLayout = QVBoxLayout()

class Window(QDialog):
    def __init__(self):
        super().__init__() # parent = None??
        self.setWindowTitle("receipt system")
        self.appLayout = QVBoxLayout() #
        formLayout = QFormLayout()

        self.name = QLineEdit()
        formLayout.addRow("Name: ", self.name)
        self.class_pricing = QPlainTextEdit()
        formLayout.addRow("class,pricing: ", self.class_pricing)
        self.note = QLineEdit()
        formLayout.addRow("note", self.note)

        self.appLayout.addLayout(formLayout)
        
        self.buttons = QDialogButtonBox()
        self.buttons.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel|
            QDialogButtonBox.StandardButton.Ok
        )

        # https://stackoverflow.com/questions/33547821/execute-function-after-click-ok-qdialogbuttonbox
        # try-except case
        self.buttons.accepted.connect(self._accept)
        self.buttons.rejected.connect(self._reject)
        
        self.appLayout.addWidget(self.buttons)
        self.setLayout(self.appLayout)

    def _accept(self):
        # Q: how to extract the information in input box of formlayout?
        name_data = self.name.text()
        # http://www.learningaboutelectronics.com/Articles/How-to-retrieve-data-from-plain-text-edit-qt-widget-c++.php
        class_pricing_data = self.class_pricing.toPlainText()
        note_data = self.note.text()
        # generating pdf file
        pdf_file(name_data, class_pricing_data, note_data)

        sys.exit()

    def _reject(self):
        # TODO: clear the dialog box
        self.name.setText("")
        self.class_pricing.clear()
        self.note.setText("")
        print("request declined.")
        # sys.exit()
    
def pdf_file(name, class_price, note):
    print("entered this line")
    class_price_list = class_price.split("\n")
    print(class_price_list)
    
    total = 0
    storage = []
    for line_input in class_price_list:
        entry = line_input.split(",")
        entry[1] = int(entry[1])
        total += entry[1]
        storage.append(entry)

    today_date = datetime.today().strftime("%d %b, %Y")

    # loading template
    template_loader = jinja2.FileSystemLoader("./")
    template_env = jinja2.Environment(loader = template_loader)

    template = template_env.get_template("template.html")
    context = {"myname": name, "entry": storage, "date": today_date, "total": total}
    output_text = template.render(context)

    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
    pdfkit.from_string(output_text, "pdf_generated.pdf", configuration = config, css="./style.css")


        
if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
