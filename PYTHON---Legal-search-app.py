from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
import os

# Define the schema for the index
schema = Schema(title=TEXT(stored=True), content=TEXT, path=ID(stored=True))

# Create an index directory
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")

# Create the index
ix = create_in("indexdir", schema)

# Add documents to the index
writer = ix.writer()
writer.add_document(title="Case 1: Roe v. Wade",
                    content="The U.S. Supreme Court case Roe v. Wade dealt with abortion rights.",
                    path="/legal/case1.txt")
writer.add_document(title="Statute: GDPR",
                    content="The General Data Protection Regulation governs data privacy in the EU.",
                    path="/legal/gdpr.txt")
writer.commit()

# Search function
def search_query(query_str):
    ix = create_in("indexdir", schema)
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(query_str)
        results = searcher.search(query)
        for result in results:
            print(f"Title: {result['title']}")
            print(f"Path: {result['path']}")
            print("-" * 40)

# User input for search
if __name__ == "__main__":
    query_str = input("Enter your search query: ")
    search_query(query_str)
