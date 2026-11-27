---
title: "Швидкий старт Remotion + Claude Code"
description: "15-хвилинний швидкий старт зі створення програмних відео за допомогою Remotion і Claude Code"
tags: [tutorial, workflow, integration]
---

# Швидкий старт Remotion + Claude Code

**Мета**: створити своє перше програмне відео за допомогою Remotion і Claude Code за 15 хвилин.

**Рівень**: початківець у React (достатньо базових знань)

---

## ⚡ Передумови

| Потрібно | Мінімальна версія | Перевірка |
|----------|-------------------|-----------|
| **Node.js** | 18+ | `node --version` |
| **npm** | 8+ | `npm --version` |
| **Claude Code** | 2.1+ | `claude --version` |
| **Основи React** | синтаксис JSX | Знати `<div>`, `props`, `useState` |

**Орієнтовний час**: 15-20 хвилин (перший раз)

---

## 📦 Крок 1: встановлення skills Remotion

### Варіант A: через skills.sh (рекомендовано)

```bash
# Dans un nouveau dossier de projet
mkdir my-remotion-test && cd my-remotion-test

# Installer les skills Remotion pour Claude Code
npx skills add remotion-dev/skills
```

**Очікуваний результат**:
```
✓ Skills added to .claude/skills/
  - remotion-best-practices
  - remotion-animations
  - remotion-audio
  [... 20+ skills installés]
```

### Варіант B: вручну (якщо skills.sh недоступний)

```bash
# Cloner le repo skills directement
git clone https://github.com/remotion-dev/skills.git .claude/skills/remotion
```

---

## 🎬 Крок 2: створення першого проєкту Remotion

### Через Claude Code (рекомендований спосіб)

Запустіть Claude Code і використайте цей промпт:

```
Create a new Remotion project for a simple 5-second video with:
- A fade-in title "Hello Remotion"
- Background gradient (blue to purple)
- Smooth animation

Use npx create-video to scaffold the project.
```

**Що зробить Claude**:
1. Виконає `npx create-video@latest my-video`
2. Згенерує шаблонний код Remotion
3. Створить React-компонент для вашого відео
4. Налаштує `remotion.config.ts`

### Очікуваний результат

```
my-remotion-test/
├── src/
│   ├── Root.tsx           # Entry point
│   ├── HelloWorld.tsx     # Votre composition vidéo
│   └── ...
├── public/
├── package.json
└── remotion.config.ts
```

---

## 🖼️ Крок 3: попередній перегляд відео

### Запуск студії Remotion

```bash
npm start
```

**Результат**: локальний сервер запускається за адресою `http://localhost:3000`

**Інтерфейс студії**:
- Інтерактивна часова шкала (прокручуйте, щоб побачити кадри)
- Живий попередній перегляд вашої композиції
- Елементи керування відтворенням
- Панель props (змінюйте параметри в реальному часі)

### Перевірка змін

У `src/HelloWorld.tsx` змініть текст:

```tsx
<h1 style={{fontSize: 100}}>Hello Remotion!</h1>
```

**Hot reload** → зміна одразу видна в студії.

---

## 📹 Крок 4: рендер відео

### Базова команда

```bash
npm run build
```

**Що відбувається**:
1. Remotion компілює ваш React-код
2. Генерує кожен кадр (30 fps × тривалість = 150 кадрів для 5 с)
3. FFmpeg кодує кадри в MP4
4. Вивід: `out/video.mp4`

### Розширені параметри рендеру

```bash
# Haute qualité (1080p, 60fps)
npx remotion render src/index.ts HelloWorld out/video.mp4 \
  --width 1920 \
  --height 1080 \
  --fps 60

# Format GIF
npx remotion render src/index.ts HelloWorld out/video.gif \
  --image-format png
```

---

## 🤖 Крок 5: ітерації з Claude Code

### Ефективні промпти

**Приклад 1: додати анімацію**
```
Add a smooth scale animation to the title:
- Start at scale 0.8
- End at scale 1.0
- Use spring physics with config {damping: 20}
```

**Приклад 2: додати аудіо**
```
Add background music to the video:
- Use a public domain track from /public/music.mp3
- Fade in over 1 second
- Volume at 0.5
```

**Приклад 3: кілька послідовностей**
```
Create a 3-scene video:
1. Intro (0-2s): Logo fade in
2. Main (2-8s): Product showcase with transitions
3. Outro (8-10s): Call to action text
```

### Ефективний патерн роботи з Claude Code

```
1. Describe what you want (natural language)
   └─ Claude génère le JSX + animations

2. Preview in Studio
   └─ Vérifier visuellement

3. Iterate with specific feedback
   └─ "Make the transition slower"
   └─ "Change color to #FF6B35"

4. Render final video
   └─ npm run build
```

---

## 🐛 Усунення несправностей

### Проблема: "Command not found: remotion"

**Рішення**:
```bash
# Installer globalement
npm install -g @remotion/cli

# Ou utiliser npx
npx remotion --version
```

### Проблема: "React is not defined"

**Рішення**: переконайтеся, що `react` і `react-dom` є в `package.json`:
```bash
npm install react react-dom
```

### Проблема: помилка FFmpeg під час рендеру

**Рішення**: встановіть FFmpeg:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
choco install ffmpeg
```

### Проблема: Claude генерує код, що не компілюється

**Причина**: skills завантажено неправильно.

**Рішення**:
```bash
# Vérifier que .claude/skills/ existe
ls -la .claude/skills/remotion

# Re-sourcer les skills
claude --reload-skills
```

### Проблема: відео відрендерено, але чорний екран

**Налагодження**:
1. Перевірте консоль студії (F12)
2. Пошукайте помилки TypeScript
3. Переконайтеся, що `<Composition>` має правильні props:
   ```tsx
   <Composition
     id="HelloWorld"
     component={HelloWorld}
     durationInFrames={150}  // 5s × 30fps
     fps={30}
     width={1920}
     height={1080}
   />
   ```

---

## 📊 Метрики успіху

Після цього швидкого старту ви маєте мати:

- ✅ Робочий проєкт Remotion (створену структуру)
- ✅ Відрендерене тестове відео (MP4 у `out/`)
- ✅ Розуміння воркфлоу Claude → Preview → Render
- ✅ 1-2 анімації, створені через промпти Claude

**Типовий час рендеру** (відео 5 с, 1080p):
- MacBook Pro M1: ~10-15 секунд
- Intel i5: ~30-45 секунд
- Хмара (GitHub Actions): ~60-90 секунд

---

## 🎯 Наступні кроки

### Середній рівень

1. **Додати ресурси**:
   ```
   Claude, import an image from /public/logo.png and animate it rotating 360°
   ```

2. **Відео на основі даних**:
   ```tsx
   // Générer 100 vidéos à partir d'un dataset
   const data = [{name: "John", score: 95}, ...];
   npx remotion render --props='{"data": data}'
   ```

3. **Складні композиції**:
   ```
   Create a video with 3 scenes using <Sequence>:
   - Scene 1: Intro (0-30 frames)
   - Scene 2: Content (30-150 frames)
   - Scene 3: Outro (150-180 frames)
   ```

### Ресурси

| Ресурс | URL | Тип |
|--------|-----|-----|
| **Remotion Docs** | [remotion.dev/docs](https://www.remotion.dev/docs/) | Офіційна документація |
| **Agent Skills Repo** | [github.com/remotion-dev/skills](https://github.com/remotion-dev/skills) | GitHub |
| **Discord Community** | [remotion.dev/discord](https://www.remotion.dev/discord) | Підтримка спільноти (~1,5 тис. учасників) |
| **Examples Gallery** | [remotion.dev/showcase](https://www.remotion.dev/showcase) | Натхнення |

---

## 💡 Перевірені сценарії використання

| Сценарій | Приклад | Складність |
|----------|---------|------------|
| **Демо продуктів** | Огляд функції з виділеннями | ⭐⭐ |
| **Інтро для YouTube** | Анімований логотип + титрова картка | ⭐ |
| **Візуалізація даних** | Анімовані графіки, інфографіка | ⭐⭐⭐ |
| **Соцмережі** | Instagram stories, шаблони TikTok | ⭐⭐ |
| **Пояснювальні відео** | Анімовані покрокові туторіали | ⭐⭐⭐⭐ |

**Історії успіху**: Icon.me ($5M ARR), Submagic ($8M ARR), Crayo ($500K/міс.)

---

## ⚠️ Важливі обмеження

1. **Потрібні знання React**: Claude допомагає, але розуміння JSX є суттєвим для налагодження
2. **Крива навчання**: перші відео = 2-4 год. Володіння = 2-4 тижні
3. **Витрати**: комерційна ліцензія (>3 осіб) + Claude API + обчислення для рендерингу
4. **Не замінник After Effects**: інша парадигма (код проти часової шкали)

---

## 🎓 Повний приклад сесії

```bash
# 1. Setup
mkdir remotion-demo && cd remotion-demo
npx skills add remotion-dev/skills

# 2. Claude Code prompt
claude

> Create a 10-second countdown timer video:
> - Large numbers (1-10) centered
> - Each number appears for 1 second
> - Use spring animations for each transition
> - Background gradient that changes color per number
> - Add a "beep" sound effect on each number change

# Claude génère le code...

# 3. Preview
npm start
# Ouvrir http://localhost:3000

# 4. Ajustements
> Make the spring animation bouncier (increase damping to 40)
> Change gradient colors to warm tones (orange to red)

# 5. Render final
npm run build

# Résultat: out/video.mp4 (10 secondes, 300 frames)
```

**Загальна тривалість сесії**: ~25 хвилин (з ітераціями)

---

## 📝 Контрольний список перед продакшеном

- [ ] Протестувати повний рендер (а не лише попередній перегляд)
- [ ] Перевірити продуктивність (watch mode проти продакшену)
- [ ] Перевірити ресурси (ліцензії, роздільність, формати)
- [ ] Передбачити витрати на рендеринг (хмара проти локально)
- [ ] Задокументувати динамічні props (для сценаріїв на основі даних)
- [ ] Налаштувати CI/CD, якщо генерація автоматична (GitHub Actions + Remotion Lambda)

---

## 📚 Додаткові ресурси

### 🎯 Топ-3 найважливіших (почніть звідси)

| Ресурс | Тип | URL | Чому |
|--------|-----|-----|------|
| **Official Resources** | Центральний хаб | [remotion.dev/docs/resources](https://www.remotion.dev/docs/resources) | 50+ шаблонів, інтеграцій, ефектів |
| **Fireship Tutorial** | Відео (8 хв) | [This video was made with code](https://www.youtube.com/watch?v=deg8bOoziaE) | Надшвидке вступне відео, 1M+ переглядів |
| **Discord Community** | Жива підтримка | [Remotion Discord](https://discord.com/servers/remotion-809501355504959528) | 5,6 тис.+ учасників, вбудований AI-бот |

### 📖 Рекомендовані письмові туторіали

| Стаття | Рівень | URL | Спеціалізація |
|--------|--------|-----|---------------|
| **ClipCat Beginner's Guide** | Початківець | [Create Videos Programmatically](https://www.clipcat.com/blog/create-videos-programmatically-using-react-a-beginners-guide-to-remotion/) | Покрокове встановлення |
| **Prismic Tutorial** | Початківець | [Learn to Create Videos](https://prismic.io/blog/create-videos-with-code-remotion-tutorial) | Повні основи |
| **SitePoint Introduction** | Середній | [Remotion Tutorial](https://www.sitepoint.com/remotion-create-animated-videos-using-html-css-react/) | Отримання даних, компоненти |

### 🎥 Відеотуторіали за метою

**Швидкий старт** (15 хв):
- [Fireship - This video was made with code](https://www.youtube.com/watch?v=deg8bOoziaE) (8:41, 1M переглядів)

**Поглиблене навчання** (1-2 год):
- [CoderOne - Create Videos with React](https://www.youtube.com/watch?v=VOX98RoITMk) (1 год, повний приклад анімованого логотипа)

**Інтеграція з Claude Code** (30 хв):
- [Snapper AI - Generate Animated Videos](https://www.youtube.com/watch?v=EwKCAgt4aKI) (9:48, січ. 2026)
- [chantastic - Making Remotion Videos](https://www.youtube.com/watch?v=z87bczUZ0uo) (30 хв, січ. 2026)

### 🛠️ Шаблони та приклади

| Шаблон | Призначення | Посилання | Складність |
|--------|-------------|-----------|------------|
| **Hello World** | Перший проєкт | [Official Templates](https://www.remotion.dev/templates/) | ⭐ Просто |
| **Audiogram** | Візуалізація подкасту | [Official Templates](https://www.remotion.dev/templates/) | ⭐⭐ Середньо |
| **GitHub Unwrapped** | Реальний продакшен-кейс | [github.com/remotion-dev/github-unwrapped](https://github.com/remotion-dev/github-unwrapped) | ⭐⭐⭐ Складно |

**Повна сторінка**: [remotion.dev/docs/resources](https://www.remotion.dev/docs/resources) (50+ підтримуваних шаблонів)

### 🏆 Історії успіху (натхнення)

Реальні продукти, що приносять дохід завдяки Remotion:

- **Icon.me**: $5M ARR за 30 днів (конструктор оголошень)
- **Revid.ai**: $1M ARR за 15 місяців (відеоплатформа зі ШІ)
- **Typeframes**: після поглинання (відео-презентації продуктів)

[Переглянути всі showcases](https://www.remotion.dev/showcase)

### 💬 Де ставити запитання

| Платформа | URL | Найкраще для | Активність |
|-----------|-----|--------------|------------|
| **Discord** | [Remotion Discord](https://discord.com/servers/remotion-809501355504959528) | Швидка підтримка, AI-бот | ⭐⭐⭐⭐⭐ Дуже висока |
| **GitHub Discussions** | [remotion-dev/discussions](https://github.com/orgs/remotion-dev/discussions) | Архітектурні запитання | ⭐⭐⭐ Помірна |
| **Stack Overflow** | [тег #remotion](https://stackoverflow.com/questions/tagged/remotion) | Конкретні проблеми | ⭐⭐ Низька |

**Порада**: у Discord позначте бота CrawlChat AI, щоб отримати миттєві відповіді з посиланнями на документацію.

### 🚀 Розширені ресурси

**Продуктивність і оптимізація**:
- [Офіційна документація з продуктивності](https://www.remotion.dev/docs/performance)
- [YouTube: Optimizing Remotion Lambda](https://www.youtube.com/results?search_query=optimizing+remotion+lambda+jonny+burger) (Jonny Burger, 17 хв)

**Agent Skills і ШІ**:
- [Офіційна документація AI Skills](https://www.remotion.dev/docs/ai/skills)
- [Стаття AIbase](https://news.aibase.com/news/24827) (січ. 2026, дуже свіжа)

**Розгортання**:
- [Шаблон Railway](https://railway.com/deploy/remotion-on-rails) (розгортання в 1 клік)
- [Документація Lambda](https://www.remotion.dev/docs/lambda) (безсерверний рендеринг AWS)

### 📊 Корисні пакети

| Пакет | Призначення | Встановлення |
|-------|-------------|--------------|
| `@remotion/shapes` | SVG-фігури (трикутники, зірки) | `npm i @remotion/shapes` |
| `remotion-transition-series` | Переходи між сценами | `npm i remotion-transition-series` |
| `remotion-subtitle` | Автоматичні субтитри | `npm i remotion-subtitle` |
| `@remotion/tailwind` | Інтеграція Tailwind CSS | `npm i @remotion/tailwind` |

[Повний список на сторінці Resources](https://www.remotion.dev/docs/resources)

---

## 🎓 Рекомендований маршрут навчання

### Тиждень 1: основи (6-8 год)
1. Прочитати офіційну документацію (2 год)
2. Подивитися туторіал Fireship (15 хв)
3. Пройти посібник ClipCat: створити Hello World (2 год)
4. Відтворити приклад CoderOne (2-3 год)
5. Приєднатися до Discord, ставити запитання

### Тиждень 2: практика (8-10 год)
1. Створити 3 різні відео (інтро, зворотний відлік, візуалізація даних)
2. Дослідити вихідний код GitHub Unwrapped
3. Протестувати інтеграцію з Claude Code (Agent Skills)
4. Поекспериментувати з пакетами (@remotion/shapes, переходи)

### Тиждень 3: продакшен (постійно)
1. Створити реальний проєкт для конкретного сценарію використання
2. Оптимізувати продуктивність (Lambda за потреби)
3. Налаштувати CI/CD (GitHub Actions)
4. Поділитися в Discord для відгуків

---

**Створено**: 2026-01-23
**Оновлено**: 2026-01-24 (додано ресурси)
**Протестовано з**: Claude Code 2.1.17, Remotion 4.x, Node.js 20.x
**Середня тривалість**: 15-20 хв (перше відео), 5-10 хв (наступні)
**Ресурси перевірено**: 2026-01-24 (Perplexity Pro, 50+ джерел)
