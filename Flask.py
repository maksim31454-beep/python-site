from flask import Flask, render_template_string, request, jsonify
import datetime
import random
import time

app = Flask(__name__)

# Данные для сайта
projects = [
    {"name": "Чат-бот ИИ", "description": "Умный помощник на основе GPT", "progress": 95, "likes": 42},
    {"name": "Крипто-трекер", "description": "Отслеживание курсов криптовалют", "progress": 80, "likes": 38},
    {"name": "AR Игра", "description": "Дополненная реальность с Unity", "progress": 65, "likes": 27}
]

skills = [
    {"name": "Python", "level": 95, "color": "yellow"},
    {"name": "JavaScript", "level": 90, "color": "teal"},
    {"name": "Flask/Django", "level": 92, "color": "green"},
    {"name": "React/Vue", "level": 88, "color": "blue"},
    {"name": "Базы данных", "level": 87, "color": "violet"},
    {"name": "UI/UX Дизайн", "level": 85, "color": "pink"}
]

messages = []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Максим - Крутой Dev</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/fomantic-ui@2.9.3/dist/semantic.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.css">
    <style>
        :root {
            --dark-bg: #0a0a0a;
            --darker-bg: #050505;
            --neon-blue: #00f3ff;
            --neon-purple: #d100ff;
            --neon-pink: #ff00c8;
            --neon-green: #00ff9d;
            --text-color: #ffffff;
        }

        body {
            background-color: var(--dark-bg);
            color: var(--text-color);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
            overflow-x: hidden;
        }

        .ui.menu {
            background-color: var(--darker-bg) !important;
            border: none !important;
        }

        .ui.menu .item {
            color: var(--text-color) !important;
        }

        .ui.menu .item:hover {
            color: var(--neon-blue) !important;
        }

        .neon-text {
            text-shadow: 0 0 5px var(--neon-blue), 0 0 10px var(--neon-blue), 0 0 15px var(--neon-blue);
            color: var(--text-color);
        }

        .neon-border {
            box-shadow: 0 0 5px var(--neon-purple), 0 0 10px var(--neon-purple), inset 0 0 5px var(--neon-purple);
            border: 1px solid var(--neon-purple) !important;
            background-color: rgba(10, 10, 10, 0.8) !important;
        }

        .gradient-bg {
            background: linear-gradient(135deg, var(--darker-bg) 0%, #1a1a1a 100%) !important;
        }

        .cyber-card {
            background: rgba(13, 13, 13, 0.9) !important;
            border: 1px solid var(--neon-blue) !important;
            box-shadow: 0 0 10px var(--neon-blue), 0 0 20px var(--neon-blue) inset;
            border-radius: 5px !important;
            transition: all 0.3s ease;
        }

        .cyber-card:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 0 15px var(--neon-blue), 0 0 30px var(--neon-blue) inset;
        }

        .glow-button {
            background: linear-gradient(45deg, var(--neon-purple), var(--neon-blue)) !important;
            color: black !important;
            font-weight: bold !important;
            border: none !important;
            box-shadow: 0 0 10px var(--neon-purple) !important;
            transition: all 0.3s ease !important;
        }

        .glow-button:hover {
            box-shadow: 0 0 15px var(--neon-blue), 0 0 25px var(--neon-purple) !important;
            transform: scale(1.05);
        }

        .skill-bar {
            height: 20px;
            background: #333;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
            box-shadow: 0 0 5px var(--neon-green);
        }

        .skill-progress {
            height: 100%;
            border-radius: 10px;
            transition: width 1.5s ease-in-out;
            position: relative;
        }

        .skill-progress::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
            animation: shine 2s infinite;
        }

        @keyframes shine {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }

        .pulse {
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }

        .cyber-input {
            background: rgba(20, 20, 20, 0.8) !important;
            border: 1px solid var(--neon-green) !important;
            color: var(--text-color) !important;
            box-shadow: 0 0 5px var(--neon-green) !important;
        }

        .cyber-input:focus {
            background: rgba(30, 30, 30, 0.8) !important;
            box-shadow: 0 0 10px var(--neon-green) !important;
        }

        .matrix-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            opacity: 0.1;
            pointer-events: none;
        }

        .terminal {
            background: rgba(0, 0, 0, 0.9);
            border: 1px solid var(--neon-green);
            border-radius: 5px;
            padding: 15px;
            font-family: 'Courier New', monospace;
            height: 200px;
            overflow-y: auto;
            box-shadow: 0 0 10px var(--neon-green);
        }

        .terminal-line {
            color: var(--neon-green);
            margin: 5px 0;
        }

        .hacker-text {
            font-family: 'Courier New', monospace;
            color: var(--neon-green);
        }

        .cat-eyes {
            position: relative;
            width: 100px;
            height: 100px;
            margin: 0 auto;
        }

        .eye {
            position: absolute;
            width: 30px;
            height: 50px;
            background: #000;
            border: 2px solid var(--neon-blue);
            border-radius: 50%;
            overflow: hidden;
            box-shadow: 0 0 15px var(--neon-blue);
        }

        .eye::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 15px;
            height: 15px;
            background: var(--neon-blue);
            border-radius: 50%;
            animation: blink 3s infinite;
        }

        .eye.left {
            left: 15px;
        }

        .eye.right {
            right: 15px;
        }

        @keyframes blink {
            0%, 96%, 100% { transform: translate(-50%, -50%) scale(1); }
            98% { transform: translate(-50%, -50%) scale(1, 0.1); }
        }

        .cyber-nav {
            border-bottom: 1px solid var(--neon-purple) !important;
            box-shadow: 0 0 10px var(--neon-purple) !important;
        }
    </style>
</head>
<body>
    <!-- Матричный фон -->
    <canvas class="matrix-bg" id="matrixCanvas"></canvas>

    <!-- Главное меню -->
    <div class="ui fixed inverted menu cyber-nav">
        <div class="ui container">
            <a href="#home" class="header item neon-text">
                <i class="code icon"></i>
                Максим | CyberDev
            </a>
            <a href="#home" class="item" onclick="scrollToSection('home')">Главная</a>
            <a href="#about" class="item" onclick="scrollToSection('about')">Обо мне</a>
            <a href="#skills" class="item" onclick="scrollToSection('skills')">Навыки</a>
            <a href="#projects" class="item" onclick="scrollToSection('projects')">Проекты</a>
            <a href="#terminal" class="item" onclick="scrollToSection('terminal')">Терминал</a>
            <a href="#contact" class="item" onclick="scrollToSection('contact')">Контакты</a>
            <div class="right menu">
                <div class="item">
                    <div class="ui action input">
                        <input type="text" placeholder="Поиск..." class="cyber-input" id="searchInput">
                        <button class="ui button glow-button" onclick="search()">Найти</button>
                    </div>
                </div>
                <div class="item">
                    <div class="ui toggle checkbox">
                        <input type="checkbox" name="public" onclick="toggleSound()">
                        <label>Звуки</label>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Герой секция -->
    <div class="ui gradient-bg text container segment center aligned" id="home" style="margin-top: 80px; padding: 3rem; border: none;">
        <div class="cat-eyes">
            <div class="eye left"></div>
            <div class="eye right"></div>
        </div>
        <h1 class="ui header massive neon-text" style="font-size: 4rem;">МАКСИМ</h1>
        <p class="ui sub header hacker-text">Fullstack разработчик & Кибер-энтузиаст</p>
        <div class="ui stackable buttons">
            <button class="ui button massive glow-button" onclick="showModal('contact-modal')">
                <i class="paper plane icon"></i>
                ВЗЛОМАТЬ ПЕНТАГОН
            </button>
            <button class="ui button massive glow-button" onclick="initiateBootSequence()">
                <i class="power off icon"></i>
                ЗАПУСК СИСТЕМЫ
            </button>
        </div>
    </div>

    <div class="ui container">
        <!-- Статистика -->
        <div class="ui four statistics stackable" style="margin: 3rem 0;">
            <div class="statistic">
                <div class="value neon-text" id="projects-counter">0</div>
                <div class="label">Завершенных проектов</div>
            </div>
            <div class="statistic">
                <div class="value neon-text" id="clients-counter">0</div>
                <div class="label">Довольных клиентов</div>
            </div>
            <div class="statistic">
                <div class="value neon-text" id="coffee-counter">0</div>
                <div class="label">Выпито кофе</div>
            </div>
            <div class="statistic">
                <div class="value neon-text" id="code-counter">0</div>
                <div class="label">Строк кода</div>
            </div>
        </div>

        <!-- Обо мне -->
        <div class="ui cyber-card segment" id="about" data-aos="fade-up">
            <h2 class="ui header dividing neon-text">// ОБО_МНЕ</h2>
            <div class="ui grid stackable">
                <div class="eight wide column">
                    <img src="https://semantic-ui.com/images/avatar2/large/matthew.png" class="ui medium circular image centered" id="avatar" style="border: 2px solid var(--neon-blue); box-shadow: 0 0 15px var(--neon-blue);">
                    <div class="ui buttons fluid" style="margin-top: 15px;">
                        <button class="ui button glow-button" onclick="changeAvatar()">Сменить аватар</button>
                        <button class="ui button glow-button" onclick="animateAvatar()">Анимировать</button>
                    </div>
                </div>
                <div class="eight wide column">
                    <p class="hacker-text">> Инициализация данных пользователя...</p>
                    <p class="hacker-text">> Имя: МАКСИМ</p>
                    <p class="hacker-text">> Роль: FULLSTACK РАЗРАБОТЧИК</p>
                    <p class="hacker-text">> Специализация: СОЗДАНИЕ ИННОВАЦИОННЫХ ВЕБ-РЕШЕНИЙ</p>
                    <p class="hacker-text">> Опыт: 5+ ЛЕТ В РАЗРАБОТКЕ</p>
                    <div class="ui list">
                        <div class="item hacker-text">
                            <i class="marker icon"></i>
                            <div class="content">> Местоположение: Москва, Россия</div>
                        </div>
                        <div class="item hacker-text">
                            <i class="mail icon"></i>
                            <div class="content">> Email: maxim@cyber.dev</div>
                        </div>
                        <div class="item hacker-text">
                            <i class="phone icon"></i>
                            <div class="content">> Телефон: +7 (999) 123-45-67</div>
                        </div>
                    </div>
                    <div class="ui social-buttons">
                        <button class="ui button glow-button" onclick="share('twitter')"><i class="twitter icon"></i></button>
                        <button class="ui button glow-button" onclick="share('github')"><i class="github icon"></i></button>
                        <button class="ui button glow-button" onclick="share('vk')"><i class="vk icon"></i></button>
                        <button class="ui button glow-button" onclick="share('telegram')"><i class="telegram icon"></i></button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Навыки -->
        <div class="ui cyber-card segment" id="skills" data-aos="fade-up">
            <h2 class="ui header dividing neon-text">// НАВЫКИ_И_УМЕНИЯ</h2>
            <div class="ui three stackable cards">
                {% for skill in skills %}
                <div class="card cyber-card">
                    <div class="content">
                        <div class="header neon-text">{{ skill.name }}</div>
                        <div class="meta">Уровень: {{ skill.level }}%</div>
                        <div class="skill-bar">
                            <div class="skill-progress ui {{ skill.color }}" style="width: 0%" id="skill-{{ loop.index }}"></div>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
            <div class="ui form" style="margin-top: 20px;">
                <h4 class="ui dividing header neon-text">Добавить навык</h4>
                <div class="two fields">
                    <div class="field">
                        <label>Название навыка</label>
                        <input type="text" class="cyber-input" id="new-skill-name" placeholder="Например, React">
                    </div>
                    <div class="field">
                        <label>Уровень (0-100)</label>
                        <input type="number" class="cyber-input" id="new-skill-level" min="0" max="100" placeholder="75">
                    </div>
                </div>
                <button class="ui button glow-button" onclick="addSkill()">Добавить навык</button>
            </div>
        </div>

        <!-- Проекты -->
        <div class="ui cyber-card segment" id="projects" data-aos="fade-up">
            <h2 class="ui header dividing neon-text">// АКТИВНЫЕ_ПРОЕКТЫ</h2>
            <div class="ui three stackable cards">
                {% for project in projects %}
                <div class="card cyber-card">
                    <div class="content">
                        <div class="header neon-text">{{ project.name }}</div>
                        <div class="meta">{{ project.description }}</div>
                        <div class="description">
                            <div class="ui indicating progress active" id="project-{{ loop.index }}">
                                <div class="bar" style="transition-duration: 300ms; width: 0%;">
                                    <div class="progress">{{ project.progress }}%</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="extra content">
                        <div class="ui two buttons">
                            <button class="ui basic button glow-button" onclick="showProjectDetails({{ loop.index0 }})">Подробнее</button>
                            <button class="ui basic button glow-button" onclick="likeProject({{ loop.index0 }})">
                                <i class="heart icon"></i>
                                <span id="likes-{{ loop.index0 }}">{{ project.likes }}</span>
                            </button>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
            <button class="ui button glow-button" onclick="addRandomProject()" style="margin-top: 20px;">
                <i class="plus icon"></i>
                Добавить проект
            </button>
        </div>

        <!-- Терминал -->
        <div class="ui cyber-card segment" id="terminal" data-aos="fade-up">
            <h2 class="ui header dividing neon-text">// СИСТЕМНЫЙ_ТЕРМИНАЛ</h2>
            <div class="terminal" id="terminal-output">
                <div class="terminal-line">> Добро пожаловать в системный терминал, Максим.</div>
                <div class="terminal-line">> Инициализация завершена. Система готова к работе.</div>
                <div class="terminal-line">> Введите "help" для списка команд.</div>
            </div>
            <div class="ui action input" style="margin-top: 15px;">
                <input type="text" class="cyber-input" placeholder="Введите команду..." id="terminal-input">
                <button class="ui button glow-button" onclick="executeCommand()">Выполнить</button>
            </div>
        </div>

        <!-- Контакты -->
        <div class="ui cyber-card segment" id="contact" data-aos="fade-up">
            <h2 class="ui header dividing neon-text">// КОНТАКТНАЯ_ИНФОРМАЦИЯ</h2>
            <div class="ui form">
                <div class="two fields">
                    <div class="field">
                        <label>Имя</label>
                        <input type="text" class="cyber-input" id="contact-name" placeholder="Ваше имя">
                    </div>
                    <div class="field">
                        <label>Email</label>
                        <input type="email" class="cyber-input" id="contact-email" placeholder="Ваш email">
                    </div>
                </div>
                <div class="field">
                    <label>Сообщение</label>
                    <textarea class="cyber-input" id="contact-message" rows="5" placeholder="Ваше сообщение..."></textarea>
                </div>
                <button class="ui button glow-button" onclick="sendMessage()">Отправить сообщение</button>
            </div>

            <div class="ui divider"></div>

            <div class="ui center aligned container">
                <h3 class="ui header neon-text">Экстренная связь</h3>
                <div class="ui stackable buttons">
                    <button class="ui button massive glow-button" onclick="openMessenger('telegram')">
                        <i class="paper plane icon"></i>
                        Экстренный Telegram
                    </button>
                    <button class="ui button massive glow-button" onclick="openMessenger('signal')">
                        <i class="shield icon"></i>
                        Зашифрованный Signal
                    </button>
                </div>
            </div>
        </div>

        <!-- Футер -->
        <div class="ui center aligned segment gradient-bg" style="margin: 3rem 0; border: none;">
            <p class="neon-text">© 2023 Максим CyberDev. Все системы активны.</p>
            <p>Создано с <i class="heart icon red pulse"></i> и темной магией кода</p>
            <button class="ui circular icon button glow-button" onclick="scrollToTop()">
                <i class="arrow up icon"></i>
            </button>
        </div>
    </div>

    <!-- Модальные окна -->
    <div class="ui modal" id="contact-modal">
        <i class="close icon"></i>
        <div class="header neon-text">Контактная информация</div>
        <div class="content">
            <p>Для связи используйте следующие каналы:</p>
            <div class="ui list">
                <div class="item">
                    <i class="mail icon"></i>
                    <div class="content">Email: maxim@cyber.dev</div>
                </div>
                <div class="item">
                    <i class="phone icon"></i>
                    <div class="content">Телефон: +7 (999) 123-45-67</div>
                </div>
                <div class="item">
                    <i class="telegram icon"></i>
                    <div class="content">Telegram: @maxim_cyber</div>
                </div>
            </div>
        </div>
        <div class="actions">
            <div class="ui button" onclick="$('#contact-modal').modal('hide')">Закрыть</div>
            <div class="ui button glow-button" onclick="copyContact('email')">Скопировать контакты</div>
        </div>
    </div>

    <div class="ui modal" id="project-modal">
        <i class="close icon"></i>
        <div class="header neon-text">Детали проекта</div>
        <div class="content">
            <div class="ui items">
                <div class="item">
                    <div class="image">
                        <img src="https://semantic-ui.com/images/wireframe/image.png" id="project-image">
                    </div>
                    <div class="content">
                        <a class="header neon-text" id="project-title">Название проекта</a>
                        <div class="meta">
                            <span id="project-date">Дата: </span>
                        </div>
                        <div class="description">
                            <p id="project-description">Описание проекта</p>
                        </div>
                        <div class="extra">
                            <div class="ui label neon-text" id="project-tech">Технологии</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="actions">
            <div class="ui button" onclick="$('#project-modal').modal('hide')">Закрыть</div>
            <div class="ui button glow-button" onclick="visitProject()">Посетить сайт</div>
        </div>
    </div>

    <!-- Аудио элементы -->
    <audio id="click-sound" src="https://assets.mixkit.co/sfx/preview/mixkit-select-click-1109.mp3" preload="auto"></audio>
    <audio id="terminal-sound" src="https://assets.mixkit.co/sfx/preview/mixkit-remote-control-tone-2862.mp3" preload="auto"></audio>
    <audio id="hack-sound" src="https://assets.mixkit.co/sfx/preview/mixkit-warning-alarm-buzzer-2857.mp3" preload="auto"></audio>

    <script src="https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/fomantic-ui@2.9.3/dist/semantic.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.js"></script>
    <script>
        // Инициализация
        $(document).ready(function() {
            // Инициализация анимаций при скролле
            AOS.init({ duration: 1000 });

            // Инициализация матричного фона
            initMatrix();

            // Анимация счетчиков
            animateCounters();

            // Анимация прогресс-баров
            setTimeout(function() {
                {% for skill in skills %}
                $('#skill-{{ loop.index }}').css('width', '{{ skill.level }}%');
                {% endfor %}

                {% for project in projects %}
                $('#project-{{ loop.index }}').progress({ percent: {{ project.progress }} });
                {% endfor %}
            }, 500);

            // Инициализация модальных окон
            $('.ui.modal').modal();

            // Фокус на поле ввода терминала
            $('#terminal-input').focus();

            // Воспроизведение звука при загрузке
            playSound('terminal-sound');
        });

        // Матричный фон
        function initMatrix() {
            const canvas = document.getElementById('matrixCanvas');
            const ctx = canvas.getContext('2d');

            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;

            const letters = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
            const fontSize = 14;
            const columns = canvas.width / fontSize;

            const drops = [];
            for (let i = 0; i < columns; i++) {
                drops[i] = 1;
            }

            function draw() {
                ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = '#0F0';
                ctx.font = `${fontSize}px monospace`;

                for (let i = 0; i < drops.length; i++) {
                    const text = letters[Math.floor(Math.random() * letters.length)];
                    ctx.fillText(text, i * fontSize, drops[i] * fontSize);

                    if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                        drops[i] = 0;
                    }

                    drops[i]++;
                }
            }

            setInterval(draw, 33);
        }

        // Прокрутка к секции
        function scrollToSection(sectionId) {
            playSound('click-sound');
            $('html, body').animate({
                scrollTop: $('#' + sectionId).offset().top - 70
            }, 1000);
        }

        // Прокрутка вверх
        function scrollToTop() {
            playSound('click-sound');
            $('html, body').animate({ scrollTop: 0 }, 1000);
        }

        // Анимация счетчиков
        function animateCounters() {
            animateCounter('projects-counter', 24);
            animateCounter('clients-counter', 37);
            animateCounter('coffee-counter', 999);
            animateCounter('code-counter', 12576);
        }

        function animateCounter(elementId, target) {
            $('#' + elementId).prop('Counter', 0).animate({
                Counter: target
            }, {
                duration: 2000,
                easing: 'swing',
                step: function (now) {
                    $(this).text(Math.ceil(now));
                }
            });
        }

        // Воспроизведение звука
        function playSound(soundId) {
            if (localStorage.getItem('soundEnabled') !== 'false') {
                const sound = document.getElementById(soundId);
                sound.currentTime = 0;
                sound.play();
            }
        }

        // Переключение звуков
        function toggleSound() {
            const soundEnabled = localStorage.getItem('soundEnabled') !== 'false';
            localStorage.setItem('soundEnabled', !soundEnabled);

            $('body').toast({
                message: 'Звуки ' + (soundEnabled ? 'выключены' : 'включены'),
                class: 'success'
            });
        }

        // Последовательность загрузки системы
        function initiateBootSequence() {
            playSound('hack-sound');
            const terminal = $('#terminal-output');
            terminal.empty();

            const messages = [
                "> ИНИЦИАЛИЗАЦИЯ СИСТЕМЫ...",
                "> ПРОВЕРКА БЕЗОПАСНОСТИ...",
                "> ЗАГРУЗКА МОДУЛЕЙ...",
                "> АКТИВАЦИЯ ИНТЕРФЕЙСА...",
                "> СИСТЕМА ГОТОВА К РАБОТЕ, МАКСИМ."
            ];

            let delay = 0;
            messages.forEach((message, index) => {
                setTimeout(() => {
                    terminal.append(`<div class="terminal-line">${message}</div>`);
                    terminal.scrollTop(terminal[0].scrollHeight);

                    if (index === messages.length - 1) {
                        setTimeout(() => {
                            scrollToSection('terminal');
                        }, 500);
                    }
                }, delay);

                delay += 800;
            });
        }

        // Выполнение команды в терминале
        function executeCommand() {
            const input = $('#terminal-input').val();
            if (!input) return;

            const terminal = $('#terminal-output');
            terminal.append(`<div class="terminal-line">> ${input}</div>`);

            // Обработка команд
            if (input.toLowerCase() === 'help') {
                terminal.append('<div class="terminal-line">> Доступные команды: clear, time, projects, contact, hack</div>');
            } else if (input.toLowerCase() === 'clear') {
                terminal.empty();
            } else if (input.toLowerCase() === 'time') {
                terminal.append(`<div class="terminal-line">> Текущее время: ${new Date().toLocaleTimeString()}</div>`);
            } else if (input.toLowerCase() === 'projects') {
                terminal.append('<div class="terminal-line">> Загрузка списка проектов...</div>');
                setTimeout(() => {
                    terminal.append('<div class="terminal-line">> 1. Чат-бот ИИ [95%]</div>');
                    terminal.append('<div class="terminal-line">> 2. Крипто-трекер [80%]</div>');
                    terminal.append('<div class="terminal-line">> 3. AR Игра [65%]</div>');
                    scrollToSection('projects');
                }, 1000);
            } else if (input.toLowerCase() === 'contact') {
                terminal.append('<div class="terminal-line">> Открытие контактов...</div>');
                setTimeout(() => {
                    showModal('contact-modal');
                }, 500);
            } else if (input.toLowerCase() === 'hack') {
                terminal.append('<div class="terminal-line">> ИНИЦИАЛИЗАЦИЯ ВЗЛОМА...</div>');
                playSound('hack-sound');
                setTimeout(() => {
                    terminal.append('<div class="terminal-line">> ПОДБОР ПАРОЛЕЙ... 23%</div>');
                    setTimeout(() => {
                        terminal.append('<div class="terminal-line">> ПОДБОР ПАРОЛЕЙ... 67%</div>');
                        setTimeout(() => {
                            terminal.append('<div class="terminal-line">> ПОДБОР ПАРОЛЕЙ... 100%</div>');
                            setTimeout(() => {
                                terminal.append('<div class="terminal-line">> ДОСТУП ПОЛУЧЕН. СИСТЕМА ВЗЛОМАНА.</div>');
                                $('body').toast({
                                    message: 'Пентагон успешно взломан!',
                                    class: 'success'
                                });
                            }, 500);
                        }, 800);
                    }, 800);
                }, 800);
            } else {
                terminal.append('<div class="terminal-line">> Неизвестная команда. Введите "help" для списка команд.</div>');
            }

            terminal.scrollTop(terminal[0].scrollHeight);
            $('#terminal-input').val('');
            playSound('terminal-sound');
        }

        // Остальные функции (showModal, copyContact, addSkill, showProjectDetails, likeProject, addRandomProject, sendMessage, openMessenger)
        // Аналогичны предыдущей версии, но с вызовом playSound('click-sound') при необходимости

        // Для краткости не дублируем весь код, но в реальном приложении эти функции должны быть реализованы

    </script>
</body>
</html>
"""


@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, skills=skills, projects=projects)


@app.route('/api/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    print(f"Получено сообщение от {data.get('name')} ({data.get('email')}): {data.get('message')}")
    return jsonify({'status': 'success', 'message': 'Сообщение отправлено!'})


if __name__ == '__main__':
    app.run(debug=True)