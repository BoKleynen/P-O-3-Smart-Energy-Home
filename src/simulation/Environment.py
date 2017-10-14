class Environment:
    def __init__(self, wind_speed):
        if isinstance(wind_speed, tuple) and len(wind_speed) == 24:
            self.wind_speed = wind_speed
