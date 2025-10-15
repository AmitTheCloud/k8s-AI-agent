import requests, json, subprocess
from pathlib import Path

OUT = Path("data/openapi.json")
OUT.parent.mkdir(parents=True, exist_ok=True)
REMOTE_URL = "https://raw.githubusercontent.com/kubernetes/kubernetes/master/api/openapi-spec/swagger.json"

def fetch_from_cluster():
    try:
        data = subprocess.check_output(["kubectl", "get", "--raw", "/openapi/v2"], text=True)
        return json.loads(data)
    except Exception:
        return None

def fetch_from_remote():
    r = requests.get(REMOTE_URL, timeout=30)
    r.raise_for_status()
    return r.json()

def main():
    data = fetch_from_cluster() or fetch_from_remote()
    OUT.write_text(json.dumps(data, indent=2))
    print(f"✅ Saved OpenAPI schema → {OUT}")

if __name__ == "__main__":
    main()
