import os
from supabase import create_client, Client
from st_aggrid import AgGrid
import pandas as pd

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

mood_emoji = {

1: "😭", # Extremely Sad/Broken

2: "☹️", # Very Sad

3: "😞", # Sad

4: "😔", # Somewhat Unhappy

5: "😐", # Neutral

6: "🙂", # Somewhat Happy

7: "😊", # Happy

8: "😃", # Very Happy

9: "😄", # Extremely Happy

10: "😁" # Elated/Overjoyed

}



def create_moodboard():
    data = supabase.table("daily_journal").select("date, mood_scale, description").execute()
    df = pd.DataFrame(data.data)
    df['mood'] = df['mood_scale'].map(mood_emoji)
    df = df.reindex(columns=['date', 'mood', 'mood_scale', 'description'])
    df = df.rename(columns={"description": "nut shell"})
    df_show = df.drop(columns=['mood_scale'])   
    AgGrid(df_show)


## Enhancements ##
# - add a mood card showing the moods of last x days
# - add a mood chart with option to select the number of days
# - provide an expert opinion on how you are feeling for the x days
# - add a productivity to the database