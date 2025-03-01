# Farm Manager Utility Scripts

## Overview
This directory contains utility scripts to help manage and set up the Farm Manager project.

## Scripts

### `setup_environment.sh`
Sets up the development environment for the Farm Manager project.

#### Usage
```bash
./setup_environment.sh
```

#### Features
- Creates a virtual environment
- Installs project dependencies
- Sets up initial data directories
- Initializes configuration files

### `populate_knowledge_base.py`
Populates the knowledge base with initial data from JSON files.

#### Usage
```bash
python populate_knowledge_base.py
```

#### Features
- Loads climate data
- Adds crop knowledge
- Imports agricultural practices
- Imports agricultural regulations

### `generate_sample_data.py`
Generates sample data for testing and development.

#### Usage
```bash
python generate_sample_data.py
```

#### Features
- Generates sample machinery data
- Creates sample personnel records
- Produces usage logs
- Generates climate data for multiple regions
- Creates crop-specific information

## Prerequisites
- Python 3.8+
- Virtual environment activated
- Project dependencies installed

## Recommended Workflow
1. Run `setup_environment.sh` to prepare the development environment
2. Use `generate_sample_data.py` to create test data
3. Run `populate_knowledge_base.py` to load data into the knowledge base
