import src.csv_parser as csvp

file_path = 'sample_data/transaction.csv'

df = csvp.read_csv_file(file_path)

if isinstance(df, str):
    print(df)
    exit()

csvp.normalize_column_names(df)
df, conflicts, manual_mapping_req, unmapped = csvp.map_columns_alias(df)

if manual_mapping_req is False:
    all_mandatory_present, missing = csvp.check_column_mapping(df)
    if all_mandatory_present is True:
        df = df.drop(columns = unmapped)
        print(df)
    else:
        print(f"These mandatory columns {missing} are not mapped, therefore proceed with manual mapping.")
        while True:
            while True:
                user_mapping = csvp.manual_mapping(df, conflicts, user_mapping = None)
                all_mandatory_columns_present, missing_columns = csvp.validate_mandatory_mapping(df, user_mapping)
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
        csvp.apply_manual_mapping(df, user_mapping)
        print(df)
else:
    print(f"Manual mapping is required as these columns {conflicts} were mapped to same the same standaed columns.")
    while True:
                while True:
                    user_mapping = csvp.manual_mapping(df, conflicts, user_mapping = None)
                    all_mandatory_columns_present, missing_columns = csvp.validate_mandatory_mapping(df, user_mapping)
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
    csvp.apply_manual_mapping(df, user_mapping)
    print(df)    

