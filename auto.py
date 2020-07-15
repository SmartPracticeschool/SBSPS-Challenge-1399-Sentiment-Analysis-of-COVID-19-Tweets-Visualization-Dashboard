import os
print("Welcome to SBSPS-Challenge-1399-Sentiment-Analysis-of-COVID-19-Tweets-Visualization-Dashboard")



osy = 1

if osy == 1:

    cwd = os.getcwd()
    os.chdir("/".join([cwd,"model building"]))
    os.system("ls")
    # Twitter auth and running model



    os.chdir(cwd)
    # os.system("virtualenv venv")
    # os.system("source venv/bin/activate")

    os.system("python run.py")
    print(os.getcwd())
    # os.system("google-chrome localhost:5000")


elif osy == 2:
    print("You Choosed Windows")

else:
    print("Wrong Choise")