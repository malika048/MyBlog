// Функция удаления заметки
function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }), // Запись id заметки, которую необходимо удалить
  }).then((_res) => {
    window.location.href = "/home";
  });
}



// Функция редактирования заметки
function editNote(noteId) {
  fetch("/edit", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId, new_note: document.getElementById("new_note").value }), // Запись текста новой заметки
  }).then((_res) => {
    window.location.href = "/home";
  });
}