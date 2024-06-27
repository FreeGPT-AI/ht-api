from .chat import router as chat
from .home import router as home
from .images import router as images
from .models import router as models
from .embeddings import router as embeddings
from .moderation import router as moderation
from .tts import router as tts
from .transcriptions import router as transcriptions

routers = [
    chat,
    home,
    images,
    models,
    embeddings,
    moderation,
    tts,
    transcriptions
]