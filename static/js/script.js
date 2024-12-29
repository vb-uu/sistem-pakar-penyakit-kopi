{
  /* <script>
  let currentQuestionIndex = 0;
  let answers = {};
  let questions = [];

  // Fetch pertanyaan dari server
  fetch("/static/soal.json")
    .then((response) => response.json())
    .then((data) => {
      questions = data;
      displayQuestion();
    })
    .catch((error) => console.error("Error fetching questions:", error));

  function displayQuestion() {
    const questionContainer = document.getElementById("question-container");
    questionContainer.innerText = questions[currentQuestionIndex];
  }

  function selectAnswer(value) {
    answers[currentQuestionIndex] = value;
    currentQuestionIndex++;

    if (currentQuestionIndex < questions.length) {
      displayQuestion();
    } else {
      submitAnswers();
    }
  }

  function submitAnswers() {
    fetch("/diagnose", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(answers),
    })
      .then((response) => response.json())
      .then((result) => {
        document.getElementById("question-container").style.display = "none";
        document.getElementById("answer-buttons").style.display = "none";
        document.getElementById("result").style.display = "block";

        document.getElementById(
          "diagnosis-result"
        ).innerText = `Penyakit: ${result.disease}`;
        document.getElementById(
          "solution-result"
        ).innerText = `Solusi: ${result.solution}`;
        document.getElementById(
          "confidence-result"
        ).innerText = `Kepercayaan: ${result.confidence}`;
      })
      .catch((error) => console.error("Error:", error));
  }

  window.onload = () => {
    document
      .querySelectorAll(".answer-btn")
      .forEach((btn) =>
        btn.addEventListener("click", () =>
          selectAnswer(btn.getAttribute("data-value"))
        )
      );
  };
</script> */
}
