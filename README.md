## SBSPS-Challenge-1399-Sentiment-Analysis-of-COVID-19-Tweets-Visualization-Dashboard
----

### Problem Statement

The sentiment analysis of Indians after the extension of lockdown announcements to be analyzed with the relevant #tags on twitter and build a predictive analytics model to understand the behavior of people if the lockdown is further extended.
Also develop a dashboard with visualization of people reaction to the govt announcements on lockdown extension

### Proposed Solution

Inorder to solve above problem, We have build predictive system to understand the sentiments of people from Live Tweets. For building the model we have used sentiment140 dataset. It contains 1,600,000 tweets extracted using the Twitter API. The tweets have been annotated (-1 = negative, 0 = neutral, 1 = positive)

According to the creators of the dataset:
 	''Our approach was unique because our training data was automatically created, as opposed to having humans manual annotate tweets. In our approach, we assume that any tweet with positive emoticons, like :), were positive, and tweets with negative emoticons, like :(, were negative. We used the Twitter Search API to collect these tweets by using keyword search''          
    
So, with the help of visualization of these Live sentiments we get prior notice of increasing negative sentiments curve.

### Technology Stack

Front End: Flask Framework

Back End : phpmyadmin, Tensorflow 2.2

### Usage

1. Download the repository

    ```markdown
    $ git clone https://github.com/SmartPracticeschool/SBSPS-Challenge-1399-Sentiment-Analysis-of-COVID-19-Tweets-Visualization-Dashboard.git
    ```



2. Locate repository

    ```markdown
    $ cd SBSPS-Challenge-1399-Sentiment-Analysis-of-COVID-19-Tweets-Visualization-Dashboard
    ```



3. Start the phpmyadmin server and create database named twitterdb



4. Locate Model Building for data Grathering

    ```markdown
    $ cd model building
    ```



5. Edit `credentials.py` with your twitterAPI keys



6. Extract `model.h5.tar.gz` and run jupyter-server and run all the cells in  `IBM_Challenge.ipynb`
    Now data will be store on `tweeterdb` which we have created in Usage 3



7. Locate SBSPS-Challenge-1399-Sentiment-Analysis-of-COVID-19-Tweets-Visualization-Dashboard turn on virtualenv

    ```markdown
    # Create Virtual environment
    virtualenv venv
    # Use Virtual environment
    source venv/bin/activate
    # Install requirements
    pip install -r requirements.txt
    #run flask server
    python run.py
    ```



8. Open `localhost:5000` on chrome and Visualize data in real time.

### Screenshots
 
![Image1](https://smartpracticeschool.github.io/SBSPS-Challenge-1399-Sentiment-Analysis-of-COVID-19-Tweets-Visualization-Dashboard/screenshots/Screenshot1.png)

![Image2](https://smartpracticeschool.github.io/SBSPS-Challenge-1399-Sentiment-Analysis-of-COVID-19-Tweets-Visualization-Dashboard/screenshots/Screenshot2.png)

### Team Profile

1. Shubham Kondekar [Github](https://github.com/kondekarshubham123) , [Linkedin](https://in.linkedin.com/in/shubham-kondekar)

2. Pranali Yangandul [Github](https://github.com/Pranaliyangandul) , [Linkedin](https://in.linkedin.com/in/pranaliyangandul)

3. Sarthak Phatate [Github](https://github.com/SarthakPhatate) , [Linkedin](https://in.linkedin.com/in/sarthak-phatate-292794175)

4. Nilesh Chilka [Github](https://github.com/nileshchilka1) , [Linkedin](https://in.linkedin.com/in/nilesh-chilka-8a55b4146)
