
//
// Delete event handler
//
function deleteTodo(e) {
  // e.preventDefault();
  // console.log('event', e);
  const todo_id = e.target.dataset['id'];
  // console.log('clicked: ', todo_id);
  fetch('/todos/' + todo_id + '/delete', {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(function() {
    e.target.parentNode.remove();
  })
  .then(function() {
    document.getElementById('error').className = 'hidden';
  })
  .catch(function() {
    document.getElementById('error').className = '';
  });
}

//
//  Update checkbox event handler
//
function updateComplete(e) {
  // console.log('event', e);
  const newCompleted = e.target.checked;
  const todoid = e.target.dataset['id'];
  fetch('/todos/' + todoid + '/set-completed', {
    method: 'POST',
    body: JSON.stringify({
      'completed': newCompleted
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(function() {
    document.getElementById('error').className = 'hidden';
  })
  .catch(function() {
    document.getElementById('error').className = '';
  })
};

//
// Add delete handler to all todo items
//
const deleteBtns = document.querySelectorAll('.deleteBtn');
for (let deleteBtn of deleteBtns) {
  deleteBtn.onclick = deleteTodo
  };

//
//  Add select complete checkbox handler to all todo items
//
const checkboxes = document.querySelectorAll('.check-completed');
for (let i = 0; i < checkboxes.length; i++) {
  const checkbox = checkboxes[i];
  checkbox.onchange = updateComplete;
  }

//
// Create new todo Item
//
document.getElementById('form').onsubmit = function(e) {
  e.preventDefault();
  const list_id = e.target.dataset['id'];
  console.log(e)
  fetch('/todos/create', {
    method: 'POST',
    body: JSON.stringify({
      'description': document.getElementById('description').value,
      'list_id': list_id
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(function(response) {
    return response.json();
  })
  .then(function(jsonResponse) {
    const newId = jsonResponse['id'];
    const newDescription = jsonResponse['description'];

    newRow = `<input class="check-completed" data-id="${newId}" type="checkbox">${newDescription}<button class="deleteBtn" data-id="${newId}">&cross;</button>`;

    const liItem = document.createElement('LI');
    liItem.innerHTML = newRow;

    // Add event handlers for complete checkbox and delete buttons
    liItem.firstChild.onchange = updateComplete;
    liItem.lastChild.onclick = deleteTodo

    document.getElementById('todos').appendChild(liItem);

  })
  .catch(function() {
    document.getElementById('error').className = '';
  });
}
