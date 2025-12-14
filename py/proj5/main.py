import argparse
from main_window import *

def main():
    parser = argparse.ArgumentParser(description="выводит графический интерфейс с изображениями из файла аннотации")
    parser.add_argument("annotation_name", type=str, help="абсолютный путь до файла аннотации csv")

    try:
        args = parser.parse_args()

        # Проверяем существование файла аннотации
        if not os.path.exists(args.annotation_name):
            raise FileNotFoundError(f"Файл аннотации не найден: {args.annotation_name}")

        # Проверяем, что файл имеет расширение .csv
        if not args.annotation_name.lower().endswith('.csv'):
            raise ValueError(f"Файл должен иметь расширение .csv: {args.annotation_name}")

        annotation_check(args.annotation_name)

        app = QApplication(sys.argv)
        widget = MyWidget(args.annotation_name)
        widget.resize(800, 600)
        widget.show()

        sys.exit(app.exec_())

    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
        print("Убедитесь, что указан правильный путь к файлу аннотации.")
        sys.exit(1)

    except ValueError as e:
        print(f"Ошибка: {e}")
        print("Файл аннотации должен быть в формате CSV.")
        sys.exit(1)

    except PermissionError as e:
        print(f"Ошибка доступа: {e}")
        print("Убедитесь, что у вас есть права на чтение файла аннотации.")
        sys.exit(1)

    except Exception as e:
        print(f"Неизвестная ошибка: {type(e).__name__}: {e}")
        print("Попробуйте проверить корректность данных в файле аннотации.")
        sys.exit(1)

if __name__ == '__main__':
    main()
