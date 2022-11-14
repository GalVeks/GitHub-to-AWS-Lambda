from insta_public_functions import GetInstagramProfile
import pandas as pd
import random
from public_func import save_pd_csv_to_s3
from datetime import date

def main_run(profile):
    data = {'Index': [1], 'Username': ['lapicanteff'], 'Password': ['Gv300444494!!']}
    dfigaccounts = pd.DataFrame(data)

    today = date.today()
    year = today.strftime("%Y")
    month = today.strftime("%m")
    day = today.strftime("%d")

    # profiles = {'galvekselman'}  # df['followee_username'].tolist()
    cls = GetInstagramProfile()

    # for profile in profiles:
    print(profile)
    account_index = random.randint(1, len(dfigaccounts.index))-1
    df = cls.get_users_followers(profile,
                                dfigaccounts['Username'][account_index],
                                dfigaccounts['Password'][account_index]
                                )
    directory = "instagram/followers/{}/{}/{}/{}.csv".format(year, month, day, profile)
    save_pd_csv_to_s3(df=df, key=directory)