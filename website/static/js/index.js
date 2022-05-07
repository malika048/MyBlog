function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/home";
  });
}


function editNote(noteId) {
  fetch("/edit", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId, new_note: document.getElementById("new_note").value }),
  }).then((_res) => {
    window.location.href = "/home";
  });
}