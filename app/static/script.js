function handleDelete(studentId, csrfToken) {
  fetch(`/delete_student/${studentId}`, {
      method: 'DELETE',
      headers: {
          'X-CSRFToken': csrfToken
      }
  })
  .then(response => {
      if (response.ok) {
          window.location.reload();
      } else {
          alert('Failed to delete student.');
      }
  })
  .catch(error => {
      console.error('Error:', error);
      alert('An error occurred. Please try again later.');
  });
}

// Add event listener to the delete button
document.getElementById('confirmDeleteBtn').addEventListener('click', function() {
  var studentId = document.querySelector('.btn-danger').getAttribute('student-id');
  var csrfToken = document.querySelector('.btn-danger').getAttribute('csrf-token');
  handleDelete(studentId, csrfToken);
});


function confirmDeleteCourse(button) {
  var course_code= button.getAttribute('course-code');
  var csrfToken = button.getAttribute('csrf-token');
  if (confirm("Are you sure you want to delete " + course_code + "?\nStudents under this Course will also be deleted.\n")) {
      fetch(`/delete_course/${course_code}`, {
          method: 'DELETE',
          headers: {
              'X-CSRFToken': csrfToken
          }
      }).then(response => response.json())
      .then(data => {
        if(data.success == true) {
          window.location.reload( );
        } else {
          console.error("Error: " + data.error)
        }
      });
  }
}