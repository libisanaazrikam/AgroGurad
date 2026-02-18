document.addEventListener('DOMContentLoaded', () => {
    const scroller = document.querySelector('.scroll-container');
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav-links a');
    const dots = document.querySelectorAll('.scroll-indicator .dot');

    // Smooth Scroll Navigation
    function scrollToSection(id) {
        const section = document.querySelector(id);
        if (section) {
            section.scrollIntoView({ behavior: 'smooth' });
        }
    }

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            scrollToSection(targetId);
        });
    });

    dots.forEach(dot => {
        dot.addEventListener('click', () => {
            const targetId = dot.getAttribute('data-target');
            scrollToSection(targetId);
        });
    });

    // Active Section Highlighter using Intersection Observer
    const observerOptions = {
        root: scroller,
        threshold: 0.5
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = '#' + entry.target.id;

                // Update Nav Links
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === id) {
                        link.classList.add('active');
                    }
                });

                // Update Dots
                dots.forEach(dot => {
                    dot.classList.remove('active');
                    if (dot.getAttribute('data-target') === id) {
                        dot.classList.add('active');
                    }
                });

                // Trigger Animation
                const card = entry.target.querySelector('.glass-card');
                if (card) {
                    card.style.animation = 'none';
                    card.offsetHeight; /* trigger reflow */
                    card.style.animation = 'fadeInUp 1s ease-out';
                }
            }
        });
    }, observerOptions);

    sections.forEach(section => {
        observer.observe(section);
    });

    // Soil Form Submission
    const soilForm = document.getElementById('soilForm');
    if (soilForm) {
        soilForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(soilForm);
            const resultDiv = document.getElementById('soilResult');

            try {
                const response = await fetch('/soilgrade', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();

                if (data.error) {
                    resultDiv.innerHTML = `<p style="color:red">${data.error}</p>`;
                } else {
                    resultDiv.innerHTML = `
                        <h3>Soil Analysis Result</h3>
                        <p>Nitrogen (N): <strong>${data.N_grade}</strong></p>
                        <p>Phosphorous (P): <strong>${data.P_grade}</strong></p>
                        <p>Potassium (K): <strong>${data.K_grade}</strong></p>
                    `;
                    resultDiv.style.display = 'block';
                }
            } catch (err) {
                console.error(err);
                resultDiv.innerHTML = `<p style="color:red">Error processing request.</p>`;
            }
        });
    }

    // Crop Suggestion Form Submission
    const cropForm = document.getElementById('cropForm');
    if (cropForm) {
        cropForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(cropForm);
            const resultDiv = document.getElementById('cropResult');

            try {
                const response = await fetch('/suggesveg', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();

                if (data.error) {
                    resultDiv.innerHTML = `<p style="color:red">${data.error}</p>`;
                } else {
                    let html = `<h3>Recommended Crops</h3><div class="crop-grid">`;
                    data.recommendations.forEach(rec => {
                        html += `
                            <div class="crop-item">
                                ${rec.img ? `<img src="/static/${rec.img}" class="crop-img" alt="${rec.name}">` : ''}
                                <h4>${rec.name.toUpperCase()}</h4>
                                <p>${rec.prob}% Match</p>
                            </div>
                        `;
                    });
                    html += `</div>`;
                    resultDiv.innerHTML = html;
                    resultDiv.style.display = 'block';
                }
            } catch (err) {
                console.error(err);
                resultDiv.innerHTML = `<p style="color:red">Error processing request.</p>`;
            }
        });
    }

    // Flood Form Submission
    const floodForm = document.getElementById('floodForm');
    const floodModal = document.getElementById('floodModal');
    const closeBtn = document.querySelector('.close');
    const loadingDiv = document.getElementById('loading');
    const floodResultDiv = document.getElementById('floodResult');

    if (floodForm) {
        floodForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            // Show Modal and Loading
            floodModal.style.display = 'flex';
            loadingDiv.style.display = 'block';
            floodResultDiv.style.display = 'none';

            // Collect Data
            const formData = new FormData(floodForm);
            const symptoms = [];
            document.querySelectorAll('input[name="symptoms"]:checked').forEach(checkbox => {
                symptoms.push(checkbox.value);
            });

            const payload = {
                description: formData.get('description'),
                symptoms: symptoms
            };

            try {
                // Introduce fake delay for "Analyzing" animation feel
                await new Promise(r => setTimeout(r, 1500));

                const response = await fetch('/analyze_flood', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await response.json();

                if (data.error) {
                    floodResultDiv.innerHTML = `<p style="color:red">${data.error}</p>`;
                } else {
                    // Render Result
                    let html = `
                        <div class="analysis-section">
                            <h3 style="color:#e74c3c;">Problem Discovered</h3>
                            <p>${data.problem}</p>
                            <ul>${data.reasons.map(r => `<li>${r}</li>`).join('')}</ul>
                        </div>
                        
                        <div class="analysis-section" style="background:#f0f9eb; padding:10px; border-radius:8px; margin-top:10px;">
                            <h4 style="color:#2ecc71;">Immediate Actions</h4>
                            <ul>${data.immediate_actions.map(a => `<li><i class="fas fa-check-circle"></i> ${a}</li>`).join('')}</ul>
                        </div>

                        <div class="analysis-section" style="margin-top:15px;">
                            <h4>Suggested Fertilizers</h4>
                            <p>${data.fertilizers.length ? data.fertilizers.join(', ') : 'None specifically required.'}</p>
                        </div>
                        
                         <div class="analysis-section" style="margin-top:15px;">
                            <h4>Crops to Replant</h4>
                            <div class="crop-grid" style="grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));">
                                ${data.crops_to_plant.map(c => `<div class="crop-item" style="padding:5px;"><strong>${c}</strong></div>`).join('')}
                            </div>
                        </div>
                    `;
                    floodResultDiv.innerHTML = html;
                }
            } catch (err) {
                console.error(err);
                floodResultDiv.innerHTML = `<p style="color:red">Error communicating with server.</p>`;
            } finally {
                loadingDiv.style.display = 'none';
                floodResultDiv.style.display = 'block';
            }
        });
    }

    // Close Modal Logic
    if (closeBtn) {
        closeBtn.onclick = () => {
            floodModal.style.display = 'none';
        }
    }

    // Close if clicked outside
    window.onclick = (event) => {
        if (event.target == floodModal) {
            floodModal.style.display = 'none';
        }
    }

});
