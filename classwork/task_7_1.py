import sched, time

s = sched.scheduler(time.time, time.sleep)
start = time.time()

def say(text):
    print(f"{time.time() - start:5.2f} c | {text}")

s.enter(2, 1, say, ("событие A (задержка 2, приоритет 1)",))
s.enter(1, 0, say, ("событие B (задержка 1, приоритет 0)",))
s.enter(2, 0, say, ("событие C (задержка 2, приоритет 0)",))
s.enter(3, 2, say, ("событие D (задержка 3, приоритет 2)",))
s.enter(1, 1, say, ("событие E (задержка 1, приоритет 1)",))
s.enterabs(start + 3, 0, say, ("событие F (enterabs: start+3)",))

print("Размер очереди до run():", len(s.queue))
s.run()
print("Очередь пуста после run():", s.empty())