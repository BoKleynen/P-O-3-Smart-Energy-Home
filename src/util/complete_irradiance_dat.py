import pandas as pd

# No need to run this script again
irradiance_df = pd.read_csv(filepath_or_buffer="../../data/Irradiance.csv",
                            header=0,
                            index_col="Date/Time",
                            dtype={"watts-per-meter-sq": float},
                            skiprows=8,
                            parse_dates=["Date/Time"]
                            )

start = pd.Timestamp("2016-05-24 00:00")
end = pd.Timestamp("2017-04-21 23:55")

time_index = pd.date_range(start, end, freq="300S")
irradiance_df = pd.merge(pd.DataFrame(index=time_index), irradiance_df, how="left", left_index=True, right_index=True)
irradiance_df.interpolate(method="time", inplace=True)
irradiance_df.to_csv("../../data/Irradiance.csv")
