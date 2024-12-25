document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const resultsSection = document.getElementById('results');
    const resultsContainer = document.querySelector('.results-container');

    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    // Highlight drop zone when dragging over it
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    // Handle dropped files
    dropZone.addEventListener('drop', handleDrop, false);
    fileInput.addEventListener('change', handleFiles, false);

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function highlight(e) {
        dropZone.classList.add('highlight');
    }

    function unhighlight(e) {
        dropZone.classList.remove('highlight');
    }

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles({ target: { files } });
    }

    function handleFiles(e) {
        const files = [...e.target.files];
        uploadFiles(files);
    }

    async function uploadFiles(files) {
        const file = files[0]; // Handle only the first file for now
        if (!file.type.startsWith('image/')) {
            alert('Please upload an image file');
            return;
        }

        // Show loading state
        resultsSection.style.display = 'block';
        resultsContainer.innerHTML = '<p>Processing your receipt...</p>';

        const formData = new FormData();
        formData.append('receipt', file);

        try {
            const response = await fetch('http://localhost:5000/api/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Upload failed');
            }

            const data = await response.json();
            displayResults(data);
        } catch (error) {
            console.error('Error:', error);
            resultsContainer.innerHTML = '<p>Error processing receipt. Please try again.</p>';
        }
    }

    function displayResults(data) {
        // Create a table to display the results
        const table = document.createElement('table');
        table.innerHTML = `
            <thead>
                <tr>
                    <th>Item</th>
                    <th>Price</th>
                    <th>Store</th>
                    <th>Date</th>
                </tr>
            </thead>
            <tbody>
                ${data.items.map(item => `
                    <tr>
                        <td>${item.name}</td>
                        <td>$${item.price.toFixed(2)}</td>
                        <td>${data.store}</td>
                        <td>${new Date(data.date).toLocaleDateString()}</td>
                    </tr>
                `).join('')}
            </tbody>
        `;

        resultsContainer.innerHTML = '';
        resultsContainer.appendChild(table);
    }
}); 