import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import oracledb
import os
from dotenv import load_dotenv

# Connect using just the username, password, and service name
# connection = oracledb.connect(
#     user="ADMIN",
#     password="Askfoundation1",
#     dsn="askfoundation_high",
#     config_dir="/Users/shaswatjoshi/Desktop/ASK Foundation/dashboard/Wallet_askfoundation",  # <- full path to Wallet folder
#     wallet_location="/Users/shaswatjoshi/Desktop/ASK Foundation/dashboard/Wallet_askfoundation",
#     wallet_password="Askfoundation1"  # password you set when downloading wallet
# )

# Load environment variables
load_dotenv()

connection = oracledb.connect(
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    dsn=os.getenv("DB_DSN"),
    config_dir=os.getenv("WALLET_PATH"),
    wallet_location=os.getenv("WALLET_PATH"),
    wallet_password=os.getenv("WALLET_PASSWORD")
)

st.title("Aged Care Home Data Model")

cursor = connection.cursor()
cursor.execute("SELECT * FROM RESIDENT")
rows = cursor.fetchall()

# Load into pandas DataFrame for easy viewing
df = pd.DataFrame(rows, columns=[col[0] for col in cursor.description])
print(df)

################### DATA CHARTS
# Count the number of each living status
status_counts = df['LIVING_STATUS'].value_counts()

# Plot pie chart
fig, ax = plt.subplots()
ax.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio to make the pie circular

st.subheader("Living Status Distribution")
st.pyplot(fig)
################### DATA CHARTS

cursor.close()
connection.close()



