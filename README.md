# 🎉 Event Planner System

A real-time event planning system built with Python, Redis Pub/Sub, Flask, and React. This system demonstrates a complete Pub/Sub architecture where hosts can send invitations, guests respond automatically, and responses are collected in real-time.

## 📋 Table of Contents

- [System Architecture](#-system-architecture)
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Components](#-components)
- [API Endpoints](#-api-endpoints)
- [Demo Instructions](#-demo-instructions)
- [Testing](#-testing)
- [Project Structure](#-project-structure)

## 🏗️ System Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    Host     │    │ Coordinator │    │   Guests    │
│   (CLI/API) │    │  (Service)  │    │(guest1,2,3) │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       │ 1. Send Event    │ 2. Forward       │
       ├─────────────────►├─────────────────►│
       │                  │                  │
       │                  │ 3. Collect       │
       │                  │◄─────────────────┤
       │ 4. Send Summary  │                  │
       │◄─────────────────┤                  │
       │                  │                  │
   ┌───▼────┐         ┌───▼────┐         ┌───▼────┐
   │ Redis  │         │ Redis  │         │ Redis  │
   │Pub/Sub │         │Pub/Sub │         │Pub/Sub │
   └────────┘         └────────┘         └────────┘
```

## ✨ Features

- **Real-time Communication**: Uses Redis Pub/Sub for instant message delivery
- **Multiple Interfaces**: CLI, Web API, and React frontend
- **Intelligent Guest Simulation**: Guests have different response patterns and personalities
- **Auto-refresh**: Frontend automatically updates when responses arrive
- **Complete Workflow**: End-to-end invitation → response → summary cycle
- **Error Handling**: Robust error handling and logging
- **Scalable Architecture**: Easy to add more guests or features

## 📋 Prerequisites

- **Python 3.7+**
- **Redis Server** (running on localhost:6379)
- **Node.js 14+** (for frontend)
- **npm or yarn** (for frontend dependencies)

### Install Redis:
- **Windows**: [Download Redis](https://redis.io/download) or use WSL
- **macOS**: `brew install redis && brew services start redis`
- **Linux**: `sudo apt-get install redis-server && sudo systemctl start redis`

## 🚀 Quick Start

### 1. Clone and Setup Backend
```bash
cd backend
pip install -r requirements.txt
```

### 2. Setup Frontend
```bash
cd frontend
npm install
```

### 3. Start Redis Server
Make sure Redis is running on `localhost:6379`

### 4. Run the Complete Demo
```bash
cd backend
python demo.py
```

### 5. Start Frontend (in separate terminal)
```bash
cd frontend
npm start
```

Visit `http://localhost:3000` to use the web interface!

## 🔧 Components

### 1. **Coordinator** (`coordinator.py`)
- Central message broker
- Forwards invitations from hosts to all guests
- Collects responses and generates summaries
- Handles message routing and state management

### 2. **Host** (`host.py`)
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

## 🎮 Demo Instructions

### Option 1: Full System Demo
```bash
cd backend
python demo.py
```
This starts all components automatically in separate windows.

### Option 2: Manual Component Start

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
│   └── demo.py           # Complete demo script
└── frontend/
    ├── src/
    │   ├── App.js         # Main React component
    │   ├── index.js       # React entry point
    │   └── index.css      # Styling
    ├── public/
    └── package.json       # Node.js dependencies
```

## 🎯 Key Features Demonstrated

1. **Pub/Sub Architecture**: Decoupled communication between components
2. **Real-time Processing**: Instant message delivery and processing
3. **Multiple Interfaces**: CLI, API, and Web frontend
4. **State Management**: Proper handling of event states and responses
5. **Error Handling**: Robust error handling throughout the system
6. **Scalability**: Easy to add more guests or modify behavior
7. **User Experience**: Clean, intuitive interfaces for all interaction methods

## 🔮 Future Enhancements

If given more time, additional features could include:

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

## 📝 Configuration

The system uses `config.json` for channel configuration:

```json
{
  "host_channel": "event_invitations",
  "guest_response_channel": "guest_responses", 
  "summary_channel": "event_summary",
  "guests": ["guest1", "guest2", "guest3"]
}
