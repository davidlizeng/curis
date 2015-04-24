import codecs

def printEntities():
    infile = codecs.open('csv/dblpusers.csv', 'r', 'utf-8')
    outfile = codecs.open('csv/entities.csv', 'w', 'utf-8')
    lines = infile.read().splitlines()
    entities = set()
    for line in lines:
        tokens = line.split('||')
        email = ''
        if tokens[3] != '':
            email = tokens[3][tokens[3].index('@') + 1:]
        aff = tokens[4]
        entities.add((email, aff))
    infile.close()
    for entity in entities:
        outfile.write(entity[0] + '|' + entity[1] + '\n')
    outfile.close()

def writeEntitites():
    afffile = codecs.open('csv/affiliations.tsv', 'r', 'utf-8')
    missfile = codecs.open('csv/missingentities.tsv', 'r', 'utf-8')
    usersfile = codecs.open('csv/dblpusers.csv', 'r', 'utf-8')
    outfile = codecs.open('csv/dblpusersaff.csv', 'w', 'utf-8')
    lines = afffile.read().splitlines()
    entities = {}
    for line in lines:
        tokens = line.split('\t')
        entities[(tokens[0], tokens[1])] = tokens[2:5]
    missingentities = {}
    lines = missfile.read().splitlines()
    for line in lines:
        tokens = line.split('\t')
        missingentities[tokens[0]] = tokens[4:7]
    lines = usersfile.read().splitlines()
    for line in lines:
        tokens = line.split('||')
        email = ''
        if tokens[3] != '':
            email = tokens[3][tokens[3].index('@') + 1:]
        aff = tokens[4]
        key = (email, aff)
        if key in entities:
            tokens[4] = entities[key][0]
            outfile.write('||'.join(tokens) + '||' + '||'.join(entities[key][1:3]) + '\n')
        elif tokens[0] in missingentities:
            tokens[4] = missingentities[tokens[0]][0]
            outfile.write('||'.join(tokens) + '||' + '||'.join(missingentities[tokens[0]][1:3]) + '\n')
        else:
            print tokens[0], 'uhoh'
    afffile.close()
    missfile.close()
    usersfile.close()
    outfile.close()

def getMissingEntities():
    infile = codecs.open('csv/dblpusersaff.csv', 'r', 'utf-8')
    outfile = codecs.open('csv/missingentities.csv', 'w', 'utf-8')
    lines = infile.read().splitlines()
    for line in lines:
        tokens = line.split('||')
        if tokens[4] == '':
            outfile.write('|'.join(tokens[0:4]) + '\n')
    outfile.close()
    infile.close()
