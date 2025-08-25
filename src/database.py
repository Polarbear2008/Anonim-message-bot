import secrets
import string
from typing import Optional, Dict, Any
from supabase import create_client, Client
from config_reader import config

class Database:
    def __init__(self):
        self._supabase = None
    
    @property
    def supabase(self) -> Client:
        if self._supabase is None:
            # Lazy initialization - only connect when needed
            self._supabase = create_client(
                config.SUPABASE_URL.get_secret_value(),
                config.SUPABASE_SERVICE_KEY.get_secret_value()
            )
        return self._supabase
    
    def generate_unique_code(self) -> str:
        """Generate a unique code for anonymous links"""
        return ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(12))
    
    async def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        response = self.supabase.table('users').select('*').eq('id', user_id).execute()
        return response.data[0] if response.data else None
    
    async def get_user_by_code(self, code: str) -> Optional[Dict[str, Any]]:
        """Get user by their unique code"""
        response = self.supabase.table('users').select('*').eq('unique_code', code).execute()
        return response.data[0] if response.data else None
    
    async def create_user(self, user_id: int) -> Dict[str, Any]:
        """Create a new user with unique code"""
        unique_code = self.generate_unique_code()
        
        # Ensure code is unique
        while await self.get_user_by_code(unique_code):
            unique_code = self.generate_unique_code()
        
        user_data = {
            'id': user_id,
            'unique_code': unique_code,
            'message_count': 0
        }
        response = self.supabase.table('users').insert(user_data).execute()
        return response.data[0] if response.data else None
    
    async def update_user(self, user_id: int, **updates) -> Dict[str, Any]:
        """Update user data"""
        response = self.supabase.table('users').update(updates).eq('id', user_id).execute()
        return response.data[0] if response.data else None
    
    async def increment_message_count(self, user_id: int) -> None:
        """Increment message count for user"""
        user = await self.get_user(user_id)
        if user:
            await self.update_user(user_id, message_count=user['message_count'] + 1)
    
    async def create_message_record(self, sender_id: int, receiver_id: int, bot_message_id: int, sender_username: str = None) -> None:
        """Store message record for reply functionality"""
        message_data = {
            'sender_id': sender_id,
            'receiver_id': receiver_id,
            'bot_message_id': bot_message_id,
            'sender_username': sender_username,
            'created_at': 'now()'
        }
        self.supabase.table('message_records').insert(message_data).execute()
    
    async def get_original_sender(self, bot_message_id: int) -> Optional[int]:
        """Get original sender ID from bot message ID"""
        response = self.supabase.table('message_records').select('sender_id').eq('bot_message_id', bot_message_id).execute()
        return response.data[0]['sender_id'] if response.data else None
    
    async def get_message_info(self, bot_message_id: int) -> Optional[dict]:
        """Get full message information including sender, receiver, and username"""
        response = self.supabase.table('message_records').select('*').eq('bot_message_id', bot_message_id).execute()
        return response.data[0] if response.data else None

# Create a singleton instance
db = Database()
