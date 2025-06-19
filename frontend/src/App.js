import React, { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [title, setTitle] = useState("");
  const [time, setTime] = useState("");
  const [eventId, setEventId] = useState(null);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [events, setEvents] = useState([]);
  const [autoRefresh, setAutoRefresh] = useState(false);

  // Auto-refresh functionality
  useEffect(() => {
    if (autoRefresh && eventId && !summary) {
      const interval = setInterval(() => {
        getSummary();
      }, 3000); // Check every 3 seconds

      return () => clearInterval(interval);
    }
  }, [autoRefresh, eventId, summary]);

  const sendInvite = async () => {
    if (!title.trim()) {
      setError("Please enter an event title");
      return;
    }

    setError(null);
    setSummary(null);
    setLoading(true);
    setAutoRefresh(false);

    try {
      const res = await axios.post("http://localhost:5000/send-invite", {
        title: title.trim(),
        time: time.trim() || "Time TBD",
      });
      
      setEventId(res.data.event_id);
      setAutoRefresh(true); // Start auto-refresh
      setTitle("");
      setTime("");
      
      // Show success message
      setError(`✅ Invitation sent to ${res.data.guests_invited} guests!`);
      
    } catch (err) {
      console.error("Error sending invite", err);
      setError("❌ Failed to send invitation. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const getSummary = async () => {
    if (!eventId) return;
    
    try {
      const res = await axios.get(`http://localhost:5000/get-summary/${eventId}`);
      if (res.status === 200) {
        setSummary(res.data);
        setAutoRefresh(false); // Stop auto-refresh when summary is received
        setError("🎉 All guests have responded!");
      }
    } catch (err) {
      if (err.response?.status === 202) {
        // Still waiting for responses
        setError("⏳ Waiting for guest responses...");
      } else {
        setError("❌ Error fetching summary");
      }
    }
  };

  const loadEvents = async () => {
    try {
      const res = await axios.get("http://localhost:5000/events");
      setEvents(res.data.events || []);
    } catch (err) {
      console.error("Error loading events", err);
    }
  };

  const formatDate = (timestamp) => {
    return new Date(timestamp * 1000).toLocaleString();
  };

  const resetForm = () => {
    setTitle("");
    setTime("");
    setEventId(null);
    setSummary(null);
    setError(null);
    setAutoRefresh(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">🎉 Event Planner</h1>
          <p className="text-gray-600">Send invitations and track guest responses in real-time</p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {/* Create Event Card */}
          <div className="bg-white p-6 rounded-xl shadow-lg">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">Create New Event</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Event Title *
                </label>
                <input
                  type="text"
                  placeholder="e.g., Birthday Party, Team Meeting"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="w-full border border-gray-300 p-3 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Event Time
                </label>
                <input
                  type="text"
                  placeholder="e.g., 7:00 PM tonight, Tomorrow at 2 PM"
                  value={time}
                  onChange={(e) => setTime(e.target.value)}
                  className="w-full border border-gray-300 p-3 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <button
                onClick={sendInvite}
                disabled={loading}
                className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white py-3 px-4 rounded-lg font-medium transition-colors"
              >
                {loading ? "Sending..." : "📤 Send Invitation"}
              </button>

              {error && (
                <div className={`p-3 rounded-lg text-sm ${
                  error.includes('❌') ? 'bg-red-50 text-red-700' : 
                  error.includes('✅') || error.includes('🎉') ? 'bg-green-50 text-green-700' : 
                  'bg-yellow-50 text-yellow-700'
                }`}>
                  {error}
                </div>
              )}

              {eventId && !summary && (
                <div className="space-y-2">
                  <button
                    onClick={getSummary}
                    className="w-full bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-lg font-medium transition-colors"
                  >
                    🔄 Check Responses
                  </button>
                  {autoRefresh && (
                    <div className="text-center text-sm text-gray-500">
                      Auto-refreshing every 3 seconds...
                    </div>
                  )}
                </div>
              )}

              {summary && (
                <button
                  onClick={resetForm}
                  className="w-full bg-gray-600 hover:bg-gray-700 text-white py-2 px-4 rounded-lg font-medium transition-colors"
                >
                  🆕 Create Another Event
                </button>
              )}
            </div>
          </div>

          {/* Results Card */}
          <div className="bg-white p-6 rounded-xl shadow-lg">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">Guest Responses</h2>
            
            {!summary && !eventId && (
              <div className="text-center text-gray-500 py-8">
                <div className="text-4xl mb-2">📋</div>
                <p>Create an event to see guest responses here</p>
              </div>
            )}

            {eventId && !summary && (
              <div className="text-center text-gray-500 py-8">
                <div className="text-4xl mb-2">⏳</div>
                <p>Waiting for guests to respond...</p>
                <div className="mt-4 text-sm">
                  Event ID: <code className="bg-gray-100 px-2 py-1 rounded">{eventId}</code>
                </div>
              </div>
            )}

            {summary && (
              <div className="space-y-4">
                <div className="bg-gray-50 p-4 rounded-lg">
                  <h3 className="font-medium text-gray-800 mb-2">📊 Summary</h3>
                  <div className="grid grid-cols-3 gap-4 text-center">
                    <div>
                      <div className="text-2xl font-bold text-green-600">{summary.confirmed?.length || 0}</div>
                      <div className="text-sm text-gray-600">Confirmed</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-yellow-600">{summary.maybe?.length || 0}</div>
                      <div className="text-sm text-gray-600">Maybe</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-red-600">{summary.declined?.length || 0}</div>
                      <div className="text-sm text-gray-600">Declined</div>
                    </div>
                  </div>
                </div>

                <div className="space-y-3">
                  {summary.confirmed?.length > 0 && (
                    <div>
                      <h4 className="font-medium text-green-700 mb-1">✅ Confirmed</h4>
                      <div className="flex flex-wrap gap-2">
                        {summary.confirmed.map((guest, index) => (
                          <span key={index} className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">
                            {guest}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {summary.maybe?.length > 0 && (
                    <div>
                      <h4 className="font-medium text-yellow-700 mb-1">🤔 Maybe</h4>
                      <div className="flex flex-wrap gap-2">
                        {summary.maybe.map((guest, index) => (
                          <span key={index} className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm">
                            {guest}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {summary.declined?.length > 0 && (
                    <div>
                      <h4 className="font-medium text-red-700 mb-1">❌ Declined</h4>
                      <div className="flex flex-wrap gap-2">
                        {summary.declined.map((guest, index) => (
                          <span key={index} className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm">
                            {guest}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-gray-500 text-sm">
          <p>🚀 Powered by Redis Pub/Sub • Real-time event planning system</p>
        </div>
      </div>
    </div>
  );
}

export default App;
