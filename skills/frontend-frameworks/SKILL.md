---
name: frontend-frameworks
description: Master modern frontend frameworks including React, Vue, Angular, and Next.js for building interactive, performant web applications.
---

# Frontend Frameworks

## Quick Start

Choose a framework based on your project needs and learn its core concepts.

### Framework Comparison

| Framework | Learning Curve | Ecosystem | Performance | Best For |
|-----------|---------------|-----------|-----------|----|
| React | Medium | Large | Excellent | SPAs, complex UIs |
| Vue | Easy | Growing | Excellent | Quick development, small teams |
| Angular | Steep | Large | Good | Enterprise, large apps |
| Next.js | Medium | Growing | Excellent | Full-stack, SSR/SSG |

## React

### Core Concepts

**Components**
```jsx
function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

**Hooks**
- useState: State management in functional components
- useEffect: Side effects and lifecycle
- useContext: Context consumption
- useReducer: Complex state logic
- Custom hooks: Reusable stateful logic

**State Management**
- Local component state
- Context API for prop drilling solutions
- Redux/Zustand for complex apps
- TanStack Query for server state

## Vue

### Core Concepts

**Composition API**
```javascript
import { ref, onMounted } from 'vue'

export default {
  setup() {
    const count = ref(0)
    onMounted(() => console.log('mounted'))
    return { count }
  }
}
```

**Reactivity System**
- Automatic dependency tracking
- Computed properties
- Watchers
- Watchers vs effects

**Template Features**
- v-if, v-show, v-for directives
- Two-way binding (v-model)
- Event handling (@click)
- Dynamic classes and styles

## Angular

### Core Concepts

**Decorators & Dependency Injection**
```typescript
@Component({
  selector: 'app-example',
  template: '<div>{{ title }}</div>'
})
export class ExampleComponent {
  constructor(private service: MyService) {}
}
```

**RxJS & Observables**
- Stream-based programming
- Operators: map, filter, switchMap
- Subject types: Subject, BehaviorSubject, ReplaySubject

**Module System**
- Feature modules
- Lazy loading
- HTTP client module

## Next.js

### Key Features

**Pages & Routing**
- File-based routing
- Dynamic routes: [id].js
- API routes: pages/api/

**Data Fetching**
```javascript
export async function getStaticProps() {
  return { props: { data } }
}

export async function getServerSideProps() {
  return { props: { data } }
}
```

**Performance Optimizations**
- Image optimization (next/image)
- Automatic code splitting
- Font optimization
- Script optimization

## Common Patterns

### Component Architecture

**Smart vs Presentational**
- Smart components: Logic, state management
- Presentational components: Pure render functions

**Composition over Inheritance**
- Favor component composition
- Render props pattern
- Custom hooks pattern

### Performance Optimization

**Code Splitting**
- Dynamic imports
- Route-based splitting
- Component lazy loading

**Memoization**
- React.memo for pure components
- useMemo for expensive calculations
- useCallback for stable function references

**Virtualization**
- Render only visible list items
- react-window, react-virtualized libraries

## Testing

**Unit Testing**
- Jest + React Testing Library
- Testing user interactions, not implementation

**E2E Testing**
- Cypress, Playwright
- Full application workflows

## Roadmaps Covered

- React (https://roadmap.sh/react)
- Vue (https://roadmap.sh/vue)
- Angular (https://roadmap.sh/angular)
- Next.js (https://roadmap.sh/nextjs)
- Frontend (https://roadmap.sh/frontend)
