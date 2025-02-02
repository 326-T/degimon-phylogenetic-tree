# デジモンの進化検索アプリ

## How to use

### Python

```bash
$ sudo apt-get update
$ sudo apt-get install graphviz fonts-noto-cjk
$ pip install -r requirements.txt
$ fastapi dev app/main.py --port 8080
```

### Docker

```bash
$ docker build -t digimon:latest .
$ docker run -d -p 8080:80 digimon:latest
```
