# Contributing to Spot

Thank you for your interest in contributing to Spot! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and add your Spotify API credentials
5. Make your changes
6. Test your changes thoroughly

## Development Guidelines

### Code Style
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and modular

### Testing
- Test your changes with different playlist types (public/private)
- Verify downloads work correctly
- Check that file naming and organization work as expected
- Test the car audio optimization feature

### Commit Messages
- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove, etc.)
- Keep the first line under 50 characters
- Add details in the body if needed

## Pull Request Process

1. Ensure your code follows the project's style guidelines
2. Update documentation if you've made changes to functionality
3. Add or update tests if applicable
4. Update the README.md if you've added new features
5. Submit a pull request with:
   - Clear description of changes
   - Reasoning for the changes
   - Any breaking changes noted

## Issues

When reporting issues:
- Use the issue templates if available
- Provide clear reproduction steps
- Include your environment details (OS, Python version, etc.)
- Include relevant error messages or logs

## Feature Requests

When requesting features:
- Explain the use case
- Describe the proposed solution
- Consider backward compatibility
- Be open to alternative implementations

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

## Questions?

If you have questions about contributing, feel free to:
- Open an issue with the "question" label
- Reach out to the maintainers
- Check existing issues and documentation first

Thank you for contributing to Spot!
