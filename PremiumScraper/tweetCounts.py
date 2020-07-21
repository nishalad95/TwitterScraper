from searchtweets import ResultStream, gen_rule_payload, load_credentials, collect_results

import json
import pandas as pd
import ast


RUN_SCRAPER = False


premium_search_args = load_credentials("twitter_keys.yaml",
                                       yaml_key="search_tweets_api",
                                       env_overwrite=False)

query = ''
from_date = "2020-01-01"
to_date = "2020-06-21"
bucket = "hour"
results_per_call = 8000
filename = "covid_counts"


if RUN_SCRAPER:

    rule = gen_rule_payload(query,
                            from_date=from_date,
                            to_date=to_date,
                            count_bucket=bucket,
                            results_per_call=results_per_call)

    counts = collect_results(rule, max_results=results_per_call, result_stream_args=premium_search_args)


    with open(filename) as f:
        data = ast.literal_eval(f.read())

    df = pd.DataFrame(data)
    df.to_csv(filename + '.csv', index=False)
