#!/usr/bin/env python3
"""
Demo script for Event Planner System
This script demonstrates the complete end-to-end flow of the event planning system.
"""

import subprocess
import sys
import time
import os
import signal
from threading import Thread

def print_banner():
    print("\n" + "="*60)
    print("🎉 EVENT PLANNER SYSTEM DEMO 🎉")
    print("="*60)
    print("This demo will start all components of the event planning system:")
    print("1. 📡 Coordinator (message broker)")
    print("2. 👥 Three Guest processes (guest1, guest2, guest3)")
    print("3. 🌐 Flask API Server")
    print("4. 🎯 Demo Host (sends invitation)")
    print("="*60)

def check_redis():
    """Check if Redis is running"""
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.ping()
        print("✅ Redis server is running")
        return True
    except Exception as e:
        print("❌ Redis server is not running!")
        print("Please start Redis server first:")
        print("Windows: Start Redis server or use WSL")
        print("macOS: brew services start redis")
        print("Linux: sudo systemctl start redis")
        return False

def start_component(name, command, delay=0):
    """Start a component in background"""
    if delay:
        time.sleep(delay)
    
    print(f"🚀 Starting {name}...")
    try:
        if sys.platform == "win32":
            # Windows
            process = subprocess.Popen(
                command,
                shell=True,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            # Unix/Linux/macOS
            process = subprocess.Popen(
                command,
                shell=True,
                preexec_fn=os.setsid
            )
        return process
    except Exception as e:
        print(f"❌ Failed to start {name}: {e}")
        return None

def main():
    print_banner()
    
    # Check Redis
    if not check_redis():
        sys.exit(1)
    
    input("Press Enter to start the demo...")
    
    processes = []
    
    try:
        # Start Coordinator
        coordinator = start_component("Coordinator", "python coordinator.py")
        if coordinator:
            processes.append(("Coordinator", coordinator))
        time.sleep(2)
        
        # Start Guests
        for i in range(1, 4):
            guest = start_component(f"Guest {i}", f"python guest.py guest{i}", delay=1)
            if guest:
                processes.append((f"Guest {i}", guest))
        
        time.sleep(2)
        
        # Start API Server
        api = start_component("API Server", "python api.py", delay=1)
        if api:
            processes.append(("API Server", api))
        
        time.sleep(3)
        print("\n" + "="*60)
        print("🎊 ALL COMPONENTS STARTED! 🎊")
        print("="*60)
        print("📡 Coordinator: Running")
        print("👥 Guests: guest1, guest2, guest3 are listening")
        print("🌐 API Server: http://localhost:5000")
        print("🎯 Frontend: http://localhost:3000 (start with 'npm start')")
        print("="*60)
        
        print("\n🚀 Now you can:")
        print("1. Open http://localhost:3000 in your browser")
        print("2. Or use the CLI demo by running: python host.py")
        print("3. Or test API endpoints with Postman")
        
        print("\n⏹️  Press Ctrl+C to stop all components")
        
        # Keep running until interrupted
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping all components...")
        
        # Terminate all processes
        for name, process in processes:
            try:
                print(f"Stopping {name}...")
                if sys.platform == "win32":
                    process.terminate()
                else:
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            except Exception as e:
                print(f"Error stopping {name}: {e}")
        
        print("✅ All components stopped!")
        print("🎉 Demo completed!")

if __name__ == "__main__":
    main()
