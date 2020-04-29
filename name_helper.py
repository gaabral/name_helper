import os
import pandas
import csv


def read_file_into_dict(csv_file):
    name_score_dict = pandas.read_csv(csv_file, header=None, index_col=0, squeeze=True).to_dict()
    return name_score_dict


def get_all_csvs_from_location(location):
    arr_dicts = []
    for file in os.listdir(location):
        if file.endswith(".csv"):
            file_dict = read_file_into_dict(file)
            arr_dicts.append(file_dict)
    return arr_dicts


def merge_csvs(arr_dicts):
    merged_with_sum = dict()
    for d in arr_dicts:
        for key, val in d.items():
            if merged_with_sum.get(key) is None:
                merged_with_sum.update({key: float(val)})
            else:
                merged_with_sum.update({key: float(merged_with_sum.get(key)) + float(val)})
    return merged_with_sum


def write_result_to_file(result, name):
    with open(name + ".csv", 'w', newline="") as generated_csv_file:
        writer = csv.writer(generated_csv_file)
        writer.writerow(["Name", "score"])
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
    return (female_list, male_list)


location = input("Please specify path, or leave empty for current folder: ")
if os.path.exists(location):
    validated_location = location
else:
    print("Provided path does not exist, path: " + location)
    print("Using current folder instead")
    validated_location = os.getcwd()
print("Generating result files.........")
arr_dicts = get_all_csvs_from_location(validated_location)
merged_csv = merge_csvs(arr_dicts)
sorted_result = sort(merged_csv)
(full_female_rank, full_male_rank) = divide_by_gender(sorted_result)
write_result_to_file(full_female_rank, "full_female_rank")
write_result_to_file(full_male_rank, "full_male_rank")
write_result_to_file(full_female_rank[:10], "top_ten_female")
write_result_to_file(full_male_rank[:10], "top_ten_male")
print("Full_rank and top_10 files generated")
