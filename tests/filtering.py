from queryexpander.query_filter import QueryFilter

if __name__ == '__main__':
    path = "QUERIES"
    query_filter = QueryFilter(path)

    print('Similarity')
    for query in query_filter.similarity_filter(0.15):
        print(query)

    print('Mesh')
    for query in query_filter.mesh_filter('/home/rivi/meshSynonyms.xml'):
        print(query)
