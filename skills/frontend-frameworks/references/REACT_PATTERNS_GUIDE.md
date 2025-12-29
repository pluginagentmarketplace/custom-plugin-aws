# React Patterns Guide

## Component Patterns

### Composition
```tsx
<Card>
  <Card.Header>Title</Card.Header>
  <Card.Body>Content</Card.Body>
</Card>
```

### Custom Hooks
```tsx
function useAsync<T>(fn: () => Promise<T>) {
  const [state, setState] = useState<{data?: T; loading: boolean; error?: Error}>();
  useEffect(() => { fn().then(data => setState({data, loading: false})); }, []);
  return state;
}
```

## State Management

| Solution | Use Case | Complexity |
|----------|----------|------------|
| useState | Local state | Low |
| useReducer | Complex local | Medium |
| Context | Prop drilling | Medium |
| Zustand | Global state | Low |
| TanStack Query | Server state | Medium |

## Performance

1. **React.memo** - Prevent re-renders
2. **useMemo** - Cache calculations
3. **useCallback** - Stable callbacks
4. **Code splitting** - lazy() + Suspense
