class Game {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.canvas.width = 800;
        this.canvas.height = 600;
        
        this.input = new InputHandler();
        this.player = new Player(this.canvas.width, this.canvas.height);
        this.sprites = new SpriteManager();
        
        // Add obstacle management
        this.obstacles = [];
        this.obstacleTimer = 0;
        this.obstacleInterval = 2000; // New obstacle every 2 seconds
        this.lastTime = 0;
        this.gameOver = false;
        
        this.gameLoop = this.gameLoop.bind(this);
        requestAnimationFrame(this.gameLoop);
    }

    update(deltaTime) {
        if (this.gameOver) return;

        this.player.update(this.input);

        // Update obstacle timer
        this.obstacleTimer += deltaTime;
        if (this.obstacleTimer > this.obstacleInterval) {
            this.obstacles.push(new Obstacle(this.canvas.width, this.canvas.height));
            this.obstacleTimer = 0;
        }

        // Update obstacles and check collisions
        this.obstacles = this.obstacles.filter(obstacle => {
            obstacle.update();
            if (obstacle.collidesWith(this.player)) {
                this.gameOver = true;
            }
            return !obstacle.isOffScreen();
        });
    }

    draw() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw background
        this.ctx.fillStyle = '#6b8cff';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw ground
        this.ctx.fillStyle = '#5c3c00';
        this.ctx.fillRect(0, this.canvas.height - 10, this.canvas.width, 10);
        
        this.player.draw(this.ctx);
        
        // Draw obstacles
        this.obstacles.forEach(obstacle => obstacle.draw(this.ctx));

        // Draw game over message
        if (this.gameOver) {
            this.ctx.fillStyle = 'black';
            this.ctx.font = '48px Arial';
            this.ctx.fillText('Game Over!', this.canvas.width / 2 - 100, this.canvas.height / 2);
        }
    }

    gameLoop(timestamp) {
        const deltaTime = timestamp - this.lastTime;
        this.lastTime = timestamp;

        this.update(deltaTime);
        this.draw();
        requestAnimationFrame(this.gameLoop);
    }
}

// Start the game when the window loads
window.addEventListener('load', () => {
    const canvas = document.getElementById('gameCanvas');
    new Game(canvas);
}); 