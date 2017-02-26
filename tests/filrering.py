from dataloader.queryFilter import QueryFilter

if __name__ == '__main__':
    path = "queries.txt"
    queryFilter = QueryFilter(path)
    queryFilter.similarity_filter(0.15)
