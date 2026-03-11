### CRM Override

A custom app to override the UI in the CRM portal.

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app crm_override https://github.com/lijsamuael/crm_override.git
bench --site <your site name> install-app crm_override
```

### Building the Frontend (Required)

**Important:** Frontend build artifacts are NOT committed to the repository. You must build the frontend after cloning or pulling changes.

```bash
cd $PATH_TO_YOUR_BENCH/apps/crm_override
yarn install
yarn build
```

Then build the Frappe assets:

```bash
cd $PATH_TO_YOUR_BENCH
bench build --app crm_override
```

### After Pulling Changes

Every time you pull changes from the repository, run:

```bash
cd $PATH_TO_YOUR_BENCH/apps/crm_override
yarn build
cd $PATH_TO_YOUR_BENCH
bench build --app crm_override
bench restart  # if on production
```

### Development

For local development with hot-reload:

```bash
cd $PATH_TO_YOUR_BENCH/apps/crm_override
yarn dev
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/crm_override
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
