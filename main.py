import pandas as pd
import os

def generate_snippets_from_xlsx(xlsx_file, output_directory, skip_rows):
    if (output_directory not in os.listdir(".")):
        os.mkdir(output_directory)

    data_frame = pd.read_excel(xlsx_file, engine="openpyxl", skiprows=[i for i in range(skip_rows)])

    first_integer_column = 1

    for column in data_frame.columns:
        if isinstance(column, (int, float)):
            first_integer_column = data_frame.columns.get_loc(column)
            break

    snippet_numbers = data_frame.columns[first_integer_column:]

    for snippet in snippet_numbers:
        snippet_content = f'#4.0# "Q{snippet}" 128 131071 0 0 1\n'

        for _, row in data_frame.iterrows():
            if not row.iloc[0]:
                continue

            mic_num = int(row.iloc[0])
            unmuted = pd.notna(row[snippet])

            mute_state = "ON" if unmuted else "OFF"
            formatted_snippet = str(mic_num).zfill(2)

            snippet_content += f'/ch/{formatted_snippet}/mix/on {mute_state}\n'

        file_name = f"Q{snippet}.snp"
        with open(f"{output_directory}/{file_name}", "w") as file:
            file.write(snippet_content)

        print(f"Snippet '{snippet}' saved as {file_name}")

def locate_xlsx_files():
    return [file for file in os.listdir(".") if file.endswith(".xlsx")]

print("Locating xlsx files...")
xlsx_files = locate_xlsx_files()

print("")
if len(xlsx_files) == 0:
    print("No xlsx files found in the current directory.")
    exit()

if len(xlsx_files) > 1:
    print("Enter the number of the xlsx file you want to use:")

    for i, xlsx_file in enumerate(xlsx_files):
        print(f"{i + 1}. {xlsx_file}")

    user_input = input()
    try:
        user_input = int(user_input)
    except ValueError:
        print("Invalid input.")
        exit()

    if user_input < 1 or user_input > len(xlsx_files):
        print("Invalid input.")
        exit()

    xlsx_file = xlsx_files[user_input - 1]
else:
    xlsx_file = xlsx_files[0]

print("")
print("How many rows should be skipped at the beginning of the xlsx file?")
skip_rows = input()
try:
    skip_rows = int(skip_rows)
except ValueError:
    print("Invalid input.")
    exit()

print("Generating snippets...")
generate_snippets_from_xlsx(xlsx_file, "output", skip_rows)