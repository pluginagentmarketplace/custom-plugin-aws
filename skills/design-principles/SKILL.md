---
name: design-principles
description: Master SOLID principles, design patterns, and software design best practices for building maintainable systems.
---

# Software Design Principles & Patterns

## SOLID Principles

### Single Responsibility Principle (SRP)

**One reason to change**
```python
# Bad: Multiple responsibilities
class User:
    def save(self): pass
    def send_email(self): pass
    def validate(self): pass

# Good: Single responsibility
class User:
    def __init__(self, name, email): pass

class UserRepository:
    def save(self, user): pass

class UserValidator:
    def validate(self, user): pass

class EmailService:
    def send(self, user): pass
```

### Open/Closed Principle (OCP)

**Open for extension, closed for modification**
```python
# Bad: Modify for each new payment type
def process_payment(payment_type, amount):
    if payment_type == 'credit':
        # process credit card
    elif payment_type == 'paypal':
        # process paypal

# Good: Extension through abstraction
class PaymentProcessor:
    def process(self, amount): pass

class CreditCardProcessor(PaymentProcessor):
    def process(self, amount): pass
```

### Liskov Substitution Principle (LSP)

**Subclass should be substitutable for parent**
```python
# Bad: Square breaks rectangle contract
class Rectangle:
    def set_width(self, w): self.width = w
    def set_height(self, h): self.height = h

class Square(Rectangle):
    def set_width(self, w):
        self.width = w
        self.height = w  # Breaks contract!

# Good: Proper inheritance
class Shape:
    def area(self): pass

class Rectangle(Shape):
    def area(self): return self.width * self.height
```

### Interface Segregation Principle (ISP)

**Small, focused interfaces**
```python
# Bad: Fat interface
class Worker:
    def work(self): pass
    def eat(self): pass

# Good: Segregated interfaces
class Employee:
    def work(self): pass

class Eater:
    def eat(self): pass
```

### Dependency Inversion Principle (DIP)

**Depend on abstractions, not concretions**
```python
# Bad: Direct dependency
class UserService:
    def __init__(self):
        self.db = MySQLDatabase()

# Good: Dependency injection
class UserService:
    def __init__(self, database):
        self.db = database  # Can be any database
```

## Design Patterns

### Creational Patterns

**Singleton** - One instance globally
**Factory** - Create objects without specifying classes
**Builder** - Construct complex objects step-by-step
**Prototype** - Clone existing objects

### Structural Patterns

**Adapter** - Make incompatible interfaces compatible
**Decorator** - Add behavior dynamically
**Facade** - Simplify complex subsystems
**Proxy** - Control access to another object

### Behavioral Patterns

**Observer** - Notify multiple objects of state change
**Strategy** - Encapsulate algorithm variations
**Command** - Encapsulate request as object
**State** - Change behavior based on state

## DRY Principle

**Don't Repeat Yourself**
- Extract common code
- Create reusable components
- Reduce duplication

## KISS Principle

**Keep It Simple, Stupid**
- Simplest solution first
- Avoid over-engineering
- Clear is better than clever

## YAGNI Principle

**You Aren't Gonna Need It**
- Don't build unused features
- Focus on requirements
- Refactor when needed

## Architecture Patterns

**Layered Architecture** - Layers for different concerns
**Hexagonal Architecture** - Core logic isolated
**Clean Architecture** - Dependencies point inward
**Event-Driven** - Asynchronous event handling

## Roadmaps Covered

- Software Design (https://roadmap.sh/software-design-architecture)
- Code Review (https://roadmap.sh/code-review)
