from state_store import StateStore

store = StateStore()

truck_id = input("Enter truck ID: ")
temperature = float(input("Enter temperature: "))

state = store.load(truck_id)

total = state["total"]
count = state["count"]

total += temperature
count += 1

average = total / count

store.save(truck_id, total, count)

print("\nUpdated State")
print("Truck ID:", truck_id)
print("Total:", total)
print("Count:", count)
print("Average:", round(average, 2))

store.close()