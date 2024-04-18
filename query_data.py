import argparse
from dataclasses import dataclass
from langchain.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Path where the Chroma vector store data will be saved
CHROMA_PATH = "chroma"

# Template for constructing the prompt sent to the language model
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def main():
    # Initialize the command line interface parser.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text  # Extract the query text from command line arguments

    # Initialize embeddings using OpenAI's model and set up the Chroma database for vector storage.
    embedding_function = OpenAIEmbeddings()  # Create an instance of OpenAIEmbeddings for use in Chroma
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)  # Create a Chroma instance with specified persistence directory and embedding function

    # Conduct a similarity search in the Chroma database with the query text to find relevant documents.
    results = db.similarity_search_with_relevance_scores(query_text, k=3)  # Perform a similarity search to retrieve top 3 similar documents
    if len(results) == 0 or results[0][1] < 0.7:  # Check if no results were found or if the top result has a relevance score less than 0.7
        print("Unable to find matching results.")
        return

    # Create a context string by joining contents of the retrieved documents.
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])  # Concatenate page contents separated by a divider

    # Create a prompt for the language model using the found context and the original query.
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)  # Initialize a ChatPromptTemplate with the defined template
    prompt = prompt_template.format(context=context_text, question=query_text)  # Format the template with the actual context and question
    print(prompt)  # Print the constructed prompt

    # Initialize the language model and predict the answer based on the constructed prompt.
    model = ChatOpenAI()  # Initialize the ChatOpenAI model
    response_text = model.predict(prompt)  # Use the model to generate a response based on the prompt

    # Gather sources of the documents returned by the search.
    sources = [doc.metadata.get("source", None) for doc, _score in results]  # Retrieve the source metadata from each document
    formatted_response = f"Response: {response_text}\nSources: {sources}"  # Format the response and the sources for output
    print(formatted_response)  # Print the final formatted response

if __name__ == "__main__":
    main()

