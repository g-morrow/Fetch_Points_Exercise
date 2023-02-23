import sys
import csv

def processArgs():
    '''
    Processes user command line input, ensuring that it exists and assigns values to global variables.
    @param none
    @return 1. points_spent: amount of points to spend, 2. csv_filename: name of CSV file
    '''
    if (len(sys.argv) >= 3) :
        points_spent = int(sys.argv[1])
        csv_filename = sys.argv[2]
    else:
        raise Exception('Command Line Error: Please run with 2 command line args; 1. points spent, 2. csv filename.')
    return points_spent, csv_filename

def readCSV(csv_filename):
    '''
    Reads CSV file and saves data in a dictionary. Returns if the filename doesn't exist or the file is empty.
    @param csv_filename: name of CSV file
    @return data: dictionary of data extracted from the CSV file
    '''
    data = {}
    try:
        with open(csv_filename) as csv_file:
            csv_data = csv.reader(csv_file)
            headers = next(csv_data)
            for row in csv_data:
                data[row[2]] = {headers[0]: row[0], headers[1]: row[1]} 
    except FileNotFoundError as e:
        print('CSV Error:', csv_filename, 'does not exist. Please make sure it is in the correct folder.')
    except: 
        print('CSV Error:', csv_filename, 'is empty.')
    return data

def pointCalculations(points_spent, data):
    '''
    Sorts data by timestamp (dict key) and extracts points from the oldest transactions.
    @param 1. points_spent: amount of points to spend, 2. data: dictionary of data extracted from the CSV file
    @return output: dictionary of remaining point values
    '''
    output = {}
    keys = list(data.keys())
    keys.sort()
    data = {i: data[i] for i in keys}                                   
    for row in data:
        entry_points = int(data[row]['points'])
        if (points_spent != 0 and points_spent - entry_points > 0):    
            points_spent -= entry_points
            data[row]['points'] = 0
        if (points_spent != 0 and points_spent - entry_points <= 0): 
            data[row]['points'] = entry_points - points_spent
            points_spent = 0
        try: 
            output[data[row]['payer']] += int(data[row]['points'])
        except:
            output[data[row]['payer']] = int(data[row]['points'])
    if (points_spent > 0):
        print('Points Spent Error: Customer spending more points than available.')
    return output

if __name__ == "__main__":
    points_spent, csv_filename = processArgs()
    data = readCSV(csv_filename)
    print(pointCalculations(points_spent, data))