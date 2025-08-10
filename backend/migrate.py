#!/usr/bin/env python3
"""
Утилита для управления миграциями Alembic в проекте InvestV2

Использование:
    python migrate.py status      # Показать текущий статус
    python migrate.py upgrade     # Применить все миграции
    python migrate.py downgrade   # Откатить одну миграцию
    python migrate.py create "Описание"  # Создать новую миграцию
"""

import sys
import subprocess
from pathlib import Path


def run_alembic_command(command: list[str]) -> int:
    """Запускает команду Alembic из директории migrations"""
    try:
        # Переходим в директорию migrations
        migrations_dir = Path(__file__).parent / "migrations"
        if not migrations_dir.exists():
            print("❌ Директория migrations не найдена")
            return 1
            
        # Запускаем команду из директории migrations
        result = subprocess.run(
            ['alembic'] + command, 
            cwd=migrations_dir,
            check=False
        )
        return result.returncode
    except FileNotFoundError:
        print("❌ Alembic не найден. Убедитесь, что виртуальное окружение активировано.")
        print("💡 Запустите: source venv/bin/activate")
        return 1


def show_status():
    """Показывает текущий статус миграций"""
    print("📊 Текущий статус миграций:")
    print("-" * 40)
    run_alembic_command(['current'])
    print()
    print("📜 История миграций:")
    print("-" * 40)
    run_alembic_command(['history', '--verbose'])


def upgrade_migrations():
    """Применяет все миграции"""
    print("⬆️ Применение миграций...")
    return run_alembic_command(['upgrade', 'head'])


def downgrade_migrations():
    """Откатывает одну миграцию"""
    print("⬇️ Откат миграций...")
    return run_alembic_command(['downgrade', '-1'])


def create_migration(message: str):
    """Создает новую миграцию"""
    print(f"📝 Создание миграции: {message}")
    return run_alembic_command(['revision', '--autogenerate', '-m', message])


def show_help():
    """Показывает справку"""
    print(__doc__)


def main():
    """Главная функция"""
    if len(sys.argv) < 2:
        show_help()
        return 1

    command = sys.argv[1].lower()

    if command == 'status':
        show_status()
    elif command == 'upgrade':
        return upgrade_migrations()
    elif command == 'downgrade':
        return downgrade_migrations()
    elif command == 'create':
        if len(sys.argv) < 3:
            print("❌ Необходимо указать описание миграции")
            print("💡 Пример: python migrate.py create 'Add new field'")
            return 1
        message = sys.argv[2]
        return create_migration(message)
    elif command in ['help', '--help', '-h']:
        show_help()
    else:
        print(f"❌ Неизвестная команда: {command}")
        show_help()
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
