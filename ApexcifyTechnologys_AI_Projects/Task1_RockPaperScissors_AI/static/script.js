document.addEventListener('DOMContentLoaded', () => {
    const choiceBtns = document.querySelectorAll('.choice-btn');
    const playerHand = document.getElementById('player-hand');
    const compHand = document.getElementById('comp-hand');
    const resultText = document.getElementById('result-text');
    
    const userScoreEl = document.getElementById('user-score');
    const compScoreEl = document.getElementById('comp-score');
    const drawScoreEl = document.getElementById('draw-score');
    
    const resetBtn = document.getElementById('reset-btn');

    let isPlaying = false;

    choiceBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            if (isPlaying) return;
            
            const userChoice = this.getAttribute('data-choice');
            playRound(userChoice);
        });
    });

    resetBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/api/reset', { method: 'POST' });
            const data = await response.json();
            updateScores(data.scores);
            resultText.textContent = "VS";
            resultText.style.fontSize = "2.5rem";
            playerHand.src = "images/rock.png";
            compHand.src = "images/rock.png";
        } catch (err) {
            console.error("Error resetting game:", err);
        }
    });

    async function playRound(userChoice) {
        isPlaying = true;
        
        // Reset hands to rock for shaking animation
        playerHand.src = "images/rock.png";
        compHand.src = "images/rock.png";
        resultText.textContent = "...";
        resultText.style.fontSize = "2.5rem";

        // Add shake animation classes
        playerHand.classList.add('shake-player');
        compHand.classList.add('shake-comp');

        try {
            // Fetch AI move and result from backend
            const response = await fetch('/api/play', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ move: userChoice })
            });
            
            const data = await response.json();

            // Wait for animation to finish (1.5s as defined in CSS)
            setTimeout(() => {
                // Remove shake classes
                playerHand.classList.remove('shake-player');
                compHand.classList.remove('shake-comp');

                // Update images based on choices
                playerHand.src = `images/${data.user_move}.png`;
                compHand.src = `images/${data.computer_move}.png`;

                // Update result text
                resultText.textContent = data.result;
                
                // Adjust text size based on result length
                if(data.result === "Draw!") {
                    resultText.style.fontSize = "2.2rem";
                } else if(data.result === "You win!") {
                    resultText.style.fontSize = "2rem";
                    resultText.style.color = "#38bdf8";
                } else {
                    resultText.style.fontSize = "1.5rem";
                    resultText.style.color = "#f43f5e";
                }

                // Update scores
                updateScores(data.scores);

                isPlaying = false;
            }, 1500);

        } catch (error) {
            console.error("Error playing round:", error);
            resultText.textContent = "Error!";
            isPlaying = false;
            playerHand.classList.remove('shake-player');
            compHand.classList.remove('shake-comp');
        }
    }

    function updateScores(scores) {
        animateValue(userScoreEl, parseInt(userScoreEl.textContent), scores.user);
        animateValue(compScoreEl, parseInt(compScoreEl.textContent), scores.computer);
        animateValue(drawScoreEl, parseInt(drawScoreEl.textContent), scores.draws);
    }

    function animateValue(obj, start, end) {
        if (start === end) return;
        obj.classList.add('pop-score');
        obj.textContent = end;
        setTimeout(() => {
            obj.classList.remove('pop-score');
        }, 300);
    }
});
