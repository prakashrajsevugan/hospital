from flask import Flask, render_template, request, redirect, session, flash, jsonify, send_file
from collections import deque
import json
import os
import csv
from io import StringIO, BytesIO
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'  # Change this in production!

# ---------------------------------------------------------------
# Linked List for Patient Records
# ---------------------------------------------------------------
class Patient:
    def __init__(self, pid, name):
        self.id = pid
        self.name = name
        self.next = None


class PatientList:
    def __init__(self):
        self.head = None

    def add(self, pid, name):
        newp = Patient(pid, name)
        if not self.head:
            self.head = newp
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = newp

    def get_all(self):
        temp = self.head
        result = []
        while temp:
            result.append((temp.id, temp.name))
            temp = temp.next
        return result

    def delete(self, pid):
        if not self.head:
            return False
        
        # If head node needs to be deleted
        if self.head.id == pid:
            self.head = self.head.next
            return True
        
        # Search for the node to delete
        temp = self.head
        while temp.next:
            if temp.next.id == pid:
                temp.next = temp.next.next
                return True
            temp = temp.next
        return False


patient_records = PatientList()

# ---------------------------------------------------------------
# Queue: Patient requests
# ---------------------------------------------------------------
from collections import deque

patient_queue = deque()

# ---------------------------------------------------------------
# Stack: Incident log
# ---------------------------------------------------------------
incident_stack = []

# ---------------------------------------------------------------
# Tree: Hospital hierarchy
# ---------------------------------------------------------------
hospital_tree = {
    "Hospital Director": {
        "staff": [],
        "departments": {
            "Medical Head": [],
            "Surgery Head": [],
            "Nursing Head": []
        }
    }
}

# ---------------------------------------------------------------
# Graph: City map
# ---------------------------------------------------------------
city_graph = {}

def add_route(a, b):
    city_graph.setdefault(a, []).append(b)
    city_graph.setdefault(b, []).append(a)

def delete_route(a, b):
    if a in city_graph and b in city_graph[a]:
        city_graph[a].remove(b)
        if not city_graph[a]:  # Remove empty list
            del city_graph[a]
    if b in city_graph and a in city_graph[b]:
        city_graph[b].remove(a)
        if not city_graph[b]:  # Remove empty list
            del city_graph[b]

# ---------------------------------------------------------------
# Hash Table: Emergency ID lookup
# ---------------------------------------------------------------
class EmergencyHash:
    SIZE = 10

    def __init__(self):
        self.table = [[] for _ in range(self.SIZE)]

    def hash_fn(self, k):
        return k % self.SIZE

    def insert(self, pid, name):
        idx = self.hash_fn(pid)
        self.table[idx].append((pid, name))

    def search(self, pid):
        idx = self.hash_fn(pid)
        for k, v in self.table[idx]:
            if k == pid:
                return v
        return None

    def delete(self, pid):
        idx = self.hash_fn(pid)
        for i, (k, v) in enumerate(self.table[idx]):
            if k == pid:
                self.table[idx].pop(i)
                return True
        return False


hash_table = EmergencyHash()

# ---------------------------------------------------------------
# DATA PERSISTENCE FUNCTIONS
# ---------------------------------------------------------------
DATA_FILE = 'hospital_data.json'

def save_data():
    """Save all data structures to JSON file"""
    try:
        data = {
            'patients': patient_records.get_all(),
            'queue': list(patient_queue),
            'incidents': incident_stack,
            'hierarchy': hospital_tree,
            'graph': city_graph,
            'hash_table': hash_table.table,
            'last_updated': datetime.now().isoformat()
        }
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

def load_data():
    """Load data from JSON file"""
    global patient_queue, incident_stack, hospital_tree, city_graph
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
            
            # Load patients
            for pid, name in data.get('patients', []):
                patient_records.add(pid, name)
            
            # Load queue
            patient_queue.extend(data.get('queue', []))
            
            # Load incidents
            incident_stack.extend(data.get('incidents', []))
            
            # Load hierarchy
            if 'hierarchy' in data:
                hospital_tree.update(data['hierarchy'])
            
            # Load graph
            city_graph.update(data.get('graph', {}))
            
            # Load hash table
            if 'hash_table' in data:
                hash_table.table = data['hash_table']
            
            return True
    except Exception as e:
        print(f"Error loading data: {e}")
        return False

# Load data on startup
load_data()

# ---------------------------------------------------------------
# MAIN ROUTE AND PAGE
# ---------------------------------------------------------------
# Simple user database (in production, use proper database)
users = {
    'admin': {'password': 'admin123', 'role': 'admin'},
    'staff': {'password': 'staff123', 'role': 'staff'}
}

@app.route("/")
def index():
    if 'username' not in session:
        return redirect('/login')
    return render_template(
        "index.html",
        patients=patient_records.get_all(),
        queue=list(patient_queue),
        incidents=list(reversed(incident_stack)),
        hierarchy=hospital_tree,
        graph=city_graph,
        hash_data=hash_table.table,
        username=session.get('username'),
        role=session.get('role')
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['role'] = users[username]['role']
            flash(f'Welcome, {username}!', 'success')
            return redirect("/")
        else:
            flash('Invalid credentials!', 'warning')
            return redirect("/login")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    username = session.get('username')
    session.clear()
    flash(f'Goodbye, {username}!', 'success')
    return redirect("/login")

# ---------------------------------------------------------------
# POST ACTION ROUTES
# ---------------------------------------------------------------
@app.route("/add_patient", methods=["POST"])
def add_patient():
    pid = int(request.form["id"])
    name = request.form["name"]
    patient_records.add(pid, name)
    save_data()
    flash(f'Patient {name} added successfully!', 'success')
    return redirect("/")


@app.route("/delete_patient/<int:pid>")
def delete_patient(pid):
    patient_records.delete(pid)
    save_data()
    flash('Patient deleted successfully!', 'success')
    return redirect("/")


@app.route("/add_queue", methods=["POST"])
def add_queue():
    name = request.form["name"]
    patient_queue.append(name)
    save_data()
    flash(f'{name} added to queue!', 'success')
    return redirect("/")


@app.route("/process_queue")
def process_queue():
    if patient_queue:
        name = patient_queue.popleft()
        save_data()
        flash(f'Processed patient: {name}', 'success')
    else:
        flash('Queue is empty!', 'warning')
    return redirect("/")


@app.route("/add_incident", methods=["POST"])
def add_incident():
    inc = request.form["incident"]
    incident_stack.append(inc)
    save_data()
    flash('Incident logged!', 'success')
    return redirect("/")


@app.route("/undo_incident")
def undo_incident():
    if incident_stack:
        incident = incident_stack.pop()
        save_data()
        flash(f'Undone: {incident}', 'success')
    else:
        flash('No incidents to undo!', 'warning')
    return redirect("/")


@app.route("/add_route", methods=["POST"])
def add_route_web():
    a = request.form["city_a"]
    b = request.form["city_b"]
    add_route(a, b)
    save_data()
    flash(f'Route added: {a} ↔ {b}', 'success')
    return redirect("/")


@app.route("/delete_route/<city_a>/<city_b>")
def delete_route_web(city_a, city_b):
    delete_route(city_a, city_b)
    save_data()
    flash(f'Route deleted: {city_a} ↔ {city_b}', 'success')
    return redirect("/")


@app.route("/add_hash", methods=["POST"])
def add_hash():
    pid = int(request.form["pid"])
    name = request.form["name"]
    hash_table.insert(pid, name)
    save_data()
    flash(f'Emergency ID {pid} stored!', 'success')
    return redirect("/")


@app.route("/search_hash", methods=["POST"])
def search_hash():
    pid = int(request.form["pid"])
    result = hash_table.search(pid)
    return f"<h1>Search Result: {result if result else 'Not Found'}</h1><a href='/'>Back</a>"


@app.route("/delete_hash/<int:pid>")
def delete_hash(pid):
    hash_table.delete(pid)
    save_data()
    flash(f'Emergency ID {pid} deleted!', 'success')
    return redirect("/")


@app.route("/add_staff", methods=["POST"])
def add_staff():
    department = request.form["department"]
    staff_name = request.form["staff_name"]
    if department in hospital_tree["Hospital Director"]["departments"]:
        hospital_tree["Hospital Director"]["departments"][department].append(staff_name)
        save_data()
        flash(f'{staff_name} added to {department}!', 'success')
    return redirect("/")


@app.route("/delete_staff/<department>/<staff_name>")
def delete_staff(department, staff_name):
    if department in hospital_tree["Hospital Director"]["departments"]:
        if staff_name in hospital_tree["Hospital Director"]["departments"][department]:
            hospital_tree["Hospital Director"]["departments"][department].remove(staff_name)
            save_data()
            flash(f'{staff_name} removed from {department}!', 'success')
    return redirect("/")


# ---------------------------------------------------------------
# EXPORT FUNCTIONALITY
# ---------------------------------------------------------------
@app.route("/export/patients")
def export_patients():
    """Export patients to CSV"""
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Patient ID', 'Patient Name'])
    for pid, name in patient_records.get_all():
        writer.writerow([pid, name])
    
    output.seek(0)
    return send_file(
        BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'patients_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@app.route("/export/queue")
def export_queue():
    """Export queue to CSV"""
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Position', 'Patient Name'])
    for i, name in enumerate(patient_queue, 1):
        writer.writerow([i, name])
    
    output.seek(0)
    return send_file(
        BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'queue_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@app.route("/export/emergency")
def export_emergency():
    """Export emergency IDs to CSV"""
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Emergency ID', 'Patient Name'])
    for bucket in hash_table.table:
        for pid, name in bucket:
            writer.writerow([pid, name])
    
    output.seek(0)
    return send_file(
        BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'emergency_ids_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@app.route("/stats")
def get_stats():
    """Get statistics"""
    return jsonify({
        'total_patients': len(patient_records.get_all()),
        'queue_length': len(patient_queue),
        'total_incidents': len(incident_stack),
        'total_routes': sum(len(routes) for routes in city_graph.values()) // 2,
        'total_emergency_ids': sum(len(bucket) for bucket in hash_table.table),
        'total_staff': sum(len(staff) for staff in hospital_tree["Hospital Director"]["departments"].values())
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
