import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise ValueError("Credenciais do Supabase não encontradas no .env")

# Cliente instanciado pras rotas
supabase: Client = create_client(url, key)
