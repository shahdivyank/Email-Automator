import gspread
from oauth2client.service_account import ServiceAccountCredentials
import smtplib
from email.message import EmailMessage

text = open("message.txt", "r")
subs = dict()
email = ""

for line in text:
    email += line
    split_line = line.rsplit()
    for element in split_line:
        if "__" in element:
            subs.update({element: "0"})
text.close()

for item in subs:
    while True:
        msg = "Would you like this element" + item + "to be constant or variable? Enter 0 for constant and 1 for variable:\t"
        try:
            var = int(input(msg))
            if var == 0:
                con = str("Enter the constant value for" + item + ":\t")
                val = input(con)
                subs.update({item: str(val)})
                break
            elif var == 1:
                subs.update({item: str(var)})
                break
            else:
                print("Invalid Input, please try again")
        except:
            print("Please enter integer values only!")

keys = []
for key in subs:
    if subs[key] != "1":
        email = email.replace(key, str(subs[key]))
        keys.append(key)

for key in keys:
    if key in subs:
        subs.pop(key)

sender_email = input("Enter Email:\t")
password = input("Enter Password:\t")

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender_email, password)
print("Login Successful")

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("CRA Forms").sheet1
data = sheet.get_all_records()

msg = EmailMessage()
msg["From"] = sender_email

i = 2
for row in data:
    if row["Email Sent?"] == "":
        for key in subs:
            email = email.replace(subs[key], row[key])

        msg["Subject"] = row["__program__"] + "Confirmation"
        msg["To"] = row["__email__"]
        msg.set_content(email)
        print(email)
        server.send_message(msg)
        sheet.update_cell(i, 11, "Sent")
        del msg["Subject"]
        del msg["To"]
        i += 1
server.quit()