import pdfkit
import jinja2
from datetime import datetime

def pdfFile(name, class_price, note):
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
    template_loader = jinja2.FileSystemLoader("../template")
    template_env = jinja2.Environment(loader = template_loader)

    template = template_env.get_template("template.html")
    context = {"myname": name, "entry": storage, "date": today_date, "total": total, "note": note}
    output_text = template.render(context)

    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
    pdfkit.from_string(output_text, "../pdf_generated.pdf", configuration = config, css="../template/style.css")

