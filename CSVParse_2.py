import pandas as pd
import re


def IsNaN(string):
    return string != string


df_movie = pd.read_csv("files/data/movies_metadata_needed_columns.csv", sep=";", engine="python", encoding="utf_8_sig")

print("File opened")

belongs_to_collection_list = []
original_title_list = []
overview_list = []
production_companies_list = []
vote_average_list = []
cast_list = []
crew_list = []

counter = 0

for index, row in enumerate(df_movie.values):
    # belongs_to_collection
    belongs_to_collection = row[0]
    if IsNaN(belongs_to_collection):
        belongs_to_collection = f"row {counter}"
        belongs_to_collection_list.append(belongs_to_collection)
    elif belongs_to_collection == "[]":
        belongs_to_collection_list.append(f"row {counter}")
    else:
        ids = re.findall(r"'name': '\w+'", belongs_to_collection)

        first = True
        text = ""
        for el in ids:
            if first:
                text = "".join([text, el[9:-1]])
                first = False
            else:
                text = "".join([text, ", ", el[9:-1]])

        if text:
            belongs_to_collection_list.append(text)
        else:
            belongs_to_collection_list.append(belongs_to_collection)

    # original_title
    original_title = row[2]
    if IsNaN(original_title):
        original_title = f"row {counter}"
    elif original_title == "[]":
        original_title_list.append(f"row {counter}")


    original_title_list.append(original_title)

    # overview
    overview = row[3]
    if IsNaN(overview):
        overview = f"row {counter}"
    elif overview == "[]":
        overview_list.append(f"row {counter}")

    overview_list.append(overview)

    # production_companies
    production_companies = row[4]
    if IsNaN(production_companies):
        production_companies = f"row {counter}"
        production_companies_list.append(production_companies)
    elif production_companies == "[]":
        production_companies_list.append(f"row {counter}")
    else:
        ids = re.findall(r"'name': '[^}]+',", production_companies)

        first = True
        text = ""
        for el in ids:
            if first:
                text = "".join([text, el[9:-2]])
                first = False
            else:
                text = "".join([text, ", ", el[9:-1]])

        if text:
            production_companies_list.append(text)
        else:
            production_companies_list.append(production_companies)

    # vote_average
    vote_average = row[7]
    if IsNaN(vote_average):
        vote_average = f"row {counter}"
    elif vote_average == "[]":
        vote_average_list.append(f"row {counter}")

    vote_average_list.append(vote_average)

    # cast
    cast = row[9]
    if IsNaN(cast):
        cast = f"row {counter}"
        cast_list.append(cast)
    elif cast == "[]":
        cast_list.append(f"row {counter}")
    else:
        ids = re.findall(r"'name': '[\w\s\..]+'", cast)

        first = True
        text = ""
        for el in ids:
            if first:
                text = "".join([text, el[9:-1]])
                first = False
            else:
                text = "".join([text, ", ", el[9:-1]])

        if text:
            cast_list.append(text)
        else:
            cast_list.append(cast)

    # crew
    crew = row[10]
    if IsNaN(crew):
        crew = f"row {counter}"
        crew_list.append(crew)
    elif crew == "[]":
        crew_list.append(f"row {counter}")
    else:

        ids = re.findall(r"'name': '[\w\s\..]+'", crew)

        first = True
        text = ""
        for el in ids:
            if first:
                text = "".join([text, el[9:-1]])
                first = False
            else:
                text = "".join([text, ", ", el[9:-1]])

        if text:
            crew_list.append(text)
        else:
            crew_list.append(crew)

    counter += 1

    if index % 10000 == 0:
        print(index / 10000)

dictionary = {
    "belongs_to_collection": belongs_to_collection_list,
    "original_title": original_title_list,
    "overview": overview_list,
    "production_companies": production_companies_list,
    "cast": cast_list,
    "crew": crew_list,
    "vote_average": vote_average_list,
}

new_df = pd.DataFrame(dictionary)
# noinspection PyTypeChecker
new_df.to_csv(r"files/data/movies_metadata_prepared.csv", sep=";", index=False, encoding="utf_8_sig")
