def makeDotR(filename):
    with open(filename, 'r') as f:
        data = f.readlines()

    # TODO : Header needs to be formatted
    header = data[0:3]

    # Put data in nested list while preserving column structure - use tab as delimiter in split()
    '''
        >> dataArray[0]
        ['01', '0000', '-2.7', '966.5', '', '', '30.2', '153', '', '', '', '', '63.4', '-8.7', 
        '', '', '', '', '', '', '', '', '', '', '', '', '', '', '12.7', 'AO1', '\n']
    '''
    dataArray = [line.split('\t') for line in data[6:]]

    # List of days in data
    dayList = [*set(line[0] for line in dataArray)]
    dayList.sort()

    # Create arbitrary list of hour/minute data points
    hourList = [n for n in range(24)]
    tenMinuteList = [n * 10 for n in range(6)]

    # Generate dictionary containing one key per hour/minute data point
    # This is where the data will go
    dailyIntervals = {}
    for hourlyInterval in hourList:
        for minuteInterval in tenMinuteList:
            dailyIntervals[(str(hourlyInterval).rjust(2, '0') + str(minuteInterval).rjust(2, '0'))] = []    # rjust() adds leading zeroes to hr/min

    # Create nested dictionaries: one key per date containing one key per hour/minute
    # We will then store existing data points as values for hour/minute
    # E.g. dataDict[01][1100] == 11 AM on the first day of the month
    '''
            dataDict = {
                {day} : {
                    {interval}: [data],
                    {interval2}: [data],
                    ...
                },
                {day2} : {
                    {interval}: [data],
                    ...
                }
            }
    '''
    dataDict = {}
    for day in dayList:
        dataDict[day] = dailyIntervals.copy()

    # Iterate through dataArray; assign each line to respective point in dataDict using date/time
    for line in dataArray:
        dataDict[line[0]][line[1]] = line[2:30]

    # Iterate through dataDict; assign emptyLine to empty datapoints
    emptyLine = ['444.0', '444.0', '', '', '444.0', '444.0', '', '', '', '', '444.0', '444.0', 
                '', '', '', '', '', '', '', '', '', '', '', '', '', '', '444.0', '']
    for day in dataDict.keys():
        for datapoint in dataDict[day].keys():
            if dataDict[day][datapoint] == []:
                dataDict[day][datapoint] = emptyLine

    # Print dataDict to new .r file
    with open(filename+'.r', 'w') as f:
        month = filename[-8:-6]     # Extract month from filename
        f.writelines(header)
        for day in dayList:
            for interval in dailyIntervals.keys():
                thisDatapoint = dataDict[day][interval]

                # .r = month + day + temp + pressure + windspeed + wind direction + rel humidit
                # right justify: ----0----0--000.0--000.0--000.0--000.0 ('-' are whitespace)
                formattedLine = month.rjust(5, ' ') + day.rjust(5, ' ') + thisDatapoint[0].rjust(7, ' ') + thisDatapoint[1].rjust(7, ' ') + thisDatapoint[4].rjust(7, ' ') + thisDatapoint[5].rjust(7, ' ') + thisDatapoint[10].rjust(7, ' ')

                f.write(formattedLine + '\n')