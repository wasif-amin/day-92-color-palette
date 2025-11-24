<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Color Palette Extractor</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 40px;
            max-width: 900px;
            width: 100%;
            margin-top: 20px;
        }

        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 2.5em;
        }

        .upload-area {
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            background: #f8f9ff;
            margin-bottom: 30px;
        }

        .upload-area:hover {
            border-color: #764ba2;
            background: #f0f2ff;
        }

        .upload-area.dragover {
            border-color: #764ba2;
            background: #e8ebff;
            transform: scale(1.02);
        }

        #fileInput {
            display: none;
        }

        .upload-icon {
            font-size: 48px;
            margin-bottom: 15px;
        }

        .upload-text {
            font-size: 18px;
            color: #666;
            margin-bottom: 10px;
        }

        .upload-hint {
            font-size: 14px;
            color: #999;
        }

        .image-preview {
            margin: 30px 0;
            text-align: center;
            display: none;
        }

        .image-preview img {
            max-width: 100%;
            max-height: 400px;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }

        .controls {
            display: flex;
            gap: 15px;
            justify-content: center;
            margin: 20px 0;
            flex-wrap: wrap;
        }

        .control-group {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        label {
            font-weight: 600;
            color: #555;
        }

        input[type="number"] {
            padding: 8px 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            width: 80px;
        }

        input[type="number"]:focus {
            outline: none;
            border-color: #667eea;
        }

        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }

        button:active {
            transform: translateY(0);
        }

        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .loading {
            text-align: center;
            padding: 20px;
            display: none;
        }

        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .palette-container {
            margin-top: 30px;
            display: none;
        }

        .palette-title {
            font-size: 1.5em;
            color: #333;
            margin-bottom: 20px;
            text-align: center;
        }

        .color-palette {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }

        .color-item {
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s;
            cursor: pointer;
        }

        .color-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
        }

        .color-box {
            height: 120px;
            width: 100%;
        }

        .color-info {
            padding: 15px;
            background: white;
        }

        .color-hex {
            font-weight: 600;
            font-size: 16px;
            color: #333;
            margin-bottom: 5px;
            font-family: 'Courier New', monospace;
        }

        .color-rgb {
            font-size: 12px;
            color: #666;
            margin-bottom: 5px;
        }

        .color-percentage {
            font-size: 12px;
            color: #999;
        }

        .error-message {
            background: #fee;
            color: #c33;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            display: none;
            text-align: center;
        }

        .copy-message {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #4caf50;
            color: white;
            padding: 15px 25px;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            display: none;
            z-index: 1000;
            animation: slideIn 0.3s ease;
        }

        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 Color Palette Extractor</h1>
        
        <div class="upload-area" id="uploadArea">
            <div class="upload-icon">📤</div>
            <div class="upload-text">Click to upload or drag and drop</div>
            <div class="upload-hint">Supports JPG, PNG, GIF, and WebP</div>
            <input type="file" id="fileInput" accept="image/*">
        </div>

        <div class="error-message" id="errorMessage"></div>

        <div class="image-preview" id="imagePreview">
            <img id="previewImage" alt="Preview">
        </div>

        <div class="controls">
            <div class="control-group">
                <label for="colorCount">Colors:</label>
                <input type="number" id="colorCount" min="1" max="20" value="10">
            </div>
            <div class="control-group">
                <label for="tolerance">Tolerance:</label>
                <input type="number" id="tolerance" min="0" max="50" value="10">
            </div>
            <button id="analyzeBtn" disabled>Analyze Colors</button>
        </div>

        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Analyzing image colors...</p>
        </div>

        <div class="palette-container" id="paletteContainer">
            <h2 class="palette-title">Most Common Colors</h2>
            <div class="color-palette" id="colorPalette"></div>
        </div>
    </div>

    <div class="copy-message" id="copyMessage">Color copied to clipboard!</div>

    <script>
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const imagePreview = document.getElementById('imagePreview');
        const previewImage = document.getElementById('previewImage');
        const analyzeBtn = document.getElementById('analyzeBtn');
        const colorCountInput = document.getElementById('colorCount');
        const toleranceInput = document.getElementById('tolerance');
        const loading = document.getElementById('loading');
        const paletteContainer = document.getElementById('paletteContainer');
        const colorPalette = document.getElementById('colorPalette');
        const errorMessage = document.getElementById('errorMessage');
        const copyMessage = document.getElementById('copyMessage');

        let currentImage = null;

        // Upload area click
        uploadArea.addEventListener('click', () => fileInput.click());

        // File input change
        fileInput.addEventListener('change', (e) => {
            handleFile(e.target.files[0]);
        });

        // Drag and drop
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            if (e.dataTransfer.files.length > 0) {
                handleFile(e.dataTransfer.files[0]);
            }
        });

        function handleFile(file) {
            if (!file || !file.type.startsWith('image/')) {
                showError('Please select a valid image file.');
                return;
            }

            hideError();
            const reader = new FileReader();
            
            reader.onload = (e) => {
                previewImage.src = e.target.result;
                imagePreview.style.display = 'block';
                analyzeBtn.disabled = false;
                paletteContainer.style.display = 'none';
                
                // Load image for analysis
                const img = new Image();
                img.onload = () => {
                    currentImage = img;
                };
                img.src = e.target.result;
            };

            reader.readAsDataURL(file);
        }

        function showError(message) {
            errorMessage.textContent = message;
            errorMessage.style.display = 'block';
        }

        function hideError() {
            errorMessage.style.display = 'none';
        }

        // Analyze button
        analyzeBtn.addEventListener('click', () => {
            if (!currentImage) return;
            
            const colorCount = parseInt(colorCountInput.value) || 10;
            const tolerance = parseInt(toleranceInput.value) || 10;
            
            loading.style.display = 'block';
            paletteContainer.style.display = 'none';
            analyzeBtn.disabled = true;

            // Use setTimeout to allow UI to update
            setTimeout(() => {
                const colors = extractColors(currentImage, colorCount, tolerance);
                displayPalette(colors);
                loading.style.display = 'none';
                analyzeBtn.disabled = false;
            }, 100);
        });

        function extractColors(image, maxColors, tolerance) {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            
            // Set canvas size (resize for performance)
            const maxSize = 200;
            let width = image.width;
            let height = image.height;
            
            if (width > maxSize || height > maxSize) {
                const ratio = Math.min(maxSize / width, maxSize / height);
                width = Math.floor(width * ratio);
                height = Math.floor(height * ratio);
            }
            
            canvas.width = width;
            canvas.height = height;
            
            ctx.drawImage(image, 0, 0, width, height);
            
            const imageData = ctx.getImageData(0, 0, width, height);
            const pixels = imageData.data;
            
            // Count color frequencies
            const colorMap = new Map();
            
            for (let i = 0; i < pixels.length; i += 4) {
                const r = pixels[i];
                const g = pixels[i + 1];
                const b = pixels[i + 2];
                const a = pixels[i + 3];
                
                // Skip transparent pixels
                if (a < 128) continue;
                
                // Quantize colors based on tolerance
                const qr = Math.round(r / tolerance) * tolerance;
                const qg = Math.round(g / tolerance) * tolerance;
                const qb = Math.round(b / tolerance) * tolerance;
                
                const key = `${qr},${qg},${qb}`;
                colorMap.set(key, (colorMap.get(key) || 0) + 1);
            }
            
            // Convert to array and sort by frequency
            const colors = Array.from(colorMap.entries())
                .map(([key, count]) => {
                    const [r, g, b] = key.split(',').map(Number);
                    return { r, g, b, count };
                })
                .sort((a, b) => b.count - a.count)
                .slice(0, maxColors);
            
            // Calculate percentages
            const totalPixels = colors.reduce((sum, color) => sum + color.count, 0);
            colors.forEach(color => {
                color.percentage = ((color.count / totalPixels) * 100).toFixed(2);
            });
            
            return colors;
        }

        function displayPalette(colors) {
            colorPalette.innerHTML = '';
            
            colors.forEach(color => {
                const hex = rgbToHex(color.r, color.g, color.b);
                
                const colorItem = document.createElement('div');
                colorItem.className = 'color-item';
                
                colorItem.innerHTML = `
                    <div class="color-box" style="background-color: rgb(${color.r}, ${color.g}, ${color.b})"></div>
                    <div class="color-info">
                        <div class="color-hex">${hex}</div>
                        <div class="color-rgb">RGB(${color.r}, ${color.g}, ${color.b})</div>
                        <div class="color-percentage">${color.percentage}%</div>
                    </div>
                `;
                
                colorItem.addEventListener('click', () => {
                    copyToClipboard(hex);
                });
                
                colorPalette.appendChild(colorItem);
            });
            
            paletteContainer.style.display = 'block';
        }

        function rgbToHex(r, g, b) {
            return '#' + [r, g, b].map(x => {
                const hex = x.toString(16);
                return hex.length === 1 ? '0' + hex : hex;
            }).join('');
        }

        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(() => {
                copyMessage.style.display = 'block';
                setTimeout(() => {
                    copyMessage.style.display = 'none';
                }, 2000);
            });
        }
    </script>
</body>
</html>

