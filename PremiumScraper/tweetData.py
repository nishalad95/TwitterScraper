import requests
import json
import urllib.parse

endpoint = "<TWITTER PREM API ENDPOINT>" 
headers = {"Authorization":"Bearer <BEARER TOKEN HERE>", "Content-Type": "application/json", "charset": "utf-8"}


# IMPORTANT: CHANGE TO RUN PREMIUM API
RUN_SCRAPER = False


# variables
month_name = 'jun'
month = '06'
date = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
hour = ['09', '10', '11', '12', '13', '14', '15', '16', '17']
filename = month_name + "/GB_covid19_hashtags_" + month + "_"
min_time = 16  # start time hour of double tweet collection
max_time = 19  # end time hour of doublet tweet collection
query = '(#covid OR #coronavirus) -is:retweet lang:en profile_country:GB'



print("Scraping Twitter Data...")
for i in range(len(date)):
    
    # date format YYYYMMDDHHMM (hour and minutes optional)
    date_fmt = '2020' + month + date[i]
    
    for j in range(len(hour) - 1):

        from_date = date_fmt + hour[j] + '00'
        to_date = date_fmt + hour[j+1] + '00'

        data = '{"query": "' + query + '",' \
                '"fromDate": "' + from_date +'",' \
                '"toDate": "' + to_date + '",' \
                '"maxResults": 500}'

        print("\nfrom: ", from_date, "to: ", to_date)
        print(data)
        
        if RUN_SCRAPER:
            
            response = requests.post(endpoint,data=data,headers=headers).json()
            #print(json.dumps(response, indent = 2))

            savefile = filename + from_date + '_' + to_date + '.json'
            print("Saving data in: \n" + str(savefile))
            with open(savefile, 'w') as json_file:
                json.dump(response, json_file)

            # Acquire larger sample of data within a specific time period
            if int(hour[j]) >= min_time and int(hour[j]) <= max_time:
                
                try:
                    next_token = response['next']
                    print("Next token: ", next_token)
                    url_encoded_token = next_token

                    # handle pagination
                    data = '{"query": "' + query + '",' \
                            '"fromDate": "' + from_date +'",' \
                            '"toDate": "' + to_date + '",' \
                            '"maxResults": 500, "next": "'+ url_encoded_token +'"}'

                    print("Paginating next 500 tweets...")
                    print(data)

                    response = requests.post(endpoint,data=data,headers=headers).json()
                    savefile = filename + from_date + '_' + to_date + '_next500.json'
                    print("Saving next 500 tweets in: \n" + str(savefile))
                    with open(savefile, 'w') as json_file:
                        json.dump(response, json_file)
                except:
                    pass

