
## Installation 
- Install Ollama : https://ollama.com/
- Intall llama3.2:3b
``` bash
    Ollama pull llama3.2:3b
```
- Install Python Dependensi
```bash
    pip install -r requirements.txt
```
- Run Program
```bash
    python main.py
```

====

- Jika Run Di Server
```bash
    docker-compose up -d
```

- Hapus file vectordb
```bash
    docker exec -it ollama rm -rf ./data/vector_db 
```

- Restart
- Setelah itu pull llm yang dibutkan
```bash
    docker exec -it ollama ollama pull llama3.2:1b
```