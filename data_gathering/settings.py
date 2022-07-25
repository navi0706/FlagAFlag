from decouple import config, Csv


class Config:
    CHROMEDRIVER_PATH = config("CHROMEDRIVER_PATH")
    DATA_GATHERING_PATH = config("DATA_GATHERING_PATH")