
import os

# Define paths
dB_path = "D:/ML/Databases/Birds_dB/Images/"
bucket_path = "/electric-birder-71281-bird-db/Birds_dB/Images/"



# Files
f = open('allfiles.csv','w')

with os.scandir(dB_path) as folders:
    for folder in folders:
        img_path = dB_path + "/" + folder.name
        with os.scandir(img_path) as files:
            for file in files:
                line = bucket_path + folder.name + "/" + file.name + "," + folder.name + "\n"
                print(line)
                f.write(line)  # Give your csv text here.
f.close()



print("The End")
