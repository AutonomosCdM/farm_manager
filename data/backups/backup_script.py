#!/usr/bin/env python3
import os
import shutil
from datetime import datetime
import json

def load_backup_config():
    with open('data/knowledge_base/config.json', 'r') as f:
        config = json.load(f)
    return config

def create_backup():
    config = load_backup_config()
    backup_dir = 'data/backups'
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Backup knowledge base
    knowledge_base_path = os.path.join('data/knowledge_base', config.get('database_path', 'chroma.sqlite3'))
    backup_knowledge_base_path = os.path.join(backup_dir, f'knowledge_base_{timestamp}.sqlite3')
    shutil.copy2(knowledge_base_path, backup_knowledge_base_path)
    
    # Backup resources
    resources_backup_path = os.path.join(backup_dir, f'resources_{timestamp}')
    shutil.copytree('data/resources', resources_backup_path)
    
    # Rotate backups
    max_backup_count = config.get('max_backup_count', 7)
    backups = sorted([
        os.path.join(backup_dir, f) for f in os.listdir(backup_dir) 
        if f.startswith('knowledge_base_') or f.startswith('resources_')
    ])
    
    while len(backups) > max_backup_count:
        oldest_backup = backups.pop(0)
        if os.path.isdir(oldest_backup):
            shutil.rmtree(oldest_backup)
        else:
            os.remove(oldest_backup)

if __name__ == '__main__':
    create_backup()
