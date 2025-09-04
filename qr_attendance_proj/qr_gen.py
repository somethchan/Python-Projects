
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

# [JSON Input]: date
date = input("Enter Date of Attendance as MM/DD/YYYY:").strip()

# [Error Handling]
if validate_date(date):
    prompt_user(f"{date} is the correct date")
else:
    print("Invalid date format. Please use MM/DD/YYYY.")

# [Generate]: Public/Private keys
key_gen()

# [Dataframe Manipulation]: Filtering Columns & Cleaning
df_1 = df_0[['Username', 'Email']]
df_1.columns = ['Username', 'Email'] #Enforce column headers
df_1.loc[:,'Username'] = df_1['Username'].str.lstrip('#').str.strip()
df_1.loc[:,'Email'] = df_1['Email'].str.rstrip('#').str.strip()

print(df_1)

# [Call]: QR generation function
qr_gen(df_1,date)