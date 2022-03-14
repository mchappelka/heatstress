import pandas as pd 
import os
import json

cwd = os.getcwd()

proj_path = cwd[:cwd.rindex("\\")]
data_path = os.path.join(proj_path, "data")
in_path = os.path.join(data_path, "input")
out_path = os.path.join(data_path, "output")
##############################################
#
#         READ IN DATA
#
##############################################

raw_data = pd.read_csv(os.path.join(in_path, "data_200249.csv"))


percap_data= pd.read_csv(os.path.join(in_path, "data_192842.csv"))


##############################################
#
#         CLEAN DATA
#
##############################################
cols_to_drop = ['StateFIPS', 'Data Comment']

raw_data = raw_data.drop(cols_to_drop, axis=1)

percap_data = percap_data.rename(columns={"Value": "Value Per Capita"})
percap_data = percap_data.drop(cols_to_drop, axis=1)

##############################################
#
#         MERGE DATA
#
##############################################

merged_data = pd.merge(left=raw_data,
                        right=percap_data,
                        on=["State", "Year", "Age Group", "Gender"])

# Identify years each state has data for
state_year_df = merged_data[["State", "Year"]].drop_duplicates()
state_df = pd.DataFrame(state_year_df.groupby(['State'])['Year'].apply(list)).reset_index()
state_df = state_df.rename(columns={"Year": "YearsList"})

merged_data_with_years = pd.merge(left=merged_data,
                            right=state_df,
                            on = "State")

##############################################
#
#         Output Data
#
##############################################

merged_data_with_years.to_csv(os.path.join(out_path, "cleaned_data.csv"), index=False)