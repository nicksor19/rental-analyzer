from dbfread import DBF
import pandas as pd

#Tell Pandas to display every column when printing a df
pd.set_option("display.max_columns", None)
# Display large numbers normally instead of using scientific notation
pd.set_option("display.float_format", "{:,.2f}".format)


'''
INFO
CODE |DESCRIPTION

 Residential property use codes:
 101  = Single Family Residential
 104  = Two-Family Residential
 105  = Three-Family Residential
 111  = Apartments with Four to Eight Units
 112  = Apartments with More than Eight Units
 1010 = Single Family Residential
 1040 = Two-Family Residential
 1050 = Three-Family Residential
 1110 = Apartments with Four to Eight Units
 1120 = Apartments with More than Eight Units

'''

#main df
file_path = "data/raw/L3_SHP_M271_Shrewsbury/M271Assess_CY26_FY27.dbf"
table = DBF(file_path)
df = pd.DataFrame(iter(table)) #iter (iterate)
################################################
#use_code_df
use_code_table = DBF(
    "data/raw/L3_SHP_M271_Shrewsbury/M271UC_LUT_CY26_FY27.dbf"
)
use_codes_df = pd.DataFrame(iter(use_code_table))
##############################################################


print(df.head()) #top 5 rows

print(df.columns.tolist()) #all col heads
df.info() #inspecting the health of the data

#next we gotta investigate some data to see if it is healthy or not
#Count how many properties have each number of units and sort by unit count
print(df["UNITS"].value_counts().sort_index()) 
#this tells us what properties have units and then how many units exist
#exmaple 2 (2 unit proptery) 18(there 18 2 unit propert)

# Show properties where the UNITS field contains a value greater than 0
print(df[df["UNITS"] > 0][["SITE_ADDR", "USE_CODE", "UNITS", "STYLE"]])

#all of these showed condo main whihc isnt a great way to find true rentals.

#next we will try use code
print(df["USE_CODE"].value_counts().sort_index())

# Show the first 5 rows
print(use_codes_df.head())

# Show the column names
print(use_codes_df.columns.tolist())

#try finding use codes for "family"
print(use_codes_df[use_codes_df["USE_DESC"].str.contains("Family|Apartment", case =False)][["USE_CODE", "USE_DESC"]])


#nowwww we can filter for propeties that are actual rentals
# Use codes that represent residential properties with 2 or more units
multifamily_codes = ["104", "105", "111", "112", "1040", "1050", "1110", "1120"]

# Keep only properties whose use code is in our multifamily code list
multifamily_df = df[df["USE_CODE"].isin(multifamily_codes)]

# Show how many multifamily properties were found
print(len(multifamily_df))


#now that we know use_code is good we are gonna pring out all the usefull info

#Show the first 10 multifamily properties with useful information
print(
    multifamily_df[
        ["SITE_ADDR", "USE_CODE", "TOTAL_VAL", "LS_DATE", "LS_PRICE", "YEAR_BUILT", "BLD_AREA"]
    ].head(10)
)

# Show summary statistics for multifamily sale prices
print(multifamily_df["LS_PRICE"].describe())

# Count the most common sale prices and show the top 15
print(multifamily_df["LS_PRICE"].value_counts().head(15))

# Calculate the assessed value per square foot for each multifamily property
multifamily_df["VALUE_PER_SQFT"] = (
    multifamily_df["TOTAL_VAL"] / multifamily_df["BLD_AREA"]
)

# Show the first 10 properties with the new calculated value
print(
    multifamily_df[
        ["SITE_ADDR", "TOTAL_VAL", "BLD_AREA", "VALUE_PER_SQFT"]
    ].head(10)
)

# Count multifamily properties that have no recorded building area
print("Properties with 0 building area:")
print((multifamily_df["BLD_AREA"] == 0).sum())

# Show summary statistics for assessed value per square foot
print(multifamily_df["VALUE_PER_SQFT"].describe())

# Show the 10 properties with the highest assessed value per square foot
print(
    multifamily_df[
        ["SITE_ADDR", "USE_CODE", "TOTAL_VAL", "BLD_AREA", "VALUE_PER_SQFT"]
    ]
    .sort_values("VALUE_PER_SQFT", ascending=False)
    .head(10)
)


# Show value-per-square-foot statistics for each property use code
print(
    multifamily_df.groupby("USE_CODE")["VALUE_PER_SQFT"].describe()
)

