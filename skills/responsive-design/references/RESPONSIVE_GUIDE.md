# Responsive Design Guide

## Mobile-First Approach

```css
/* Base: Mobile */
.container { padding: 1rem; }

/* Tablet and up */
@media (min-width: 768px) {
  .container { padding: 2rem; }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .container { max-width: 1200px; }
}
```

## Flexible Units

| Unit | Use Case |
|------|----------|
| rem | Typography, spacing |
| em | Component-relative |
| % | Fluid widths |
| vw/vh | Viewport-relative |
| clamp() | Fluid typography |

## Grid Patterns

```css
/* Auto-fit grid */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}
```

## Image Optimization

```html
<img
  srcset="small.jpg 480w, medium.jpg 768w, large.jpg 1200w"
  sizes="(max-width: 600px) 100vw, 50vw"
  src="medium.jpg"
  loading="lazy"
/>
```
