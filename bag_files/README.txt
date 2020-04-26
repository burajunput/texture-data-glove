1) Record data from all topics with:
rosbag record --duration=10 /accelX /accelY /accelZ

2) Rename the bag file to appropriate texture

3) Use the bag to csv to convert to csv files seperately:
python bag_to_csv.py [bag name].bag