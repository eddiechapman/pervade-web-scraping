from degrees import AnalyticsNCSUDegree, DataSciGradProgramsDegree
from explorers import AnalyticsNCSUExplorer, DataSciGradProgramsExplorer

if __name__ == '__main__':
    explorer = AnalyticsNCSUExplorer()
    #explorer = DataSciGradProgramsExplorer()
    print(explorer.degree_count)
    #print(len(explorer.degrees))