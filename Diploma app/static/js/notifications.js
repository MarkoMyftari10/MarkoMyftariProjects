class NotificationSystem {
    constructor() {
        this.notifications = [];
        this.initializeNotifications();
    }

    // Requests permission to show browser notifications
    async initializeNotifications() {
        if ('Notification' in window) {
            const permission = await Notification.requestPermission();
            if (permission === 'granted') {
                this.startNotificationListener();
            }
        }
    }

    // Sets up WebSocket connection for real-time notifications
    startNotificationListener() {
        const ws = new WebSocket('ws://your-server/notifications');
        
        ws.onmessage = (event) => {
            const notification = JSON.parse(event.data);
            this.showNotification(notification);
        };
    }

    // Shows browser notification and adds to notification center
    showNotification(notification) {
        // Browser notification
        new Notification(notification.title, {
            body: notification.body,
            icon: notification.icon
        });

        // Add to in-app notification center
        this.addToNotificationCenter(notification);
    }

    addToNotificationCenter(notification) {
        const center = document.getElementById('notificationCenter');
        if (!center) return;

        const notificationElement = document.createElement('div');
        notificationElement.className = 'notification-item';
        notificationElement.innerHTML = `
            <div class="notification-header">
                <span class="notification-title">${notification.title}</span>
                <span class="notification-time">${new Date().toLocaleTimeString()}</span>
            </div>
            <div class="notification-body">${notification.body}</div>
        `;

        center.prepend(notificationElement);
    }
} 