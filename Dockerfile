FROM python:3.9-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y openvpn
RUN openvpn --config outline.ovpn

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
