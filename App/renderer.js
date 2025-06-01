// This file will contain the frontend logic for the authentication system
const { ipcRenderer } = require('electron');

document.addEventListener('DOMContentLoaded', () => {
    console.log('Authentication system loaded');

    // Get references to DOM elements
    const closeButton = document.getElementById('closeButton');
    const toggleLoginForm = document.getElementById('toggleLoginForm');
    const loginForm = document.getElementById('loginForm');
    const authContainer = document.getElementById('authContainer');
    const accessMessage = document.getElementById('accessMessage');
    const mainMessage = document.getElementById('mainMessage');
    const videoFrame = document.getElementById("video");

    let connected = false;
    let connectionTimeOut;
    connectionTimeOut = setTimeout(() => {
        if (connected == false) {
            showMainMessage(`⚠️⚠️ No Connection! ⚠️⚠️`);
        }
    }, 1000);
    
    const usersSocket = new WebSocket("ws://192.168.68.77:8766");
    usersSocket.onmessage = (event) => {
        showAuthSuccessMessage(event.data);
    };

    const videoSocket = new WebSocket("ws://192.168.68.77:8765");
    videoSocket.onmessage = (event) => {
        videoFrame.src = "data:image/jpeg;base64," + event.data;

        if (connected == false) {
            connected = true;
            showMainMessage(`Please come closer for facial recognition`)
        }

        clearTimeout(connectionTimeOut);
        connectionTimeOut = setTimeout(() => {
            connected = false;
            showMainMessage(`⚠️⚠️ LOST Connection! ⚠️⚠️`);
        }, 1000);
    };

    // Facial recognition simulation (will be replaced with actual facial recognition)
    let isFacialAuthenticationEnabled = true;
    
    // Close button functionality
    if (closeButton) {
        closeButton.addEventListener('click', () => {
            ipcRenderer.send('app-quit');
        });
    }
    
    // Toggle login form
    if (toggleLoginForm && loginForm) {
        toggleLoginForm.addEventListener('click', () => {
            loginForm.classList.toggle('visible');
            
            // If form is now visible, focus on username field
            if (loginForm.classList.contains('visible')) {
                document.getElementById('username').focus();
            }
        });
        
        // Handle form submission
        const form = loginForm.querySelector('form');
        if (form) {
            form.addEventListener('submit', (event) => {
                event.preventDefault();
                const username = document.getElementById('username').value;
                const password = document.getElementById('password').value;
                
                // Simulate authentication logic
                authenticateUser(username, password);
            });
        }
    }

    function showMainMessage(message) {
        mainMessage.textContent = message;
    }
    
    // Function to show authentication success message
    function showAuthSuccessMessage(username) {
        if (authContainer) {
            authContainer.classList.add('authenticated');
            
            // Change accessMessage text if needed
            if (accessMessage) {
                accessMessage.innerText = `Access authorised for ${username}`;
            }
            
            // After 4 seconds, remove authentication and reset
            setTimeout(() => {
                console.log('Authentication expired');
                authContainer.classList.remove('authenticated');
                showMainMessage("OLA");
            }, 4000);
        }
    }
    
    // Authentication function
    function authenticateUser(username, password) {
        const form = loginForm.querySelector('form');
        
        // For demo purposes, simple authentication
        // In a real app, this would validate against a database or service
        if (username && password) {
            console.log('Authentication successful!');
            
            // Show the authentication success message
            showAuthSuccessMessage(username);
            
            // Clear and hide the form
            if (form) form.reset();
            loginForm.classList.remove('visible');
        } else {
            alert('Please enter both username and password');
        }
    }
    
    // Simulate facial recognition (for demo purposes)
    if (isFacialAuthenticationEnabled && authContainer) {
        // Connect to a camera and facial recognition API
        const simulateFacialRecognition = () => {
            // Uncomment this to simulate facial recognition
            // setTimeout(() => {
            //     console.log('Facial recognition successful!');
            //     showAuthSuccessMessage();
            // }, 5000);
        };
        
        simulateFacialRecognition();
    }
    
    // Add keyboard shortcut for closing (Esc key)
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            // If login form is visible, hide it first
            if (loginForm && loginForm.classList.contains('visible')) {
                loginForm.classList.remove('visible');
            } else {
                window.close();
            }
        }
    });
});