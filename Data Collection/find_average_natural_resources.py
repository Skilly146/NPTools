import json
f = open("../game_data/gamma_merak.json")
payload = json.load(f)

all_resources = []
unique_resources = []
for star in payload:
    all_resources.append(payload[star]['nr'])
    if payload[star]['nr'] not in unique_resources:
        unique_resources.append(payload[star]['nr'])

all_resources.sort()
total_nr = 0
total_stars = len(payload)
amount_of_each_nr = [0 for i in range(len(unique_resources))]
for num in all_resources:
    amount_of_each_nr[num - 1] += 1
    total_nr += num
for i, amount in enumerate(amount_of_each_nr):
    print(i + 1, (amount/total_stars)*100)

for i, amount in enumerate(amount_of_each_nr):
    print(i + 1, amount)
