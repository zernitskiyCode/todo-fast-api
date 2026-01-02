// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    loadTasks();
    document.getElementById('registerForm').addEventListener('submit', handleRegister);
    document.getElementById('taskForm').addEventListener('submit', handleCreateTask);
});

let userId = null;

// Функция регистрации пользователя
async function handleRegister(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await axios.post('http://127.0.0.1:8000/register', {
            username,
            email,
            password
        });

        const data = response.data;
        if (data.user_id) {
            userId = data.user_id;
            alert('Registration successful!');
            document.getElementById('registerForm').reset();
        } else {
            alert('Error: ' + data.message);
        }
    } catch (error) {
        console.error('Error during registration:', error);
        alert('Error during registration!');
    }
}

// Функция создания задачи
async function handleCreateTask(event) {
    event.preventDefault();

    if (!userId) {
        alert('You must register first!');
        return;
    }

    const title = document.getElementById('taskTitle').value;
    const description = document.getElementById('taskDescription').value;
    const deadline = document.getElementById('taskDeadline').value;

    try {
        const response = await axios.post('http://127.0.0.1:8000/task', {
            title,
            description,
            deadline,
            user_id: userId
        });

        const data = response.data;
        if (data.task_id) {
            loadTasks(); // Перезагружаем задачи
            alert('Task created!');
        } else {
            alert('Error: ' + data.message);
        }
    } catch (error) {
        console.error('Error during task creation:', error);
        alert('Error during task creation!');
    }
}

// Функция загрузки задач
async function loadTasks() {
    if (!userId) return;

    try {
        const response = await axios.get(`http://127.0.0.1:8000/tasks/${userId}`);
        const data = response.data;

        const taskList = document.getElementById('taskList');
        taskList.innerHTML = '';

        data.tasks.forEach(task => {
            const li = document.createElement('li');
            li.innerHTML = `
                <span>${task.title}</span>
                <button onclick="deleteTask(${task.id})">Delete</button>
            `;
            taskList.appendChild(li);
        });
    } catch (error) {
        console.error('Error loading tasks:', error);
        alert('Error loading tasks!');
    }
}

// Функция удаления задачи
async function deleteTask(taskId) {
    if (!userId) {
        alert('You must register first!');
        return;
    }

    try {
        const response = await axios.delete(`http://127.0.0.1:8000/task/${taskId}`);

        const data = response.data;
        if (data.message === 'Task deleted') {
            loadTasks();
            alert('Task deleted!');
        } else {
            alert('Error: ' + data.message);
        }
    } catch (error) {
        console.error('Error deleting task:', error);
        alert('Error deleting task!');
    }
}
