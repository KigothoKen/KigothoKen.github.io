class Player {
    constructor(gameWidth, gameHeight) {
        this.gameWidth = gameWidth;
        this.gameHeight = gameHeight;
        this.width = 32;
        this.height = 48;
        this.x = 50;
        this.y = this.gameHeight - this.height - 10;
        this.speed = 0;
        this.vy = 0;
        this.weight = 1;
        this.isJumping = false;
    }

    update(input) {
        // Horizontal movement
        if (input.keys.right) this.speed = 5;
        else if (input.keys.left) this.speed = -5;
        else this.speed = 0;

        this.x += this.speed;

        // Horizontal boundaries
        if (this.x < 0) this.x = 0;
        if (this.x > this.gameWidth - this.width) this.x = this.gameWidth - this.width;

        // Vertical movement
        if (input.keys.up && !this.isJumping) {
            this.vy = -20;
            this.isJumping = true;
        }

        this.y += this.vy;
        
        // Apply gravity
        if (this.y < this.gameHeight - this.height) {
            this.vy += this.weight;
        } else {
            this.vy = 0;
            this.y = this.gameHeight - this.height;
            this.isJumping = false;
        }
    }

    draw(ctx) {
        ctx.fillStyle = 'red';
        ctx.fillRect(this.x, this.y, this.width, this.height);
    }
} 