import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
matches=pd.read_csv("C:/Users/venuv/Downloads/Project4 - IPL Data Analysis/matches.csv")
deliveries=pd.read_csv("C:/Users/venuv/Downloads/Project4 - IPL Data Analysis/deliveries.csv")
print(matches.head())
print(deliveries.head())
print(" matches dataset shape:",matches.shape)
print("deliveries dataset shape",deliveries.shape)
print(deliveries.info())
print(matches.info())
print(matches.describe())
print(deliveries.describe())
print(matches.isnull().sum())
print(deliveries.isnull().sum())
matches['city']=matches['city'].fillna('UnKnown',inplace=True)
matches['winner']=matches['winner'].fillna('No Result',inplace=True)
print(matches.isnull().sum())
matches['date']=pd.to_datetime(matches['date'])
matches.columns=matches.columns.str.lower().str.strip()
deliveries.columns=deliveries.columns.str.lower().str.strip()
print(matches.head())
print(matches.info())
matches['win_by_runs']=np.where(matches['result']=='runs',matches['result_margin'],0)
print(matches.head())
matches['win_by_wickets']=np.where(matches['result']=='wickets',matches['result_margin'],0)
print(matches.head())
matches['is_no_result']=matches['winner']=='no result'
matches['toss_winner_match_winner']=(matches['toss_winner']==matches['winner'])
print(matches.sample(10))
deliveries['is_boundary']=deliveries['batsman_runs'].isin([4,6])
deliveries['is_dot_ball']=deliveries['total_runs']==0
deliveries['is_single']=deliveries['total_runs']==1
deliveries['is_double']=deliveries['total_runs']==2
deliveries['is_triple']=deliveries['total_runs']==3
deliveries['is_wicket_ball']=deliveries['is_wicket']==1
print(deliveries[['is_boundary','is_dot_ball','is_wicket_ball']].head())
#EDA
matches_per_season=matches.groupby('season')['id'].count()
print(matches_per_season)
matches_per_season.plot(kind='bar',figsize=(10,5),title='Number Of Matches Played Per Season')
plt.xlabel('season')
plt.ylabel('Number Of Matches')
plt.show()
team_wins=matches['winner'].value_counts()
print(team_wins.head(10))
team_wins.head(10).plot(kind='bar',figsize=(10,5),title='Top 10 Most Sucessful Teams')
plt.xlabel('Team')
plt.ylabel('Number Of Wins')
plt.show()
print(matches['toss_winner_match_winner'].value_counts())
toss_win_per=(matches['toss_winner_match_winner'].mean()*100)
print(toss_win_per)
ax=matches['toss_winner_match_winner'].value_counts().plot(kind='bar',figsize=(10,5),title='Toss Winner VS Match Winner')
ax.bar_label(ax.containers[0])
plt.xticks([0,1],['won match','lost match'],rotation=0)
plt.ylabel('Match count')
plt.show()
matches['result'].value_counts().plot(kind='pie',autopct='%1.1f%%',figsize=(6,6),title='Match Result Type Distribution')
plt.ylabel('')
plt.show()
season_team_wins=(matches.groupby(['season','winner']).size().unstack(fill_value=0))
print(season_team_wins)
#EDA :BALL-LEVEL INSIGHTS
top_batsman_runs=(deliveries.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False))
print(top_batsman_runs.head(10))
bx=top_batsman_runs.head(10).plot(kind='bar',figsize=(10,5),title='Top 10 Batsman by Total Runs')
bx.bar_label(bx.containers[0])
plt.xlabel('Batsman')
plt.ylabel('Total Runs')
plt.show()
balls_faced=deliveries.groupby('batter').size().sort_values(ascending=False)
print(balls_faced)
batsman_stats=deliveries.groupby('batter').agg(total_runs=('batsman_runs','sum'),balls_faced=('ball','count'))
print(batsman_stats)
batsman_stats['strike_rate']=(batsman_stats['total_runs']/ batsman_stats['balls_faced'])*100
print(batsman_stats.sort_values('strike_rate',ascending=False).head(10))
print(batsman_stats[batsman_stats['balls_faced']>10].sort_values('strike_rate',ascending=False).head(10))
#BOUNDARY COUNT BY  BATSMAN
boundary_count=(deliveries[deliveries['is_boundary']].groupby('batter').size().sort_values(ascending=False))
print(boundary_count.head(10))
#TOP 10 BOWLERS BY WICKETS
top_bowlers_wickets=deliveries[deliveries['is_wicket_ball']].groupby('bowler').size().sort_values(ascending=False)
print(top_bowlers_wickets.head(10))
#visualization
cx=top_bowlers_wickets.head(10).plot(kind='bar',figsize=(10,5),title='Top 10 Bowlers by Total Wickets')
cx.bar_label(cx.containers[0])
plt.xlabel('Bowlers')
plt.ylabel('Total Wickets')
plt.show()
#ECONOMY 
bowlers_stats=deliveries.groupby('bowler').agg(runs_conceded=('total_runs',sum),balls_bowled=('ball','count'))
bowlers_stats['economy_rate']=(bowlers_stats['runs_conceded']/ bowlers_stats['balls_bowled']*6)
print(bowlers_stats.sort_values('economy_rate',ascending=True).head(10))
#dot ball percentage
dot_balls_stats=deliveries.groupby('bowler').agg(dot_balls=('is_dot_ball',sum),balls_bowled=('ball','count'))
dot_balls_stats['dot_ball_per']=(dot_balls_stats['dot_balls']/ dot_balls_stats['balls_bowled']*100)
print(dot_balls_stats.sort_values('dot_ball_per',ascending=False).head(10))
vd=dot_balls_stats['dot_ball_per'].sort_values(ascending=False)
#visualization for dot ball percentage by bowler
dx=vd.head(10).plot(kind='bar',figsize=(10,5),title='Top 10 Bowlers by dot ball percentage')
dx.bar_label(dx.containers[0])
plt.xlabel('Bowlers')
plt.ylabel('percentage')
plt.show()
#filter batsmen with minimum balls faced
batsman_stats_filtered=batsman_stats[batsman_stats['balls_faced']>=500]
print(batsman_stats_filtered.sort_values('strike_rate',ascending=False).head(10))
#merge match_level  and ball_level data
merged_df=deliveries.merge(matches[['id','season','winner','toss_decision']],left_on='match_id',right_on='id',how='left')
print(merged_df.head(10))
#average runs per season
season_runs=(merged_df.groupby('season')['total_runs'].sum().reset_index())
matches_per_season=matches.groupby('season')['id'].count()
season_summary=season_runs.merge(matches_per_season,on="season")
season_summary['avg_runs_per_match']=(season_summary['total_runs']/ season_summary['id'])
print(season_summary)
#visualization using seaborn
import seaborn as sns
plt.figure(figsize=(10,5))
sns.lineplot(data=season_summary,x='season',y='avg_runs_per_match',marker="o")
plt.title('Average Runs Per match Across Seasons')
plt.xlabel('Season')
plt.ylabel('Average Runs Per Match')
plt.show()
#Runs scored on toss decision
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
toss_runs=(merged_df.groupby('toss_decision')['total_runs'].sum().reset_index())
print(toss_runs)
# visualization
plt.figure(figsize=(6,4))
sns.barplot(data=toss_runs,x='toss_decision',y='total_runs')
plt.title('Total Runs Scored Based on Toss Decision')
plt.xlabel('Toss Decision')
plt.ylabel('Total Runs')
plt.show()
#top batsmen runs by season
top_batsman=(merged_df.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(5).index)
print(top_batsman)
batsman_season_runs=(merged_df[merged_df['batter'].isin(top_batsman)].groupby(['season','batter'])['batsman_runs'].sum().reset_index())
print(batsman_season_runs.head(5))
# visualization
plt.figure(figsize=(12,6))
sns.lineplot(data=batsman_season_runs,x='season',y='batsman_runs',hue='batter',marker='o')
plt.title('Season Wise Runs for Top Batsman')
plt.xlabel('Season')
plt.ylabel('Runs Scored')
plt.legend(title='Batsman')
plt.show()
#runs scored in winning matches
winning_team_runs=(merged_df[merged_df['batting_team']==merged_df['winner']].groupby('winner')['total_runs'].sum().sort_values(ascending=False))
print(winning_team_runs)
# visualization
winning_team_runs.head(10).plot(kind='bar',figsize=(10,5),title='Total Runs Scored by Winning Team')
plt.xlabel('Team')
plt.ylabel('Runs')
plt.show()
#mtaches played per city
import folium
city_matches=(matches.groupby('city')['id'].count().reset_index().rename(columns={'id':'match_count'}))
city_matches=city_matches[city_matches['city']!='unknown']
print(city_matches.head())
city_coordinates = {
    "Ahmedabad": (23.0225, 72.5714),
    "Bangalore": (12.9716, 77.5946),
    "Bengaluru": (12.9716, 77.5946),  
    "Chandigarh": (30.7333, 76.7794),
    "Chennai": (13.0827, 80.2707),
    "Cuttack": (20.4625, 85.8830),
    "Delhi": (28.6139, 77.2090),
    "Dharamsala": (32.2190, 76.3234),
    "Hyderabad": (17.3850, 78.4867),
    "Indore": (22.7196, 75.8577),
    "Jaipur": (26.9124, 75.7873),
    "Kanpur": (26.4499, 80.3319),
    "Kochi": (9.9312, 76.2673),
    "Kolkata": (22.5726, 88.3639),
    "Lucknow": (26.8467, 80.9462),
    "Mohali": (30.7046, 76.7179),
    "Mumbai": (19.0760, 72.8777),
    "Nagpur": (21.1458, 79.0882),
    "Navi Mumbai": (19.0330, 73.0297),
    "Pune": (18.5204, 73.8567),
    "Raipur": (21.2514, 81.6296),
    "Rajkot": (22.3039, 70.8022),
    "Ranchi": (23.3441, 85.3096),
    "Sharjah": (25.3463, 55.4209),
    "Abu Dhabi": (24.4539, 54.3773),
    "Dubai": (25.2048, 55.2708),
    "Visakhapatnam": (17.6868, 83.2185)
}
city_matches['coordinates']=city_matches['city'].map(city_coordinates)
city_matches=city_matches.dropna(subset=['coordinates'])
print(city_matches.head())
# create base map centered on india
india_map=folium.Map(location=[22.5937,78.9629],zoom_start=5,tiles='OpenStreetMap')
#add markers for each city
for _,row in city_matches.iterrows():
    folium.CircleMarker(
        location=row['coordinates'],radius=row['match_count']/5,popup=f"{row['city']}<br>matches:{row['match_count']}",color='crimson',fill=True,fill_colours='crimson',fill_opacity=0.7

    ).add_to(india_map)
india_map.save("ipl_map.html")
#orange cap holder by season
season_run=merged_df.groupby(['season','batter'])['batsman_runs'].sum().reset_index()
orange_cap=season_run.loc[season_run.groupby('season')['batsman_runs'].idxmax()]
orange_cap=orange_cap.rename(columns={'batter':'orange_cap_holder'})
print(orange_cap)
#purple cap holder by season
season_wickets=merged_df.groupby(['season','bowler'])['is_wicket'].sum().reset_index()
purple_cap=season_wickets.loc[season_wickets.groupby('season')['is_wicket'].idxmax()]
purple_cap=purple_cap.rename(columns={'bowler':'purple_cap_holder'})
purple_cap=purple_cap.rename(columns={'is_wicket':'wickets'})


print(purple_cap)
