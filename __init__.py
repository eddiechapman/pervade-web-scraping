from explorers import AnalyticsNCSUExplorer, DataSciGradProgramsExplorer, EdisonProjectExplorer

if __name__ == '__main__':
    # explorer = AnalyticsNCSUExplorer()
    # print(explorer.degree_count)
    explorer = DataSciGradProgramsExplorer()
    print(len(explorer.degrees))
    explorer.export_degrees('datascigradprogramsdegrees.json')

    #explorer = EdisonProjectExplorer()
