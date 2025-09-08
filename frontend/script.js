document.addEventListener('DOMContentLoaded', () => {
    const taskInput = document.getElementById('task-input');
    const submitBtn = document.getElementById('submit-btn');
    const subtasksList = document.getElementById('subtasks-list');
    const deleteBtn = document.getElementById('delete-btn');

    submitBtn.addEventListener('click', async () => {
        const task = taskInput.value.trim();
        if (!task) {
            alert('Please enter a task.');
            return;
        }

        // Disable form and show loading state
        submitBtn.disabled = true;
        submitBtn.textContent = 'Decomposing...';
        subtasksList.innerHTML = '<li>Loading...</li>';

        try {
            const response = await fetch('/api/decompose', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: task }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // Display subtasks
            subtasksList.innerHTML = '';
            if (data.subtasks && data.subtasks.length > 0) {
                data.subtasks.forEach(subtask => {
                    const li = document.createElement('li');
                    li.textContent = subtask;
                    subtasksList.appendChild(li);
                });
                // Enable controls
                deleteBtn.disabled = false;
            } else {
                subtasksList.innerHTML = '<li>No subtasks were generated.</li>';
            }

        } catch (error) {
            console.error('Error:', error);
            subtasksList.innerHTML = `<li>Error: ${error.message}</li>`;
            alert('Failed to decompose task. Please check the console for details.');
        } finally {
            // Re-enable form
            submitBtn.disabled = false;
            submitBtn.textContent = 'Decompose Task';
        }
    });

    deleteBtn.addEventListener('click', () => {
        if (confirm('Are you sure you want to clear the task and results?')) {
            taskInput.value = '';
            subtasksList.innerHTML = '';
            deleteBtn.disabled = true;
        }
    });
});
