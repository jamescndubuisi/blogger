document.addEventListener('DOMContentLoaded', function () {
    // Find the body field and inject regenerate button
    const bodyField = document.querySelector('.gemini-body-field');
    if (!bodyField) return;

    const articleId = bodyField.dataset.articleId;
    if (!articleId) return;

    // Create button container
    const buttonContainer = document.createElement('div');
    buttonContainer.className = 'mb-4';
    buttonContainer.innerHTML = `
        <button type="button" id="gemini-regenerate-btn"
                class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1.5 text-sm rounded-md flex items-center">
            <span class="material-symbols-outlined mr-1">auto_awesome</span>
            Regenerate with Gemini
        </button>
        <div id="gemini-status" class="mt-2 text-sm text-gray-500 dark:text-gray-400 hidden"></div>
    `;

    // Insert before the body field
    bodyField.parentNode.insertBefore(buttonContainer, bodyField);

    // Handle button click
    document.getElementById('gemini-regenerate-btn').addEventListener('click', function () {
        if (!confirm('This will replace the current article content with AI-generated text. Are you sure?')) {
            return;
        }

        const titleField = document.querySelector('#id_title');
        const descField = document.querySelector('#id_description');

        const title = titleField?.value.trim() || '';
        const description = descField?.value.trim() || '';
        const wordTarget = 800; // or get from a hidden input if needed

        if (!title) {
            alert('Please enter a title first.');
            return;
        }

        const statusDiv = document.getElementById('gemini-status');
        statusDiv.textContent = 'Generating...';
        statusDiv.classList.remove('hidden');
        this.disabled = true;
        this.innerHTML = '<span class="material-symbols-outlined animate-spin">progress_activity</span> Generating...';

        fetch('/admin/blog/article/generate-gemini-ajax/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: new URLSearchParams({
                title: title,
                description: description,
                word_target: wordTarget
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update the body field
                bodyField.value = data.content;

                // If using WysiwygWidget (which uses textarea), this is enough
                // Trigger input event for Unfold's auto-save or validation
                bodyField.dispatchEvent(new Event('input', { bubbles: true }));

                statusDiv.textContent = '✅ Content regenerated!';
                setTimeout(() => statusDiv.classList.add('hidden'), 3000);
            } else {
                statusDiv.textContent = '❌ Error: ' + (data.error || 'Unknown error');
                statusDiv.classList.remove('hidden');
            }
        })
        .catch(error => {
            statusDiv.textContent = '❌ Network error: ' + error.message;
            statusDiv.classList.remove('hidden');
        })
        .finally(() => {
            this.disabled = false;
            this.innerHTML = '<span class="material-symbols-outlined mr-1">auto_awesome</span> Regenerate with Gemini';
        });
    });
});

// Helper to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//
// document.addEventListener('DOMContentLoaded', function () {
//     // Helper to get CSRF token
//     function getCookie(name) {
//         let cookieValue = null;
//         if (document.cookie && document.cookie !== '') {
//             const cookies = document.cookie.split(';');
//             for (let i = 0; i < cookies.length; i++) {
//                 const cookie = cookies[i].trim();
//                 if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                     break;
//                 }
//             }
//         }
//         return cookieValue;
//     }
//
//     function injectRegenerateButton() {
//         const bodyField = document.querySelector('.gemini-body-field');
//         if (!bodyField) return;
//
//         // Avoid injecting multiple times
//         if (bodyField.dataset.geminiButtonInjected) return;
//         bodyField.dataset.geminiButtonInjected = 'true';
//
//         const articleId = bodyField.dataset.articleId;
//         if (!articleId) return;
//
//         const buttonContainer = document.createElement('div');
//         buttonContainer.className = 'mb-4';
//         buttonContainer.innerHTML = `
//             <button type="button" id="gemini-regenerate-btn"
//                     class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1.5 text-sm rounded-md flex items-center">
//                 <span class="material-symbols-outlined mr-1">auto_awesome</span>
//                 <span id="gemini-btn-text">Regenerate with Gemini</span>
//             </button>
//             <div id="gemini-status" class="mt-2 text-sm text-gray-500 dark:text-gray-400 hidden"></div>
//         `;
//
//         bodyField.parentNode.insertBefore(buttonContainer, bodyField);
//
//         const button = document.getElementById('gemini-regenerate-btn');
//         const buttonText = document.getElementById('gemini-btn-text');
//         const statusDiv = document.getElementById('gemini-status');
//
//         button.addEventListener('click', function () {
//             if (!confirm('This will replace the current article content with AI-generated text. Are you sure?')) {
//                 return;
//             }
//
//             const titleField = document.querySelector('#id_title');
//             const descField = document.querySelector('#id_description');
//
//             const title = titleField?.value.trim() || '';
//             const description = descField?.value.trim() || '';
//             const wordTarget = 800;
//
//             if (!title) {
//                 alert('Please enter a title first.');
//                 return;
//             }
//
//             // Update UI for loading
//             statusDiv.textContent = 'Generating...';
//             statusDiv.classList.remove('hidden');
//             button.disabled = true;
//             buttonText.textContent = 'Generating...';
//             const icon = button.querySelector('.material-symbols-outlined');
//             icon.textContent = 'progress_activity';
//             icon.classList.add('animate-spin');
//
//             fetch('/admin/blog/article/generate-gemini-ajax/', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/x-www-form-urlencoded',
//                     'X-CSRFToken': getCookie('csrftoken')
//                 },
//                 body: new URLSearchParams({
//                     title: title,
//                     description: description,
//                     word_target: wordTarget
//                 })
//             })
//             .then(response => response.json())
//             .then(data => {
//                 if (data.success) {
//                     bodyField.value = data.content;
//                     bodyField.dispatchEvent(new Event('input', { bubbles: true }));
//                     statusDiv.textContent = '✅ Content regenerated!';
//                     setTimeout(() => statusDiv.classList.add('hidden'), 3000);
//                 } else {
//                     statusDiv.textContent = '❌ Error: ' + (data.error || 'Unknown error');
//                     statusDiv.classList.remove('hidden');
//                 }
//             })
//             .catch(error => {
//                 statusDiv.textContent = '❌ Network error: ' + error.message;
//                 statusDiv.classList.remove('hidden');
//             })
//             .finally(() => {
//                 // Restore button state safely
//                 button.disabled = false;
//                 buttonText.textContent = 'Regenerate with Gemini';
//                 const icon = button.querySelector('.material-symbols-outlined');
//                 icon.textContent = 'auto_awesome';
//                 icon.classList.remove('animate-spin');
//             });
//         });
//     }
//
//     // Initial injection
//     injectRegenerateButton();
//
//     // Optional: Re-inject if Unfold re-renders the field (e.g., after dynamic form changes)
//     // You can use MutationObserver if needed, but often not necessary.
//     // For now, this should suffice.
// });


