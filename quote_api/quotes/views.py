from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
import random

quotes = [
    {"quote": "All of us do not have equal talent. But, all of us have an equal opportunity to develop our talents. - A. P. J. Abdul Kalam"},
    {"quote": "All the world's a stage, and all the men and women merely players. - William Shakespeare"},
    {"quote": "Be kind, for everyone you meet is fighting a hard battle. - Plato"},
    {"quote": "It is during our darkest moments that we must focus to see the light. - Aristotle Onassis"},
    {"quote": "Spread love everywhere you go. Let no one ever come to you without leaving happier. - Mother Teresa"},
    {"quote": "Don't let your happiness depend on something you may lose. - C.S.Lewis"},
    {"quote": "We are all broken, that's how the light gets in. - Ernest Hemingway"},
    {"quote": "To produce a mighty book, you must choose a mighty theme. - Herman Melville"},
    {"quote": "The Six Golden Rules of Writing: Read, read, read, and write, write, write. - Ernest Gaines"},
    {"quote": "Trust our heart if the seas catch fire, live by love though the stars walk backwards. - E. E. Cummings"},
    {"quote": "'If I waited for perfection, I would never write a word. - Margaret Atwood"},
    {"quote": "We are what we repeatedly do. Excellence, then, is not an act, but a habit.- Aristotle"},
    {"quote": "A good writer possesses not only his own spirit but also the spirit of his friends. - Friedrich Nietzsche"},
    {"quote": "In your name, the family name is at last because it's the family name that lasts. - Amit Kalantri"},
    {"quote": "That's the thing about books. They let you travel without moving your feet. -Jhumpa Lahiri"},
    {"quote": "If you want to leave your footprints on the sands of time, do not drag your feet. -A. P. J. Abdul Kalam"},


    
]

@extend_schema(responses={"200": dict})
def get_random_quote(request):
    quote = random.choice(quotes)
    return JsonResponse(quote)