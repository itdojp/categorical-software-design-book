/**
 * Mermaid renderer for GitHub Pages (client-side).
 *
 * - Detects fenced code blocks tagged as `mermaid` by Rouge/Kramdown.
 * - Replaces them with `<div class="mermaid">` nodes.
 * - Loads Mermaid from CDN only when needed.
 * - Re-renders on theme toggle (light/dark).
 */

(function () {
    'use strict';

    const MERMAID_VERSION = '10.9.1';
    const MERMAID_CDN_URL = `https://cdn.jsdelivr.net/npm/mermaid@${MERMAID_VERSION}/dist/mermaid.min.js`;

    function findMermaidCodeBlocks() {
        return Array.from(
            document.querySelectorAll(
                'code.language-mermaid, code.lang-mermaid, code[class*="language-mermaid"], code[class*="lang-mermaid"]'
            )
        );
    }

    function getTheme() {
        const t = document.documentElement.getAttribute('data-theme');
        return t === 'dark' ? 'dark' : 'default';
    }

    function loadMermaidIfNeeded() {
        if (window.mermaid) return Promise.resolve(window.mermaid);

        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = MERMAID_CDN_URL;
            script.async = true;
            script.onload = () => resolve(window.mermaid);
            script.onerror = () => reject(new Error('Failed to load Mermaid from CDN'));
            document.head.appendChild(script);
        });
    }

    function replaceCodeBlock(codeEl) {
        const source = (codeEl.textContent || '').trim();
        if (!source) return null;

        const pre = codeEl.closest('pre');
        if (!pre) return null;

        // Jekyll/Rouge often wraps code blocks as:
        // <div class="language-mermaid highlighter-rouge"><div class="highlight"><pre>...</pre></div></div>
        const outer =
            pre.closest('.highlighter-rouge') ||
            pre.closest('.highlight') ||
            pre;

        const wrapper = document.createElement('div');
        wrapper.className = 'mermaid-wrapper';

        const mermaidEl = document.createElement('div');
        mermaidEl.className = 'mermaid';
        mermaidEl.setAttribute('data-mermaid-source', source);
        mermaidEl.textContent = source;

        wrapper.appendChild(mermaidEl);
        outer.replaceWith(wrapper);

        return mermaidEl;
    }

    function restoreSources(nodes) {
        nodes.forEach((node) => {
            const src = node.getAttribute('data-mermaid-source') || '';
            node.removeAttribute('data-processed');
            node.textContent = src;
        });
    }

    function renderAll() {
        if (!window.mermaid) return;

        const nodes = Array.from(document.querySelectorAll('.mermaid[data-mermaid-source]'));
        if (nodes.length === 0) return;

        // Restore original source so re-render is deterministic across theme changes.
        restoreSources(nodes);

        try {
            window.mermaid.initialize({
                startOnLoad: false,
                securityLevel: 'strict',
                theme: getTheme(),
                flowchart: { useMaxWidth: true },
            });
        } catch (e) {
            // If initialize fails, do not block page rendering.
            console.warn('Mermaid initialize failed:', e);
        }

        try {
            if (typeof window.mermaid.run === 'function') {
                window.mermaid.run({ nodes });
            } else if (typeof window.mermaid.init === 'function') {
                window.mermaid.init(undefined, nodes);
            }
        } catch (e) {
            console.warn('Mermaid render failed:', e);
        }
    }

    function init() {
        const codeBlocks = findMermaidCodeBlocks();
        if (codeBlocks.length === 0) return;

        // Replace code blocks before loading Mermaid so the DOM is ready for rendering.
        codeBlocks.forEach(replaceCodeBlock);

        loadMermaidIfNeeded()
            .then(() => renderAll())
            .catch((e) => console.warn(String(e && e.message ? e.message : e)));

        // Re-render on theme toggle (diagram theme is baked into SVG).
        const themeToggle = document.querySelector('.theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                setTimeout(renderAll, 0);
            });
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();

