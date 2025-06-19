# 🎉 Event Planner System

A real-time event planning system built with Python, Redis Pub/Sub, Flask, and React. Hosts send invitations, guests respond automatically, and responses are collected in real-time.

## 📋 Prerequisites

- **Python 3.8+**
- **Redis Server**
- **Node.js 14+**

### Install Redis:
- **Windows**: [Download Redis](https://redis.io/download) or use WSL
- **macOS**: `brew install redis && brew services start redis`
- **Linux**: `sudo apt-get install redis-server && sudo systemctl start redis`

---

## 🚀 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/madboy482/Pub-Sub_Model.git
cd Pub-Sub_Model
```

### 2. Setup backend
```bash
cd backend
pip install -r requirements.txt
```

### 3. Setup frontend
```bash
cd frontend
npm install
```

### 4. Make sure Redis is running
Start Redis server on your system (default: localhost:6379)

---

## 🏃 Running the System

### Start each component in separate terminals:

#### Terminal 1 - Coordinator
```bash
cd backend
python coordinator.py
```

#### Terminal 2 - Guest 1
```bash
cd backend
python guest.py guest1
```

#### Terminal 3 - Guest 2
```bash
cd backend
python guest.py guest2
```

#### Terminal 4 - Guest 3
```bash
cd backend
python guest.py guest3
```

#### Terminal 5 - API Server
```bash
cd backend
python api.py
```

#### Terminal 6 - Frontend (optional)
```bash
cd frontend
npm start
```

---

## 🎯 How to Test

### Option 1: CLI Demo
```bash
cd backend
python host.py
```

### Option 2: Web Interface
- Start frontend with `npm start`
- Open `http://localhost:3000`
- Create events through the web interface

### Option 3: API Testing
Use Postman or curl to test `http://localhost:5000/send-invite`

**Sample JSON:**
```json
{
    "title": "Birthday Party",
    "time": "7:00 PM tonight"
}
```

---

## 🏗️ How it Works

1. **Host** sends invitation → **Coordinator**
2. **Coordinator** forwards invitation → All **Guests**
3. **Guests** respond (Yes/No/Maybe) → **Coordinator**  
4. **Coordinator** collects responses → Sends summary to **Host**

---

## 📁 Components

- `coordinator.py` - Message broker service
- `guest.py` - Guest simulation (run with guest1, guest2, guest3)
- `host.py` - CLI interface for creating events
- `api.py` - REST API server
- `frontend/` - React web interface
- Creates and sends event invitations
- Receives and displays final guest summaries
- Interactive CLI interface for event creation

### 3. **Guests** (`guest.py`)
- Simulates real guests with unique personalities
- **guest1**: Usually says yes (80% likelihood), responds quickly
- **guest2**: Uncertain (50% likelihood), takes time to decide  
- **guest3**: Usually declines (30% likelihood), moderate response time
- Realistic response timing and decision-making

### 4. **API Server** (`api.py`)
- RESTful Flask API for web integration
- Handles invitation sending and summary retrieval
- CORS enabled for frontend communication
- Multiple endpoints for different operations

### 5. **Frontend** (`src/App.js`)
- Modern React interface with Tailwind CSS
- Real-time updates and auto-refresh
- Beautiful, responsive design
- Error handling and user feedback

---

## 🌐 API Endpoints

### `POST /send-invite`
Send a new event invitation.

**Request:**
```json
{
  "title": "Birthday Party at Sarah's House",
  "time": "2025-06-25T18:00:00Z"
}
```

**Response:**
```json
{
  "message": "Invitation sent successfully",
  "event_id": "uuid-here",
  "event": { ... },
  "guests_invited": 3
}
```

### `GET /get-summary/{event_id}`
Get the guest response summary for an event.

**Response (when complete):**
```json
{
  "event_id": "uuid-here",
  "total_guests": 3,
  "responses_received": 3,
  "confirmed": ["guest1"],
  "maybe": ["guest2"],
  "declined": ["guest3"],
  "timestamp": 1640995200.0
}
```

### `GET /events`
List all events and their status.

### `GET /`
API information and available endpoints.

---

## 🎮 Demo Instructions

### Option 1: Manual Component Start

1. **Start Coordinator:**
   ```bash
   python coordinator.py
   ```

2. **Start Guests (in separate terminals):**
   ```bash
   python guest.py guest1
   python guest.py guest2
   python guest.py guest3
   ```

3. **Start API Server:**
   ```bash
   python api.py
   ```

4. **Send Invitation (CLI):**
   ```bash
   python host.py
   ```

### Option 3: Web Interface
1. Start backend components (coordinator, guests, API)
2. Start frontend: `cd frontend && npm start`
3. Open `http://localhost:3000`
4. Create events through the web interface

---

## 🧪 Testing

### Test with Postman
Use the sample JSON data provided in the assignment for API testing:

```json
{
    "title": "Birthday Party at Sarah's House",
    "time": "2025-06-25T18:00:00Z"
}
```

### Test Scenarios
1. **Basic Flow**: Send invitation → Wait for responses → Check summary
2. **Multiple Events**: Send multiple invitations simultaneously
3. **Error Handling**: Send invalid data, check non-existent events
4. **Performance**: Test with rapid successive invitations

---

## 📁 Project Structure

```
event-planner/
├── backend/
│   ├── api.py              # Flask REST API
│   ├── coordinator.py      # Message coordinator service
│   ├── guest.py           # Guest simulation
│   ├── host.py            # Host CLI interface
│   ├── utils.py           # Redis pub/sub utilities
│   ├── config.json        # Configuration file
│   ├── requirements.txt   # Python dependencies
└── frontend/
    ├── src/
    │   ├── App.js         # Main React component
    │   ├── index.js       # React entry point
    │   └── index.css      # Styling
    ├── public/
    └── package.json       # Node.js dependencies
```

---

## 🎯 Key Features Demonstrated

1. **Pub/Sub Architecture**: Decoupled communication between components
2. **Real-time Processing**: Instant message delivery and processing
3. **Multiple Interfaces**: CLI, API, and Web frontend
4. **State Management**: Proper handling of event states and responses
5. **Error Handling**: Robust error handling throughout the system
6. **Scalability**: Easy to add more guests or modify behavior
7. **User Experience**: Clean, intuitive interfaces for all interaction methods

---

## 🔮 Future Enhancements

1. **Database Integration**: Persistent storage for events and responses
2. **Authentication**: User login and event ownership
3. **Email Notifications**: Real email invitations and reminders
4. **Event Templates**: Pre-defined event types and templates
5. **Calendar Integration**: Google Calendar, Outlook integration
6. **Mobile App**: React Native mobile application
7. **Analytics**: Event success metrics and reporting
8. **Multi-tenant**: Support for multiple organizations
9. **Real-time Chat**: Discussion features for events
10. **RSVP Deadlines**: Time-based response handling

---

## 📝 Configuration

The system uses `config.json` for channel configuration:

```json
{
  "host_channel": "event_invitations",
  "guest_response_channel": "guest_responses", 
  "summary_channel": "event_summary",
  "guests": ["guest1", "guest2", "guest3"]
}
```

---

# Contributing

Feel free to submit pull requests or create issues for any bugs or feature requests.

---

# License

This project is open source and available under the [MIT License](LICENSE).
