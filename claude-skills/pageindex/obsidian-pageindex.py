#!/usr/bin/env python3
"""
Obsidian Vault RAG - Query with LiteLLM + Bedrock (or local fallback)
Usage: python vault-rag.py "Your question here"
"""
import sys
import os
from pathlib import Path
import subprocess

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import litellm

# Load AWS_BEARER_TOKEN_BEDROCK from ~/.zshrc
def load_bedrock_token():
    """Extract AWS_BEARER_TOKEN_BEDROCK from ~/.zshrc"""
    try:
        result = subprocess.run(
            ['bash', '-c', 'source ~/.zshrc && echo $AWS_BEARER_TOKEN_BEDROCK'],
            capture_output=True,
            text=True,
            timeout=5
        )
        token = result.stdout.strip()
        if token:
            return token
    except:
        pass
    return os.environ.get("AWS_BEARER_TOKEN_BEDROCK", "")

# Setup paths using environment variables
obsidian_path = os.environ.get("OBSIDIAN_PATH")
if not obsidian_path:
    raise ValueError(
        "OBSIDIAN_PATH environment variable not set.\n"
        "Set it to your Obsidian vault path, e.g.:\n"
        "export OBSIDIAN_PATH=\"$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianVault\"\n"
        "or equivalent for your system."
    )

vault_path = Path(obsidian_path).expanduser()
if not vault_path.exists():
    raise ValueError(f"Obsidian vault path does not exist: {vault_path}")

db_path = vault_path / "rag-vectorstore"
if not db_path.exists():
    raise ValueError(f"Vector store not found at: {db_path}")

# Load embeddings and vector store
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.load_local(str(db_path / "index"), embeddings, allow_dangerous_deserialization=True)

def query_rag(question: str, k: int = 5, use_bedrock: bool = True):
    """
    Query the RAG system.

    Args:
        question: Your question
        k: Number of context chunks to retrieve
        use_bedrock: Use Bedrock (True) or fallback to summary (False)
    """
    print(f"\n🔍 Searching vault for: {question}")
    print("-" * 60)

    # Retrieve relevant chunks
    results = vectorstore.similarity_search(question, k=k)

    # Build context
    context = "\n".join([
        f"[{doc.metadata.get('source', 'Unknown')}]\n{doc.page_content[:500]}..."
        for doc in results
    ])

    if not use_bedrock:
        # Fallback: just show context and ask user to reason
        print("\n📄 Relevant context from your vault:\n")
        for doc in results:
            print(f"From: {doc.metadata.get('source', 'Unknown')}")
            print(f"Content: {doc.page_content[:200]}...\n")
        return {
            "answer": "Context retrieved. Use above to reason about your question.",
            "sources": [doc.metadata.get('source', 'Unknown') for doc in results[:3]]
        }

    # Try Bedrock via boto3
    prompt = f"""You are an AI assistant analyzing an Obsidian vault.

Context from vault:
{context}

Question: {question}

Provide a clear, concise answer based on the context."""

    try:
        import json
        import boto3

        # Create Bedrock client using vault-bedrock profile
        session = boto3.Session(profile_name='vault-bedrock')
        bedrock = session.client('bedrock-runtime', region_name='us-east-1')

        # Invoke Claude Sonnet 4.6 via cross-region inference profile
        response = bedrock.invoke_model(
            modelId='us.anthropic.claude-sonnet-4-6',
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 500,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7
            })
        )

        # Parse response
        response_body = json.loads(response['body'].read())
        answer = response_body['content'][0]['text']

        return {
            "answer": answer,
            "sources": [doc.metadata.get('source', 'Unknown') for doc in results[:3]]
        }
    except Exception as e:
        print(f"\n⚠️  Bedrock error: {str(e)[:100]}")
        print("Falling back to context retrieval...\n")
        return query_rag(question, k, use_bedrock=False)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Interactive mode
        print("Obsidian Vault RAG - Ask questions about your notes")
        print("="*60)
        while True:
            q = input("\n❓ Question (or 'quit'): ").strip()
            if q.lower() == 'quit':
                break
            result = query_rag(q)
            print(f"\n✅ Answer:\n{result['answer']}")
            print("\n📄 Sources:")
            for src in result['sources']:
                print(f"  • {src}")
    else:
        # Command line mode
        question = " ".join(sys.argv[1:])
        result = query_rag(question)
        print(f"\n✅ Answer:\n{result['answer']}")
        print("\n📄 Sources:")
        for src in result['sources']:
            print(f"  • {src}")
