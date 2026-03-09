    (function() {
      // state
      let tasks = [];
      let currentFilter = 'all';

      // dom elements
      const taskInput = document.getElementById('taskInput');
      const prioritySelect = document.getElementById('prioritySelect');
      const addBtn = document.getElementById('addBtn');
      const taskList = document.getElementById('taskList');
      const emptyState = document.getElementById('emptyState');
      const taskCountSpan = document.getElementById('taskCount');
      const progressRing = document.getElementById('progressRing');
      const progressPercent = document.getElementById('progressPercent');
      const clearCompletedBtn = document.getElementById('clearCompletedBtn');
      const filterBtns = document.querySelectorAll('.filter-btn');
      const currentTimeSpan = document.getElementById('currentTime');
      const currentDateSpan = document.getElementById('currentDate');

      // load from storage
      function loadTasks() {
        const saved = localStorage.getItem('light-todos');
        if (saved) {
          try {
            tasks = JSON.parse(saved);
          } catch (e) {
            tasks = [];
          }
        } else {
          // demo tasks
          tasks = [
            { id: Date.now() - 1000000, text: 'welcome to do', completed: false, priority: 'medium' },
            { id: Date.now() - 2000000, text: 'click to complete', completed: true, priority: 'low' },
            { id: Date.now() - 3000000, text: 'high priority task', completed: false, priority: 'high' }
          ];
        }
        renderTasks();
      }

      // save to storage
      function saveTasks() {
        localStorage.setItem('light-todos', JSON.stringify(tasks));
      }

      // render tasks
      function renderTasks() {
        let filtered = tasks;
        
        if (currentFilter === 'active') {
          filtered = tasks.filter(t => !t.completed);
        } else if (currentFilter === 'completed') {
          filtered = tasks.filter(t => t.completed);
        }

        // sort
        filtered.sort((a, b) => {
          if (a.completed !== b.completed) {
            return a.completed ? 1 : -1;
          }
          const order = { high: 1, medium: 2, low: 3 };
          return order[a.priority] - order[b.priority];
        });

        if (filtered.length === 0) {
          taskList.innerHTML = '';
          emptyState.style.display = 'block';
        } else {
          emptyState.style.display = 'none';
          
          let html = '';
          filtered.forEach(task => {
            html += `
              <li class="task-item ${task.completed ? 'completed' : ''}" data-id="${task.id}">
                <div class="task-checkbox ${task.completed ? 'checked' : ''}" onclick="toggleTask(${task.id})">
                  <i class="fas fa-check"></i>
                </div>
                <div class="task-content">
                  <div class="task-title">${escapeHtml(task.text)}</div>
                  <div class="task-meta">
                    <span class="task-priority priority-${task.priority}">
                      <i class="fas fa-flag"></i>
                      ${task.priority}
                    </span>
                  </div>
                </div>
                <div class="task-actions">
                  <button class="task-btn delete" onclick="deleteTask(${task.id})" title="delete">
                    <i class="fas fa-times"></i>
                  </button>
                </div>
              </li>
            `;
          });
          taskList.innerHTML = html;
        }

        updateStats();
        saveTasks();
      }

      function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
      }

      function updateStats() {
        const total = tasks.length;
        const completed = tasks.filter(t => t.completed).length;
        const active = total - completed;
        
        taskCountSpan.textContent = `${active} left, ${completed} done`;
        
        const percent = total === 0 ? 0 : Math.round((completed / total) * 100);
        progressPercent.textContent = percent + '%';
        
        clearCompletedBtn.disabled = completed === 0;
      }

      // add task
      function addTask() {
        const text = taskInput.value.trim();
        if (!text) {
          alert('task cannot be empty');
          return;
        }

        tasks.push({
          id: Date.now(),
          text: text,
          completed: false,
          priority: prioritySelect.value
        });

        taskInput.value = '';
        taskInput.focus();
        renderTasks();

        // feedback
        addBtn.innerHTML = '<i class="fas fa-check"></i> done';
        setTimeout(() => {
          addBtn.innerHTML = '<i class="fas fa-plus"></i> add';
        }, 500);
      }

      // global functions
      window.toggleTask = function(id) {
        const task = tasks.find(t => t.id === id);
        if (task) {
          task.completed = !task.completed;
          renderTasks();
        }
      };

      window.deleteTask = function(id) {
        const el = document.querySelector(`.task-item[data-id="${id}"]`);
        if (el) {
          el.classList.add('deleting');
          setTimeout(() => {
            tasks = tasks.filter(t => t.id !== id);
            renderTasks();
          }, 200);
        } else {
          tasks = tasks.filter(t => t.id !== id);
          renderTasks();
        }
      };

      function clearCompleted() {
        tasks = tasks.filter(t => !t.completed);
        renderTasks();
      }

      function setFilter(filter) {
        currentFilter = filter;
        filterBtns.forEach(btn => {
          btn.classList.toggle('active', btn.dataset.filter === filter);
        });
        renderTasks();
      }

      function updateDateTime() {
        const now = new Date();
        currentTimeSpan.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        currentDateSpan.textContent = now.toLocaleDateString([], { month: 'short', day: 'numeric' });
      }

      // event listeners
      addBtn.addEventListener('click', addTask);
      
      taskInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') addTask();
      });

      clearCompletedBtn.addEventListener('click', clearCompleted);

      filterBtns.forEach(btn => {
        btn.addEventListener('click', () => setFilter(btn.dataset.filter));
      });

      // init
      loadTasks();
      updateDateTime();
      setInterval(updateDateTime, 60000);
    })();
