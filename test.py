import numpy as np
import pandas as pd
import pandas as pd
data = pd.read_csv("AIS_2019_01_01_inverted.csv",names=["MMSI", "TimeDate", "LAT","LON", "SOG","COG","Heading","Name","IMO","CallSign","VesselType","Status","Length","Width","Draft","Cargo","TranscieverClass"])
data["TimeDate"] = pd.to_datetime(data["TimeDate"]).apply(lambda x: x.timestamp())
for i,g in data.groupby("VesselType"):
    g.to_pickle("./class_"+str(int(i))+".pkl")
