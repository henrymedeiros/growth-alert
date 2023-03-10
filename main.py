import os
import smtplib
import email.message
from dotenv import load_dotenv
from requests_html import HTMLSession

load_dotenv()
session = HTMLSession()

def read_links_from_txt():
    with open('links.txt', 'r') as f:
        links = f.read().splitlines()
        return links

links = read_links_from_txt()

def get_product_data(link, page_html):
    name = r.html.find('.topoDetalhe-boxRight-nome', first=True)
    price = r.html.find('[data-desconto-boleto-valor]', first=True)
    if name is None or price is None:
        print('erro ao pegar infos do produto')
    product = {
        'name': name.text,
        'price': price.text
    }
    return product

def check_availability(link, page_html):
    not_available_buy_button = r.html.find('.btIndisponivel', first=True)
    if not_available_buy_button:
        return False
    return True

def send_mail(product, user_email, password):
    msg = email.message.Message()
    msg['Subject'] = f"[ALERTA GROWTH] - {product['name']}"
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(f"O item {product['name']} está disponível por {product['price']}! <br> Acesse o link: " + link)
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(user_email, password)
    s.sendmail(user_email, user_email, msg.as_string().encode('utf-8'))
    print('email enviado')

   
for link in links:
    r = session.get(link)
    page_html = r.html.render(sleep=2)
    product = get_product_data(link,page_html)
    is_available = check_availability(link,page_html)
    if(is_available):
        send_mail(product, os.getenv('USER_EMAIL'), os.getenv('APP_PASSWORD'))
    print(product)
    print(is_available)
