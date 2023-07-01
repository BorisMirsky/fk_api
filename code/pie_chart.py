import matplotlib.pyplot as plt
from Citizenship_team import Citizenship_team

country_and_club_eng_statistics = Citizenship_team('france', 'nice')

def make_plot():
        sizes  = country_and_club_eng_statistics.date_for_plot()[1]   
        labels = country_and_club_eng_statistics.date_for_plot()[0]
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels = labels, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal')  
        plt.show()

make_plot()
