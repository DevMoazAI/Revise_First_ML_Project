import pandas as pd

# load all data set
pro_df =pd.read_csv('Production Schedule.csv')
qua_df = pd.read_csv('Quality.csv')
mac_df = pd.read_csv('Machines.csv')
emp_df = pd.read_csv('Employees.csv')

# print all dataset table
# print("Production dataset \n", pro_df.head())
# print("Quality dataset \n",qua_df.head())
# print("Machine dataset \n",mac_df.head())
# print("Empolye dataset \n",emp_df.head())


# e_df.info()
# check all data set data types
# print("Production dataset \n",pro_df.info())
# print("Quality dataset \n",qua_df.info())
# print("Machine dataset \n",mac_df.info())
# print("Empolye dataset \n",emp_df.info())

# print("Missing values in Employee Data:\n", emp_df.isnull().sum())
# print("\nMissing values in Machine Data:\n", mac_df.isnull().sum())
# print("\nMissing values in Production Data:\n", pro_df.isnull().sum())
# print("\nMissing values in Quality Data:\n", qua_df.isnull().sum())

# dateformat change both  Production and Quality dataset.
pro_df['Date'] = pd.to_datetime(pro_df['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
qua_df['Date'] = pd.to_datetime(qua_df['Date'], errors='coerce').dt.strftime('%Y-%m-%d')

merge_pq = pd.merge(pro_df, qua_df, on=['Date', 'Shift'], how='left' )

## Save the merged DataFrame to a CSV file
# merge_pq.to_csv('merged_data_production_Quality.csv', index=False)

# print(merge_pq.head())
# print(merge_pq.info())

# change the date format of machine dataset
mac_df['Date']= pd.to_datetime(mac_df['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
# print(mac_df['Date'])

# Rename columns of empolyee dataset
emp_df.rename(columns={'EmployeeID': 'Employee', 'Experience (Years)': 'Experience'}, inplace=True)
# emp_df.columns

emp = emp_df
# emp.columns
# print(emp.columns)

# Summary statistics for numeric fields
# print("Employee Data Summary:\n", emp.describe().T)
# print("\nMachine Data Summary:\n", mac_df.describe().T)
# print("\nProduction Data Summary:\n", pro_df.describe().T)
# print("\nQuality Data Summary:\n", qua_df.describe().T)


# List of DataFrames to check for duplicates
# dataframes = [emp, pro_df, mac_df, qua_df]

# Loop through each DataFrame and check for duplicates
# for df in dataframes:
#     print(f'Duplicates in {df}: {df.duplicated().sum()}')


# Function to calculate required statistics for each row in merged_pq
def calculate_employee_stats(employee_ids_str):
    # Split and strip each employee ID to ensure no extra spaces
    employee_ids = [emp_id.strip() for emp_id in employee_ids_str.split(',')]

    # Filter employees who are in the current EmployeeIDs list
    relevant_employees = emp[emp['Employee'].isin(employee_ids)]

    # Calculate the required statistics
    avg_age = relevant_employees['Age'].mean()
    avg_experience = relevant_employees['Experience'].mean()
    num_of_highschool = sum(relevant_employees['Education'] == 'High School')
    num_of_masters = sum(relevant_employees['Education'] == "Master's Degree")
    num_of_diploma = sum(relevant_employees['Education'] == 'Diploma')
    num_of_bachelors = sum(relevant_employees['Education'] == "Bachelor's Degree")

    return pd.Series([avg_age, avg_experience, num_of_highschool, 
                      num_of_masters, num_of_diploma, num_of_bachelors])


# merge_pq = pd.merge()

# Apply the function to each row in merged_pq
merge_pq[['average_age', 'average_experience', 'num_high_school', 'num_masters',
          'num_diploma', 'num_bachelors']] = merge_pq['EmployeeIDs'].apply(calculate_employee_stats)
# print(merge_pq)
# Ensure average_age and average_experience are rounded to 2 decimal places and convert to float
merge_pq['average_age'] = merge_pq['average_age'].round(2).astype(float)
merge_pq['average_experience'] = merge_pq['average_experience'].round(2).astype(float)

# Convert education count columns to integer type explicitly to remove decimals
merge_pq['num_high_school'] = merge_pq['num_high_school'].astype(int)
merge_pq['num_masters'] = merge_pq['num_masters'].astype(int)
merge_pq['num_diploma'] = merge_pq['num_diploma'].astype(int)
merge_pq['num_bachelors'] = merge_pq['num_bachelors'].astype(int)

# updated DataFrame with only relevant columns
merge_pq[['Date', 'Shift', 'GarmentType', 'TargetUnits', 'EmployeeIDs', 'DefectsCount',
                 'average_age', 'average_experience', 'num_high_school', 'num_masters', 'num_diploma', 'num_bachelors']]
# print(merge_pq.head(10))

# merge_pq.to_csv('merged_data_1.csv', index=False)

# Filter assigned machines
assigned_machines_df = mac_df[mac_df['Assigned (Yes/No)'] == 'Yes']

# Filter unassigned machines
unassigned_machines_df = mac_df[mac_df['Assigned (Yes/No)'] == 'No']

# Merge the assigned and unassigned machines into one DataFrame
merged_df = pd.concat([assigned_machines_df, unassigned_machines_df])

# print(merged_df)

# Group by Date, Shift, and Make, then count the number of each machine type
mac_counts = merged_df.groupby(['Date', 'Shift', 'Make']).size().unstack(fill_value=0)
# print(mac_counts)

# Rename columns for clarity
mac_counts.columns = ['num_of_Brother', 'num_of_Juki', 'num_of_Singer']
# print(mac_counts)
mac_counts.to_csv('machine_counts.csv')

# # Merge the machine counts back into merge_pq based on Date and Shift
merge_pqm = pd.merge(merge_pq, mac_counts, on=['Date', 'Shift'], how='left')

merge_pqm = merge_pqm[['Date', 'Shift', 'GarmentType', 'TargetUnits', 'EmployeeIDs', 'DefectsCount',
                                   'average_age', 'average_experience','num_high_school', 
                                   'num_masters', 'num_diploma', 'num_bachelors','num_of_Brother', 
                                   'num_of_Juki', 'num_of_Singer']]
# Apply one-hot encoding to 'Shift' and 'GarmentType'
merge_pqm = pd.get_dummies(merge_pqm, columns=['Shift', 'GarmentType'], dtype='int64')

# Display the transformed dataframe
# print(final_merge_df.head())

# Get total number of columns
# total_columns = merge_pqm.shape[1]

# # Display columns in groups of 5
# for i in range(0, total_columns, 7):  # Step size of 5
#     print(merge_pqm.iloc[:, i:i+7].head())  # Select columns from i to i+5
#     print("\n--- Next 7 Columns ---\n")

# print(merge_pqm.dtypes)

# Save the marging dataset of production quality and machine and make csv file
# merge_pqm.to_csv('marge_pq_mac_counts.csv', index=False)

# Display the updated DataFrame with machine counts
# print(merge_pqm.head(10))

total_columns = merge_pqm.shape[1]
# Display columns in groups of 5
for i in range(0, total_columns, 7):  # Step size of 5
    print(merge_pqm.iloc[:, i:i+7].head())  # Select columns from i to i+5
    print("\n--- Next 7 Columns ---\n")

print(merge_pqm.info())

# its marge the merged_data_production_Quality plus Machines 
# merge_df2 = pd.merge(merge_df, mac_df, on=['Date', 'Shift'], how='left' )

## Save the merged DataFrame to a CSV file
# merge_df2.to_csv('merged_data_production_Quality_Machines.csv', index=False)

# print(merge_df2.head())

# print(merge_df2.info())










