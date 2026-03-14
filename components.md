# Yango Tech — Component Library Reference

This document contains detailed patterns for each reusable component.
All CSS classes referenced here are defined in `boilerplate.css`.

---

## 1. Navigation

The nav is fixed to the top of the viewport with a gradient fade overlay.

### HTML Structure

```html
<nav class="yt-nav" id="nav">
  <div class="yt-nav__inner">
    <a href="/" class="yt-nav__logo">
      <img src="https://avatars.mds.yandex.net/get-lpc/14837328/21641dca-3288-4eeb-8d99-81f8cb31a763/orig"
           alt="Yango Tech" width="176" height="30">
    </a>
    <ul class="yt-nav__links">
      <li><a class="yt-nav__link" href="#section">LINK</a></li>
      <li><a class="yt-btn yt-btn--dark" href="#contact">TALK TO AN EXPERT</a></li>
    </ul>
  </div>
</nav>
```

### Behavior

- **Default state (hero visible):** Dark gradient overlay fading from semi-black at top to transparent. White text, white logo.
- **Scrolled past hero:** Add `.yt-nav--dark` class. This switches the gradient to white, inverts the logo, and changes link colors to dark. Implement via JS `IntersectionObserver` or scroll listener.
- **Hover on links:** Non-hovered links fade to `opacity: 0.4`. This is handled by the CSS rule `.yt-nav__links:hover .yt-nav__link:not(:hover)`.
- **CTA button:** Always present as the rightmost nav item. Uses `.yt-btn--dark` (dark bg, hover to red).

### Dropdown Menus (for multi-page sites)

For sites with dropdown menus (like Industries / Products on tech.yango.com):

```html
<li class="yt-nav__dropdown-trigger">
  <a class="yt-nav__link" href="#">Industries</a>
  <div class="yt-nav__dropdown">
    <div class="yt-nav__dropdown-inner">
      <a href="/retail" class="yt-nav__dropdown-item">
        <span class="yt-label">Retail & E-Commerce</span>
        <p class="yt-body yt-text-secondary">Digital commerce solutions</p>
      </a>
      <!-- more items -->
    </div>
  </div>
</li>
```

Dropdown CSS:

```css
.yt-nav__dropdown {
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  width: 56rem;
  max-width: calc(100vw - 2 * var(--yt-padding));
  background: var(--dropdown-bg);
  border-radius: var(--radius-dropdown);
  padding: 1.25rem;
  opacity: 0;
  pointer-events: none;
  transition: var(--transition-fast);
}

.yt-nav__dropdown-trigger:hover .yt-nav__dropdown {
  opacity: 1;
  pointer-events: auto;
}

.yt-nav__dropdown-item {
  display: block;
  padding: 1.4rem 1rem;
  border-bottom: 1px solid var(--border-color);
  text-decoration: none;
}

.yt-nav__dropdown-item:last-child {
  border-bottom: none;
}
```

---

## 2. Hero Section

Full-viewport height, dark background, white text.

### Variants

**A) Video background** (like tech.yango.com homepage):
```html
<section class="yt-hero">
  <div class="yt-hero__bg">
    <video autoplay muted loop playsinline>
      <source src="hero.mp4" type="video/mp4">
    </video>
  </div>
  <div class="yt-hero__content yt-container">
    <h1 class="yt-h1">Empower businesses<br>with global technologies</h1>
    <p class="yt-body" style="margin-top:2rem; opacity:0.7;">Subtitle text here</p>
    <a href="#" class="yt-btn yt-btn--primary" style="margin-top:3rem;">Talk to an expert</a>
  </div>
</section>
```

**B) CSS animation background** (red swirl on black):
```css
.yt-hero__bg-animated {
  width: 100%;
  height: 100%;
  background:
    radial-gradient(ellipse at 25% 50%, rgba(255,26,26,0.2) 0%, transparent 50%),
    radial-gradient(ellipse at 75% 30%, rgba(255,26,26,0.1) 0%, transparent 50%),
    #000;
}
```

**C) Static image background:**
```html
<div class="yt-hero__bg">
  <img src="hero.jpg" alt="" style="object-fit:cover; width:100%; height:100%;">
  <div style="position:absolute; inset:0; background:rgba(0,0,0,0.5);"></div>
</div>
```

### Rules
- Headline max-width: `50rem` (prevents ultra-wide unreadable lines)
- Subtitle: sentence case, `opacity: 0.6`, `letter-spacing: 0.05em` for softer secondary text
- CTA button: always `.yt-btn--primary` (red), text uppercase
- Include `padding-top: 6rem` to clear the fixed nav

---

## 3. Cards

### Industry Card (image + overlaid tags)

```html
<div class="yt-card">
  <div class="yt-card__image-wrap">
    <img src="industry.jpg" alt="Retail" loading="lazy">
    <div class="yt-card__tags">
      <span class="yt-card__tag">E-Commerce</span>
      <span class="yt-card__tag">Logistics</span>
    </div>
  </div>
  <div class="yt-card__body">
    <h3 class="yt-h3">Retail & E-Commerce</h3>
    <p class="yt-body yt-text-secondary" style="margin-top:1rem;">
      End-to-end digital commerce infrastructure
    </p>
  </div>
</div>
```

### Product Card (hover reveals background)

```css
.yt-product-card {
  position: relative;
  background: white;
  border-radius: var(--radius-card);
  overflow: hidden;
  padding: 2.5rem;
  min-height: 24rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.yt-product-card__bg {
  position: absolute;
  inset: 0;
  opacity: 0;
  transition: opacity var(--transition-card);
  z-index: 0;
}

.yt-product-card__bg img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: scale(1.1);
  transition: transform var(--transition-card);
}

.yt-product-card:hover .yt-product-card__bg {
  opacity: 1;
}

.yt-product-card:hover .yt-product-card__bg img {
  transform: scale(1.3);
}

.yt-product-card__content {
  position: relative;
  z-index: 1;
}
```

### Stat Card (simple number + label)

```html
<div class="yt-card" style="padding: 2.5rem; text-align: center;">
  <p class="yt-h2" style="color: var(--primary-color);">35+</p>
  <p class="yt-label yt-text-secondary" style="margin-top: 0.75rem;">Markets worldwide</p>
</div>
```

### Rules for all cards
- NEVER use `box-shadow` — rely on white-on-`#F5F5F5` contrast
- Always use `border-radius: var(--radius-card)` (1.875rem)
- Image hover: `transform: scale(1.1)` with `transition: var(--transition-image)` (1.2s)
- Tag pills: glassmorphic (`backdrop-filter: blur(5px)`, semi-transparent bg)

---

## 4. Buttons / CTAs

### Variants

| Class               | Background         | Text Color | Hover Background   | Use Case              |
|---------------------|--------------------|------------|--------------------|-----------------------|
| `.yt-btn--primary`  | `#FF1A1A`          | White      | `#141414` (dark)   | Main CTAs             |
| `.yt-btn--dark`     | `#232323`          | White      | `#FF1A1A` (red)    | Nav CTA, secondary    |
| `.yt-btn--outline`  | Transparent        | Dark/White | Red border + text  | Tertiary / ghost      |

### Button sizing
- Default padding: `1rem 2rem`
- Large (hero): `1.25rem 2.5rem`
- Small (inline): `0.75rem 1.5rem`

### Rules
- All buttons: `border-radius: var(--radius-btn)` (2rem) — always pill-shaped
- Text: `uppercase`, `letter-spacing: 0.15em`, `font-weight: 500`
- Transitions: `var(--transition-fast)` (0.2s ease-in-out)
- Never use icons inside primary CTAs on tech.yango.com — text only

---

## 5. Forms

### Standard Contact Form

```html
<div style="display: flex; flex-direction: column; gap: 1.5rem; max-width: 48rem;">
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
    <input class="yt-input" type="text" placeholder="Name">
    <input class="yt-input" type="email" placeholder="Email">
  </div>
  <input class="yt-input" type="text" placeholder="Company">
  <select class="yt-input">
    <option value="" disabled selected>Industry</option>
    <option>Retail & E-Commerce</option>
    <option>Financial Services</option>
    <option>Government</option>
    <option>Logistics</option>
    <option>Telecom</option>
  </select>
  <textarea class="yt-input" placeholder="Message"></textarea>
  <button class="yt-btn yt-btn--primary">SUBMIT</button>
</div>
```

### Rules
- Input bg: `var(--input-bg)` — `rgb(226,226,226)`
- Radius: `var(--radius-input)` — `1.25rem`
- Padding: `2rem 1.5rem`
- Placeholder text: sentence case, `letter-spacing: 0.04em`, `var(--text-secondary)` color
- Focus: red outline `2px solid var(--primary-color)`
- Submit button: `.yt-btn--primary` (uppercase), hover goes dark

---

## 6. Footer

### Structure

```html
<footer class="yt-footer">
  <div class="yt-container">
    <!-- Top: logo + link columns -->
    <div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:2rem;">
      <a href="/"><img src="[LOGO_URL]" alt="Yango Tech" style="filter:invert(1);" width="176" height="30"></a>
      <div style="display:flex; gap:3.75rem; flex-wrap:wrap;">
        <!-- Column -->
        <div>
          <p class="yt-label" style="margin-bottom:1rem; opacity:0.5;">COLUMN TITLE</p>
          <ul style="list-style:none; display:flex; flex-direction:column; gap:0.75rem;">
            <li><a href="#" class="yt-label--sentence">Link 1</a></li>
            <li><a href="#" class="yt-label--sentence">Link 2</a></li>
          </ul>
        </div>
        <!-- More columns as needed -->
      </div>
    </div>

    <!-- Bottom bar -->
    <div class="yt-footer__bottom">
      <span class="yt-label" style="opacity:0.5;">&copy; 2026 Yango Tech</span>
      <a href="#" class="yt-label">Privacy Policy</a>
    </div>
  </div>
</footer>
```

### Rules
- Background: `#141414` (near-black)
- Logo: inverted (white) with `filter: invert(1)`
- Column titles: `.yt-label` (uppercase, `0.12em`)
- Column link items: `.yt-label--sentence` (sentence case, `0.05em`)
- Link hover: `opacity: 0.5` (no color change)
- Social icons: `background: rgb(31,31,31)`, `border-radius: 1rem`, `padding: 0.75rem`
- Bottom bar: separated by `border-top: 1px solid rgba(255,255,255,0.1)`
- Link gap in bottom bar: `1rem 3.75rem`

---

## 7. Map / Interactive Elements

### Map Markers

```css
.yt-marker {
  position: absolute;
  width: 1rem;
  aspect-ratio: 1;
  background: var(--surface-mid);
  border-radius: 0.2rem;
  translate: -50% -50%;
  cursor: pointer;
}

.yt-marker::before {
  content: "";
  position: absolute;
  width: 300%;
  aspect-ratio: 1;
  background: rgba(50, 50, 50, 0.4);
  left: 50%;
  top: 50%;
  translate: -50% -50%;
  border-radius: inherit;
  transition: var(--transition-fast);
  opacity: 0;
  scale: 0.8;
}

.yt-marker:hover::before,
.yt-marker.active::before {
  opacity: 1;
  scale: 1;
}
```

### Map Tooltips

```html
<div class="yt-tooltip">
  <span class="yt-label">COUNTRY</span>
  <span style="font-size:2rem; letter-spacing:0.05em;">City Name</span>
</div>
```

---

## 8. Scroll Animations

### Fade-in on scroll

Add `.yt-fade-in` to any element, then use the IntersectionObserver from the template:

```html
<div class="yt-fade-in">
  <h2 class="yt-h2">This fades in</h2>
</div>
```

### Staggered reveals

For card grids, add incremental `transition-delay`:

```html
<div class="yt-card yt-fade-in" style="transition-delay: 0s;">...</div>
<div class="yt-card yt-fade-in" style="transition-delay: 0.1s;">...</div>
<div class="yt-card yt-fade-in" style="transition-delay: 0.2s;">...</div>
```

---

## 9. Multi-Page Sites

For multi-page sites, extract the nav and footer into shared HTML partials or use a build tool. Every page should:

1. Include the full `boilerplate.css`
2. Use the same nav with appropriate active states
3. Use the same footer
4. Follow the dark-hero → light-body pattern

### Shared nav active state:

```css
.yt-nav__link--active {
  color: var(--primary-color) !important;
}
```

---

## 10. Interactive Demos / Dashboards

For dashboards and data-heavy demos:

- Use the same font stack and color palette
- Charts: use `#FF1A1A` as primary data color, greys for secondary series
- Tables: no outer border, use `border-bottom: 1px solid var(--border-color)` between rows
- Sidebar nav (if needed): `background: white`, `border-radius: var(--radius-card)`
- Tabs: use `.yt-label` styling with bottom-border active indicator in `var(--primary-color)`
- Data cards: white bg, `border-radius: var(--radius-card)`, no shadow, generous padding `2rem+`

```css
/* Dashboard-specific utilities */
.yt-tab {
  padding: 1rem 1.5rem;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  transition: var(--transition-fast);
}

.yt-tab--active,
.yt-tab:hover {
  border-bottom-color: var(--primary-color);
  color: var(--primary-color);
}

.yt-data-card {
  background: white;
  border-radius: var(--radius-card);
  padding: 2rem;
}

.yt-table {
  width: 100%;
  border-collapse: collapse;
}

.yt-table th,
.yt-table td {
  padding: 1rem 1.5rem;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
  font-size: 0.78rem;
  font-weight: 500;
  letter-spacing: var(--letter-spacing-body);
  text-transform: none;
}

.yt-table th {
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-ui);
  font-size: 0.72rem;
}
```

---

## Summary: Class Reference

| Class                | Purpose                              |
|----------------------|--------------------------------------|
| `.yt-container`      | Max-width centered content wrapper   |
| `.yt-section`        | Standard section with 6rem padding   |
| `.yt-section--tight` | Compact section with 3rem padding    |
| `.yt-grid-2`         | 2-column responsive grid             |
| `.yt-grid-3`         | 3-column responsive grid             |
| `.yt-dark`           | Dark background section              |
| `.yt-light`          | Light (#F5F5F5) background section   |
| `.yt-h1` / `h2` / `h3` | Yango Headline typography         |
| `.yt-body`           | Sentence-case body text (0.05em)     |
| `.yt-label`          | Uppercase UI chrome (0.72rem, 0.12em)|
| `.yt-label--sentence`| Sentence-case label (footer links)   |
| `.yt-text-secondary` | Muted grey text color                |
| `.yt-btn--primary`   | Red CTA button                       |
| `.yt-btn--dark`      | Dark CTA button (nav style)          |
| `.yt-btn--outline`   | Ghost/outline button                 |
| `.yt-card`           | Standard card container              |
| `.yt-card__tag`      | Glassmorphic pill tag                |
| `.yt-input`          | Form input field                     |
| `.yt-nav`            | Fixed navigation bar                 |
| `.yt-hero`           | Full-height hero section             |
| `.yt-footer`         | Page footer                          |
| `.yt-tooltip`        | Map/overlay tooltip                  |
| `.yt-fade-in`        | Scroll-triggered fade animation      |
| `.yt-hover-scale`    | Hover to scale 1.1x                  |
| `.yt-hover-fade`     | Hover to fade 0.5 opacity            |
