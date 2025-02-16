import subprocess
import sys
import time
import threading

def run_command(command):
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True)
        print(f'Запустился процесс: {command}')

        def log_output(stream, prefix):
            for line in stream:
                print(f'{prefix}: {line.strip()}')
        
        threading.Thread(target=log_output, args=(process.stdout, 'stdout')).start()
        threading.Thread(target=log_output, args=(process.stderr, 'stderr')).start()

        return process
    except Exception as e:
        print(f'Ошибка при запуске команды {command}: {e}')
        return None

def restart_process(command, process_name):
    while True:
        print(f'Запуск {process_name}')
        process = run_command(command)

        if process:
            process.wait()
            print(f'{process_name} завершился. Перезапуск через 5 секунд')
            time.sleep(5)
        else:
            print(f"Не удалось запустить {process_name}. Повторная попытка через 5 секунд...")
            time.sleep(5)

if __name__ == '__main__':
    threading.Thread(target=restart_process, args=("python manage.py runserver 0.0.0.0:8000", "Django")).start()
    threading.Thread(target=restart_process, args=("python tg_bot_for_all.py", "Bot for All")).start()
    threading.Thread(target=restart_process, args=("python tg_bot_for_staff.py", "Bot for Staff")).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Завершение работы")
        for process in processes:
            process.terminate()
        sys.exit(0)
