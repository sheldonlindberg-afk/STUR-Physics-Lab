/**
 * STUR Physics Lab - Service Worker Registration
 * Handles SW registration, update detection, and auto-refresh
 *
 * Cache Version: stur-v2.5.0 (must match sw.js)
 */

(function() {
  'use strict';

  // Only proceed if service workers are supported
  if (!('serviceWorker' in navigator)) {
    console.log('[SW Register] Service workers not supported');
    return;
  }

  const SW_URL = '/sw.js';
  const UPDATE_CHECK_INTERVAL = 60 * 60 * 1000; // Check for updates every hour

  let refreshing = false;
  let registration = null;

  /**
   * Initialize service worker registration
   */
  function init() {
    // Wait for page load to avoid blocking initial render
    if (document.readyState === 'complete') {
      registerServiceWorker();
    } else {
      window.addEventListener('load', registerServiceWorker);
    }

    // Handle controller changes (new SW taking over)
    navigator.serviceWorker.addEventListener('controllerchange', handleControllerChange);
  }

  /**
   * Register the service worker
   */
  async function registerServiceWorker() {
    try {
      registration = await navigator.serviceWorker.register(SW_URL, {
        scope: '/'
      });

      console.log('[SW Register] Service worker registered successfully');
      console.log('[SW Register] Scope:', registration.scope);

      // Check the current state
      if (registration.installing) {
        console.log('[SW Register] Service worker installing');
        trackInstalling(registration.installing);
      } else if (registration.waiting) {
        console.log('[SW Register] Service worker waiting');
        notifyUserOfUpdate(registration.waiting);
      } else if (registration.active) {
        console.log('[SW Register] Service worker active');
      }

      // Listen for new service workers
      registration.addEventListener('updatefound', handleUpdateFound);

      // Set up periodic update checks
      setupPeriodicUpdateCheck();

    } catch (error) {
      console.error('[SW Register] Registration failed:', error);
    }
  }

  /**
   * Handle when a new service worker is found
   */
  function handleUpdateFound() {
    console.log('[SW Register] Update found!');

    const newWorker = registration.installing;
    if (newWorker) {
      trackInstalling(newWorker);
    }
  }

  /**
   * Track the installing service worker's state
   */
  function trackInstalling(worker) {
    worker.addEventListener('statechange', () => {
      console.log('[SW Register] Worker state changed:', worker.state);

      switch (worker.state) {
        case 'installed':
          if (navigator.serviceWorker.controller) {
            // New version available - there was already a controller
            console.log('[SW Register] New version available');
            notifyUserOfUpdate(worker);
          } else {
            // First install - content is now cached
            console.log('[SW Register] Content cached for offline use');
            showNotification('STUR is now available offline', 'success');
          }
          break;

        case 'activated':
          console.log('[SW Register] New service worker activated');
          break;

        case 'redundant':
          console.log('[SW Register] Service worker became redundant');
          break;
      }
    });
  }

  /**
   * Handle when a new service worker takes control
   */
  function handleControllerChange() {
    if (refreshing) {
      return;
    }

    console.log('[SW Register] New service worker took control, refreshing...');
    refreshing = true;

    // Reload the page to get fresh content
    window.location.reload();
  }

  /**
   * Notify user that an update is available
   */
  function notifyUserOfUpdate(worker) {
    // Create update notification UI
    const notification = createUpdateNotification(() => {
      // User clicked update - tell SW to skip waiting
      worker.postMessage({ action: 'skipWaiting' });
    });

    document.body.appendChild(notification);
  }

  /**
   * Create the update notification element
   */
  function createUpdateNotification(onUpdate) {
    const container = document.createElement('div');
    container.id = 'sw-update-notification';
    container.setAttribute('role', 'alert');
    container.setAttribute('aria-live', 'polite');

    container.innerHTML = `
      <div class="sw-update-content">
        <span class="sw-update-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
            <path d="M3 3v5h5"/>
            <path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/>
            <path d="M16 16h5v5"/>
          </svg>
        </span>
        <span class="sw-update-message">A new version of STUR is available</span>
        <button class="sw-update-btn" type="button">Update Now</button>
        <button class="sw-update-dismiss" type="button" aria-label="Dismiss">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"/>
            <line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      </div>
    `;

    // Add styles
    const style = document.createElement('style');
    style.textContent = `
      #sw-update-notification {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 10000;
        animation: swUpdateSlideIn 0.3s ease-out;
      }

      @keyframes swUpdateSlideIn {
        from {
          opacity: 0;
          transform: translateX(-50%) translateY(20px);
        }
        to {
          opacity: 1;
          transform: translateX(-50%) translateY(0);
        }
      }

      @keyframes swUpdateSlideOut {
        from {
          opacity: 1;
          transform: translateX(-50%) translateY(0);
        }
        to {
          opacity: 0;
          transform: translateX(-50%) translateY(20px);
        }
      }

      .sw-update-content {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 16px;
        background: rgba(40, 40, 45, 0.95);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(74, 222, 128, 0.3);
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), 0 0 20px rgba(74, 222, 128, 0.1);
        font-family: inherit;
      }

      .sw-update-icon {
        width: 24px;
        height: 24px;
        color: #4ade80;
        flex-shrink: 0;
      }

      .sw-update-icon svg {
        width: 100%;
        height: 100%;
      }

      .sw-update-message {
        color: #e5e7eb;
        font-size: 14px;
        white-space: nowrap;
      }

      .sw-update-btn {
        background: linear-gradient(135deg, rgba(74, 222, 128, 0.9) 0%, rgba(34, 197, 94, 0.9) 100%);
        color: #000;
        border: none;
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 600;
        font-family: inherit;
        cursor: pointer;
        transition: all 0.2s ease;
        white-space: nowrap;
      }

      .sw-update-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(74, 222, 128, 0.3);
      }

      .sw-update-btn:active {
        transform: scale(0.98);
      }

      .sw-update-dismiss {
        width: 28px;
        height: 28px;
        padding: 4px;
        background: transparent;
        border: none;
        color: rgba(255, 255, 255, 0.5);
        cursor: pointer;
        border-radius: 6px;
        transition: all 0.2s ease;
        flex-shrink: 0;
      }

      .sw-update-dismiss:hover {
        color: rgba(255, 255, 255, 0.8);
        background: rgba(255, 255, 255, 0.1);
      }

      .sw-update-dismiss svg {
        width: 100%;
        height: 100%;
      }

      @media (max-width: 480px) {
        #sw-update-notification {
          left: 16px;
          right: 16px;
          transform: none;
          bottom: calc(16px + env(safe-area-inset-bottom, 0px));
        }

        @keyframes swUpdateSlideIn {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes swUpdateSlideOut {
          from {
            opacity: 1;
            transform: translateY(0);
          }
          to {
            opacity: 0;
            transform: translateY(20px);
          }
        }

        .sw-update-content {
          flex-wrap: wrap;
          justify-content: center;
          text-align: center;
        }

        .sw-update-message {
          flex: 1 1 100%;
          white-space: normal;
          margin-bottom: 4px;
        }

        .sw-update-dismiss {
          position: absolute;
          top: 8px;
          right: 8px;
        }
      }
    `;

    container.appendChild(style);

    // Event handlers
    const updateBtn = container.querySelector('.sw-update-btn');
    const dismissBtn = container.querySelector('.sw-update-dismiss');

    updateBtn.addEventListener('click', () => {
      updateBtn.textContent = 'Updating...';
      updateBtn.disabled = true;
      onUpdate();
    });

    dismissBtn.addEventListener('click', () => {
      container.style.animation = 'swUpdateSlideOut 0.3s ease-out forwards';
      setTimeout(() => container.remove(), 300);
    });

    return container;
  }

  /**
   * Show a temporary notification
   */
  function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `sw-notification sw-notification-${type}`;
    notification.setAttribute('role', 'status');
    notification.setAttribute('aria-live', 'polite');
    notification.textContent = message;

    const style = document.createElement('style');
    style.textContent = `
      .sw-notification {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        padding: 12px 24px;
        background: rgba(40, 40, 45, 0.95);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 8px;
        font-size: 14px;
        color: #e5e7eb;
        z-index: 10000;
        animation: swNotificationFade 3s ease-in-out forwards;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
      }

      .sw-notification-success {
        border: 1px solid rgba(74, 222, 128, 0.3);
      }

      .sw-notification-info {
        border: 1px solid rgba(96, 165, 250, 0.3);
      }

      @keyframes swNotificationFade {
        0% { opacity: 0; transform: translateX(-50%) translateY(20px); }
        10% { opacity: 1; transform: translateX(-50%) translateY(0); }
        90% { opacity: 1; transform: translateX(-50%) translateY(0); }
        100% { opacity: 0; transform: translateX(-50%) translateY(-10px); }
      }

      @media (max-width: 480px) {
        .sw-notification {
          left: 16px;
          right: 16px;
          transform: none;
          text-align: center;
          bottom: calc(16px + env(safe-area-inset-bottom, 0px));
        }

        @keyframes swNotificationFade {
          0% { opacity: 0; transform: translateY(20px); }
          10% { opacity: 1; transform: translateY(0); }
          90% { opacity: 1; transform: translateY(0); }
          100% { opacity: 0; transform: translateY(-10px); }
        }
      }
    `;

    notification.appendChild(style);
    document.body.appendChild(notification);

    // Remove after animation
    setTimeout(() => notification.remove(), 3000);
  }

  /**
   * Set up periodic update checks
   */
  function setupPeriodicUpdateCheck() {
    // Check for updates periodically
    setInterval(async () => {
      if (registration) {
        try {
          await registration.update();
          console.log('[SW Register] Checked for updates');
        } catch (error) {
          console.log('[SW Register] Update check failed:', error);
        }
      }
    }, UPDATE_CHECK_INTERVAL);

    // Also check when page becomes visible
    document.addEventListener('visibilitychange', async () => {
      if (document.visibilityState === 'visible' && registration) {
        try {
          await registration.update();
          console.log('[SW Register] Checked for updates on visibility change');
        } catch (error) {
          console.log('[SW Register] Update check failed:', error);
        }
      }
    });
  }

  /**
   * Public API for external access
   */
  window.STURServiceWorker = {
    /**
     * Force check for updates
     */
    checkForUpdates: async function() {
      if (registration) {
        try {
          await registration.update();
          return true;
        } catch (error) {
          console.error('[SW Register] Manual update check failed:', error);
          return false;
        }
      }
      return false;
    },

    /**
     * Clear the cache
     */
    clearCache: function() {
      return new Promise((resolve, reject) => {
        if (!registration || !registration.active) {
          reject(new Error('No active service worker'));
          return;
        }

        const messageChannel = new MessageChannel();
        messageChannel.port1.onmessage = (event) => {
          if (event.data.success) {
            resolve();
          } else {
            reject(new Error('Failed to clear cache'));
          }
        };

        registration.active.postMessage(
          { action: 'clearCache' },
          [messageChannel.port2]
        );
      });
    },

    /**
     * Get current cache size
     */
    getCacheSize: function() {
      return new Promise((resolve, reject) => {
        if (!registration || !registration.active) {
          reject(new Error('No active service worker'));
          return;
        }

        const messageChannel = new MessageChannel();
        messageChannel.port1.onmessage = (event) => {
          resolve(event.data.size);
        };

        registration.active.postMessage(
          { action: 'getCacheSize' },
          [messageChannel.port2]
        );
      });
    },

    /**
     * Get registration status
     */
    getStatus: function() {
      if (!registration) {
        return 'not-registered';
      }
      if (registration.installing) {
        return 'installing';
      }
      if (registration.waiting) {
        return 'waiting';
      }
      if (registration.active) {
        return 'active';
      }
      return 'unknown';
    }
  };

  // Initialize
  init();

})();
