from dataloader.queryFilter import QueryFilter

if __name__ == '__main__':
    path = "queries.txt"
    queryFilter = QueryFilter(path)

    print('start')
    for query in queryFilter.queriesWords:
        print(query)

    queryFilter.similarity_filter(0.15)

    print('Similarity')
    for query in queryFilter.queriesWords:
        print(query)

    queryFilter.mesh_filter('meshSynonyms.xml')
    print('Mesh')
    for query in queryFilter.queriesWords:
        print(query)
