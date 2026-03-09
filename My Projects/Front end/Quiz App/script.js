    (function() {
      // ---------- STATE ----------
      let questions = [];                // array of { question, options, correctIndex }
      let currentIndex = 0;
      let userAnswers = [];               // selected option index per question (null = no answer)
      let quizSubmitted = false;

      // DOM elements
      const questionText = document.getElementById('questionText');
      const optionsContainer = document.getElementById('optionsContainer');
      const counterEl = document.getElementById('counter');
      const scoreEl = document.getElementById('scoreValue');
      const nextBtn = document.getElementById('nextBtn');
      const prevBtn = document.getElementById('prevBtn');
      const newQuizBtn = document.getElementById('newQuizBtn');
      const playAgainBtn = document.getElementById('playAgainBtn');
      const resultPanel = document.getElementById('resultPanel');
      const finalScoreEl = document.getElementById('finalScore');
      const resultMessageEl = document.getElementById('resultMessage');
      const feedbackMsg = document.getElementById('feedbackMsg');
      const categorySelect = document.getElementById('categorySelect');

      // ---------- HELPER: decode HTML entities ----------
      function decodeHTMLEntities(text) {
        const textarea = document.createElement('textarea');
        textarea.innerHTML = text;
        return textarea.value;
      }

      // ---------- FETCH from Open Trivia DB ----------
      async function fetchQuestions() {
        const category = categorySelect.value;
        // show loading state
        questionText.innerHTML = '<i class="fas fa-spinner fa-spin"></i> fetching fresh questions...';
        optionsContainer.innerHTML = '';
        resultPanel.classList.add('hidden');
        feedbackMsg.textContent = '';

        try {
          const url = `https://opentdb.com/api.php?amount=5&category=${category}&type=multiple`;
          const response = await fetch(url);
          const data = await response.json();

          if (data.response_code !== 0 || !data.results.length) {
            throw new Error('No questions received');
          }

          // transform API data into our format
          questions = data.results.map((item) => {
            const questionText = decodeHTMLEntities(item.question);
            // decode all options
            const incorrect = item.incorrect_answers.map(ans => decodeHTMLEntities(ans));
            const correct = decodeHTMLEntities(item.correct_answer);

            // combine all options and shuffle (place correct at random position)
            const allOptions = [...incorrect];
            const correctIndex = Math.floor(Math.random() * (incorrect.length + 1));
            allOptions.splice(correctIndex, 0, correct);

            return {
              question: questionText,
              options: allOptions,
              correctIndex: correctIndex,
            };
          });

          // reset quiz state with new questions
          startNewQuiz();

        } catch (error) {
          questionText.textContent = '⚠️ Failed to load questions. Please try again.';
          optionsContainer.innerHTML = '';
          console.error('Fetch error:', error);
        }
      }

      // ---------- reset with current questions ----------
      function startNewQuiz() {
        currentIndex = 0;
        userAnswers = new Array(questions.length).fill(null);
        quizSubmitted = false;
        resultPanel.classList.add('hidden');
        feedbackMsg.textContent = '';
        renderQuestion();
      }

      // ---------- compute current score ----------
      function computeScore() {
        let correct = 0;
        for (let i = 0; i < questions.length; i++) {
          if (userAnswers[i] !== null && userAnswers[i] === questions[i].correctIndex) {
            correct++;
          }
        }
        return correct;
      }

      // ---------- update header (counter & score) ----------
      function updateHeader() {
        if (questions.length === 0) return;
        counterEl.textContent = `${currentIndex + 1}/${questions.length}`;
        scoreEl.textContent = computeScore();
      }

      // ---------- render current question & options ----------
      function renderQuestion() {
        if (!questions.length) return;

        const q = questions[currentIndex];
        questionText.textContent = q.question;
        updateHeader();

        let htmlStr = '';
        for (let i = 0; i < q.options.length; i++) {
          const optText = q.options[i];
          const isSelected = (userAnswers[currentIndex] === i);
          let optionClass = 'option';

          if (quizSubmitted) {
            // highlight correct/incorrect after submission
            if (i === q.correctIndex) {
              optionClass += ' correct';
            } else if (isSelected && i !== q.correctIndex) {
              optionClass += ' wrong';
            } else if (isSelected && i === q.correctIndex) {
              optionClass += ' correct';
            }
            optionClass += ' disabled-option';
          } else {
            if (isSelected) {
              optionClass += ' selected';
            }
          }

          // prefix letter (A, B, C, D)
          const prefix = String.fromCharCode(65 + i);

          htmlStr += `
            <div class="${optionClass}" data-opt-index="${i}">
              <span class="option-prefix">${prefix}</span>
              ${optText}
            </div>
          `;
        }

        optionsContainer.innerHTML = htmlStr;

        // attach click listeners (if not submitted)
        if (!quizSubmitted) {
          document.querySelectorAll('.option').forEach(opt => {
            opt.addEventListener('click', (e) => {
              if (quizSubmitted) return;
              const idx = parseInt(opt.dataset.optIndex, 10);
              // set answer for current question
              userAnswers[currentIndex] = idx;
              // re-render to reflect selection
              renderQuestion();
              // clear any feedback
              feedbackMsg.textContent = '';
            });
          });
        }

        // update button states and labels
        prevBtn.disabled = (currentIndex === 0);

        if (quizSubmitted) {
          nextBtn.disabled = true;
          nextBtn.innerHTML = `next <i class="fas fa-arrow-right"></i>`;
        } else {
          nextBtn.disabled = false;
          if (currentIndex === questions.length - 1) {
            nextBtn.innerHTML = `finish <i class="fas fa-check"></i>`;
          } else {
            nextBtn.innerHTML = `next <i class="fas fa-arrow-right"></i>`;
          }
        }
      }

      // ---------- finish quiz: compute final score, show result panel ----------
      function finishQuiz() {
        quizSubmitted = true;
        const finalScore = computeScore();

        finalScoreEl.textContent = `${finalScore} / ${questions.length}`;

        let message = '';
        if (finalScore === questions.length) message = '🌟 perfect! you nailed it.';
        else if (finalScore >= questions.length - 1) message = '🚀 almost there, brilliant!';
        else if (finalScore >= 3) message = '👍 good effort — keep learning!';
        else message = '🌱 nice start — practice makes progress.';
        resultMessageEl.textContent = message;

        resultPanel.classList.remove('hidden');
        renderQuestion();   // show correct/wrong highlights
        feedbackMsg.textContent = '✅ quiz completed — review your answers.';
      }

      // ---------- EVENT HANDLERS ----------
      nextBtn.addEventListener('click', (e) => {
        e.preventDefault();

        if (quizSubmitted) {
          // if already finished, just navigate (but next disabled anyway)
          return;
        }

        // validation: check if current question is answered
        if (userAnswers[currentIndex] === null) {
          feedbackMsg.textContent = '⚠️ please select an answer before proceeding.';
          return;
        }

        // if not on last question → go forward
        if (currentIndex < questions.length - 1) {
          currentIndex++;
          renderQuestion();
          feedbackMsg.textContent = ''; // clear warning
        }
        // if on last question and all answered → finish
        else if (currentIndex === questions.length - 1) {
          // check if all questions answered
          if (userAnswers.every(ans => ans !== null)) {
            finishQuiz();
          } else {
            feedbackMsg.textContent = '⚠️ answer all questions before finishing.';
          }
        }
      });

      prevBtn.addEventListener('click', (e) => {
        e.preventDefault();
        if (currentIndex > 0) {
          currentIndex--;
          renderQuestion();
          feedbackMsg.textContent = ''; // clear warnings when navigating
        }
      });

      // new quiz / play again: fetch fresh set from selected category
      function loadNewQuiz() {
        fetchQuestions();
      }

      newQuizBtn.addEventListener('click', (e) => {
        e.preventDefault();
        loadNewQuiz();
      });

      playAgainBtn.addEventListener('click', (e) => {
        e.preventDefault();
        loadNewQuiz();
      });

      // also reload when category changes (optional but user-friendly)
      categorySelect.addEventListener('change', () => {
        loadNewQuiz();
      });

      // initial load
      fetchQuestions();

      // expose for debugging (optional)
      window.selectOption = null; // not needed anymore, we use direct listeners
    })();
