# 🏥 Hospital Emergency Management System

A comprehensive web-based Hospital Emergency Management System built with Flask that demonstrates various data structures and their practical applications in a healthcare setting.

## ✨ Features

### � Authentication System
- Secure login/logout functionality
- Role-based access (Admin/Staff)
- Session management
- Demo credentials provided

### �📋 Patient Records (Linked List)
- Add and manage patient records with unique IDs
- Delete patient records with confirmation
- Search patients by ID or name
- Export to CSV
- Efficient sequential data storage using linked list implementation

### ⏱️ Patient Queue (Queue)
- FIFO-based patient queue management
- Process patients in order of arrival
- Export queue to CSV
- Real-time queue display with counter

### 🚨 Incident Log (Stack)
- Log emergency incidents
- LIFO-based incident tracking
- Undo last incident feature
- Real-time incident counter

### 🏢 Hospital Hierarchy (Tree)
- Interactive department structure
- Collapsible department views
- Add/delete staff members to different departments (Medical, Surgery, Nursing)
- Dynamic staff management with counters
- Department-wise staff organization

### 🗺️ City Map (Graph)
- Bidirectional city route mapping
- Add/delete routes between cities
- Visual route display with delete options
- Route counter

### 🔍 Emergency ID Lookup (Hash Table)
- Fast patient lookup by emergency ID
- Search by ID or name
- Delete emergency records
- Export to CSV
- Hash-based storage and retrieval
- Collision handling with chaining

### 💾 Data Persistence
- Auto-save all data to JSON file
- Load data on startup
- Persistent storage across sessions

### 📊 Real-Time Statistics
- Live dashboard with counts
- Patient count, queue length
- Incident tracking, route statistics

### 🔔 Notifications
- Toast notifications for all actions
- Success/warning messages
- Auto-dismiss after 5 seconds

### 📥 Export Functionality
- Export patients to CSV
- Export queue to CSV
- Export emergency IDs to CSV
- Timestamped file names

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

### Local Development

1. Run the application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://127.0.0.1:5000
```

### Deploy to Render

1. Fork or clone this repository
2. Sign up at [Render.com](https://render.com)
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Render will automatically detect the configuration from `render.yaml`
6. Click "Create Web Service"
7. Wait for deployment to complete!

The app will be live at: `https://your-app-name.onrender.com`

3. **Login** with demo credentials:
   - Admin: `admin` / `admin123`
   - Staff: `staff` / `staff123`

4. Interact with different modules:
   - **Add/Delete patients** with search functionality
   - **Queue patients** for processing
   - **Log incidents** and undo if needed
   - **Manage staff** in different departments
   - **Add/Delete city routes** to build the map
   - **Store/Search/Delete** emergency IDs
   - **Export data** to CSV files
   - **View real-time statistics** in the header

## 🛠️ Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Authentication**: Session-based authentication
- **Data Persistence**: JSON file storage
- **Export**: CSV generation
- **Data Structures**: 
  - Linked List (Custom implementation)
  - Queue (using collections.deque)
  - Stack (Python list)
  - Tree (Nested dictionary)
  - Graph (Adjacency List)
  - Hash Table (Custom implementation with chaining)

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

## 🎨 UI/UX Features

- Modern gradient design with purple/blue theme
- Responsive grid layout (mobile, tablet, desktop)
- Smooth animations and transitions
- Interactive collapsible sections
- Toast notifications for user actions
- Real-time statistics dashboard
- Search functionality with live filtering
- Export buttons with visual feedback
- Login page with demo credentials
- User profile display with role badges
- Hover effects and visual feedback
- Touch-friendly buttons (44px minimum)
- Auto-dismissing flash messages
- Loading states and confirmations

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
