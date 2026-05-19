from fastapi import FastAPI, Request
import json

app = FastAPI()

@app.post("/webhook")
async def receive_signal(request: Request):
    data = await request.json()
    # Save the signal to a file so Streamlit can read it
    with open("last_signal.json", "w") as f:
        json.dump(data, f)
    print(f"Signal received: {data}")
    return {"status": "success"}
    