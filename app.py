from src.csv_parser import read_csv_file, normalize_column_names, map_columns_alias

file_path = 'sample_data/transaction.csv'

df = read_csv_file(file_path)
df= normalize_column_names(df)
df = map_columns_alias(df)

print(df)

