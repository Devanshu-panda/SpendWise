import pandas as pd

def read_csv_file(file_path):
   try:
      df = pd.read_csv(file_path)
   except FileNotFoundError:
      return f"Error: The file at {file_path} was not found."
   except pd.errors.ParserError:
      return "Error: The file could not be parsed. Please check the file format."
   except pd.errors.EmptyDataError:
      return "Error: The file is empty."
   
   return df

column_alias = {
   'date' : ["date", "txn date", "transaction date", "trans date", "date of transaction", "date of txn", "date of trans"],
   'description' : ["description", "desc", "transaction description", "txn description", "trans description", "details", "transaction details", "txn details", "trans details", "narration", "transaction narration", "txn narration", "trans narration", "particulars", "transaction particulars", "txn particulars", "trans particulars", "remarks", "transaction remarks", "txn remarks", "trans remarks", "merchant", "transaction merchant", "txn merchant", "trans merchant", "payee", "transaction payee", "txn payee", "trans payee"],
   'amount' : ["amount", 'amt', "transaction amount", "txn amount", "trans amount"],
   'currency' : ["currency", "curr", "txn currency", "trans currency", "transaction currency", "currency of transaction", "currency of txn", "currency of trans", "ccy"],
   'transaction_type' : ["transaction type", "txn type", "trans type", "type of transaction", "type of txn", "type of trans", "debit/credit", "debit or credit", "debit or credit indicator", "debit/credit indicator", "dr/cr", "dr or cr"],
}

def normalize_column_names(df):
   df.columns = df.columns.str.strip().str.lower().str.replace("_", " ")
   return df

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

   unmapped = [col for col in df if col not in mapping]
   
   for values in mapping.values():
      if list(mapping.values()).count(values) > 1 and values not in checked:
         manual_mapping_req = True
         checked.add(values)
         conflicts[values] = [k for k, v in mapping.items() if v == values]
   
   if not manual_mapping_req:
      df.rename(columns=mapping, inplace=True)   
   
   return df, conflicts, manual_mapping_req, unmapped




   