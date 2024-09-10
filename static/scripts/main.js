document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const signupForm = document.getElementById('signup-form');
  const resetPasswordForm = document.getElementById('reset-password-form');

  // Login form validation
  if (loginForm) {
      loginForm.addEventListener('submit', function(event) {
          event.preventDefault();
          const email = document.getElementById('email').value;
          const password = document.getElementById('password').value;
          
          // Simulate login validation
          if (email !== "user@example.com" || password !== "password123") {
              document.getElementById('login-error').textContent = "Incorrect email or password.";
              document.getElementById('login-error').style.display = "block";
          } else {
              document.getElementById('login-error').style.display = "none";
              // Proceed with login (e.g., redirect to user dashboard)
          }
      });
  }

  // Signup form validation
  if (signupForm) {
      signupForm.addEventListener('submit', function(event) {
          event.preventDefault();
          const password = document.getElementById('password').value;
          const confirmPassword = document.getElementById('confirm-password').value;
          
          if (password !== confirmPassword) {
              document.getElementById('signup-error').textContent = "Passwords do not match.";
              document.getElementById('signup-error').style.display = "block";
          } else {
              document.getElementById('signup-error').style.display = "none";
              // Proceed with signup (e.g., send data to backend for account creation)
          }
      });
  }

  // Reset password form validation
  if (resetPasswordForm) {
      resetPasswordForm.addEventListener('submit', function(event) {
          event.preventDefault();
          const newPassword = document.getElementById('new-password').value;
          const confirmNewPassword = document.getElementById('confirm-new-password').value;
          
          if (newPassword !== confirmNewPassword) {
              document.getElementById('reset-password-error').textContent = "Passwords do not match.";
              document.getElementById('reset-password-error').style.display = "block";
          } else if (newPassword.length < 7 || newPassword.length > 14) {
              document.getElementById('reset-password-error').textContent = "Password must be between 7 and 14 characters.";
              document.getElementById('reset-password-error').style.display = "block";
          } else {
              document.getElementById('reset-password-error').style.display = "none";
              // Proceed with password reset (e.g., send data to backend to update password)
          }
      });
  }
});
document.addEventListener('DOMContentLoaded', () => {
  const inviteForm = document.getElementById('invite-form');
  const uploadBookForm = document.getElementById('upload-book-form');
  
  // Handle Invitation Form Submission
  if (inviteForm) {
      inviteForm.addEventListener('submit', function(event) {
          event.preventDefault();
          const email = document.getElementById('invite-email').value;
          
          // Simulate sending an invitation (e.g., make an API call)
          // If successful:
          document.getElementById('invite-message').textContent = `Invitation sent to ${email}`;
          document.getElementById('invite-message').style.color = "green";
          // If there's an error:
          // document.getElementById('invite-message').textContent = "Failed to send invitation.";
          // document.getElementById('invite-message').style.color = "red";
      });
  }

  // Handle Upload Book Form Submission
  if (uploadBookForm) {
      uploadBookForm.addEventListener('submit', function(event) {
          event.preventDefault();
          
          const bookName = document.getElementById('book-name').value;
          const authorName = document.getElementById('author-name').value;
          const bookFile = document.getElementById('book-file').files[0];
          
          // Simulate file upload process
          if (bookFile) {
              // Handle file upload (e.g., make an API call to upload the book)
              document.getElementById('upload-message').textContent = `${bookName} by ${authorName} has been successfully uploaded.`;
              document.getElementById('upload-message').style.color = "green";
              // Redirect to My Shelf page after successful upload
              setTimeout(() => {
                  window.location.href = 'myshelf.html';
              }, 2000);
          } else {
              document.getElementById('upload-message').textContent = "Failed to upload the book.";
              document.getElementById('upload-message').style.color = "red";
          }
      });
  }
});
