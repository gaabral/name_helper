import os
import pandas
import csv


def read_file_into_dict(csv_file):
    name_score_dict = pandas.read_csv(csv_file, header=None, index_col=0, squeeze=True).to_dict()
    return name_score_dict


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def get_all_csvs_from_location(location):
    arr_dicts = []
    for file in os.listdir(location):
        if file.endswith(".csv"):
            file_dict = read_file_into_dict(file)
            arr_dicts.append(file_dict)
    return arr_dicts


def merge_csvs(arr_dicts):
    merged_with_sum = dict()
    header = dict()
    for d in arr_dicts:
        for key, val in d.items():
            if not (is_float(val)):
                header = (key, val)
            elif merged_with_sum.get(key, "def") == "def":
                merged_with_sum.update({key: float(val)})
            else:
                merged_with_sum.update({key: float(merged_with_sum.get(key)) + float(val)})
    return (merged_with_sum, header)


def write_result_to_file(header, result, name):
    with open(name+ ".csv", 'w', newline="") as generated_csv_file:
        writer = csv.writer(generated_csv_file)
        writer.writerow([header[0], header[1]])
        for item in result:
            writer.writerow([item[0], item[1]])


def sort(merged_csv):
    return sorted(merged_csv.items(), key=lambda x: x[1], reverse=True)


def divide_by_gender(full_rank):
    female_list = list()
    male_list = list()
    for item in full_rank:
        if item[0].endswith("a") or item[0].endswith("A"):
            female_list.append(item)
        else:
            male_list.append(item)
    return {"female": female_list, "male": male_list}


def get_top_N(full_rank, n):
    return full_rank[:n]



def write_result_to_file_with_comparison(header, result, name):
    with open(name + ".csv", 'w', newline="") as generated_csv_file:
        writer = csv.writer(generated_csv_file)
        writer.writerow([header[0], header[1], header[2], header[3]])
        for item in result:
            writer.writerow([item[0], item[1]])


location = input("Please specify path, or leave empty for current folder: ")
validated_location = location if location else os.getcwd()
arr_dicts = get_all_csvs_from_location(validated_location)
header = merge_csvs(arr_dicts)[1]
merged_csv = merge_csvs(arr_dicts)[0]
sorted_result = sort(merged_csv)
full_female_rank = divide_by_gender(sorted_result).get("female")
full_male_rank = divide_by_gender(sorted_result).get("male")
top_ten_female = get_top_N(full_female_rank, 10)
top_ten_male = get_top_N(full_male_rank, 10)
write_result_to_file(header, full_female_rank, "full_female_rank")
write_result_to_file(header, full_male_rank, "full_male_rank")
write_result_to_file(header, top_ten_female, "top_ten_female")
write_result_to_file(header, top_ten_male, "top_ten_male")
