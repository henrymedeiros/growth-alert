from requests_html import HTMLSession
import smtplib

import email.message

session = HTMLSession()

links = [
    'https://www.gsuplementos.com.br/creatina-monohidratada-250gr-growth-supplements-p985931',
    'https://www.gsuplementos.com.br/pasta-de-amendoim-integral-torrado-1kg-growth-supplements-p988045'
]



def get_product_data(link, page_html):
    product = {
        'name': r.html.find('.topoDetalhe-boxRight-nome', first=True).text,
        'price': r.html.find('[data-desconto-boleto-valor]', first=True).text
    }
    return product

def check_availability(link, page_html):
    not_available_buy_button = r.html.find('.btIndisponivel', first=True)
    if not_available_buy_button:
        return False
    return True
   
for link in links:
    r = session.get(link)
    page_html = r.html.render(sleep=1)
    product = get_product_data(link,page_html)
    is_available = check_availability(link,page_html)
    print(product)
    print(is_available)