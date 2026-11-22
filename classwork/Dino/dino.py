import os
import time
import random

import numpy as np
from playwright.sync_api import sync_playwright

GAME_URL = "https://wayou.github.io/t-rex-runner/"

EPISODES = 1000
ALPHA = 0.05
GAMMA = 0.9
EPSILON = 0.1
STEP_DELAY = 0.05
MAX_STEPS = 150000
MODEL_FILE = "q_table.npy"

# ВАЖНО: Для первого запуска поставь TRAIN_MODE = True и LOAD_MODEL = False
TRAIN_MODE = True
LOAD_MODEL = True
SAVE_MODEL = True

# Таблица теперь создается динамически, чтобы избежать ошибок со старыми файлами
q_table = {} 

def get_q(state):
    # Если состояние новое, создаем для него три нуля (три действия)
    if state not in q_table:
        q_table[state] = [0.0, 0.0, 0.0]
    return q_table[state]

def load_q_table():
    global q_table
    if LOAD_MODEL and os.path.exists(MODEL_FILE):
        try:
            loaded = np.load(MODEL_FILE, allow_pickle=True).item()
            # Проверяем, что старая таблица совместима (в ней должно быть 3 действия)
            if isinstance(loaded, dict) and len(list(loaded.values())[0]) == 3:
                q_table = loaded
                print("Загружена сохранённая Q-таблица.")
            else:
                print("Старая таблица несовместима. Создаём новую.")
        except Exception:
            print("Ошибка загрузки. Создаём новую таблицу.")
    else:
        print("Q-таблица создана с нуля.")


def save_q_table():
    if SAVE_MODEL:
        np.save(MODEL_FILE, q_table)
        print(f"Q-таблица сохранена в файл {MODEL_FILE}")

def get_state(page):
    try:
        result = page.evaluate(
            """
            () => {
                const runner = window.Runner?.instance_;
                if (!runner) return { status: "NO_RUNNER" };
                if (runner.crashed) return { status: "DEAD" };
                if (!runner.playing) return { status: "NOT_PLAYING" };

                const dino = runner.tRex;
                const obstacles = runner.horizon?.obstacles || [];

                if (obstacles.length === 0) {
                    return { status: "OK", distance: 1000, is_bird: 0 };
                }

                const obstacle = obstacles[0];
                const distance = obstacle.xPos - dino.xPos;
                
                // Проверяем, является ли препятствие птицей
                const typeStr = String(obstacle.type || "");
                const is_bird = typeStr.includes("PTERODACTYL") ? 1 : 0;

                return {
                    status: "OK",
                    distance: distance,
                    is_bird: is_bird
                };
            }
            """
        )

        status = result["status"]
        if status != "OK":
            return -1, status

        distance = result["distance"]
        is_bird = result["is_bird"]

        # Определяем состояние по расстоянию
        if distance > 150:
            state = 0
        elif distance > 70:
            state = 1
        else:
            state = 2

        # Если это птица, прибавляем 10 к номеру состояния, чтобы динозавр их различал
        if is_bird == 1:
            state += 10

        return state, f"distance={distance:.1f}, bird={is_bird}"

    except Exception as error:
        return -1, f"ERROR: {error}"

def choose_action(state):
    # Выбор из трех действий: 0, 1 или 2
    if TRAIN_MODE and random.random() < EPSILON:
        return random.choice([0, 1, 2])

    return int(np.argmax(get_q(state)))

def update_q_table(state, action, reward, next_state):
    current_q = get_q(state)[action]

    if next_state == -1:
        max_next_q = 0
    else:
        max_next_q = max(get_q(next_state))

    new_q = current_q + ALPHA * (
        reward + GAMMA * max_next_q - current_q
    )

    get_q(state)[action] = new_q

def start_game(page):
    page.keyboard.up("ArrowDown") # Отпускаем клавишу вниз на всякий случай
    canvas = page.locator("canvas")
    canvas.click()
    time.sleep(0.3)
    page.keyboard.press("Space")
    time.sleep(1.0)
    state, info = get_state(page)
    return state, info

def print_q_table():
    print("\nИтоговая Q-таблица:")
    print("Действия: [0=Ничего, 1=Прыжок, 2=Присесть]")
    for state, values in sorted(q_table.items()):
        best_action = int(np.argmax(values))
        action_name = ["НИЧЕГО", "ПРЫЖОК", "ПРИСЕСТЬ"][best_action]
        print(f"Состояние {state}: [{values[0]:.2f}, {values[1]:.2f}, {values[2]:.2f}] -> Лучшее: {action_name}")

def main():
    print("Запускаем программу...")
    load_q_table()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=False,
            args=["--disable-gpu", "--disable-extensions"]
        )

        page = browser.new_page(viewport={"width": 800, "height": 600})
        print("Открываем игру...")
        page.goto(GAME_URL, wait_until="networkidle")
        time.sleep(2.5)

        for episode in range(1, EPISODES + 1):
            print(f"\n--- Игра №{episode} ---")
            
            # Флаг, чтобы не зажимать клавишу вниз много раз подряд
            is_ducking = False 

            state, info = start_game(page)
            if state == -1:
                print(f"Игра не запустилась. Причина: {info}")
                page.reload(wait_until="networkidle")
                time.sleep(2.5)
                continue
            
            total_reward = 0

            for step in range(1, MAX_STEPS + 1):
                action = choose_action(state)
                
                # Выполняем действие
                if action == 1:
                    # Если приседаем, сначала нужно встать
                    if is_ducking:
                        page.keyboard.up("ArrowDown")
                        is_ducking = False
                    page.keyboard.press("Space")
                elif action == 2:
                    # Зажимаем клавишу вниз
                    if not is_ducking:
                        page.keyboard.down("ArrowDown")
                        is_ducking = True
                else:
                    # Если ничего не делаем, но сидим — встаем
                    if is_ducking:
                        page.keyboard.up("ArrowDown")
                        is_ducking = False

                time.sleep(STEP_DELAY)
                next_state, info = get_state(page)

                if next_state == -1:
                    reward = -100
                else:
                    reward = 1

                if TRAIN_MODE:
                    update_q_table(state, action, reward, next_state)

                total_reward += reward
                state = next_state

                if next_state == -1:
                    if is_ducking:
                        page.keyboard.up("ArrowDown")
                        is_ducking = False
                    print(f"Игра окончена. Шагов: {step}. Награда: {total_reward}. Причина: {info}")
                    break

            else:
                if is_ducking:
                    page.keyboard.up("ArrowDown")
                    is_ducking = False
                print(f"Достигнут лимит шагов: {MAX_STEPS}. Награда: {total_reward}")

            if TRAIN_MODE and episode % 10 == 0:
                save_q_table()

            time.sleep(1.0)

        print("\nОБУЧЕНИЕ ЗАВЕРШЕНО!")
        print_q_table()
        
        if TRAIN_MODE:
            save_q_table()

        input("\nНажми Enter, чтобы закрыть браузер...")
        browser.close()

if __name__ == "__main__":
    main()