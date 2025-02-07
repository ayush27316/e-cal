// Wait for the page to load completely before executing the script
let currentIndex = -1; 



if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initNavigation);
} else {
    initNavigation();
}

function initNavigation() {
    console.log("Content script loaded");

    // Collect all navigation links in a flat array
    // Collect all navigation links in a flat array and normalize them
    const navLinks = Array.from(document.querySelectorAll('.nav a'))
    .map(link => ({
        element: link,
        href: normalizeUrl(link.href)  // Store normalized URLs
    }));

    console.log("Found links:", navLinks.map(link => link.href));

    if (navLinks.length === 0) {
        console.warn("No navigation links found. Check your selector.");
        return;
    }

    function normalizeUrl(url) {
        let parsedUrl = new URL(url, window.location.origin);
        let path = parsedUrl.pathname;
        return path.endsWith('/') ? path : path + '/'; // Ensure trailing slash
    }
    

    
    // Find the index of the current page in the navLinks array
    const currentPageUrl = normalizeUrl(window.location.href);
    console.log("Normalized current URL:", currentPageUrl);
    console.log("Normalized nav links:", navLinks.map(link => normalizeUrl(link.href)));

    currentIndex = navLinks.findIndex(linkObj => linkObj.href === currentPageUrl);

    // If current page is not found in navLinks, start from the first link
    if (currentIndex === -1) {
        console.warn("Current page not found in navigation links. Defaulting to first link.");
        currentIndex = 0;
    }

    console.log("Initialized currentIndex:", currentIndex, "Current Page:", currentPageUrl);

    document.addEventListener('keydown', (event) => {
        console.log(`Key pressed: ${event.key}, Ctrl: ${event.ctrlKey}, Shift: ${event.shiftKey}`);

        if (event.ctrlKey && event.shiftKey && event.key === 'ArrowRight') {
            event.preventDefault();
            navigateNext(navLinks);
        }
        
        if (event.ctrlKey && event.shiftKey && event.key === 'ArrowLeft') {
            event.preventDefault();
            navigatePrevious(navLinks);
        }
    });
}

function navigateNext(navLinks) {
    if (navLinks.length === 0) return;
    
    currentIndex = (currentIndex + 1) % navLinks.length;
    console.log("Navigating to next:", navLinks[currentIndex].href);
    window.location.href = navLinks[currentIndex].href;  // Navigate to the link
}

function navigatePrevious(navLinks) {
    if (navLinks.length === 0) return;
    
    currentIndex = (currentIndex - 1 + navLinks.length) % navLinks.length;
    console.log("Navigating to previous:", navLinks[currentIndex].href);
    window.location.href = navLinks[currentIndex].href;  // Navigate to the link
}
