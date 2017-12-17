import pandas as pd

# No need to run this script again
wind_speed_df = pd.read_csv(filepath_or_buffer="/Users/bokleynen/Documents/2Bir/P&O3/Smart-Energy-Home/data/Average-Wind-Speed.csv",
                            header=0,
                            index_col="Date/Time",
                            dtype={"miles-per-hour": float},
                            skiprows=8,
                            parse_dates=["Date/Time"]
                            )
wind_speed_df["miles-per-hour"] = wind_speed_df["miles-per-hour"] * 2

start = pd.Timestamp("2016-05-24 00:00")
end = pd.Timestamp("2017-04-21 23:55")

time_index = pd.date_range(start, end, freq="300S")
wind_speed_df = pd.merge(pd.DataFrame(index=time_index), wind_speed_df, how="left", left_index=True, right_index=True)
wind_speed_df.interpolate(method="time", inplace=True)
wind_speed_df.to_csv("/Users/bokleynen/Documents/2Bir/P&O3/Smart-Energy-Home/data/wind_speed.csv")

