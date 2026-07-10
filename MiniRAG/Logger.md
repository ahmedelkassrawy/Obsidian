```python
def _setup_logging(self) -> logging.Logger:
```
We use the _setup_logging because the ( _ ) means that this is a private method

```python
logger = logging.getLogger(f"agent.{self.agent_name}")
```

```python
logger.setLevel(getattr(logging, settings.LOG_LEVEL))
```
**Details**:
- settings.LOG_LEVEL is likely a string (e.g., "DEBUG", "INFO") defined in a settings module or object.
- getattr(logging, settings.LOG_LEVEL) retrieves the corresponding log level constant from the logging module (e.g., logging.DEBUG, logging.INFO).
- logger.setLevel() configures the minimum severity level for messages the logger will process. For example, if set to logging.DEBUG, the logger processes DEBUG and higher severity messages (INFO, WARNING, ERROR, CRITICAL).
```python
# prevent duplicate handlers:
if logger.handlers:
    return logger
```

#### File Formatter
```python
# create file handler
log_file = settings.LOG_ROOT / f"{self.agent_name}.log"
log_file.parent.mkdir(parents=True, exist_ok=True)
```
- log_file.parent.mkdir(parents=True, exist_ok=True) ensures the parent directory of the log file exists:
        - parents=True creates parent directories if they don’t exist.
        - exist_ok=True prevents errors if the directory already exists.
```python
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)
```
- file_handler.setLevel(logging.DEBUG) sets the handler’s log level to DEBUG, meaning it will handle DEBUG and higher severity messages. This allows detailed logs to be written to the file.
#### Console Handler
```python
# create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
```
Creates and configures a console handler to output logs to the console (e.g., terminal or standard output).
- **Details**:
    - logging.StreamHandler() creates a handler that writes log messages to the console (typically sys.stdout).
    - console_handler.setLevel(logging.INFO) sets the handler’s log level to INFO, meaning it will only handle INFO and higher severity messages (WARNING, ERROR, CRITICAL). This ensures the console shows less verbose output than the file.
```python
# create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

return logger
```