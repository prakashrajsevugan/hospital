from flask import Flask, render_template, request, redirect

app = Flask(__name__)

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
# MAIN ROUTE AND PAGE
# ---------------------------------------------------------------
@app.route("/")
def index():
    return render_template(
        "index.html",
        patients=patient_records.get_all(),
        queue=list(patient_queue),
        incidents=list(reversed(incident_stack)),
        hierarchy=hospital_tree,
        graph=city_graph,
        hash_data=hash_table.table
    )

# ---------------------------------------------------------------
# POST ACTION ROUTES
# ---------------------------------------------------------------
@app.route("/add_patient", methods=["POST"])
def add_patient():
    pid = int(request.form["id"])
    name = request.form["name"]
    patient_records.add(pid, name)
    return redirect("/")


@app.route("/delete_patient/<int:pid>")
def delete_patient(pid):
    patient_records.delete(pid)
    return redirect("/")


@app.route("/add_queue", methods=["POST"])
def add_queue():
    name = request.form["name"]
    patient_queue.append(name)
    return redirect("/")


@app.route("/process_queue")
def process_queue():
    if patient_queue:
        patient_queue.popleft()
    return redirect("/")


@app.route("/add_incident", methods=["POST"])
def add_incident():
    inc = request.form["incident"]
    incident_stack.append(inc)
    return redirect("/")


@app.route("/undo_incident")
def undo_incident():
    if incident_stack:
        incident_stack.pop()
    return redirect("/")


@app.route("/add_route", methods=["POST"])
def add_route_web():
    a = request.form["city_a"]
    b = request.form["city_b"]
    add_route(a, b)
    return redirect("/")


@app.route("/delete_route/<city_a>/<city_b>")
def delete_route_web(city_a, city_b):
    delete_route(city_a, city_b)
    return redirect("/")


@app.route("/add_hash", methods=["POST"])
def add_hash():
    pid = int(request.form["pid"])
    name = request.form["name"]
    hash_table.insert(pid, name)
    return redirect("/")


@app.route("/search_hash", methods=["POST"])
def search_hash():
    pid = int(request.form["pid"])
    result = hash_table.search(pid)
    return f"<h1>Search Result: {result if result else 'Not Found'}</h1><a href='/'>Back</a>"


@app.route("/delete_hash/<int:pid>")
def delete_hash(pid):
    hash_table.delete(pid)
    return redirect("/")


@app.route("/add_staff", methods=["POST"])
def add_staff():
    department = request.form["department"]
    staff_name = request.form["staff_name"]
    if department in hospital_tree["Hospital Director"]["departments"]:
        hospital_tree["Hospital Director"]["departments"][department].append(staff_name)
    return redirect("/")


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
