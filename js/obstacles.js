class Obstacle {
    constructor(gameWidth, gameHeight) {
        this.gameWidth = gameWidth;
        this.gameHeight = gameHeight;
        this.width = 50;
        this.height = 50;
        this.x = this.gameWidth; // Start from the right side
        this.y = this.gameHeight - this.height - 10; // Place on ground
        this.speed = 3; // Move left at constant speed
    }

    update() {
        this.x -= this.speed;
    }

    draw(ctx) {
        ctx.fillStyle = '#2d5a27'; // Dark green color for obstacles
        ctx.fillRect(this.x, this.y, this.width, this.height);
    }

    isOffScreen() {
        return this.x + this.width < 0;
    }

    collidesWith(player) {
        return !(player.x > this.x + this.width || 
                player.x + player.width < this.x || 
                player.y > this.y + this.height ||
                player.y + player.height < this.y);
    }
} 