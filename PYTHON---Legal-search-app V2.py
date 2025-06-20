from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
import os

# Define the schema for the index
schema = Schema(title=TEXT(stored=True), content=TEXT, path=ID(stored=True))

# Create the index directory and index if not already present
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")
    ix = create_in("indexdir", schema)
else:
    ix = open_dir("indexdir")

# Add initial documents
def add_sample_docs():
    writer = ix.writer()
    writer.add_document(title="Case 1: Roe v. Wade",
                        content="The U.S. Supreme Court case Roe v. Wade dealt with abortion rights.",
                        path="/legal/case1.txt")
    writer.add_document(title="Statute: GDPR",
                        content="The General Data Protection Regulation governs data privacy in the EU.",
                        path="/legal/gdpr.txt")
    writer.commit()

# Search function with result score
def search_query(query_str):
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(query_str)
        results = searcher.search(query)
        print(f"\n🔍 {len(results)} result(s) found for: \"{query_str}\"\n")
        for result in results:
            print(f"📄 Title: {result['title']}")
            print(f"📂 Path: {result['path']}")
            print(f"📈 Score: {result.score:.2f}")
            print("-" * 40)

# List all documents
def list_documents():
    with ix.searcher() as searcher:
        results = searcher.documents()
        print("\n📚 All indexed documents:\n")
        for doc in results:
            print(f"- {doc['title']} ({doc['path']})")

# Delete a document by title
def delete_document(title):
    writer = ix.writer()
    writer.delete_by_term("title", title)
    writer.commit()
    print(f"🗑️ Deleted document with title: '{title}'")

# Reindex from a list of documents
def reindex_documents(documents):
    writer = ix.writer()
    writer.mergetype = writing.CLEAR  # Clears previous index
    for doc in documents:
        writer.add_document(**doc)
    writer.commit()
    print("🔁 Reindexed documents.")

# CLI Menu
if __name__ == "__main__":
    if not os.listdir("indexdir"):
        add_sample_docs()

    while True:
        print("\n⚖️ Legal Document Search App Menu:")
        print("1. Search documents")
        print("2. List all documents")
        print("3. Delete a document by title")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            query_str = input("Enter your search query: ")
            search_query(query_str)
        elif choice == "2":
            list_documents()
        elif choice == "3":
            title = input("Enter the title of the document to delete: ")
            delete_document(title)
        elif choice == "4":
            print("👋 Exiting. Stay legally curious!")
            break
        else:
            print("❌ Invalid choice. Try again.")
