# Contributing to ClickCheck Python SDK

Thank you for your interest in contributing to ClickCheck!

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/clickcheck.git
   cd clickcheck
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

4. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   pip install -e .
   ```

## Code Style

- Follow PEP 8
- Use `black` for code formatting: `black clickcheck/`
- Use `flake8` for linting: `flake8 clickcheck/`
- Type hints are encouraged

## Testing

Run tests:
```bash
pytest
```

With coverage:
```bash
pytest --cov=clickcheck --cov-report=html
```

## Submitting Changes

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes and test them
3. Commit with descriptive messages
4. Push to your fork: `git push origin feature/your-feature`
5. Open a Pull Request

## Questions?

Open an issue or contact support@getclickcheck.com

