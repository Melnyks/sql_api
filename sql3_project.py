# รายชื่อสมาชิก
# 1.จิรวัฒน์ พึ่งวงศ์ตระกูล  6510615047
# 2.ปรุฬห์  เงาเฉลิมพงศ์  6510615195 


import requests
import sqlite3

# Make a GET request to the API endpoint
response = requests.get('https://api.coincap.io/v2/assets')

data = response.json()

list_data=[]

con = sqlite3.connect("crypto_price.db")
cur=con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS crypto(id PRIMARY KEY,symbol, priceUsd FLOAT, changePercent24Hr FLOAT, marketCapUsd FLOAT)")

for x in data['data']:
    listing = [x['id'],x['symbol'],x['priceUsd'],x['changePercent24Hr'],x['marketCapUsd']]
    list_data.append(listing)

cur.executemany("INSERT OR IGNORE INTO crypto VALUES(?, ?, ?, ?, ?)", list_data)

# แสดงราคาเหรียญคริปโตที่สูงที่สุด 5 อันดับแรก
cur.execute("SELECT symbol,priceUsd FROM crypto ORDER BY priceUsd DESC LIMIT 5")
con.commit()

print("แสดงราคาเหรียญคริปโตที่สูงที่สุด 5 อันดับแรก")
for row in cur:
    symbol,priceUsd=row
    print(f" symbol : {symbol}, priceUsd : {priceUsd:.3f} USD")

# แสดงค่าเฉลี่ยการเปลี่ยนแปลงราคาของเหรียญคริปโต
cur.execute("SELECT AVG(changePercent24Hr) FROM crypto")
con.commit()

print("\nแสดงค่าเฉลี่ยการเปลี่ยนแปลงราคาของเหรียญคริปโต")

for row in cur:
    changePercent24Hr = row[0]  
    print(f"priceChange : {changePercent24Hr} %")

# แสดงมูลค่าทางตลาดที่น้อยที่สุด 5 อันดับ
cur.execute("SELECT symbol,marketCapUsd FROM crypto ORDER BY marketCapUsd LIMIT 5")
con.commit()

print("\nแสดงมูลค่าทางตลาดที่น้อยที่สุด 5 อันดับ")
for row in cur:
    symbol,marketCapUsd=row
    print(f" symbol : {symbol} , marketCap : {marketCapUsd:.3f} USD")

con.close()