
def rewriteDistanceCsv():
    infile = open('csv/.distances6.csv', 'r')
    outfile = open('csv/distances6.csv', 'w')
    lastUser = ''
    for line in infile.read().splitlines():
        tokens = line.split('||')
        if lastUser == tokens[0]:
            outfile.write('||' + tokens[1] + '||' + tokens[2])
        else:
            lastUser = tokens[0]
            outfile.write('\n' + line)
    outfile.write('\n')
    outfile.close()
    infile.close()

