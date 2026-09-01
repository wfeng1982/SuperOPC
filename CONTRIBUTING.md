"""Contributing to SuperOPC."""

# Contributing to SuperOPC

We welcome contributions from the community! This guide will help you get started.

## 🤝 Code of Conduct

Please be respectful and constructive in all interactions.

## 🚀 Getting Started

### 1. Fork & Clone

```bash
git clone https://github.com/YOUR_USERNAME/SuperOPC.git
cd SuperOPC
git remote add upstream https://github.com/wfeng1982/SuperOPC.git
```

### 2. Create Feature Branch

```bash
git checkout -b feature/my-feature
# or
git checkout -b fix/my-bug
```

### 3. Setup Development Environment

```bash
uv sync --all-extras
uv run pytest tests/  # Verify tests pass
```

## 📝 Making Changes

### Code Style

- **Format**: `black` (auto-format)
- **Lint**: `ruff` (style & logic)
- **Types**: `mypy` (type checking)
- **Tests**: `pytest` (test framework)

### Before Committing

```bash
# Format code
uv run black superopc/ tests/

# Check lint
uv run ruff check superopc/ tests/ --fix

# Type checking
uv run mypy superopc/

# Run tests
uv run pytest tests/ --cov=superopc
```

## 📚 Types of Contributions

### Bug Fixes

1. Create issue describing the bug
2. Reference issue in PR: `Fixes #123`
3. Add test that reproduces bug
4. Fix bug
5. Verify test passes

### New Features

1. Discuss in GitHub Discussions first
2. Create issue with `[Feature]` tag
3. Create branch: `feature/my-feature`
4. Implement feature with tests
5. Update documentation
6. Submit PR with description

### Documentation

1. Fix typos/clarifications: Direct PR is fine
2. New guides: Discuss first in Discussions
3. Update affected docs when code changes
4. Use clear, concise language

### Skills

1. Create skill in `superopc/skills/<category>/`
2. Inherit from `BaseSkill`
3. Implement `execute()` method
4. Add comprehensive tests
5. Document actions and parameters
6. Submit PR with skill demo

## 🧪 Testing Guidelines

### Write Tests For

- New functions/methods
- Bug fixes
- Edge cases
- Error conditions

### Test File Structure

```python
import pytest
from superopc.module import MyClass

class TestMyClass:
    @pytest.fixture
    def instance(self):
        return MyClass()
    
    def test_basic_functionality(self, instance):
        result = instance.method()
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_async_functionality(self, instance):
        result = await instance.async_method()
        assert result["success"] is True
```

### Run Tests

```bash
# All tests
uv run pytest tests/

# Specific file
uv run pytest tests/test_my_feature.py

# With verbose output
uv run pytest tests/ -v

# With coverage
uv run pytest tests/ --cov=superopc --cov-report=html
```

## 📋 PR Checklist

- [ ] Code passes `black`, `ruff`, `mypy`
- [ ] All tests pass: `pytest tests/`
- [ ] Coverage maintained (>70%)
- [ ] No hardcoded secrets/credentials
- [ ] Logs use `logger` not `print`
- [ ] Documentation updated
- [ ] Commit messages clear and descriptive
- [ ] PR description explains changes
- [ ] Links to related issues/discussions

## 🎯 Priority Areas

We're especially interested in contributions for:

1. **Browser Automation**
   - Playwright/Puppeteer integration
   - DOM snapshot improvements
   - New anti-bot strategies

2. **Skills**
   - eBay automation
   - Shopify integration
   - Marketing skills (social, email)

3. **Infrastructure**
   - PostgreSQL support
   - Kubernetes deployment
   - CLI tools

4. **Documentation**
   - API examples
   - Tutorial content
   - Troubleshooting guides

5. **Testing**
   - Integration tests
   - Performance tests
   - Stress tests

## 🔄 Review Process

1. Submit PR with clear description
2. Automated checks run (tests, lint, coverage)
3. Maintainers review and request changes if needed
4. You address feedback
5. PR approved and merged
6. Your changes published in next release

## 📖 Documentation Guidelines

### Docstrings

```python
def my_function(param1: str, param2: int) -> Dict[str, Any]:
    """Brief description.
    
    Longer description if needed. Explain:
    - What the function does
    - How to use it
    - Important edge cases
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When something is wrong
        RuntimeError: When X happens
    
    Example:
        >>> result = my_function("test", 42)
        >>> print(result)
    """
    pass
```

### Markdown Files

- Use clear headings (H2-H4)
- Include code examples
- Add emojis for visual breaks
- Keep lines under 100 chars
- Link to related docs

## 🎁 Recognition

Contributors are recognized in:
- Git commit history
- GitHub contributors page
- Release notes
- Contributors file

## ❓ Questions?

- **GitHub Discussions**: Ask questions
- **GitHub Issues**: Report bugs
- **Discord/Slack**: Coming soon!

## 📜 License

By contributing, you agree that your contributions will be licensed under Apache 2.0.

Thank you for contributing to SuperOPC! 🙏
