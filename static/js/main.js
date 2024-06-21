document.addEventListener('DOMContentLoaded', function () {
    const socket = io();

    const scoreForm = document.getElementById('score-form');
    const playerInput = document.getElementById('player');
    const equationTextarea = document.getElementById('equation');
    const answerInput = document.getElementById('answer');
    const scoreList = document.getElementById('score-list');

    socket.on('update_scores', function (data) {
        scoreList.innerHTML = '';
        data.high_scores.forEach(function (score) {
            const li = document.createElement('li');
            li.textContent = `${score[0]}: ${score[1]}`;
            scoreList.appendChild(li);
        });
    });

    scoreForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(scoreForm);

        fetch('/save_score', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Clear inputs
            playerInput.value = '';
            answerInput.value = '';
        });
    });
});
