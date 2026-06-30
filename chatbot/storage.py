from .conversation_storage import ConversationStorage

def load_conversation(save_file): 
    return ConversationStorage(save_file).load_conversation()
        
def save_conversation(messages, save_file):
    ConversationStorage(save_file).save_conversation(messages)