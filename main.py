<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Dominant Color Extractor</title>
    <!-- Load Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
      /* Custom scrollbar styling for aesthetics */
      body {
        font-family: "Inter", sans-serif;
        background-color: #f7f9fb;
      }
      .color-swatch {
        transition: transform 0.2s, box-shadow 0.2s;
      }
      .color-swatch:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1),
          0 4px 6px -2px rgba(0, 0, 0, 0.05);
      }
    </style>
  </head>
  <body class="min-h-screen flex items-center justify-center p-4">
    <!-- Main Application Card -->
    <div class="w-full max-w-xl bg-white shadow-2xl rounded-xl p-8 space-y-8">
      <header class="text-center">
        <h1 class="text-3xl font-extrabold text-gray-900">
          Image Color Palette Generator
        </h1>
        <p class="mt-2 text-gray-500">
          Upload an image to extract its 5 most dominant colors.
        </p>
      </header>

      <!-- Image Upload Form -->
      <form id="uploadForm" class="space-y-4">
        <!-- File Input -->
        <label for="imageUpload" class="block text-sm font-medium text-gray-700"
          >Select Image File</label
        >
        <input
          type="file"
          id="imageUpload"
          name="image"
          accept="image/*"
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 transition duration-150"
        />

        <!-- Submit Button -->
        <button
          type="submit"
          id="submitButton"
          class="w-full flex justify-center py-2 px-4 border border-transparent rounded-lg shadow-md text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-150 ease-in-out disabled:opacity-50"
        >
          Extract Colors
        </button>
      </form>

      <!-- Status and Results Area -->
      <div id="resultsArea" class="pt-6 border-t border-gray-100">
        <!-- Loading Indicator -->
        <div
          id="loadingMessage"
          class="hidden text-center text-indigo-600 font-semibold"
        >
          <svg
            class="animate-spin -ml-1 mr-3 h-5 w-5 inline-block text-indigo-500"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              class="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
            ></circle>
            <path
              class="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
          Analyzing image and clustering colors...
        </div>

        <!-- Error Message -->
        <div
          id="errorMessage"
          class="hidden p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg"
          role="alert"
        >
          <p class="font-bold">Error:</p>
          <p id="errorText"></p>
        </div>

        <!-- Color Palette Display -->
        <div id="paletteDisplay" class="hidden space-y-4">
          <h2 class="text-xl font-bold text-gray-800">Dominant Palette</h2>
          <div id="colorSwatches" class="grid grid-cols-5 gap-4">
            <!-- Swatches will be inserted here by JavaScript -->
          </div>
        </div>
      </div>
    </div>

    <script>
      // Set up the API endpoint. Since Flask is running locally, this should be correct.
      const API_ENDPOINT = "http://127.0.0.1:5000/upload";

      // Get references to DOM elements
      const form = document.getElementById("uploadForm");
      const fileInput = document.getElementById("imageUpload");
      const submitButton = document.getElementById("submitButton");
      const loadingMessage = document.getElementById("loadingMessage");
      const errorMessage = document.getElementById("errorMessage");
      const errorText = document.getElementById("errorText");
      const paletteDisplay = document.getElementById("paletteDisplay");
      const colorSwatchesContainer = document.getElementById("colorSwatches");

      // Function to show a message in the custom alert box
      const showMessage = (type, message) => {
        errorMessage.classList.add("hidden");
        loadingMessage.classList.add("hidden");
        paletteDisplay.classList.add("hidden");

        if (type === "loading") {
          loadingMessage.classList.remove("hidden");
        } else if (type === "error") {
          errorText.textContent = message;
          errorMessage.classList.remove("hidden");
        } else if (type === "results") {
          paletteDisplay.classList.remove("hidden");
        }
      };

      // Function to render the color swatches
      const renderColors = (hexColors) => {
        colorSwatchesContainer.innerHTML = ""; // Clear previous results

        hexColors.forEach((hex) => {
          const swatchDiv = document.createElement("div");
          swatchDiv.className =
            "color-swatch p-2 rounded-xl text-center cursor-pointer transform hover:scale-[1.02] transition duration-200";
          swatchDiv.style.backgroundColor = hex;
          swatchDiv.innerHTML = `
                    <div class="mt-16 h-12 flex items-center justify-center bg-white bg-opacity-90 backdrop-blur-sm rounded-lg shadow-md text-gray-800 font-mono text-xs font-semibold p-1 border border-gray-200">
                        ${hex}
                    </div>
                `;

          // Add click listener to copy hex code
          swatchDiv.addEventListener("click", () => {
            copyToClipboard(hex);
            // Simple visual feedback (can be improved with a custom toast)
            const originalText = swatchDiv.querySelector("div").textContent;
            swatchDiv.querySelector("div").textContent = "Copied!";
            setTimeout(() => {
              swatchDiv.querySelector("div").textContent = originalText;
            }, 1000);
          });

          colorSwatchesContainer.appendChild(swatchDiv);
        });
      };

      // Function to copy text to clipboard
      const copyToClipboard = (text) => {
        // Fallback for secure contexts in iFrames
        const textarea = document.createElement("textarea");
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        try {
          document.execCommand("copy");
        } catch (err) {
          console.error("Could not copy text: ", err);
        }
        document.body.removeChild(textarea);
      };

      // Handle form submission
      form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // Guard clause for file selection
        if (fileInput.files.length === 0) {
          showMessage("error", "Please select an image file before uploading.");
          return;
        }

        // Prepare form data
        const formData = new FormData();
        formData.append("image", fileInput.files[0]);

        // UI feedback
        submitButton.disabled = true;
        submitButton.textContent = "Processing...";
        showMessage("loading");

        // Retry mechanism for API calls
        const MAX_RETRIES = 5;
        let attempt = 0;
        let success = false;

        while (attempt < MAX_RETRIES && !success) {
          try {
            const response = await fetch(API_ENDPOINT, {
              method: "POST",
              body: formData,
            });

            // Check for HTTP errors (e.g., 400, 500)
            if (!response.ok) {
              const errorData = await response
                .json()
                .catch(() => ({ error: "Unknown server error." }));
              throw new Error(
                `Server returned status ${response.status}: ${errorData.error}`
              );
            }

            const data = await response.json();

            if (data.dominant_colors && data.dominant_colors.length > 0) {
              renderColors(data.dominant_colors);
              showMessage("results");
              success = true; // Mark as success
            } else {
              // Handle cases where the response is technically 200 but lacks the expected data
              throw new Error(
                "Received an empty or invalid color list from the server."
              );
            }
          } catch (error) {
            console.error("Fetch attempt failed:", error);
            attempt++;

            if (attempt < MAX_RETRIES) {
              // Implement exponential backoff: 1s, 2s, 4s, 8s...
              const delay = Math.pow(2, attempt) * 1000;
              await new Promise((resolve) => setTimeout(resolve, delay));
              // Do not log retry as an error in the console.
            } else {
              // All retries failed
              showMessage(
                "error",
                error.message ||
                  "Failed to connect to the Flask server after multiple attempts. Is your Python script running?"
              );
            }
          }
        }

        // Final UI reset
        submitButton.disabled = false;
        submitButton.textContent = "Extract Colors";
      });
    </script>
  </body>
</html>
