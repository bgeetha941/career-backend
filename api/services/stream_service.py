import json
import os

class StreamService:
    def __init__(self):
        # Path relative to where main.py is run
        self.streams_file = 'backend/data/streams.json'
        # Fallback to local path if running from backend dir
        if not os.path.exists(self.streams_file):
             self.streams_file = 'data/streams.json'
             
        self.load_data()
    
    def load_data(self):
        """Load streams and job roles data"""
        try:
            with open(self.streams_file, 'r', encoding='utf-8') as f:
                self.streams = json.load(f)
        except Exception as e:
            print(f"Error loading streams data: {e}")
            self.streams = []
    
    def get_all_streams(self):
        """Get all main streams"""
        self.load_data() # Reload for dev/demo purposes so json edits reflect immediately
        return self.streams
    
    def get_stream_by_id(self, stream_id):
        """Get stream by ID"""
        for stream in self.streams:
            if stream['id'] == stream_id:
                return stream
        return None
    
    def get_sub_streams(self, stream_id):
        """Get all sub-streams for a main stream"""
        stream = self.get_stream_by_id(stream_id)
        if not stream:
            return None
        return stream.get('sub_streams', [])
    
    def get_sub_stream_details(self, stream_id, sub_stream_id):
        """Get detailed information about a sub-stream"""
        stream = self.get_stream_by_id(stream_id)
        if not stream:
            return None
        
        for sub_stream in stream.get('sub_streams', []):
            if sub_stream['id'] == sub_stream_id:
                return sub_stream
        
        return None
