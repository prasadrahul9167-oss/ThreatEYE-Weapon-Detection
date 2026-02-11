# ThreatEYE - Contributing Guide

Thank you for considering contributing to ThreatEYE! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported
2. Create a detailed bug report including:
   - Description of the issue
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, Node version)
   - Screenshots if applicable

### Suggesting Enhancements

1. Check existing enhancement requests
2. Clearly describe the enhancement
3. Explain why it would be useful
4. Provide examples if possible

### Code Contributions

#### Development Setup

1. Fork the repository
2. Clone your fork
3. Create a feature branch: `git checkout -b feature-name`
4. Make your changes
5. Test thoroughly
6. Commit with clear messages
7. Push to your fork
8. Create a pull request

#### Code Style

**Python (Backend)**
- Follow PEP 8 style guide
- Use type hints where applicable
- Add docstrings to functions
- Keep functions focused and small

**JavaScript/React (Frontend)**
- Use functional components with hooks
- Follow React best practices
- Use meaningful variable names
- Add comments for complex logic

**Commit Messages**
- Use present tense ("Add feature" not "Added feature")
- Be descriptive but concise
- Reference issue numbers when applicable

#### Testing

- Add tests for new features
- Ensure existing tests pass
- Test on multiple browsers (for frontend changes)
- Verify performance impact

### Pull Request Process

1. Update documentation if needed
2. Add yourself to CONTRIBUTORS.md
3. Ensure CI/CD checks pass
4. Request review from maintainers
5. Address review feedback

## Development Guidelines

### Backend Development

- Use async/await for database operations
- Validate input data with Pydantic
- Handle errors gracefully
- Log important events
- Optimize for performance

### Frontend Development

- Keep components focused and reusable
- Use custom hooks for shared logic
- Optimize re-renders
- Ensure responsive design
- Follow accessibility guidelines

### AI Model Improvements

- Document model changes thoroughly
- Compare performance metrics
- Test with various datasets
- Consider CPU/GPU requirements
- Maintain backward compatibility

## Feature Roadmap

See CHANGELOG.md for planned features. Feel free to pick up any item or suggest new ones!

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what's best for the project
- Welcome newcomers

## Questions?

Feel free to open an issue for questions or discussions.

---

Thank you for contributing to ThreatEYE! 🎯