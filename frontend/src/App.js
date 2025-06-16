import React, { useEffect, useState } from 'react';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/tasks/';
const LOGIN_URL = 'http://127.0.0.1:8000/auth/jwt/create/';

function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  // Загружаем задачи
  const fetchTasks = () => {
    axios.get(API_URL, {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => setTasks(res.data))
      .catch(err => console.error('Ошибка загрузки задач:', err));
  };

  // Логин
  const login = () => {
    axios.post(LOGIN_URL, { username, password })
      .then(res => {
        const newToken = res.data.access;
        setToken(newToken);
        localStorage.setItem('token', newToken);
        fetchTasks();
      })
      .catch(err => alert('Ошибка входа: ' + err.response?.data?.detail || err.message));
  };

  // Выход
  const logout = () => {
    setToken('');
    localStorage.removeItem('token');
    setTasks([]);
  };

  // Добавление задачи
  const addTask = () => {
    if (!title.trim()) return;
    axios.post(API_URL, {
      title,
      description: '',
      completed: false,
    }, {
      headers: { Authorization: `Bearer ${token}` }
    }).then(() => {
      setTitle('');
      fetchTasks();
    }).catch(err => console.error('Ошибка добавления:', err));
  };

  // Удаление задачи
  const deleteTask = (id) => {
    axios.delete(`${API_URL}${id}/`, {
      headers: { Authorization: `Bearer ${token}` }
    }).then(fetchTasks);
  };

  // Обновление (переключение выполнено)
  const toggleComplete = (task) => {
    axios.put(`${API_URL}${task.id}/`, {
      ...task,
      completed: !task.completed,
    }, {
      headers: { Authorization: `Bearer ${token}` }
    }).then(fetchTasks);
  };

  useEffect(() => {
    if (token) fetchTasks();
  }, [token]);

  // --- UI ---
  if (!token) {
    return (
      <div style={{ padding: 20 }}>
        <h2>Вход</h2>
        <input placeholder="Имя пользователя" value={username} onChange={e => setUsername(e.target.value)} /><br />
        <input type="password" placeholder="Пароль" value={password} onChange={e => setPassword(e.target.value)} /><br />
        <button onClick={login}>Войти</button>
      </div>
    );
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>Задачи</h1>
      <button onClick={logout}>Выйти</button>

      <div style={{ marginTop: 20 }}>
        <input
          placeholder="Новая задача"
          value={title}
          onChange={e => setTitle(e.target.value)}
        />
        <button onClick={addTask}>Добавить</button>
      </div>

      <ul style={{ marginTop: 20 }}>
        {tasks.map(task => (
          <li key={task.id}>
            <span
              onClick={() => toggleComplete(task)}
              style={{
                textDecoration: task.completed ? 'line-through' : 'none',
                cursor: 'pointer'
              }}
            >
              {task.title}
            </span>
            <button onClick={() => deleteTask(task.id)} style={{ marginLeft: 10 }}>
              ❌
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
