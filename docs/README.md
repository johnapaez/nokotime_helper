# Noko Time Helper - Documentation

**Project**: Noko Time Helper  
**Last Updated**: 2026-02-05

---

## Quick Links

- [Main Application README](../README.md) - Setup and basic usage
- [Documentation Guide](DocumentationGuide.md) - Standards for documenting this project
- [CSV Export Format Quick Reference](CSV-Export-QuickReference.md) - Noko CSV format details
- [Technical Architecture](#technical-architecture)
- [Feature Details](#feature-details)

---

## Overview

The Noko Time Helper is a Flask-based web application that automates the generation of time-tracking CSV files for import into the Noko time-tracking system. It intelligently manages project time allocation, holiday tracking, and time-off management across weekly work periods.

---

## Technical Architecture

### System Components

**Backend**: Python Flask application (`app.py`)
- RESTful API endpoints for month info, project management, and CSV generation
- CSV parsing for project configuration
- Date/time calculation logic for work weeks and holidays
- Profile saving/loading functionality

**Frontend**: Single-page application (`templates/index.html`)
- Vanilla JavaScript (no frameworks)
- Dynamic UI generation for weekly breakdowns
- Client-side validation and data collection
- Responsive CSS with gradient styling

**Data Storage**:
- `noko_projects.csv` - Project configuration source
- `projects.json` - Fallback project configuration
- `profiles/*.json` - Saved user profiles

### Key Technologies

- **Python 3.x** - Backend runtime
- **Flask** - Web framework
- **CSV/JSON** - Data formats
- **HTML/CSS/JavaScript** - Frontend stack

---

## Feature Details

### Core Features

#### 1. Intelligent Week Calculation
- Automatically calculates work weeks for any month
- Filters out weeks with zero work days
- Handles month boundaries correctly
- Sequential week numbering (only counts weeks with work days)

**Technical Details**: See `get_month_weeks()` function in `app.py`

#### 2. Holiday Management
- Pre-loaded US holidays for 2026
- Automatic filtering by selected month
- Manual time-off entry support
- Hours calculation accounts for holidays

**Technical Details**: See `/api/us-holidays-2026` endpoint and `loadHolidaysForMonth()` in JavaScript

#### 3. Project Allocation
- Percentage-based time allocation per week
- Custom tags (development, productionsupport, QA, other)
- Free-text descriptions per project entry
- Copy previous week functionality
- Real-time percentage validation

**Technical Details**: See `addProjectToWeek()` and `generateCSV()` JavaScript functions

#### 4. Profile Management
- Save current month configuration
- Load previously saved profiles
- Stores all data: projects, percentages, tags, descriptions, time-off

**Technical Details**: See `/api/save-profile` and `/api/load-profile` endpoints

#### 5. CSV Export
- Noko-compatible format
- Automatic rounding and hour adjustments
- Tag formatting (removes leading "#")
- Time-off entries with "other" tag
- Per-project metadata (tags and descriptions)

**Technical Details**: See `calculate_time_entries()` and `/api/generate` endpoint

---

## API Reference

### Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/projects` | GET | Get project configuration |
| `/api/month-info/<year>/<month>` | GET | Get weeks and work days for month |
| `/api/us-holidays-2026` | GET | Get US holidays for 2026 |
| `/api/generate` | POST | Generate CSV file |
| `/api/save-profile` | POST | Save current configuration |
| `/api/load-profile/<filename>` | GET | Load saved profile |
| `/api/list-profiles` | GET | List all saved profiles |

### Data Structures

#### Month Info Response
```json
{
  "weeks": [
    {
      "week_number": 1,
      "start_date": "2026-02-02",
      "end_date": "2026-02-08",
      "work_days": 5
    }
  ],
  "total_days": 28,
  "month_name": "February"
}
```

#### CSV Generation Request
```json
{
  "year": 2026,
  "month": 2,
  "weekly_data": {
    "week_1": {
      "project_key": 50.0
    }
  },
  "time_off_data": {
    "2026-02-16": {
      "hours": 8,
      "description": "Presidents' Day"
    }
  },
  "project_metadata": {
    "week_1_project_key": {
      "tags": "development",
      "description": "Feature work"
    }
  }
}
```

---

## Configuration

### Project Configuration

Projects are loaded from `noko_projects.csv` with the following columns:
- `Project Name` - Display name
- `Project Group/Client Name` - Client/group classification
- `Billable` - yes/no
- `Notes` - Optional notes (not used in default config)

### User Configuration

User information is hardcoded in `load_projects_from_csv()`:
- Name: John Paez
- Teams: Full-Time Employees, Software Engineering
- Email: john.paez@nrgmr.com

---

## Development Workflow

### Adding New Projects
1. Update `noko_projects.csv` with new project details
2. Restart the application
3. Projects will be loaded automatically

### Modifying Holidays
- Edit the `holidays` dictionary in `/api/us-holidays-2026` endpoint
- Format: `'YYYY-MM-DD': {'hours': 8, 'description': 'Holiday Name'}`

### Testing
1. Start the application: `python app.py`
2. Navigate to `http://localhost:5000`
3. Select a month and test the workflow
4. Verify CSV output format

---

## Common Patterns

### Tag Management
- **Time-off entries**: Always use "other" tag
- **Project entries**: User-selectable (development, productionsupport, QA, other)
- **CSV Export**: Tags exported without "#" prefix

### Description Handling
- Time-off: From user input in time-off section
- Projects: From user input in project metadata fields
- Empty descriptions are allowed

### Week Numbering Logic
1. Calculate all weeks that overlap with target month
2. Count work days (Mon-Fri) in each week
3. Filter out weeks with 0 work days
4. Renumber sequentially starting from 1

---

## Troubleshooting

### Issue: Empty week sections
**Cause**: Month has weeks with no work days  
**Solution**: This is expected behavior - weeks with 0 work days are automatically filtered

### Issue: Percentages don't add to 100%
**Cause**: User input error  
**Solution**: UI displays running total - adjust project percentages

### Issue: Projects not loading
**Cause**: CSV file missing or malformed  
**Solution**: Check `noko_projects.csv` exists and has proper format

---

## File Structure

```
nokotime_helper/
├── app.py                      # Flask application
├── requirements.txt            # Python dependencies
├── noko_projects.csv          # Project configuration
├── projects.json              # Fallback config
├── README.md                  # Main documentation
├── docs/
│   ├── README.md              # This file
│   └── DocumentationGuide.md  # Documentation standards
├── templates/
│   └── index.html             # Frontend UI
└── profiles/                  # Saved user profiles
    └── *.json
```

---

## Related Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Noko API Documentation](https://developer.nokotime.com/)
- [Python datetime module](https://docs.python.org/3/library/datetime.html)

---

## Contributing

When making changes to this application:

1. **Read** the [Documentation Guide](DocumentationGuide.md)
2. **Test** your changes thoroughly
3. **Document** session work following guide templates
4. **Update** this README if adding major features
5. **Validate** CSV output format

---

## Next Steps / Future Enhancements

- 🔲 Support for multiple years (currently hardcoded to 2026)
- 🔲 Dynamic holiday loading from external API
- 🔲 User configuration UI (vs hardcoded values)
- 🔲 Week preview before CSV generation
- 🔲 CSV import for editing existing entries
- 🔲 Multi-user support
- 🔲 Database storage instead of JSON files

---

**For Questions**: Refer to inline code comments in `app.py` and `index.html` for implementation details.
