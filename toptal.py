#%%
import numpy as np

def mutual_information(arr):
    pi = np.sum(arr, axis=1)
    pj = np.sum(arr, axis=0)
    total = np.sum(arr)

    mut_inf =0
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            try:
                mut_inf += arr[i,j]*np.log(arr[i,j]/(pi[i]*pj[j]))
            except:
                pass

    mut_inf /= total

    return mut_inf
# %%

arr = np.array([[1,2,3],[4,5,6],[7,8,9]])
#%%
np.sum(arr)


# %%
mutual_information(arr)
# %%
# importing the pandas library
import pandas as pd
import numpy as np
#https://www.studypool.com/discuss/41314152/need-to-help-with-timed-3-task-using-python-language-with-and-machine-learning-packages
# creating solution function which takes list of datasets/files
def solution(files):
    output=[]
    for file in files:
        file = pd.read_csv(file)
        file['date'] = pd.to_datetime(file['date'], format = '%Y-%m-%d')
        grouped1 = file.groupby(file['date'].dt.year)['vol']
        max1 = grouped1.idxmax().reset_index().drop('date',axis=1).vol.to_list()
        output1 = pd.DataFrame()
        for i in max1:
            output1 = output1.append(file.loc[i],ignore_index=True,sort=False)[file.columns.tolist()]
        output1=output1.drop(['open','min','max','close'],axis=1)
        
        
        grouped2 = file.groupby(file['date'].dt.year)['close']
        max2 = grouped2.idxmax().reset_index().drop('date',axis=1).close.to_list()
        output2 = pd.DataFrame()
        for i in max2:
            output2 = output2.append(file.loc[i],ignore_index=True,sort=False)[file.columns.tolist()]
        output2=output2.drop(['open','min','max','vol'],axis=1)
    
        output.append([output1, output2])    
        
    return output
#%%
files = [
        #"./data/framp.csv" 
        #,"./data/gnyned.csv" 
        #,"./data/gwoomed.csv"
        #,"./data/hoilled.csv"
        #,"./data/plent.csv"
        "./data/throwsh.csv"
        ,"./data/twerche.csv"
        #,"./data/veeme.csv"
        ]

# %%
dfs=solution(files)

dfs
# %%
file = pd.read_csv('./data/twerche.csv')

file['date'] = pd.to_datetime(file['date'], format = '%Y-%m-%d')
gb1 = file.groupby(file['date'].dt.year)['vol']
my1 = gb1.idxmax()
# my1.reset_index().drop('date',axis=1).vol.to_list()
# df1 = pd.DataFrame()
# gb2 = file.groupby(file['date'].dt.year)['close']
# my2 = gb2.idxmax()
# my2.reset_index().drop('date',axis=1).close.to_list()
# df2 = pd.DataFrame()
# for i in my1:
# df1 = df1.append(file.loc[i],ignore_index=True,sort=False)[file.columns.tolist()]
# for i in my2:
# df2 = df2.append(file.loc[i],ignore_index=True,sort=False)[file.columns.tolist()]
# df1=df1.drop(['open','min','max','close'],axis=1)
# df2=df2.drop(['open','min','max','vol'],axis=1)
# output.append(df1)
# output.append(df2)




# %%

# %%
dfs[1][1]

# %%

#https://www.answersdive.com/ExpertAnswers/solve-in-java-john-likes-to-travel-he-has-visited-a-lot-of-cities-over-many-years-whenever-he-visits
string = """photo.jpg, Warsaw, 2013-09-05 14:08:15
john.png, London, 2015-06-20 15:13:22
myFriends.png, Warsaw, 2013-09-05 14:07:13
Eiffel.jpg, Paris, 2015-07-23 08:03:02
pisatower.jpg, Paris, 2015-07-22 23:59:59
BOB.jpg, London, 2015-08-05 00:02:03
notredame.png, Paris, 2015-09-01 12:00:00
me.jpg, Warsaw, 2013-09-06 15:40:22
a.png, Warsaw, 2016-02-13 13:33:50
b.jpg, Warsaw, 2016-01-02 15:12:22
c.jpg, Warsaw, 2016-01-02 14:34:30
d.jpg, Warsaw, 2016-01-02 15:15:01
e.png, Warsaw, 2016-01-02 09:49:09
f.png, Warsaw, 2016-01-02 10:55:32
g.jpg, Warsaw, 2016-02-29 22:13:11"""

def solution(S):
    lines = S.split('\n')
    output = []
    photos = {}
    for i, line in enumerate(lines):
        original_name, city, time = [s.strip() for s in line.split(',')]
        name, extension = original_name.split('.')
        if city in photos:
            photos[city].append((name, extension, time, i))
        else:
            photos[city] = [(name, extension, time, i)]
    for city in photos:
        count = len(photos[city])
        zeros = len(str(count))
        counter = 1
        photos[city].sort(key=lambda n: n[-2])
        for name in photos[city]:
            output.append((name[-1], city+str(counter).zfill(zeros)+'.'+name[1]))
            counter += 1
    output.sort(key=lambda n: n[0])
    final_output = [i[1] for i in output]
    return final_output
# %%
solution(string)
# %%
