from jinja2 import Template, Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('./templates'))

formvalues = []
for i in range(12):
    formvalues.append("String "+str(i))

print(formvalues)

items = []
finalvalues = ["123", "456", "789", "369"]

invoice_template = env.get_template('taxinvoice.html.j2')
parsed_template = invoice_template.render(formvalues=formvalues, items=items, finalvalues=finalvalues)

with open('./taxinvoice.htm', 'w') as page:
    page.write(parsed_template)