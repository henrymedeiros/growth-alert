import os
import smtplib
import email.message
from dotenv import load_dotenv
from requests_html import HTMLSession

def read_links_from_txt():
    with open('links.txt', 'r') as f:
        links = f.read().splitlines()
        return links

def check_availability():
    not_available_buy_button = page_html.find('.btIndisponivel', first=True)
    if not_available_buy_button:
        return False
    return True

def get_product_data(page_html):
    name = page_html.find('.topoDetalhe-boxRight-nome', first=True).text
    price = page_html.find('[data-desconto-boleto-valor]', first=True).text
    if name is None or price is None:
        print('erro ao pegar infos do produto')
    product = {
        'name': name,
        'price': price,
        'is_available': check_availability(page_html),
    }
    return product

def send_mail(product, user_email, password, email_list = []):
    msg = email.message.Message()
    msg['Subject'] = f"[ALERTA GROWTH] - {product['name']}"
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(f"O item {product['name']} está disponível por {product['price']}! <br> Acesse o link: " + link)
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(user_email, password)
    if(len(email_list) > 0):
        for e in email_list:
            s.sendmail(user_email, e, msg.as_string().encode('utf-8'))
    else:
        s.sendmail(user_email, user_email, msg.as_string().encode('utf-8'))
    print('Email enviado!')

def main():
    load_dotenv()
    session = HTMLSession()
    links = read_links_from_txt()

    for link in links:
        r = session.get(link)
        r.html.render(sleep=2)
        page_html = r.html
        product = get_product_data(page_html)
        print(product)
        if(product['is_available']):        
            send_mail(product, os.getenv('USER_EMAIL'), os.getenv('APP_PASSWORD'), os.getenv('EMAIL_LIST').split(','))

main()
    

