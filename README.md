## Development

This project has a [dev container](https://containers.dev/) configuration, allowing it to be used in VSCode with the dev container extension or Github Codespaces.
When starting this dev container, all dependencies and tools should be installed and ready for you to use.

To begin developing, open two terminals. In one, start the backend service by executing:
```
pipenv run uvicorn main:app --reload
```

In the other, start the frontend app server by executing:
```
cd frontend && npm run dev
```