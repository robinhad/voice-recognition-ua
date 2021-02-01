import os
from random import shuffle
from shutil import copyfile

# file template needed for import script
template = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}"
# structure example below
# client_id	path	sentence	up_votes	down_votes	age	gender	accent	locale	segment
structure = template.format("client_id", "path", "sentence", "up_votes",
                            "down_votes", "age", "gender", "accent", "locale", "segment")

iterator = 1
speaker_iterator = 1


def write_dataset(path, name, data):
    """
    Function to write converted data list
    """
    global iterator
    global speaker_iterator
    file_path = os.path.join(path, name)
    clip_path = os.path.join(os.path.dirname(path), "wav")
    result = open(file_path, mode="w", encoding="utf-8")
    result.write(structure)
    result.write("\n")
    for row in data:
        file_name = row[0]
        if file_name.endswith(".wav"):
            pass
        elif file_name.endswith(".mp3"):
            pass
        elif file_name.find(".") == -1:
            file_name += ".wav"
        parted_name = file_name.split(".")

        new_file_name = f"{iterator}." + parted_name[1]

        old_file_path = os.path.join(clip_path, file_name)
        new_file_path = os.path.join("clips", new_file_name)
        if os.path.exists(old_file_path):
            copyfile(old_file_path,
                     new_file_path)
            result.write(template.format(
                speaker_iterator, new_file_name, row[1], "", "", "", "", "", "uk", "\n"))
            speaker_iterator += 1
            iterator += 1
        else:
            print("File not found", old_file_path)
    result.close()


if not os.path.exists("clips"):
    os.makedirs("clips")  # create folder to contain processed clips

# iterate over all data lists and write converted version near them
for subdir, dirs, files in os.walk(os.path.abspath(os.path.curdir)):
    print(subdir)
    for file in files:
        if file == "txt.final.data":
            file_path = os.path.join(subdir, file)
            file = open(file_path, mode="r")
            data = [row.replace(" \n", "").split(" ", 1)
                    for row in file.readlines()]
            file.close()

            shuffle(data)

            dataset_size = len(data)
            train_point = int(dataset_size*0.8)
            dev_point = int(train_point + (dataset_size - train_point) / 2)
            # split dataset
            write_dataset(subdir, "train.tsv", data[:train_point])
            write_dataset(subdir, "dev.tsv", data[train_point:dev_point])
            write_dataset(subdir, "test.tsv", data[dev_point:])

# write dataset splits into single files
final_files = {
    "train.tsv": open("train.tsv", mode="w", encoding="utf-8"),
    "dev.tsv": open("dev.tsv", mode="w", encoding="utf-8"),
    "test.tsv": open("test.tsv", mode="w", encoding="utf-8")
}
for file in final_files.values():
    file.write(structure)
    file.write("\n")

for subdir, dirs, files in os.walk(os.path.curdir):
    for file in files:
        if file in ["train.tsv", "dev.tsv", "test.tsv"]:
            input_file = open(os.path.join(subdir, file))
            data = [row for row in input_file.readlines()][1::]
            input_file.close()
            for row in data:
                final_files[file].write(row)

for file in final_files.values():
    file.close()
