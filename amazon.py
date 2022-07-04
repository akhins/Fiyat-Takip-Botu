from distutils.command.check import check
from turtle import title
import requests
from bs4 import BeautifulSoup
import smtplib

url = "https://www.amazon.com.tr/Spigen-Rugged-Serisi-iPhone-Uyumlu/dp/B07SZHKGZJ?ref_=Oct_d_obs_d_13710045031&pd_rd_w=xAq2r&content-id=amzn1.sym.45f4ccca-3f9c-43f3-82eb-899165d0302d&pf_rd_p=45f4ccca-3f9c-43f3-82eb-899165d0302d&pf_rd_r=4TNSQBW38C073K4HN39N&pd_rd_wg=ckW8v&pd_rd_r=defb2eb4-f36e-4cf4-afe2-c6fe1bc8cb14&pd_rd_i=B07SZHKGZJ"

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36" 
}

def priceCheck(url, max_price):
    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.find(id="productTitle").getText().strip()

    price = soup.find("span",{"class":"a-offscreen"}).getText().strip()

    new_price = float(price[:-5].replace(",","."))

    if(new_price >= max_price):
        send_Email("TO_EMAİL", url)
    else:
        print("Urun Fiyati Daha Dusmedi!")

# Start SMTP Server
def send_Email(toMail, url):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login("FROM_EMAİL","PASSWORD")

    subject = 'Beklediginiz Urun Fiyati Dustu'
    content = 'Urun Linki:' + url
    msg = f'Subject: {subject}\n\n{content}'

    server.sendmail (
        "FROM_EMAİL",
        "TO_EMAİL",
        msg
    )

    print("Urun Mesaji Gonderildi")
    server.quit()

# Check Price
priceCheck(url, 200)
