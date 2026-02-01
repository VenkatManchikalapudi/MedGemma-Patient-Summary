# MedGemma Patient Summary

## Overview
MedGemma Patient Summary is a modular system designed to process and summarize patient data using a combination of structured data, text, and images. The system integrates a router, database, and decision-making agent to provide a seamless flow of information.

## Features
- **UI**: A Flask-based user interface running on port 5000 for querying patient data.
- **Router**: A modular router running on port 7000 to handle requests and determine the appropriate processing modality.
- **Agent**: A decision-making agent running on port 8000 to process data and provide insights.
- **Database**: SQLite database for storing and querying patient data.

## System Flow
The system flow is represented in the [flow_diagram.md](flow_diagram.md) file using a Mermaid diagram.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd MedGemma\ Patient\ Summary
   ```
3. Set up the virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Start the router and agent:
   ```bash
   source .venv/bin/activate
   (cd multi-modal-agent && PYTHONPATH=$(pwd) python3.11 src/router.py &)
   (cd multi-modal-agent && PYTHONPATH=$(pwd) python3.11 src/agent.py &)
   ```
2. Access the UI at [http://localhost:5000](http://localhost:5000).

## Contributing
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-branch
   ```
5. Open a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.