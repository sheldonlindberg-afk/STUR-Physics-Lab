/**
 * STUR UI Utilities v1.0
 * Shared JavaScript for all STUR Physics Lab pages
 *
 * Import via: <script src="../assets/js/stur-ui.js"></script>
 */

(function(global) {
  'use strict';

  const STUR = {
    version: '1.0.0',
    framework: 'v9.2'
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
        id: 'stur-toast-container',
        style: 'position:fixed;bottom:1.5rem;right:1.5rem;z-index:9999;display:flex;flex-direction:column;gap:0.5rem;'
      });
      document.body.appendChild(toastContainer);
    }

    // Create toast element
    const toast = STUR.createElement('div', {
      className: `glass-toast ${type}`
    });

    // Icon based on type
    const iconMap = {
      success: 'check-circle',
      error: 'x-circle',
      warning: 'alert-circle',
      info: 'info'
    };

    toast.innerHTML = `
      <span class="stur-icon icon-${iconMap[type] || 'info'} md" style="color:var(--neon-${type === 'error' ? 'red' : type === 'success' ? 'green' : type === 'warning' ? 'gold' : 'cyan'})"></span>
      <span style="flex:1">${message}</span>
    `;

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

  /**
   * Initialize mobile nav toggle
   */
  STUR.initNav = function() {
    const toggle = STUR.$('.glass-nav-toggle');
    const links = STUR.$('.glass-nav-links');

    if (toggle && links) {
      toggle.addEventListener('click', () => {
        links.classList.toggle('open');
        toggle.setAttribute('aria-expanded', links.classList.contains('open'));
      });

      // Close on click outside
      document.addEventListener('click', (e) => {
        if (!toggle.contains(e.target) && !links.contains(e.target)) {
          links.classList.remove('open');
          toggle.setAttribute('aria-expanded', 'false');
        }
      });
    }
  };

  /**
   * Create standard navigation HTML
   */
  STUR.createNavHTML = function(currentPage) {
    const pages = [
      { id: 'index', label: 'Index', href: '../index.html' },
      { id: 'foundations', label: 'Foundations', href: 'stur_foundations.html' },
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

    // Add keyboard handlers
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
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
