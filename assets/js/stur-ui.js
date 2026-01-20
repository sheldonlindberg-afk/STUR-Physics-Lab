/**
 * STUR UI Utilities
 * Shared JavaScript for all STUR Physics Lab pages
 * Complete Theory Edition (MHP + DHP)
 *
 * Import via: <script src="../assets/js/stur-ui.js"></script>
 */

(function(global) {
  'use strict';

  const STUR = {
    versionName: 'Complete Theory'
  };

  // ============================================================
  // SAFE DOM UTILITIES
  // ============================================================

  /**
   * Safe DOM query - returns null if element not found
   */
  STUR.$ = function(selector, context) {
    return (context || document).querySelector(selector);
  };

  /**
   * Safe DOM query all - returns empty array if no elements found
   */
  STUR.$$ = function(selector, context) {
    return Array.from((context || document).querySelectorAll(selector));
  };

  /**
   * Safe element creation
   */
  STUR.createElement = function(tag, attrs, children) {
    const el = document.createElement(tag);
    if (attrs) {
      Object.entries(attrs).forEach(([key, value]) => {
        if (key === 'className') {
          el.className = value;
        } else if (key === 'dataset') {
          Object.entries(value).forEach(([k, v]) => el.dataset[k] = v);
        } else if (key.startsWith('on')) {
          el.addEventListener(key.slice(2).toLowerCase(), value);
        } else {
          el.setAttribute(key, value);
        }
      });
    }
    if (children) {
      if (typeof children === 'string') {
        el.textContent = children;
      } else if (Array.isArray(children)) {
        children.forEach(child => {
          if (child) el.appendChild(typeof child === 'string' ? document.createTextNode(child) : child);
        });
      } else {
        el.appendChild(children);
      }
    }
    return el;
  };

  // ============================================================
  // SHARE FUNCTIONALITY
  // ============================================================

  let shareMenuEl = null;

  /**
   * Social share platforms configuration
   */
  const sharePlatforms = [
    {
      id: 'copy',
      label: 'Copy Link',
      icon: 'link',
      color: '#4ade80',
      action: 'copy'
    },
    {
      id: 'x',
      label: 'X (Twitter)',
      icon: 'x',
      color: '#000000',
      url: 'https://twitter.com/intent/tweet?url={url}&text={title}'
    },
    {
      id: 'facebook',
      label: 'Facebook',
      icon: 'facebook',
      color: '#1877f2',
      url: 'https://www.facebook.com/sharer/sharer.php?u={url}'
    },
    {
      id: 'linkedin',
      label: 'LinkedIn',
      icon: 'linkedin',
      color: '#0a66c2',
      url: 'https://www.linkedin.com/sharing/share-offsite/?url={url}'
    },
    {
      id: 'reddit',
      label: 'Reddit',
      icon: 'reddit',
      color: '#ff4500',
      url: 'https://reddit.com/submit?url={url}&title={title}'
    },
    {
      id: 'email',
      label: 'Email',
      icon: 'mail',
      color: '#64748b',
      url: 'mailto:?subject={title}&body={url}'
    }
  ];

  /**
   * Create share menu element
   */
  function createShareMenu() {
    if (shareMenuEl) return shareMenuEl;

    shareMenuEl = STUR.createElement('div', {
      id: 'stur-share-menu',
      className: 'stur-share-menu'
    });

    shareMenuEl.innerHTML = `
      <div class="stur-share-menu-content">
        <div class="stur-share-menu-header">
          <span>Share</span>
          <button class="stur-share-menu-close" aria-label="Close">&times;</button>
        </div>
        <div class="stur-share-menu-options">
          ${sharePlatforms.map(p => `
            <button class="stur-share-option" data-platform="${p.id}" style="--platform-color: ${p.color}">
              <span class="stur-share-icon stur-share-icon-${p.icon}"></span>
              <span class="stur-share-label">${p.label}</span>
            </button>
          `).join('')}
        </div>
      </div>
    `;

    // Add styles if not already present
    if (!document.getElementById('stur-share-styles')) {
      const styles = document.createElement('style');
      styles.id = 'stur-share-styles';
      styles.textContent = `
        .stur-share-menu {
          position: fixed;
          inset: 0;
          background: rgba(0, 0, 0, 0.75);
          backdrop-filter: blur(8px);
          -webkit-backdrop-filter: blur(8px);
          display: flex;
          align-items: flex-end;
          justify-content: center;
          z-index: 10000;
          opacity: 0;
          visibility: hidden;
          transition: opacity 0.25s ease, visibility 0.25s ease;
          padding: 0;
          padding-bottom: env(safe-area-inset-bottom, 0);
        }
        .stur-share-menu.open {
          opacity: 1;
          visibility: visible;
        }
        .stur-share-menu-content {
          background: linear-gradient(180deg, rgba(15, 23, 42, 0.98) 0%, rgba(10, 15, 30, 0.99) 100%);
          border: 1px solid rgba(255, 255, 255, 0.1);
          border-bottom: none;
          border-radius: 20px 20px 0 0;
          padding: 0;
          width: 100%;
          max-width: 420px;
          max-height: 85vh;
          box-shadow: 0 -10px 40px rgba(0, 0, 0, 0.5);
          transform: translateY(100%);
          transition: transform 0.3s cubic-bezier(0.32, 0.72, 0, 1);
          overflow: hidden;
        }
        .stur-share-menu.open .stur-share-menu-content {
          transform: translateY(0);
        }
        .stur-share-menu-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 18px 20px 14px;
          border-bottom: 1px solid rgba(255, 255, 255, 0.08);
          font-weight: 600;
          font-size: 17px;
          color: var(--text-main, #f1f5f9);
        }
        .stur-share-menu-header::before {
          content: '';
          position: absolute;
          top: 8px;
          left: 50%;
          transform: translateX(-50%);
          width: 36px;
          height: 4px;
          background: rgba(255, 255, 255, 0.2);
          border-radius: 2px;
        }
        .stur-share-menu-close {
          background: rgba(255, 255, 255, 0.1);
          border: none;
          color: var(--text-muted, #94a3b8);
          font-size: 20px;
          cursor: pointer;
          padding: 0;
          width: 32px;
          height: 32px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          line-height: 1;
          transition: background 0.15s, color 0.15s;
        }
        .stur-share-menu-close:hover,
        .stur-share-menu-close:focus {
          background: rgba(255, 255, 255, 0.15);
          color: var(--text-main, #f1f5f9);
        }
        .stur-share-menu-options {
          padding: 16px 16px 24px;
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 12px;
        }
        .stur-share-option {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 10px;
          padding: 18px 12px;
          background: rgba(255, 255, 255, 0.04);
          border: 1px solid rgba(255, 255, 255, 0.06);
          border-radius: 14px;
          cursor: pointer;
          transition: all 0.2s ease;
          color: var(--text-main, #f1f5f9);
          -webkit-tap-highlight-color: transparent;
          min-height: 90px;
        }
        .stur-share-option:hover,
        .stur-share-option:focus {
          background: rgba(255, 255, 255, 0.08);
          border-color: var(--platform-color);
          transform: scale(1.02);
          outline: none;
        }
        .stur-share-option:active {
          transform: scale(0.97);
          background: rgba(255, 255, 255, 0.12);
        }
        .stur-share-icon {
          width: 44px;
          height: 44px;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 12px;
          background: var(--platform-color);
          color: white;
          font-size: 18px;
          font-weight: bold;
          flex-shrink: 0;
        }
        .stur-share-icon-link::before { content: "🔗"; font-size: 20px; }
        .stur-share-icon-x::before { content: "𝕏"; font-family: serif; font-size: 20px; }
        .stur-share-icon-facebook::before { content: "f"; font-family: Georgia, serif; font-size: 22px; }
        .stur-share-icon-linkedin::before { content: "in"; font-size: 14px; font-weight: 700; }
        .stur-share-icon-reddit::before { content: "r/"; font-size: 13px; }
        .stur-share-icon-mail::before { content: "✉"; font-size: 18px; }
        .stur-share-label {
          font-size: 12px;
          font-weight: 500;
          color: var(--text-muted, #94a3b8);
          text-align: center;
          line-height: 1.3;
        }
        /* Desktop: center the modal */
        @media (min-width: 481px) {
          .stur-share-menu {
            align-items: center;
            padding: 1.5rem;
          }
          .stur-share-menu-content {
            border-radius: 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            transform: scale(0.95) translateY(20px);
            max-width: 380px;
          }
          .stur-share-menu.open .stur-share-menu-content {
            transform: scale(1) translateY(0);
          }
          .stur-share-menu-header::before {
            display: none;
          }
        }
        /* Small mobile: 2-column grid */
        @media (max-width: 360px) {
          .stur-share-menu-options {
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            padding: 14px 14px 20px;
          }
          .stur-share-option {
            padding: 14px 10px;
            min-height: 80px;
          }
          .stur-share-icon {
            width: 40px;
            height: 40px;
          }
        }
      `;
      document.head.appendChild(styles);
    }

    document.body.appendChild(shareMenuEl);

    // Close button handler
    shareMenuEl.querySelector('.stur-share-menu-close').addEventListener('click', () => {
      STUR.closeShareMenu();
    });

    // Click outside to close
    shareMenuEl.addEventListener('click', (e) => {
      if (e.target === shareMenuEl) {
        STUR.closeShareMenu();
      }
    });

    // Platform button handlers
    shareMenuEl.querySelectorAll('.stur-share-option').forEach(btn => {
      btn.addEventListener('click', () => {
        const platformId = btn.dataset.platform;
        const platform = sharePlatforms.find(p => p.id === platformId);
        if (platform) {
          handleShare(platform);
        }
      });
    });

    return shareMenuEl;
  }

  /**
   * Handle share action for a platform
   */
  function handleShare(platform) {
    const url = encodeURIComponent(window.location.href);
    const title = encodeURIComponent(document.title);

    if (platform.action === 'copy') {
      STUR.copyToClipboard(window.location.href, 'Link copied!');
      STUR.closeShareMenu();
    } else if (platform.url) {
      const shareUrl = platform.url
        .replace('{url}', url)
        .replace('{title}', title);
      window.open(shareUrl, '_blank', 'width=600,height=400,menubar=no,toolbar=no');
      STUR.closeShareMenu();
    }
  }

  /**
   * Open share menu
   */
  STUR.openShareMenu = function() {
    const menu = createShareMenu();
    requestAnimationFrame(() => {
      menu.classList.add('open');
    });
    document.body.style.overflow = 'hidden';
  };

  /**
   * Close share menu
   */
  STUR.closeShareMenu = function() {
    if (shareMenuEl) {
      shareMenuEl.classList.remove('open');
      document.body.style.overflow = '';
    }
  };

  /**
   * Share function for nav button (replaces old shareRepo)
   */
  STUR.share = function() {
    // Try native share API first (mobile)
    if (navigator.share) {
      navigator.share({
        title: document.title,
        url: window.location.href
      }).catch(() => {
        // User cancelled or error, fall back to menu
        STUR.openShareMenu();
      });
    } else {
      STUR.openShareMenu();
    }
  };

  // ============================================================
  // CLIPBOARD / COPY UTILITIES
  // ============================================================

  /**
   * Copy text to clipboard with fallback
   */
  STUR.copyToClipboard = async function(text, successMessage) {
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(text);
      } else {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
      }
      STUR.toast(successMessage || 'Copied to clipboard', 'success');
      return true;
    } catch (err) {
      STUR.toast('Failed to copy', 'error');
      console.error('Copy failed:', err);
      return false;
    }
  };

  /**
   * Copy content from a textarea or code element
   */
  STUR.copyFromElement = function(elementId, label) {
    const el = document.getElementById(elementId);
    if (!el) {
      console.warn('Element not found:', elementId);
      return false;
    }
    const text = el.value || el.textContent;
    return STUR.copyToClipboard(text, label ? `${label} copied` : 'Copied');
  };

  // ============================================================
  // TOAST / NOTIFICATION SYSTEM
  // ============================================================

  let toastContainer = null;

  /**
   * Show a toast notification
   */
  STUR.toast = function(message, type, duration) {
    type = type || 'info';
    duration = duration || 3000;

    // Create container if needed
    if (!toastContainer) {
      toastContainer = STUR.createElement('div', {
        id: 'stur-toast-container'
      });
      // Apply styles that work well on mobile
      toastContainer.style.cssText = `
        position: fixed;
        bottom: max(1rem, env(safe-area-inset-bottom, 1rem));
        left: 1rem;
        right: 1rem;
        z-index: 9999;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
        pointer-events: none;
      `;
      document.body.appendChild(toastContainer);
    }

    // Create toast element
    const toast = STUR.createElement('div', {
      className: `glass-toast ${type}`
    });

    // Make toast clickable/dismissible
    toast.style.pointerEvents = 'auto';
    toast.style.maxWidth = '360px';
    toast.style.width = '100%';

    // Icon based on type
    const iconMap = {
      success: 'check-circle',
      error: 'x-circle',
      warning: 'alert-circle',
      info: 'info'
    };

    toast.innerHTML = `
      <span class="stur-icon icon-${iconMap[type] || 'info'} md" style="color:var(--neon-${type === 'error' ? 'red' : type === 'success' ? 'green' : type === 'warning' ? 'gold' : 'cyan'});flex-shrink:0"></span>
      <span style="flex:1">${message}</span>
    `;

    // Allow dismissing by clicking
    toast.addEventListener('click', () => {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), 300);
    });

    toastContainer.appendChild(toast);

    // Animate in
    requestAnimationFrame(() => {
      toast.classList.add('show');
    });

    // Auto dismiss
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), 300);
    }, duration);
  };

  // ============================================================
  // EXPORT / DOWNLOAD UTILITIES
  // ============================================================

  /**
   * Download data as a file
   */
  STUR.download = function(data, filename, mimeType) {
    mimeType = mimeType || 'application/octet-stream';
    const blob = new Blob([data], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
    STUR.toast(`Downloaded ${filename}`, 'success');
  };

  /**
   * Export data as JSON
   */
  STUR.exportJSON = function(data, filename) {
    filename = filename || `stur-export-${Date.now()}.json`;
    const json = JSON.stringify(data, null, 2);
    STUR.download(json, filename, 'application/json');
  };

  /**
   * Export data as CSV
   */
  STUR.exportCSV = function(data, filename, headers) {
    filename = filename || `stur-export-${Date.now()}.csv`;

    let csv = '';

    // Headers
    if (headers) {
      csv += headers.join(',') + '\n';
    } else if (data.length > 0 && typeof data[0] === 'object') {
      csv += Object.keys(data[0]).join(',') + '\n';
    }

    // Data rows
    data.forEach(row => {
      if (Array.isArray(row)) {
        csv += row.map(v => `"${String(v).replace(/"/g, '""')}"`).join(',') + '\n';
      } else if (typeof row === 'object') {
        csv += Object.values(row).map(v => `"${String(v).replace(/"/g, '""')}"`).join(',') + '\n';
      }
    });

    STUR.download(csv, filename, 'text/csv');
  };

  // ============================================================
  // STANDARD STUR DATA SCHEMA
  // ============================================================

  /**
   * Create standard STUR export schema
   */
  STUR.createExportSchema = function(pageId, params, predictions, results, rawData) {
    return {
      meta: {
        page: pageId,
        version: STUR.framework,
        timestamp: new Date().toISOString(),
        exportVersion: STUR.version
      },
      params: params || {},
      predictions: predictions || {},
      results: results || {
        fitMetrics: {},
        decision: null
      },
      data: rawData || { x: [], y: [] }
    };
  };

  // ============================================================
  // NAVIGATION UTILITIES
  // ============================================================

  // Track if nav has been initialized to prevent double-init
  let navInitialized = false;

  /**
   * Initialize mobile nav toggle - robust, mobile-first implementation
   */
  STUR.initNav = function() {
    // Prevent double initialization
    if (navInitialized) return;

    const toggle = STUR.$('.glass-nav-toggle');
    const links = STUR.$('.glass-nav-links');

    if (!toggle || !links) {
      // Elements not found, skip init
      return;
    }

    navInitialized = true;

    // State
    let isOpen = false;

    /**
     * Open the mobile menu
     */
    const openMenu = () => {
      if (isOpen) return;
      isOpen = true;
      links.classList.add('open');
      toggle.setAttribute('aria-expanded', 'true');
      toggle.innerHTML = '<span class="stur-icon icon-x lg"></span>';
      document.body.style.overflow = 'hidden';
    };

    /**
     * Close the mobile menu
     */
    const closeMenu = () => {
      if (!isOpen) return;
      isOpen = false;
      links.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.innerHTML = '<span class="stur-icon icon-menu lg"></span>';
      document.body.style.overflow = '';
    };

    /**
     * Toggle the mobile menu
     */
    const toggleMenu = () => {
      if (isOpen) {
        closeMenu();
      } else {
        openMenu();
      }
    };

    // ============================================================
    // TOGGLE BUTTON - Simple click handler only
    // Using only click (not touchend) prevents double-firing issues
    // Modern mobile browsers handle click properly with ~300ms delay removed
    // ============================================================
    toggle.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      toggleMenu();
    });

    // ============================================================
    // MENU LINK CLICKS - Close menu when a link is clicked
    // Use event delegation for reliability
    // ============================================================
    links.addEventListener('click', function(e) {
      const link = e.target.closest('.glass-nav-link');
      if (!link) return;

      // Always close menu after clicking a link
      // Share button will open its own modal, but menu should still close
      closeMenu();
    });

    // ============================================================
    // CLOSE ON OUTSIDE CLICK - Using capture phase for reliability
    // ============================================================
    document.addEventListener('click', function(e) {
      if (!isOpen) return;

      // Check if click is outside both toggle and menu
      if (!toggle.contains(e.target) && !links.contains(e.target)) {
        closeMenu();
      }
    }, true); // Use capture phase

    // ============================================================
    // CLOSE ON ESCAPE KEY
    // ============================================================
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && isOpen) {
        closeMenu();
        toggle.focus();
      }
    });

    // ============================================================
    // CLOSE ON RESIZE to desktop
    // ============================================================
    let resizeTimer;
    window.addEventListener('resize', function() {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function() {
        // Close if resized to desktop width
        if (window.innerWidth > 768 && isOpen) {
          closeMenu();
        }
      }, 150);
    });

    // Expose close function for programmatic use
    STUR.closeNav = closeMenu;
  };

  /**
   * Create standard navigation HTML
   */
  STUR.createNavHTML = function(currentPage) {
    const pages = [
      { id: 'index', label: 'Index', href: '../index.html' },
      { id: 'foundations', label: 'Foundations', href: 'stur_core_theory.html' },
      { id: 'unified', label: 'Framework', href: 'stur_unified_framework.html' },
      { id: 'verifier', label: 'Verifier', href: 'stur_geometry_verifier.html' },
      { id: 'sandbox', label: 'Sandbox', href: 'stur_sandbox.html' }
    ];

    return `
      <header class="glass-header">
        <nav class="glass-nav">
          <a href="../index.html" class="glass-nav-brand">
            <span class="stur-icon icon-atom lg"></span>
            STUR Lab
          </a>
          <button class="glass-nav-toggle" aria-label="Toggle navigation" aria-expanded="false">
            <span class="stur-icon icon-menu lg"></span>
          </button>
          <div class="glass-nav-links">
            ${pages.map(p => `
              <a href="${p.href}" class="glass-nav-link${currentPage === p.id ? ' active' : ''}">${p.label}</a>
            `).join('')}
            <a href="https://github.com/sheldonlindberg/STUR-Physics-Lab" target="_blank" rel="noopener" class="glass-nav-link">
              <span class="stur-icon icon-github"></span>
            </a>
          </div>
        </nav>
      </header>
    `;
  };

  // ============================================================
  // FALSIFICATION UTILITIES
  // ============================================================

  /**
   * Calculate RMSE between prediction and data
   */
  STUR.calcRMSE = function(predicted, observed) {
    if (predicted.length !== observed.length || predicted.length === 0) {
      return NaN;
    }
    const sumSq = predicted.reduce((sum, p, i) => {
      const diff = p - observed[i];
      return sum + diff * diff;
    }, 0);
    return Math.sqrt(sumSq / predicted.length);
  };

  /**
   * Calculate chi-squared statistic
   */
  STUR.calcChiSquared = function(predicted, observed, errors) {
    if (predicted.length !== observed.length || predicted.length === 0) {
      return NaN;
    }
    return predicted.reduce((sum, p, i) => {
      const sigma = errors ? errors[i] : 1;
      const diff = (p - observed[i]) / sigma;
      return sum + diff * diff;
    }, 0);
  };

  /**
   * Calculate AIC (Akaike Information Criterion)
   */
  STUR.calcAIC = function(n, k, rss) {
    // n = number of data points, k = number of parameters, rss = residual sum of squares
    return n * Math.log(rss / n) + 2 * k;
  };

  /**
   * Calculate BIC (Bayesian Information Criterion)
   */
  STUR.calcBIC = function(n, k, rss) {
    return n * Math.log(rss / n) + k * Math.log(n);
  };

  /**
   * Determine pass/fail verdict
   */
  STUR.getVerdict = function(metrics, thresholds) {
    thresholds = thresholds || { rmse: 0.1, deltaAIC: 2 };

    const verdict = {
      pass: true,
      reasons: []
    };

    if (metrics.rmse !== undefined && metrics.rmse > thresholds.rmse) {
      verdict.pass = false;
      verdict.reasons.push(`RMSE ${metrics.rmse.toFixed(4)} > threshold ${thresholds.rmse}`);
    }

    if (metrics.deltaAIC !== undefined && metrics.deltaAIC > thresholds.deltaAIC) {
      verdict.pass = false;
      verdict.reasons.push(`ΔAIC ${metrics.deltaAIC.toFixed(2)} favors competitor model`);
    }

    return verdict;
  };

  // ============================================================
  // MATHJAX EQUATION COLOR SYSTEM
  // ============================================================

  /**
   * Physics domain colors for equation color coding
   */
  STUR.eqColors = {
    diffusion: '#4ade80',  // Green - Kinetic/Diffusion: ½(∇R)²
    potential: '#f472b6',  // Pink - Relaxation Potential: V(R)
    xcrm: '#fbbf24',       // Gold - XCRM Coupling: χR∂_X R
    torsion: '#60a5fa',    // Blue - Torsion Source: αR𝕋
    quantum: '#a78bfa',    // Violet - Loop corrections, holonomy
    matter: '#22d3ee'      // Cyan - Matter fields: ℒ_matter
  };

  /**
   * Configure MathJax with STUR color macros
   * Call this before MathJax loads or use MathJax.startup.promise
   */
  STUR.configureMathJax = function() {
    // Extend MathJax configuration with STUR macros
    if (typeof window.MathJax === 'undefined') {
      window.MathJax = { tex: { macros: {} }, svg: { fontCache: 'global' } };
    }
    if (!window.MathJax.tex) window.MathJax.tex = {};
    if (!window.MathJax.tex.macros) window.MathJax.tex.macros = {};

    // Add color macros for physics domains
    Object.assign(window.MathJax.tex.macros, {
      // Physics domain color macros
      Diff: ['\\color{' + STUR.eqColors.diffusion + '}{#1}', 1],
      Pot: ['\\color{' + STUR.eqColors.potential + '}{#1}', 1],
      XCRM: ['\\color{' + STUR.eqColors.xcrm + '}{#1}', 1],
      Tor: ['\\color{' + STUR.eqColors.torsion + '}{#1}', 1],
      Quant: ['\\color{' + STUR.eqColors.quantum + '}{#1}', 1],
      Matt: ['\\color{' + STUR.eqColors.matter + '}{#1}', 1],
      // Common physics symbols
      Rcal: '\\mathcal{R}',
      Mcal: '\\mathcal{M}',
      Lcal: '\\mathcal{L}',
      Tcal: '\\mathcal{T}'
    });

    // If MathJax already loaded, re-typeset
    if (window.MathJax && window.MathJax.typeset) {
      window.MathJax.typeset();
    }
  };

  /**
   * Add equation legend to page if not present
   */
  STUR.addEquationLegend = function(containerId) {
    const container = document.getElementById(containerId) || document.querySelector('.container');
    if (!container || container.querySelector('.physics-legend')) return;

    const legend = STUR.createElement('div', { className: 'physics-legend' });
    legend.innerHTML = `
      <div class="physics-legend-title">Equation Color Code — Physics Domains</div>
      <div class="physics-legend-item"><span class="physics-legend-dot diffusion"></span><span class="eq-diffusion">Diffusion</span></div>
      <div class="physics-legend-item"><span class="physics-legend-dot potential"></span><span class="eq-potential">Potential</span></div>
      <div class="physics-legend-item"><span class="physics-legend-dot xcrm"></span><span class="eq-xcrm">XCRM</span></div>
      <div class="physics-legend-item"><span class="physics-legend-dot torsion"></span><span class="eq-torsion">Torsion</span></div>
      <div class="physics-legend-item"><span class="physics-legend-dot quantum"></span><span class="eq-quantum">Quantum</span></div>
      <div class="physics-legend-item"><span class="physics-legend-dot matter"></span><span class="eq-matter">Matter</span></div>
    `;
    const firstSection = container.querySelector('.section, .glass-panel');
    if (firstSection) {
      container.insertBefore(legend, firstSection);
    } else {
      container.prepend(legend);
    }
  };

  // ============================================================
  // VERSION STAMP
  // ============================================================

  /**
   * Get version stamp HTML
   */
  STUR.getVersionStamp = function() {
    const now = new Date();
    return `
      <div class="stur-version-stamp" style="font-size:0.72rem;color:var(--text-dim);text-align:center;margin-top:2rem;padding:0.5rem;border-top:1px solid var(--border-dim);">
        STUR Framework ${STUR.framework} | Generated ${now.toISOString().split('T')[0]} | UI v${STUR.version}
      </div>
    `;
  };

  // ============================================================
  // MODAL UTILITIES
  // ============================================================

  /**
   * Open a modal
   */
  STUR.openModal = function(modalId) {
    const overlay = document.getElementById(modalId);
    if (overlay) {
      overlay.classList.add('open');
      document.body.style.overflow = 'hidden';
    }
  };

  /**
   * Close a modal
   */
  STUR.closeModal = function(modalId) {
    const overlay = document.getElementById(modalId);
    if (overlay) {
      overlay.classList.remove('open');
      document.body.style.overflow = '';
    }
  };

  /**
   * Initialize modal close handlers
   */
  STUR.initModals = function() {
    STUR.$$('.glass-modal-overlay').forEach(overlay => {
      overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
          overlay.classList.remove('open');
          document.body.style.overflow = '';
        }
      });
    });

    STUR.$$('.glass-modal-close').forEach(btn => {
      btn.addEventListener('click', () => {
        const overlay = btn.closest('.glass-modal-overlay');
        if (overlay) {
          overlay.classList.remove('open');
          document.body.style.overflow = '';
        }
      });
    });
  };

  // ============================================================
  // INITIALIZATION
  // ============================================================

  /**
   * Initialize all STUR UI components
   */
  STUR.init = function() {
    STUR.initNav();
    STUR.initModals();

    // Add global keyboard handlers
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        // Close share menu if open
        if (shareMenuEl && shareMenuEl.classList.contains('open')) {
          STUR.closeShareMenu();
          return;
        }

        // Close any open modals
        STUR.$$('.glass-modal-overlay.open').forEach(overlay => {
          overlay.classList.remove('open');
          document.body.style.overflow = '';
        });
      }
    });

    console.log(`STUR UI v${STUR.version} initialized`);
  };

  // Auto-init on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', STUR.init);
  } else {
    STUR.init();
  }

  // Expose to global
  global.STUR = STUR;

})(typeof window !== 'undefined' ? window : this);
