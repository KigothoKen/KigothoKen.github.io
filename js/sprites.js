class SpriteManager {
    constructor() {
        this.sprites = {};
    }

    loadSprite(name, src) {
        const sprite = new Image();
        sprite.src = src;
        this.sprites[name] = sprite;
        return new Promise((resolve, reject) => {
            sprite.onload = () => resolve(sprite);
            sprite.onerror = () => reject(new Error(`Failed to load sprite: ${src}`));
        });
    }

    getSprite(name) {
        return this.sprites[name];
    }
} 