import json
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

def main():
    data = json.load(open("data/openapi.json"))
    definitions = data.get("definitions", {})
    docs = []
    for name, schema in definitions.items():
        desc = schema.get("description", "")
        fields = list(schema.get("properties", {}).keys())
        text = f"{name}\nDescription: {desc}\nFields: {', '.join(fields)}"
        docs.append(text)

    embeddings = OpenAIEmbeddings()
    Chroma.from_texts(docs, embedding=embeddings, persist_directory="data/chroma")
    print(f"✅ Indexed {len(docs)} Kubernetes API definitions.")

if __name__ == "__main__":
    main()
