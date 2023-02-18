# %%
import pandas as pd
import psycopg2 as pg

# Read data from files
df = pd.read_csv("../Parser/Results.csv")
# Delete the creationdate column as we have no use
del df["CreationDate"]

# Connect to postgres database
conn = pg.connect(database="NAaaS", user="postgres",
                  password="1234", host="127.0.0.1", port="8008")
cursor = conn.cursor()

# For each row in the dataframe, insert into database
for data in df.itertuples():

    # Check if focus location is a province, then insert with district, tehsil, union council as NULL
    cursor.execute("Select name from province where name=%s",
                   (str(data[7]).upper(),))
    province = cursor.fetchone()

    if province:
        cursor.execute("Insert into NEWS(header, summary, details, focus_time, focus_location, link, category, province) VALUES( %s, %s, %s, %s, %s, %s, %s, %s);",
                       (data[2], data[3], data[4], data[1], province[0], data[5], data[6],  province[0]))
    # Else, Check if focus location is a district, then insert with tehsil, union council as NULL
    else:
        cursor.execute(
            "Select name, province from district where name=%s", (str(data[7]).upper(),))
        district = cursor.fetchone()
        if district:
            cursor.execute("Insert into NEWS(header, summary, details, focus_time, focus_location, link, category, province, district) VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                           (data[2], data[3], data[4], data[1], district[0], data[5], data[6],  district[1], district[0]))
    # Else, Check if focus location is a tehsil, then insert with union council as NULL
        else:
            cursor.execute(
                "Select name, district from tehsil where name=%s", (str(data[7]).upper(),))
            tehsil = cursor.fetchone()
            if tehsil:
                cursor.execute(
                    "Select name, province from district where name=%s", (tehsil[1],))
                district = cursor.fetchone()
                if district:
                    cursor.execute("Insert into NEWS(header, summary, details, focus_time, focus_location, link, category, province, district, tehsil) VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                                   (data[2], data[3], data[4], data[1], tehsil[0], data[5], data[6],  district[1], district[0], tehsil[0]))


# %%
# Commit to database
conn.commit()


