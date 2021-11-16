import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import streamlit as st


df_asian = pd.read_csv("D:\Medal_List_Combined.csv")
df_asian["Year"] = [int(x) for x in df_asian["Year"].tolist()]
df_asian = df_asian.astype({"Year":object})
df_asian.rename(columns = {"Nation":"Country"},inplace=True)
df_oly = pd.read_csv("D:\Olympics_Medal_List.csv")

df_asian.replace("Republic of China","China",inplace=True)
df_asian.replace("Ceylon","Sri Lanka",inplace=True)

asian_countries = df_asian["Country"].unique().tolist()
oly_countries = df_oly["Country"].unique().tolist()
final_countries = list(set(asian_countries).intersection(oly_countries))
final_countries.sort()
final_countries.insert(0,None)
final_countries.append("Overall")

def Helper1(game_df,country,year):
    

    li3=[]
    df = game_df[game_df["Year"] == year]
    countries = df["Country"].unique().tolist()
    for nation in countries:
        df_c = df[df["Country"] == nation]
        li3.append((nation,year,df_c["Gold"].sum(),df_c["Silver"].sum(),df_c["Bronze"].sum(),df_c["Total"].sum()))
    li3.sort(key=lambda x : x[2],reverse=True)
    ans3_df = pd.DataFrame(li3,columns=["Country","Year","Gold","Silver","Bronze","Total"])

    
    li4=[]
    countries = game_df["Country"].unique().tolist()
    for nation in countries:
        df_c = game_df[game_df["Country"] == nation]
        li4.append((nation,df_c["Gold"].sum(),df_c["Silver"].sum(),df_c["Bronze"].sum(),df_c["Total"].sum()))
    li4.sort(key=lambda x : x[1],reverse=True)
    ans4_df = pd.DataFrame(li4,columns=["Country","Gold","Silver","Bronze","Total"])
    
    
    li5=[]
    years = game_df["Year"].unique().tolist()
    df_c = game_df[game_df["Country"] == country]
    for y in years:
        df_y = df_c[df_c["Year"] == y]
        li5.append((country,y,df_y["Gold"].sum(),df_y["Silver"].sum(),df_y["Bronze"].sum(),df_y["Total"].sum()))
    li5.sort(key=lambda x : x[1],reverse=False)
    ans5_df = pd.DataFrame(li5,columns=["Country","Year","Gold","Silver","Bronze","Total"])
    

   
    if(year == "All years"):

        fig = plt.figure(figsize = (15, 5))
        sns.barplot(ans5_df["Year"],ans5_df["Total"])
        plt.xticks(rotation = 45)
        plt.title("No Of Medals Won By "+country+" Year Wise",fontsize = 20)
        plt.xlabel("Year",fontsize=15)
        plt.ylabel("Total Medals",fontsize=15)
        plt.savefig(country+"_all_years.png",bbox_inches='tight')
        #plt.close()
        return (ans5_df,plt)
    
    elif(country == "Overall" and year != "Overall"):
        
        fig = plt.figure(figsize = (15, 5))
        sns.barplot(ans3_df["Country"],ans3_df["Total"])
        plt.xticks(rotation = 90)
        plt.title("No Of Medals Won in "+str(year),fontsize = 20)
        plt.xlabel("Countries",fontsize=15)
        plt.ylabel("Total Medals",fontsize=15)
        plt.savefig("Overall_"+str(year)+".png",bbox_inches='tight')
        #plt.close()
        return (ans3_df,plt)
    
    elif(country == "Overall" and year == "Overall"):
        
        fig = plt.figure(figsize = (15, 5))
        sns.barplot(ans4_df["Country"],ans4_df["Total"])
        plt.xticks(rotation = 90)
        plt.title("No Of Medals Won By Each Country",fontsize = 20)
        plt.xlabel("Countries",fontsize=15)
        plt.ylabel("Total Medals",fontsize=15)
        plt.savefig("Overall_Overall.png",bbox_inches='tight')
        #plt.close()
        return (ans4_df,plt)
    
    elif(country != "Overall" and year == "Overall"):
        return ans4_df[ans4_df["Country"] == country]
    elif(country != "Overall" and year != "Overall"):
        return ans3_df[ans3_df["Country"] == country]
    
    
    
def Medal_Tally(game,country,year):
    
    if(game == "Asian"):
        return Helper1(df_asian.copy(),country,year)
    elif(game == "Olympics"):
        return Helper1(df_oly.copy(),country,year)
    else:
        return (Helper1(df_asian.copy(),country,year),Helper1(df_oly.copy(),country,year))



def Helper2(game_df,country,year):
    
    li3=[]
    df_y = game_df[game_df["Year"] == year]
    countries = df_y["Country"].unique().tolist()
    for nation in countries:
        df_c = df_y[df_y["Country"] == nation]
        li3.append((nation,year,(df_c["Gold"].sum()/df_y["Gold"].sum())*100,(df_c["Silver"].sum()/df_y["Silver"].sum())*100,(df_c["Bronze"].sum()/df_y["Bronze"].sum())*100,(df_c["Total"].sum()/df_y["Total"].sum())*100))
    ans3_df = pd.DataFrame(li3,columns=["Country","Year","% Gold","% Silver","% Bronze","% Total"])
    

    li4=[]
    countries = game_df["Country"].unique().tolist()
    for nation in countries:
        df_c = game_df[game_df["Country"] == nation]
        li4.append((nation,(df_c["Gold"].sum()/game_df["Gold"].sum())*100,(df_c["Silver"].sum()/game_df["Silver"].sum())*100,(df_c["Bronze"].sum()/game_df["Bronze"].sum())*100,(df_c["Total"].sum()/game_df["Total"].sum())*100))
    ans4_df = pd.DataFrame(li4,columns=["Country","% Gold","% Silver","% Bronze","% Total"])
    


    if(country == "Overall" and year == "Overall"):
        
        fig = plt.figure(figsize = (15, 5))
        sns.barplot(ans4_df["Country"],ans4_df["% Total"])
        plt.xlabel("Countries",fontsize=15)
        plt.ylabel("% Total",fontsize=15)
        plt.title("Overall % Of Medals Won by Each Country",fontsize=20)
        plt.xticks(rotation = 90)
        plt.savefig("Overall_percentage.png",bbox_inches='tight')
        #plt.close()
        return (ans4_df,plt)
    
    elif(country == "Overall" and year != "Overall"):
        fig = plt.figure(figsize = (15, 5))
        sns.barplot(ans3_df["Country"],ans3_df["% Total"])
        plt.xlabel("Countries",fontsize=15)
        plt.ylabel("% Total",fontsize=15)
        plt.title("% Of Medals Won by Each Country in "+str(year),fontsize=20)
        plt.xticks(rotation = 90)
        plt.savefig("Overall_percentage_"+str(year)+".png",bbox_inches='tight')
        #plt.close()
        return (ans3_df,plt)
    
    elif(country != "Overall" and year == "Overall"):
        return ans4_df[ans4_df["Country"] == country]
    
    elif(country != "Overall" and year != "Overall"):
        return ans3_df[ans3_df["Country"] == country]
    
def Medal_percentage(game,country,year):
    
    if(game == "Asian"):
        return Helper2(df_asian.copy(),country,year)
    elif(game == "Olympics"):
        return Helper2(df_oly.copy(),country,year)
    else:
        return (Helper2(df_asian.copy(),country,year),Helper2(df_oly.copy(),country,year))



def Helper3(game_df,country,year):
    
    if(year != "Overall"):
        li3=[]
        df = game_df[game_df["Year"] == year]
        countries = df["Country"].unique().tolist()
        ans3_df = pd.DataFrame()
        for nation in countries:
            df_c = df[(df["Country"] == nation)]
            ans3_df = pd.concat([ans3_df,df_c[["Country","Sport","Year","Gold","Silver","Bronze","Total"]]])
        ans3_df.sort_values(["Country","Sport"],ascending=[True,True],inplace=True)
        ans3_df.reset_index(drop=True,inplace=True)
        
    
    
    li4=[]
    countries = game_df["Country"].unique().tolist()
    games = game_df["Sport"].unique().tolist()
    for nation in countries:
        for game in games:
            df_c = game_df[(game_df["Sport"] == game) & (game_df["Country"] == nation)]
            if(df_c.empty):
                continue
            li4.append((nation,game,df_c["Gold"].sum(),df_c["Silver"].sum(),df_c["Bronze"].sum(),df_c["Total"].sum()))
    ans4_df = pd.DataFrame(li4,columns=["Country","Sport","Gold","Silver","Bronze","Total"])
    ans4_df.sort_values(["Country","Sport"],ascending=[True,True],inplace=True)
    ans4_df.reset_index(drop=True,inplace=True)
    
    
    
    if(country == "Overall" and year == "Overall"):
        return ans4_df
    
    elif(country == "Overall" and year != "Overall"):
        return ans3_df
    
    elif(country != "Overall" and year == "Overall"):
        
        df =  ans4_df[ans4_df["Country"] == country]
        fig = plt.figure(figsize = (15, 5))
        sns.barplot(df["Sport"],df["Total"],ci=None,dodge=False)
        plt.xticks(rotation = 45)
        plt.title("No Of Medals Won By "+country+" in "+str(year)+" Sport Wise",fontsize = 20)
        plt.xlabel("Sports",fontsize=15)
        plt.ylabel("Total Medals",fontsize=15)
        plt.savefig(country+"_sport_wise.png",bbox_inches='tight')
        #plt.close()
        return (df,plt)
    
    elif(country != "Overall" and year != "Overall"):
        
        df =  ans3_df[ans3_df["Country"] == country]
        fig = plt.figure(figsize = (15, 5))
        sns.barplot(df["Sport"],df["Total"],ci=None,dodge=False)
        plt.xticks(rotation = 45)
        plt.title("No Of Medals Won By "+country+" in "+str(year)+" Sport Wise",fontsize = 20)
        plt.xlabel("Sports",fontsize=15)
        plt.ylabel("Total Medals",fontsize=15)
        plt.savefig(country+"_sport_wise.png",bbox_inches='tight')
        #plt.close()
        return (df,plt)
    
    
def Medal_sport_wise(game,country,year):
    
    if(game == "Asian"):
        return Helper3(df_asian.copy(),country,year)
    elif(game == "Olympics"):
        return Helper3(df_oly.copy(),country,year)
    else:
        return (Helper3(df_asian.copy(),country,year),Helper3(df_oly.copy(),country,year))









game = st.sidebar.selectbox("Select Game",options=["Asian","Olympics"])
analysis = st.sidebar.selectbox("What Do You Want To Analyze",options=["None","Medal Tally","Medal Percentage","Medal Sport Wise"])
country = st.sidebar.selectbox("Select Country",options=final_countries)

if(game == "Asian"):
    years = df_asian["Year"].unique().tolist()
    years.append("Overall")
    years.append("All years")
    year = st.sidebar.selectbox("Select Year",options=years)
elif(game == "Olympics"):
    years = df_oly["Year"].unique().tolist()
    years.append("Overall")
    years.append("All years")
    year = st.sidebar.selectbox("Select Year",options=years) 



#st.header
header = st.container()
display = st.container()
plot = st.container()

fig = None
if(analysis == "Medal Tally"):
    if(country == "Overall" or year == "All years"):
        df,fig = Medal_Tally(game,country,year)
    else:
        df = Medal_Tally(game,country,year)

elif(analysis == "Medal Percentage"):
    if(country == "Overall"):
        df,fig = Medal_percentage(game,country,year)
    else:
        df = Medal_percentage(game,country,year)

elif(analysis == "Medal Sport Wise"):
    if(country != "Overall"):
        df,fig = Medal_sport_wise(game,country,year)
    else:
        df = Medal_sport_wise(game,country,year)

with header:
    st.title("Data Analysis On Asian and Olympic Games")

with display:
    st.title("Table")
    st.write(df)
    #st.pyplot(fig)

with plot:
    if(fig != None):
        st.title("Graph")
        st.pyplot(fig)