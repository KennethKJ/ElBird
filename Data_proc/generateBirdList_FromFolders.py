import os

GD_path = "D:/Google Drive/"
DB_path = "/ML/Databases/Birds_dB/Images/"

dirs = [item for item in os.listdir(GD_path + DB_path)]

with open(GD_path + '/ML/Databases/Birds_dB/Mappings/full_bird_list.txt', 'w') as f:
    for item in dirs:
        print(item)
        f.write("%s\n" % item)
print("Total classes = " + str(len(dirs)))
