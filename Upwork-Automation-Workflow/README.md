# Upwork Automation Workflow

## Overview
Automated n8n workflow that fetches Upwork jobs, scores them using AI (OpenAI GPT-4o), and stores qualified leads in Airtable with priority classification.

## Features
-  AI-powered job scoring (1-10 scale)
-  Priority classification (High/Medium/Low)
-  Automated data collection every 8 hours
-  High-priority job alerts
-  Structured storage in Airtable

## Tech Stack
- **n8n** - Workflow automation
- **OpenAI GPT-4o** - AI job scoring
- **Airtable** - Data storage
- **Docker** - Containerization

## Setup Instructions

### Prerequisites
- Docker Desktop installed
- OpenAI API account with credits
- Airtable account
- Apify account (optional)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/not2511/Projects
cd Upwork-Automation-Workflow
```

2. **Start n8n with Docker:**
```bash
docker run -d --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n n8nio/n8n
```

3. **Access n8n:**
Open browser to `http://localhost:5678`

4. **Import workflow:**
- Click menu (three dots) → Import from File
- Select `workflows/Upwork-Automation-Enhanced.json`

5. **Configure credentials:**
Create a `.env` file (see `.env.example`) with:
```env
APIFY_API_TOKEN=your_apify_token
OPENAI_API_KEY=your_openai_key
AIRTABLE_TOKEN=your_airtable_token
AIRTABLE_BASE_ID=your_base_id
```

6. **Set up credentials in n8n:**
- OpenAI: Add API key in OpenAI Chat Model node
- Airtable: Add Personal Access Token in Create Record node

## Workflow Architecture
```
Schedule Trigger (Every 8 hours)
    ↓
Mock Data Generation (Code Node)
    ↓
Edit Fields (Data Formatting)
    ↓
Analyse Job (OpenAI Scoring)
    ↓
Structured Output Parser
    ↓
IF (Priority Check)
    ├─ TRUE (High Priority) → Set Alert → Create Record
    └─ FALSE (Medium/Low) → Create Record
```

## Issues Fixed During Development

### 1. Apify Actor Trial Limitation
**Problem:** Apify actor required paid subscription after trial period  
**Solution:** Implemented mock data generation for demonstration purposes

### 2. Airtable Field Name Mismatch
**Problem:** Field names in workflow didn't match Airtable schema  
**Solution:** Standardized field names to match Airtable exactly

### 3. Score Data Type Error
**Problem:** AI returned score as "8/10" (string) but Airtable expected number  
**Solution:** Updated JSON schema and prompt to return numeric values (1-10)

## Enhancements Implemented

### 1. High-Priority Job Alerts
- Added IF node to detect high-priority jobs (score ≥ 8)
- Set node creates alert record with job details
- Easily extensible to Slack/Email notifications

### 2. Mock Data for Testing
- Created realistic test data for development
- Demonstrates full workflow without API dependencies
- Easy to replace with live Apify integration

## Future Improvements

1. **Production Scraping:** Replace mock data with working Apify actor or alternative scraper
2. **Real-time Notifications:** Add Slack/Email integration for instant alerts
3. **Budget Filtering:** Pre-filter jobs by budget range before AI scoring
4. **Duplicate Detection:** Prevent re-processing of already scored jobs
5. **Analytics Dashboard:** Create visualization of job trends and scoring patterns
6. **Multi-platform Support:** Extend to Freelancer, Fiverr, etc.

## Sample Output

The workflow processes jobs and outputs structured data to Airtable:

| Job Title | Score | Priority | Reasoning |
|-----------|-------|----------|-----------|
| n8n Automation Expert Needed | 9 | High | Explicitly mentions n8n and workflow automation |
| WordPress Website Design | 3 | Low | No automation components mentioned |
| AI Chatbot with Twilio | 8 | High | Requires Twilio and conversational AI expertise |

## Usage

### Manual Execution
Click "Execute workflow" in n8n interface

### Scheduled Execution
Workflow automatically runs every 8 hours via Schedule Trigger

### Viewing Results
Check your Airtable base for new job entries with scores and priorities

## Project Structure
```
upwork-automation-workflow/
├── workflows/
│   └── Upwork-Automation-Enhanced.json
├── docs/
│   ├── setup-guide.md
│   └── report.md
├── config/
│   └── credentials-template.json
├── .env.example
├── .gitignore
└── README.md
```

## Contributing
This is an assignment project, but feedback is welcome!

## License
MIT

## Contact
[Ranjot Singh] - [ranjotsingh2511@yahoo.com]