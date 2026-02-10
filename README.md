# Learnix_Bot_Telegram

## 📁 Git Ignore Environment Files

Prevent changes to sensitive environment files from being tracked:

```sh
git update-index --assume-unchanged .env
```

### 🔄 Restore Change Tracking

If you need to track changes again:

```sh
git update-index --no-assume-unchanged .env
```

## 🗄️ Database Migrations

This project uses Alembic for database migrations. Here are the available migration commands:

### Apply Migrations

Apply all pending migrations to the database:

```sh
py .\src\migrate.py upgrade
```

Apply migrations up to a specific revision:

```sh
py .\src\migrate.py upgrade <revision>
```

Example:
```sh
py .\src\migrate.py upgrade head
```

### Rollback Migrations

Rollback to a specific revision:

```sh
py .\src\migrate.py downgrade <revision>
```

Example (rollback one migration):
```sh
py .\src\migrate.py downgrade -1
```

### Create New Migration

Generate a new migration file (autogenerate):

```sh
py .\src\migrate.py revision -m "migration message"
```

Example:
```sh
py .\src\migrate.py revision -m "add user table"
```

### Check Current Version

Display the current database migration version:

```sh
py .\src\migrate.py current
```

### View Migration History

Show all applied migrations:

```sh
py .\src\migrate.py history
```

## ✍️ Authors

- [IPOleksenko](https://github.com/IPOleksenko) (Owner)

## 📜 License

This project is licensed under the [MIT License](./LICENSE).
