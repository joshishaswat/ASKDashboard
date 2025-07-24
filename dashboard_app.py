import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import oracledb
import os
from dotenv import load_dotenv

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

# Show total number of residents at the top
st.metric(label="Total Residents", value=len(df))

################### LIVING STATUS BAR CHART
# Count the number of each living status
status_counts = df['LIVING_STATUS'].value_counts()

# Plot bar chart
fig1, ax1 = plt.subplots()
ax1.bar(status_counts.index, status_counts.values)
ax1.set_xlabel("Living Status")
ax1.set_ylabel("Number of Residents")
ax1.set_title("Living Status Distribution")

st.subheader("Living Status Distribution")
st.pyplot(fig1)
################### LIVING STATUS BAR CHART

################### GENDER PIE CHART
# Count gender distribution
gender_counts = df['GENDER'].value_counts()

# Plot donut pie chart with percentages only
fig2, ax2 = plt.subplots()
wedges, texts, autotexts = ax2.pie(
    gender_counts,
    labels=gender_counts.index,
    autopct='%1.1f%%',
    startangle=90,
    labeldistance=1.1,
    pctdistance=0.75
)

# Draw center circle for donut effect
centre_circle = plt.Circle((0, 0), 0.55, fc='white')
fig2.gca().add_artist(centre_circle)

# Adjust font sizes
for text in texts:
    text.set_fontsize(10)
for autotext in autotexts:
    autotext.set_fontsize(9)

ax2.set_title("Gender Distribution")
ax2.axis('equal')  # Equal aspect ratio ensures the pie is a circle

st.subheader("Gender Distribution")
st.pyplot(fig2)
################### GENDER PIE CHART

################### ADMISSION YEAR LINE CHART (EVERY OTHER YEAR)
df['ADMISSION_DATE'] = pd.to_datetime(df['ADMISSION_DATE'])

# Count residents admitted per year
admissions_by_year = df['ADMISSION_DATE'].dt.year.value_counts().sort_index()

# Fill in all years (including 0-admission years)
full_year_range = pd.Series(index=range(admissions_by_year.index.min(), admissions_by_year.index.max() + 1), dtype=int)
admissions_filled = full_year_range.fillna(0).add(admissions_by_year, fill_value=0).astype(int)

# Plot line chart
fig3, ax3 = plt.subplots()
ax3.plot(admissions_filled.index, admissions_filled.values, marker='o')
ax3.set_xlabel("Year")
ax3.set_ylabel("Number of Residents Admitted")
ax3.set_title("Yearly Resident Admissions")

# Show every other year
every_other_year = admissions_filled.index[::2]
ax3.set_xticks(every_other_year)
ax3.tick_params(axis='x', rotation=45)

ax3.grid(False)

st.subheader("Admissions by Year")
st.pyplot(fig3)
################### ADMISSION YEAR LINE CHART

################### ETHNICITY BAR CHART
import matplotlib.pyplot as plt
import streamlit as st

# Count ethnicity values
ethnicity_counts = df['ETHNICITY'].value_counts()

# Plot bar chart
fig, ax = plt.subplots()
ax.bar(ethnicity_counts.index, ethnicity_counts.values)

# Label formatting
ax.set_title("Ethnicity Distribution")
ax.set_xlabel("Ethnicity")
ax.set_ylabel("Number of Residents")
plt.xticks(rotation=45, ha='right')

st.subheader("Ethnicity Distribution")
st.pyplot(fig)
################### ETHNICITY BAR CHART

cursor.close()
connection.close()



