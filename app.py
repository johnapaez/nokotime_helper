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
    """Load project configuration from JSON file"""
    try:
        with open('projects.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return default configuration if file doesn't exist
        return get_default_projects()

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
                "description": "#development",
                "tags": "development",
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
                "description": "#productionsupport",
                "tags": "productionsupport", 
                "billable": "yes"
            },
            "google_safety_tracker": {
                "name": "Google Safety Tracker (GST)",
                "group_client": "CapEx Projects",
                "description": "#development",
                "tags": "development",
                "billable": "yes"
            },
            "linear_iq": {
                "name": "Linear IQ (LIQ)", 
                "group_client": "CapEx Projects",
                "description": "#development",
                "tags": "development",
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
                "description": "#productionsupport", 
                "tags": "productionsupport",
                "billable": "yes"
            },
            "syndicate_tracking": {
                "name": "Syndicate Tracking Product (STP)",
                "group_client": "OpEx Projects", 
                "description": "#development API discussion",
                "tags": "development",
                "billable": "yes"
            },
            "time_off": {
                "name": "Time-Off (OOO)",
                "group_client": "",
                "description": "Sick Day and/or Memorial Day",
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
    
    # Get all Monday dates for the month
    weeks = []
    current_monday = first_monday
    
    while current_monday.month <= month and current_monday.year == year:
        weeks.append(current_monday)
        current_monday += timedelta(days=7)
    
    # Add one more week if it contains days from our target month
    if current_monday.month == month and current_monday.year == year:
        weeks.append(current_monday)
    
    return weeks

def calculate_time_entries(year, month, weekly_data, time_off_data, projects_config):
    """Calculate time entries for the entire month"""
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
                'Tags': project_info['tags'],
                'Description': time_off_info.get('description', project_info['description']),
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
            
            entry = {
                'Date': date_str,
                'Person': user_info['name'], 
                'Teams': user_info['teams'],
                'Email': user_info['email'],
                'Group/Client': project_info['group_client'],
                'Project': project_info['name'],
                'Minutes': minutes,
                'Hours': hours,
                'Tags': project_info['tags'],
                'Description': project_info['description'],
                'Billable': project_info['billable'],
                'Invoiced': 'no',
                'Invoice Reference': '',
                'Paid': 'no',
                'Approved': 'no', 
                'Approved By': ''
            }
            entries.append(entry)
    
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
        
        print(f"Generating CSV for {year}-{month}")
        print(f"Weekly data: {weekly_data}")
        print(f"Time off data: {time_off_data}")
        
        projects_config = load_projects()
        
        # Calculate all time entries
        entries = calculate_time_entries(year, month, weekly_data, time_off_data, projects_config)
        
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

@app.route('/api/month-info/<int:year>/<int:month>')
def get_month_info(year, month):
    """Get information about a specific month (weeks, work days, etc.)"""
    try:
        weeks = get_month_weeks(year, month)
        _, num_days = calendar.monthrange(year, month)
        
        # Calculate work days per week
        week_info = []
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
            
            week_info.append({
                'week_number': i + 1,
                'start_date': week_start.strftime('%Y-%m-%d'),
                'end_date': week_end.strftime('%Y-%m-%d'), 
                'work_days': work_days
            })
        
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