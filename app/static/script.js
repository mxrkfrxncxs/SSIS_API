document.addEventListener('DOMContentLoaded', function() {
  // Add event listener to the delete button inside the modal
  document.querySelectorAll('.confirm-delete-student').forEach(function(button) {
      button.addEventListener('click', function() {
          var studentId = this.getAttribute('student-id');
          var csrfToken = this.getAttribute('csrf-token');
          handleDeleteStudent(studentId, csrfToken);
      });
  });
});

function handleDeleteStudent(studentId, csrfToken) {
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


// Function to handle delete course action
function handleDeleteCourse(courseId, csrfToken) {
  fetch(`/delete_course/${courseId}`, {
      method: 'DELETE',
      headers: {
          'X-CSRFToken': csrfToken
      }
  })
  .then(response => {
      if (response.ok) {
          window.location.reload(); // Reload the page after successful deletion
      } else {
          alert('Failed to delete course.'); // Display an alert if deletion fails
      }
  })
  .catch(error => {
      console.error('Error:', error);
      alert('An error occurred. Please try again later.'); // Display an alert if an error occurs
  });
}

// Add event listener to delete course buttons
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.confirm-delete-course').forEach(function(button) {
      button.addEventListener('click', function() {
          var courseId = this.getAttribute('course-id');
          var csrfToken = this.getAttribute('csrf-token');
          handleDeleteCourse(courseId, csrfToken);
      });
  });
});
