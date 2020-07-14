TRACK_WORDS = ['#covid','#COVID19','#Coronavirus','#SARSCoV2','#coronavirus' ,'#covid', '#corona', '#stayhome', '#quarantine' ,'#lockdown', '#socialdistancing', '#staysafe', '#virus', '#Mask' ,'#coronav', '#stayathome', '#pandemic']
TABLE_NAME = "covid19"
TABLE_ATTRIBUTES = "id_str VARCHAR(255), created_at DATETIME, text VARCHAR(255), \
            sentiment INT, user_created_at VARCHAR(255), user_location VARCHAR(255), \
            user_description VARCHAR(255), user_followers_count INT, longitude DOUBLE, latitude DOUBLE, \
            retweet_count INT, favorite_count INT"
