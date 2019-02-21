from watson_developer_cloud import ToneAnalyzerV3
import json
import pandas as pd

tone_analyzer = ToneAnalyzerV3(
    version='2019-01-26',
    iam_apikey='gUyh2OR0IBixeyvJWRfs_QjOdDGphIDi2ZhpbsmAg_aE',
    url='https://gateway-lon.watsonplatform.net/tone-analyzer/api'
)
tone_analyzer.set_default_headers({'x-watson-learning-opt-out': "true"})

def analyze_sentiment(text):
    tone_analysis = tone_analyzer.tone(
        {'text': text},
        'application/json'
    ).get_result()

    tones = tone_analysis['document_tone']['tones']
    tones_sorted = sorted(tones, key=lambda k: k['score'], reverse=True)
    main_tone = ''
    main_tone_score = 0
    if len(tones_sorted):
        main = tones_sorted[0]
        if main['tone_name'] != 'Analytical':
            main_tone = main['tone_name']
            main_tone_score = main['score']
        else:
            try:
                if tones_sorted[1]['tone_name'] != 'Analytical':
                    main_tone = tones_sorted[1]['tone_name']
                    main_tone_score = tones_sorted[1]['score']
            except:
                pass
    return main_tone, main_tone_score

df = pd.read_csv('merged.csv')
df1 = pd.DataFrame(columns = ['debate', 'date', 'speech', 'name', 'party', 'sentiment', 'score'])
df = df.iloc[20703:]
for index, row in df.iterrows():
    try:
        sentiment, score = analyze_sentiment(row['speech'])
        if score!=0:
            row = [row['debate_name'], row['debate_date'], row['speech'], row['name'], row['party'], sentiment, score]
            df1.loc[len(df1)] = row
    except:
        pass

df1.to_csv('sentiment_new.csv')


