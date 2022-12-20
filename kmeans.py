# ----- K-means Clustering Task ----- #
'''
 This program is an unsupervised K-Means algorithm that utilises the euclidean formula to plot a k number of clusters, based on the birth rate and life expectancy of countries, over a user defined number of iterations. 

* See docstrings at the end of the program for my steps and references.
'''

# ----- Libraries ----- #

import csv # for reading file
import matplotlib.pyplot as plt # for plotting
import random  # for randomising initial centroids
from math import sqrt # for calculating square root

# ----- Functions ----- #

# Function to read, extract and convert data from a csv file.
def readCSV(file_name): 
    
    # Read the chosen CSV file into a list, then remove the first row of column labels.
    with open(file_name, 'r') as csv_db:
        data_list = list(csv.reader(csv_db, delimiter = ','))
        data_list.remove(data_list[0])

    # Extract and convert each row of data to return a list of the datapoints.
    extract_data = [[data[0], [float(data[1]), float(data[2])]] for data in data_list]    

    return extract_data

# Function to calculate the distance between two points.
def calcDistance(centroids, points): 

    # Calculate and return the distance between the two coordinates using the Euclidean formula: distance = sqr(((x1-x2)**2) + ((y1-y2)**2)))
    return sqrt((centroids[0] - points[0]) ** 2 + (centroids[1] - points[1]) ** 2)

# Function to assign datapoints to centroids based on their distance.
def assignCentroids(calcDistance, k, centroids, clusters, points): 
   
    # Initilaise list to store the distances from each point to each centroid.
    distances_list = []

    # Call function to calculate the distance from each point to each centroid.
    for centroid in range(k):
        distances_list.append(calcDistance(centroids[centroid], points))

    # Uncomment to see distances of each data point to each centroid.
    # print(f"\nDistance of data point {points} to:")
    # for num in range(k):
    #   print(f"centroid {num} at {round(centroids[num][0],2)}, {round(centroids[num][1],2)} = {round(distances_list[num],2)}")

    # Assign points to cluster with the centroid with the nearest(min) distance.
    for index, distance in enumerate(distances_list): 
        if distance == min(distances_list):
            clusters[index].append(points) 
            print(f"Data point {points} assigned to Centroid {index +1}")
    
# Function to calaculate the mean x and y data values for the new centroids.
def calcMean(cluster): 

    # Extract the x and y data in each each cluster.
    x_data = [point[0] for point in cluster]
    y_data = [point[1] for point in cluster]

     # Calculate and return the mean values for the centroids new x and y data.
    x_mean = (sum(x_data) / len(cluster))
    y_mean = (sum(y_data) / len(cluster))

    return [x_mean, y_mean]

# Function to print information of the data.
def printInfo(): 

    # Print the information for each cluster.
    for info in range(k):
        print(f"\n--- Cluster {info +1} Data ---")

        # Print the clusters centroids and assigned data points.
        print(f"\nCentroids: \nx({round(centroids[info][0], 2)}), y({round(centroids[info][1], 2)})")
        print(f"\nData points in cluster:\n{clusters[info]}")

        # Initialise list to store countries belonging to the cluster.
        countries = []
        for index, data in enumerate(database):
            # If the datapoints (at index 1) is in the cluster, add the country from the corresponding indexed database to the list.
            if data[1] in clusters[info]:
                countries.append(database[index][0])

        # Print the country info of each cluster.
        print(f"\nNumber of countries:\n{len(clusters[info])}")
        print(f"\nCountries in cluster:\n{countries}")

        # Print the birth rate and life expectancy of each cluster.
        print(f"\nBirth rate:\n{round(centroids[info][0], 2)}")
        print(f"\nLife expectancy:\n{round(centroids[info][1], 2)}\n")

# Function to plot the x,y data, centroids and labels on the chart.
def scatterPlot(): 

    # Plot the x and y data points in each cluster.
    for plots in clusters:
        x_data = [point[0] for point in plots]
        y_data = [point[1] for point in plots]
        plt.scatter(x_data, y_data, s = 10)

    # Plot the centroids x [0] and y [1] values for each k-amount of clusters.
    for plots in range(k):
        plt.scatter(centroids[plots][0], centroids[plots][1], 
        marker="+", s=100, c='black')

    # Plot the labels for the graph.
    plt.title("Birth Rate & Life Expectancy")
    plt.xlabel("Birth Rate")
    plt.ylabel("Life Expectancy")

    # Plot legend to identify cluster and centroids, based on number of k.
    plt.legend([("Cluster: "+ (str(cluster+1)), "Centroids: "+ str(round(centroids[cluster][0],2))+ ", " + str(round(centroids[cluster][1],2))) for cluster in range(k)], title = "Clusters & Centroids")

    # Plot and save an image of the graph.
    plt.savefig(f"BirthRate_LifeExpectancy.png")
    plt.show()

# --------------- MAIN --------------- # 
print(f"\n----- Birth Rate & Life Expectancy Clustering -----\n")

# ----- Initialise Inputs ----- #

# Prompt user for input to initalise dataset.
user_selection = (input('''Database:
1. data1953.csv
2. data2008.csv
3. dataBoth.csv

Enter the number of the file to use: ''' )) 

file_name = ""
if user_selection == "1":
    file_name = "data1953.csv"
elif user_selection == "2":
    file_name = "data2008.csv"
elif user_selection == "3":
    file_name  = "dataBoth.csv"

# Prompt user for input to initalise the number of clusters.
k = int(input("Enter the number of groups to cluster: "))

# ----- Initialise Procedure ----- #

# Read csv file and return list of data.
database = readCSV(file_name)

# Extract the x,y data points from the database.
data_points = [data[1] for data in database]

# Initalise number of iterations.
iterations = 6

# Randomly generate starting values of centroids.
centroids = random.sample(data_points, k)

# ----- Initialise Algorithm ----- #
for iteration in range(iterations):

    # Initilaise cluster list to store the closest point to each cluster.
    clusters = [[] for cluster in range(k)]

    # Call function to assign each data point to its nearest centroid.
    print(f"\n--- Assign data points for iteration {iteration +1} ---\n") 
    for points in data_points:
        assignCentroids(calcDistance, k, centroids, clusters, points)

    # Call function to compute the mean for the new centroids.
    print(f"\n--- Compute centroids for iteration {iteration +1} ---\n") 
    for cluster in range(k):
        centroids[cluster] = calcMean(clusters[cluster])
        
        print(f"New centroid {cluster +1} at {round(centroids[cluster][0],2)}, {round(centroids[cluster][1],2)}")

# ----- Display Results ----- #
#  
# Call function to print and plot cluster information.
print(f"\n----- Clustering Results -----")
printInfo() 
scatterPlot()

# ----- APPROACH ----- #
'''
--- K-means Clustering Task ---

Brief description of steps and how I implemented the clustering algo:

1.  Get user inputs and initialise global variables for the database to use and 
    the amount of clusters(k) to produce.
2.  Read CSV files to get the data.
        - use reader to use data directly into list
        - remove first line of column names to have raw data only
        - iterate through list to extract and convert each row of data into a 2d list with the countries as one element and the birth rate and life expectany (as float types) as the second element.
3.  Extract and store the x,y value pair from the data list at index [1].
        (Initial approach was to seperate the countries and data in step 2 but I reverted to having the key:value pairs in the original database for accessing corresponding countries later in step 6)
4.  Initialise the amount of iterations and randomly generate the starting set 
    of k-amount of centroids. 
        - use the random sample() function
5.  Once the inputs and procedure has been initialised, the k-mean algo begins 
    and repeats the following steps for the amount of iterations. 
    5.1.    To start, initilaise empty cluster list to store each cluster as it 
            is generated. (This is accessed in step 5.2 when assigning new centroids to the corresponding cluster list index. It's also accessed in step 5.3 when calculating the mean values of each datapoint in each cluster.)
    5.2.    Assign each data point to the centroid with the nearest distance to 
            form the associated clusters.
            - each data point, in the list of data points, is passed to the 'assignCentroids' function 
            - iterate through the number of clusters and pass the data points together with the centroids points to the 'calcDistance' function which calculates and returns the euclideam distance between each data point and the centroid
            - the distances, of the data point to each of the centroids, are appended to a list
            - enumerate the distances list to find the distance with the smallest/nearest value using the the min function, then append the data points(from the main iteration) to the cluster with the corresponding key.
    5.3     Once the initial centroids have been used, generate new points for 
            each centroid, of each cluster, that will be used for the next iteration.
            - new centroids are generated by calculating the centre position (mean value) of all the x and y coordinates for each datapoint in each cluster.
            - for each centroid, pass each clusters datapoints to the 'calcMean' function
            - for each x,y datapoint in the cluster, split the data pairs into x data values and y data values, then calculate the mean value of all the x and y data (sum/amount)  
            - the new x and y pair is returned as the values for the corresponding centroids
    5.4     As the algo iterates through each cluster, it reassigns each    
            datapoint to the new closest centroid of each cluster.
    5.5     Algo iteration stops when the amount of clusters initialied has    
            been met.
6.  Print the information requested.
    - iterate through number of clusters
    - enumerate the database list to check if the datapoints are present in the cluster that's being iterated through
    - add the country from the corresponding index to the list
    - use list of countries to print out info regarding countries
    - print the birth rate (the x value) and life expectancy (the y value) of the clusters centroid
7.  Plot the cluster information.
    - extract and plot all the x and y data points from each cluster
    - plot each of the centroids positions
    - add labels, legends and show diagram
'''

# ----- RESOURCES ----- #
'''
# For understanding of the k-mean algo: 
    # Rao, S. (2022) K-Means Clustering: Explain It To Me Like I’m 10. https://towardsdatascience.com/k-means-clustering-explain-it-to-me-like-im-10-e0badf10734a
    # Sharma, P. (2019) The Most Comprehensive Guide to K-Means Clustering You’ll Ever Need. https://www.analyticsvidhya.com/blog/2019/08/comprehensive-guide-k-means-clustering/#h2_10
    # Unfold Data Science. (2021) K Means Clustering in 15 Minutes | K means clustering explained | K means clustering in python. https://www.youtube.com/watch?v=m9UxVdXVYMs.
    # Singh, S. (2019) K-Means Clustering. https://medium.datadriveninvestor.com/k-means-clustering-b89d349e98e6
# For examples of the k-mean algo:
    # Haussmann, A. (2020) K-Means Clustering for Beginners. https://towardsdatascience.com/k-means-clustering-for-beginners-ea2256154109.
    # Bauscher, E. (2019) From Pseudocode to Python code: K-Means Clustering, from scratch. https://medium.com/analytics-vidhya/from-pseudocode-to-python-code-k-means-clustering-from-scratch-2e32aa469bef. Although this author used modules (numpy, pandas, seaborn) that I wasn't familar with it did however help me see the logical steps to take. So I had to interpret it to non-numpy language which was a learning curve. The author did some additional plot styling, which I didn't attempt, but it helped me add some final touches like the legend to my algo. I also gained understanding of how to assign the centroids when enumerating the distances liist.
    # Shmidkte, N. (2022) K-Means-clustering-from-scratch. https://github.com/Nadia-JSch/K-Means-clustering-from-scratch. This example resource helped guide me through the logic and development of my own approach to this algo. I believe my approach is a simpler solution as the author's approach resulted in extensive code that had to be repeated for both the x and y data, centroids, means etc instead of as a pair of datapoints. I studied the authors use of 'np.argim' and colour maps for plotting but couldn't get it to work for the different appraoch I took. '''

# ----- CHALLENGES ----- #
'''
# I couldn't figure out how to remove the brackets, apostrophies and commas from the plt.legend() function for a cleaner output.
# I researched the numpy method 'argmin' to get the smallest distance but couldn't figure out how to then assign the data points to them so I chose to rather loop through the distances and use the min() function.
# '''