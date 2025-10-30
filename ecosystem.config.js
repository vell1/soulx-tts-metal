module.exports = {
  apps: [
    {
      name: "soulx-tts",
      script: "uvicorn",
      args: "app:app --host 0.0.0.0 --port 8000",
      interpreter: "none",
      autorestart: true,
      watch: false,
      max_memory_restart: "4G",
      env: { PYTHONUNBUFFERED: "1" }
    }
  ]
}