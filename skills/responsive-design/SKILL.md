---
name: responsive-design
description: Master HTML, CSS, responsive design, and accessibility to create beautiful, inclusive user interfaces that work across all devices.
---

# Responsive Design & HTML/CSS

## Quick Start

Build beautiful, accessible interfaces with semantic HTML and modern CSS.

## HTML Fundamentals

### Semantic HTML

```html
<!-- Good: Semantic markup -->
<header>
  <nav>Navigation</nav>
</header>
<main>
  <article>
    <h1>Article Title</h1>
    <section>Content</section>
  </article>
</main>
<footer>Footer content</footer>
```

### Accessibility (a11y)

**ARIA Attributes**
- aria-label: Alternative text
- aria-describedby: Description reference
- aria-live: Dynamic content announcements
- aria-hidden: Hide from accessibility tree

**Semantic Elements**
- Use `<button>` not `<div onclick>`
- Use `<nav>`, `<main>`, `<footer>`
- Proper heading hierarchy: h1 > h2 > h3

**WCAG 2.1 Levels**
- Level A: Basic accessibility
- Level AA: Enhanced accessibility (recommended)
- Level AAA: Advanced accessibility

## CSS Fundamentals

### The Cascade, Specificity & Inheritance

**Specificity Calculation**
- Inline styles: 1000
- IDs: 100
- Classes, pseudo-classes, attributes: 10
- Elements: 1

**Inheritance**
- Some properties inherit by default (color, font)
- Some don't (padding, margin, border)
- Use `inherit` and `initial` keywords

### Modern CSS Layout

**Flexbox (1D Layout)**
```css
.container {
  display: flex;
  justify-content: space-between;  /* Horizontal alignment */
  align-items: center;              /* Vertical alignment */
  gap: 1rem;
}

.item {
  flex: 1;  /* Grow equally */
}
```

**CSS Grid (2D Layout)**
```css
.grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 1rem;
}

.card {
  grid-column: span 4;
}
```

### Responsive Design Patterns

**Mobile-First Approach**
```css
/* Base styles for mobile */
.container { width: 100%; }

/* Tablet and up */
@media (min-width: 768px) {
  .container { width: 750px; }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .container { width: 960px; }
}
```

**Flexible Units**
- rem: Relative to root font size
- em: Relative to parent font size
- vw/vh: Viewport width/height
- percentages: Relative to parent

## Advanced CSS

### CSS Variables (Custom Properties)

```css
:root {
  --primary-color: #3498db;
  --spacing: 1rem;
}

.button {
  background: var(--primary-color);
  padding: var(--spacing);
}
```

### CSS-in-JS Solutions

- Styled Components
- CSS Modules
- Emotion
- Tailwind CSS

### Animations & Transitions

```css
.button {
  transition: background-color 0.3s ease;
}

.button:hover {
  background-color: #2980b9;
}

@keyframes slideIn {
  from { transform: translateX(-100%); }
  to { transform: translateX(0); }
}

.modal {
  animation: slideIn 0.3s ease;
}
```

## Performance Optimization

### Critical Rendering Path

1. Parse HTML (create DOM)
2. Parse CSS (create CSSOM)
3. Combine into render tree
4. Layout (calculate positions)
5. Paint (draw pixels)
6. Composite (layer composition)

### Performance Tips

**Reduce Repaints & Reflows**
- Batch DOM updates
- Use transform and opacity (GPU accelerated)
- Avoid expensive CSS selectors

**Font Optimization**
- Font subsetting
- Variable fonts
- Font loading strategies (FOUT, FOIT)

**Image Optimization**
- Responsive images with srcset
- Modern formats (WebP, AVIF)
- Lazy loading with loading="lazy"

## Design Systems & Components

### Component Library Structure

- Atoms: Buttons, inputs, labels
- Molecules: Form groups, cards, search bars
- Organisms: Headers, footers, navigation
- Templates: Page layouts
- Pages: Real content

### Spacing, Typography, Colors

- Define spacing scale (8px, 16px, 24px, etc.)
- Limit font families (2-3 max)
- Establish color palette with shades
- Use CSS variables for consistency

## Accessibility Checklist

- ✅ Semantic HTML
- ✅ Keyboard navigation
- ✅ Color contrast (4.5:1 for text)
- ✅ Alt text for images
- ✅ Form labels and ARIA
- ✅ Focus indicators
- ✅ Skip navigation links
- ✅ Responsive text scaling

## Roadmaps Covered

- HTML (https://roadmap.sh/html)
- CSS (https://roadmap.sh/css)
- Responsive Design (part of frontend)
- UX Design (https://roadmap.sh/ux-design)
