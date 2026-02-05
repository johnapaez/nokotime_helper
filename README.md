# Noko Time Helper

An application to automate the generation of Noko time import files based on weekly project percentage breakdowns.

## Quick Links

- 📚 **[Full Documentation](docs/README.md)** - Comprehensive technical documentation
- 📖 **[Documentation Guide](docs/DocumentationGuide.md)** - Standards for documenting this project
- 🚀 **Quick Start** - See below

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

### 3. Set Weekly Percentages
- For each week with work days, enter the percentage of time spent on each project
- For each project, select a **Tag** from the dropdown:
  - `development` - Feature development work
  - `productionsupport` - Production support and maintenance
  - `QA` - Quality assurance and testing
  - `other` - Administrative or miscellaneous work
- Add a custom **Description** in the text field for each project entry
- The total percentage for each week is displayed with color coding:
  - **Green**: Exactly 100% (perfect!)
  - **Yellow**: Less than 100% (partial week or time off)
  - **Red**: Over 100% (needs adjustment)
- **Note**: Weeks with 0 work days are automatically excluded from the breakdown

### 2. Add Time Off/Special Days
- **For 2026**: Holidays automatically load when you select a month
- Review pre-loaded holidays and adjust hours if needed
- Click "Add Time Off Entry" for additional time off (sick days, vacation, etc.)
- Enter the date, hours, and description
- **Tag**: All time-off entries automatically use the "other" tag
- **Description**: Free text from your input field
- These will automatically generate appropriate time entries in the CSV

### 4. Generate CSV
- Click "Generate CSV File" to create your Noko import file
- The file will automatically download to your computer
- Import this CSV directly into Noko

### 5. Save/Load Profiles (Optional)
- **Save Profile**: Enter a profile name and click "Save Profile" to save your current configuration
- **Load Profile**: Select a saved profile from the dropdown and click "Load Profile"
- Profiles save all data: project allocations, tags, descriptions, and time-off entries

## Project Configuration

The application loads projects from `noko_projects.csv`. Projects are categorized as:

### CapEx Projects (Capital Expenditures)
Development projects and new initiatives

### OpEx Projects (Operating Expenditures)
Operational support and maintenance work

### Special Categories
- **Time-Off (OOO)** - Holidays, sick days, vacation (automatically tagged as "other")

**Note**: Project tags and descriptions are set per-entry in the UI using dropdowns and text fields, not in the CSV configuration file.

## Customizing Projects

Projects are loaded from `noko_projects.csv` with the following columns:

- **Project Name** - Display name of the project
- **Project Group/Client Name** - CapEx Projects, OpEx Projects, or custom client name
- **Billable** - "yes" or "no"
- **Notes** - Optional notes (for reference, not used in time entries)

To add or modify projects, edit the `noko_projects.csv` file and restart the application.

**Important**: Tags and descriptions are NOT configured in the CSV. They are set per time entry using the UI dropdowns and text fields during weekly allocation.

## Features

### Smart Calculations
- **Automatic Time Conversion**: Percentages are automatically converted to hours and minutes
- **8-Hour Standard Day**: Based on 480 minutes per workday
- **Weekend Detection**: Automatically skips Saturdays and Sundays
- **Partial Week Handling**: Handles months that start/end mid-week
- **Zero-Day Week Filtering**: Weeks with no work days are excluded and week numbers are adjusted accordingly
- **Holiday Integration**: Pre-loaded 2026 US holidays automatically appear for the selected month

### User-Friendly Interface
- **Visual Percentage Tracking**: See totals in real-time with color coding
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Error Prevention**: Input validation and helpful warnings
- **One-Click Export**: Direct CSV download ready for Noko import

### Flexible Time Management
- **Weekly Breakdown**: Enter different percentages for each week
- **Time Off Support**: Easy handling of holidays and sick days with automatic "other" tag
- **Custom Tags**: Select from development, productionsupport, QA, or other per project entry
- **Custom Descriptions**: Free-text descriptions for each project entry
- **Copy Week**: Copy previous week's allocations (including tags and descriptions)
- **Profile Management**: Save and load configurations for reuse

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
- Edit `noko_projects.csv` to add custom projects
- Restart the application after changes

**CSV format issues:**
- Verify your Noko import settings match the generated format
- Check that all required fields are present

## Files Structure

```
nokotime_helper/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── noko_projects.csv     # Project configuration (primary source)
├── projects.json         # Fallback project configuration
├── templates/
│   └── index.html        # Web interface
├── profiles/             # Saved user profiles
│   └── *.json
├── docs/
│   ├── README.md         # Technical documentation
│   └── DocumentationGuide.md  # Documentation standards
└── README.md             # This file
```

## Support & Customization

This application is designed to match your existing workflow while automating the tedious parts. 

For detailed technical documentation, API references, and architecture details, see **[docs/README.md](docs/README.md)**.

If you need to:
- Add new projects → Edit `noko_projects.csv`
- Change user information → Modify `load_projects_from_csv()` in `app.py`
- Adjust the interface → Edit `templates/index.html`
- Add new features → See [Documentation Guide](docs/DocumentationGuide.md) for standards

The application is built with Python Flask, making it easy to customize and extend.

---

## Documentation

- 📚 **[Technical Documentation](docs/README.md)** - Full technical reference
- 📖 **[Documentation Guide](docs/DocumentationGuide.md)** - Standards for documenting changes

---

**Ready to save hours of manual work each month? Start the application and generate your first automated Noko import file!**