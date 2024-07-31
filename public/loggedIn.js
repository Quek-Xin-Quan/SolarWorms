const logoutbtn = document.querySelector('.btnLogin-popup');

logoutbtn.addEventListener('click', () => {
    window.location.href = "index.html";
});

function toggleComments() {
    var commentsSection = document.getElementById('comments-section');
    if (commentsSection.style.display === 'none' || commentsSection.style.display === '') {
      commentsSection.style.display = 'block';
    } else {
      commentsSection.style.display = 'none';
    }
  }