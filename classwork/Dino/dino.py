import os
import time
import random

import numpy as np
from playwright.sync_api import sync_playwright

GAME_URL = "https://wayou.github.io/t-rex-runner/"

EPISODES = 150
ALPHA = 0.1
GAMMA = 0.9
EPSILON = 0.1
STEP_DELAY = 0.05
MAX_STEPS = 1500
MODEL_FILE = "q_table.npy"
TRAIN_MODE = True
LOAD_MODEL = True
SAVE_MODEL = True

q_table = {
    0: [0.0, 0.0],
    1: [0.0, 0.0],
    2: [0.0, 0.0],
}

def load_q_table():
    global q_table
    if LOAD_MODEL and os.path.exists(MODEL_FILE):
        q_table = np.load(MODEL_FILE, allow_pickle=True).item()
        print("Загружена сохранённая Q-таблица.")
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
                if (!runner) {
                    return {
                        status: "NO_RUNNER"
                    };
                }

                if (runner.crashed) {
                    return {
                        status: "DEAD"
                    };
                }

                if (!runner.playing) {
                    return {
                        status: "NOT_PLAYING"
                    };
                }

                const dino = runner.tRex;

                const obstacles = runner.horizon?.obstacles || [];

                if (obstacles.length === 0) {
                    return {
                        status: "OK",
                        distance: 1000
                    };
                }

                const obstacle = obstacles[0];

                const distance = obstacle.xPos - dino.xPos;

                return {
                    status: "OK",
                    distance: distance
                };
            }
            """
        )

        status = result["status"]

        if status != "OK":
            return -1, status

        distance = result["distance"]

        if distance > 150:
            state = 0
        elif distance > 70:
            state = 1
        else:
            state = 2

        return state, f"distance={distance:.1f}"

    except Exception as error:
        return -1, f"ERROR: {error}"

def choose_action(state):
    if TRAIN_MODE and random.random() < EPSILON:
        return random.choice([0, 1])

    return int(np.argmax(q_table[state]))

def update_q_table(state, action, reward, next_state):
    current_q = q_table[state][action]

    if next_state == -1:
        max_next_q = 0
    else:
        max_next_q = max(q_table[next_state])

    new_q = current_q + ALPHA * (
        reward + GAMMA * max_next_q - current_q
    )

    q_table[state][action] = new_q

def start_game(page):
    canvas = page.locator("canvas")
    canvas.click()
    time.sleep(0.3)
    page.keyboard.press("Space")
    time.sleep(1.0)
    state, info = get_state(page)
    return state, info

def print_q_table():
    print("\nИтоговая Q-таблица:")
    print("Состояния: 0=Далеко, 1=Средне, 2=Близко")
    print("Действия: [0=Не прыгать, 1=Прыгать]")

    for state, values in q_table.items():
        best_action = int(np.argmax(values))

        if best_action == 0:
            action_name = "НЕ ПРЫГАТЬ"
        else:
            action_name = "ПРЫГАТЬ"

        print(
            f"Состояние {state}: "
            f"[{values[0]:.2f}, {values[1]:.2f}] "
            f"-> Лучшее действие: {action_name}"
        )

def main():
    print("Запускаем программу...")
    load_q_table()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chromium",
            headless=False,
            args=[
                "--disable-gpu",
                "--disable-extensions",
            ]
        )

        page = browser.new_page(
            viewport={
                "width": 800,
                "height": 600
            }
        )

        print("Открываем игру...")
        page.goto(GAME_URL, wait_until="networkidle")

        print("Ждём загрузку игры...")
        time.sleep(2.5)

        for episode in range(1, EPISODES + 1):
            print(f"\n--- Игра №{episode} ---")

            state, info = start_game(page)

            if state == -1:
                print(f"Игра не запустилась. Причина: {info}")
                print("Перезагружаем страницу...")

                page.reload(wait_until="networkidle")
                time.sleep(2.5)

                continue
            total_reward = 0

            for step in range(1, MAX_STEPS + 1):
                action = choose_action(state)
                if action == 1:
                    page.keyboard.press("Space")
                time.sleep(STEP_DELAY)

                next_state, info = get_state(page)

                if next_state == -1:
                    reward = -100
                else:
                    reward = 1

                if TRAIN_MODE:
                    update_q_table(
                        state=state,
                        action=action,
                        reward=reward,
                        next_state=next_state
                    )

                total_reward += reward

                state = next_state

                if next_state == -1:
                    print(
                        f"Игра окончена. "
                        f"Шагов: {step}. "
                        f"Награда: {total_reward}. "
                        f"Причина: {info}"
                    )
                    break

            else:
                print(
                    f"Достигнут лимит шагов: {MAX_STEPS}. "
                    f"Награда: {total_reward}"
                )

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