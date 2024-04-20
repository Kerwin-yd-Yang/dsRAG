from abc import ABC, abstractmethod
import os
import pickle

class ChunkDB(ABC):
    @abstractmethod
    def add_document(self, doc_id: str, chunks: dict[dict]):
        """
        Store all chunks for a given document.
        """
        pass

    @abstractmethod
    def remove_document(self, doc_id: str):
        """
        Remove all chunks and metadata associated with a given document ID.
        """
        pass

    @abstractmethod
    def get_chunk_text(self, doc_id: str, chunk_index: int) -> dict:
        """
        Retrieve a specific chunk from a given document ID.
        """
        pass

    @abstractmethod
    def get_chunk_header(self, doc_id: str, chunk_index: int) -> str:
        """
        Retrieve the header of a specific chunk from a given document ID.
        """
        pass


class BasicChunkDB(ChunkDB):
    """
    This is a basic implementation of a ChunkDB that stores chunks in a nested dictionary and persists them to disk by pickling the dictionary.
    """
    def __init__(self, kb_id: str, storage_directory: str = '~/spRAG'):
        self.storage_directory = os.path.expanduser(storage_directory)  # Expand the user path
        # Ensure the base directory and the chunk storage directory exist
        os.makedirs(os.path.join(self.storage_directory, 'chunk_storage'), exist_ok=True)
        self.storage_path = os.path.join(self.storage_directory, 'chunk_storage', f'{kb_id}.pkl')
        self.load()

    def add_document(self, doc_id: str, chunks: dict[dict]):
        self.data[doc_id] = chunks
        self.save()

    def remove_document(self, doc_id: str):
        self.data.pop(doc_id, None)
        self.save()

    def get_chunk_text(self, doc_id: str, chunk_index: int) -> str:
        if doc_id in self.data and chunk_index in self.data[doc_id]:
            return self.data[doc_id][chunk_index]['chunk_text']
        return None

    def get_chunk_header(self, doc_id: str, chunk_index: int) -> str:
        if doc_id in self.data and chunk_index in self.data[doc_id]:
            return self.data[doc_id][chunk_index]['chunk_header']
        return None

    def load(self):
        try:
            with open(self.storage_path, 'rb') as f:
                self.data = pickle.load(f)
        except FileNotFoundError:
            self.data = {}

    def save(self):
        with open(self.storage_path, 'wb') as f:
            pickle.dump(self.data, f)