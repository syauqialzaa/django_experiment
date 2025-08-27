import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ.get("URL")
SUPABASE_KEY = os.environ.get("KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
db = supabase.schema("public")