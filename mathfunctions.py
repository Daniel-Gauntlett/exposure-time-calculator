def interpolate(interplist, guideline):
    # interplist a list of ordered pairs (tuples)
    # guideline a list of numbers
    # interpolates the graph described by interplist at the x values in guideline, providing an interpolated function
    output = []
    currentguideline = 0
    currentinterp = 0
    while currentinterp < len(interplist) and currentguideline < len(guideline):
        if guideline[currentguideline] == interplist[currentinterp][0]:
            output.append(interplist[currentinterp])
            currentguideline = currentguideline + 1
        elif guideline[currentguideline] < interplist[currentinterp][0] and currentinterp > 0:
            proportion = (guideline[currentguideline] - interplist[currentinterp - 1][0]) / (interplist[currentinterp][0] - interplist[currentinterp - 1][0])
            newy = interplist[currentinterp][1] + ((interplist[currentinterp][1] - interplist[currentinterp - 1][1]) * proportion)
            output.append((guideline[currentguideline], newy))
            currentguideline = currentguideline + 1
        currentinterp = currentinterp + 1
    return output

def integrate(list, lowbound, highbound):
    # integrates the list between the bounds
    # traverses the list one at a time, checking if within bounds.
    total = 0
    for i in range(len(list) - 1):
        width = min(highbound, list[i+1][0]) - max(lowbound, list[i][0])
        if list[i][0] >= lowbound and list[i][0] <= highbound:
            if list[i+1][0] >= highbound:
                interpedbound = ((width / (list[i+1][0] - list[i][0])) * (list[i+1][1] - list[i][1])) + list[i][1]
                total = total + width * (list[i][1] + interpedbound) / 2.0
            else:
                total = total + width * (list[i][1] + list[i+1][1]) / 2.0
        elif list[i][1] >= lowbound and list[i][1] <= highbound:
            interpedbound = ((width / (list[i+1][0] - list[i][0])) * (list[i+1][1] - list[i][1])) + list[i][1]
            total = total + width * ((list[i][1] + interpedbound) / 2.0)
    return total