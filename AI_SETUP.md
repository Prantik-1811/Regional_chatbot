# 🧠 AI Model Setup & Management

This guide explains how to manage the Local AI (Ollama) component of the chatbot deployment.

## 1. Quick Start (Run Once)

After starting your Docker containers, you **MUST** download the AI model. The container starts empty to keep the image size small.

```bash
# Pull the Llama 3.2 model (approx 2GB)
docker exec chatbot-ollama ollama pull llama3.2
```

> [!IMPORTANT]
> The chatbot will **NOT** generate summaries until you run this command. It will only show source links.

## 2. Verifying the Model

Check if the model is loaded and ready:

```bash
# List installed models
docker exec chatbot-ollama ollama list

# Test the model directly (CLI)
docker exec chatbot-ollama ollama run llama3.2 "Hello, are you working?"
```

## 3. Performance Tuning

### CPU Mode (Default)
- **Pros**: Works on any server (AWS t3.xlarge, DigitalOcean Droplet).
- **Cons**: Slow. Responses take 30-90 seconds.
- **Note**: Nginx is configured with a `300s` timeout to handle this.

### GPU Mode (Recommended for Production)
If your server has an NVIDIA GPU (e.g., AWS `g4dn.xlarge`), enable GPU support for 10x faster responses.

1. **Install NVIDIA Container Toolkit** on your host server.
2. **Edit `docker-compose.yml`**:
   Uncomment the `deploy` section under the `ollama` service:

   ```yaml
   # deploy:
   #   resources:
   #     reservations:
   #       devices:
   #         - driver: nvidia
   #           count: 1
   #           capabilities: [gpu]
   ```
3. **Restart**:
   ```bash
   docker-compose up -d
   ```

## 4. Using Different Models

You can swap `llama3.2` for other models (e.g., `mistral`, `gemma`).

1. **Pull the new model**:
   ```bash
   docker exec chatbot-ollama ollama pull mistral
   ```

2. **Update Backend**:
   Edit `backend/rag.py` line 20 to change the model name:
   ```python
   self.llm = ChatOllama(model="mistral", ...)
   ```

3. **Rebuild Backend**:
   ```bash
   docker-compose build backend
   docker-compose up -d backend
   ```
