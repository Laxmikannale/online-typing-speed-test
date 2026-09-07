let passageText = "";
let timer;
let timeLeft;
let typedText = "";
let errors = 0;
let isTestRunning = false;
let testDuration = 0; // store total duration globally

// Load passage from backend
function loadParagraph() {
    const difficulty = document.getElementById("difficulty").value;
    const durationMinutes = parseInt(document.getElementById("duration").value);

    fetch(`/get_paragraph/?difficulty=${encodeURIComponent(difficulty)}&duration=${durationMinutes}`)
        .then(response => response.json())
        .then(data => {
            if (data.text) {
                passageText = data.text.trim();
                document.getElementById("passage").innerText = passageText;
            } else {
                document.getElementById("passage").innerText = "⚠ No passage found.";
            }
        })
        .catch(error => {
            console.error("Error fetching paragraph:", error);
            document.getElementById("passage").innerText = "⚠ Failed to load passage.";
        });
}

// Start the typing test
function startTest(durationMinutes) {
    if (!passageText) {
        alert("No passage loaded. Please click 'Load Passage' first.");
        return;
    }

    testDuration = durationMinutes * 60;
    timeLeft = testDuration;
    errors = 0;
    typedText = "";
    isTestRunning = true;

    document.getElementById("typingArea").disabled = false;
    document.getElementById("typingArea").value = "";
    document.getElementById("typingArea").focus();

    document.getElementById("time").innerText = timeLeft;

    // Hide performance button if visible
    const perfBtn = document.getElementById("seePerformanceBtn");
    if (perfBtn) perfBtn.style.display = "none";

    timer = setInterval(updateTimer, 1000);
}

// Timer countdown
function updateTimer() {
    timeLeft--;
    document.getElementById("time").innerText = timeLeft;

    if (timeLeft <= 0) {
        endTest();
    }
}

// Typing input
document.getElementById("typingArea").addEventListener("input", function () {
    if (!isTestRunning) return;

    typedText = this.value;
    updateLiveStats();
});

function updateLiveStats() {
    let typedChars = typedText.split("");
    let passageChars = passageText.split("");

    errors = 0;
    for (let i = 0; i < typedChars.length; i++) {
        if (typedChars[i] !== passageChars[i]) {
            errors++;
        }
    }

    let wordsTyped = typedText.trim().split(/\s+/).filter(word => word.length > 0).length;
    let minutesElapsed = (testDuration - timeLeft) / 60;
    let wpm = minutesElapsed > 0 ? Math.round(wordsTyped / minutesElapsed) : 0;
    let accuracy = typedChars.length > 0
        ? Math.max(0, Math.round(((typedChars.length - errors) / typedChars.length) * 100))
        : 100;

    document.getElementById("wpm").innerText = wpm;
    document.getElementById("accuracy").innerText = accuracy + "%";
    document.getElementById("errors").innerText = errors;

    return { wpm, accuracy, errors };
}

// End the test -> save results -> show "See Performance" button
function endTest() {
    clearInterval(timer);
    isTestRunning = false;
    document.getElementById("typingArea").disabled = true;

    const finalStats = updateLiveStats();
    const difficulty = document.getElementById("difficulty").value;
    const durationMinutes = parseInt(document.getElementById("duration").value);

    fetch("/save_performance/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            wpm: finalStats.wpm,
            accuracy: finalStats.accuracy,
            difficulty: difficulty,
            duration: durationMinutes
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            // Show "See Your Performance" button instead of redirect
            let btn = document.getElementById("seePerformanceBtn");
            if (!btn) {
                btn = document.createElement("a");
                btn.id = "seePerformanceBtn";
                btn.href = "/performance/";
                btn.className = "btn btn-success mt-3";
                btn.innerText = "🎯 See Your Performance";
                document.getElementById("resultSection").appendChild(btn);
            }
            btn.style.display = "inline-block";
        } else {
            alert("Error saving results. Please try again.");
        }
    })
    .catch(error => console.error("Error saving performance:", error));
}

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
