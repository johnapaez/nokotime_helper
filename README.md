# Noko Time Helper

An application to automate the generation of Noko time import files based on weekly project percentage breakdowns.

## Overview

This tool helps automate the monthly time tracking process by generating CSV files suitable for importing into Noko, based on simple weekly percentage allocations across different projects.

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Application**
   ```bash
   python app.py
   ```

3. **Open Your Browser**
   Navigate to: `http://localhost:5000`

## How to Use

### 1. Select Month/Year
- Choose the target month and year from the dropdown menus
- Click "Load Month" to see the weekly breakdown

### 2. Set Weekly Percentages
- For each week, enter the percentage of time spent on each project
- The total percentage for each week is displayed with color coding:
  - **Green**: Exactly 100% (perfect!)
  - **Yellow**: Less than 100% (partial week or time off)
  - **Red**: Over 100% (needs adjustment)

### 3. Add Time Off (Optional)
- Click "Add Time Off Entry" for holidays, sick days, etc.
- Enter the date, hours, and optional description
- These will automatically generate appropriate time entries

### 4. Generate CSV
- Click "Generate CSV File" to create your Noko import file
- The file will automatically download to your computer
- Import this CSV directly into Noko

## Project Configuration

The application comes pre-configured with your standard projects based on the provided CSV data:

### CapEx Projects (Development)
- **Cinesys+ (C+)** - development work
- **GCP Migration** - cloud migration tasks
- **Google Safety Tracker (GST)** - development work
- **Linear IQ (LIQ)** - development work
- **Mindwave (Mw)** - translation discussions

### OpEx Projects (Operations)
- **Administration** - admin meetings & tasks
- **General Support (IT)** - production support
- **NRG Website** - production support
- **Syndicate Tracking Product (STP)** - API discussions

### Special Categories
- **Time-Off (OOO)** - holidays, sick days, etc.

## Customizing Projects

You can modify the project configuration by editing the `projects.json` file:

```json
{
  "user_info": {
    "name": "Your Name",
    "teams": "Your Team",
    "email": "your.email@company.com"
  },
  "projects": {
    "project_key": {
      "name": "Project Display Name",
      "group_client": "CapEx Projects or OpEx Projects",
      "description": "Default description for time entries",
      "tags": "development, productionsupport, other, or blank",
      "billable": "yes or no"
    }
  }
}
```

## Features

### Smart Calculations
- **Automatic Time Conversion**: Percentages are automatically converted to hours and minutes
- **8-Hour Standard Day**: Based on 480 minutes per workday (matches your current system)
- **Weekend Detection**: Automatically skips Saturdays and Sundays
- **Partial Week Handling**: Handles months that start/end mid-week

### User-Friendly Interface
- **Visual Percentage Tracking**: See totals in real-time with color coding
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Error Prevention**: Input validation and helpful warnings
- **One-Click Export**: Direct CSV download ready for Noko import

### Flexible Time Management
- **Weekly Breakdown**: Enter different percentages for each week
- **Time Off Support**: Easy handling of holidays and sick days
- **Custom Descriptions**: Override default descriptions when needed
- **Project Categories**: Maintains CapEx/OpEx classification

## Output Format

The generated CSV includes all required Noko columns:
- Date, Person, Teams, Email
- Group/Client, Project, Minutes, Hours
- Tags, Description, Billable status
- Invoice tracking fields (Invoiced, Paid, Approved, etc.)

## Benefits Over Manual Process

1. **Speed**: Generate entire month in seconds vs. hours of manual work
2. **Accuracy**: Eliminates calculation errors and copy/paste mistakes
3. **Consistency**: Standardized project information and formatting
4. **Flexibility**: Easy to adjust percentages and handle varying weeks
5. **Maintainability**: Simple to add/modify projects and configurations

## Troubleshooting

### Common Issues

**Application won't start:**
- Ensure Python 3.7+ is installed
- Run `pip install -r requirements.txt`
- Check for port conflicts (default: 5000)

**Percentages don't add to 100%:**
- This is okay for partial weeks or time-off days
- Yellow warning helps identify intentional vs. accidental discrepancies

**Missing projects:**
- Edit `projects.json` to add custom projects
- Restart the application after changes

**CSV format issues:**
- Verify your Noko import settings match the generated format
- Check that all required fields are present

## Files Structure

```
nokotime_helper/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── projects.json         # Project configuration
├── templates/
│   └── index.html        # Web interface
├── README.md             # This file
├── may-noko-final.csv    # Example output format
└── 2025 Helper Worksheet for Noko.xlsx  # Original template
```

## Support & Customization

This application is designed to match your existing workflow while automating the tedious parts. If you need to:

- Add new projects
- Change time allocations
- Modify user information
- Adjust the interface

Simply edit the `projects.json` file or modify the code as needed. The application is built with Python Flask, making it easy to customize and extend.

---

**Ready to save hours of manual work each month? Start the application and generate your first automated Noko import file!**