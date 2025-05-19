// Wait for the game to load and initialize
window.addEventListener('load', () => {
    // Give the game a moment to render
    setTimeout(() => {
        const canvas = document.getElementById('gameCanvas');
        
        // Create a download link
        const link = document.createElement('a');
        link.download = 'super-mario-clone-screenshot.png';
        link.href = canvas.toDataURL('image/png');
        
        // Add the link to the page
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }, 2000); // Wait 2 seconds for game to render
}); 