# [Import Statements]: Libraries & Functions
import os
import pandas as pd

from datetime import date
from functions import qr_gen
from functions import prompt_user
from functions import send
from functions import key_gen
from functions import validate_date

# [User Input]: file_path
file_path = input("Enter File Path for Roster (.csv format): ").strip()

# [Input Validation]: file_path
if not os.path.isfile(file_path):
    print("Error: File does not exist.")
    exit()
if not file_path.endswith('.csv'):
    print("Error: File is not a .csv file.")
    exit()

# [Error Handling]
try:
    df_0 = pd.read_csv(file_path)
    prompt_user(f"{file_path} is the correct file path")
except FileNotFoundError:
    print("Error: File Does not Exist.")
except Exception as e:
    print(f"An error occured: {e}")

# [User Input]: date
date = input("Enter Date of Attendance as MM/DD/YYYY:").strip()

# [Error Handling]
if validate_date(date):
    prompt_user(f"{date} is the correct date")
else:
    print("Invalid date format. Please use MM/DD/YYYY.")

# [Generate]: Public/Private keys
prompt_user("Proceed with generating new encryption keys")
key_gen()

# [Dataframe Manipulation]: Filtering Columns & Cleaning
df_1 = df_0[['Username', 'Email']]
df_1.columns = ['Username', 'Email'] #Enforce column headers
df_1.loc[:,'Username'] = df_1['Username'].str.lstrip('#').str.strip()
df_1.loc[:,'Email'] = df_1['Email'].str.rstrip('#').str.strip()

print(df_1)

# [Call]: QR generation function
qr_gen(df_1,date)

# [Call]: Prompt user to continue
prompt_user("Proceed with mass mailing")

# [Configuration]: SMTP Server and sender mail configurations
smtp_server ='SMTP SERVER HERE.'
smtp_port = 25
sender_email = 'attendance.noreply@cit.lcl'
department = 'Computer and Information Technology'
course = 'CNIT34500'
current_directory = os.getcwd()

for index, row in df_1.iterrows():
    student_email = row['Email']
    path = os.path.join(current_directory, 'qr_png', f"{row['Username']}.png")

    # [Call]: Send email to each user
    send(
        smtp_server, smtp_port, sender_email, student_email,

        # [Configuration]: E-mail subject/body
        subject=f"{course} Attendance QR code",
        body= f"""Dear, {row['Username']},

        Please find your unique QR code below to mark your attendance.
        Date: {date}
        Course: {course}

        Please scan the attached QR code during lecture to receive attendance credit

        {department}
        """,
        fpath=path
    )
    print(f"QR codes have been sent to {row['Username']}")

