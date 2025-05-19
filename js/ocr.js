document.addEventListener('DOMContentLoaded', () => {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const previewArea = document.getElementById('previewArea');
    const imagePreview = document.getElementById('imagePreview');
    const loading = document.getElementById('loading');
    const resultArea = document.getElementById('resultArea');
    const resultText = document.getElementById('resultText');
    const copyBtn = document.getElementById('copyBtn');

    // Handle drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.background = '#f0f7ff';
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.background = 'transparent';
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.background = 'transparent';
        handleFile(e.dataTransfer.files[0]);
    });

    // Handle click to upload
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        handleFile(e.target.files[0]);
    });

    // Copy button functionality
    copyBtn.addEventListener('click', () => {
        resultText.select();
        document.execCommand('copy');
        copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
        setTimeout(() => {
            copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy Text';
        }, 2000);
    });

    function handleFile(file) {
        if (!file) return;
        if (!file.type.startsWith('image/')) {
            alert('Please upload an image file');
            return;
        }

        // Show preview
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            previewArea.style.display = 'block';
        };
        reader.readAsDataURL(file);

        // Process image
        processImage(file);
    }

    async function processImage(file) {
        try {
            // Show loading state
            loading.style.display = 'block';
            resultArea.style.display = 'none';

            // Perform OCR
            const result = await Tesseract.recognize(
                file,
                'eng',
                { logger: m => console.log(m) }
            );

            // Display result
            resultText.value = result.data.text;
            resultArea.style.display = 'block';
        } catch (error) {
            console.error('Error:', error);
            alert('Error processing image. Please try again.');
        } finally {
            loading.style.display = 'none';
        }
    }
}); 