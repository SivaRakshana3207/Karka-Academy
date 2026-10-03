/**
 * Karka AI and Tech Academy (karka.academy)
 * Gen-Z High-Performance Interactive Engine
 * Zero dependencies · 60fps animations · Instant responsiveness
 */

(function () {
  'use strict';

  // =========================================================================
  // Confetti Particle System (Lightweight Canvas Engine)
  // =========================================================================
  const Confetti = {
    canvas: null,
    ctx: null,
    particles: [],
    animationId: null,
    colors: ['#ff4d00', '#00f5ff', '#a855f7', '#ffb800', '#10b981', '#f43f5e'],

    init() {
      let canvas = document.getElementById('karka-confetti-canvas');
      if (!canvas) {
        canvas = document.createElement('canvas');
        canvas.id = 'karka-confetti-canvas';
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100vw';
        canvas.style.height = '100vh';
        canvas.style.pointerEvents = 'none';
        canvas.style.zIndex = '9999';
        document.body.appendChild(canvas);
      }
      this.canvas = canvas;
      this.ctx = canvas.getContext('2d');
      this.resize();
      window.addEventListener('resize', () => this.resize());
    },

    resize() {
      if (this.canvas) {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
      }
    },

    burst(x = window.innerWidth / 2, y = window.innerHeight * 0.4, count = 90) {
      if (!this.canvas) this.init();
      this.resize();

      for (let i = 0; i < count; i++) {
        const angle = Math.random() * Math.PI * 2;
        const velocity = Math.random() * 8 + 4;
        this.particles.push({
          x: x,
          y: y,
          vx: Math.cos(angle) * velocity,
          vy: Math.sin(angle) * velocity - 2,
          size: Math.random() * 8 + 4,
          color: this.colors[Math.floor(Math.random() * this.colors.length)],
          rotation: Math.random() * 360,
          rotationSpeed: (Math.random() - 0.5) * 12,
          opacity: 1,
          gravity: 0.22,
          decay: Math.random() * 0.015 + 0.012
        });
      }

      if (!this.animationId) {
        this.loop();
      }
    },

    loop() {
      if (!this.ctx) return;
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

      for (let i = this.particles.length - 1; i >= 0; i--) {
        const p = this.particles[i];
        p.x += p.vx;
        p.y += p.vy;
        p.vy += p.gravity;
        p.rotation += p.rotationSpeed;
        p.opacity -= p.decay;

        if (p.opacity <= 0 || p.y > this.canvas.height + 20) {
          this.particles.splice(i, 1);
          continue;
        }

        this.ctx.save();
        this.ctx.translate(p.x, p.y);
        this.ctx.rotate((p.rotation * Math.PI) / 180);
        this.ctx.globalAlpha = Math.max(0, p.opacity);
        this.ctx.fillStyle = p.color;
        this.ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 0.6);
        this.ctx.restore();
      }

      if (this.particles.length > 0) {
        this.animationId = requestAnimationFrame(() => this.loop());
      } else {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.animationId = null;
      }
    }
  };

  // =========================================================================
  // Terminal Simulation Runner (Hero Section)
  // =========================================================================
  const initTerminalSimulation = () => {
    const runBtn = document.getElementById('btn-run-simulation');
    const simOutput = document.getElementById('terminal-sim-output');
    if (!runBtn || !simOutput) return;

    let isRunning = false;
    const stages = [
      { text: '➜ [1/4] Compiling autonomous LLM Agent container...', color: 'var(--accent-cyan)' },
      { text: '➜ [2/4] Indexing client documentation into ChromaDB Vector Store...', color: 'var(--accent-violet)' },
      { text: '➜ [3/4] Running automated test suite (42 unit tests passed in 0.8s)...', color: 'var(--accent-yellow)' },
      { text: '✔ [4/4] STATUS 200 OK: Production Container Deployed! Latency: 98ms 🚀', color: 'var(--accent-green)' }
    ];

    runBtn.addEventListener('click', () => {
      if (isRunning) return;
      isRunning = true;
      runBtn.disabled = true;
      runBtn.innerHTML = '<span class="spinner-dot"></span> <span>Executing Pipeline...</span>';

      let stageIndex = 0;
      simOutput.innerHTML = '<span class="term-arrow">➜</span> Initializing build environment...';
      simOutput.style.color = 'var(--text-muted)';

      const interval = setInterval(() => {
        if (stageIndex < stages.length) {
          const current = stages[stageIndex];
          simOutput.innerHTML = `<span style="color: ${current.color}">${current.text}</span>`;
          stageIndex++;
        } else {
          clearInterval(interval);
          isRunning = false;
          runBtn.disabled = false;
          runBtn.innerHTML = '<span>▶ Re-run Simulation</span>';
          Confetti.burst(window.innerWidth * 0.75, window.innerHeight * 0.45, 70);
        }
      }, 700);
    });
  };

  // =========================================================================
  // Career Tracks Category Filter
  // =========================================================================
  const initTrackFilters = () => {
    const filterButtons = document.querySelectorAll('.track-filter-btn');
    const trackCards = document.querySelectorAll('.track-card');
    if (!filterButtons.length || !trackCards.length) return;

    filterButtons.forEach((btn) => {
      btn.addEventListener('click', () => {
        const filter = btn.dataset.filter;

        filterButtons.forEach((b) => {
          const isActive = b === btn;
          b.classList.toggle('active', isActive);
          b.setAttribute('aria-selected', String(isActive));
        });

        trackCards.forEach((card) => {
          const category = card.dataset.category;
          const matches = filter === 'all' || category === filter;

          if (matches) {
            card.style.display = 'flex';
            card.style.opacity = '0';
            card.style.transform = 'translateY(16px)';
            requestAnimationFrame(() => {
              card.style.transition = 'opacity 0.35s ease, transform 0.35s ease';
              card.style.opacity = '1';
              card.style.transform = 'translateY(0)';
            });
          } else {
            card.style.display = 'none';
          }
        });
      });
    });
  };

  // =========================================================================
  // Dynamic Syllabus Inspection Modal
  // =========================================================================
  const initSyllabusModal = () => {
    const modalBackdrop = document.getElementById('syllabus-modal-backdrop');
    const modalTarget = document.getElementById('modal-content-target');
    const modalCloseBtn = document.getElementById('modal-close-btn');
    const triggers = document.querySelectorAll('.syllabus-trigger');

    if (!modalBackdrop || !modalTarget) return;

    const tracksData = window.KARKA_TRACKS || [];

    const openModal = (trackId) => {
      const track = tracksData.find((t) => t.id === trackId) || tracksData[0];
      if (!track) return;

      const syllabusHtml = (track.syllabus || [])
        .map(
          (item) => `
        <div class="syllabus-week-item">
          <div class="week-badge">
            <span class="week-number">${item.week}</span>
          </div>
          <div class="week-content">
            <p class="week-topic">${item.topic}</p>
          </div>
        </div>
      `
        )
        .join('');

      const stackChips = (track.stack || [])
        .map((s) => `<span class="stack-chip">${s}</span>`)
        .join('');

      modalTarget.innerHTML = `
        <div class="modal-track-header">
          <div class="modal-track-topline">
            <span class="track-kicker">${track.eyebrow || 'INTENSIVE TRACK'}</span>
            <span class="track-salary-badge">${track.salary_range}</span>
          </div>
          <h2 id="modal-track-title" class="modal-track-title">${track.title}</h2>
          <p class="modal-track-desc">${track.desc}</p>
          <div class="modal-key-outcome">
            <span>🎯 Placement Target: <strong>${track.key_outcome}</strong></span>
          </div>
        </div>

        <div class="modal-meta-bar">
          <div class="modal-meta-item">
            <span class="meta-label">Duration</span>
            <strong>${track.duration}</strong>
          </div>
          <div class="modal-meta-item">
            <span class="meta-label">Upfront Tuition</span>
            <strong class="text-accent">₹0 (Pay After Placement)</strong>
          </div>
          <div class="modal-meta-item">
            <span class="meta-label">Client Projects</span>
            <strong>${track.projects_count}</strong>
          </div>
        </div>

        <div class="modal-tech-stack">
          <h4>What you’ll learn</h4>
          <div class="modal-chips-row">${stackChips}</div>
        </div>

        <div class="modal-syllabus-section">
          <h4>Learning plan</h4>
          <div class="syllabus-timeline">${syllabusHtml}</div>
        </div>

        <div class="modal-actions-row">
          <a class="btn btn-primary btn-lg" href="/apply?track=${encodeURIComponent(track.id)}">
            <span>Enroll in ${track.title} (₹0 Upfront) ⚡</span>
          </a>
          <a class="btn btn-secondary" href="https://wa.me/919345580857?text=Hi%20Karka%20Admissions!%20I%20have%20questions%20about%20the%20${encodeURIComponent(track.title)}%20syllabus." target="_blank" rel="noopener">
            <span>Ask on WhatsApp 💬</span>
          </a>
        </div>
      `;

      modalBackdrop.style.display = 'flex';
      modalBackdrop.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';

      // Focus close button for accessibility
      if (modalCloseBtn) modalCloseBtn.focus();
    };

    const closeModal = () => {
      modalBackdrop.style.display = 'none';
      modalBackdrop.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    };

    triggers.forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const trackId = btn.dataset.trackId;
        openModal(trackId);
      });
    });

    if (modalCloseBtn) {
      modalCloseBtn.addEventListener('click', closeModal);
    }

    modalBackdrop.addEventListener('click', (e) => {
      if (e.target === modalBackdrop) {
        closeModal();
      }
    });

    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modalBackdrop.getAttribute('aria-hidden') === 'false') {
        closeModal();
      }
    });
  };

  // =========================================================================
  // Interactive Pay After Placement ROI Calculator
  // =========================================================================
  const initRoiCalculator = () => {
    const slider = document.getElementById('salary-range-input');
    const salaryDisplay = document.getElementById('calc-salary-display');
    const monthlyPayDisplay = document.getElementById('calc-monthly-pay');
    const threeYrIncomeDisplay = document.getElementById('calc-3yr-income');

    if (!slider || !salaryDisplay || !monthlyPayDisplay || !threeYrIncomeDisplay) return;

    const updateCalculator = () => {
      const lpa = parseFloat(slider.value) || 6.5;
      salaryDisplay.textContent = `₹ ${lpa.toFixed(1)} LPA`;

      // Gross salary estimate before tax and other deductions.
      const annualRupees = lpa * 100000;
      const monthlyGross = Math.round(annualRupees / 12);
      monthlyPayDisplay.textContent = `₹ ${monthlyGross.toLocaleString('en-IN')} / mo`;

      // 3-Year cumulative earnings with estimated 12% annual compounding hike
      const yr1 = annualRupees;
      const yr2 = annualRupees * 1.12;
      const yr3 = annualRupees * 1.25;
      const threeYrTotal = Math.round(yr1 + yr2 + yr3);
      threeYrIncomeDisplay.textContent = `₹ ${threeYrTotal.toLocaleString('en-IN')}`;
    };

    slider.addEventListener('input', updateCalculator);
    updateCalculator(); // Initialize on load
  };

  // =========================================================================
  // The 4-Pillar Career Engine Selector
  // =========================================================================
  const initPillarsEngine = () => {
    const pillarButtons = document.querySelectorAll('.pillar-select-btn');
    const pillarCards = document.querySelectorAll('.pillar-card-inner');
    if (!pillarButtons.length || !pillarCards.length) return;

    pillarButtons.forEach((btn) => {
      btn.addEventListener('click', () => {
        const index = btn.dataset.pillarIndex;

        pillarButtons.forEach((b) => {
          const isActive = b === btn;
          b.classList.toggle('active', isActive);
          b.setAttribute('aria-selected', String(isActive));
        });

        pillarCards.forEach((card) => {
          const isTarget = card.id === `pillar-card-${index}`;
          card.classList.toggle('active', isTarget);
          if (isTarget) {
            card.style.opacity = '0';
            card.style.transform = 'translateY(12px)';
            requestAnimationFrame(() => {
              card.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
              card.style.opacity = '1';
              card.style.transform = 'translateY(0)';
            });
          }
        });
      });
    });
  };

  // =========================================================================
  // 180-Day Career Simulator Stepper
  // =========================================================================
  const initCareerSimulator = () => {
    const stageButtons = document.querySelectorAll('.stage-node-btn');
    const simActiveDay = document.getElementById('sim-active-day');
    const simActiveMilestone = document.getElementById('sim-active-milestone');
    const simActiveTitle = document.getElementById('sim-active-title');
    const simActiveSkills = document.getElementById('sim-active-skills');

    if (!stageButtons.length || !simActiveDay || !simActiveTitle || !simActiveSkills) return;

    const simulatorData = window.KARKA_SIMULATOR || [];

    stageButtons.forEach((btn) => {
      btn.addEventListener('click', () => {
        const index = parseInt(btn.dataset.stageIndex, 10);
        const stage = simulatorData[index];
        if (!stage) return;

        stageButtons.forEach((b) => {
          const isActive = b === btn;
          b.classList.toggle('active', isActive);
          b.setAttribute('aria-selected', String(isActive));
        });

        simActiveDay.textContent = stage.day;
        if (simActiveMilestone) simActiveMilestone.textContent = `🎯 Milestone: ${stage.milestone}`;
        simActiveTitle.textContent = stage.title;

        simActiveSkills.innerHTML = (stage.skills || [])
          .map((item) => `<li>${item}</li>`)
          .join('');

        const displayCard = document.querySelector('.simulator-display-card');
        if (displayCard) {
          displayCard.style.opacity = '0.7';
          requestAnimationFrame(() => {
            displayCard.style.transition = 'opacity 0.25s ease';
            displayCard.style.opacity = '1';
          });
        }
      });
    });
  };

  // =========================================================================
  // 60-Second Matchmaker Questionnaire & XP Rewards
  // =========================================================================
  const initMatchmakerQuiz = () => {
    const form = document.getElementById('discovery-form');
    const resultPanel = document.getElementById('path-result');
    if (!form || !resultPanel) return;

    const titleEl = document.getElementById('discover-title');
    const goalEl = document.getElementById('discover-goal');
    const journeyEl = document.getElementById('discover-journey');
    const summaryEl = document.getElementById('discover-summary');
    const xpRewardEl = document.getElementById('xp-reward');
    const enrollBtn = document.getElementById('btn-quiz-enroll');

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(form);
      const interest = (formData.get('interest') || '').toString();
      const level = (formData.get('level') || '').toString();
      const role = (formData.get('role') || '').toString();
      const time = (formData.get('time') || '').toString();

      if (!interest || !level || !role) return;

      // Smart Track Recommendation Logic
      let matchedTrackId = 'fullstack';
      let matchedTrackName = 'React + Python Fullstack Development';
      let matchedJourney = 'Programming Foundations → Modern React 19 → Python FastAPI Microservices → Client Deliverables → Placement';

      if (interest.includes('Generative AI') || role.includes('Gen AI')) {
        matchedTrackId = 'genai';
        matchedTrackName = 'Generative AI & LLM Engineering';
        matchedJourney = 'Python Fundamentals → Vector RAG Pipelines → LangChain Autonomous Agents → Model Deployment → Placement';
      } else if (interest.includes('Data Science') || role.includes('Data Scientist')) {
        matchedTrackId = 'datascience';
        matchedTrackName = 'AI, Machine Learning & Data Science';
        matchedJourney = 'SQL & Data Wrangling → Scikit-Learn Predictive Modeling → PyTorch Deep Learning → Dashboard Demos → Placement';
      } else if (interest.includes('UI/UX') || role.includes('UI/UX')) {
        matchedTrackId = 'uiux';
        matchedTrackName = 'UI/UX & Product Experience Design';
        matchedJourney = 'Design Thinking & UX Psychology → Figma Design Systems 5.0 → Micro-Prototyping → Portfolio Case Studies → Placement';
      } else if (interest.includes('Internship') || role.includes('Internship')) {
        matchedTrackId = 'internship';
        matchedTrackName = 'Full Stack Developer Internship';
        matchedJourney = 'Codebase Orientation → Daily Standups & Code Reviews → Live Client Features → Pre-Placement Offer (PPO)';
      }

      if (titleEl) titleEl.textContent = matchedTrackName;
      if (goalEl) goalEl.textContent = role;
      if (journeyEl) journeyEl.textContent = matchedJourney;
      if (summaryEl) {
        summaryEl.textContent = `Given your ${level} background and dedication of ${time}, we've selected ${matchedTrackName} as your optimal 180-day rocketship. Zero upfront fees — you only pay once placed.`;
      }
      if (enrollBtn) {
        enrollBtn.href = `/apply?track=${encodeURIComponent(matchedTrackId)}`;
      }

      // Gamified XP System
      try {
        const storedXp = parseInt(localStorage.getItem('karka_builder_xp') || '0', 10);
        const newXp = storedXp + 150;
        localStorage.setItem('karka_builder_xp', newXp.toString());
        if (xpRewardEl) {
          xpRewardEl.textContent = `+150 XP UNLOCKED! (${newXp} TOTAL BUILDER XP) ⚡`;
        }
      } catch (err) {
        if (xpRewardEl) xpRewardEl.textContent = '+150 XP UNLOCKED! ⚡';
      }

      // Reveal Result with Smooth Scroll & Celebration
      resultPanel.hidden = false;
      resultPanel.style.display = 'block';
      resultPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      Confetti.burst(window.innerWidth / 2, window.innerHeight * 0.35, 100);

      // Async lead capture for admissions team
      try {
        await fetch('/api/discovery', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            selected_path: matchedTrackName,
            current_level: level,
            goal: role,
            journey: matchedJourney
          })
        });
      } catch (err) {
        console.warn('Discovery API sync offline, local match saved:', err);
      }
    });
  };

  // =========================================================================
  // AI Career Concierge 2.0 (Chat Widget)
  // =========================================================================
  const initAiConcierge = () => {
    const form = document.getElementById('assistant-form');
    const input = document.getElementById('assistant-input');
    const chatContainer = document.getElementById('assistant-chat');
    const chips = document.querySelectorAll('.chip-query');

    if (!form || !input || !chatContainer) return;

    const appendMessage = (text, sender, isTyping = false) => {
      const bubble = document.createElement('div');
      bubble.className = `chat-bubble ${sender}${isTyping ? ' typing-bubble' : ''}`;

      if (sender === 'bot') {
        bubble.innerHTML = `
          <div class="bot-header"><span class="bot-icon">🤖</span> <strong>Karka AI:</strong></div>
          <div class="bot-text">${text}</div>
        `;
      } else {
        bubble.innerHTML = `
          <div class="user-header"><span class="user-icon">👤</span> <strong>You:</strong></div>
          <div class="user-text">${text}</div>
        `;
      }

      chatContainer.appendChild(bubble);
      chatContainer.scrollTop = chatContainer.scrollHeight;
      return bubble;
    };

    const handleSend = async (messageText) => {
      const text = messageText.trim();
      if (!text) return;

      appendMessage(text, 'user');
      input.value = '';
      input.disabled = true;

      const typingBubble = appendMessage('Consulting Karka admissions database...', 'bot', true);

      try {
        const response = await fetch('/api/assistant', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: text })
        });
        const data = await response.json();
        typingBubble.remove();
        appendMessage(data.answer || 'I am ready to help with our career tracks, client projects, or Pay After Placement admissions.', 'bot');
      } catch (err) {
        typingBubble.remove();
        appendMessage('I am currently syncing with Karka admissions mentors. You can also chat directly on WhatsApp at +91 93455 80857 for immediate guidance!', 'bot');
      } finally {
        input.disabled = false;
        input.focus();
      }
    };

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      handleSend(input.value);
    });

    chips.forEach((chip) => {
      chip.addEventListener('click', () => {
        const query = chip.textContent.trim();
        handleSend(query);
      });
    });
  };

  // =========================================================================
  // Mobile Navigation Drawer
  // =========================================================================
  const initMobileNavigation = () => {
    const menuBtn = document.getElementById('mobile-menu-btn');
    const drawer = document.getElementById('mobile-drawer');
    const closeBtn = document.getElementById('mobile-close-btn');

    if (!menuBtn || !drawer) return;

    const openDrawer = () => {
      drawer.classList.add('open');
      drawer.setAttribute('aria-hidden', 'false');
      menuBtn.setAttribute('aria-expanded', 'true');
      document.body.style.overflow = 'hidden';
    };

    const closeDrawer = () => {
      drawer.classList.remove('open');
      drawer.setAttribute('aria-hidden', 'true');
      menuBtn.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    };

    menuBtn.addEventListener('click', () => {
      const isOpen = drawer.classList.contains('open');
      if (isOpen) closeDrawer();
      else openDrawer();
    });

    if (closeBtn) closeBtn.addEventListener('click', closeDrawer);

    drawer.querySelectorAll('.mobile-link').forEach((link) => {
      link.addEventListener('click', closeDrawer);
    });
  };

  // =========================================================================
  // FAQ Accordion
  // =========================================================================
  const initFaqAccordion = () => {
    const items = document.querySelectorAll('.faq-item');
    if (!items.length) return;

    items.forEach((item) => {
      const button = item.querySelector('.faq-question');
      if (!button) return;

      button.addEventListener('click', () => {
        const isOpen = item.classList.contains('open');

        // Close others for clean accordion feel
        items.forEach((other) => {
          other.classList.remove('open');
          const otherBtn = other.querySelector('.faq-question');
          if (otherBtn) {
            otherBtn.setAttribute('aria-expanded', 'false');
            const icon = other.querySelector('.faq-icon-cross');
            if (icon) icon.textContent = '+';
          }
        });

        if (!isOpen) {
          item.classList.add('open');
          button.setAttribute('aria-expanded', 'true');
          const icon = item.querySelector('.faq-icon-cross');
          if (icon) icon.textContent = '−';
        }
      });
    });
  };

  // =========================================================================
  // Scroll Reveal Animations (IntersectionObserver)
  // =========================================================================
  const initScrollReveals = () => {
    const reveals = document.querySelectorAll('.reveal');
    if (!reveals.length) return;

    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add('visible');
              observer.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
      );

      reveals.forEach((el) => observer.observe(el));
    } else {
      reveals.forEach((el) => el.classList.add('visible'));
    }
  };

  // =========================================================================
  // Auto-Confetti for Success Page
  // =========================================================================
  const initSuccessCelebration = () => {
    const successPlaceholder = document.getElementById('confetti-canvas');
    if (successPlaceholder || window.location.pathname.includes('/success')) {
      setTimeout(() => {
        Confetti.burst(window.innerWidth / 2, window.innerHeight * 0.35, 120);
        setTimeout(() => {
          Confetti.burst(window.innerWidth * 0.3, window.innerHeight * 0.45, 60);
          Confetti.burst(window.innerWidth * 0.7, window.innerHeight * 0.45, 60);
        }, 400);
      }, 300);
    }
  };

  // =========================================================================
  // Bootloader
  // =========================================================================
  const bootKarkaEngine = () => {
    initTerminalSimulation();
    initTrackFilters();
    initSyllabusModal();
    initRoiCalculator();
    initPillarsEngine();
    initCareerSimulator();
    initMatchmakerQuiz();
    initAiConcierge();
    initMobileNavigation();
    initFaqAccordion();
    initScrollReveals();
    initSuccessCelebration();
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bootKarkaEngine);
  } else {
    bootKarkaEngine();
  }
})();
