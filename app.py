#!/usr/bin/env python3
"""
Noko Time Helper - Web Application
Generates Noko time import files from weekly project percentage breakdowns.
"""

from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime, timedelta
import calendar
import csv
import json
import io
import os

app = Flask(__name__)

# Load project configuration
def load_projects():
    """Load project configuration from CSV file"""
    try:
        # First try to load from CSV
        projects_dict = load_projects_from_csv()
        if projects_dict:
            return projects_dict
    except Exception as e:
        print(f"Error loading from CSV: {e}")
    
    # Fall back to JSON if CSV fails
    try:
        with open('projects.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return default configuration if file doesn't exist
        return get_default_projects()

def load_projects_from_csv():
    """Load projects from noko_projects.csv"""
    import csv
    
    user_info = {
        "name": "John Paez",
        "teams": "Full-Time Employees, Software Engineering",
        "email": "john.paez@nrgmr.com"
    }
    
    projects = {}
    
    try:
        with open('noko_projects.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                project_name = row['Project Name']
                group_client = row['Project Group/Client Name']
                billable = row['Billable']
                notes = row.get('Notes', '').strip()
                
                # Create a key from the project name (lowercase, replace spaces with underscores)
                project_key = project_name.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_').replace('+', 'plus').replace('-', '_')
                
                # Clean up project key
                project_key = ''.join(c if c.isalnum() or c == '_' else '_' for c in project_key)
                project_key = '_'.join(filter(None, project_key.split('_')))  # Remove consecutive underscores
                
                projects[project_key] = {
                    "name": project_name,
                    "group_client": group_client if group_client else "",
                    "description": notes if notes else "",
                    "tags": "",  # Will be set by user in UI
                    "billable": billable
                }
        
        return {
            "user_info": user_info,
            "projects": projects
        }
    except FileNotFoundError:
        return None

def get_default_projects():
    """Default project configuration based on CSV analysis"""
    return {
        "user_info": {
            "name": "John Paez",
            "teams": "Full-Time Employees, Software Engineering", 
            "email": "john.paez@nrgmr.com"
        },
        "projects": {
            "administration": {
                "name": "Administration",
                "group_client": "OpEx Projects",
                "description": "Admin Meetings & Tasks",
                "tags": "",
                "billable": "yes"
            },
            "cinesys_plus": {
                "name": "Cinesys+ (C+)",
                "group_client": "CapEx Projects", 
                "description": "",
                "tags": "",
                "billable": "yes"
            },
            "gcp_migration": {
                "name": "GCP Migration",
                "group_client": "CapEx Projects",
                "description": "GCP Tasks/Meetings with SADA", 
                "tags": "",
                "billable": "yes"
            },
            "general_support": {
                "name": "General Support (IT)",
                "group_client": "OpEx Projects",
                "description": "",
                "tags": "",
                "billable": "yes"
            },
            "google_safety_tracker": {
                "name": "Google Safety Tracker (GST)",
                "group_client": "CapEx Projects",
                "description": "",
                "tags": "",
                "billable": "yes"
            },
            "linear_iq": {
                "name": "Linear IQ (LIQ)", 
                "group_client": "CapEx Projects",
                "description": "",
                "tags": "",
                "billable": "yes"
            },
            "mindwave": {
                "name": "Mindwave (Mw)",
                "group_client": "CapEx Projects", 
                "description": "Mindwave Translations discussion",
                "tags": "",
                "billable": "yes"
            },
            "nrg_website": {
                "name": "NRG Website",
                "group_client": "OpEx Projects",
                "description": "",
                "tags": "",
                "billable": "yes"
            },
            "syndicate_tracking": {
                "name": "Syndicate Tracking Product (STP)",
                "group_client": "OpEx Projects", 
                "description": "",
                "tags": "",
                "billable": "yes"
            },
            "time_off": {
                "name": "Time-Off (OOO)",
                "group_client": "",
                "description": "",
                "tags": "other", 
                "billable": "yes"
            }
        }
    }

def save_projects(projects_data):
    """Save project configuration to JSON file"""
    with open('projects.json', 'w') as f:
        json.dump(projects_data, f, indent=2)

def get_month_weeks(year, month):
    """Get list of week starting dates for a given month"""
    # Get first day of month
    first_day = datetime(year, month, 1)
    
    # Find the first Monday of the month (or before if month starts mid-week)
    days_since_monday = first_day.weekday()
    first_monday = first_day - timedelta(days=days_since_monday)
    
    # Get last day of month
    if month == 12:
        last_day = datetime(year, 12, 31)
    else:
        last_day = datetime(year, month + 1, 1) - timedelta(days=1)
    
    # Get all Monday dates for weeks that contain days from this month
    weeks = []
    current_monday = first_monday
    
    # Continue adding weeks while the week's Sunday (6 days after Monday) 
    # is before or equal to the last day of the month
    while current_monday <= last_day:
        # Add this week if it contains at least one day from the target month
        week_end = current_monday + timedelta(days=6)
        # Check if this week overlaps with the target month
        if current_monday <= last_day and week_end >= first_day:
            weeks.append(current_monday)
        current_monday += timedelta(days=7)
    
    return weeks

def calculate_time_entries(year, month, weekly_data, time_off_data, projects_config, project_metadata=None):
    """Calculate time entries for the entire month"""
    if project_metadata is None:
        project_metadata = {}
    
    entries = []
    user_info = projects_config['user_info']
    projects = projects_config['projects']
    
    # Get the last business day of each week that falls within the target month
    weeks = get_month_weeks(year, month)
    week_registration_days = []
    
    for week_index, week_start in enumerate(weeks):
        # Find the last business day of this week that's in our target month
        for day_offset in range(6, -1, -1):  # Start from Saturday, work backwards
            check_date = week_start + timedelta(days=day_offset)
            
            # If this day is in our target month and is a weekday (Mon-Fri)
            if (check_date.month == month and 
                check_date.year == year and 
                check_date.weekday() < 5):  # Monday=0, Friday=4
                
                week_registration_days.append((check_date, week_index))
                break  # Found the last business day for this week
    
    print(f"Week registration days: {[d[0].strftime('%Y-%m-%d') for d in week_registration_days]}")
    
    for current_date, week_index in week_registration_days:
        date_str = current_date.strftime('%Y-%m-%d')
            
        # Add time off entry if present (but don't skip project processing)
        if date_str in time_off_data:
            time_off_info = time_off_data[date_str]
            project_info = projects['time_off_ooo']
            
            entry = {
                'Date': date_str,
                'Person': user_info['name'],
                'Teams': user_info['teams'],
                'Email': user_info['email'],
                'Group/Client': project_info['group_client'],
                'Project': project_info['name'],
                'Minutes': int(time_off_info['hours'] * 60),
                'Hours': time_off_info['hours'],
                'Tags': 'other',  # Time off uses 'other' tag
                'Description': time_off_info.get('description', project_info.get('description', '')),
                'Billable': project_info['billable'],
                'Invoiced': 'no',
                'Invoice Reference': '',
                'Paid': 'no', 
                'Approved': 'no',
                'Approved By': ''
            }
            entries.append(entry)
            # Continue to process project time for this day as well
        
        if f"week_{week_index + 1}" not in weekly_data:
            continue
            
        week_data = weekly_data[f"week_{week_index + 1}"]
        
        # Calculate available work hours for this week (accounting for time off)
        week_start = weeks[week_index]
        week_work_hours = 0
        for day_offset in range(7):
            check_date = week_start + timedelta(days=day_offset)
            check_date_str = check_date.strftime('%Y-%m-%d')
            
            # If it's a weekday in our target month
            if (check_date.month == month and 
                check_date.year == year and 
                check_date.weekday() < 5):  # Monday=0, Friday=4
                
                if check_date_str in time_off_data:
                    # Subtract time off hours
                    week_work_hours += (8 - time_off_data[check_date_str]['hours'])
                else:
                    # Full 8-hour day
                    week_work_hours += 8
        
        # Generate entries for each project with time allocated
        # First, calculate all raw hours and round them
        project_hours = []
        total_rounded_hours = 0
        
        for project_key, percentage in week_data.items():
            if percentage <= 0:
                continue
                
            if project_key not in projects:
                print(f"Warning: Project key '{project_key}' not found in projects config")
                continue
                
            # Calculate raw hours and round them
            raw_hours = (percentage / 100.0) * week_work_hours
            rounded_hours = round(raw_hours * 2) / 2
            
            project_hours.append({
                'project_key': project_key,
                'raw_hours': raw_hours,
                'rounded_hours': rounded_hours,
                'percentage': percentage
            })
            total_rounded_hours += rounded_hours
        
        # Calculate the difference and adjust the largest project
        hours_difference = week_work_hours - total_rounded_hours
        
        if abs(hours_difference) >= 0.5 and project_hours:
            # Find the project with the largest raw hours (most impactful to adjust)
            largest_project = max(project_hours, key=lambda x: x['raw_hours'])
            
            # Adjust in 0.5-hour increments toward the correct total
            adjustment_increments = int(hours_difference / 0.5)
            adjustment = adjustment_increments * 0.5
            
            largest_project['rounded_hours'] += adjustment
            
            # Ensure we don't go negative
            if largest_project['rounded_hours'] < 0:
                largest_project['rounded_hours'] = 0
            
            print(f"Adjusted {largest_project['project_key']} by {adjustment} hours to match weekly total of {week_work_hours}")
        
        # Create entries with the final adjusted hours
        for project_data in project_hours:
            project_key = project_data['project_key']
            hours = project_data['rounded_hours']
            
            if hours <= 0:
                continue
                
            project_info = projects[project_key]
            minutes = int(hours * 60)
            
            # Get custom tags and description from metadata if provided
            week_key = f"week_{week_index + 1}"
            metadata_key = f"{week_key}_{project_key}"
            custom_tags = ""
            custom_description = ""
            
            if metadata_key in project_metadata:
                custom_tags = project_metadata[metadata_key].get('tags', '')
                custom_description = project_metadata[metadata_key].get('description', '')
            
            # Remove leading # from tags if present
            if custom_tags and custom_tags.startswith('#'):
                custom_tags = custom_tags[1:]
            
            entry = {
                'Date': date_str,
                'Person': user_info['name'], 
                'Teams': user_info['teams'],
                'Email': user_info['email'],
                'Group/Client': project_info['group_client'],
                'Project': project_info['name'],
                'Minutes': minutes,
                'Hours': hours,
                'Tags': custom_tags if custom_tags else project_info.get('tags', ''),
                'Description': custom_description if custom_description else project_info.get('description', ''),
                'Billable': project_info['billable'],
                'Invoiced': 'no',
                'Invoice Reference': '',
                'Paid': 'no',
                'Approved': 'no', 
                'Approved By': ''
            }
            entries.append(entry)
    
    # Add any remaining time-off entries that weren't on week registration days
    # (This matches the frontend preview logic)
    added_time_off_dates = set()
    for entry in entries:
        if entry.get('Project') == projects['time_off_ooo']['name']:
            added_time_off_dates.add(entry['Date'])
    
    for date_str, time_off_info in time_off_data.items():
        if date_str not in added_time_off_dates:
            project_info = projects['time_off_ooo']
            
            entry = {
                'Date': date_str,
                'Person': user_info['name'],
                'Teams': user_info['teams'],
                'Email': user_info['email'],
                'Group/Client': project_info['group_client'],
                'Project': project_info['name'],
                'Minutes': int(time_off_info['hours'] * 60),
                'Hours': time_off_info['hours'],
                'Tags': 'other',  # Time off uses 'other' tag
                'Description': time_off_info.get('description', project_info.get('description', '')),
                'Billable': project_info['billable'],
                'Invoiced': 'no',
                'Invoice Reference': '',
                'Paid': 'no', 
                'Approved': 'no',
                'Approved By': ''
            }
            entries.append(entry)
            print(f"Added remaining time off entry for {date_str}")
    
    return entries

@app.route('/')
def index():
    """Main page"""
    projects_config = load_projects()
    return render_template('index.html', projects=projects_config['projects'])

@app.route('/api/generate', methods=['POST'])
def generate_csv():
    """Generate CSV file from form data"""
    try:
        data = request.json
        year = int(data['year'])
        month = int(data['month'])
        weekly_data = data['weekly_data']
        time_off_data = data.get('time_off_data', {})
        project_metadata = data.get('project_metadata', {})  # New: tags and descriptions
        
        print(f"Generating CSV for {year}-{month}")
        print(f"Weekly data: {weekly_data}")
        print(f"Time off data: {time_off_data}")
        print(f"Project metadata: {project_metadata}")
        
        projects_config = load_projects()
        
        # Calculate all time entries
        entries = calculate_time_entries(year, month, weekly_data, time_off_data, projects_config, project_metadata)
        
        # Generate CSV
        output = io.StringIO()
        fieldnames = ['Date', 'Person', 'Teams', 'Email', 'Group/Client', 'Project', 
                     'Minutes', 'Hours', 'Tags', 'Description', 'Billable', 'Invoiced',
                     'Invoice Reference', 'Paid', 'Approved', 'Approved By']
        
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        
        for entry in entries:
            writer.writerow(entry)
        
        # Convert to bytes for download
        csv_content = output.getvalue()
        output.close()
        
        return jsonify({
            'success': True,
            'csv_content': csv_content,
            'filename': f"noko-import-{year}-{month:02d}.csv"
        })
        
    except Exception as e:
        print(f"Error generating CSV: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/projects')
def get_projects():
    """Get project configuration"""
    projects_config = load_projects()
    return jsonify(projects_config)

@app.route('/api/save-profile', methods=['POST'])
def save_profile():
    """Save a month profile for backup/restore"""
    try:
        data = request.json
        profile_name = data['profile_name']
        year = data['year']
        month = data['month']
        weekly_data = data['weekly_data']
        time_off_data = data.get('time_off_data', {})
        
        profile = {
            'profile_name': profile_name,
            'year': year,
            'month': month,
            'created_date': datetime.now().isoformat(),
            'weekly_data': weekly_data,
            'time_off_data': time_off_data
        }
        
        # Create profiles directory if it doesn't exist
        import os
        if not os.path.exists('profiles'):
            os.makedirs('profiles')
        
        # Save profile to file
        filename = f"profiles/{profile_name}_{year}_{month:02d}.json"
        with open(filename, 'w') as f:
            json.dump(profile, f, indent=2)
        
        return jsonify({
            'success': True,
            'message': f'Profile "{profile_name}" saved successfully',
            'filename': filename
        })
        
    except Exception as e:
        print(f"Error saving profile: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/load-profile/<filename>')
def load_profile(filename):
    """Load a saved month profile"""
    try:
        filepath = f"profiles/{filename}"
        with open(filepath, 'r') as f:
            profile = json.load(f)
        
        return jsonify({
            'success': True,
            'profile': profile
        })
        
    except FileNotFoundError:
        return jsonify({'success': False, 'error': 'Profile not found'}), 404
    except Exception as e:
        print(f"Error loading profile: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/list-profiles')
def list_profiles():
    """List all saved month profiles"""
    try:
        import os
        profiles = []
        
        if os.path.exists('profiles'):
            for filename in os.listdir('profiles'):
                if filename.endswith('.json'):
                    filepath = f"profiles/{filename}"
                    try:
                        with open(filepath, 'r') as f:
                            profile = json.load(f)
                        
                        profiles.append({
                            'filename': filename,
                            'profile_name': profile.get('profile_name', 'Unknown'),
                            'year': profile.get('year'),
                            'month': profile.get('month'),
                            'created_date': profile.get('created_date'),
                            'month_name': calendar.month_name[profile.get('month', 1)]
                        })
                    except:
                        continue
        
        # Sort by creation date (newest first)
        profiles.sort(key=lambda x: x['created_date'], reverse=True)
        
        return jsonify({
            'success': True,
            'profiles': profiles
        })
        
    except Exception as e:
        print(f"Error listing profiles: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/us-holidays-2026')
def get_us_holidays_2026():
    """Get US Recharge Days for 2026"""
    holidays = {
        '2026-01-01': {'hours': 8, 'description': 'New Year\'s Day'},
        '2026-01-02': {'hours': 8, 'description': 'New Year\'s Day'},
        '2026-01-19': {'hours': 8, 'description': 'Martin Luther King Jr Day'},
        '2026-02-16': {'hours': 8, 'description': 'Presidents\' Day'},
        '2026-04-03': {'hours': 8, 'description': 'Good Friday'},
        '2026-05-22': {'hours': 8, 'description': 'Memorial Day'},
        '2026-05-25': {'hours': 8, 'description': 'Memorial Day'},
        '2026-06-19': {'hours': 8, 'description': 'Juneteenth'},
        '2026-07-02': {'hours': 8, 'description': 'Fourth of July'},
        '2026-07-03': {'hours': 8, 'description': 'Fourth of July'},
        '2026-09-04': {'hours': 8, 'description': 'Labor Day'},
        '2026-09-07': {'hours': 8, 'description': 'Labor Day'},
        '2026-11-25': {'hours': 8, 'description': 'Thanksgiving'},
        '2026-11-26': {'hours': 8, 'description': 'Thanksgiving'},
        '2026-11-27': {'hours': 8, 'description': 'Thanksgiving'},
        '2026-12-24': {'hours': 8, 'description': 'Christmas Eve'},
        '2026-12-25': {'hours': 8, 'description': 'Christmas'},
        '2026-12-28': {'hours': 8, 'description': 'Holiday Break'},
        '2026-12-29': {'hours': 8, 'description': 'Holiday Break'},
        '2026-12-30': {'hours': 8, 'description': 'Holiday Break'},
        '2026-12-31': {'hours': 8, 'description': 'New Year\'s Eve'}
    }
    
    return jsonify({
        'success': True,
        'holidays': holidays
    })

@app.route('/api/month-info/<int:year>/<int:month>')
def get_month_info(year, month):
    """Get information about a specific month (weeks, work days, etc.)"""
    try:
        weeks = get_month_weeks(year, month)
        _, num_days = calendar.monthrange(year, month)
        
        # Calculate work days per week
        week_info = []
        week_number = 1  # Track actual week numbers separately
        
        for i, week_start in enumerate(weeks):
            week_end = week_start + timedelta(days=6)
            work_days = 0
            
            # Count work days in this week that fall within the target month
            for day_offset in range(7):
                check_date = week_start + timedelta(days=day_offset)
                if (check_date.month == month and 
                    check_date.year == year and 
                    check_date.weekday() < 5):  # Monday=0, Friday=4
                    work_days += 1
            
            # Only include weeks with at least 1 work day
            if work_days > 0:
                week_info.append({
                    'week_number': week_number,
                    'start_date': week_start.strftime('%Y-%m-%d'),
                    'end_date': week_end.strftime('%Y-%m-%d'), 
                    'work_days': work_days
                })
                week_number += 1  # Increment only when we add a week
        
        return jsonify({
            'weeks': week_info,
            'total_days': num_days,
            'month_name': calendar.month_name[month]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Initialize projects file if it doesn't exist
    if not os.path.exists('projects.json'):
        save_projects(get_default_projects())
    
    print("Starting Noko Time Helper...")
    print("Open your browser to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)