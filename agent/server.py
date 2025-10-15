from fastapi import FastAPI
from pydantic import BaseModel
from langchain.chat_models import ChatOpenAI
import subprocess
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

class Request(BaseModel):
    prompt: str
    k8s_version: str = "v1.34"

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

def validate_yaml(yaml_str: str):
    process = subprocess.Popen(
        ["kubectl", "apply", "--dry-run=server", "-f", "-"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    out, err = process.communicate(input=yaml_str)
    return process.returncode == 0, out or err

@app.post("/generate")
def generate(req: Request):
    prompt = f"""
    You are a Kubernetes expert (version {req.k8s_version}).
    Generate a valid YAML manifest for this request:
    {req.prompt}

    Rules:
    - Only output YAML, no explanations.
    - Must follow Kubernetes OpenAPI schema.
    - Include metadata, spec, and required fields.
    """
    resp = llm.invoke(prompt)
    yaml_text = resp.content.strip()
    valid, result = validate_yaml(yaml_text)
    return {"valid": valid, "output": yaml_text, "validation": result}
