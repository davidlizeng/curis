import xml.etree.ElementTree as et
import sys
import snap
import codecs

distances = {}

def xmlScrape():
    authorsDict = {}
    graph = snap.TNEANet.New()
    used = ['article', 'inproceedings', 'proceedings', 'book', 'incollection', 'phdthesis', 'mastersthesis', 'www', 'author']

    for event, elem in et.iterparse('/lfs/local/0/dzeng0/dblp/rep-dblp.xml', events=('start', 'end')):
        if event == 'end':
            if elem.tag not in used:
                elem.clear()
            elif elem.tag != 'author':
                authors = elem.findall('author')
                for author in authors:
                    name = author.text.encode('utf-8')
                    if name not in authorsDict:
                        id = graph.AddNode(-1)
                        authorsDict[name] = id
                        graph.AddStrAttrDatN(id, name, 'name')
                        graph.AddIntAttrDatN(id, 0, 'exp')
                    id = authorsDict[name]
                    graph.AddIntAttrDatN(id, graph.GetIntAttrDatN(id, 'exp') + 1, 'exp')
                for a1 in authors:
                    n1 = a1.text.encode('utf-8')
                    i1 = authorsDict[n1]
                    for a2 in authors:
                        n2 = a2.text.encode('utf-8')
                        i2 = authorsDict[n2]
                        if not graph.IsEdge(i1, i2) and i1 != i2:
                            eid = graph.AddEdge(i1, i2)
                            eid = graph.AddEdge(i2, i1)

                print elem.get('key'), len(authors)
                sys.stdout.flush()
                elem.clear()
    fout = snap.TFOut('coauthor.graph')
    graph.Save(fout)
    fout.Flush()
