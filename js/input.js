class InputHandler {
    constructor() {
        this.keys = {
            right: false,
            left: false,
            up: false
        };

        // Prevent default behavior for game control keys
        window.addEventListener('keydown', (e) => {
            // Prevent scrolling for arrow keys and space
            if(['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', ' '].includes(e.key)) {
                e.preventDefault();
            }
            
            switch(e.key) {
                case 'ArrowRight':
                    this.keys.right = true;
                    break;
                case 'ArrowLeft':
                    this.keys.left = true;
                    break;
                case 'ArrowUp':
                case ' ':
                    this.keys.up = true;
                    break;
            }
        });

        window.addEventListener('keyup', (e) => {
            switch(e.key) {
                case 'ArrowRight':
                    this.keys.right = false;
                    break;
                case 'ArrowLeft':
                    this.keys.left = false;
                    break;
                case 'ArrowUp':
                case ' ':
                    this.keys.up = false;
                    break;
            }
        });
    }
} 