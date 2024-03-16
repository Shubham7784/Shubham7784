import requests as rs
import pandas as pd
from bs4 import BeautifulSoup


def page(key):
  payload = {
      "api_key":
      key,
      "url":
      "https://www.amazon.in/s?hidden-keywords=B0C7QS9M38+%7C+B08TV2P1N8+%7C+B09N3ZNHTY+%7C+B07PR1CL3S+%7C+B0BSGQTVP1+%7C+B0BKG5PQ6T+%7C+B0CC8VF47L+%7C+B09YRYCWF8+%7C+B0BW8TXJJ2+%7C+B0BW9NWMPL+%7C+B08JQN8DGZ+%7C+B0BZ4DJ7GZ+%7C+B071Z8M4KX+%7C+B0BKZFKQ3G+%7C+B0BVRDWC9C+%7C+B09LHXTXMX+%7C+B0BYZ26QGB+%7C+B09NYK3CF2+%7C+B0CC5VH2LW+%7C+B09MTRDQB5+%7C+B0BBTYDK6Y+%7C+B0C7CNFKJ3+%7C+B08MSYDMZ7+%7C+B08JMC1988+%7C+B09GFRV7L5+%7C+B09X74RB6D+%7C+B0BTDNZQWJ+%7C+B072PQRS12+%7C+B0856HNMR7+%7C+B07KXR889N+%7C+B01FSYQ2A4+%7C+B08CVTJ7NJ+%7C+B07T2CZCMR+%7C+B0B4NW64R1+%7C+B07NBWT3Z2+%7C+B08H9Z3XQW+%7C+B0BBVBCL3F+%7C+B07SMH67DJ+%7C+B0C7QWGZ6Z+%7C+B01J82IYLW+%7C+B08JM7X6RY+%7C+B0B12Q8K2X+%7C+B0BR5CMNNT+%7C+B0BBTYBLJV+%7C+B01MF8MB65+%7C+B08CVTT65T+%7C+B09JGRDGDG+%7C+B0BTDRVFW1+%7C+B0BZHRB9J1+%7C+B0C592CYFJ&_encoding=UTF8&content-id=amzn1.sym.9c8f8322-71f0-487d-87cc-e704eb7c4ec9&pd_rd_r=18596fdd-3a54-4604-a173-160a5c267531&pd_rd_w=HMra8&pd_rd_wg=zmNbv&pf_rd_p=9c8f8322-71f0-487d-87cc-e704eb7c4ec9&pf_rd_r=153MVDTKX7V889NAGN0Q&ref=pd_gw_unk"
  }
  url = "http://api.scraperapi.com"
  con = rs.get(url, params=payload)
  soup = BeautifulSoup(con.content, "html.parser")
  soup.prettify()
  return soup


api_key = input("Enter your api key : ")
soup = page(api_key)
con = soup.find_all("div", class_="a-section a-spacing-base")
name = []
price = []
link = []
for items in con:
  pro_name = items.find(
      "span", class_="a-size-base-plus a-color-base a-text-normal").get_text()
  name.append(pro_name)
  pro_price = items.find("span", class_="a-offscreen").get_text()
  price.append(pro_price)
  pro_link = items.find_all(
      "a",
      class_=
      "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal",
      href=True)
  for l in pro_link:
    link.append(l["href"])

data = {"Product Name ": name, "Product Price": price, "Product Link": link}
df = pd.DataFrame(data=data)
df.to_csv("Earphone_Amazon.csv", index=False)
print("Process Complete !!")
