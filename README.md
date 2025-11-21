# 🏥 Hospital Emergency Management System

A comprehensive web-based Hospital Emergency Management System built with Flask that demonstrates various data structures and their practical applications in a healthcare setting.

## ✨ Features

### 📋 Patient Records (Linked List)
- Add and manage patient records with unique IDs
- Efficient sequential data storage using linked list implementation

### ⏱️ Patient Queue (Queue)
- FIFO-based patient queue management
- Process patients in order of arrival
- Real-time queue display

### 🚨 Incident Log (Stack)
- Log emergency incidents
- LIFO-based incident tracking
- Undo last incident feature

### 🏢 Hospital Hierarchy (Tree)
- Interactive department structure
- Collapsible department views
- Add staff members to different departments (Medical, Surgery, Nursing)
- Dynamic staff management

### 🗺️ City Map (Graph)
- Bidirectional city route mapping
- Add routes between cities
- Visual route display

### 🔍 Emergency ID Lookup (Hash Table)
- Fast patient lookup by emergency ID
- Hash-based storage and retrieval
- Collision handling with chaining

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/prakashrajsevugan/hospital.git
cd hospital
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Usage

1. Run the application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://127.0.0.1:5000
```

3. Interact with different modules:
   - **Add patients** to the linked list
   - **Queue patients** for processing
   - **Log incidents** and undo if needed
   - **Click department heads** to expand and add staff members
   - **Add city routes** to build the map
   - **Store and search** emergency IDs

## 🛠️ Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Structures**: 
  - Linked List
  - Queue (using deque)
  - Stack
  - Tree (Dictionary-based)
  - Graph (Adjacency List)
  - Hash Table (Custom implementation)

## 📂 Project Structure

```
hospital/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   └── style.css         # Styling and animations
└── README.md             # Project documentation
```

## 🎨 UI Features

- Modern gradient design with purple/blue theme
- Responsive grid layout
- Smooth animations and transitions
- Interactive collapsible sections
- Hover effects and visual feedback
- Mobile-friendly design

## 📝 Data Structures Implementation

### Linked List
Custom `Patient` and `PatientList` classes for sequential patient record management.

### Queue
Python's `collections.deque` for efficient FIFO operations.

### Stack
Python list with `append()` and `pop()` for LIFO incident logging.

### Tree
Nested dictionary structure for hierarchical hospital organization.

### Graph
Adjacency list using dictionary for city route mapping.

### Hash Table
Custom `EmergencyHash` class with chaining for collision resolution.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Prakash Raj Sevugan**
- GitHub: [@prakashrajsevugan](https://github.com/prakashrajsevugan)

## 🌟 Show your support

Give a ⭐️ if you like this project!

---

© 2025 Hospital Emergency Management System
