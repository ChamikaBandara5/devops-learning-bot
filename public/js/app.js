/**
 * DevOps Learning Assistant - Interactive Frontend
 * Handles all UI interactions and API calls
 */

// API Base URL
const API_BASE = '';

// Current state
let currentCategory = '';
let currentQuestion = null;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initDockerTerminal();
    initKubernetesTerminal();
    initCICDVisualizer();
    initYAMLValidator();
    initQuiz();
    initAIExplainer();
});

// ============ Navigation ============
function initNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const tab = btn.dataset.tab;

            // Update nav buttons
            navButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Update tab content
            tabContents.forEach(content => {
                content.classList.remove('active');
                if (content.id === tab) {
                    content.classList.add('active');
                }
            });
        });
    });
}

// ============ Docker Terminal ============
function initDockerTerminal() {
    const input = document.getElementById('docker-input');
    const output = document.getElementById('docker-output');
    const cmdButtons = document.querySelectorAll('#docker .cmd-btn');

    input.addEventListener('keypress', async (e) => {
        if (e.key === 'Enter') {
            const command = input.value.trim();
            if (command) {
                await executeDocker(command);
                input.value = '';
            }
        }
    });

    cmdButtons.forEach(btn => {
        btn.addEventListener('click', async () => {
            const command = btn.dataset.cmd;
            input.value = command;
            await executeDocker(command);
            input.value = '';
        });
    });
}

async function executeDocker(command) {
    const output = document.getElementById('docker-output');

    // Add command to output
    output.innerHTML += `<p class="command">$ ${escapeHtml(command)}</p>`;

    try {
        const response = await fetch(`${API_BASE}/api/docker`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ command })
        });

        const data = await response.json();
        output.innerHTML += `<div class="output">${formatOutput(data.output)}</div>`;

        if (data.explanation) {
            const exp = data.explanation.en || data.explanation;
            output.innerHTML += `<div class="output info">${formatOutput(exp)}</div>`;
        }
    } catch (err) {
        output.innerHTML += `<p class="error">Error: ${err.message}</p>`;
    }

    output.scrollTop = output.scrollHeight;
}

// ============ Kubernetes Terminal ============
function initKubernetesTerminal() {
    const input = document.getElementById('k8s-input');
    const conceptCards = document.querySelectorAll('.concept-card');

    input.addEventListener('keypress', async (e) => {
        if (e.key === 'Enter') {
            const command = input.value.trim();
            if (command) {
                await executeKubectl(command);
                input.value = '';
            }
        }
    });

    conceptCards.forEach(card => {
        card.addEventListener('click', async () => {
            const concept = card.dataset.concept;
            await loadConcept(concept);
        });
    });
}

async function executeKubectl(command) {
    const output = document.getElementById('k8s-output');

    output.innerHTML += `<p class="command">$ ${escapeHtml(command)}</p>`;

    try {
        const response = await fetch(`${API_BASE}/api/kubernetes`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ command })
        });

        const data = await response.json();
        output.innerHTML += `<div class="output">${formatOutput(data.output)}</div>`;

        if (data.explanation) {
            const exp = data.explanation.en || data.explanation;
            output.innerHTML += `<div class="output info">${formatOutput(exp)}</div>`;
        }
    } catch (err) {
        output.innerHTML += `<p class="error">Error: ${err.message}</p>`;
    }

    output.scrollTop = output.scrollHeight;
}

async function loadConcept(name) {
    const output = document.getElementById('k8s-output');
    const lang = document.getElementById('sinhala-toggle')?.checked ? 'si' : 'en';

    try {
        const response = await fetch(`${API_BASE}/api/kubernetes/concept/${name}?lang=${lang}`);
        const data = await response.json();

        output.innerHTML += `<div class="output">${formatOutput(data.explanation)}</div>`;
    } catch (err) {
        output.innerHTML += `<p class="error">Error: ${err.message}</p>`;
    }

    output.scrollTop = output.scrollHeight;
}

// ============ CI/CD Visualizer ============
function initCICDVisualizer() {
    const visualizeBtn = document.getElementById('visualize-btn');
    const sampleBtns = document.querySelectorAll('.sample-btn');

    visualizeBtn?.addEventListener('click', visualizePipeline);

    sampleBtns.forEach(btn => {
        btn.addEventListener('click', async () => {
            const sample = btn.dataset.sample;
            await loadSampleWorkflow(sample);
        });
    });
}

async function loadSampleWorkflow(name) {
    try {
        const response = await fetch(`${API_BASE}/api/cicd/sample/${name}`);
        const data = await response.json();

        if (data.yaml) {
            document.getElementById('cicd-input').value = data.yaml;
            await visualizePipeline();
        }
    } catch (err) {
        console.error(err);
    }
}

async function visualizePipeline() {
    const input = document.getElementById('cicd-input');
    const output = document.getElementById('cicd-output');
    const content = input.value.trim();

    if (!content) {
        output.innerHTML = '<p class="placeholder">Please enter workflow YAML...</p>';
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/cicd/visualize`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content })
        });

        const data = await response.json();
        output.innerHTML = formatOutput(data.visualization);

        if (data.explanation) {
            output.innerHTML += `<div class="output info">${formatOutput(data.explanation)}</div>`;
        }
    } catch (err) {
        output.innerHTML = `<p class="error">Error: ${err.message}</p>`;
    }
}

// ============ YAML Validator ============
function initYAMLValidator() {
    const validateBtn = document.getElementById('validate-btn');
    validateBtn?.addEventListener('click', validateYAML);
}

async function validateYAML() {
    const input = document.getElementById('yaml-input');
    const output = document.getElementById('yaml-output');
    const content = input.value.trim();

    if (!content) {
        output.innerHTML = '<p class="placeholder">Please enter YAML content...</p>';
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/yaml/validate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content })
        });

        const data = await response.json();

        let html = `<div class="${data.valid ? 'success' : 'error'}">${formatOutput(data.output)}</div>`;

        if (data.explanation) {
            html += `<div class="output info">${formatOutput(data.explanation)}</div>`;
        }

        output.innerHTML = html;
    } catch (err) {
        output.innerHTML = `<p class="error">Error: ${err.message}</p>`;
    }
}

// ============ Quiz ============
function initQuiz() {
    const categoryBtns = document.querySelectorAll('.cat-btn');
    const showAnswerBtn = document.getElementById('show-answer');
    const nextQuestionBtn = document.getElementById('next-question');

    categoryBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            categoryBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentCategory = btn.dataset.category;
        });
    });

    showAnswerBtn?.addEventListener('click', showAnswer);
    nextQuestionBtn?.addEventListener('click', loadNewQuestion);
}

async function loadNewQuestion() {
    const questionText = document.getElementById('question-text');
    const answerText = document.getElementById('answer-text');

    answerText.classList.add('hidden');

    try {
        const url = currentCategory
            ? `${API_BASE}/api/quiz/question?category=${currentCategory}`
            : `${API_BASE}/api/quiz/question`;

        const response = await fetch(url);
        const data = await response.json();

        currentQuestion = data;
        questionText.innerHTML = `<strong>${data.category}</strong><br><br>${escapeHtml(data.question)}`;
    } catch (err) {
        questionText.innerHTML = `<p class="error">Error: ${err.message}</p>`;
    }
}

function showAnswer() {
    const answerText = document.getElementById('answer-text');
    const useSinhala = document.getElementById('sinhala-toggle')?.checked;

    if (currentQuestion) {
        const answer = useSinhala && currentQuestion.answer_si
            ? currentQuestion.answer_si
            : currentQuestion.answer;
        answerText.innerHTML = formatOutput(answer);
        answerText.classList.remove('hidden');
    }
}

// ============ AI Error Explainer ============
function initAIExplainer() {
    const explainBtn = document.getElementById('explain-btn');
    explainBtn?.addEventListener('click', explainError);
}

async function explainError() {
    const input = document.getElementById('error-input');
    const output = document.getElementById('ai-output');
    const useSinhala = document.getElementById('sinhala-explain')?.checked;
    const errorLog = input.value.trim();

    if (!errorLog) {
        output.innerHTML = '<p class="placeholder">Please enter an error message...</p>';
        return;
    }

    output.innerHTML = '<p><span class="loading"></span> Analyzing error...</p>';

    try {
        const response = await fetch(`${API_BASE}/api/explain`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                error: errorLog,
                lang: useSinhala ? 'si' : 'en'
            })
        });

        const data = await response.json();
        output.innerHTML = `<div class="output">${formatOutput(data.explanation)}</div>`;
    } catch (err) {
        output.innerHTML = `<p class="error">Error: ${err.message}</p>`;
    }
}

// ============ Utility Functions ============
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatOutput(text) {
    if (!text) return '';

    // Convert markdown-style formatting
    let html = escapeHtml(text);

    // Bold: **text**
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Code blocks: ```code```
    html = html.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');

    // Inline code: `code`
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

    // Line breaks
    html = html.replace(/\n/g, '<br>');

    return html;
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl + 1-6 for tab switching
    if (e.ctrlKey && e.key >= '1' && e.key <= '6') {
        e.preventDefault();
        const tabs = ['docker', 'kubernetes', 'cicd', 'yaml', 'quiz', 'ai'];
        const index = parseInt(e.key) - 1;
        if (tabs[index]) {
            document.querySelector(`[data-tab="${tabs[index]}"]`)?.click();
        }
    }
});
