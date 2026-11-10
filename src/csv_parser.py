import pandas as pd

#This Function reades the csv file and look for errors and reports them.
def read_csv_file(file_path):
   try:
      df = pd.read_csv(file_path)
      if df.empty:
         return "Error: The file is empty."
   except FileNotFoundError:
      return f"Error: The file at {file_path} was not found."
   except pd.errors.ParserError:
      return "Error: The file could not be parsed. Please check the file format."
   except pd.errors.EmptyDataError:
      return "Error: The file is empty."
   
   return df

#Standard columns are used in datdabase and the mandatory columns are requred to process the data further. 
standard_columns = ['date', 'description', 'amount', 'currency', 'transaction_type']
mandatory_columns = ['date', 'description', 'amount']

#The following alias will only be identified for automatic mapping.
column_alias = {
   'date' : ["date", "txn date", "transaction date", "trans date", "date of transaction", "date of txn", "date of trans"],
   'description' : ["description", "desc", "transaction description", "txn description", "trans description", "details", "transaction details", "txn details", "trans details", "narration", "transaction narration", "txn narration", "trans narration", "particulars", "transaction particulars", "txn particulars", "trans particulars", "remarks", "transaction remarks", "txn remarks", "trans remarks", "merchant", "transaction merchant", "txn merchant", "trans merchant", "payee", "transaction payee", "txn payee", "trans payee"],
   'amount' : ["amount", 'amt', "transaction amount", "txn amount", "trans amount", "value"],
   'currency' : ["currency", "curr", "txn currency", "trans currency", "transaction currency", "currency of transaction", "currency of txn", "currency of trans", "ccy"],
   'transaction_type' : ["type", "transaction type", "txn type", "trans type", "type of transaction", "type of txn", "type of trans", "debit/credit", "debit or credit", "debit or credit indicator", "debit/credit indicator", "dr/cr", "dr or cr"],
}

#This function deals with the normalization of column names of dataframe.
def normalize_column_names(df):
   df.columns = df.columns.str.strip().str.lower().str.replace("_", " ")
   return df

#This automatically maps the found alias only if there are no multipe column in dataframe mapped to same standard column.
#If there is a conflict it reports as manual_mapping_req
def map_columns_alias(df):
   mapping = {}
   conflicts = {}
   checked = set()
   manual_mapping_req = False
   
   for key in column_alias.keys():
      for alias in column_alias[key]:
         for col in df.columns:
            if col == alias:
               mapping[col] = key

   unmapped = [col for col in df.columns if col not in mapping]
   
   for values in mapping.values():
      if list(mapping.values()).count(values) > 1 and values not in checked:
         manual_mapping_req = True
         checked.add(values)
         conflicts[values] = [k for k, v in mapping.items() if v == values]
   
   if not manual_mapping_req:
      df = df.rename(columns=mapping)   
   
   return df, conflicts, manual_mapping_req, unmapped

#This function validates the mapping for mandatory columns, if there is no conflict.
def check_column_mapping(df):
   missing = [col for col in mandatory_columns if col not in df.columns]
   all_mandatory_present = not missing
   return all_mandatory_present, missing

#This function let the user map the columns manually and ask for revision if user wants to.
def manual_mapping(df, conflicts, user_mapping = None):   
   if user_mapping is None:
      user_mapping = {}
      
      if conflicts:
         columns_to_map = list(df.columns)
         choices = standard_columns.copy()
         choices.append("ignore")

      else:
         columns_to_map = [col for col in df.columns if col not in standard_columns]
         choices = [choice for choice in standard_columns if choice not in df.columns]
         choices.append("ignore")
      
      for col in columns_to_map:
         print(f"Chose an option(1-{len(choices)}) form the following to map {col} column with SpendWise's standard columns: ")
         for index, options in enumerate(choices, start = 1):
            print(f"{index}. {options}")
         while True:
            try:
               choice = int(input("choice: "))
               if not (1 <= choice <= len(choices)):
                  print(f"Eneter a valid choice")
               else:
                  break
            except ValueError:
               print("Enter a valid choice.")
            
         user_mapping[col] = choices[choice-1]

         if choices[choice-1] != "ignore":
            del choices[choice-1] 
      return user_mapping

   else:
      ignored_cloumns = [col for col in user_mapping if user_mapping[col] == "ignore"]
      columns_to_map = [
         col for col in df.columns if (col not in user_mapping) and (col not in standard_columns)
      ]
      columns_to_map.extend(ignored_cloumns)
      choices = [
         choice for choice in standard_columns if (choice not in user_mapping.values()) and (choice not in df.columns)
      ]
      choices.append("ignore")
      
      for col in columns_to_map:
         print(f"Chose an option(1-{len(choices)}) form the following to map {col} column with SpendWise's standard columns: ")
         for index, options in enumerate(choices, start = 1):
            print(f"{index}. {options}")
         while True:
            try:
               choice = int(input("choice: "))
               if not (1 <= choice <= len(choices)):
                  print(f"Eneter a valid choice")
               else:
                  break
            except ValueError:
               print("Enter a valid choice.")
                  
         user_mapping[col] = choices[choice-1]
      
         if choices[choice-1] != "ignore":
            del choices[choice-1] 
      return user_mapping

#This validates if all the mandatory columns are mapped or not an if not then reports the missing_columns.
def validate_mandatory_mapping(df, user_mapping):
   missing_columns = [
      col for col in mandatory_columns if (col not in user_mapping.values()) and(col not in df.columns)
   ]
   all_mandatory_columns_present = not missing_columns
   return all_mandatory_columns_present, missing_columns

#After validation of the manual mapping this function applies it to the dataframe.
def apply_manual_mapping(df, user_mapping):
   ignored_columns = [col for col in user_mapping if user_mapping[col] == "ignore"]
   rename_mapping = {
      col: standard_col
      for col, standard_col in user_mapping.items()
      if standard_col != "ignore"
   }
   df = df.drop(columns = ignored_columns)
   df = df.rename(columns = rename_mapping)
   return df

def implement_csv_parser(file_path):
   df = read_csv_file(file_path)
   if isinstance(df, str):
      return df
   normalize_column_names(df)
   df, conflicts, manual_mapping_req, unmapped = map_columns_alias(df)

   if not manual_mapping_req:
      all_mandatory_present, missing = check_column_mapping(df)
      if all_mandatory_present:
         df = df.drop(columns = unmapped)
         return df
      else:
         print(f"These mandatory columns {missing} are not mapped, therefore proceed with manual mapping.")
         while True:
            while True:
               user_mapping = manual_mapping(df, conflicts, user_mapping = None)
               all_mandatory_columns_present, missing_columns = validate_mandatory_mapping(df, user_mapping)
               if all_mandatory_columns_present:
                  break
               else:
                  print(f"These mandatory columns {missing_columns} are not mapped, please revise the mapping!")
            print("Current Mapping: ")
            for key, value in user_mapping.items():
               print(f"{key}: {value}")
            while True:
               want_to_revise = input("Do you want to revise the mapping(y/n)?").lower()
               if want_to_revise in {"y", "n"}:
                  break
               else:
                  print("Enter a valid option.")
                  continue
            if want_to_revise == "y":
               continue
            else:
               break
         df = apply_manual_mapping(df, user_mapping)
         return df
   else:
      print(f"Manual mapping is required as these columns {conflicts} were mapped to same the same standaed columns.")
      while True:
         while True:
            user_mapping = manual_mapping(df, conflicts, user_mapping = None)
            all_mandatory_columns_present, missing_columns = validate_mandatory_mapping(df, user_mapping)
            if all_mandatory_columns_present:
                break
            else:
               print(f"These mandatory columns {missing_columns} are not mapped, please revise the mapping!")
         print("Current Mapping: ")
         for key, value in user_mapping.items():
            print(f"{key}: {value}")
         while True:
            want_to_revise = input("Do you want to revise the mapping(y/n)?").lower()
            if want_to_revise in {"y", "n"}:
               break
            else:
               print("Enter a valid option.")
               continue
         if want_to_revise == "y":
            continue
         else:
            break
      df = apply_manual_mapping(df, user_mapping)
      return df
