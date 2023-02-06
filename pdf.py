import jinja2
import pdfkit
from datetime import datetime

my_name = "Test User"

# connect to database
# change to arbitrary input

num_rows = int(input("type in number of rows"))
data_storage = []
total = 0
for i in range(num_rows):
    line_input = input("type in the course name and the price, separated by comma")
    entry = line_input.split(",")
    entry[1] = int(entry[1])
    total += entry[1]
    data_storage.append(entry)

today_date = datetime.today().strftime("%d %b, %Y")
template_loader = jinja2.FileSystemLoader("./")
template_env = jinja2.Environment(loader = template_loader)

template = template_env.get_template("template.html")
context = {"myname": my_name, "entry": data_storage, "date": today_date, "total": total}
output_text = template.render(context)

config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
pdfkit.from_string(output_text, "pdf_generated.pdf", configuration = config, css="./style.css")

print(data_storage)


